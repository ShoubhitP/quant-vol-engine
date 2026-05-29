import numpy as np
from pricing.black_scholes import (
    black_scholes_call,
    delta_call,
    gammaOption,
    vegaOption,
    theta_call,
    rho_call,
)

def finite_diff_delta(S, K, vol, r, T, eps=1e-4):
    return (
        black_scholes_call(S + eps, K, vol, r, T)
        - black_scholes_call(S - eps, K, vol, r, T)
    ) / (2 * eps)

def finite_diff_gamma(S, K, vol, r, T, eps=1e-3):
    return (
        black_scholes_call(S + eps, K, vol, r, T)
        - 2 * black_scholes_call(S, K, vol, r, T)
        + black_scholes_call(S - eps, K, vol, r, T)
    ) / (eps ** 2)

def finite_diff_vega(S, K, vol, r, T, eps=1e-4):
    return (
        black_scholes_call(S, K, vol + eps, r, T)
        - black_scholes_call(S, K, vol - eps, r, T)
    ) / (2 * eps)

def finite_diff_rho(S, K, vol, r, T, eps=1e-4):
    return (
        black_scholes_call(S, K, vol, r + eps, T)
        - black_scholes_call(S, K, vol, r - eps, T)
    ) / (2 * eps)

def test_delta_matches_finite_difference():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1
    assert abs(delta_call(S, K, vol, r, T) - finite_diff_delta(S, K, vol, r, T)) < 1e-4

def test_gamma_matches_finite_difference():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1
    assert abs(gammaOption(S, K, vol, r, T) - finite_diff_gamma(S, K, vol, r, T)) < 1e-4

def test_vega_matches_finite_difference():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1
    assert abs(vegaOption(S, K, vol, r, T) - finite_diff_vega(S, K, vol, r, T)) < 1e-4

def test_rho_matches_finite_difference():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1
    assert abs(rho_call(S, K, vol, r, T) - finite_diff_rho(S, K, vol, r, T)) < 1e-3

def test_greek_signs():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1

    assert delta_call(S, K, vol, r, T) > 0
    assert gammaOption(S, K, vol, r, T) > 0
    assert vegaOption(S, K, vol, r, T) > 0
    assert theta_call(S, K, vol, r, T) < 0
    assert rho_call(S, K, vol, r, T) > 0