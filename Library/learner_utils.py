import torch

#        obs:     [n_samples, n_agents, obs_dim]
#        states:  [n_samples, state_dim]
#        actions: [n_samples, n_agents]

# Assume state is not empty
def collate_batch(batch):
    obs = []
    states = []
    actions = []

    for sample in batch:
        sample_obs = []
        sample_states = []
        sample_actions = []

        for step in sample:
            step_obs = step["observations"]
            step_state = step["state"]
            step_actions = step["actions"]

            sample_obs.append(step_obs)
            sample_states.append(step_state)
            sample_actions.append(step_actions)

        obs.append(sample_obs)
        states.append(sample_states)
        actions.append(sample_actions)

    obs = torch.tensor(obs, dtype=torch.float32)
    obs = obs.permute(1, 0, 2, 3)
    states = torch.tensor(states, dtype=torch.float32)
    states = states.permute(1, 0, 2)
    actions = torch.tensor(actions, dtype=torch.int64)
    actions = actions.permute(1, 0, 2)
    return obs, states, actions
