import random

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, initial_params, max_params):
        super().__init__()
        self.action_space = spaces.Box(low=np.array(initial_params), high=np.array(max_params), dtype=np.float32)
        self.observation_space = spaces.Box(low=0, high=1, shape=(len(initial_params),), dtype=np.float32)

        self.params = initial_params
        self.max_params = max_params

    def step(self, action):
        self.params = action

        # query_time = execute_query(self.params)
        query_time = random.random()

        reward = -query_time

        done = query_time >= 0.9

        info = {}

        return self.params / self.max_params, reward, done, False, info

    def reset(self, seed=None, options=None):
        if seed is not None:
            np.random.seed(seed)
        self.params = self.params
        return self.params / self.max_params

    def render(self):
        pass

    def close(self):
        pass
