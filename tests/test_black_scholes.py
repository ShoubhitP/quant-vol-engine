import numpy as np
from pricing.black_scholes import black_scholes_call, black_scholes_put

def test_black_scholes_atm_call():
    actual = black_scholes_call(100, 100, 0.2, 0.05, 1)
    expected = 10.4506
    assert abs(actual - expected) < 1e-4

def test_put_call_parity():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1
    call = black_scholes_call(S, K, vol, r, T)
    put = black_scholes_put(S, K, vol, r, T)

    left = call - put
    right = S - K * np.exp(-r * T)

    assert abs(left - right) < 1e-10

def test_call_monotonicity_in_stock_price():
    K, vol, r, T = 100, 0.2, 0.05, 1

    otm = black_scholes_call(50, K, vol, r, T)
    atm = black_scholes_call(100, K, vol, r, T)
    itm = black_scholes_call(150, K, vol, r, T)

    assert itm > atm > otm

def test_option_prices_nonnegative():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1

    assert black_scholes_call(S, K, vol, r, T) >= 0
    assert black_scholes_put(S, K, vol, r, T) >= 0