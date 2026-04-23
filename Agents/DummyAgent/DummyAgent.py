#!/usr/bin/env python3
import sys
import hfo
import itertools
import random
import torch
from pathlib import Path
import math


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
    passed = False
    min_dist = 0
    distance = 99
    
    for episode in itertools.count():
        status = hfo.IN_GAME
        t = 0
        c = 0
        while status == hfo.IN_GAME:
            state = env.getState()
          
    
            if my_unum == 11:
                env.act(hfo.REORIENT)
                
            
            else:
                if state[5] != 1: 
                    env.act(hfo.GO_TO_BALL)
                    print(f"Dist? {distance}")
                    print("Moving to ball") #Debug print
                    if passed:
                        if min_dist < distance:
                            min_dist = distance
                        print(f"Min DISTANCE {min_dist}")
                    passed = False
                else:
                    print("HAS BALL")
                    if state[15] != -2: 
                        print(f"SEE TEAMMATE {state[15]}")
                        
                        u = random.random()
                        p1 = (state[0],state[3])
                        p2 = (state[1],state[4])
                        distance = math.dist(p1,p2)
                        print(f"Player [{state[0]},{state[1]}], Ball [{state[3]},{state[4]}], distance {distance}")
                        if distance > 0.15 and distance < 1:
                            env.act(hfo.PASS, state[15])
                            passed = True
                            #env.act(hfo.SHOOT)
                            print(f"-------------------------------------------Passing to {state[15]}, Sucess? {state[19]} Stammina {state[20]}") #Debug print

                        else:
                            env.act(hfo.DRIBBLE)
                            print(f"Dribbling") #Debug print
                    

                    else:
                        u = random.random()
                        passed = False
                        print(f"Dont have ball") #Debug print
                        if u < 0.5:
                            env.act(hfo.DRIBBLE)
                            print("Dribbling") #Debug print
                        else:
                            env.act(hfo.REORIENT)
                            print("REORIENT") 
                        
            
            
            print("\n")
            status = env.step()
            t += 1

        print(f"Episode {episode} ended with {env.statusToString(status)}")

        if status == hfo.SERVER_DOWN:
            env.act(hfo.QUIT)
            break

if __name__ == "__main__":
    run_DummyAgent()