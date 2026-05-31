import time
import quant_cpp
from pricing.black_scholes import black_scholes_call, black_scholes_put
from pricing.monte_carlo import monte_carlo_call

S, K, vol, r, T = 100, 100, 0.2, 0.05, 1

def benchmark(name, fn, runs=100_000):
    start = time.perf_counter()
    for _ in range(runs):
        fn()
    elapsed = time.perf_counter() - start
    print(f"{name:<25} {elapsed:.6f}s")
    return elapsed

def main():
    runs = 100_000
    py_call_time = benchmark("Python BS Call", lambda: black_scholes_call(S,K,vol,r,T), runs,)
    cpp_call_time = benchmark("C++ BS Call", lambda: quant_cpp.bs_call(S,K,vol,r,T), runs,)
    py_put_time = benchmark("Python BS Put", lambda: black_scholes_put(S,K,vol,r,T), runs,)
    cpp_put_time = benchmark("C++ BS Put", lambda: quant_cpp.bs_put(S,K,vol,r,T), runs,)

    py_mc_time = benchmark("Python MC 100k",lambda: monte_carlo_call(S, K, vol, r, T, 100_000)[0],runs=10,)
    cpp_mc_time = benchmark("C++ MC 100k",lambda: quant_cpp.mc_call(S, K, vol, r, T, 100_000)[0],runs=10,)
    print(f"Monte Carlo speedup: {py_mc_time / cpp_mc_time:.2f}x")

    print()
    print(f"Call speedup: {py_call_time / cpp_call_time:.2f}x")
    print(f"Put speedup:  {py_put_time / cpp_put_time:.2f}x")


if __name__ == "__main__":
    main()

