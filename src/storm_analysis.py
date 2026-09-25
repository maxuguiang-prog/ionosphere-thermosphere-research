"""Storm-window and summary analysis."""

import pandas as pd


def add_storm_flag(
    df: pd.DataFrame,
    storm_start: str,
    storm_end: str,
) -> pd.DataFrame:
    """Flag observations that fall inside the selected storm window."""
    out = df.copy()
    start = pd.Timestamp(storm_start, tz="UTC")
    end = pd.Timestamp(storm_end, tz="UTC")
    out["storm_period"] = (
        (out["timestamp"] >= start) & (out["timestamp"] <= end)
    )
    return out


def summarize_storm(df: pd.DataFrame) -> dict:
    """Return simple storm-period summary statistics."""
    storm = df[df["storm_period"]].copy()

    if storm.empty:
        return {"n": 0}

    result = {
        "n": int(len(storm)),
        "mean_tec_tecu": float(storm["tec"].mean()),
        "median_tec_tecu": float(storm["tec"].median()),
        "max_tec_tecu": float(storm["tec"].max()),
        "min_tec_tecu": float(storm["tec"].min()),
    }

    if "tec_anomaly_tecu" in storm:
        result["max_positive_anomaly_tecu"] = float(
            storm["tec_anomaly_tecu"].max()
        )
        result["min_anomaly_tecu"] = float(
            storm["tec_anomaly_tecu"].min()
        )

    return result
