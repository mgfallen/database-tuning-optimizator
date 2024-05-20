import re
import subprocess
import sys
from pathlib import Path

from PyInquirer import prompt


def print_help():
    print("Parameters:")
    print("--num-params: Number of parameters to optimize. Range: 1-26. Default: All parameters.")
    print(
        "--params: Specific set of parameters for optimization. Comma-separated string. Not compatible with "
        "--num-params. Default: All parameters.")
    print("--epochs: Number of epochs for model training. Default: 100.")
    print("--device: Physical device for model training (CPU or GPU). Default: CPU.")
    print(
        "--config: Path to the configuration file containing database usage scenario and pgbench SQL "
        "transactions. Example provided in Listing 1.")
    print("--rl-algorithm: RL algorithm to use for optimization. Choices: TQC, SAC, DDPG, TRPO, TD3. Default: TQC.")
    print(
        "--hyperparameters: Model hyperparameters such as learning rate, discount factor, batch size, etc., "
        "for different models. Each algorithm has its own set of hyperparameters.")


def start_search():
    questions = [
        {
            'type': 'input',
            'name': 'num_params',
            'message': 'Enter the number of parameters to configure:',
            'validate': lambda x: 0 < len(x) <= 26 or 'You must enter the number of parameters in range of 1 to 26',
            'default': '26'
        },
        {
            'type': 'input',
            'name': 'param_set',
            'message': 'Enter a specific set of parameters to configure:',
            'validate': validate_param_set,
            'default': 'None'
        },
        {
            'type': 'input',
            'name': 'num_epochs',
            'message': 'Enter the number of epochs for model training:',
            'validate': lambda x: len(x) > 0 or 'You must enter the positive number of epochs',
            'default': '100'
        },
        {
            'type': 'list',
            'name': 'device',
            'message': 'Choose the device for model training:',
            'choices': ['CPU', 'GPU'],
            'default': 'CPU'
        },
        {
            'type': 'input',
            'name': 'config_file',
            'message': 'Enter the path to the configuration file for the database usage scenario:',
            'validate': validate_config_file_and_sql,
            'default': 'None'
        },
        {
            'type': 'input',
            'name': 'rl_algorithm',
            'message': 'Enter the RL algorithm to use:',
            'validate': validate_rl_algorithm,
            'default': 'TQC'
        },
        {
            'type': 'input',
            'name': 'model_hparams',
            'message': 'Enter model hyperparameters in key-value format:',
            'validate': lambda x: len(x) > 0 or 'You must enter model hyperparameters',
            'default': 'None'
        }
    ]

    if '--help' in sys.argv:
        print_help()
        return

    answers = prompt(questions)

    subprocess.run(['python', '-m', '../entry_points/experimental/database_tuning_entry',
                    '--num_params', answers['num_params'],
                    '--param_set', answers['param_set'],
                    '--num_epochs', answers['num_epochs'],
                    '--device', answers['device'],
                    '--config_file', answers['config_file'],
                    '--rl_algorithm', answers['rl_algorithm'],
                    '--model_hparams', answers['model_hparams']], check=True)


def validate_param_set(x):
    if not x:
        return 'You must enter a set of parameters'
    pattern = r'^[a-zA-Z0-9\s\,]+$'
    if not re.match(pattern, x):
        return 'Invalid parameter set. Use comma-separated string of literals.'
    return True


def validate_sql_transaction(x):
    if not x:
        return 'You must enter the path to the configuration file'
    sql_keywords = r'(BEGIN|INSERT|UPDATE|SELECT|COMMIT)'
    if not re.search(sql_keywords, x):
        return 'The configuration file does not contain a valid SQL transaction.'
    return True


def validate_config_file_path(x):
    if not x:
        return 'You must enter the path to the configuration file'
    path = Path(x)
    if not path.is_file():
        return 'The specified file does not exist or is not accessible.'
    return True


def validate_config_file_and_sql(x):
    if not validate_config_file_path(x):
        return False
    with open(x, 'r') as file:
        content = file.read()
    if not validate_sql_transaction(content):
        return False
    return True


def validate_rl_algorithm(x):
    valid_rl_algorithms = ['TQC', 'TD3', 'TRPO', 'DDPG', 'SAC']

    if not x:
        return 'You must enter the RL algorithm'

    if x not in valid_rl_algorithms:
        return f'Invalid RL algorithm. Choose from {", ".join(valid_rl_algorithms)}.'

    return True


if __name__ == "__main__":
    start_search()
