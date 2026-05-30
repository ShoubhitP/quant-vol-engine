import time
import quant_cpp
from pricing.black_scholes import black_scholes_call, black_scholes_put

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

    print()
    print(f"Call speedup: {py_call_time / cpp_call_time:.2f}x")
    print(f"Put speedup:  {py_put_time / cpp_put_time:.2f}x")


if __name__ == "__main__":
    main()

