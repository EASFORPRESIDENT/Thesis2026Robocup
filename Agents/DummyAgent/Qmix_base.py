import torch
import torch.nn as nn
import torch.nn.functional as F


class AgentNetwork(nn.Module):
    """
    Per-agent Q-network.
    Input:  local observation for one agent
    Output: Q-values for that agent's discrete actions
    """
    def __init__(self, obs_dim: int, hidden_dim: int, n_actions: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, n_actions)
        )

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        # obs: [batch, n_agents, obs_dim]
        return self.net(obs)  # [batch, n_agents, n_actions]


class RecurrentAgentNetwork(nn.Module):
    def __init__(self, obs_dim: int, hidden_dim: int, n_actions: int):
        super().__init__()
        self.fc1 = nn.Linear(obs_dim, hidden_dim)
        self.gru = nn.GRUCell(hidden_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, n_actions)

    def init_hidden(self, batch_agents: int, device=None):
        return torch.zeros(batch_agents, self.gru.hidden_size, device=device)

    def forward(self, obs: torch.Tensor, hidden: torch.Tensor):
        """
        obs:    [batch * n_agents, obs_dim]
        hidden: [batch * n_agents, hidden_dim]
        """
        x = F.relu(self.fc1(obs))
        h = self.gru(x, hidden)
        q = self.fc2(h)
        return q, h
    
    
class QMixer(nn.Module):
    """
    QMIX mixing network.
    Monotonic mixing is enforced by making hypernetwork-produced weights non-negative.
    """
    def __init__(self, n_agents: int, state_dim: int, mixing_hidden_dim: int):
        super().__init__()
        self.n_agents = n_agents
        self.state_dim = state_dim
        self.mixing_hidden_dim = mixing_hidden_dim

        # Hypernetworks generate weights conditioned on global state
        self.hyper_w1 = nn.Linear(state_dim, n_agents * mixing_hidden_dim)
        self.hyper_b1 = nn.Linear(state_dim, mixing_hidden_dim)

        self.hyper_w2 = nn.Linear(state_dim, mixing_hidden_dim)
        self.hyper_b2 = nn.Sequential(
            nn.Linear(state_dim, mixing_hidden_dim),
            nn.ReLU(),
            nn.Linear(mixing_hidden_dim, 1)
        )

    def forward(self, agent_qs: torch.Tensor, states: torch.Tensor) -> torch.Tensor:
        """
        agent_qs: [batch, n_agents]
        states:   [batch, state_dim]
        returns:  [batch, 1]
        """
        batch_size = agent_qs.size(0)

        # First layer
        w1 = torch.abs(self.hyper_w1(states))  # enforce non-negative weights
        b1 = self.hyper_b1(states)

        w1 = w1.view(batch_size, self.n_agents, self.mixing_hidden_dim)
        b1 = b1.view(batch_size, 1, self.mixing_hidden_dim)

        agent_qs = agent_qs.view(batch_size, 1, self.n_agents)
        hidden = F.elu(torch.bmm(agent_qs, w1) + b1)  # [batch, 1, mixing_hidden_dim]

        # Second layer
        w2 = torch.abs(self.hyper_w2(states))  # [batch, mixing_hidden_dim]
        w2 = w2.view(batch_size, self.mixing_hidden_dim, 1)

        b2 = self.hyper_b2(states).view(batch_size, 1, 1)

        q_tot = torch.bmm(hidden, w2) + b2  # [batch, 1, 1]
        return q_tot.view(batch_size, 1)


class QMIX(nn.Module):
    """
    Full QMIX model = shared agent network + mixer.
    """
    def __init__(
        self,
        obs_dim: int,
        state_dim: int,
        n_agents: int,
        n_actions: int,
        agent_hidden_dim: int = 64,
        mixing_hidden_dim: int = 32
    ):
        super().__init__()
        self.n_agents = n_agents
        self.n_actions = n_actions

        # Usually parameter-shared across agents
        self.agent_net = AgentNetwork(obs_dim, agent_hidden_dim, n_actions)
        self.mixer = QMixer(n_agents, state_dim, mixing_hidden_dim)

    def forward(self, obs: torch.Tensor, states: torch.Tensor, actions: torch.Tensor):
        """
        obs:     [batch, n_agents, obs_dim]
        states:  [batch, state_dim]
        actions: [batch, n_agents]  integer action indices

        returns:
            q_tot: [batch, 1]
            all_q: [batch, n_agents, n_actions]
            chosen_q: [batch, n_agents]
        """
        all_q = self.agent_net(obs)  # [batch, n_agents, n_actions]

        # Gather Q-values for chosen actions
        chosen_q = torch.gather(all_q, dim=2, index=actions.unsqueeze(-1)).squeeze(-1)
        # [batch, n_agents]

        q_tot = self.mixer(chosen_q, states)  # [batch, 1]
        return q_tot, all_q, chosen_q