# Research plan

## Phase 1 — Establish the pipeline
- Use one real geomagnetic storm.
- Load real GNSS/TEC observations.
- Establish a quiet-time baseline.
- Calculate TEC anomalies.
- Verify data quality and reproduce published/known storm behavior.

## Phase 2 — Make the question spatial
- Add multiple stations.
- Focus on high-latitude stations.
- Compare northern and southern high-latitude responses where data permit.
- Separate local-time and latitude effects.

## Phase 3 — Add storm drivers
Possible explanatory variables:
- Dst or SYM-H
- Kp
- solar wind parameters
- IMF Bz
- F10.7 solar flux

Do not add variables merely because they are available; each should have a scientific reason.

## Phase 4 — Model comparison
Compare observations with an established model or archived model output.

Calculate:
- bias
- MAE
- RMSE
- correlation
- timing error
- amplitude error

The objective is to identify reproducible conditions under which model error is large.

## Phase 5 — Thermosphere
Add neutral-density observations or model output. The thermosphere matters for satellite drag and is directly coupled to ionospheric variability.

NASA CCMC ITMAP is a useful reference because it already supports ionosphere/thermosphere model-data validation.

## Phase 6 — Hardware justification
Only after the data analysis reveals a specific unresolved measurement need should we design the ground GNSS station or potential CubeSat payload.
