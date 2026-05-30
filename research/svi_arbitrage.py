import numpy as np
import pandas as pd


def normalize_surface(surface_data):
    df = pd.DataFrame(surface_data)

    df = df.rename(
        columns={
            "Strike Price": "strike",
            "Time Till Expiry": "expiry",
            "Extracted Volatility": "iv",
        }
    )

    df = df.dropna(subset=["strike", "expiry", "iv"])

    df = (
        df.groupby(["strike", "expiry"], as_index=False)["iv"]
        .mean()
    )

    df["total_variance"] = (df["iv"] ** 2) * df["expiry"]

    return df


def check_calendar_arbitrage(surface_data, tolerance=1e-4):
    df = normalize_surface(surface_data)

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