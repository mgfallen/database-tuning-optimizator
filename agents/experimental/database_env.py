import subprocess
import numpy as np
import gym
from gym import spaces


class DbOptimizationEnv(gym.Env):
    def __init__(self, db_params):
        self.action_space = spaces.Box(
            low=np.array([param[0] for param in db_params.values()]),
            high=np.array([param[1] for param in db_params.values()]),
            dtype=np.float32
        )
        self.observation_space = spaces.Dict({
            'benchmark': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
            'params': spaces.Box(
                low=np.array([param[0] for param in db_params.values()]),
                high=np.array([param[1] for param in db_params.values()]),
                dtype=np.float32
            )
        })
        self.db_params = db_params
        self.default_params = {param: value[2] for param, value in db_params.items()}
        self.conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="0.0.0.0",
                                     port="5432")

    def reset(self):
        self.set_default_params()
        benchmark = self.get_benchmark()
        return {'benchmark': benchmark,
                'params': np.array([self.default_params[param] for param in self.db_params.keys()])}

    def step(self, action):
        self.set_params(action)
        benchmark = self.get_benchmark()
        reward = -benchmark
        done = False
        info = {}
        return {'benchmark': benchmark, 'params': action}, reward, done, False, info

    def set_default_params(self):
        with self.conn.cursor() as cur:
            for param, value in self.default_params.items():
                cur.execute(f"ALTER SYSTEM SET {param} = {value}")
                self.conn.commit()

    def set_params(self, params):
        with self.conn.cursor() as cur:
            for param, value in zip(self.db_params.keys(), params):
                cur.execute(f"ALTER SYSTEM SET {param} = {value}")
                self.conn.commit()

    def get_benchmark(self):
        pgbench_cmd = f"pgbench -c 10 -j 2 -t 1000 my_database_for_benchmark"
        result = subprocess.run(pgbench_cmd, shell=True, capture_output=True, text=True)
        tps = float(result.stdout.split('\n')[-3].split(' = ')[-1])
        return tps
