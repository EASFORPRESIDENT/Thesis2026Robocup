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

    parser.add_argument("--n-O_agents", type=int, default=2,
                        help="Number of offensive agents")
    
    parser.add_argument("--n-D_agents", type=int, default=2,
                        help="Number of defensive agents")

    #parser.add_argument("--port", type=int, default=6000, help="HFO server port")

    #parser.add_argument("--headless", action="store_true", help="Run HFO in headless mode")

    return parser.parse_args()

def main():
    args = parse_args()
    OBS_DIM = 10 + 6*(args.n_O_agents-1) + 3*args.n_D_agents
    STATE_DIM = OBS_DIM*args.n_O_agents #kolla upp om kan använda motståndare obs också
    N_AGENTS= args.n_O_agents
    N_ACTIONS= 10 + (args.n_O_agents-1)
    WEIGHTS_PATH = PROJECT_ROOT / f"Agents/Agent/{args.n_O_agents}v{args.n_D_agents}.pt"

    model = QMIX(OBS_DIM,STATE_DIM,N_AGENTS,N_ACTIONS)
    torch.save(model.agent_net.state_dict(), WEIGHTS_PATH)

    processes = []

    for i in range(N_AGENTS):
        p = subprocess.Popen([
            sys.executable,
            "Agents/Agent/Agent.py",
            "--agent-id", str(i),
            "--weights-path", str(WEIGHTS_PATH)
        ])
        processes.append(p)
        time.sleep(3) #Need this to avoid race condition

    for p in processes:
        p.wait()

if __name__ == "__main__":
    main()