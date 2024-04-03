import gymnasium as gym
import numpy as np


class DatabaseTuningEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = gym.spaces.Box(low=np.array([0]), high=np.array([100]), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=-np.float32(1000), high=np.float32(1000), shape=(3,), dtype=np.float32)
        self.shared_buffers = np.float32(50.0)
        self.latency = np.float32(100.0)
        self.throughput = np.float32(10.0)

    def step(self, action):
        self.shared_buffers += action
        self.latency -= action * 0.1
        self.throughput += action * 0.05
        reward = float(self.throughput - self.latency)
        state = np.array([self.shared_buffers, self.latency, self.throughput], dtype=np.float32).flatten()
        return state, reward, False, False, {}

    def reset(self, seed=42):
        # Reset database parameters and metrics
        self.shared_buffers = np.float32(50.0)
        self.latency = np.float32(100.0)
        self.throughput = np.float32(10.0)
        return (np.array([self.shared_buffers, self.latency, self.throughput], dtype=np.float32), {})
