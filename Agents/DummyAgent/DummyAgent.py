#!/usr/bin/env python3
import sys
import hfo
import itertools
import random
import torch
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

HFO_ROOT = PROJECT_ROOT / "HFO"
FORMATIONS_PATH = HFO_ROOT / "bin/teams/base/config/formations-dt"

def run_DummyAgent(Debug_barrier=None):

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
    pause = False
  
    
    for episode in itertools.count():
        status = hfo.IN_GAME
        t = 0
        c = 0
        while status == hfo.IN_GAME:
            state = env.getState()
          
            

            

            if my_unum == 11:
                env.act(hfo.REORIENT)
                
            
            else:
                if state[5] != 1: # Check if any opponent is in marking range
                    env.act(hfo.GO_TO_BALL)
                    print("Moving to ball") #Debug print
                else:
                    if state[15] != -2: # Check if in possession of the ball
                        if c < 10:
                            env.act(hfo.PASS, state[15])
                            c += 1
                        else:
                            env.act(hfo.DRIBBLE)
                            c=0
                        print(f"Passing to {state[15]}") #Debug print


                    else:
                        env.act(hfo.DRIBBLE)
                        print("Dribbling") #Debug print
                        
            
            
            
            status = env.step()
            t += 1

        print(f"Episode {episode} ended with {env.statusToString(status)}")

        if status == hfo.SERVER_DOWN:
            env.act(hfo.QUIT)
            break

if __name__ == "__main__":
    run_DummyAgent()