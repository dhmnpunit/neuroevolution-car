import numpy as np

MUTATION_STRENGTH = 0.1

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

def mutate(brain):

    W1 = brain["W1"]
    b1 = brain["b1"]
    W2 = brain["W2"]
    b2 = brain["b2"]

    new_W1 = W1 + np.random.uniform(-MUTATION_STRENGTH, MUTATION_STRENGTH, W1.shape)
    new_b1 = b1 + np.random.uniform(-MUTATION_STRENGTH, MUTATION_STRENGTH, b1.shape)
    new_W2 = W2 + np.random.uniform(-MUTATION_STRENGTH, MUTATION_STRENGTH, W2.shape)
    new_b2 = b2 + np.random.uniform(-MUTATION_STRENGTH, MUTATION_STRENGTH, b2.shape)

    new_brain = {
        "W1": new_W1,
        "b1": new_b1,
        "W2": new_W2,
        "b2": new_b2
    }

    return new_brain