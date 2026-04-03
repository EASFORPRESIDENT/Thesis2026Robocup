from collections import deque
import random

class Episode(list):
    def save_transition(self, observation, action, reward, timestep: int, agent_id: int, done):
        transition = {
            "observation": observation,
            "action": action,
            "reward": reward,
            "timestep": timestep,
            "agent_id": agent_id,
            "done": done,
        }
        self.append(transition)

    def done(self):
        if self:
            self[-1]["done"] = True

    def reset(self):
        self.clear()

class ReplayBuffer:
    def __init__(self, num_of_episodes: int):
        self.buffer = deque(maxlen=num_of_episodes)
        self.episode = Episode()

    def extend_episode(self, episode: Episode):
        self.episode.extend(episode)

    def end_episode(self):
        if not self.episode:
            return

        self.episode.sort(key=lambda transition: (transition["timestep"], transition["agent_id"]))
        num_agents = max(transition["agent_id"] for transition in self.episode) + 1

        joint_episode = []
        for transition in self.episode:
            timestep = transition["timestep"]
            agent_id = transition["agent_id"]

            while len(joint_episode) <= timestep:
                joint_episode.append({
                    "observations": [None] * num_agents,
                    "state": [], # Compute with another function
                    "actions": [None] * num_agents,
                    "reward": None,
                    "done": None,
                    })

            joint_episode[timestep]["observations"][agent_id] = transition["observation"]
            joint_episode[timestep]["actions"][agent_id] = transition["action"]

            joint_episode[timestep]["reward"] = transition["reward"] # Okay for now
            joint_episode[timestep]["done"] = transition["done"] # Okay for now

        for step in joint_episode:
            if any(obs is None for obs in step["observations"]):
                raise ValueError("Missing agent observation in timestep")

            for obs in step["observations"]:
                step["state"].extend(obs)

        self.buffer.append(joint_episode.copy())
        self.episode = Episode()

    def get_batch(self, num_of_samples: int, sample_size: int):
        random_episodes = random.choices(self.buffer, k=num_of_samples)
        batch = []
        for episode in random_episodes:
            if sample_size >= len(episode):
                batch.append(list(episode))
            else:
                start = random.randint(0, len(episode) - sample_size)
                batch.append(list(episode)[start:start + sample_size])
        return batch