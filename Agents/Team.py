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
import matplotlib.pyplot as plt
from multiprocessing import Semaphore

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Library.replay_buffer import ReplayBuffer
from Library.learner_utils import backprop,calc_q_vals_buffer, collate_batch

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
    LEARNING_RATE = 1e-4
    MAX_GRAD = 5
    training_step = 0
   
    NUMBER_OF_SAMPLES = 26
    BURN_IN_TIME_STEPS = 5 #Number of time steps to unroll GRU for during training
    BOOTSTRAP_TIME_STEPS = 6 #Number of time steps to build target Q-values for during training
    TRAINING_TIME_STEPS = 4 #Number of time steps to train on during each training iteration
    SAMPLE_SIZE = BURN_IN_TIME_STEPS + BOOTSTRAP_TIME_STEPS + TRAINING_TIME_STEPS
    DISCOUNT_FACTOR = 0.99
    
    if training:
        model = QMIX(OBS_DIM,STATE_DIM,N_AGENTS,N_ACTIONS)
        target_model = QMIX(OBS_DIM,STATE_DIM,N_AGENTS,N_ACTIONS)
        target_agent_net = target_model.agent_net
        target_mixer_net = target_model.mixer
        agent_net = model.agent_net
        mixer_net = model.mixer
        plt.ion()
        losses = []
        barrier = mp.Barrier(N_AGENTS + 1) # +1 for main process
        Debug_semaphore = Semaphore(1) #CAN REMOVE LATER
        replay_buffer = ReplayBuffer(num_of_episodes=1000)
        
    else:
        
        agent_net = RecurrentAgentNetwork(OBS_DIM, HIDDEN_DIM, N_ACTIONS) #Load network from file
        state_dict = torch.load(WEIGHTS_PATH, map_location="cpu")
        agent_net.load_state_dict(state_dict)
        agent_net.eval()
    
    
    agent_net.share_memory()
    #torch.save(model.agent_net.state_dict(), WEIGHTS_PATH) #After training complete

    processes = []
    queue = mp.Queue()

  
        
    
      
    for i in range(N_AGENTS):
        p = mp.Process(target=run_agent, args=(i,agent_net,queue,barrier,training,N_ACTIONS,Epsilon,Debug_semaphore if training else None)) #CAN REMOVE BARRIER LATER
        #p = mp.Process(target=run_DummyAgent, args=())
        p.start()
        processes.append(p)
        time.sleep(3) #Need this to avoid race condition

    
    
    while training:
        barrier.wait() # Wait for all agents to finish episode
        

        if training_step % 20 == 0:
            target_mixer_net.load_state_dict(mixer_net.state_dict())
            target_agent_net.load_state_dict(agent_net.state_dict())

        # Get episode data from queue and store in replay buffer
        for i in range(N_AGENTS):
            sub_episode = queue.get()
            replay_buffer.extend_episode(sub_episode)
        replay_buffer.end_episode()
        batch = replay_buffer.get_batch(num_of_samples=NUMBER_OF_SAMPLES, sample_size=SAMPLE_SIZE, extra_steps=BOOTSTRAP_TIME_STEPS) #Get batch of transitions for training
        # Collate batch of transitions into tensors for training
        
        # Collate batch of transitions into tensors for training
        obs, states, actions, rewards , done = collate_batch(batch)


        rewards = rewards[:, :, 0] # Shared reward for all agents, take reward of first agent in each transition
        #Train model here using batch of transitions

        
        
        q_vals_buffer = calc_q_vals_buffer(agent_net, obs, len(batch), N_AGENTS, SAMPLE_SIZE-BOOTSTRAP_TIME_STEPS) #Compute Q-values for all time steps in sample (including burn-in) of online network
        with torch.no_grad(): 
            target_q_vals_buffer = calc_q_vals_buffer(target_agent_net, obs, len(batch), N_AGENTS, SAMPLE_SIZE) #Compute target Q-values for all time steps in sample (including burn-in and bootstrap time steps) of target network

        TD_target_buffer = torch.zeros(TRAINING_TIME_STEPS, NUMBER_OF_SAMPLES, device=obs.device)
        Q_tot_buffer = torch.zeros(TRAINING_TIME_STEPS, NUMBER_OF_SAMPLES, device=obs.device)
        
        for t in range(BURN_IN_TIME_STEPS, BURN_IN_TIME_STEPS + TRAINING_TIME_STEPS ): #Build TD target per time step for training time steps, also compute Q_tot for online network for training time steps
            
            Future_reward = torch.zeros(NUMBER_OF_SAMPLES, device=obs.device)
            mask = torch.ones(NUMBER_OF_SAMPLES, device=obs.device)

            with torch.no_grad(): # Compute target Q-values for training time steps using rewards and target network Q-values for bootstrap time steps
                mask = (done.cumsum(dim=0) <= 1).float()

                for i in range(0, BOOTSTRAP_TIME_STEPS):
                    Future_reward += (DISCOUNT_FACTOR ** (i)) * rewards[t+i] * mask[t+i] # Compute discounted future reward for bootstrap time steps, only use reward of first agent in each transition since shared reward setting
                    

                agent_qs_target,_ = torch.max(target_q_vals_buffer[t+BOOTSTRAP_TIME_STEPS], dim=-1) #Greedy action selection for bootstrap time steps using target network Q-values
                q_tot_target = target_mixer_net(agent_qs_target, states[t+BOOTSTRAP_TIME_STEPS]).squeeze() # Get target Q-values for bootstrap time steps
                y_t = Future_reward + q_tot_target*mask[t+BOOTSTRAP_TIME_STEPS] # Compute target Q-values using rewards and discounted future Q-values
                TD_target_buffer[t-BURN_IN_TIME_STEPS] = y_t  # Add TD target to buffer for training time steps

            chosen_q = torch.gather(q_vals_buffer[t], dim=2, index=actions[t].unsqueeze(-1)).squeeze(-1)
            Q_tot_buffer[t-BURN_IN_TIME_STEPS] = mixer_net(chosen_q, states[t]).squeeze()

        loss = F.mse_loss(TD_target_buffer, Q_tot_buffer)
        losses.append(loss.item())

        if training_step % 10 == 0:
            plt.clf()
            plt.plot(losses)
            plt.savefig("loss.png")


        optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
        backprop(model, optimizer, loss, max_grad_norm=MAX_GRAD)

        if Epsilon > epsilon_min:
            Epsilon -= decay_rate
        barrier.wait() # Signal agents to start next episode

        training_step += 1
        
    plt.ioff()
    plt.show()

    for p in processes:
        p.join() #Wait for all processes to finish before exiting main

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    main()