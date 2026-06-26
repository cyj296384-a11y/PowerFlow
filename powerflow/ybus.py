import numpy as np

def calc_ybus(branches, nb):
    """
    branches: list of (from, to, r, x)
    nb: number of buses
    """

    Y = np.zeros((nb, nb), dtype=complex)

    for br in branches:
        f = br["from"] - 1
        t = br["to"] - 1

        z = complex(br["r"], br["x"])
        y = 1 / z

        Y[f, f] += y
        Y[t, t] += y
        Y[f, t] -= y
        Y[t, f] -= y

    return Y