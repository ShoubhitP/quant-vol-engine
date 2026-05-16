import numpy as np
from scipy import integrate, optimize
from pricing.black_scholes import black_scholes_call

def heston_char_func(u, S, K, T, r, kappa, theta, xi, rho, v0):
    forwardPrice = S * np.exp(r * T)
    d = np.sqrt(np.square((rho * xi * (u*1j)) - kappa) + np.square(xi) * (u*1j + np.square(u)))
    g = (kappa - (rho*xi*(u*1j)) - d) / (kappa - (rho*xi*(u*1j)) + d)
    charFunction = np.exp(1j * u * np.log(forwardPrice) + (kappa * theta / xi**2) * ((kappa - rho * xi * u * 1j - d) * T - 2 * np.log((1 - g * np.exp(-d * T)) / (1 - g))) + (v0 / xi**2) * (kappa - rho * xi * u * 1j - d) * ((1 - np.exp(-d * T)) / (1 - g * np.exp(-d * T))))
    return charFunction

def heston_fourier_price(S, K, T, r, kappa, theta, xi, rho, v0, option_type="call", N=100):
    F = S * np.exp(r * T)

    def P(phi_sign):
        def integrand(u):
            phi = heston_char_func(u - phi_sign * 1j, S, K, T, r, kappa, theta, xi, rho, v0)
            phi_denom = heston_char_func(-phi_sign * 1j, S, K, T, r, kappa, theta, xi, rho, v0)
            return np.real(np.exp(-1j * u * np.log(K)) * phi / (phi_denom * 1j * u))
        result, _ = integrate.quad(integrand, 1e-6, 200, limit=200)
        return 0.5 + result / np.pi

    P1 = P(1)
    P2 = P(0)
    callPrice = S * P1 - K * np.exp(-r * T) * P2

    if option_type == "call":
        return callPrice
    else:
        return callPrice - S + K * np.exp(-r * T)

def calibrate_heston(strikes, expiries, ivs, S, r):
    market_prices = []
    for strike, expiry, iv in zip(strikes, expiries, ivs):
        market_prices.append(black_scholes_call(S, strike, iv, r, expiry))

    def loss(params):
        heston_prices = []
        kappa, theta, xi, rho, v0 = params
        for strike, expiry in zip(strikes, expiries):
            heston_prices.append(heston_fourier_price(S, strike, expiry, r, kappa, theta, xi, rho, v0, "call"))
        return np.sum(np.square(np.array(heston_prices) - np.array(market_prices)))

    result = optimize.minimize(loss, [2, 0.04, 0.3, -0.7, 0.04], bounds=[(0.001, None), (0.001, None), (0.001, None), (-0.999, 0.999), (0.001, None)])
    return result.x 

def main():
    testCall1Val = heston_fourier_price(100, 100, 1, 0.05, 2, 0.04, 0.3, -0.7, 0.04, "call", 100)
    print(f"{testCall1Val:.2f} is the call price for test 1.")
    testPutVal = heston_fourier_price(100, 100, 1, 0.05, 2, 0.04, 0.3, -0.7, 0.04, "put", 100)
    print(f"{testPutVal:.2f} is the put price for test 2.")

if __name__ == "__main__":
    main()