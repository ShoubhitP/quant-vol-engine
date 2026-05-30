import numpy as np
import pandas as pd
import yfinance as yf
from arch import arch_model

def get_returns(ticker, period="5y"):
    data = yf.download(ticker, period=period, auto_adjust=True)
    prices = data["Close"].squeeze()
    returns = np.log(prices/prices.shift(1))
    returns = returns.dropna()

    return returns

def fit_garch_model(returns):
    scaled_returns = returns*100
    model = arch_model(scaled_returns, vol="Garch", p=1, q=1, mean="Constant", dist="normal")
    modelFit = model.fit(disp="off")
    return modelFit

def forecast_volatility(garch_result, horizon=30):
    forecast = garch_result.forecast(horizon=horizon)
    return forecast

def get_annualized_forecast(result, horizon=30):
    forecast = result.forecast(horizon=horizon)
    variance = forecast.variance.iloc[-1]
    daily_vol = np.sqrt(variance)
    annualized_Vol = daily_vol * np.sqrt(252)
    return annualized_Vol
def get_volatility_forecast(ticker, horizon=30):
    returns = get_returns(ticker)
    result = fit_garch_model(returns)
    annumVol = get_annualized_forecast(result)
    return {
        "ticker": ticker.upper(),
        "one_day": float(annumVol["h.01"] / 100),
        "five_day": float(annumVol["h.05"] / 100),
        "ten_day": float(annumVol["h.10"] / 100),
        "thirty_day": float(annumVol["h.30"] / 100),
        "alpha": float(result.params["alpha[1]"]),
        "beta": float(result.params["beta[1]"]),
        "persistence": float(result.params["alpha[1]"] + result.params["beta[1]"]),
    }




def main():
    
    forecast = get_volatility_forecast("SPY")
    print(forecast)

if __name__ == "__main__":

    main()