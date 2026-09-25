# Ionosphere–Thermosphere Research

Beginner-friendly research toolkit for studying how the high-latitude ionosphere responds to geomagnetic storms and, later, comparing observations with ionosphere–thermosphere models.

## Research question

**How accurately do existing ionosphere–thermosphere models predict high-latitude upper-atmosphere changes during geomagnetic storms, and under what conditions are their errors largest?**

## Phase 1

Phase 1 starts with Total Electron Content (TEC), an ionospheric observable derived from GNSS measurements.

The workflow is:

**GNSS/TEC observations → quality control → quiet-time baseline → TEC anomaly → storm response → model comparison**

This repository deliberately does **not** claim a scientific gap has been discovered yet. The purpose of the first phase is to establish a reproducible analysis pipeline and then test where models and observations disagree.

## Data sources

The primary planned observational source is NASA/JPL GUARDIAN near-real-time ionospheric TEC. NASA describes GUARDIAN as providing TEC time series from more than 90 GNSS ground stations and four GNSS constellations. The NASA Open Data record covers September 2022 onward.

NASA dataset:
https://data.nasa.gov/dataset/ground-based-global-navigation-satellite-system-gnss-based-upper-atmospheric-realtime-disa-720c1

GUARDIAN:
https://guardian.jpl.nasa.gov/

IGS global ionospheric maps are another planned source. IGS provides final and rapid VTEC maps in IONEX format.

IGS:
https://www.igs.org/products/

NASA CCMC ITMAP is the eventual model-validation reference point. ITMAP combines observations with ionosphere/thermosphere models and includes TEC and thermospheric neutral-density validation.

ITMAP:
https://ccmc.gsfc.nasa.gov/tools/ITMAP/

## Important data-access note

Some CDDIS products require a free NASA Earthdata Login for direct download. This repository therefore includes:

1. a clearly labeled synthetic test dataset so the code runs immediately;
2. a loader for real CSV-like TEC observations;
3. documentation for replacing the test file with real observations.

**Synthetic data must never be presented as scientific observations.**

## Run the first version

From the repository root:

```bash
python -m pip install -r requirements.txt
python -m src.main
```

The default run uses the labeled synthetic test dataset and writes figures to:

`results/figures/`

To use a real CSV file:

```bash
python -m src.main --input data/raw/guardian_tec.csv
```

The real CSV should contain at minimum:

- `timestamp`
- `tec`

Optional columns:

- `station`
- `latitude`
- `longitude`
- `constellation`

## First outputs

The pipeline produces:

- TEC time series
- quiet-time baseline
- TEC anomaly
- storm-window shading
- summary statistics

The next scientific phase will add:

- multiple stations
- high-latitude filtering
- geomagnetic indices such as Dst/SYM-H/Kp
- model output
- observed-vs-modeled error metrics
- thermospheric neutral-density observations
