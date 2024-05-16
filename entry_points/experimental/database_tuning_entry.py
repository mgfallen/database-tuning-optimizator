import argparse

import numpy as np
from stable_baselines3 import DDPG
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.vec_env import DummyVecEnv

from agents.experimental.database_env import DbOptimizationEnv

from knobs_env.knobs_selector import KnobsSelector

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Скрипт для обработки параметров')
    parser.add_argument('--num_params', type=int, required=True, help='Число параметров для настройки')
    parser.add_argument('--param_set', type=str, required=True, help='Конкретный набор параметров для настройки')
    parser.add_argument('--num_epochs', type=int, required=True, help='Число эпох для обучения модели')
    parser.add_argument('--device', choices=['CPU', 'GPU'], required=True, help='Устройство для обучения модели')
    parser.add_argument('--config_file', type=str, required=True,
                        help='Путь к конфигурационному файлу сценария использования базы данных')
    parser.add_argument('--rl_algorithm', type=str, required=True, help='Алгоритм RL для использования')
    parser.add_argument('--model_hparams', type=str, required=True, help='Гиперпараметры модели в формате JSON')

    # db_params = {
    #     "shared_buffers": [32 * 1024 * 1024, 1 * 1024 * 1024 * 1024, 128 * 1024 * 1024],
    #     "effective_cache_size": [512 * 1024 * 1024, 4 * 1024 * 1024 * 1024, 1 * 1024 * 1024 * 1024],
    #     "work_mem": [4 * 1024 * 1024, 64 * 1024 * 1024, 16 * 1024 * 1024],
    #     "maintenance_work_mem": [64 * 1024 * 1024, 1 * 1024 * 1024 * 1024, 256 * 1024 * 1024],
    #     "max_parallel_workers_per_gather": [0, 8, 4]
    # }

    selector = KnobsSelector()
    db_params = selector.select_and_evaluate()
    pgbench_params = parser.__dict__

    env = DbOptimizationEnv(db_params, pgbench_params)

    print(env)
    env = DummyVecEnv([lambda: env])

    n_actions = db_params.keys().__len__()

    action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

    model = DDPG('MlpPolicy', env, verbose=2,
                 buffer_size=64,
                 learning_starts=32,
                 batch_size=16,
                 tau=0.005,
                 gamma=0.8,
                 seed=42,
                 action_noise=action_noise)
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
