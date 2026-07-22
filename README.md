# Quant Vol Engine

> A quantitative derivatives research platform for option pricing, volatility modeling, volatility surface construction, arbitrage diagnostics, volatility forecasting, and high-performance pricing engines.

Built to explore the mathematics, numerical methods, and software engineering behind modern derivatives trading systems through production-style implementations of pricing models, calibration routines, empirical volatility research, and C++ acceleration.

---

# Live Demo

**Frontend:** https://quant-vol-engine.vercel.app

**Backend API (Swagger Docs):** https://quant-vol-engine-production.up.railway.app/docs

**GitHub Repository:** https://github.com/ShoubhitP/quant-vol-engine

**Deployment:** React (Vercel) • FastAPI (Railway) • C++ Extensions (pybind11)

# Overview

Quant Vol Engine combines classical derivatives pricing models with modern volatility research workflows.

The platform supports:

- Black-Scholes pricing and Greeks
- Monte Carlo simulation with variance reduction
- Finite Difference methods for American options
- Heston stochastic volatility pricing
- Implied volatility extraction
- SVI volatility surface calibration
- Volatility surface arbitrage diagnostics
- GARCH volatility forecasting
- Volatility Risk Premium research
- C++ pricing acceleration using pybind11
- Interactive React dashboard

Unlike many educational pricing calculators, this project emphasizes:

- Numerical validation
- Calibration quality
- Empirical research
- Performance benchmarking
- Production-style architecture

---

# Volatility Risk Premium Research

Using approximately **1,225 trading days** of SPY and VIX data from 2021–2026, the project investigated whether implied volatility systematically differs from subsequently realized volatility.

## Research Question

Does the market systematically overprice future volatility?

Defined as:

```text
VRP = Implied Volatility − Future Realized Volatility
```

## Key Results

| Metric                 |           Result |
| ---------------------- | ---------------: |
| Mean VRP               | +3.58 vol points |
| Median VRP             | +4.12 vol points |
| Positive VRP Frequency |           84.24% |
| Corr(IV, Future RV)    |           0.6095 |

## Distribution of Volatility Risk Premium

![VRP Distribution](docs/images/vrp_distribution.png)

## Findings

The study found:

- Implied volatility exceeded subsequent realized volatility on **84.24%** of trading days.
- Implied volatility contained meaningful predictive information regarding future realized volatility.
- Market participants consistently paid a premium for volatility exposure and downside protection.
- The volatility risk premium was larger during elevated volatility environments.

### Regime Analysis

| Regime               |        Mean VRP |
| -------------------- | --------------: |
| High VIX Environment | 3.94 vol points |
| Low VIX Environment  | 3.22 vol points |

These findings are consistent with the existence of a persistent volatility risk premium.

---

# C++ Acceleration

Core pricing engines were rewritten in modern C++ and exposed to Python using pybind11.

This architecture enables:

- Python research workflows
- FastAPI integration
- Native C++ performance

## Performance Benchmarks

| Model                    | Python Runtime | C++ Runtime | Speedup |
| ------------------------ | -------------: | ----------: | ------: |
| Black-Scholes Call       |          5.10s |      0.021s |  244.6× |
| Black-Scholes Put        |          5.26s |      0.021s |  250.1× |
| Monte Carlo (100k Paths) |          4.03s |      0.046s |   87.7× |

### Benchmark Visualization

![C++ Benchmarks](docs/images/cpp_benchmarks.png)

### Why It Matters

The project demonstrates how computational bottlenecks in quantitative finance can be accelerated through native C++ extensions while preserving a Python-based research workflow.

---

# Dashboard

The platform includes an interactive frontend for pricing, volatility analysis, and model calibration.

### Main Dashboard

![Dashboard](docs/images/dashboard.png)

Features:

- Option pricing
- Volatility surface visualization
- Volatility forecasting
- Heston calibration
- Arbitrage diagnostics
- Volatility comparison tools

### Volatility Surface

![Volatility Surface](docs/images/vol_surface.png)

### SVI Smile Fit

![SVI Smile](docs/images/svi_smile.png)

---

# Project Architecture

![Architecture Diagram](docs/images/architecture.png)

```text
React Frontend
       |
       v
FastAPI Backend
       |
       +--> Pricing Engines
       |      Black-Scholes
       |      Monte Carlo
       |      Finite Difference
       |      Heston
       |
       +--> Volatility Models
       |      GARCH
       |      SVI
       |
       +--> Research Layer
       |      Volatility Risk Premium
       |      Forecast Validation
       |
       +--> C++ Extensions
              pybind11
```

---

# Models Implemented

## Black-Scholes

Implemented analytically from first principles.

Supports:

- European Calls
- European Puts
- Implied Volatility Extraction

Greeks:

- Delta
- Gamma
- Vega
- Theta
- Rho

---

## Monte Carlo Simulation

European option pricing using:

- Geometric Brownian Motion
- Antithetic Variates
- Confidence Interval Estimation

Outputs:

- Fair Value
- 95% Confidence Interval
- Convergence Analysis

---

## Finite Difference Methods

American option pricing via:

- Explicit Finite Difference
- Implicit Finite Difference
- Crank-Nicolson

Validation includes:

- Stability Testing
- Convergence Analysis

---

## Heston Stochastic Volatility Model

Implemented:

- Heston Characteristic Function
- Fourier Inversion Pricing
- Market Calibration

Purpose:

Models stochastic variance dynamics beyond Black-Scholes assumptions.

---

# Volatility Modeling

## Implied Volatility Extraction

Live option chains are downloaded and converted into implied volatility observations.

Workflow:

```text
Market Option Price
        ↓
Black-Scholes Inversion
        ↓
Implied Volatility
```

---

## SVI Volatility Surface

Implemented Gatheral's SVI parameterization.

Workflow:

```text
Option Chain
      ↓
Implied Volatility Extraction
      ↓
SVI Calibration
      ↓
Volatility Surface Construction
```

---

# Arbitrage Diagnostics

One of the primary challenges in volatility surface modeling is ensuring consistency.

The platform includes automated diagnostics for:

## Calendar Arbitrage

Checks:

```text
w(T₂) ≥ w(T₁)
```

where:

```text
T₂ > T₁
```

Violations indicate inconsistent term structure behavior.

---

## Butterfly Arbitrage

Checks convexity of option prices across strikes.

Condition:

```text
∂²C/∂K² ≥ 0
```

Violations imply negative risk-neutral probabilities.

### Arbitrage Report Example

![Arbitrage Diagnostics](docs/images/arbitrage_report.png)

---

# GARCH Forecasting

Implemented:

```text
GARCH(1,1)
```

using the ARCH package.

Forecast horizons:

- 1 Day
- 5 Day
- 10 Day
- 30 Day

---

## Forecast Validation

### 30-Day SPY Backtest

| Model               |    MAE |   RMSE |
| ------------------- | -----: | -----: |
| GARCH               | 0.0535 | 0.0847 |
| Naive Forecast      | 0.0536 | 0.0919 |
| Long Run Volatility | 0.0700 | 0.0886 |

### Forecast Comparison

![GARCH Backtest](docs/images/garch_backtest.png)

### Conclusion

GARCH modestly outperformed naive and long-run volatility forecasts while highlighting the inherent difficulty of volatility prediction.

---

# Testing & Validation

The project includes validation studies for:

- Monte Carlo convergence
- Confidence interval coverage
- Finite Difference stability
- Finite Difference convergence
- Heston calibration quality
- Volatility forecasting accuracy
- Arbitrage detection consistency
- Volatility risk premium analysis

The emphasis throughout the project is on verification and empirical evaluation rather than treating financial models as black boxes.

---

# Technology Stack

## Quantitative Finance

- Black-Scholes
- Monte Carlo
- Finite Difference
- Heston
- SVI
- GARCH

## Backend

- Python
- FastAPI
- NumPy
- SciPy
- Pandas
- ARCH
- yfinance

## Frontend

- React
- TypeScript
- Plotly

## Performance

- C++17
- pybind11

---

# Repository Structure

```text
quant-vol-engine/

├── backend/
├── frontend/
├── cpp/
│   ├── quant_cpp.cpp
│   ├── black_scholes.cpp
│   └── monte_carlo.cpp
│
├── pricing/
├── models/
├── research/
├── tests/
├── docs/
│   └── images/
│
└── README.md
```

---

# Future Work

## Quantitative Research

- Delta-neutral volatility trading strategy backtest
- Arbitrage-free SVI calibration
- Heston parameter stability analysis
- Volatility term structure research

## Quantitative Development

- C++ Finite Difference engine
- OpenMP parallel Monte Carlo
- SIMD vectorization
- GPU acceleration

---

# Motivation

This project was built to develop a deeper understanding of:

- Derivatives pricing
- Volatility modeling
- Numerical methods
- Quantitative research workflows
- High-performance quantitative software engineering

while exploring the tools and techniques used by modern options market makers, volatility trading desks, and quantitative research teams.

---

# Highlights

- 10+ quantitative models and research components
- 1,225-day volatility risk premium study
- 84.24% positive volatility risk premium frequency
- 0.6095 correlation between implied and future realized volatility
- Live option chain ingestion and volatility surface construction
- Automated arbitrage diagnostics
- Up to **250× speedup** via C++ acceleration
- Full-stack deployment with React + FastAPI
- Empirical volatility forecasting validation
- Production-style quantitative research workflow
