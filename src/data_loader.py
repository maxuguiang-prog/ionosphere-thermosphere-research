"""Data loading utilities for TEC research."""

from pathlib import Path
import pandas as pd


def load_tec_csv(path: str | Path) -> pd.DataFrame:
    """Load a TEC CSV and standardize its column names.

    Accepted TEC column names:
        - tec
        - tec_tecu

    Required:
        timestamp + one TEC column

    Optional:
        station, latitude, longitude, constellation
    """

    path = Path(path)
    df = pd.read_csv(path)

    # Accept the actual IGS-derived column name.
    if "tec_tecu" in df.columns and "tec" not in df.columns:
        df = df.rename(columns={"tec_tecu": "tec"})

    required_columns = {"timestamp", "tec"}
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}. "
            "The file must contain timestamp and tec/tec_tecu."
        )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True,
        errors="coerce",
    )

    df["tec"] = pd.to_numeric(
        df["tec"],
        errors="coerce",
    )

    df = df.dropna(
        subset=["timestamp", "tec"]
    ).copy()

    df = df.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    return df


def save_processed(
    df: pd.DataFrame,
    path: str | Path,
) -> None:
    """Save a processed dataframe as CSV."""

    path = Path(path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        path,
        index=False,
    )
