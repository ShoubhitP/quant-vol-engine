import numpy as np

def singleStockPrice(initialStock, rFr, vol, timeToExpiry):
    
    randomDraw = np.random.normal()
    stock_t = (initialStock * np.exp((rFr - (np.square(vol)/2))*timeToExpiry + (vol*np.sqrt(timeToExpiry)*randomDraw)))
    return stock_t

def monte_carlo_call(initialStock, strikePrice, vol, rFr, timeToExpiry, numSimulations):

    callPayoff = 0
    averagePayoff = 0

    for i in range(numSimulations):
        simulatedPrice = singleStockPrice(initialStock, rFr, vol, timeToExpiry)
        averagePayoff += max(simulatedPrice - strikePrice, 0)

    averagePayoff /= numSimulations
    return (averagePayoff * np.exp(-1*rFr*timeToExpiry))



def main():
    
    for i in range(5):
        testPrice = singleStockPrice(100,0.05,0.2,1)
        print(f"{testPrice:.2f} is a sample stock price at time T.")

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


    
