#include <random>
#include <vector>
#include <algorithm>

/*
Loop N simulations
Generate random Z from normal distribution
Compute positive and negative stock paths (antithetic variates)
Compute payoff for each
Average and discount
*/
extern "C" double singleStockPrice(double stockPrice, double strikePrice, double vol, double r, double timeToExpiry, double Z)
{

    return stockPrice * exp((r - ((vol * vol) / 2)) * timeToExpiry + (vol * sqrt(timeToExpiry) * Z));
}

extern "C" void mc_call(double stockPrice, double strikePrice, double vol, double r, double timeToExpiry, int numSimulations, double *price, double *lower, double *upper)
{

    std::random_device rd;
    std::mt19937 generator(rd());
    std::normal_distribution<double> standard_normal(0.0, 1.0);

    double sum = 0.0;
    double sum_sq = 0.0;

    for (int i = 0; i < numSimulations; i++)
    {
        double Z = standard_normal(generator);
        double positiveSimulatedPrice = singleStockPrice(stockPrice, strikePrice, vol, r, timeToExpiry, Z);
        double negativeSimulatedPrice = singleStockPrice(stockPrice, strikePrice, vol, r, timeToExpiry, -1 * Z);
        double payoff = (std::max(positiveSimulatedPrice - strikePrice, 0.0) + std::max(negativeSimulatedPrice - strikePrice, 0.0)) / 2;
        sum += payoff;
        sum_sq += payoff * payoff;
    }

    double averagePayoff = sum / numSimulations;
    double discountFactor = exp((-1 * r * timeToExpiry));
    double sampleVariance = (sum_sq - numSimulations * averagePayoff * averagePayoff) / (numSimulations - 1);
    double standardError = sqrt(sampleVariance / numSimulations);

    double margin = 1.96 * standardError * discountFactor;
    *price = averagePayoff * discountFactor;
    *lower = *price - margin;
    *upper = *price + margin;
}
