from stable_baselines3 import DDPG
from stable_baselines3.common.vec_env import DummyVecEnv

import agents.experimental.custom_test_env as env_maker


if __name__ == '__main__':
    params = [1, 2, 3]
    max_params = [3, 3, 3]
    env = DummyVecEnv([lambda: env_maker.DatabaseTuningEnv()])

    model = DDPG('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=10000)

    # Evaluate trained agent
    obs = env.reset()
    for _ in range(100):
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        if done:
            obs = env.reset()

