import sys
import torch
from pathlib import Path
from Qmix.Qmix_base import QMIX, RecurrentAgentNetwork
import torch.multiprocessing as mp
import torch.nn.functional as F
import time
import argparse
from Agent.Agent import run_agent
from DummyAgent.DummyAgent import run_DummyAgent
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Library.replay_buffer import ReplayBuffer
import Library.learner_utils as learner_utils
import Library.file_manager as file_manager


def parse_args():
    parser = argparse.ArgumentParser(description="Team controller")

    parser.add_argument("--config", type=str, default=str(
        PROJECT_ROOT / "configs" / "base_config.json"),
        help="Path to config file")


    # parser.add_argument("--port", type=int, default=6000, help="HFO server port")
    # parser.add_argument("--headless", action="store_true", help="Run HFO in headless mode")

    return parser.parse_args()


def main():

    # =================== Hyperparameters and setup ==================

    args = parse_args()
    params = file_manager.load_params(args.config)
    obs_dim = 10 + 6*(params["n_O_agents"]-1) + 3*params["n_D_agents"] + 2
    state_dim = obs_dim*params["n_O_agents"] # kolla upp om kan använda motståndare obs också
    n_agent = params["n_O_agents"]
    n_opponents = params["n_D_agents"]
    n_actions = 7 + (params["n_O_agents"]-1) + (params["n_D_agents"]) 
    hidden_dim = 64
    weights_path = PROJECT_ROOT / "log/run_1776341363/agent_weights.pth"
    Eval_flag = mp.Value('b', False) #Flag to signal agents to start evaluation episodes
   
    

    Eval_time_steps = params["Eval_every_x_time_steps"] #Number of time steps between evaluations during training
    Eval_interval = params["Eval_interval"] #Number of episodes to average over during evaluation

    
    training = params["training"]
    epsilon = mp.Value('d', params["epsilon_start"]) # Start value for epsilon-greedy action selection
    epsilon_min = params["epsilon_min"]
    epsilon_decay = params["epsilon_decay"]
    learning_rate = params["learning_rate"]
    learning_rate_decay = params["learning_rate_decay"]
    min_learning_rate = params["min_learning_rate"]
    max_grad = params["max_grad_norm"]
    target_update_interval = params["target_update_interval"]
    training_step = 0
   
    number_of_samples = params["number_of_samples"] # Number of samples to use for each training iteration, i.e. number of time steps to sample from replay buffer for training per training iteration, set to 1 to train on one time step at a time, set to higher value to train on multiple time steps at once (e.g. 32 for batch training)
    burn_in_time_steps = params["burn_in_steps"] # Number of time steps to unroll GRU for during training
    bootstrap_time_steps = params["bootstrap_steps"] # Number of time steps to build target Q-values for during training
    training_time_steps = params["training_steps"] # Number of time steps to train on during each training iteration
    sample_size = burn_in_time_steps + bootstrap_time_steps + training_time_steps
    discount_factor = params["discount_factor"]
    
    dupe = params["duplicate_positive_episodes"]
    dup_cap = params["max_duplication"] # Cap on how much to duplicate positive reward episodes in replay buffer to prevent overfitting to them, set to a high value to disable cap
    scale = params["duplication_scale_factor"] # Scale factor for how much to duplicate positive reward episodes in replay buffer based on average goal rate, higher value means more duplication of positive reward episodes when average goal rate is low, set to 0 to disable biasing towards positive reward episodes
    logging = params["logging"]
    plotting = params["plotting"]
    duration = params.get("duration", -1)

    # ===================== End of hyperparameters and setup ==================

    if logging:
        run_dir, metrics = file_manager.init_run_logging(PROJECT_ROOT, params)


    if training:
        model = QMIX(obs_dim,state_dim,n_agent,n_actions)
        target_model = QMIX(obs_dim,state_dim,n_agent,n_actions)
        target_agent_net = target_model.agent_net
        target_mixer_net = target_model.mixer
        agent_net = model.agent_net
        mixer_net = model.mixer
        losses = []
        Q_tot_buffer_mean = []
        Q_tot_buffer_max_abs = []
        TD_target_buffer_mean = []
        Gradient_norms = []
        barrier = mp.Barrier(n_agent + 1) # +1 for main process
        replay_buffer = ReplayBuffer(num_of_episodes=1000)
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        loss_plt_start = 0
        
    else:
        agent_net = RecurrentAgentNetwork(obs_dim, hidden_dim, n_actions) #Load network from file
        state_dict = torch.load(weights_path, map_location="cpu")
        agent_net.load_state_dict(state_dict)
        agent_net.eval()
        Eval_flag.value = True

    agent_net.share_memory()
    
    

    processes = []
    queue = mp.Queue()
    stop_event = mp.Event()
    
    # Start agent processes
    for i in range(n_agent):
        p = mp.Process(target=run_agent, args=(
            i,
            agent_net,
            queue,
            barrier if training else None,
            stop_event,
            training,
            n_actions,
            epsilon,
            Eval_flag,
            Eval_interval,
            plotting if training else None,
            run_dir)) 
        # p = mp.Process(target=run_DummyAgent, args=())
        p.start()
        processes.append(p)
        time.sleep(3) # Need this to avoid race condition

    # Main training loop
    while training:
        barrier.wait() # Wait for all agents to finish episode

        

        if duration > 0 and training_step >= duration:
            training = False
            stop_event.set() # Signal agents to stop

        if Eval_flag.value == False:
        
            if training_step % 3000 == 0 and training_step > 0 and learning_rate > min_learning_rate:
                    learning_rate *= learning_rate_decay
                    for param_group in optimizer.param_groups:
                        param_group["lr"] = learning_rate
                    print(f"Updated learning rate to {learning_rate:.8f}")
                

            if training_step % target_update_interval == 0:
                target_mixer_net.load_state_dict(mixer_net.state_dict())
                target_agent_net.load_state_dict(agent_net.state_dict())

            # Get episode data from queue and store in replay buffer
            for i in range(n_agent):
                sub_episode = queue.get()
                replay_buffer.extend_episode(sub_episode)
            average_goal_rate = replay_buffer.get_average_goal_rate(num_episodes=500)
            print(f"Avrage Goalrate: {average_goal_rate:.5f}")

            # Duplicate episodes with positive rewards
            num_duplications = min(
            dup_cap,
            max(1, int(1 + (1.0 - average_goal_rate) * scale))
            ) * int(dupe)


            replay_buffer.end_episode(num_duplications) # Prioritize episodes with positive reward in replay buffer by duplicating them.
            batch = replay_buffer.get_batch(num_of_samples=number_of_samples, sample_size=sample_size, extra_steps=bootstrap_time_steps) #Get batch of transitions for training
            # Collate batch of transitions into tensors for training
            
            # Collate batch of transitions into tensors for training
            obs, states, actions, rewards , done = learner_utils.collate_batch(batch)

            rewards = rewards[:, :, 0] # Shared reward for all agents, take reward of first agent in each transition
            #Train model here using batch of transitions

            if training_step > 200: #Only start training after enough transitions have been collected
            
                q_vals_buffer = learner_utils.calc_q_vals_buffer(agent_net, obs, len(batch), n_agent, sample_size) #Compute Q-values for all time steps in sample (including burn-in) of online network
                with torch.no_grad(): 
                    target_q_vals_buffer = learner_utils.calc_q_vals_buffer(target_agent_net, obs, len(batch), n_agent, sample_size) #Compute target Q-values for all time steps in sample (including burn-in and bootstrap time steps) of target network

                TD_target_buffer = torch.zeros(training_time_steps, number_of_samples, device=obs.device)
                Q_tot_buffer = torch.zeros(training_time_steps, number_of_samples, device=obs.device)
                
                for t in range(burn_in_time_steps, burn_in_time_steps + training_time_steps ): #Build TD target per time step for training time steps, also compute Q_tot for online network for training time steps
                    
                    Future_reward = torch.zeros(number_of_samples, device=obs.device)
                    mask = torch.ones(number_of_samples, device=obs.device)

                    with torch.no_grad(): # Compute target Q-values for training time steps using rewards and target network Q-values for bootstrap time steps
                        mask = (done.cumsum(dim=0) <= 1).float()

                        for i in range(0, bootstrap_time_steps):
                            Future_reward += (discount_factor ** (i)) * rewards[t+i] * mask[t+i] # Compute discounted future reward for bootstrap time steps, only use reward of first agent in each transition since shared reward setting
                            
                        masked_actions = q_vals_buffer[t+bootstrap_time_steps].clone()

                        for a in range(n_agent):
                            for s in range(number_of_samples):
                                _,_,action_mask = learner_utils.get_action_mask(n_actions,n_agent-1,n_opponents, obs[t+bootstrap_time_steps,s,a]) # Get action mask for bootstrap time step
                                masked_actions[s,a] = masked_actions[s,a].masked_fill(~action_mask, float('-inf')) # Mask out invalid actions for bootstrap time step
                                
                        best_actions = torch.argmax(masked_actions, dim=-1) # Get greedy actions for bootstrap time steps using online network Q-values
                        
                        
                        q_vals_target = target_q_vals_buffer[t+bootstrap_time_steps].clone()
                        
                        agent_qs_target = torch.gather(q_vals_target, dim=-1, index=best_actions.unsqueeze(-1)).squeeze(-1) #Greedy action selection for bootstrap time steps using target network Q-values
                        q_tot_target = target_mixer_net(agent_qs_target, states[t+bootstrap_time_steps]).squeeze() * (discount_factor**bootstrap_time_steps) # Get target Q-values for bootstrap time steps
                        y_t = Future_reward + q_tot_target*mask[t+bootstrap_time_steps] # Compute target Q-values using rewards and discounted future Q-values
                        TD_target_buffer[t-burn_in_time_steps] = y_t  # Add TD target to buffer for training time steps

                    chosen_q = torch.gather(q_vals_buffer[t], dim=2, index=actions[t].unsqueeze(-1)).squeeze(-1)
                    Q_tot_buffer[t-burn_in_time_steps] = mixer_net(chosen_q, states[t]).squeeze()

                Mean_Q_tot = Q_tot_buffer.mean().item()
                max_Q_tot = Q_tot_buffer.abs().max().item()
                Mean_TD_target = TD_target_buffer.mean().item()

                
                loss = F.mse_loss(TD_target_buffer, Q_tot_buffer)
                losses.append(loss.item())

                Q_tot_buffer_mean.append(Mean_Q_tot)
                Q_tot_buffer_max_abs.append(max_Q_tot)
                TD_target_buffer_mean.append(Mean_TD_target)
            
                gradiend_norm = learner_utils.backprop(model, optimizer, loss, max_grad_norm=max_grad)
                Gradient_norms.append(gradiend_norm)

                if plotting and training_step % 100 == 0:
                    if training_step % 1000 == 0 and len(losses) > 1000:
                        loss_plt_start = len(losses) - 1000
                    plt.clf()
                    plt.xlabel("EPISODE")
                    plt.plot(range(loss_plt_start, loss_plt_start + len(losses[loss_plt_start:])), losses[loss_plt_start:])
                    plt.savefig(run_dir / "loss.png")
                    plt.clf()
                    plt.xlabel("EPISODE")
                    plt.plot(Q_tot_buffer_mean)
                    plt.savefig(run_dir / "Q_tot_mean.png")
                    plt.clf()
                    plt.xlabel("EPISODE")
                    plt.plot(Q_tot_buffer_max_abs)
                    plt.savefig(run_dir / "Q_tot_max_abs.png")
                    plt.clf()
                    plt.xlabel("EPISODE")
                    plt.plot(TD_target_buffer_mean)
                    plt.savefig(run_dir / "TD_target_mean.png")
                    plt.clf()
                    plt.xlabel("EPISODE")
                    plt.plot(Gradient_norms)
                    plt.savefig(run_dir / "Gradient_norms.png")

                if epsilon.value > epsilon_min:
                    epsilon.value -= epsilon_decay
                    

            if training_step % 25 == 0:
                print(f"Training step:  {training_step}, epsilon: {epsilon.value:.3f}") #Debug print

            if logging:
                metrics["episodes"] += 1
                metrics["goals"] += replay_buffer.real_buffer[-1][-1]["reward"][-1] > 0
                metrics["best_avg_goal_rate"] = max(metrics["best_avg_goal_rate"], average_goal_rate)
                metrics["epsilon"] = epsilon.value
                metrics["learning_rate"] = learning_rate

            training_step += 1

            if training_step % Eval_time_steps == 0:
                    Eval_flag.value = True
                    print(f"Starting evaluation at training step {training_step} ") #Debug print

        else:
            print(f"Evaluating") #Debug print

        
        barrier.wait() # Signal agents to start next episode

    if logging:
        file_manager.save_metrics(run_dir, metrics)
    plt.ioff()
    plt.show()

    for p in processes:
        p.join() #Wait for all processes to finish before exiting main

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    main()