import os
import sys
import hfo
import itertools
import random
import torch
from pathlib import Path
from Qmix.Qmix_base import QMIX,RecurrentAgentNetwork
import torch.multiprocessing as mp
import time
import argparse
from Agent.Agent import run_agent

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from Library.replay_buffer import ReplayBuffer

def parse_args():
    parser = argparse.ArgumentParser(description="Team controller")

    parser.add_argument("--n-O_agents", type=int, default=1,
                        help="Number of offensive agents")
    
    parser.add_argument("--n-D_agents", type=int, default=1,
                        help="Number of defensive agents")
    
    parser.add_argument("--Training", type=bool, default=True,
                        help="Set to True if you want to train a model")

    #parser.add_argument("--port", type=int, default=6000, help="HFO server port")

    #parser.add_argument("--headless", action="store_true", help="Run HFO in headless mode")

    return parser.parse_args()


def main():
    args = parse_args()
    OBS_DIM = 10 + 6*(args.n_O_agents-1) + 3*args.n_D_agents + 2
    STATE_DIM = OBS_DIM*args.n_O_agents #kolla upp om kan använda motståndare obs också
    N_AGENTS = args.n_O_agents
    N_ACTIONS = 10 + (args.n_O_agents-1) + (args.n_D_agents) 
    HIDDEN_DIM = 64
    WEIGHTS_PATH = PROJECT_ROOT / f"Agents/Agent/{args.n_O_agents}v{args.n_D_agents}.pt"
    Unums = torch.empty(N_AGENTS, dtype=torch.int16)
    training = args.Training

    if args.Training == True:
        model = QMIX(OBS_DIM,STATE_DIM,N_AGENTS,N_ACTIONS)
        agent_net = model.agent_net
    else:
        agent_net = RecurrentAgentNetwork(OBS_DIM, HIDDEN_DIM, N_ACTIONS) #Load network from file
        state_dict = torch.load(WEIGHTS_PATH, map_location="cpu")
        agent_net.load_state_dict(state_dict)
        agent_net.eval()
    
    Unums.share_memory_()
    agent_net.share_memory()
    #torch.save(model.agent_net.state_dict(), WEIGHTS_PATH) #After training complete

    processes = []
    queue = mp.Queue()

    if training:
        barrier = mp.Barrier(N_AGENTS + 1) # +1 for main process
    

    for i in range(N_AGENTS):
        p = mp.Process(target=run_agent, args=(i,agent_net,queue,barrier,training,N_ACTIONS,Unums))
        p.start()
        processes.append(p)
        time.sleep(3) #Need this to avoid race condition

    

    if training:
        replay_buffer = ReplayBuffer(num_of_episodes=1000)
    
        while training:
            barrier.wait() # Wait for all agents to finish episode
            for i in range(N_AGENTS):
                sub_episode = queue.get()
                replay_buffer.extend_episode(sub_episode)
            replay_buffer.end_episode()
            batch = replay_buffer.get_batch(num_of_samples=32, sample_size=10) #Get batch of transitions for training
            
            #Train model here using batch of transitions

            barrier.wait() # Signal agents to start next episode


    for p in processes:
        p.join() #Wait for all processes to finish before exiting main

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    main()