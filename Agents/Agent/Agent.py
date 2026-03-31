#!/usr/bin/env python3
import hfo
import itertools
import random
import torch
from pathlib import Path
import argparse
import sys
from pathlib import Path

AGENTS_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(AGENTS_DIR))

from Qmix.Qmix_base import RecurrentAgentNetwork


PROJECT_ROOT = Path(__file__).resolve().parents[2]

HFO_ROOT = PROJECT_ROOT / "HFO"
FORMATIONS_PATH = HFO_ROOT / "bin/teams/base/config/formations-dt"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-id", type=int, required=True)
    parser.add_argument("--weights-path", type=str, required=True)
    parser.add_argument("--obs-dim", type=int, required=True)
    parser.add_argument("--n-actions", type=int, required=True)
    
    return parser.parse_args()

def main():
    args = parse_args()

    hidden_dim = 64      # samma som i träningen

    agent_net = RecurrentAgentNetwork(args.obs_dim, hidden_dim, args.n_actions)
   
    if args.weight_path != None:
        state_dict = torch.load(args.weights_path, map_location="cpu")
        agent_net.load_state_dict(state_dict)
        agent_net.eval()

    else:
        print("Läs ifrån pipe eller shared memmory")

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