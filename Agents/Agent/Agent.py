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

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from Agents.Qmix.Qmix_base import RecurrentAgentNetwork
from Library.replay_buffer import Episode




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


def get_action_mask(n_actions,n_temates,n_opponents, obs : hfo.HFOEnvironment):
    action_mask = torch.ones(n_actions, dtype=torch.bool) # 10 possible actions
    temmate_pass_unums = [] # List of teammate unums for pass actions
    opponent_mark_unums = [] # List of opponent unums for mark actions

    if n_temates > 0:
        teammate_start_idx = 9 + n_temates*3 + 3
    else:
        teammate_start_idx = 9
        
        
    if n_opponents > 0:
        if n_temates > 0:
            opponent_start_idx = teammate_start_idx + n_temates*3
        else:
            opponent_start_idx = 9 + 3
   

    if obs[5] != 1: # Check if in possession of the ball
        action_mask[1] = False # Can't shoot if not in possession of the ball
        action_mask[2] = False # Can't dribble if not in possession of the ball
        action_mask[6] = False # Can't reorient if not in possession of the ball
        for i in range(1, n_temates + 1):
            action_mask[6 + i] = False # Can't pass if not in possession of the ball

    else: # Check if teammates is in passing range
            action_mask[0] = False # Can't move if in possession of the ball
            action_mask[5] = False # Can't go to ball if in possession of the ball
            for i in range(0, n_temates): # Check if more than one teammate is in passing range
                obs_index = teammate_start_idx + 3*i
                action_index = 7 + i
                if obs[obs_index] == -2: # Check each teammate's passing range
                    action_mask[action_index] = False # Can't pass to this teammate if not in passing range
                else:
                    temmate_pass_unums.append([action_index,obs[obs_index]]) # Add teammate's unum to list of passable teammates


     
    for i in range(0, n_opponents): # Check if opponents is in marking range
        obs_index = opponent_start_idx + 3*i
        action_index = 7 + n_temates + i
        if obs[obs_index] == -2: # Check each opponent's marking range
            action_mask[action_index] = False # Can't mark this opponent if not in marking range
        else:
            opponent_mark_unums.append([action_index,obs[obs_index]]) # Add opponent's unum to list of markable opponents
            

    return temmate_pass_unums, opponent_mark_unums, action_mask


def run_agent(agent_id,agent_network,queue,barrier,training : bool,n_actions,Unums,Debug_barrier=None): #CAN REMOVE DEBUG_BARRIER LATER
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
    Unums[agent_id] = my_unum
    print(f"AGENT:{agent_id} has connected, Unifrom number:{my_unum}")
    n_teammates = env.getNumTeammates()
    n_opponents = env.getNumOpponents()
    
 
    for episode in itertools.count():
        status = hfo.IN_GAME
        t = 0
        hidden = agent_network.init_hidden(batch_agents=1, device="cpu")

        while status == hfo.IN_GAME:
            obs = env.getState()
            obs_tensor = torch.as_tensor(obs, dtype=torch.float32).unsqueeze(0)
            """
            print(f"{t} :obs of agent: {agent_id} uni:{my_unum}, T1: {obs_tensor[0][18]}, T2: {obs_tensor[0][21]}, O1: {obs_tensor[0][24]}, O2: {obs_tensor[0][27]} \n") #Debug print
            if t == 20: #Debug print
                Debug_barrier.wait() #Wait untill all agents reach this point
                print(f"obs of agent: {agent_id} uni:{my_unum}, T1: {obs_tensor[0][18]}, T2: {obs_tensor[0][21]}, O1: {obs_tensor[0][24]}, O2: {obs_tensor[0][27]} \n") #Debug print
                time.sleep(1)
                print("pause")
                """
            
            with torch.no_grad():
                q_values, hidden = agent_network(obs_tensor, hidden)
                masked_q_values = q_values.clone()
                temmate_pass_unums, opponent_mark_unums,action_mask = get_action_mask(n_actions, n_teammates, n_opponents, obs)
                masked_q_values = masked_q_values.masked_fill(~action_mask.unsqueeze(0), float('-inf')) # Mask out invalid actions
                action_idx = torch.argmax(masked_q_values, dim=1) #Fixa så att action val och agent val är olika
                print(f"Agent {agent_id} chose action {action_idx.item()} with q-value {q_values[0][action_idx].item()} \n") #Debug print
                acting(action_idx ,temmate_pass_unums, opponent_mark_unums, env)

            status = env.step()
            t = t+1
            if training:
                transitions.save_transition(obs,action_idx,0,t,agent_id,False)

            
        if training:
            transitions.done()
            queue.put(transitions) #Send episode to main process for backpropagation
            barrier.wait() #Wait untill all agents finish and start backpropagation
            barrier.wait() #Wait untill backpropagation finished
            transitions.reset()
        print(f"Episode {episode} ended with {env.statusToString(status)}")

        if status == hfo.SERVER_DOWN:
            env.act(hfo.QUIT)
            break

if __name__ == "__main__":
    run_agent()