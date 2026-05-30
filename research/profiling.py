import time
from pricing.black_scholes import (
    black_scholes_call, black_scholes_put, delta_call, delta_put, gammaOption, vegaOption,
    theta_call, theta_put, rho_call, rho_put, vannaOption, volgaOption, zommaOption)
from pricing.monte_carlo import monte_carlo_call
from pricing.finite_difference import explicit_fd_call, implicit_fd_call, crank_nicolson_fd_call
from pricing.heston import heston_fourier_price

S, K, vol, r, T = 100, 100, 0.2, 0.05, 1

def compute_all_greeks():
    return {
        "delta_call": delta_call(S, K, vol, r, T),
        "delta_put": delta_put(S, K, vol, r, T),
        "gamma": gammaOption(S, K, vol, r, T),
        "vega": vegaOption(S, K, vol, r, T),
        "theta_call": theta_call(S, K, vol, r, T),
        "theta_put": theta_put(S, K, vol, r, T),
        "rho_call": rho_call(S, K, vol, r, T),
        "rho_put": rho_put(S, K, vol, r, T),
        "vanna": vannaOption(S, K, vol, r, T),
        "volga": volgaOption(S, K, vol, r, T),
        "zomma": zommaOption(S, K, vol, r, T),
    }

def benchmark(name, fn, runs=5):
    times = []

    for _ in range(runs):
        start = time.perf_counter()
        result = fn()
        end = time.perf_counter()
        times.append(end - start)

    avg_time = sum(times) / len(times)
    print(f"{name:<25} Avg Time: {avg_time:.6f}s")
    return result, avg_time

benchmark("Black Scholes Call: ", lambda: black_scholes_call(S, K, vol, r, T), runs=10)
benchmark("All Greeks: ", lambda: sum(compute_all_greeks().values()), runs=10)
benchmark("Monte Carlo 10k: ", lambda: monte_carlo_call(S, K, vol, r, T, 10000)[0])
benchmark("Monte Carlo 100k: ", lambda: monte_carlo_call(S, K, vol, r, T, 100000)[0], runs=3)
benchmark("Explicit FD Price", lambda: explicit_fd_call(S, K, vol, r, T, 100, 1000), runs=5)
benchmark("Implicit FD Price", lambda: implicit_fd_call(S, K, vol, r, T, 100, 1000), runs=5)
benchmark("Crank-Nicolson Price", lambda: crank_nicolson_fd_call(S, K, vol, r, T, 100, 1000), runs=5)
benchmark("Heston Price", lambda: heston_fourier_price(S, K, T, r, 2, 0.04, 0.3, -0.7, 0.04, "call"), runs=5
)
