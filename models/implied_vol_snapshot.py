import yfinance as yf
from datetime import datetime
import numpy as np
from models.garch import volatility_snapshot

def get_atm_iv(ticker, target_days=30):
    ticker_obj = yf.Ticker(ticker)
    stock_price = ticker_obj.fast_info["lastPrice"]
    expiries = ticker_obj.options

    today = datetime.today()

    best_expiry = min(expiries, key=lambda expiry: abs((datetime.strptime(expiry, "%Y-%m-%d") - today).days - target_days))
    
    chain = ticker_obj.option_chain(best_expiry)
    calls = chain.calls

    calls["distance"] = abs(calls["strike"] - stock_price)

    atm_row = calls.sort_values("distance").iloc[0]
    days_to_expiry = (datetime.strptime(best_expiry, "%Y-%m-%d") - today).days
    return {
        "ticker": ticker.upper(),
        "stock_price": float(stock_price),
        "expiry": best_expiry,
        "days_to_expiry": int(days_to_expiry),
        "strike": float(atm_row["strike"]),
        "atm_iv": float(atm_row["impliedVolatility"]),
    }

def vol_comparison_snapshot(ticker):
    garch = volatility_snapshot(ticker)
    atm = get_atm_iv(ticker, target_days=30)
    return {
        "ticker": ticker.upper(),
        "stock_price": atm["stock_price"],
        "atm_iv": atm["atm_iv"],
        "iv_expiry": atm["expiry"],
        "days_to_expiry": atm["days_to_expiry"],
        "latest_30d_realized_vol": garch["latest_30d_realized_vol"],
        "garch_30d_forecast": garch["garch_thirty_day"],
        "iv_minus_garch": atm["atm_iv"] - garch["garch_thirty_day"],
        "iv_minus_realized": atm["atm_iv"] - garch["latest_30d_realized_vol"],
    }


def main():
    result = get_atm_iv("SPY")
    print(result)
    print(vol_comparison_snapshot("SPY"))

if __name__ == "__main__":
    main()