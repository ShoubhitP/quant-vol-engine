import numpy as np

def singleStockPrice(initialStock, rFr, vol, timeToExpiry, z_Value):
    
    stock_t = (initialStock * np.exp((rFr - (np.square(vol)/2))*timeToExpiry + (vol*np.sqrt(timeToExpiry)*z_Value)))
    return stock_t

def monte_carlo_call(initialStock, strikePrice, vol, rFr, timeToExpiry, numSimulations):

    payoffs = []
    
    for i in range(numSimulations):
        randomZ = np.random.normal()
        positiveSimulatedPrice = singleStockPrice(initialStock, rFr, vol, timeToExpiry, randomZ)
        negativeSimulatedPrice = singleStockPrice(initialStock, rFr, vol, timeToExpiry, -1*randomZ)
        payoff = (max(positiveSimulatedPrice - strikePrice, 0) + max(negativeSimulatedPrice - strikePrice, 0)) / 2
        payoffs.append(payoff)
    
    payoffs = np.array(payoffs)
    discountFactor = np.exp(-1*rFr*timeToExpiry)
    price = np.mean(payoffs) * discountFactor
    std = np.std(payoffs) * discountFactor
    margin = 1.96 * std / np.sqrt(numSimulations)
    
    return price, price - margin, price + margin

def main():

    price, lower, upper = monte_carlo_call(100, 100, 0.2, 0.05, 1, 10)
    print(f"{price:.2f} is the monte carlo call price for test 1. CI: [{lower:.2f}, {upper:.2f}]")
    price, lower, upper = monte_carlo_call(100, 100, 0.2, 0.05, 1, 1000)
    print(f"{price:.2f} is the monte carlo call price for test 2. CI: [{lower:.2f}, {upper:.2f}]")
    price, lower, upper = monte_carlo_call(100, 100, 0.2, 0.05, 1, 10000)
    print(f"{price:.2f} is the monte carlo call price for test 3. CI: [{lower:.2f}, {upper:.2f}]")
    price, lower, upper = monte_carlo_call(100, 100, 0.2, 0.05, 1, 100000)
    print(f"{price:.2f} is the monte carlo call price for test 4. CI: [{lower:.2f}, {upper:.2f}]")


if __name__ == "__main__":
    main()
