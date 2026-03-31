#!/usr/bin/env python3
import hfo
import itertools
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
HFO_ROOT = PROJECT_ROOT / "HFO"
FORMATIONS_PATH = HFO_ROOT / "bin/teams/base/config/formations-dt"

def main():
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

            if state[5] == 1:
                while(1):
                    print("Nothing")
                    pass
            else:
                env.act(hfo.MOVE)
            
            
            status = env.step()

        print(f"Episode {episode} ended with {env.statusToString(status)}")

        if status == hfo.SERVER_DOWN:
            env.act(hfo.QUIT)
            break

if __name__ == "__main__":
    main()