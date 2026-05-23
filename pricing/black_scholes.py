import numpy as np
from scipy.stats import norm

#Takes in S (stock price), K (strike price), Volatility, rFr (risk free rate), and T (time to expiry) and returns call price
def compute_d1_and_d2(stockPrice, strikePrice, vol, rFr, timeToExpiry):

    d1 = ((np.log(stockPrice/strikePrice)) + (rFr + (np.square(vol)/2))*timeToExpiry)/ (vol*np.sqrt(timeToExpiry))
    d2 = (d1 - (vol*np.sqrt(timeToExpiry)))
    return d1, d2

def black_scholes_call(stockPrice, strikePrice, vol, rFr, timeToExpiry):

    '''Calculates d1 and d2 using the Black-Scholes formula'''
    d1, d2 = compute_d1_and_d2(stockPrice, strikePrice, vol, rFr, timeToExpiry)

    '''Uses norm function from scipy.stats in order to calculate the CDF of d1 and d2'''
    nD1 = norm.cdf(d1)
    nD2 = norm.cdf(d2)

    '''returning final call price using black-scholes formula'''
    callPrice = (stockPrice * nD1) - (strikePrice * (np.exp(-1 * rFr * timeToExpiry)) * nD2)

    return callPrice

def black_scholes_put(stockPrice, strikePrice, vol, rFr, timeToExpiry):

    putPrice = black_scholes_call(stockPrice, strikePrice, vol, rFr, timeToExpiry) + ((strikePrice)*np.exp(-1*rFr*timeToExpiry)) - stockPrice
    
    return putPrice

def delta_call(stockPrice, strikePrice, vol, rFr, timeToExpiry):

    d1, _ = compute_d1_and_d2(stockPrice, strikePrice, vol, rFr, timeToExpiry)
    nD1 = norm.cdf(d1)
    return nD1

def delta_put(stockPrice, strikePrice, vol, rFr, timeToExpiry):

    d1, _ = compute_d1_and_d2(stockPrice, strikePrice, vol, rFr, timeToExpiry)
    nD1 = norm.cdf(d1)
    return (nD1 - 1)

def gammaOption(stockPrice, strikePrice, vol, rfr, timeToExpiry):
    d1, _ = compute_d1_and_d2(stockPrice, strikePrice, vol, rfr, timeToExpiry)
    n_D1 = norm.pdf(d1)
    gammaVal = n_D1 / (stockPrice * vol*np.sqrt(timeToExpiry))
    return gammaVal

def vegaOption(stockPrice, strikePrice, vol, rfr, timeToExpiry):
    d1, _ = compute_d1_and_d2(stockPrice, strikePrice, vol, rfr, timeToExpiry)
    n_D1 = norm.pdf(d1)
    vegaVal = stockPrice * n_D1 * np.sqrt(timeToExpiry)
    return vegaVal

def theta_call(stockPrice, strikePrice, vol, rfr, timeToExpiry):
    d1, d2 = compute_d1_and_d2(stockPrice, strikePrice, vol, rfr, timeToExpiry)
    n_D1 = norm.pdf(d1)
    n_D2 = norm.cdf(d2)
    theta_Val = -1*((stockPrice * n_D1 * vol)/(2*np.sqrt(timeToExpiry))) - (rfr * strikePrice * np.exp(-1*rfr*timeToExpiry) * n_D2)
    return theta_Val / 365


def theta_put(stockPrice, strikePrice, vol, rfr, timeToExpiry):
    d1, d2 = compute_d1_and_d2(stockPrice, strikePrice, vol, rfr, timeToExpiry)
    n_D1 = norm.pdf(d1)
    n_D2 = norm.cdf(-d2)
    theta_Val = -1*((stockPrice * n_D1 * vol)/(2*np.sqrt(timeToExpiry))) + (rfr * strikePrice * np.exp(-1*rfr*timeToExpiry) * n_D2)
    return theta_Val / 365

def rho_call(stockPrice, strikePrice, vol, rfr, timeToExpiry):

    _, d2 = compute_d1_and_d2(stockPrice, strikePrice, vol, rfr, timeToExpiry)
    n_D2 = norm.cdf(d2)
    rho_Val = strikePrice*timeToExpiry*np.exp(-1*rfr*timeToExpiry) * n_D2
    return rho_Val

def rho_put(stockPrice, strikePrice, vol, rfr, timeToExpiry):

    _, d2 = compute_d1_and_d2(stockPrice, strikePrice, vol, rfr, timeToExpiry)
    n_D2 = norm.cdf(-d2)
    rho_Val = -1*strikePrice*timeToExpiry*np.exp(-1*rfr*timeToExpiry) * n_D2
    return rho_Val

def vannaOption(stockPrice, strikePrice, vol, rfr, timeToExpiry):
    d1, d2 = compute_d1_and_d2(stockPrice, strikePrice, vol, rfr, timeToExpiry)
    n_D1 = norm.pdf(d1)
    vannaVal = -1*n_D1*(d2/vol)
    return vannaVal

def volgaOption(stockPrice, strikePrice, vol, rfr, timeToExpiry):
    d1, d2 = compute_d1_and_d2(stockPrice, strikePrice, vol, rfr, timeToExpiry)
    volgaVal = vegaOption(stockPrice, strikePrice, vol, rfr, timeToExpiry) * ((d1*d2)/vol)
    return volgaVal

def zommaOption(stockPrice, strikePrice, vol, rfr, timeToExpiry):
    d1, d2 = compute_d1_and_d2(stockPrice, strikePrice, vol, rfr, timeToExpiry)
    zommaVal = gammaOption(stockPrice, strikePrice, vol, rfr, timeToExpiry) * (((d1*d2)-1)/vol)
    return zommaVal

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


def main():
    
    '''testCall1Val = black_scholes_call(100, 100, 0.2,0.05,1)
    print(f"{testCall1Val:.2f} is the call price for test 1.")

    testCall2Val = black_scholes_call(150, 100, 0.2,0.05,1)
    print(f"{testCall2Val:.2f} is the call price for test 2.")

    testCall3Val = black_scholes_call(50, 100, 0.2, 0.05, 1)
    print(f"{testCall3Val:.2f} is the call price for test 3.")

    testPut1Val = black_scholes_put(100,100,0.2, 0.05, 1)
    print(f"{testPut1Val:.2f} is the put price for test 1.")

    testPut2Val = black_scholes_put(150,100,0.2, 0.05, 1)
    print(f"{testPut2Val:.2f} is the put price for test 2.")

    testPut3Val = black_scholes_put(50,100,0.2, 0.05, 1)
    print(f"{testPut3Val:.2f} is the put price for test 3.")'''

   # Delta Tests
    testDeltaCall1 = delta_call(100, 100, 0.2, 0.05, 1)
    print(f"{testDeltaCall1:.4f} is the call delta for test 1 (ATM).")
    testDeltaCall2 = delta_call(150, 100, 0.2, 0.05, 1)
    print(f"{testDeltaCall2:.4f} is the call delta for test 2 (ITM).")
    testDeltaCall3 = delta_call(50, 100, 0.2, 0.05, 1)
    print(f"{testDeltaCall3:.4f} is the call delta for test 3 (OTM).")

    testDeltaPut1 = delta_put(100, 100, 0.2, 0.05, 1)
    print(f"{testDeltaPut1:.4f} is the put delta for test 1 (ATM).")
    testDeltaPut2 = delta_put(150, 100, 0.2, 0.05, 1)
    print(f"{testDeltaPut2:.4f} is the put delta for test 2 (ITM).")
    testDeltaPut3 = delta_put(50, 100, 0.2, 0.05, 1)
    print(f"{testDeltaPut3:.4f} is the put delta for test 3 (OTM).")

    # Gamma Tests
    testGamma1 = gammaOption(100, 100, 0.2, 0.05, 1)
    print(f"{testGamma1:.4f} is the gamma for test 1 (ATM).")
    testGamma2 = gammaOption(150, 100, 0.2, 0.05, 1)
    print(f"{testGamma2:.4f} is the gamma for test 2 (ITM).")
    testGamma3 = gammaOption(50, 100, 0.2, 0.05, 1)
    print(f"{testGamma3:.4f} is the gamma for test 3 (OTM).")

    # Vega Tests
    testVega1 = vegaOption(100, 100, 0.2, 0.05, 1)
    print(f"{testVega1:.4f} is the vega for test 1 (ATM).")
    testVega2 = vegaOption(150, 100, 0.2, 0.05, 1)
    print(f"{testVega2:.4f} is the vega for test 2 (ITM).")
    testVega3 = vegaOption(50, 100, 0.2, 0.05, 1)
    print(f"{testVega3:.4f} is the vega for test 3 (OTM).")

    # Theta Tests
    testThetaCall1 = theta_call(100, 100, 0.2, 0.05, 1)
    print(f"{testThetaCall1:.4f} is the call theta for test 1 (ATM).")
    testThetaCall2 = theta_call(150, 100, 0.2, 0.05, 1)
    print(f"{testThetaCall2:.4f} is the call theta for test 2 (ITM).")
    testThetaCall3 = theta_call(50, 100, 0.2, 0.05, 1)
    print(f"{testThetaCall3:.4f} is the call theta for test 3 (OTM).")

    testThetaPut1 = theta_put(100, 100, 0.2, 0.05, 1)
    print(f"{testThetaPut1:.4f} is the put theta for test 1 (ATM).")
    testThetaPut2 = theta_put(150, 100, 0.2, 0.05, 1)
    print(f"{testThetaPut2:.4f} is the put theta for test 2 (ITM).")
    testThetaPut3 = theta_put(50, 100, 0.2, 0.05, 1)
    print(f"{testThetaPut3:.4f} is the put theta for test 3 (OTM).")

    # Rho Tests
    testRhoCall1 = rho_call(100, 100, 0.2, 0.05, 1)
    print(f"{testRhoCall1:.4f} is the call rho for test 1 (ATM).")
    testRhoCall2 = rho_call(150, 100, 0.2, 0.05, 1)
    print(f"{testRhoCall2:.4f} is the call rho for test 2 (ITM).")
    testRhoCall3 = rho_call(50, 100, 0.2, 0.05, 1)
    print(f"{testRhoCall3:.4f} is the call rho for test 3 (OTM).")

    testRhoPut1 = rho_put(100, 100, 0.2, 0.05, 1)
    print(f"{testRhoPut1:.4f} is the put rho for test 1 (ATM).")
    testRhoPut2 = rho_put(150, 100, 0.2, 0.05, 1)
    print(f"{testRhoPut2:.4f} is the put rho for test 2 (ITM).")
    testRhoPut3 = rho_put(50, 100, 0.2, 0.05, 1)
    print(f"{testRhoPut3:.4f} is the put rho for test 3 (OTM).")

    # Vanna Tests
    testVanna1 = vannaOption(100, 100, 0.2, 0.05, 1)
    print(f"{testVanna1:.4f} is the vanna for test 1 (ATM).")
    testVanna2 = vannaOption(150, 100, 0.2, 0.05, 1)
    print(f"{testVanna2:.4f} is the vanna for test 2 (ITM).")
    testVanna3 = vannaOption(50, 100, 0.2, 0.05, 1)
    print(f"{testVanna3:.4f} is the vanna for test 3 (OTM).")

    # Volga Tests
    testVolga1 = volgaOption(100, 100, 0.2, 0.05, 1)
    print(f"{testVolga1:.4f} is the volga for test 1 (ATM).")
    testVolga2 = volgaOption(150, 100, 0.2, 0.05, 1)
    print(f"{testVolga2:.4f} is the volga for test 2 (ITM).")
    testVolga3 = volgaOption(50, 100, 0.2, 0.05, 1)
    print(f"{testVolga3:.4f} is the volga for test 3 (OTM).")

    # Zomma Tests
    testZomma1 = zommaOption(100, 100, 0.2, 0.05, 1)
    print(f"{testZomma1:.4f} is the zomma for test 1 (ATM).")
    testZomma2 = zommaOption(150, 100, 0.2, 0.05, 1)
    print(f"{testZomma2:.4f} is the zomma for test 2 (ITM).")
    testZomma3 = zommaOption(50, 100, 0.2, 0.05, 1)
    print(f"{testZomma3:.4f} is the zomma for test 3 (OTM).")

    validateGreeks(100,100,0.2,0.05,1)

main()