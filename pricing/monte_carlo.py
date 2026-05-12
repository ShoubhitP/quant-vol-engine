import numpy as np

def singleStockPrice(initialStock, rFr, vol, timeToExpiry, z_Value):
    
    stock_t = (initialStock * np.exp((rFr - (np.square(vol)/2))*timeToExpiry + (vol*np.sqrt(timeToExpiry)*z_Value)))
    return stock_t

def monte_carlo_call(initialStock, strikePrice, vol, rFr, timeToExpiry, numSimulations):

    averagePayoff = 0
    
    for i in range(numSimulations):
        randomZ = np.random.normal()
        positiveSimulatedPrice = singleStockPrice(initialStock, rFr, vol, timeToExpiry, randomZ)
        negativeSimulatedPrice = singleStockPrice(initialStock, rFr, vol, timeToExpiry, -1*randomZ)
        averagePayoff += (max(positiveSimulatedPrice - strikePrice, 0) + max(negativeSimulatedPrice - strikePrice, 0)) / 2

    averagePayoff /= numSimulations
    return (averagePayoff * np.exp(-1*rFr*timeToExpiry))



def main():
    
    testCall1Val = monte_carlo_call(100, 100, 0.2,0.05, 1, 10)
    print(f"{testCall1Val:.2f} is the monte carlo call price for test 1.")

    testCall2Val = monte_carlo_call(100, 100, 0.2,0.05, 1, 1000)
    print(f"{testCall2Val:.2f} is the monte carlo call price for test 2.")

    testCall3Val = monte_carlo_call(100, 100, 0.2,0.05, 1, 10000)
    print(f"{testCall3Val:.2f} is the monte carlo call price for test 3.")

    testCall4Val = monte_carlo_call(100, 100, 0.2,0.05, 1, 100000)
    print(f"{testCall4Val:.2f} is the monte carlo call price for test 4.")


if __name__ == "__main__":
    main()
