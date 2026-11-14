import numpy as np

MUTATION_STRENGTH = 0.1

def create_brain():
    W1 = np.random.uniform(-1, 1, (8, 8))
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

def crossover(brain_a, brain_b):

    W1_a = brain_a["W1"]
    b1_a = brain_a["b1"]
    W2_a = brain_a["W2"]
    b2_a = brain_a["b2"]

    W1_b = brain_b["W1"]
    b1_b = brain_b["b1"]
    W2_b = brain_b["W2"]
    b2_b = brain_b["b2"]

    coin_W1 = np.random.uniform(0, 1, W1_a.shape) < 0.5
    coin_b1 = np.random.uniform(0, 1, b1_a.shape) < 0.5
    coin_W2 = np.random.uniform(0, 1, W2_a.shape) < 0.5
    coin_b2 = np.random.uniform(0, 1, b2_a.shape) < 0.5

    new_W1 = np.where(coin_W1, W1_a, W1_b)
    new_b1 = np.where(coin_b1, b1_a, b1_b)
    new_W2 = np.where(coin_W2, W2_a, W2_b)
    new_b2 = np.where(coin_b2, b2_a, b2_b)

    new_brain = {
        "W1": new_W1,
        "b1": new_b1,
        "W2": new_W2,
        "b2": new_b2
    }

    return new_brain