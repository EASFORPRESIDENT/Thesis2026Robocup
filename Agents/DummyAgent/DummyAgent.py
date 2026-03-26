import hfo
import torch
import itertools
from pathlib import Path
from Qmix_base import QMIX

PROJECT_ROOT = Path(__file__).resolve().parents[2]
HFO_ROOT = PROJECT_ROOT / "HFO"
FORMATIONS_PATH = HFO_ROOT / "bin/teams/base/config/formations-dt"

N_AGENTS = 3
N_ACTIONS = 8
OBS_DIM = 20
STATE_DIM = 50

def select_hfo_action(action_idx, teammate_unums=None):
    if action_idx == 0:
        return (hfo.MOVE, [])
    elif action_idx == 1:
        return (hfo.DRIBBLE, [])
    elif action_idx == 2:
        return (hfo.SHOOT, [])
    elif action_idx == 3:
        # example pass
        if teammate_unums:
            return (hfo.PASS, [teammate_unums[0]])
        return (hfo.MOVE, [])
    else:
        return (hfo.MOVE, [])

def main():
    model = QMIX(
        obs_dim=OBS_DIM,
        state_dim=STATE_DIM,
        n_agents=N_AGENTS,
        n_actions=N_ACTIONS
    )

    # one env per agent
    envs = []
    for _ in range(N_AGENTS):
        env = hfo.HFOEnvironment()
        env.connectToServer(
            hfo.HIGH_LEVEL_FEATURE_SET,
            str(FORMATIONS_PATH),
            6000,
            "localhost",
            "base_left",
            False
        )
        envs.append(env)

    my_unums = [env.getUnum() for env in envs]

    for episode in itertools.count():
        status = hfo.IN_GAME

        while status == hfo.IN_GAME:
            obs_list = []
            teammate_lists = []

            # collect obs from all agents
            for i, env in enumerate(envs):
                obs = env.getState()
                obs_tensor = torch.tensor(obs[:OBS_DIM], dtype=torch.float32)
                obs_list.append(obs_tensor)

                teammate_unums = [u for u in my_unums if u != my_unums[i]]
                teammate_lists.append(teammate_unums)

            # shape: [1, n_agents, obs_dim]
            obs_batch = torch.stack(obs_list).unsqueeze(0)

            # dummy global state example
            state = torch.zeros(1, STATE_DIM)

            # get per-agent Q-values from shared agent network
            # if your QMIX forward needs actions, use agent_net directly for acting
            with torch.no_grad():
                all_q = model.agent_net(obs_batch.squeeze(0))   # shape [n_agents, n_actions]
                actions = all_q.argmax(dim=1)                  # shape [n_agents]

            # act for each agent
            for i, env in enumerate(envs):
                action_idx = int(actions[i].item())
                action, params = select_hfo_action(action_idx, teammate_lists[i])
                env.act(action, *params)

            # advance all agents
            statuses = [env.step() for env in envs]
            status = statuses[0]

        print(f"Episode {episode} ended with {envs[0].statusToString(status)}")

        if status == hfo.SERVER_DOWN:
            for env in envs:
                env.act(hfo.QUIT)
            break

if __name__ == "__main__":
    main()