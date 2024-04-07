import numpy as np
from stable_baselines3 import PPO, DDPG, TD3
from stable_baselines3.common.vec_env import DummyVecEnv

from agents.experimental.database_env import DbOptimizationEnv

if __name__ == '__main__':
    db_params = {
        "shared_buffers": [32 * 1024 * 1024, 1 * 1024 * 1024 * 1024, 128 * 1024 * 1024],
        "effective_cache_size": [512 * 1024 * 1024, 4 * 1024 * 1024 * 1024, 1 * 1024 * 1024 * 1024],
        "work_mem": [4 * 1024 * 1024, 64 * 1024 * 1024, 16 * 1024 * 1024],
        "maintenance_work_mem": [64 * 1024 * 1024, 1 * 1024 * 1024 * 1024, 256 * 1024 * 1024],
        "max_parallel_workers_per_gather": [0, 8, 4]
    }

    env = DbOptimizationEnv(db_params)
    print(env)
    env = DummyVecEnv([lambda: env])

    model = TD3('MultiInputPolicy', env, verbose=2,
                buffer_size=64,
                learning_starts=32,
                batch_size=16,
                tau=0.005,
                gamma=0.8,
                seed=42)
    model.learn(total_timesteps=10000)

    n_eval_episodes = 10

    eval_results = []

    obs = env.reset()
    print(obs)
    done = False
    episode_reward = 0.0

    for _ in range(n_eval_episodes):
        action, _states = model.predict(obs)

        obs, reward, done, info = env.step(action)

        episode_reward += reward
        print(f"Reward is: {episode_reward}")

    eval_results.append(episode_reward)
    mean_reward = np.mean(eval_results)
    std_reward = np.std(eval_results)

    print(f"Mean reward: {mean_reward:.2f} +/- {std_reward:.2f}")
