import numpy as np

def create_brain():
    W1 = np.random.uniform(-1, 1, (8, 5))
    b1 = np.random.uniform(-1, 1, 8)

    W2 = np.random.uniform(-1, 1, (2, 8))
    b2 = np.random.uniform(-1, 1, 2)

    brain = {
        "W1": W1,
        "b1": b1,
        "W2": W2,
        "b2": b2
    }

    return brain

def think(brain, rays):

    W1 = brain["W1"]
    b1 = brain["b1"]
    W2 = brain["W2"]
    b2 = brain["b2"]

    hidden = np.tanh(W1 @ rays + b1)
    output = np.tanh(W2 @ hidden + b2)

    return output