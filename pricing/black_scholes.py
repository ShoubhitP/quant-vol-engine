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
    return zommaVal - 0
#test
