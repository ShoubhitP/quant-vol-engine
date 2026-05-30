import numpy as np
import pandas as pd 
from models.garch import get_returns, fit_garch_model, get_annualized_forecast

def future_realized_volatility(returns, horizons=30):
    future_vol = returns.rolling(horizons).std().shift(-horizons+1)
    future_vol = future_vol * np.sqrt(252)
    return future_vol

def run_garch_backtest(ticker, horizon=30, train_window=500, step=20):
    returns = get_returns(ticker)
    future_rv = future_realized_volatility(returns)
    rows = []
    for i in range(train_window, len(returns) - horizon, step):
        train_returns = returns.iloc[:i]
        result = fit_garch_model(train_returns)
        forecast = result.forecast(horizon=horizon)
        variance = forecast.variance.iloc[-1]

        forecast_daily_vol = np.sqrt(variance[f"h.{horizon:02d}"])
        forecast_annualized_vol = forecast_daily_vol * np.sqrt(252) / 100        
        date = returns.index[i]
        actual_future_vol = future_rv.iloc[i]
        rows.append({
            "date": date,
            "forecast_vol": float(forecast_annualized_vol),
            "future_realized_vol": float(actual_future_vol),
            "error": float(forecast_annualized_vol - actual_future_vol),
        })
    return pd.DataFrame(rows)


def main():
    results = run_garch_backtest("SPY", horizon=30, train_window=500, step=20)

    print(results.head())
    print(results.tail())
    print(f"Backtest rows: {len(results)}")
    print(f"MAE: {results['error'].abs().mean():.4f}")
    print(f"RMSE: {np.sqrt((results['error'] ** 2).mean()):.4f}")

if __name__ == "__main__":
    main()