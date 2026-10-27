# NASA MODIS C6.1 Active Fire & Hotspot Data

Global active fire and thermal anomaly detection analysis tools based on **NASA FIRMS MODIS Collection 6.1 (C6.1)** data spanning **2000 through 2025**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## 📌 Overview

The Moderate Resolution Imaging Spectroradiometer (MODIS) instrument aboard NASA's Terra and Aqua satellites provides global thermal anomalies and active fire monitoring. The standard science and near-real-time products are processed and distributed by NASA LANCE / FIRMS (Fire Information for Resource Management System).

This repository contains the analysis codebase, extraction pipelines, attribute schemas, and sample datasets for processing national and global country-level MODIS C6.1 fire records.

---

## 🗂️ Dataset Attributes

Each fire observation pixel corresponds to approximately 1 km spatial resolution at nadir and includes the following attributes:

| Field | Type | Description |
|---|---|---|
| `latitude` | Float | Latitude of the center of the 1 km fire pixel (WGS84) |
| `longitude` | Float | Longitude of the center of the 1 km fire pixel (WGS84) |
| `brightness` | Float | Brightness temperature (Kelvin) measured in channel 21/22 |
| `scan` | Float | Spatial resolution in along-scan direction |
| `track` | Float | Spatial resolution in along-track direction |
| `acq_date` | Date | Date of observation (YYYY-MM-DD) |
| `acq_time` | String | Time of observation in UTC (HHMM) |
| `satellite` | String | Satellite platform: `Terra` (morning overpass) or `Aqua` (afternoon overpass) |
| `instrument`| String | Instrument used: `MODIS` |
| `confidence`| Integer | Detection confidence score (0% to 100%) |
| `version` | String | Product collection and algorithm version |
| `bright_t31`| Float | Channel 31 brightness temperature (Kelvin) |
| `frp` | Float | Fire Radiative Power in MegaWatts (MW) |
| `daynight` | String | `D` = Daytime detection, `N` = Nighttime detection |
| `type` | Integer | Detection type (0=presumed vegetation fire, 1=active volcano, 2=other static source, 3=offshore) |

---

## 💾 Data Storage & Releases

- **GitHub Release (v1.0.0):** Yearly country archives are hosted as release assets on the [v1.0.0 Release Page](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0).
  - [Download 2000 Archive (modis_2000_all_countries.zip)](https://github.com/nisha200726/MODIS-C6.1/releases/download/v1.0.0/modis_2000_all_countries.zip)
- **Local Storage:** The full collection of 26 annual ZIP archives (2000–2025, ~1.80 GiB) and extracted country CSVs are kept locally and excluded from Git history via `.gitignore` to maintain a lightweight, fast repository.
- **Sample Datasets:** Small sample datasets and attribute descriptors are maintained in [`sample_data/`](sample_data/) for immediate out-of-the-box testing.
- **Source Code & Pipelines:** Analysis, filtering, and upload utilities are tracked in [`scripts/`](scripts/).

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/nisha200726/MODIS-C6.1.git
cd MODIS-C6.1
pip install -r requirements.txt
```

### 2. Run Data Processing & Summary

Process sample data or your local extracted country dataset:

```bash
# Run analysis on sample dataset
python scripts/process_modis.py --file sample_data/modis_2000_Afghanistan.csv

# Filter high-confidence fires (>=80%) and save output
python scripts/process_modis.py --file sample_data/modis_2000_Afghanistan.csv --min-confidence 80 --output sample_data/high_conf_fires.csv
```

---

## 📊 Citation & Disclaimer

Data courtesy of **NASA Earth Science Data and Information System (ESDIS) Project** and **LANCE FIRMS**.

> NASA promotes the full and open sharing of all data with the research and applications communities, private industry, academia, and the general public.
> Information presented through LANCE and FIRMS are provided "as is". For detailed user guides and citations, visit: [NASA FIRMS Citation Guidelines](https://earthdata.nasa.gov/earth-observation-data/near-real-time/citation#ed-firms-citation).
