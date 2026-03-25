#!/usr/bin/env python3
import hfo
import itertools
import random
import torch
from pathlib import Path
from Qmix_base import QMIX

PROJECT_ROOT = Path(__file__).resolve().parents[2]

HFO_ROOT = PROJECT_ROOT / "HFO"
FORMATIONS_PATH = HFO_ROOT / "bin/teams/base/config/formations-dt"

def main():

# Testing Section
    obs_dim=20 
    state_dim=50
    n_agents=5
    n_actions=8
    model = QMIX(obs_dim,state_dim,n_agents,n_actions)

    batch_size = 2 #Transitions in this case
    obs = torch.rand(batch_size,n_agents,obs_dim) 
    print(obs)

    state = torch.rand(batch_size,50)
    print(state)
    actions = torch.randint(0,n_actions,(batch_size,n_agents)) # actions taken in the batch
    print(actions)
    q_tot, all_q, chosen_q = model.forward(obs, state , actions)
    print("Q_tot = ")
    print(q_tot)
    print("All_Q = ")
    print(all_q)
    print("Choosen Q = ")
    print(chosen_q)
    # End Testing Scetion
    print(hfo.ACTION_STRINGS)

    env = hfo.HFOEnvironment()
    env.connectToServer(
        hfo.HIGH_LEVEL_FEATURE_SET, 
        str(FORMATIONS_PATH), 
        6000, 
        'localhost', 
        'base_left', 
        False
    )
    

    my_unum = env.getUnum()
    teammate_unums = [u for u in range(1, 12) if u != my_unum]
  
    
    for episode in itertools.count():
        status = hfo.IN_GAME
        while status == hfo.IN_GAME:
            state = env.getState()
            print(state.size)

            if state[5] == 1:
                if random.random() < 0.5:
                    env.act(hfo.MOVE)
                else:
                    #env.act(hfo.PASS, random.choice(teammate_unums))
                    env.act(hfo.DRIBBLE)
            else:
                env.act(hfo.MOVE)
            
            status = env.step()

        print(f"Episode {episode} ended with {env.statusToString(status)}")

        if status == hfo.SERVER_DOWN:
            env.act(hfo.QUIT)
            break

if __name__ == "__main__":
    main()