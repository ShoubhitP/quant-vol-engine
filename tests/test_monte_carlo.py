from pricing.black_scholes import black_scholes_call
from pricing.monte_carlo import monte_carlo_call

def test_monte_carlo_close_to_black_scholes():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1

    bs_price = black_scholes_call(S, K, vol, r, T)
    mc_price, lower, upper = monte_carlo_call(S, K, vol, r, T, 100000)

    assert abs(mc_price - bs_price) < 0.20

def test_monte_carlo_confidence_interval_contains_price():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1

    price, lower, upper = monte_carlo_call(S, K, vol, r, T, 10000)

    assert lower < price < upper