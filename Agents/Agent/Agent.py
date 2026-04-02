#!/usr/bin/env python3
import hfo
import itertools
import random
import torch
from pathlib import Path
import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from Agents.Qmix.Qmix_base import RecurrentAgentNetwork
from Library.ReplayBuffer import Episode




HFO_ROOT = PROJECT_ROOT / "HFO"
FORMATIONS_PATH = HFO_ROOT / "bin/teams/base/config/formations-dt"

def acting(action_choice, teammate_uni_nr, opponent_uni_nr, env: hfo.HFOEnvironment):
    if action_choice == 0:
        env.act(hfo.MOVE)




def run_agent(agent_id,agent_network,queue,barrier,obs_dim,n_actions,Unums):
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
    
 
    for episode in itertools.count():
        status = hfo.IN_GAME
        t = 0
        hidden = agent_network.init_hidden(batch_agents=1, device="cpu")

        while status == hfo.IN_GAME:
            obs = env.getState()
            obs_tensor = torch.as_tensor(obs, dtype=torch.float32).unsqueeze(0)
            
            if t == 30:
                print("pause")
            
            with torch.no_grad():
                print(obs_tensor.shape)
                print(hidden.shape)
                q_values, hidden = agent_network(obs_tensor, hidden)
                action_idx = torch.argmax(q_values, dim=1) #Fixa så att action val och agent val är olika
            
            status = env.step()
            transitions.save_transition(obs,action_idx,0,t,agent_id,False)
            t = t+1

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