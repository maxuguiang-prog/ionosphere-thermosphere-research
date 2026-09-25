"""Quality control and baseline calculations."""

import pandas as pd
import numpy as np


def quality_control(df: pd.DataFrame, min_tec: float = 0.0) -> pd.DataFrame:
    """Remove impossible/missing TEC values.

    This is intentionally conservative. Scientific QC rules should be
    refined after inspecting the real dataset's documentation.
    """
    out = df.copy()
    out = out[np.isfinite(out["tec"])]
    out = out[out["tec"] >= min_tec]
    return out.reset_index(drop=True)


def add_quiet_baseline(
    df: pd.DataFrame,
    baseline_start: str,
    baseline_end: str,
) -> pd.DataFrame:
    """Add a constant quiet-time baseline and TEC anomaly.

    The baseline is the median TEC during the selected quiet interval.
    """
    out = df.copy()
    start = pd.Timestamp(baseline_start, tz="UTC")
    end = pd.Timestamp(baseline_end, tz="UTC")

    baseline_values = out.loc[
        (out["timestamp"] >= start) & (out["timestamp"] < end), "tec"
    ]

    if baseline_values.empty:
        raise ValueError("No observations were found in the requested baseline window.")

    baseline = float(baseline_values.median())
    out["quiet_baseline_tecu"] = baseline
    out["tec_anomaly_tecu"] = out["tec"] - baseline
    out["tec_percent_anomaly"] = 100.0 * out["tec_anomaly_tecu"] / baseline

    return out


def add_moving_baseline(
    df: pd.DataFrame,
    window: str = "6h",
) -> pd.DataFrame:
    """Add a rolling median baseline for exploratory analysis."""
    out = df.copy().sort_values("timestamp")
    indexed = out.set_index("timestamp")
    rolling = indexed["tec"].rolling(window, center=True, min_periods=20).median()
    out["rolling_baseline_tecu"] = rolling.to_numpy()
    out["rolling_anomaly_tecu"] = out["tec"] - out["rolling_baseline_tecu"]
    return out.reset_index(drop=True)
