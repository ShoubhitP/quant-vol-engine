# ⬡ Quant Vol Engine

A full-stack quantitative derivatives research platform implementing option pricing, stochastic volatility modeling, volatility surface construction, volatility forecasting, numerical PDE methods, and calibration to live market data.

Built from scratch using Python, FastAPI, React, NumPy, SciPy, and modern numerical methods used throughout quantitative finance.

**Live Demo:** https://quant-vol-engine.vercel.app

---

# Overview

Most options pricing projects stop at Black-Scholes.

Quant Vol Engine extends significantly further by implementing:

- Black-Scholes pricing and Greeks
- Monte Carlo simulation with variance reduction
- Finite Difference PDE solvers
- American option pricing
- Implied volatility extraction
- SVI volatility smile fitting
- Interactive volatility surface visualization
- Heston stochastic volatility pricing
- Heston parameter calibration to live market data
- GARCH volatility forecasting
- Realized volatility analysis
- Volatility forecasting backtests
- ATM implied volatility vs GARCH comparisons
- Numerical validation and convergence analysis
- Runtime benchmarking and performance profiling

The goal of the project is not only to price derivatives, but to study how volatility models, numerical methods, and forecasting techniques behave in practice.

---

# Models Implemented

## Black-Scholes

Closed-form option pricing derived from the Black-Scholes PDE.

Implemented Greeks:

### First-Order Greeks

- Delta (Δ)
- Vega (ν)
- Theta (Θ)
- Rho (ρ)

### Second-Order Greeks

- Gamma (Γ)

### Higher-Order Greeks

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
- Statistical error measurement
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

Recovers market-implied volatility by numerically inverting Black-Scholes using Brent's root-finding algorithm.

Features:

- Bid-ask filtering
- Intrinsic value validation
- Robust root-finding
- Live option-chain integration

---

## SVI Volatility Surface Fitting

Fits the Stochastic Volatility Inspired (SVI) parameterization to implied variance across strikes and expiries.

SVI Total Variance Model:

w(k) = a + b(ρ(k − m) + √((k − m)² + σ²))

where:

- k = log-moneyness
- w = total implied variance

The resulting surface is rendered interactively using Plotly.

---

## Heston Stochastic Volatility Model

Models variance as a stochastic mean-reverting CIR process.

dSₜ = rSₜdt + √vₜSₜdW₁

dvₜ = κ(θ − vₜ)dt + ξ√vₜdW₂

Priced using Fourier inversion of the characteristic function (Gil-Pelaez inversion).

Calibrated parameters:

- κ (mean reversion speed)
- θ (long-run variance)
- ξ (volatility of volatility)
- ρ (correlation)
- v₀ (initial variance)

Calibration is performed against live option chains.

---

# Volatility Research Layer

## Realized Volatility Engine

Computes rolling realized volatility from historical log returns.

Supports:

- Historical annualized volatility
- Rolling realized volatility
- Future realized volatility generation for backtesting

---

## GARCH(1,1) Forecasting

Implements volatility forecasting using a GARCH(1,1) process.

Forecasts:

- 1-day volatility
- 5-day volatility
- 10-day volatility
- 30-day volatility

Outputs:

- Forecast volatility term structure
- Model persistence
- Volatility regime information

---

## Volatility Forecast Backtesting

A rolling out-of-sample backtest was performed on SPY.

For each forecast date:

1. Fit GARCH(1,1) using only information available at that time
2. Forecast future volatility
3. Compare against future realized volatility
4. Benchmark against naive alternatives

### Forecast Accuracy

| Model                      | MAE    | RMSE   |
| -------------------------- | ------ | ------ |
| GARCH(1,1)                 | 0.0535 | 0.0847 |
| Naive Current Realized Vol | 0.0536 | 0.0919 |
| Long-Run Historical Vol    | 0.0700 | 0.0886 |

### Result

GARCH slightly outperformed the naive realized-volatility forecast and clearly outperformed the long-run historical volatility baseline, providing an empirical evaluation of forecasting performance rather than assuming model superiority.

---

## ATM IV vs GARCH Comparison

The platform compares:

- Current ATM implied volatility
- GARCH 30-day forecast volatility
- Latest realized volatility

Example:

| Metric                     | Value  |
| -------------------------- | ------ |
| ATM IV                     | 13.10% |
| GARCH 30-Day Forecast      | 14.65% |
| Latest Realized Volatility | 10.01% |

This creates a bridge between options-implied expectations and statistical volatility forecasts.

---

# Validation & Numerical Analysis

## Greeks Validation

Analytical Greeks are validated against finite-difference approximations.

Validated quantities:

- Delta
- Gamma
- Vega
- Theta
- Rho

---

## Monte Carlo Convergence Study

Monte Carlo prices were benchmarked against Black-Scholes analytical solutions using simulation counts ranging from:

- 100
- 1,000
- 10,000
- 100,000
- 1,000,000

Observed behavior:

- Convergence toward analytical values
- Confidence interval shrinkage
- Agreement with O(1/√N) convergence

---

## Finite Difference Convergence Study

Explicit, implicit, and Crank-Nicolson methods were benchmarked against Black-Scholes solutions.

Findings:

- Error decreases under grid refinement
- Crank-Nicolson provides the strongest accuracy/stability tradeoff
- Explicit schemes require stricter stability conditions

---

## Runtime Benchmarking

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

# Automated Testing

The platform currently contains:

- 18+ automated tests
- Pricing validation
- Greeks validation
- Monte Carlo validation
- Finite Difference validation
- Heston validation
- GARCH validation

Tests verify:

- Black-Scholes benchmark values
- Put-call parity
- Greeks against finite-difference approximations
- Monte Carlo convergence
- Finite Difference convergence
- American put early-exercise behavior
- Heston pricing consistency
- Realized volatility calculations

---

# Mathematical Foundations

A companion research notebook documents the mathematical foundations behind the platform.

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

notebooks/mathematical_foundations.ipynb

---

# API Endpoints

| Method | Endpoint                   | Description                            |
| ------ | -------------------------- | -------------------------------------- |
| POST   | /price                     | Black-Scholes option pricing           |
| POST   | /greeks                    | Greeks calculation                     |
| POST   | /monte-carlo               | Monte Carlo pricing                    |
| GET    | /chain/{ticker}            | Live option chain                      |
| GET    | /vol-surface/{ticker}      | IV extraction + SVI fitting            |
| POST   | /heston                    | Heston pricing                         |
| GET    | /heston-calibrate/{ticker} | Heston calibration                     |
| GET    | /vol-snapshot/{ticker}     | Realized volatility + GARCH forecast   |
| GET    | /vol-comparison/{ticker}   | ATM IV vs GARCH vs realized volatility |

---

# Technology Stack

| Layer               | Technology      |
| ------------------- | --------------- |
| Backend             | FastAPI         |
| Numerical Computing | NumPy, SciPy    |
| Volatility Modeling | ARCH            |
| Market Data         | yFinance        |
| Frontend            | React           |
| Visualization       | Plotly          |
| Deployment          | Railway, Vercel |

---

# Project Structure

quant-vol-engine/

├── backend/

├── pricing/
│ ├── black_scholes.py
│ ├── monte_carlo.py
│ ├── finite_difference.py
│ ├── implied_vol.py
│ ├── svi.py
│ └── heston.py

├── models/
│ ├── garch.py
│ └── implied_vol_snapshot.py

├── research/
│ ├── monte_carlo_convergence.py
│ ├── fd_convergence.py
│ ├── profiling.py
│ └── garch_backtest.py

├── tests/
│ ├── test_black_scholes.py
│ ├── test_greeks.py
│ ├── test_monte_carlo.py
│ ├── test_fd.py
│ ├── test_heston.py
│ └── test_garch.py

├── cpp/
│ ├── black_scholes.cpp
│ └── monte_carlo.cpp

├── frontend/

└── notebooks/

---

# Future Work

- Volatility surface arbitrage detection
- Arbitrage-free SVI calibration
- Volatility risk premium analysis
- Historical IV forecasting studies
- pybind11 C++ acceleration
- Heston calibration optimization

---

# Author

**Shoubhit Pusuluri**

Computer Science & Engineering + Mathematics
The Ohio State University
