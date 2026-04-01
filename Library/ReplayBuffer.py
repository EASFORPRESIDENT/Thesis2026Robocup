from collections import deque
import random

class Episode(list):
    def save_transition(self, observation, action, timestep: int, agent_id: int, done):
        transition = (observation, action, timestep, agent_id, done)
        self.append(transition)

    def reset(self):
        self.clear()

class ReplayBuffer:
    def __init__(self, num_of_episodes: int):
        self.buffer = deque(maxlen=num_of_episodes)
        self.episode = Episode()

    def extend_episode(self, episode: Episode):
        self.episode.extend(episode)

    def end_episode(self):
        self.episode.sort(key=lambda transition: (transition[2], transition[3])) # Sort by timestep & agent_id
        self.buffer.append(self.episode.copy())
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