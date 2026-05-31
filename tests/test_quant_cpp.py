import quant_cpp
from pricing.black_scholes import black_scholes_call, black_scholes_put

def test_cpp_bs_call_matches_python():
    cpp_price = quant_cpp.bs_call(100, 100, 0.2, 0.05, 1)
    py_price = black_scholes_call(100, 100, 0.2, 0.05, 1)

    assert abs(cpp_price - py_price) < 1e-8

def test_cpp_bs_put_matches_python():
    cpp_price = quant_cpp.bs_put(100, 100, 0.2, 0.05, 1)
    py_price = black_scholes_put(100, 100, 0.2, 0.05, 1)

    assert abs(cpp_price - py_price) < 1e-8

def test_cpp_mc_call_contains_black_scholes_price():
    price, lower, upper = quant_cpp.mc_call(100, 100, 0.2, 0.05, 1, 100000)
    bs_price = black_scholes_call(100, 100, 0.2, 0.05, 1)

    assert lower <= bs_price <= upper