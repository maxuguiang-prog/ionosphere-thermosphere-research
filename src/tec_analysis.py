"""TEC analysis functions."""

import numpy as np
import pandas as pd


def calculate_anomaly_statistics(df: pd.DataFrame) -> dict:
    """Calculate descriptive statistics for TEC anomalies."""
    if "tec_anomaly_tecu" not in df:
        raise ValueError("Run add_quiet_baseline before calculating anomaly statistics.")

    a = df["tec_anomaly_tecu"].dropna()

    return {
        "mean_anomaly_tecu": float(a.mean()),
        "median_anomaly_tecu": float(a.median()),
        "std_anomaly_tecu": float(a.std()),
        "max_positive_anomaly_tecu": float(a.max()),
        "max_negative_anomaly_tecu": float(a.min()),
    }


def calculate_rmse(observed, modeled) -> float:
    """Root mean square error."""
    observed = np.asarray(observed, dtype=float)
    modeled = np.asarray(modeled, dtype=float)
    mask = np.isfinite(observed) & np.isfinite(modeled)

    if not mask.any():
        raise ValueError("No finite observation/model pairs were available.")

    return float(np.sqrt(np.mean((observed[mask] - modeled[mask]) ** 2)))


def calculate_mae(observed, modeled) -> float:
    """Mean absolute error."""
    observed = np.asarray(observed, dtype=float)
    modeled = np.asarray(modeled, dtype=float)
    mask = np.isfinite(observed) & np.isfinite(modeled)

    if not mask.any():
        raise ValueError("No finite observation/model pairs were available.")

    return float(np.mean(np.abs(observed[mask] - modeled[mask])))
