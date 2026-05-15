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
                    "Extracted Volatility": iv
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
                    "Extracted Volatility": iv
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





