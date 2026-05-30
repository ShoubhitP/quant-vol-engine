#include <cmath>
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

PYBIND11_MODULE(quant_cpp, m)
{
    m.doc() = "C++ pricing extensions for Quant Vol Engine";

    m.def("bs_call", &bs_call_cpp, "Black-Scholes call price");
    m.def("bs_put", &bs_put_cpp, "Black-Scholes put price");
}