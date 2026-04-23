from collections import deque
import random
import math

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

    def __init__(self, num_of_episodes: int, min_winrate : float):
        self.buffer = deque()
        self.real_buffer = deque(maxlen=num_of_episodes) # For evaluation purposes, only contains one copy of each episode, without reward-prioritized duplication
        self.episode = Episode()
        self.max_len = num_of_episodes
        self.min_winrate = min_winrate

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
            timestep = transition["timestep"]
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

        if max(joint_episode[-1]["reward"]) > 0.5:
            contains_positive_reward = True
            print(f"\033[32mINFO: Episode contains positive reward {transition['reward']} at timestep {transition['timestep']}\033[0m") #Debug print
            print(f"\033[32mINFO: Duplication factor for this episode: {positive_reward_duplication_factor}\033[0m") #Debug print


        for step in joint_episode:
            if any(obs is None for obs in step["observations"]):
                raise ValueError("Missing agent observation in timestep")

            for obs in step["observations"]:
                step["state"].extend(obs)

        joint_episode = self.inject_sucess_action_reward(joint_episode,num_agents)

        # Reward-prioritized replay: duplicate episodes with positive reward so they are sampled more often.
        duplication_count = positive_reward_duplication_factor if contains_positive_reward and positive_reward_duplication_factor > 1 else 1
        #print (f"\033[33mINFO: Added episode to replay buffer with length {len(joint_episode)} and duplication count {duplication_count}\033[0m") #Debug print
        for _ in range(duplication_count):
            self.buffer.append(joint_episode.copy())
            self.update_buffer()

        self.real_buffer.append(joint_episode.copy())
        self.update_buffer()

        self.episode = Episode()

    def update_buffer(self):

        episode = 0
        goal_rate = self.get_average_goal_rate(self.max_len,False)
        if len(self.buffer) > self.max_len:
            if goal_rate < self.min_winrate:
                while self.contain_goal(self.buffer[episode]):
                    episode += 1
                if (episode > self.max_len*self.min_winrate):
                    print("pause")
                del self.buffer[episode]
                print(f"Training buffer goalrate: {goal_rate}, deleted at index {episode}")
            else:
                self.buffer.popleft()
                print(f"Training buffer goalrate: {goal_rate}, Poped")

    def contain_goal(self,joint_episode):
        if max(joint_episode[-1]["reward"]) > 0.5:
            return True
        else:
            return False

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
            #start = int(max_start * u)
            start = int(max_start * (1 - u**1.5)) # Bias towards sampling later time steps in episode, as they are more likely to be shared between agents and contain more diverse transitions, while later time steps are more likely to be similar between agents and contain many transitions with zero reward. The bias is controlled by the exponent on u, where higher values will result in a stronger bias towards earlier time steps.
            batch.append(list(episode)[start:start + (sample_size - extra_steps)])

            for i in range(sample_size - len(batch[-1])):
                # If episode has enough steps from start, append additional steps from the episode
                if start + (sample_size - extra_steps) + i < len(episode):
                    batch[-1].append(episode[start + (sample_size - extra_steps) + i])

                else:
                    # Otherwise, pad with the last transition
                    batch[-1].append(batch[-1][-1])

        return batch
    
    def get_average_goal_rate(self, num_episodes: int, real : bool):
        if num_episodes <= 0:
            return 0
        total_goals = 0

        if real:
            buffer = self.real_buffer
        else:
            buffer = self.buffer

        for episode in list(buffer)[-num_episodes:]:
            final_transition = episode[-1]
            rewards = final_transition["reward"]
            if any(reward > 0.5 for reward in rewards):
                total_goals += 1
        return total_goals / num_episodes
    
    
    
    def inject_sucess_action_reward(self,joint_episode,nr_agents):
        episode_length = len(joint_episode)
        modified_episode = joint_episode.copy()
        sucess_index = len(joint_episode[0]["observations"][0]) - 2
        pass_sucess_window = [4,15]
        

        for t,transition in enumerate(joint_episode):
            To_close_prox = False
            Good_pass = False
            if t == 0:
                continue
            else:
                for a,agent in enumerate(transition["observations"]):
                    if agent[sucess_index] == 1:
                        if modified_episode[t-1]["actions"][a] == 1:
                            modified_episode[t-1]["reward"][a] += 0.1

                        if modified_episode[t-1]["actions"][a] > 6 and modified_episode[t-1]["actions"][a] <= 6 + nr_agents-1: #Extra reward for passing
                            modified_episode[t-1]["reward"][a] += 0.25
                            if t+pass_sucess_window[1] > episode_length:
                                pass_sucess_window[1] = episode_length-t
                            for i in range(t,t+pass_sucess_window[1]):
                                for reciving_agent in range(nr_agents):
                                    if reciving_agent == a:
                                        continue
                                    else:
                                        if joint_episode[i]["observations"][reciving_agent][5] == 1: #pass recived
                                                if i <= t+pass_sucess_window[0]:
                                                    To_close_prox = True

                                                elif not To_close_prox and i > t+pass_sucess_window[0]:
                                                    Good_pass = True
                                                    break
                                if Good_pass:
                                    break

                    if Good_pass:
                        modified_episode[t-1]["reward"][a] += 0.4

                        # elif modified_episode[t-1]["actions"][a] > 6 + nr_agents-1: 
                        #     modified_episode[t-1]["reward"][a] += 0.1

                    # else:
                    #     modified_episode[t-1]["reward"][a] -= 0.15

        return modified_episode

                
