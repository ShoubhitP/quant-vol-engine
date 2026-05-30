import numpy as np
import pandas as pd 
from models.garch import get_returns, fit_garch_model
import matplotlib.pyplot as plt

def future_realized_volatility(returns, horizon=30):
    future_vol = returns.rolling(horizon).std().shift(-horizon+1)
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
        current_realized_vol = (returns.iloc[max(0, i-horizon):i].std() * np.sqrt(252))
        long_run_vol = (returns.iloc[:i].std()*np.sqrt(252))
        rows.append({
            "date": date,

            "forecast_vol": float(forecast_annualized_vol),
            "future_realized_vol": float(actual_future_vol),

            "naive_vol": float(current_realized_vol),
            "long_run_vol": float(long_run_vol),

            "garch_error": float(
                forecast_annualized_vol - actual_future_vol
            ),

            "naive_error": float(
                current_realized_vol - actual_future_vol
            ),

            "long_run_error": float(
                long_run_vol - actual_future_vol
            ),
        })
    return pd.DataFrame(rows)


def main():
    results = run_garch_backtest("SPY", horizon=30, train_window=500, step=20)
    print(results.head())
    print(results.tail())

    print(f"Backtest rows: {len(results)}")
    results.to_csv("research/garch_backtest_results.csv", index=False)

    garch_mae = results["garch_error"].abs().mean()
    naive_mae = results["naive_error"].abs().mean()
    long_run_mae = results["long_run_error"].abs().mean()

    garch_rmse = np.sqrt((results["garch_error"] ** 2).mean())
    naive_rmse = np.sqrt((results["naive_error"] ** 2).mean())
    long_run_rmse = np.sqrt((results["long_run_error"] ** 2).mean())

    print("\nForecast Comparison")
    print("-" * 40)
    print(f"GARCH     MAE={garch_mae:.4f} RMSE={garch_rmse:.4f}")
    print(f"Naive     MAE={naive_mae:.4f} RMSE={naive_rmse:.4f}")
    print(f"Long Run  MAE={long_run_mae:.4f} RMSE={long_run_rmse:.4f}")

    plt.figure()
    plt.plot(results["date"], results["forecast_vol"], marker="o", label="GARCH Forecast")
    plt.plot(results["date"], results["future_realized_vol"], marker="o", label="Future Realized Vol")
    plt.xlabel("Date")
    plt.ylabel("Annualized Volatility")
    plt.title("GARCH 30-Day Forecast vs Future Realized Volatility")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("research/garch_backtest.png", dpi=300, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    main()