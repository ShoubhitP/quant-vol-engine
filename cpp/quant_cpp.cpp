#include <cmath>
#include <random>
#include <algorithm>
#include <tuple>
#include <pybind11/pybind11.h>

namespace py = pybind11;

double norm_cdf(double x)
{
    return 0.5 * std::erfc(-x / std::sqrt(2.0));
}

double compute_d1(double S, double K, double vol, double r, double T)
{
    return (std::log(S / K) + ((r + 0.5 * vol * vol) * T)) / (vol * std::sqrt(T));
}

double compute_d2(double d1, double vol, double T)
{
    return d1 - vol * std::sqrt(T);
}

double bs_call_cpp(double S, double K, double vol, double r, double T)
{
    double d1 = compute_d1(S, K, vol, r, T);
    double d2 = compute_d2(d1, vol, T);

    return S * norm_cdf(d1) - K * std::exp(-r * T) * norm_cdf(d2);
}

double bs_put_cpp(double S, double K, double vol, double r, double T)
{
    return bs_call_cpp(S, K, vol, r, T) + K * std::exp(-r * T) - S;
}

double single_stock_price_cpp(
    double stock_price,
    double vol,
    double r,
    double time_to_expiry,
    double z)
{
    return stock_price * std::exp(
                             (r - 0.5 * vol * vol) * time_to_expiry + vol * std::sqrt(time_to_expiry) * z);
}

std::tuple<double, double, double> mc_call_cpp(double stock_price, double strike_price, double vol, double r, double time_to_expiry, int num_simulations)
{
    std::random_device rd;
    std::mt19937 generator(rd());
    std::normal_distribution<double> standard_normal(0.0, 1.0);

    double sum = 0.0;
    double sum_sq = 0.0;

    for (int i = 0; i < num_simulations; i++)
    {
        double z = standard_normal(generator);

        double positive_price = single_stock_price_cpp(
            stock_price, vol, r, time_to_expiry, z);

        double negative_price = single_stock_price_cpp(
            stock_price, vol, r, time_to_expiry, -z);

        double payoff = (std::max(positive_price - strike_price, 0.0) + std::max(negative_price - strike_price, 0.0)) / 2.0;

        sum += payoff;
        sum_sq += payoff * payoff;
    }

    double average_payoff = sum / num_simulations;
    double discount_factor = std::exp(-r * time_to_expiry);

    double sample_variance =
        (sum_sq - num_simulations * average_payoff * average_payoff) / (num_simulations - 1);

    double standard_error = std::sqrt(sample_variance / num_simulations);
    double margin = 1.96 * standard_error * discount_factor;

    double price = average_payoff * discount_factor;
    double lower = price - margin;
    double upper = price + margin;

    return std::make_tuple(price, lower, upper);
}

PYBIND11_MODULE(quant_cpp, m)
{
    m.doc() = "C++ pricing extensions for Quant Vol Engine";

    m.def("bs_call", &bs_call_cpp, "Black-Scholes call price");
    m.def("bs_put", &bs_put_cpp, "Black-Scholes put price");
    m.def("mc_call", &mc_call_cpp, "Monte Carlo call price with antithetic variates");
}