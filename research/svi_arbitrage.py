import numpy as np
import pandas as pd

def normalize_surface(surface_data):
    df = pd.DataFrame(surface_data)

    df = df.rename(
        columns={
            "Strike Price": "strike",
            "Time Till Expiry": "expiry",
            "Extracted Volatility": "iv",
            "Option Price": "option_price",
            "Option Type": "option_type",
        }
    )
    df = df.dropna(subset=["strike", "expiry", "iv", "option_price", "option_type"])

    df = (
        df.groupby(["strike", "expiry", "option_type"], as_index=False)
        .agg({
            "iv": "mean",
            "option_price": "mean",
        })
    )
    df["total_variance"] = (df["iv"] ** 2) * df["expiry"]
    return df

def check_calendar_arbitrage(surface_data, tolerance=1e-4):
    df = normalize_surface(surface_data)
    df = (df.groupby(["strike", "expiry"], as_index=False).agg
        ({
            "iv": "mean",
            "total_variance": "mean"
        })
    )

    violations = []

    for strike, group in df.groupby("strike"):
        group = group.sort_values("expiry")

        for i in range(len(group) - 1):
            current = group.iloc[i]
            next_row = group.iloc[i + 1]

            violation_size = current["total_variance"] - next_row["total_variance"]

            if violation_size > tolerance:
                violations.append({
                    "strike": float(strike),
                    "expiry_1": float(current["expiry"]),
                    "expiry_2": float(next_row["expiry"]),
                    "variance_1": float(current["total_variance"]),
                    "variance_2": float(next_row["total_variance"]),
                    "violation_size": float(violation_size),
                })
    return violations

def check_butterfly_arbitrage(surface_data, tolerance=0.10):
    df = normalize_surface(surface_data)
    df = df[df["option_type"] == "call"]
    df = df[df["expiry"] >= 7/365]

    violations = []

    for expiry, group in df.groupby("expiry"):
        group = group.sort_values("strike").reset_index(drop=True)

        for i in range(1, len(group) - 1):
            left = group.iloc[i - 1]
            middle = group.iloc[i]
            right = group.iloc[i + 1]

            k_left = left["strike"]
            k_mid = middle["strike"]
            k_right = right["strike"]

            c_left = left["option_price"]
            c_mid = middle["option_price"]
            c_right = right["option_price"]

            slope_left = (c_mid - c_left) / (k_mid - k_left)
            slope_right = (c_right - c_mid) / (k_right - k_mid)

            convexity = slope_right - slope_left

            if convexity < -tolerance:
                violations.append({
                    "expiry": float(expiry),
                    "strike_left": float(k_left),
                    "strike_mid": float(k_mid),
                    "strike_right": float(k_right),
                    "price_left": float(c_left),
                    "price_mid": float(c_mid),
                    "price_right": float(c_right),
                    "convexity": float(convexity),
                })

    return violations