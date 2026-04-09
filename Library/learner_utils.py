import torch

#        obs:     [t, n_samples, n_agents, obs_dim]
#        states:  [t, n_samples, state_dim]
#        actions: [t, n_samples, n_agents]
#        rewards: [t, n_samples, n_agents]

# Assume state is not empty
def collate_batch(batch):
    obs = []
    states = []
    actions = []
    rewards = []
    done = []
    for sample in batch:
        sample_obs = []
        sample_states = []
        sample_actions = []
        sample_rewards = []
        sample_done = []

        for step in sample:
            step_obs = step["observations"]
            step_state = step["state"]
            step_actions = step["actions"]
            step_rewards = step["reward"]
            step_done = step["done"]
            
            sample_obs.append(step_obs)
            sample_states.append(step_state)
            sample_actions.append(step_actions)
            sample_rewards.append(step_rewards)
            sample_done.append(step_done)
        
        obs.append(sample_obs)
        states.append(sample_states)
        actions.append(sample_actions)
        rewards.append(sample_rewards)
        done.append(sample_done)


    obs = torch.tensor(obs, dtype=torch.float32)
    obs = obs.permute(1, 0, 2, 3)
    states = torch.tensor(states, dtype=torch.float32)
    states = states.permute(1, 0, 2)
    actions = torch.tensor(actions, dtype=torch.int64)
    actions = actions.permute(1, 0, 2)
    rewards = torch.tensor(rewards, dtype=torch.float32)
    rewards = rewards.permute(1, 0, 2)
    done = torch.tensor(done, dtype=torch.bool)
    done = done.permute(1, 0)

    return obs, states, actions, rewards, done

#optimizer = torch.optim.Adam(qmix.parameters(), lr=3e-4)
def backprop(qmix, optimizer, loss, max_grad_norm):
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    grad_norm = torch.nn.utils.clip_grad_norm_(qmix.parameters(), max_grad_norm)
    optimizer.step()
    return grad_norm

def calc_q_vals_buffer(agent_net, obs, batch_length, N_AGENTS, SAMPLE_SIZE):
    hidden = agent_net.init_hidden(batch_length * N_AGENTS, device=obs.device) # Initialize hidden state for all agents in batch, will be updated at each time step during training loop
    q_vals_buffer = []

    for t in range(SAMPLE_SIZE): # Unroll GRU and compute Q-values for all time steps in sample, store in buffer for later use in training loop
        obs_flat = obs[t].reshape(batch_length * N_AGENTS, -1)
        q_values, hidden = agent_net(obs_flat, hidden)
        q_values = q_values.reshape(batch_length, N_AGENTS, -1)
        q_vals_buffer.append(q_values)

    return q_vals_buffer