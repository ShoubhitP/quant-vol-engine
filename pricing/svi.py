import numpy as np
from scipy import optimize

def svi_variance(k, a, b, rho, m, sigma):
    impliedVariance = a + b * (rho * (k - m) + np.sqrt(np.square(k-m) + np.square(sigma)))
    return impliedVariance

def fit_svi(strikes, ivs, F, T):
    k_values = np.log(np.array(strikes) / F)
    impliedVolatilityVals = np.square(np.array(ivs))

    def lossHelper(params):
        a, b, rho, m, sigma = params
        return np.sum(np.square(svi_variance(k_values, a, b, rho, m, sigma) - impliedVolatilityVals))

    result = optimize.minimize(lossHelper, [0.04, 0.1, -0.7, 0.0, 0.1], bounds=[(0.001, None), (0.001, None), (-0.999, 0.999), (None, None), (0.001, None)])
    return result.x