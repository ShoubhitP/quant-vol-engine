import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pricing.black_scholes import black_scholes_call, black_scholes_put, delta_call, delta_put, gammaOption, vegaOption, theta_call, theta_put, rho_call, rho_put, vannaOption, volgaOption, zommaOption
from pricing.monte_carlo import monte_carlo_call

def fd_delta(S, K, vol, r, T, eps=0.01):

    return ((black_scholes_call(S+eps, K, vol, r, T) - black_scholes_call(S-eps, K, vol, r, T)) / (2*eps))

def fd_gamma(S, K, vol, r, T, eps = 0.01):
    return (((black_scholes_call(S+eps, K, vol, r, T) - (2*black_scholes_call(S,K,vol,r,T)) + black_scholes_call(S-eps,K, vol, r, T))) / (np.square(eps)))

def fd_vega(S, K, vol, r, T, eps=0.01):
    return ((black_scholes_call(S,K,vol+eps,r,T)) - black_scholes_call(S,K,vol-eps,r,T)) / (2*eps)

def fd_theta(S, K, vol, r, T, eps=0.01):
    return ((black_scholes_call(S,K,vol,r,T-eps,)) - black_scholes_call(S,K,vol,r,T+eps)) / (730*eps)

def fd_rho(S, K, vol, r, T, eps = 0.01):
    return ((black_scholes_call(S,K,vol,r+eps,T) - black_scholes_call(S,K,vol,r-eps,T))) / (2*eps)

def validateGreeks(S, K, vol, r, T):
    
    greeks = [
        ("Delta", delta_call(S, K, vol, r, T), fd_delta(S, K, vol, r, T, 0.01)),
        ("Gamma", gammaOption(S, K, vol, r, T), fd_gamma(S, K, vol, r, T, 0.01)),
        ("Vega",  vegaOption(S, K, vol, r, T), fd_vega(S, K, vol, r, T, 0.01)),
        ("Theta", theta_call(S, K, vol, r, T), fd_theta(S, K, vol, r, T, 0.01)),
        ("Rho",   rho_call(S, K, vol, r, T), fd_rho(S, K, vol, r, T, 0.01)),
    ]

    for name, analytical, fd in greeks:
        diff = analytical - fd
        print(f"{name:<6} Analytical = {analytical:.4f}  |  FD = {fd:.4f}  |  Diff = {diff:.4f}")

def validate_parity(S, K, vol, r, T):

    bsCallPrice = black_scholes_call(S,K,vol,r,T)
    bsPutPrice = black_scholes_put(S,K,vol,r,T)
    leftSide = bsCallPrice - bsPutPrice
    rightSide = S - K*np.exp(-1*r*T)
    print(f"Put-Call Parity:  Left Side = {leftSide:.4f}  |  Right Side = {rightSide:.4f}  |  Diff = {leftSide-rightSide:.4f}")

def plot_mc_convergence(S, K, vol, r, T):

    numSimulations = [10,100,1000,10000,100000]
    mcPrice = []
    bsPrice = black_scholes_call(S,K,vol,r,T)
    for num in numSimulations:
        price,lower,upper = monte_carlo_call(S,K,vol,r,T,num)
        mcPrice.append(price)

    plt.plot(numSimulations, mcPrice, label="Monte Carlo Price vs Number of Simulations")
    plt.axhline(y=bsPrice, color='r', label="Black Scholes Fixed Price")
    plt.xscale('log')
    plt.xlabel("Number of Simulations")
    plt.ylabel("Option Price")  
    plt.title("Monte Carlo Price vs Number of Simulations")
    plt.legend()
    plt.show()

def main():

    validateGreeks(100,100,0.2,0.05,1)
    validate_parity(100, 100, 0.2, 0.05, 1)
    validate_parity(120, 100, 0.2, 0.05, 1)
    validate_parity(80, 100, 0.2, 0.05, 1)
    plot_mc_convergence(100,100,0.2,0.05,1)

main()

