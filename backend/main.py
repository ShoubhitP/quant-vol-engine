import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import numpy as np
import json
import requests
from fastapi.responses import Response
from pydantic import BaseModel
from pricing.monte_carlo import monte_carlo_call
from datetime import datetime
from pricing.implied_vol import extract_iv
from pricing.svi import fit_svi
from pricing.heston import heston_fourier_price, calibrate_heston
from pricing.finite_difference import explicit_fd_call, implicit_fd_call, american_put_cn, crank_nicolson_fd_call
from models.garch import volatility_snapshot
from models.implied_vol_snapshot import vol_comparison_snapshot
from research.svi_arbitrage import check_calendar_arbitrage, check_butterfly_arbitrage
from pricing.black_scholes import (
    black_scholes_call, black_scholes_put,
    delta_call, delta_put,
    gammaOption, vegaOption,
    theta_call, theta_put,
    rho_call, rho_put,
    vannaOption, volgaOption, zommaOption
)

app = FastAPI(title="Quant Vol Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class OptionInput(BaseModel):

    stockPrice: float
    strikePrice: float
    vol: float
    rfr: float
    timeToExpiry: float
    numSimulations: int

class FDInput(BaseModel):
    stockPrice: float
    strikePrice: float
    vol: float
    rfr: float
    timeToExpiry: float

@app.post("/price")
def price_option(data: OptionInput):
    priceDict = {
            "Call Price": black_scholes_call(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry),
            "Put Price": black_scholes_put(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry)
    }
    return priceDict

@app.post("/greeks")
def greeksOption(data: OptionInput):

    greekDict = {
            "Delta Call": delta_call(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry),
            "Delta Put": delta_put(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry),
            "Gamma Value": gammaOption(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry),
            "Vega Value": vegaOption(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry),
            "Theta Call": theta_call(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry),
            "Theta Put": theta_put(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry),
            "Rho Call": rho_call(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry),
            "Rho Put": rho_put(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry),
            "Vanna Value": vannaOption(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry),
            "Volga Value": volgaOption(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry),
            "Zomma Value": zommaOption(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry)
    
    }
    return greekDict

@app.post("/monte-carlo")
def monteCarloOption(data: OptionInput):

    price, lowerBound, upperBound = monte_carlo_call(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry, data.numSimulations)
    monteCarloDict = {
            "Monte Carlo Value": price, 
            "Lower Bound": lowerBound,
            "Upper Bound": upperBound

    }
    return monteCarloDict

from fastapi.responses import Response

@app.get("/chain/{ticker}")
def get_chain(ticker: str):
    tickerObject = yf.Ticker(ticker)
    tickerObject.session = requests.Session()
    tickerObject.session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    expiries = tickerObject.options
    chain = tickerObject.option_chain(expiries[0])
    raw = json.dumps({
        "Calls": json.loads(chain.calls.to_json(orient="records")),
        "Puts": json.loads(chain.puts.to_json(orient="records"))
    }).encode("utf-8")
    return Response(content=raw, media_type="application/json")

@app.get("/vol-surface/{ticker}")
def get_points(ticker: str):
    tickerObject = yf.Ticker(ticker)
    stockPrice = tickerObject.fast_info["lastPrice"]
    expiries = tickerObject.options
    if len(expiries) < 1:
        return {"surface": [], "svi_fits": []}
    surface_data = []
    svi_fits = []
    for i in range(min(6, len(expiries))): 
        expiry_date = datetime.strptime(expiries[i], "%Y-%m-%d")
        today = datetime.today()
        timeToExpiry = (expiry_date - today).days / 365.0
        forwardPrice = stockPrice * np.exp(0.05 * timeToExpiry)
        chain = tickerObject.option_chain(expiries[i])
        expiry_strikes = []
        expiry_ivs = []
        for _, row in chain.calls.iterrows():
            bid1 = row["bid"]
            ask1 = row["ask"]
            strikePrice = row["strike"]
            market_price = (bid1 + ask1)/2
            if ask1 <= 0 or (ask1 - bid1) / ask1 >= 0.5:
                continue
            else: 
                iv = extract_iv(market_price, stockPrice, strikePrice, timeToExpiry, 0.05, "call")
                newDict = {
                    "Strike Price": strikePrice,
                    "Time Till Expiry": timeToExpiry,
                    "Extracted Volatility": iv,
                    "Option Price": market_price,
                    "Option Type": "call",
                }
                if not np.isnan(iv):
                    expiry_strikes.append(newDict["Strike Price"])
                    expiry_ivs.append(newDict["Extracted Volatility"])
                    surface_data.append(newDict)
        for _, row in chain.puts.iterrows():
            bid1 = row["bid"]
            ask1 = row["ask"]
            strikePrice = row["strike"]
            market_price = (bid1 + ask1)/2
            if ask1 <=0 or (ask1 - bid1) / ask1 >= 0.5:
                continue
            else: 
                iv = extract_iv(market_price, stockPrice, strikePrice, timeToExpiry, 0.05, "put")
                newDict = {
                    "Strike Price": strikePrice,
                    "Time Till Expiry": timeToExpiry,
                    "Extracted Volatility": iv,
                    "Option Price": market_price,
                    "Option Type": "put",
                }
                if not np.isnan(iv):
                    expiry_strikes.append(newDict["Strike Price"])
                    expiry_ivs.append(newDict["Extracted Volatility"])
                    surface_data.append(newDict)
        try: 
            fitParamArray = fit_svi(expiry_strikes, expiry_ivs, forwardPrice, timeToExpiry)
            svi_fits.append({"T": timeToExpiry, "params": fitParamArray.tolist()})
        except Exception as e:
            print(f"SVI fit failed: {e}")
            continue
    return {
        "surface": surface_data,
        "svi_fits": svi_fits
    }

class hestonOption(BaseModel):

    stockPrice: float
    strikePrice: float
    timeToExpiry: float
    rfr: float
    kappa: float
    theta: float
    xi: float
    rho: float
    v_0: float
    option_type: str

@app.post("/heston")
def hestonCalculation(data: hestonOption):

    return heston_fourier_price(data.stockPrice, data.strikePrice, data.timeToExpiry, data.rfr, data.kappa, data.theta, data.xi, data.rho, data.v_0, data.option_type)

@app.get("/heston-calibrate/{ticker}")
def hestonCalibrater(ticker: str):
    try:
        max_contracts = 30

        tickerObject = yf.Ticker(ticker)
        stockPrice = tickerObject.fast_info["lastPrice"]
        expiries = tickerObject.options

        strikes = []
        expiries_list = []
        ivs = []

        for i in range(min(6, len(expiries))):
            expiry_date = datetime.strptime(expiries[i], "%Y-%m-%d")
            today = datetime.today()
            timeToExpiry = (expiry_date - today).days / 365.0

            if timeToExpiry <= 0:
                continue

            chain = tickerObject.option_chain(expiries[i])

            for _, row in chain.calls.iterrows():
                bid = row["bid"]
                ask = row["ask"]
                strike = row["strike"]

                if ask <= 0:
                    continue

                if (ask - bid) / ask >= 0.5:
                    continue

                market_price = (bid + ask) / 2
                iv = extract_iv(
                    market_price,
                    stockPrice,
                    strike,
                    timeToExpiry,
                    0.05,
                    "call"
                )

                if not np.isnan(iv):
                    strikes.append(strike)
                    expiries_list.append(timeToExpiry)
                    ivs.append(iv)

                if len(strikes) >= max_contracts:
                    break

            if len(strikes) >= max_contracts:
                break

        print(f"Collected contracts: {len(strikes)}")

        if len(strikes) < 5:
            return {"error": "Not enough valid option contracts for Heston calibration"}

        params = calibrate_heston(strikes, expiries_list, ivs, stockPrice, 0.05)

        return {
            "kappa": float(params[0]),
            "theta": float(params[1]),
            "xi": float(params[2]),
            "rho": float(params[3]),
            "v0": float(params[4]),
            "contracts_used": len(strikes),
        }

    except Exception as e:
        print(f"CALIBRATION ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
    
@app.post("/fd")
def fd_price(data: FDInput):

    fdPrices = {
        "FD Explicit Price": explicit_fd_call(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry, N = 100, M = 1000),
        "FD Implicit Price": implicit_fd_call(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry, N = 100, M = 1000),
        "FD Crank-Nicolson Price": crank_nicolson_fd_call(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry, N = 100, M = 1000), 
        "FD Crank-Nicolson Price For American Put Options": american_put_cn(data.stockPrice, data.strikePrice, data.vol, data.rfr, data.timeToExpiry, N = 100, M = 1000)
    }
    return fdPrices

@app.get("/vol-snapshot/{ticker}")
def get_vol_snapshot(ticker: str):
    try: 
        return volatility_snapshot(ticker)
    except Exception as e: 
        return {"error": str(e)}
    
@app.get("/vol-comparison/{ticker}")
def get_vol_comparison(ticker: str):
    try: 
        return vol_comparison_snapshot(ticker)
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/surface-arbitrage/{ticker}")
def surface_arbitrage(ticker: str):
    try:
        data = get_points(ticker)

        calendar_violations = check_calendar_arbitrage(data["surface"])
        butterfly_violations = check_butterfly_arbitrage(data["surface"])

        calendar_sizes = [v["violation_size"] for v in calendar_violations]
        butterfly_sizes = [abs(v["convexity"]) for v in butterfly_violations]

        return {
            "ticker": ticker.upper(),

            "calendar_arbitrage_count": len(calendar_violations),
            "max_calendar_violation": max(calendar_sizes) if calendar_sizes else 0,
            "avg_calendar_violation": (
                sum(calendar_sizes) / len(calendar_sizes)
                if calendar_sizes else 0
            ),

            "butterfly_arbitrage_count": len(butterfly_violations),
            "max_butterfly_violation": max(butterfly_sizes) if butterfly_sizes else 0,
            "avg_butterfly_violation": (
                sum(butterfly_sizes) / len(butterfly_sizes)
                if butterfly_sizes else 0
            ),

            "calendar_violations": calendar_violations[:20],
            "butterfly_violations": butterfly_violations[:20],
        }

    except Exception as e:
        return {"error": str(e)}