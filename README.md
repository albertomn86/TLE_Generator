# TLE Generator

Custom TLE file generator.

## Usage:

`tle_gen [-h] [-i INPUT] [-o OUTPUT] [-v]`

## Optional arguments:

```
  -h, --help                 Show help message.
  -i INPUT, --input INPUT    Download TLE for the specified catalog numbers.
  -o OUTPUT, --output OUTPUT Output file path.
  -v, --version              Show version.
```

## Examples:

Generate TLE file with the NORAD catalog numbers included in the file `satellites.txt`:

```
# ./tle_gen.py
2020-02-04 10:57:49,523 - INFO: Saved TLE for METEOR-M 2.
2020-02-04 10:57:49,793 - INFO: Saved TLE for METEOR-M2 2.
2020-02-04 10:57:50,054 - INFO: Saved TLE for NOAA 15.
2020-02-04 10:57:50,317 - INFO: Saved TLE for NOAA 18.
2020-02-04 10:57:50,598 - INFO: Saved TLE for NOAA 19.
2020-02-04 10:57:50,853 - INFO: Saved TLE for ISS (ZARYA).
2020-02-04 10:57:51,129 - INFO: Saved TLE for FUNCUBE-1 (AO-73).
2020-02-04 10:57:51,407 - INFO: Saved TLE for RADFXSAT (FOX-1B).
2020-02-04 10:57:51,708 - INFO: Saved TLE for FOX-1CLIFF (AO-95).
2020-02-04 10:57:51,967 - INFO: Saved TLE for FOX-1D (AO-92).
2020-02-04 10:57:52,408 - INFO: Saved TLE for NAYIF-1 (EO-88).
2020-02-04 10:57:52,706 - INFO: Saved TLE for JY1SAT (JO-97).
2020-02-04 10:57:52,978 - INFO: Saved TLE for FOSSASAT-1.
2020-02-04 10:57:53,297 - INFO: Saved TLE for HUSKYSAT-1.
2020-01-22 19:28:37,777 - INFO: Custom TLE file saved in "custom_TLE.txt".
```

Generate TLE file in `/tmp/noaa.txt` with the NORAD catalog numbers `25338`, `28654`, and `33591`:

```
# ./tle_gen.py -i 25338,28654,33591 -o /tmp/noaa.txt
2020-01-22 19:35:14,158 - INFO: Saved TLE for NOAA 15.
2020-01-22 19:35:14,546 - INFO: Saved TLE for NOAA 18.
2020-01-22 19:35:14,839 - INFO: Saved TLE for NOAA 19.
2020-01-22 19:35:14,839 - INFO: Custom TLE file saved in "/tmp/noaa.txt".
```
