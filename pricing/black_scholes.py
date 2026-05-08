import numpy as np
from scipy.stats import norm

#Takes in S (stock price), K (strike price), Volatility, rFr (risk free rate), and T (time to expiry) and returns call price
def black_scholes_call(stockPrice, strikePrice, vol, rFr, timeToExpiry):

    '''Calculates d1 and d2 using the Black-Scholes formula'''
    d1 = ((np.log(stockPrice/strikePrice)) + (rFr + (np.square(vol)/2))*timeToExpiry)/ (vol*np.sqrt(timeToExpiry))
    d2 = (d1 - (vol*np.sqrt(timeToExpiry)))

    '''Uses norm function from scipy.stats in order to calcullate the CDF of d1 and d2'''
    nD1 = norm.cdf(d1)
    nD2 = norm.cdf(d2)

    '''returning final call price using black-scholes formula'''
    callPrice = (stockPrice * nD1) - (strikePrice * (np.exp(-1 * rFr * timeToExpiry)) * nD2)

    return callPrice

def black_scholes_put(stockPrice, strikePrice, vol, rFr, timeToExpiry):

    putPrice = black_scholes_call(stockPrice, strikePrice, vol, rFr, timeToExpiry) + ((strikePrice)*np.exp(-1*rFr*timeToExpiry)) - stockPrice
    
    return putPrice


def main():
    
    testCall1Val = black_scholes_call(100, 100, 0.2,0.05,1)
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
    print(f"{testPut3Val:.2f} is the put price for test 3.")



main()