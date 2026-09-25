"""Run the Phase 1 TEC analysis pipeline."""

from pathlib import Path
import argparse
import json

from .data_loader import load_tec_csv, save_processed
from .preprocessing import quality_control, add_quiet_baseline
from .storm_analysis import add_storm_flag, summarize_storm
from .tec_analysis import calculate_anomaly_statistics
from .plotting import plot_tec_timeseries, plot_anomaly
from .sample_data import generate_test_data


ROOT = Path(__file__).resolve().parents[1]

# This is a first software test window based on the May 2024 storm period.
# It is NOT a scientific conclusion.
BASELINE_START = "2024-05-08T00:00:00Z"
BASELINE_END = "2024-05-09T00:00:00Z"
STORM_START = "2024-05-10T12:00:00Z"
STORM_END = "2024-05-12T12:00:00Z"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Path to a real TEC CSV. If omitted, synthetic test data are generated.",
    )
    args = parser.parse_args()

    if args.input:
        input_path = Path(args.input)
        df = load_tec_csv(input_path)
        data_source = "USER-PROVIDED REAL DATA"
    else:
        input_path = ROOT / "data" / "raw" / "synthetic_test_tec.csv"
        generate_test_data(input_path)
        df = load_tec_csv(input_path)
        data_source = "SYNTHETIC TEST DATA — NOT SCIENTIFIC OBSERVATIONS"

    df = quality_control(df)
    df = add_quiet_baseline(df, BASELINE_START, BASELINE_END)
    df = add_storm_flag(df, STORM_START, STORM_END)

    processed_path = ROOT / "data" / "processed" / "tec_analysis.csv"
    save_processed(df, processed_path)

    summary = summarize_storm(df)
    anomaly_stats = calculate_anomaly_statistics(df)

    summary_path = ROOT / "results" / "tables" / "phase1_summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "data_source": data_source,
                "baseline_start": BASELINE_START,
                "baseline_end": BASELINE_END,
                "storm_start": STORM_START,
                "storm_end": STORM_END,
                "storm_summary": summary,
                "anomaly_statistics": anomaly_stats,
            },
            indent=2,
        )
    )

    plot_tec_timeseries(
        df,
        ROOT / "results" / "figures" / "tec_timeseries.png",
        "Phase 1 TEC Time Series",
    )

    plot_anomaly(
        df,
        ROOT / "results" / "figures" / "tec_anomaly.png",
        "Phase 1 TEC Anomaly",
    )

    print("\nPhase 1 complete.")
    print(f"Data source: {data_source}")
    print(f"Processed data: {processed_path}")
    print(f"Summary: {summary_path}")
    print("Figures:")
    print("  results/figures/tec_timeseries.png")
    print("  results/figures/tec_anomaly.png")
    print("\nIMPORTANT: If synthetic test data were used, the plots are software tests, not scientific results.")


if __name__ == "__main__":
    main()
