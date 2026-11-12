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
