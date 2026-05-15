import numpy as np

def weighted_moving_average(data, weights):
    """Calculates the WMA for a given series and weight array."""
    weights = np.array(weights)
    return np.convolve(data, weights[::-1], 'valid') / weights.sum()