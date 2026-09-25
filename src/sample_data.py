"""Generate clearly labeled synthetic data for testing the pipeline.

This file is ONLY for software testing. The generated values are not
scientific observations and must never be used as research results.
"""

from pathlib import Path
import numpy as np
import pandas as pd


def generate_test_data(path: str | Path) -> pd.DataFrame:
    """Generate a deterministic synthetic TEC time series."""
    rng = np.random.default_rng(42)

    start = pd.Timestamp("2024-05-08T00:00:00Z")
    end = pd.Timestamp("2024-05-13T00:00:00Z")
    timestamps = pd.date_range(start, end, freq="5min", inclusive="left")

    hours = (timestamps - start).total_seconds() / 3600.0

    # Smooth daily cycle + small noise.
    daily = 4.0 * np.sin(2 * np.pi * hours / 24.0)
    baseline = 25.0 + daily
    noise = rng.normal(0, 0.45, len(timestamps))

    # Synthetic storm-like perturbation for software testing only.
    storm_center = 84.0
    storm_width = 13.0
    perturbation = 9.0 * np.exp(-0.5 * ((hours - storm_center) / storm_width) ** 2)

    tec = baseline + perturbation + noise

    df = pd.DataFrame({
        "timestamp": timestamps,
        "tec": tec,
        "station": "SYNTHETIC_TEST_ONLY",
        "latitude": 65.0,
        "longitude": -20.0,
        "constellation": "TEST",
    })

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df
