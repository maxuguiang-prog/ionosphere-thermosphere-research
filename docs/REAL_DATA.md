# Replacing the test data with real observations

The repository currently runs immediately using synthetic test data. Before making scientific claims, replace it with real observations.

## Recommended first observational source

NASA/JPL GUARDIAN provides near-real-time ionospheric TEC time series from more than 90 GNSS stations around the Pacific Ring of Fire. The NASA Open Data record covers 2022 onward.

Dataset:
https://data.nasa.gov/dataset/ground-based-global-navigation-satellite-system-gnss-based-upper-atmospheric-realtime-disa-720c1

GUARDIAN:
https://guardian.jpl.nasa.gov/

The exact downloaded file format should be checked against the current dataset documentation before writing a parser. Do not guess the columns.

## Expected normalized format

After conversion to CSV, the pipeline expects:

```text
timestamp,tec,station,latitude,longitude,constellation
2024-05-10T00:00:00Z,....
```

Only `timestamp` and `tec` are required for the first analysis.

## Important scientific rule

Do not call a synthetic run a measurement, observation, result, or discovery. Synthetic data are only used to test that the software works.

## IGS alternative

IGS provides global vertical TEC maps in IONEX format, with final and rapid products. NASA CDDIS is an official archive location. Some CDDIS downloads require NASA Earthdata authentication.

IGS products:
https://www.igs.org/products/

NASA CDDIS ionosphere products:
https://data.nasa.gov/dataset/global-navigation-satellite-system-gnss-predicted-ionosphere-products-from-nasa-cddis
