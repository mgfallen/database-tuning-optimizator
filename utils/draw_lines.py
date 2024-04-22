import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    tps_values_10 = {'No-tune': 422.3, 'DDPG': 510.2, 'TRPO': 393.5, 'TQC': 469.0, 'TD3': 512.3, 'SAC': 380.3}
    tps_values_20 = {'No-tune': 422.3, 'DDPG': 523.2, 'TRPO': 423.5, 'TQC': 542.0, 'TD3': 553.3, 'SAC': 430.3}
    tps_values_50 = {'No-tune': 422.3, 'DDPG': 572.1, 'TRPO': 510.2, 'TQC': 610.0, 'TD3': 603.3, 'SAC': 439.3}
    tps_values_100 = {'No-tune': 422.3, 'DDPG': 628.3, 'TRPO': 580.5, 'TQC': 660.0, 'TD3': 635.3, 'SAC': 444.3}

    tps_err_10 = {'No-tune': 0.1 * 422.3, 'DDPG': 0.21 * 510.2, 'TRPO': 0.32 * 393.5, 'TQC': 0.24 * 469.0, 'TD3': 0.14 * 512.3, 'SAC': 0.23 * 380.3}
    tps_err_20 = {'No-tune': 0.1 * 422.3, 'DDPG': 0.19 * 523.2, 'TRPO': 0.19 * 423.5, 'TQC': 0.16 * 542.0, 'TD3': 0.18 * 553.3, 'SAC': 0.24 * 430.3}
    tps_err_50 = {'No-tune': 0.1 * 422.3, 'DDPG': 0.23 * 572.1, 'TRPO': 0.14 * 510.2, 'TQC': 0.12 * 610.0, 'TD3': 0.16 * 603.3, 'SAC': 0.12 * 439.3}
    tps_err_100 = {'No-tune': 0.1 * 422.3, 'DDPG': 0.09 * 628.3, 'TRPO': 0.19 * 580.5, 'TQC': 0.13 * 660.0, 'TD3': 0.09 * 635.3, 'SAC': 0.19 * 444.3}

    # Создание массивов для хранения значений свечей
    methods = list(tps_values_10.keys())
    width = 0.2

    colors = ['r', 'g', 'b', 'c']

    # Создание столбчатой диаграммы
    fig, ax = plt.subplots()
    ax.bar(np.arange(len(methods)) - 0.4, list(tps_values_10.values()), width, color=colors[0], yerr=tps_err_10.values(),
           ecolor='black', capsize=3, label='10 эпох')
    ax.bar(np.arange(len(methods)) - 0.2, list(tps_values_20.values()), width, color=colors[1], yerr=tps_err_20.values(),
           ecolor='black', capsize=3, label='20 эпох')
    ax.bar(np.arange(len(methods)), list(tps_values_50.values()), width, color=colors[2], yerr=tps_err_50.values(), ecolor='black',
           capsize=3, label='50 эпох')
    ax.bar(np.arange(len(methods)) + 0.2, list(tps_values_100.values()), width, color=colors[3], yerr= tps_err_100.values(),
           ecolor='black', capsize=3, label='100 эпох')

    # Добавление подписи осей
    plt.xlabel('Метод')
    plt.ylabel('TPS')

    # Добавление заголовка
    plt.title('Сравнение TPS')

    plt.legend()

    # Отображение диаграммы
    plt.xticks(np.arange(len(methods)), methods)
    plt.show()