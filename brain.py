import numpy as np

def neuron(inputs, weights, bias):
    i = np.array(inputs)
    w = np.array(weights)
    m = i * w

    total = np.sum(m) + bias
    result = np.tanh(total)

    return result