from stable_baselines3.common.env_checker import check_env

import agents.experimental.custom_test_env as env_maker


if __name__ == '__main__':
    params = [1, 2, 3]
    max_params = [3, 3, 3]
    env = env_maker.CustomEnv(params, max_params)
    check_env(env)
