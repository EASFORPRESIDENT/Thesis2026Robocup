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
    for sample in batch:
        sample_obs = []
        sample_states = []
        sample_actions = []
        sample_rewards = []

        for step in sample:
            step_obs = step["observations"]
            step_state = step["state"]
            step_actions = step["actions"]
            step_rewards = step["reward"]
            
            sample_obs.append(step_obs)
            sample_states.append(step_state)
            sample_actions.append(step_actions)
            sample_rewards.append(step_rewards)
        
        obs.append(sample_obs)
        states.append(sample_states)
        actions.append(sample_actions)
        rewards.append(sample_rewards)

    obs = torch.tensor(obs, dtype=torch.float32)
    obs = obs.permute(1, 0, 2, 3)
    states = torch.tensor(states, dtype=torch.float32)
    states = states.permute(1, 0, 2)
    actions = torch.tensor(actions, dtype=torch.int64)
    actions = actions.permute(1, 0, 2)
    rewards = torch.tensor(rewards, dtype=torch.float32)
    rewards = rewards.permute(1, 0, 2)
    print(rewards.shape)
    return obs, states, actions, rewards
