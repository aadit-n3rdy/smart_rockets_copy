#!/usr/bin/env python3

import numpy as np

learning_rate = 1.0
start_range = 1.0
rand_choice_array = np.arange(-1, 1.0001, 0.001)


class neural_network:
    weights = np.array([])
    biases = np.array([])

    def __init__(self, shape: list):
        for i in range(0, len(shape)-1):
            weights.append(np.random.choice(rand_choice_array,
                                            shape=(shape[i+1], shape[i])) * start_range)
            biases.append(np.random.choice(
                rand_choice_array, shape=(shape[i+1], 1)))

    def from_parent(self, parent: neural_network):
        self.weights = parent.weights.copy
        for i in range(0, len(weights)):
            for j in range(0, weights[i].flat):
                Weights[i].flat[j] = np.random.choice(
                    np.arange(-1, 1.0001, 0.001)) * learning_rate + weights[i].flat[j]

    def calculate(self, inp: np.ndarray):
        tmp = inp.copy()
        for weight in weights:
            tmp = weight.dot(tmp)
            for i in range(0, len(tmp.flat)):
                tmp.flat[i] *= biases[i]
