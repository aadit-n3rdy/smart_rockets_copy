import numpy as np
import math
import random

learning_rate = 1.0
start_range = 10.0
rand_choice_array = np.arange(-1, 1.0001, 0.001)


def activate(inp: float):
    ret = 0
    try:
        ret = 2/(1+math.exp(-inp)) - 1.0
    except OverflowError:
        if inp > 0:
            ret = 1
        else:
            ret = -1
    return ret


class neural_network:
    weights = None
    biases = None
    wt_count: int

    def __init__(self, shp: list):
        self.weights = [None] * (len(shp)-1)
        self.biases = [None] * (len(shp)-1)
        for i in range(0, len(shp)-1):
            self.weights[i] = np.random.choice(rand_choice_array,
                                               size=(shp[i+1], shp[i])) * start_range
            self.biases[i] = np.random.choice(
                rand_choice_array, size=(1, shp[i+1]))
        self.wt_count = len(shp)-1

    def init(shp: list, rng):
        nnet = neural_network([])
        for i in range(0, len(shp)-1):
            wt = np.random.choice(rand_choice_array, size=(
                shp[i+1], shp[i])) * start_range
            nnet.weights.append(wt.copy())
            nnet.biases.append(np.random.choice(
                rand_choice_array, size=(1, shp[i+1])))
        nnet.wt_count = len(shp)-1
        return (nnet, rng)

    def from_parent(self, parent):
        self.weights = parent.weights.copy()
        for i in range(0, len(self.weights)):
            for j in range(0, len(self.weights[i].flat)):
                self.weights[i].flat[j] = learning_rate * \
                    random.randrange(-100000, 100000) / \
                    100000.0 + self.weights[i].flat[j]

    def calculate(self, inp):
        tmp = inp
        tmp.resize((len(tmp.flat), 1))
        for i in range(0, self.wt_count):
            tmp = self.weights[i].dot(tmp)
            for j in range(0, len(tmp.flat)):
                tmp.flat[j] += self.biases[i].flat[j]
                tmp.flat[j] = activate(tmp.flat[j])
        return tmp.copy()
