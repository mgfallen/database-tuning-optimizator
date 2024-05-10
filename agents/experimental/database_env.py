import subprocess
import numpy as np
import gymnasium as gym
import psycopg2
import re
from gymnasium import spaces


class DbOptimizationEnv(gym.Env):
    def __init__(self, db_params: dict, pgbench_params: dict) -> None:
        self.db_params = db_params
        self.pgbench_params = pgbench_params

        self.action_space = spaces.Box(
            low=np.array([param[0] for param in db_params.values()]),
            high=np.array([param[1] for param in db_params.values()]),
            dtype=np.float32
        )
        self.observation_space = spaces.Box(
                low=np.array([param[0] for param in db_params.values()]),
                high=np.array([param[1] for param in db_params.values()]),
                dtype=np.float32
            )
        self.default_params = {param: value[2] for param, value in db_params.items()}
        self.conn = psycopg2.connect(**db_params)
        self.conn.autocommit = True
        print(self.get_full_bencmark()) # system monitoring

    def reset(self, seed=None):
        self.set_default_params()
        return np.array([self.default_params[param] for param in self.db_params.keys()])

    def step(self, action):
        self.set_params(action)
        benchmark = self.get_benchmark()
        reward = -benchmark
        done = False
        info = {'benchmark': benchmark}
        return action, reward, done, False, info

    def set_default_params(self):
        with self.conn.cursor() as cur:
            for param, value in self.default_params.items():
                cur.execute(f"ALTER SYSTEM SET {param} = {value}")
                cur.execute("SELECT pg_reload_conf();")
            self.conn.commit()
        restart_command = "sudo systemctl restart postgresql"
        subprocess.run(restart_command, shell=True, capture_output=True, text=True)

    def set_params(self, params):
        with self.conn.cursor() as cur:
            for param, value in zip(self.db_params.keys(), params):
                if self.db_params[param][0] == "enum":
                    value = str(value)
                cur.execute(f"ALTER SYSTEM SET {param} = {value}")
                cur.execute("SELECT pg_reload_conf();")
            self.conn.commit()
        restart_command = "sudo systemctl restart postgresql"
        subprocess.run(restart_command, shell=True, capture_output=True, text=True)

    def get_benchmark(self):
        pgbench_cmd = f"sudo -u postgres pgbench -c 10 -j 2 -t 1000 postgres"
        result = subprocess.run(pgbench_cmd, shell=True, capture_output=True, text=True)
        tps_string = result.stdout.split('\n')[-2].split(' = ')[-1]
        match = re.search(r'\d+\.\d+', tps_string)
        tps = float(match.group(0))
        return tps

    def get_full_bencmark(self):
        pgbench_cmd = ["sudo", "-u", "postgres", "pgbench"]

        if 'num_clients' in self.pgbench_params: # default value is 1
            pgbench_cmd.extend(["-c", str(self.pgbench_params['num_clients'])])

        if 'num_thread' in self.pgbench_params: # dafault value is a number of VCore
            pgbench_cmd.extend(["-j", str(self.pgbench_params['num_thread'])])

        if 'num_transactions' in self.pgbench_params: # default value is 10
            pgbench_cmd.extend(["-t", str(self.pgbench_params['num_transactions'])])

        if 'database_size' in self.pgbench_params: # default value is 1
            pgbench_cmd.extend(["-s", str(self.pgbench_params['database_size'])])

        pgbench_cmd.append("postgres")

        result = subprocess.run(pgbench_cmd, shell=True, capture_output=True, text=True)
        return result.stdout

