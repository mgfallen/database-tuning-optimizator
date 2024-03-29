import tensorflow as tf
from tensorflow.keras import layers

class SimpleActorModel(tf.keras.Model):
    def __init__(self, action_size):
        super(SimpleActorModel, self).__init__()
        self.dense1 = layers.Dense(128, activation="relu")
        self.dense2 = layers.Dense(128, activation="relu")
        self.output_action = layers.Dense(action_size, activation="softmax")

    def call(self, state):
        x = self.dense1(state)
        x = self.dense2(x)
        return self.output_action(x)

if __name__ == '__main__':
    # используем
    action_size = 2 # предположим, есть 2 возможных действия
    model = SimpleActorModel(action_size)

    state = tf.constant([[0.1, 0.2, 0.3]]) # пример состояния окружающей среды
    action_probabilities = model(state)
    print("Распределение вероятностей действий:", action_probabilities.numpy())
