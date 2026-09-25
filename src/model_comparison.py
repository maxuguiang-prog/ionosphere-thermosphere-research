"""Model-comparison scaffolding.

Phase 1 does not yet connect to a live model service. The functions here
define the interface we will use once model output is available.
"""

import pandas as pd
from .tec_analysis import calculate_mae, calculate_rmse


def compare_observed_and_modeled(
    observations: pd.DataFrame,
    model: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """Merge observed and modeled TEC by timestamp and calculate errors.

    Both inputs must contain:
        timestamp
        tec

    The model dataframe's TEC column should represent model-predicted TEC.
    """
    obs = observations[["timestamp", "tec"]].rename(columns={"tec": "observed_tecu"})
    mod = model[["timestamp", "tec"]].rename(columns={"tec": "modeled_tecu"})

    merged = pd.merge_asof(
        obs.sort_values("timestamp"),
        mod.sort_values("timestamp"),
        on="timestamp",
        direction="nearest",
        tolerance=pd.Timedelta("15min"),
    ).dropna(subset=["modeled_tecu"])

    merged["error_tecu"] = merged["observed_tecu"] - merged["modeled_tecu"]

    metrics = {
        "MAE_TECU": calculate_mae(
            merged["observed_tecu"], merged["modeled_tecu"]
        ),
        "RMSE_TECU": calculate_rmse(
            merged["observed_tecu"], merged["modeled_tecu"]
        ),
        "bias_TECU": float(merged["error_tecu"].mean()),
        "n_pairs": int(len(merged)),
    }

    return merged, metrics
