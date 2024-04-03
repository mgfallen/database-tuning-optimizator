from stable_baselines3 import DDPG

import agents.experimental.custom_test_env as env_maker


if __name__ == '__main__':
    env = env_maker.DatabaseTuningEnv()

    model = DDPG('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=100)

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

