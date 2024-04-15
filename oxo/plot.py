import numpy as np


def smooth(x, w=100):
    return np.convolve(x, np.ones(w), "valid") / w
