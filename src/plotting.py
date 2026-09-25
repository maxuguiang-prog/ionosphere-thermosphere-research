"""Scientific plotting functions."""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def plot_tec_timeseries(
    df: pd.DataFrame,
    output_path: str | Path,
    title: str,
) -> None:
    """Plot TEC and the quiet-time baseline."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df["timestamp"], df["tec"], linewidth=1.2, label="TEC")
    if "quiet_baseline_tecu" in df:
        ax.plot(
            df["timestamp"],
            df["quiet_baseline_tecu"],
            linewidth=1.2,
            label="Quiet-time median baseline",
        )

    if "storm_period" in df and df["storm_period"].any():
        storm = df[df["storm_period"]]
        ax.axvspan(
            storm["timestamp"].min(),
            storm["timestamp"].max(),
            alpha=0.15,
            label="Selected storm window",
        )

    ax.set_title(title)
    ax.set_xlabel("UTC time")
    ax.set_ylabel("TEC (TECU)")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_anomaly(
    df: pd.DataFrame,
    output_path: str | Path,
    title: str,
) -> None:
    """Plot TEC anomaly relative to the selected baseline."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(
        df["timestamp"],
        df["tec_anomaly_tecu"],
        linewidth=1.2,
    )
    ax.axhline(0, linewidth=1)

    if "storm_period" in df and df["storm_period"].any():
        storm = df[df["storm_period"]]
        ax.axvspan(
            storm["timestamp"].min(),
            storm["timestamp"].max(),
            alpha=0.15,
        )

    ax.set_title(title)
    ax.set_xlabel("UTC time")
    ax.set_ylabel("TEC anomaly (TECU)")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
