#include <cmath>

double norm_cdf(double x)
{
    return 0.5 * erfc(-x / sqrt(2.0));
}

double compute_d1(double S, double K, double vol, double r, double T)
{
    return (log(S / K) + ((r + 0.5 * (vol * vol)) * T)) / (vol * sqrt(T));
}

double compute_d2(double d1, double vol, double T)
{
    return d1 - vol * sqrt(T);
}

extern "C" double bs_call(double S, double K, double vol, double r, double T)
{
    double d1 = compute_d1(S, K, vol, r, T);
    double d2 = compute_d2(d1, vol, T);
    return S * norm_cdf(d1) - K * exp(-r * T) * norm_cdf(d2);
}

extern "C" double bs_put(double S, double K, double vol, double r, double T)
{
    return bs_call(S, K, vol, r, T) + K * exp(-r * T) - S;
}