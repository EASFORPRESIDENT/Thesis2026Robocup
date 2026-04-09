import os
import sys
import hfo
import itertools
import random
import torch
from pathlib import Path
from Qmix.Qmix_base import QMIX,RecurrentAgentNetwork
import torch.multiprocessing as mp
import torch.nn.functional as F
import time
import argparse
from Agent.Agent import run_agent
from DummyAgent.DummyAgent import run_DummyAgent

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Library.replay_buffer import ReplayBuffer
from Library.learner_utils import backprop, collate_batch

def parse_args():
    parser = argparse.ArgumentParser(description="Team controller")

    parser.add_argument("--n-O_agents", type=int, default=2,
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
    N_ACTIONS = 7 + (args.n_O_agents-1) + (args.n_D_agents) 
    HIDDEN_DIM = 64
    WEIGHTS_PATH = PROJECT_ROOT / f"Agents/Agent/{args.n_O_agents}v{args.n_D_agents}.pt"

    training = args.Training
    Epsilon = 1.0 #Start value for epsilon-greedy action selection
    epsilon_min = 0.05
    decay_rate = 1e-4
   
    NUMBER_OF_SAMPLES = 32
    BURN_IN_TIME_STEPS = 5 #Number of time steps to unroll GRU for during training
    BOOTSTRAP_TIME_STEPS = 2 #Number of time steps to build target Q-values for during training
    TRAINING_TIME_STEPS = 4 #Number of time steps to train on during each training iteration
    SAMPLE_SIZE = BURN_IN_TIME_STEPS + BOOTSTRAP_TIME_STEPS + TRAINING_TIME_STEPS
    DISCOUNT_FACTOR = 0.99
    
    if args.Training == True:
        model = QMIX(OBS_DIM,STATE_DIM,N_AGENTS,N_ACTIONS)
        agent_net = model.agent_net
        mixer_net = model.mixer
        
    else:
        
        agent_net = RecurrentAgentNetwork(OBS_DIM, HIDDEN_DIM, N_ACTIONS) #Load network from file
        state_dict = torch.load(WEIGHTS_PATH, map_location="cpu")
        agent_net.load_state_dict(state_dict)
        agent_net.eval()
    
    
    agent_net.share_memory()
    #torch.save(model.agent_net.state_dict(), WEIGHTS_PATH) #After training complete

    processes = []
    queue = mp.Queue()

    if training:
        barrier = mp.Barrier(N_AGENTS + 1) # +1 for main process
        Debug_barrier = mp.Barrier(N_AGENTS) #CAN REMOVE LATER
        replay_buffer = ReplayBuffer(num_of_episodes=1000)
    

    for i in range(N_AGENTS):
        p = mp.Process(target=run_agent, args=(i,agent_net,queue,barrier,training,N_ACTIONS,Epsilon,Debug_barrier if training else None)) #CAN REMOVE BARRIER LATER
        #p = mp.Process(target=run_DummyAgent, args=())
        p.start()
        processes.append(p)
        time.sleep(3) #Need this to avoid race condition

       
    
    while training:
        barrier.wait() # Wait for all agents to finish episode

        # Get episode data from queue and store in replay buffer
        for i in range(N_AGENTS):
            sub_episode = queue.get()
            replay_buffer.extend_episode(sub_episode)
        replay_buffer.end_episode()
        batch = replay_buffer.get_batch(num_of_samples=NUMBER_OF_SAMPLES, sample_size=SAMPLE_SIZE, extra_steps=BOOTSTRAP_TIME_STEPS) #Get batch of transitions for training
        
        # Collate batch of transitions into tensors for training
        obs, states, actions, rewards , done = collate_batch(batch)


        rewards = rewards[:, :, 0] # Shared reward for all agents, take reward of first agent in each transition
        #Train model here using batch of transitions
        print("Action batch shape:", actions.shape)
        #BURN IN TIME STEPS: Unroll GRU for burn-in time steps to get hidden state
        with torch.no_grad():
            hidden = agent_net.init_hidden(len(batch) * N_AGENTS, device=obs.device)
            q_vals_buffer = []

            for t in range(SAMPLE_SIZE):
                obs_flat = obs[t].reshape(len(batch) * N_AGENTS, -1)
                q_values, hidden = agent_net(obs_flat, hidden)
                q_values = q_values.reshape(len(batch), N_AGENTS, -1)
                q_vals_buffer.append(q_values)

            TD_target_buffer = torch.zeros(TRAINING_TIME_STEPS, NUMBER_OF_SAMPLES, device=obs.device)
            Q_tot_buffer = torch.zeros(TRAINING_TIME_STEPS, NUMBER_OF_SAMPLES, device=obs.device)
            
            for t in range(BURN_IN_TIME_STEPS, BURN_IN_TIME_STEPS + TRAINING_TIME_STEPS ):
              
                Future_reward = torch.zeros(NUMBER_OF_SAMPLES, device=obs.device)
                mask = torch.ones(NUMBER_OF_SAMPLES, device=obs.device)
                
                for i in range(0, BOOTSTRAP_TIME_STEPS):
                    Future_reward += (DISCOUNT_FACTOR ** (i)) * rewards[t+i,1] * mask[t+i] # Compute discounted future reward for bootstrap time steps, only use reward of first agent in each transition since shared reward setting
                    mask = (done.cumsum(dim=0) <= 1).float()

                agent_qs,_ = torch.max(q_vals_buffer[t+BOOTSTRAP_TIME_STEPS], dim=-1)
                q_tot = mixer_net(agent_qs, states[t+BOOTSTRAP_TIME_STEPS]).squeeze() # Get target Q-values for bootstrap time steps
                y_t = Future_reward + q_tot*mask[t+BOOTSTRAP_TIME_STEPS] # Compute target Q-values using rewards and discounted future Q-values
                TD_target_buffer[t-BURN_IN_TIME_STEPS] = y_t  # Compute TD target for training time steps

                chosen_q = torch.gather(q_vals_buffer[t], dim=2, index=actions[t].unsqueeze(-1)).squeeze(-1)
              
                Q_tot_buffer[t-BURN_IN_TIME_STEPS] = mixer_net(chosen_q, states[t]).squeeze()

            print("TD target buffer shape:", TD_target_buffer.shape , "Q tot buffer shape:", Q_tot_buffer.shape)
            TD_mean_per_time_step = TD_target_buffer.mean(dim=0)
            Q_tot_mean_per_time_step = Q_tot_buffer.mean(dim=0)
            print("TD mean per time step shape:", TD_mean_per_time_step.shape, "Q tot mean per time step shape:", Q_tot_mean_per_time_step.shape)
            loss = F.mse_loss(Q_tot_mean_per_time_step, TD_mean_per_time_step)
            print("Loss:", loss.item())

            optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)
            backprop(model, optimizer, loss, max_grad_norm=10)
        
            
        

        if Epsilon > epsilon_min:
            Epsilon -= decay_rate
        barrier.wait() # Signal agents to start next episode
        


    for p in processes:
        p.join() #Wait for all processes to finish before exiting main

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    main()