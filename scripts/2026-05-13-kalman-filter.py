import numpy as np
def kalman_filter(z, Q=1e-5, R=1e-2):
    x, p = z[0], 1.0
    res = []
    for val in z:
        p = p + Q
        k = p / (p + R)
        x = x + k * (val - x)
        p = (1 - k) * p
        res.append(x)
    return res