from pricing.heston import heston_fourier_price

def test_heston_price_positive():
    price = heston_fourier_price(
        S=100,
        K=100,
        T=1,
        r=0.05,
        kappa=2,
        theta=0.04,
        xi=0.3,
        rho=-0.7,
        v0=0.04,
        option_type="call"
    )

    assert price > 0

def test_heston_put_call_parity():
    S, K, T, r = 100, 100, 1, 0.05
    kappa, theta, xi, rho, v0 = 2, 0.04, 0.3, -0.7, 0.04

    call = heston_fourier_price(S, K, T, r, kappa, theta, xi, rho, v0, "call")
    put = heston_fourier_price(S, K, T, r, kappa, theta, xi, rho, v0, "put")

    left = call - put
    right = S - K * __import__("numpy").exp(-r * T)

    assert abs(left - right) < 1e-4