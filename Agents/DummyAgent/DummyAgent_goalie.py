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

def run_Goalie(Debug_barrier=None):

    env = hfo.HFOEnvironment()
    env.connectToServer(
        hfo.HIGH_LEVEL_FEATURE_SET, 
        str(FORMATIONS_PATH), 
        6000, 
        'localhost', 
        'base_right', 
        True
    )
    

    my_unum = env.getUnum()
    teammate_unums = [u for u in range(1, 12) if u != my_unum]
    passed = False
    min_dist = 0
    distance = 99
    
    for episode in itertools.count():
        status = hfo.IN_GAME
   
        while status == hfo.IN_GAME:
            state = env.getState()
            
            env.act(hfo.REORIENT)
            
            status = env.step()
            

        if status == hfo.SERVER_DOWN:
            env.act(hfo.QUIT)
            break

if __name__ == "__main__":
    run_Goalie()