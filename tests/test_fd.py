from pricing.black_scholes import black_scholes_call, black_scholes_put
from pricing.finite_difference import (
    explicit_fd_call,
    implicit_fd_call,
    crank_nicolson_fd_call,
    american_put_cn,
)

def test_explicit_fd_close_to_black_scholes():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1

    bs = black_scholes_call(S, K, vol, r, T)
    fd = explicit_fd_call(S, K, vol, r, T, N=100, M=1000)

    assert abs(fd - bs) < 0.10

def test_implicit_fd_close_to_black_scholes():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1

    bs = black_scholes_call(S, K, vol, r, T)
    fd = implicit_fd_call(S, K, vol, r, T, N=100, M=1000)

    assert abs(fd - bs) < 0.10

def test_crank_nicolson_close_to_black_scholes():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1

    bs = black_scholes_call(S, K, vol, r, T)
    fd = crank_nicolson_fd_call(S, K, vol, r, T, N=100, M=1000)

    assert abs(fd - bs) < 0.10

def test_american_put_at_least_european_put():
    S, K, vol, r, T = 100, 100, 0.2, 0.05, 1

    european = black_scholes_put(S, K, vol, r, T)
    american = american_put_cn(S, K, vol, r, T, N=100, M=1000)

    assert american >= european