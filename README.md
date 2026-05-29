# ⬡ Quant Vol Engine

A full-stack quantitative derivatives research platform implementing option pricing, stochastic volatility modeling, volatility surface construction, numerical PDE methods, and calibration to live market data.

Built from scratch using Python, FastAPI, React, and modern numerical methods commonly used in quantitative finance.

**Live Demo:** https://quant-vol-engine.vercel.app

---

# Overview

Most options pricing projects stop at Black-Scholes.

Quant Vol Engine extends significantly further by implementing:

- Black-Scholes pricing and Greeks
- Monte Carlo simulation with variance reduction
- Finite Difference PDE solvers
- Implied volatility extraction
- SVI volatility smile fitting
- Interactive volatility surface visualization
- Heston stochastic volatility pricing
- Heston parameter calibration to live market data
- Numerical validation and convergence analysis
- Runtime benchmarking and performance profiling

The goal of the project is not only to price derivatives, but to study how numerical methods, volatility models, and calibration techniques behave in practice.

---

# Models Implemented

## Black-Scholes

Closed-form option pricing derived from the Black-Scholes PDE.

Implemented Greeks:

- Delta (Δ)
- Gamma (Γ)
- Vega (ν)
- Theta (Θ)
- Rho (ρ)

Higher-order Greeks:

- Vanna
- Volga
- Zomma

---

## Monte Carlo Simulation

Risk-neutral Geometric Brownian Motion simulation using antithetic variates for variance reduction.

Features:

- Variance reduction
- Confidence interval estimation
- Convergence analysis
- Risk-neutral pricing framework

---

## Finite Difference Methods

Numerical PDE solvers for the Black-Scholes equation.

Implemented schemes:

- Explicit Finite Difference
- Implicit Finite Difference
- Crank-Nicolson

Supports:

- European option pricing
- American put pricing

---

## Implied Volatility Extraction

Recovers market-implied volatility by numerically inverting the Black-Scholes model using Brent's root-finding method.

Features:

- Bid-ask filtering
- Intrinsic value validation
- Robust root-finding

---

## SVI Volatility Surface Fitting

Fits the Stochastic Volatility Inspired (SVI) parameterization to implied variance across strikes and expiries.

SVI total variance model:

[
w(k)=a+b\left(\rho(k-m)+\sqrt{(k-m)^2+\sigma^2}\right)
]

where:

- k = log-moneyness
- w = total implied variance

The resulting surface is rendered interactively through Plotly.

---

## Heston Stochastic Volatility Model

Models variance as a stochastic mean-reverting process.

[
dS_t=rS_tdt+\sqrt{v_t}S_tdW_1
]

[
dv_t=\kappa(\theta-v_t)dt+\xi\sqrt{v_t}dW_2
]

Priced using Fourier inversion of the characteristic function (Gil-Pelaez inversion).

Calibrated parameters:

- κ (mean reversion speed)
- θ (long-run variance)
- ξ (volatility of volatility)
- ρ (correlation)
- v₀ (initial variance)

Calibration is performed against live option chains obtained from market data.

---

# Validation & Numerical Analysis

A major focus of this project is verifying that numerical methods are correct, stable, and convergent.

## Automated Testing

The project currently contains:

- 17 automated tests
- Pricing validation
- Greeks validation
- Monte Carlo validation
- Finite difference validation
- Heston validation

Tests verify:

- Black-Scholes benchmark values
- Put-call parity
- Greeks against finite-difference approximations
- Monte Carlo convergence
- Finite Difference convergence
- American put early-exercise behavior
- Heston pricing consistency

All tests currently pass.

---

## Greeks Validation

Analytical Greeks are compared against finite-difference approximations.

Validated quantities:

- Delta
- Gamma
- Vega
- Theta
- Rho

This confirms that closed-form implementations agree with numerical sensitivities.

---

## Monte Carlo Convergence Study

Monte Carlo prices were benchmarked against Black-Scholes analytical solutions across simulation counts ranging from:

- 100
- 1,000
- 10,000
- 100,000
- 1,000,000

Observed behavior:

- Convergence toward analytical values
- Confidence interval shrinkage
- Empirical agreement with O(1/√N) convergence

---

## Finite Difference Convergence Study

Explicit, implicit, and Crank-Nicolson methods were compared against Black-Scholes benchmarks.

Findings:

- Numerical error decreases with grid refinement
- Crank-Nicolson provides the strongest accuracy/stability tradeoff
- Explicit schemes require significantly finer time discretization for stability

---

## Runtime Profiling

All pricing engines were benchmarked to understand computational cost.

| Model              | Average Runtime |
| ------------------ | --------------- |
| Black-Scholes      | 0.00013 s       |
| Full Greeks        | 0.00039 s       |
| Monte Carlo (10k)  | 0.040 s         |
| Monte Carlo (100k) | 0.402 s         |
| Explicit FD        | 0.152 s         |
| Implicit FD        | 0.023 s         |
| Crank-Nicolson     | 0.030 s         |
| Heston Pricing     | 0.006 s         |

---

# Mathematical Foundations

A companion research notebook documents the mathematical foundations underlying the project.

Topics include:

- Itô's Lemma
- Black-Scholes PDE derivation
- Heat Equation transformation
- Girsanov's Theorem
- Risk-neutral pricing
- Feynman-Kac representation
- Monte Carlo interpretation
- Volatility smile construction
- Black-Scholes assumption stress testing

Notebook:

```text
notebooks/mathematical_foundations.ipynb
```

---

# API Endpoints

| Method | Endpoint                     | Description                   |
| ------ | ---------------------------- | ----------------------------- |
| POST   | `/price`                     | Black-Scholes option pricing  |
| POST   | `/greeks`                    | Greeks calculation            |
| POST   | `/monte-carlo`               | Monte Carlo pricing           |
| GET    | `/chain/{ticker}`            | Live option chain             |
| GET    | `/vol-surface/{ticker}`      | IV extraction and SVI fitting |
| POST   | `/heston`                    | Heston pricing                |
| GET    | `/heston-calibrate/{ticker}` | Heston calibration            |

---

# Technology Stack

| Layer               | Technology      |
| ------------------- | --------------- |
| Backend             | FastAPI         |
| Numerical Computing | NumPy, SciPy    |
| Market Data         | yFinance        |
| Frontend            | React           |
| Visualization       | Plotly          |
| Deployment          | Railway, Vercel |

---

# Project Structure

```text
quant-vol-engine/
├── backend/
│
├── pricing/
│   ├── black_scholes.py
│   ├── monte_carlo.py
│   ├── finite_difference.py
│   ├── implied_vol.py
│   ├── svi.py
│   └── heston.py
│
├── research/
│   ├── monte_carlo_convergence.py
│   ├── fd_convergence.py
│   └── profiling.py
│
├── tests/
│   ├── test_black_scholes.py
│   ├── test_greeks.py
│   ├── test_monte_carlo.py
│   ├── test_fd.py
│   └── test_heston.py
│
├── cpp/
│   ├── black_scholes.cpp
│   └── monte_carlo.cpp
│
├── frontend/
│
└── notebooks/
```

---

# Future Work

Planned extensions:

- GARCH volatility forecasting
- Realized volatility engine
- Volatility risk premium analysis
- Implied vs realized volatility forecasting study
- Volatility surface arbitrage detection
- Arbitrage-free SVI calibration
- C++ acceleration via pybind11
- Heston calibration optimization

---

# Author

**Shoubhit Pusuluri**

The Ohio State University
