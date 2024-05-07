import subprocess

from PyInquirer import prompt


def start_search():
    questions = [
        {
            'type': 'input',
            'name': 'num_params',
            'message': 'Введите число параметров для настройки:',
            'validate': lambda x: len(x) > 0 or 'Вы должны ввести число параметров'
        },
        {
            'type': 'input',
            'name': 'param_set',
            'message': 'Введите конкретный набор параметров для настройки:',
            'validate': lambda x: len(x) > 0 or 'Вы должны ввести набор параметров'
        },
        {
            'type': 'input',
            'name': 'num_epochs',
            'message': 'Введите число эпох для обучения модели:',
            'validate': lambda x: len(x) > 0 or 'Вы должны ввести число эпох',
            'default': 100
        },
        {
            'type': 'list',
            'name': 'device',
            'message': 'Выберите устройство для обучения модели:',
            'choices': ['CPU', 'GPU'],
            'default': 'CPU'
        },
        {
            'type': 'input',
            'name': 'config_file',
            'message': 'Введите путь к конфигурационному файлу сценария использования базы данных:',
            'validate': lambda x: len(x) > 0 or 'Вы должны ввести путь к конфигурационному файлу',
            'default': None
        },
        {
            'type': 'input',
            'name': 'rl_algorithm',
            'message': 'Введите алгоритм RL для использования:',
            'validate': lambda x: len(x) > 0 or 'Вы должны ввести алгоритм RL',
            'default': 'DDPG'
        },
        {
            'type': 'input',
            'name': 'model_hparams',
            'message': 'Введите гиперпараметры модели в формате ключ-значение:',
            'validate': lambda x: len(x) > 0 or 'Вы должны ввести гиперпараметры модели',
            'default': None
        }
    ]

    answers = prompt(questions)

    print(f"Запуск процесса поиска оптимальных параметров с параметрами:")
    print(f"Число параметров: {answers['num_params']}")
    print(f"Набор параметров: {answers['param_set']}")
    print(f"Число эпох: {answers['num_epochs']}")
    print(f"Устройство для обучения: {answers['device']}")
    print(f"Конфигурационный файл: {answers['config_file']}")
    print(f"Алгоритм RL: {answers['rl_algorithm']}")
    print(f"Гиперпараметры модели: {answers['model_hparams']}")

    subprocess.run(['python -m', '../entry_points/experimental/database_tuning_entry',
                    '--num_params', answers['num_params'],
                    '--param_set', answers['param_set'],
                    '--num_epochs', answers['num_epochs'],
                    '--device', answers['device'],
                    '--config_file', answers['config_file'],
                    '--rl_algorithm', answers['rl_algorithm'],
                    '--model_hparams', answers['model_hparams']], check=True)


if __name__ == "__main__":
    start_search()
