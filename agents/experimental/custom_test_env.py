import gymnasium as gym
import numpy as np


class DatabaseTuningEnv(gym.Env):
    def __init__(self):
        super(DatabaseTuningEnv, self).__init__()
        self.action_space = gym.spaces.Box(low=np.array([0]), high=np.array([100]), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(3,), dtype=np.float32)
        self.shared_buffers = 50
        self.latency = 100
        self.throughput = 10

    def step(self, action):
        self.shared_buffers += action
        self.latency -= action * 0.1
        self.throughput += action * 0.05
        reward = self.throughput - self.latency
        return np.array([self.shared_buffers, self.latency, self.throughput]), reward, False, {}

    def reset(self):
        # Reset database parameters and metrics
        self.shared_buffers = 50
        self.latency = 100
        self.throughput = 10
        return np.array([self.shared_buffers, self.latency, self.throughput])
