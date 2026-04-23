import torch
import numpy as np
import torch.nn.functional as F

# obs:     [T, B, N, obs_dim]
# states:  [T, B, state_dim]
# actions: [T, B, N]
# rewards: [T, B, N]

# B = number of samples in batch
# N = number of agents
# A = number of actions
# H = hidden dimension of agent network
# T = number of time steps in sample (including burn-in and bootstrap time steps)

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


    obs = torch.from_numpy(np.array(obs, dtype=np.float32))
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

def aux_loss(n_actions: int,
             pred: torch.Tensor,
             true_actions: torch.Tensor,
             valid_mask: torch.Tensor) -> torch.Tensor:
    """
    pred:         [B * N, N - 1, A]
    true_actions: [B * N, N - 1]
    valid_mask:   [B * N, N - 1]   True where target is valid
    """
    pred = pred.reshape(-1, n_actions)
    true_actions = true_actions.reshape(-1)
    valid_mask = valid_mask.reshape(-1)

    ce = F.cross_entropy(pred, true_actions, reduction="none")
    ce = ce[valid_mask]

    if ce.numel() == 0:
        return pred.new_tensor(0.0)

    return ce.mean()

def calc_q_vals_buffer(agent_net, obs, batch_length, n_agents, sample_size):
    hidden = agent_net.init_hidden(batch_length * n_agents, device=obs.device) # Initialize hidden state for all agents in batch, will be updated at each time step during training loop
    q_vals_buffer = []

    for t in range(sample_size): # Unroll GRU and compute Q-values for all time steps in sample, store in buffer for later use in training loop
        obs_flat = obs[t].reshape(batch_length * n_agents, -1)
        q_values, hidden = agent_net(obs_flat, hidden)
        q_values = q_values.reshape(batch_length, n_agents, -1)
        q_vals_buffer.append(q_values)

    return q_vals_buffer

def get_action_mask(n_actions,n_temates,n_opponents, obs ):
    action_mask = torch.ones(n_actions, dtype=torch.bool) # 10 possible actions
    temmate_pass_unums = [] # List of teammate unums for pass actions
    opponent_mark_unums = [] # List of opponent unums for mark actions

    if n_temates > 0:
        teammate_start_idx = 9 + n_temates*3 + 3
    else:
        teammate_start_idx = 9
        
        
    if n_opponents > 0:
        if n_temates > 0:
            opponent_start_idx = teammate_start_idx + n_temates*3
        else:
            opponent_start_idx = 9 + 3
   

    if obs[5] != 1: # Check if in possession of the ball
        action_mask[1] = False # Can't shoot if not in possession of the ball
        action_mask[2] = False # Can't dribble if not in possession of the ball
        for i in range(0, n_temates):
            action_mask[7 + i] = False # Can't pass if not in possession of the ball

    else: # Has possession of the ball
            action_mask[0] = False # Can't move if in possession of the ball
            action_mask[4] = False # Can't reduce angle to goal if in possession of the ball
            action_mask[5] = False # Can't go to ball if in possession of the ball
            action_mask[6] = False # Can't reorient if in possession of the ball
            
            for i in range(0, n_temates): # Check if more than one teammate is in passing range
                obs_index = teammate_start_idx + 3*i
                action_index = 7 + i
                if obs[obs_index] == -2: # Check each teammate's passing range
                    action_mask[action_index] = False # Can't pass to this teammate if not in passing range
                else:
                    temmate_pass_unums.append([action_index,obs[obs_index]]) # Add teammate's unum to list of passable teammates

            for i in range(n_opponents):
                action_index = 7 + n_temates + i
                action_mask[action_index] = False # Can't mark opponent if in possession of the ball

     
    for i in range(0, n_opponents): # Check if opponents is in marking range
        obs_index = opponent_start_idx + 3*i
        action_index = 7 + n_temates + i
        if obs[obs_index] == -2: # Check each opponent's marking range
            action_mask[action_index] = False # Can't mark this opponent if not in marking range
        else:
            opponent_mark_unums.append([action_index,obs[obs_index]]) # Add opponent's unum to list of markable opponents
            

    return temmate_pass_unums, opponent_mark_unums, action_mask

def unroll_qmix(model, obs, states, actions):
    """
    obs:     [T, B, N, obs_dim]
    states:  [T, B, state_dim]
    actions: [T, B, N]

    returns:
        q_tot_buf:    [T, B]
        all_q_buf:    [T, B, N, A]
        chosen_q_buf: [T, B, N]
        hidden_buf:   [T, B, N, H]
        aux_buf:      depends on aux head
    """
    T, B, N, _ = obs.shape
    hidden = model.init_hidden(B, device=obs.device)

    q_tot_buf = []
    all_q_buf = []
    chosen_q_buf = []
    aux_buf = []

    for t in range(T):
        q_tot_t, all_q_t, chosen_q_t, hidden, aux_t = model(
            obs[t], states[t], actions[t], hidden
        )

        q_tot_buf.append(q_tot_t.squeeze(-1))          # [B]
        all_q_buf.append(all_q_t)                      # [B, N, A]
        chosen_q_buf.append(chosen_q_t)                # [B, N]

        if aux_t.dim() == 2:
            aux_t = aux_t.view(B, N, -1)               # [B, N, A]
        elif aux_t.dim() == 3 and aux_t.shape[0] == B * N:
            aux_t = aux_t.view(B, N, aux_t.shape[1], aux_t.shape[2])

        aux_buf.append(aux_t)

    return (
        torch.stack(q_tot_buf, dim=0),
        torch.stack(all_q_buf, dim=0),
        torch.stack(chosen_q_buf, dim=0),
        torch.stack(aux_buf, dim=0),
    )

def unroll_agent_net(agent_net, obs):
    """
    obs: [T, B, N, obs_dim]

    returns:
        q_buf:      [T, B, N, A]
    """
    T, B, N, _ = obs.shape
    hidden = agent_net.init_hidden(B * N, device=obs.device)

    q_buf = []

    for t in range(T):
        obs_flat = obs[t].reshape(B * N, -1)
        q_flat, hidden = agent_net(obs_flat, hidden)

        q_buf.append(q_flat.view(B, N, -1))

    return torch.stack(q_buf, dim=0)
