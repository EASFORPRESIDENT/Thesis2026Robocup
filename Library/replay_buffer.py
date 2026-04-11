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

    def end_episode(self, positive_reward_duplication_factor: int = 1):
        if not self.episode:
            return

        self.episode.sort(key=lambda transition: (transition["timestep"], transition["agent_id"]))
        num_agents = max(transition["agent_id"] for transition in self.episode) + 1
        contains_positive_reward = False

        joint_episode = []
        for transition in self.episode:
            if transition["reward"] > 0 and not contains_positive_reward:
                contains_positive_reward = True
                print(f"\033[32mINFO: Episode contains positive reward {transition['reward']} at timestep {transition['timestep']} for agent {transition['agent_id']}\033[0m") #Debug print
            timestep = transition["timestep"]
            agent_id = transition["agent_id"]

            while len(joint_episode) <= timestep:
                joint_episode.append({
                    "observations": [None] * num_agents,
                    "state": [],
                    "actions": [None] * num_agents,
                    "reward": [None] * num_agents,
                    "done": None,
                    })

            joint_episode[timestep]["observations"][agent_id] = transition["observation"]
            joint_episode[timestep]["actions"][agent_id] = transition["action"]
            joint_episode[timestep]["reward"][agent_id] = transition["reward"]
            joint_episode[timestep]["done"] = transition["done"]

        for step in joint_episode:
            if any(obs is None for obs in step["observations"]):
                raise ValueError("Missing agent observation in timestep")

            for obs in step["observations"]:
                step["state"].extend(obs)

        # Reward-prioritized replay: duplicate episodes with positive reward so they are sampled more often.
        duplication_count = positive_reward_duplication_factor if contains_positive_reward and positive_reward_duplication_factor > 1 else 1
        #print (f"\033[33mINFO: Added episode to replay buffer with length {len(joint_episode)} and duplication count {duplication_count}\033[0m") #Debug print
        for _ in range(duplication_count):
            self.buffer.append(joint_episode.copy())
        self.episode = Episode()

    def get_batch(self, num_of_samples: int, sample_size: int, extra_steps: int):
        random_episodes = random.choices(self.buffer, k=num_of_samples)
        batch = []
        for episode in random_episodes:
            start = 0
            while sample_size > len(episode):
                episode = random.choice(self.buffer) # Reroll if too short
                #print(f"\033[33mWARNING! Episode length {len(episode)} is less than sample size {sample_size}, rerolling...\033[0m") #Debug print
            
            max_start = len(episode) - (sample_size - extra_steps)

            u = random.random()
            start = int(max_start * (1 - u**2))
            batch.append(list(episode)[start:start + (sample_size - extra_steps)])

            for i in range(sample_size - len(batch[-1])):
                # If episode has enough steps from start, append additional steps from the episode
                if start + (sample_size - extra_steps) + i < len(episode):
                    batch[-1].append(episode[start + (sample_size - extra_steps) + i])

                else:
                    # Otherwise, pad with the last transition
                    batch[-1].append(batch[-1][-1])

        return batch