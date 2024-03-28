import random

import numpy as np

"""
    description: this class responsible for storing in the buffer this type of data
    <state, action, reward, new_action, terminal_state>
    created by: minegoodfeeling@gmail.com
"""


class ReplayBuffer:
    def __init__(self, max_size, input_shape, n_actions):
        self.mem_size = max_size
        self.mem_cntr = 0
        self.state_memory = np.zeros((self.mem_size, *input_shape))
        self.new_state_memory = np.zeros((self.mem_size, *input_shape))
        self.action_memory = np.zeros((self.mem_size, n_actions))
        self.reward_memory = np.zeros(self.mem_size)
        self.terminal_memory = np.zeros(self.mem_size, dtype=bool)

    def store_transition(self, state, action, reward, new_state, done):
        index = self.mem_cntr % self.mem_size

        self.state_memory[index] = state
        self.new_state_memory[index] = new_state
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = done

        self.mem_cntr += 1

    def sample_buffer(self, batch_size):
        max_mem = min(batch_size, self.mem_cntr)

        batch_index = random.choice(max_mem)

        state = self.state_memory[batch_index]
        new_state = self.new_state_memory[batch_index]
        action = self.action_memory[batch_index]
        reward = self.reward_memory[batch_index]
        done = self.terminal_memory[batch_index]

        return state, action, reward, new_state, done
