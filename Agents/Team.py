import hfo
import itertools
import random
import torch
from pathlib import Path
from Qmix.Qmix_base import QMIX
import subprocess
import sys
import time
import argparse



PROJECT_ROOT = Path(__file__).resolve().parents[1]

def parse_args():
    parser = argparse.ArgumentParser(description="Team controller")

    parser.add_argument("--n-agents", type=int, default=2,
                        help="Number of offensive agents")

    #parser.add_argument("--port", type=int, default=6000, help="HFO server port")

    #parser.add_argument("--headless", action="store_true", help="Run HFO in headless mode")

    return parser.parse_args()

def main():
    args = parse_args()
    OBS_DIM = 20 
    STATE_DIM = 50
    N_AGENTS= args.n_agents
    N_ACTIONS=8
    model = QMIX(OBS_DIM,STATE_DIM,N_AGENTS,N_ACTIONS)


    processes = []

    for i in range(N_AGENTS):
        p = subprocess.Popen([
            sys.executable,
            "Agents/Agent/Agent.py",
            "--agent-id",
            str(i)
        ])
        processes.append(p)
        time.sleep(3) #Need this to avoid race condition

    for p in processes:
        p.wait()

if __name__ == "__main__":
    main()