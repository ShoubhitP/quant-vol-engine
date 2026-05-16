# ⬡ Quant Vol Engine

A full-stack quantitative derivatives analytics platform built from scratch. Implements Black-Scholes pricing, Monte Carlo simulation, implied volatility extraction, SVI surface fitting, and Heston stochastic volatility calibration — exposed through a FastAPI backend and interactive React frontend.

**Live Demo:** [quant-vol-engine.vercel.app](https://quant-vol-engine.vercel.app)

---

## What This Project Does

Most options pricing projects stop at Black-Scholes. This project goes further:

1. **Extracts implied volatility** from live market option chains using Brent's method
2. **Fits SVI parametrization** across strikes and expiries to model the volatility smile
3. **Renders an interactive 3D volatility surface** showing how IV varies with strike and time
4. **Prices options under Heston stochastic volatility** using Fourier integration (Gil-Pelaez inversion)
5. **Calibrates Heston parameters** to live market data by minimizing squared pricing errors

---

## Models Implemented

### Black-Scholes

Closed-form option pricing derived from the heat equation. Full Greeks implemented: Δ, Γ, ν, Θ, ρ, vanna, volga, zomma.

### Monte Carlo

Geometric Brownian Motion simulation with antithetic variates for variance reduction. Returns price with 95% confidence interval.

### Implied Volatility Extraction

Inverts Black-Scholes using Brent's root-finding method. Filters illiquid options by bid-ask spread and intrinsic value bounds.

### SVI Surface Fitting

Fits the Stochastic Volatility Inspired (SVI) parametrization to implied variance across strikes for each expiry:

$$w(k) = a + b\left(\rho(k-m) + \sqrt{(k-m)^2 + \sigma^2}\right)$$

Where $k = \log(K/F)$ is log-moneyness and $w = \sigma_{imp}^2 \cdot T$ is total implied variance.

### Heston Model

Stochastic volatility model where variance follows a mean-reverting CIR process:

$$dS = rS\,dt + \sqrt{v}S\,dW_1$$
$$dv = \kappa(\theta - v)\,dt + \xi\sqrt{v}\,dW_2$$

Priced via Gil-Pelaez Fourier inversion of the characteristic function. Parameters (κ, θ, ξ, ρ, v₀) calibrated to market data.

---

## Mathematical Foundations

The `notebooks/mathematical_foundations.ipynb` notebook contains:

- Full derivation of Black-Scholes from the heat equation (change of variables, chain rule, drift elimination)
- Explanation of the no-arbitrage condition embedded in the BS PDE
- SVI parametrization and its role in arbitrage-free surface construction

---

## API Endpoints

| Method | Endpoint                     | Description                              |
| ------ | ---------------------------- | ---------------------------------------- |
| POST   | `/price`                     | Black-Scholes call/put price             |
| POST   | `/greeks`                    | All Greeks including vanna, volga, zomma |
| POST   | `/monte-carlo`               | MC price with confidence interval        |
| GET    | `/chain/{ticker}`            | Live options chain via yfinance          |
| GET    | `/vol-surface/{ticker}`      | IV extraction + SVI surface fitting      |
| POST   | `/heston`                    | Heston model pricing                     |
| GET    | `/heston-calibrate/{ticker}` | Calibrate Heston to live market data     |

---

## Tech Stack

| Layer       | Technology                           |
| ----------- | ------------------------------------ |
| Backend     | Python, FastAPI                      |
| Pricing     | NumPy, SciPy                         |
| Market Data | yfinance                             |
| Frontend    | React, Plotly.js                     |
| Deployment  | Railway (backend), Vercel (frontend) |

---

## Project Structure

quant-vol-engine/
├── backend/
│ └── main.py # FastAPI endpoints
├── pricing/
│ ├── black_scholes.py # BS pricing + Greeks
│ ├── monte_carlo.py # MC simulation
│ ├── implied_vol.py # IV extraction
│ ├── svi.py # SVI fitting
│ └── heston.py # Heston model + calibration
├── frontend/
│ └── src/App.jsx # React frontend
└── notebooks/
└── mathematical_foundations.ipynb

---

## Running Locally

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## Author

**Shoubhit Pusuluri**  
Ohio State University
