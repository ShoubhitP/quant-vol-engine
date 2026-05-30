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
                    
def main():
    returns = get_returns("SPY")
    print(returns.head())
    print(returns.tail())
    print(f"Number of returns: {len(returns)}")
    print(type(returns))
    print(returns.mean()) 
    print(returns.std()) #daily realized volatility
    annualized_vol = returns.std()*np.sqrt(252)
    print(f"Annualized realized vol: {annualized_vol:.4f}")

    result = fit_garch_model(returns)

    print(result.summary())
    print(result.params)

if __name__ == "__main__":

    main()