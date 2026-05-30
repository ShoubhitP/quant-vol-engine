import numpy as np
import pandas as pd

from models.garch import realized_volatility
from research.garch_backtest import future_realized_volatility

def test_realized_volatility_length():
    returns = pd.Series([0.01, -0.01, 0.02, -0.02, 0.01])

    rv = realized_volatility(returns, window=3)

    assert len(rv) == 3

def test_realized_volatility_positive():
    returns = pd.Series([0.01, -0.01, 0.02, -0.02, 0.01])

    rv = realized_volatility(returns, window=3)

    assert (rv >= 0).all()

def test_future_realized_volatility_has_trailing_nans():
    returns = pd.Series([0.01, -0.01, 0.02, -0.02, 0.01])

    future_rv = future_realized_volatility(returns, horizon=3)

    assert future_rv.iloc[-1] != future_rv.iloc[-1]  # NaN check
    assert future_rv.iloc[-2] != future_rv.iloc[-2]