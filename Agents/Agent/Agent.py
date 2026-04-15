#!/usr/bin/env python3
import hfo
import itertools
import random
import torch
from pathlib import Path
import argparse
import sys
from pathlib import Path
import time
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from Agents.Qmix.Qmix_base import RecurrentAgentNetwork
from Library.replay_buffer import Episode
from Library.learner_utils import get_action_mask




HFO_ROOT = PROJECT_ROOT / "HFO"
FORMATIONS_PATH = HFO_ROOT / "bin/teams/base/config/formations-dt"

def acting(action_choice ,temmate_pass_unums, opponent_mark_unums, env: hfo.HFOEnvironment):

    if action_choice == 0:
        env.act(hfo.MOVE)

    elif action_choice == 1:
        env.act(hfo.SHOOT)

    elif action_choice == 2:
        env.act(hfo.DRIBBLE)
    
    elif action_choice == 3: 
        env.act(hfo.NOOP)
    
    elif action_choice == 4:
        env.act(hfo.REDUCE_ANGLE_TO_GOAL)
    
    elif action_choice == 5:
        env.act(hfo.GO_TO_BALL)
    
    elif action_choice == 6:
        env.act(hfo.REORIENT)

    elif action_choice > 6 and action_choice <= env.getNumTeammates() + 6:
        pass_to_unum = next((v for a, v in temmate_pass_unums if a == action_choice), None)
        env.act(hfo.PASS, pass_to_unum) 
    
    elif action_choice > 6 + env.getNumTeammates():
        mark_who_unum = next((v for a, v in opponent_mark_unums if a == action_choice), None)
        env.act(hfo.MARK_PLAYER, mark_who_unum) 
    else:
        raise ValueError(f"Invalid action choice: {action_choice}")

def select_action(q_values, epsilon):
    if random.random() < epsilon:
        action_value = torch.tensor([-float('inf')])
        while (action_value == float('-inf')): # Ensure that the random action is valid (not masked out)
            action = torch.randint(0, q_values.shape[-1], (1,))
            action_value = q_values[0][action]
        return action
    else:
        return torch.argmax(q_values, dim=-1)

def reward_func(status):
    if status == hfo.GOAL:
        return 5.0
    elif status == hfo.CAPTURED_BY_DEFENSE:
        return -4.0
    elif status == hfo.OUT_OF_BOUNDS:
        return -1.5
    elif status == hfo.OUT_OF_TIME:
        return -0.5
    else:
        return 0.0





def run_agent(
        agent_id,
        agent_network,
        queue,
        barrier,
        stop_event,
        training : bool,
        n_actions,
        Epsilon = 0,
        Eval=False, 
        Eval_interval=50,
        plotting = True
        ): #CAN REMOVE DEBUG_BARRIER LATER
    #args = parse_args()

    hidden_dim = 64      # samma som i träningen

    env = hfo.HFOEnvironment()
    env.connectToServer(
        hfo.HIGH_LEVEL_FEATURE_SET,
        str(FORMATIONS_PATH), 
        6000, 
        'localhost', 
        'base_left', 
        False
    )
    
    transitions = Episode()
    my_unum = env.getUnum()
    print(f"AGENT:{agent_id} has connected, Unifrom number:{my_unum}")
    n_teammates = env.getNumTeammates()
    n_opponents = env.getNumOpponents()
    plt.ion()
    Avrage_goals_per_eval = []
    Avrage_capture_per_eval = []
    Avrage_time_per_eval = []
    Avrage_bounds_per_eval = []
    nr_goals_per_eval = 0
    nr_capture_per_eval = 0
    nr_out_of_time_per_eval = 0
    nr_out_bounds_per_eval = 0
    Eval_episode = 0
    eval_max = 0
 
    for episode in itertools.count():
        if stop_event.is_set():
            print(f"Agent {agent_id} received stop signal. Exiting.")
            break
        status = hfo.IN_GAME
        t = 0
        hidden = agent_network.init_hidden(batch_agents=1, device="cpu")

        while status == hfo.IN_GAME:
            obs = env.getState()
            obs_tensor = torch.as_tensor(obs, dtype=torch.float32).unsqueeze(0)
            


            with torch.no_grad():
                q_values, hidden = agent_network(obs_tensor, hidden)
                masked_q_values = q_values.clone()
                temmate_pass_unums, opponent_mark_unums,action_mask = get_action_mask(n_actions, n_teammates, n_opponents, obs)
                masked_q_values = masked_q_values.masked_fill(~action_mask.unsqueeze(0), float('-inf')) # Mask out invalid actions

                if training and not Eval.value:
                    eps = Epsilon.value
                    #print(f"Episode {episode}, Epsilon {eps:.3f}") #Debug print
                    action_idx = select_action(masked_q_values, eps) # Epsilon-greedy action selection
                else:
                    action_idx = torch.argmax(masked_q_values, dim=-1) # Greedy action selection during evaluation
                    
                #print(f"Agent {agent_id} chose action {action_idx.item()} with q-value {q_values[0][action_idx].item()} \n") #Debug print
                acting(action_idx ,temmate_pass_unums, opponent_mark_unums, env)


            status = env.step()
            
            if training and not Eval.value:
                    transitions.save_transition(
                    obs,
                    int(action_idx.item()),
                    reward_func(status),
                    t,
                    agent_id,
                    False
                )
            t = t+1

        #print(f"Episode {episode} ended with {env.statusToString(status)}")
        
        if training:
            if not Eval.value:
                transitions.done()
                queue.put(transitions) #Send episode to main process for backpropagation
            barrier.wait() #Wait untill all agents finish and start backpropagation
            barrier.wait() #Wait untill backpropagation finished
            transitions.reset()
        
        if agent_id == 0 and Eval.value:
                print(f"Evaluation episode {Eval_episode} ended with {env.statusToString(status)}")
                if status == hfo.GOAL:
                    nr_goals_per_eval += 1

                elif status == hfo.OUT_OF_BOUNDS:
                    nr_out_bounds_per_eval += 1

                elif status == hfo.OUT_OF_TIME:
                    nr_out_of_time_per_eval += 1

                elif status == hfo.CAPTURED_BY_DEFENSE:
                    nr_capture_per_eval += 1

                Eval_episode += 1
        
        if Eval_episode == Eval_interval:
                    Avrage_goals_per_eval.append(nr_goals_per_eval / Eval_interval)
                    Avrage_capture_per_eval.append(nr_capture_per_eval/Eval_interval)
                    Avrage_time_per_eval.append(nr_out_of_time_per_eval/Eval_interval)
                    Avrage_bounds_per_eval.append(nr_out_bounds_per_eval/Eval_interval)

                        
                    plt.clf()
                    plt.xlabel("EVAL")
                    plt.ylabel(f"Outcome rate , (avrage over {Eval_interval} episodes)")
                    plt.plot(Avrage_goals_per_eval, label = "Goals")
                    plt.plot(Avrage_capture_per_eval, label = "Captured by defence")
                    plt.plot(Avrage_time_per_eval, label = "Time Out")
                    plt.plot(Avrage_bounds_per_eval, label = "Out Of bounds")
                    plt.legend()
                    plt.savefig("Avrage_goals_per_eval.png")

                    if training:
                        if nr_goals_per_eval / Eval_interval > eval_max:
                            torch.save(agent_network.state_dict(), WEIGHTS_PATH) 
                            eval_max = nr_goals_per_eval / Eval_interval

                
                    nr_goals_per_eval = 0
                    nr_out_of_time_per_eval = 0
                    nr_capture_per_eval = 0
                    nr_out_bounds_per_eval = 0
                    Eval_episode = 0
                    
                    if training:
                        Eval.value = False

           
        


        if status == hfo.SERVER_DOWN:
            env.act(hfo.QUIT)
            break

if __name__ == "__main__":
    run_agent()