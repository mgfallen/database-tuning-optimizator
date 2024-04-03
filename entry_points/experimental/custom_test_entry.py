from stable_baselines3 import DDPG
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.env_checker import check_env

import agents.experimental.custom_test_env as env_maker


if __name__ == '__main__':
    env = env_maker.DatabaseTuningEnv()

    check_env(env)
    env = DummyVecEnv([lambda: env])

    model = DDPG('MlpPolicy', env)
    model.learn(total_timesteps=1000)

    # Evaluate trained agent
    obs = env.reset()
    sum_rew = 0
    for _ in range(100):
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        sum_rew += reward
        print(sum_rew)
        if done:
            break

