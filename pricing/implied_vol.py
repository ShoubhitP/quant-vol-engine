from scipy import optimize
import numpy as np
from pricing.black_scholes import black_scholes_call, black_scholes_put

def extract_iv(market_price, S, K, T, r, option_type="call"):
    if option_type == "call":
        if (market_price * 2) <= 0:
            return np.nan
        if market_price <= max(S-K, 0):
            return np.nan
        try:
            root = optimize.brentq(lambda sigma: black_scholes_call(S, K, sigma, r, T) - market_price, 0.01, 10.0)
            return root
        except:
            return np.nan
    if option_type == "put":
        if (market_price * 2) <= 0:
            return np.nan
        if market_price <= max(K-S, 0):
            return np.nan
        try:
            root = optimize.brentq(lambda sigma: black_scholes_put(S, K, sigma, r, T) - market_price, 0.01, 10.0)
            return root
        except:
            return np.nan