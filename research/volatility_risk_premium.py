import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

from models.garch import get_returns
from research.garch_backtest import future_realized_volatility

def build_vrp_dataset():
    returns = get_returns("SPY")
    future_rv = future_realized_volatility(returns,horizon=30)

    vix = get_vix()

    df = pd.concat([future_rv.rename("future_realized_vol"), vix.rename("implied_vol")], axis=1)

    df["vrp"] = (df["implied_vol"] - df["future_realized_vol"])

    return df.dropna()

def get_vix():
    vix = yf.download("^VIX", period="5y", auto_adjust=True)["Close"]

    if isinstance(vix,pd.DataFrame):
        vix = vix.iloc[:,0]
    return vix / 100.0

def main():
    df = build_vrp_dataset()

    print(df.head())
    print(df.tail())
    print(df["vrp"].describe())
    print(len(df))

    positive_pct = (df["vrp"] > 0).mean()
    print()
    print(f"Positive VRP frequency: {positive_pct:.2%}")

    corr = df["implied_vol"].corr(df["future_realized_vol"])

    print(f"Correlation(IV, Future RV): {corr:.4f}")

    print()
    print("VRP by Regime")

    high_vix = df[df["implied_vol"] > df["implied_vol"].median()]
    low_vix = df[df["implied_vol"] <= df["implied_vol"].median()]

    print(f"High VIX mean VRP: {high_vix['vrp'].mean():.4f}")
    print(f"Low VIX mean VRP:  {low_vix['vrp'].mean():.4f}")



    plt.hist(df["vrp"], bins=50)
    plt.axvline(0, linestyle="--")
    plt.title("Volatility Risk Premium Distribution")
    plt.xlabel("IV - Future Realized Vol")
    plt.ylabel("Frequency")
    plt.show()

if __name__ == "__main__":
    main()