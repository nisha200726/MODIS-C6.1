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

## 💾 Data Access & Download

The complete global dataset comprises **26 annual archives (2000–2025)** containing **5,275 country-level CSV files** (~1.82 GiB compressed, ~8.11 GiB uncompressed).

To avoid repository bloat, connection timeouts, and Git bandwidth limitations, raw datasets are kept outside Git history and can be downloaded on-demand using our automated script or direct links below.

### 📥 Automated Downloader & Extractor

Use the built-in script [`scripts/download_modis.py`](scripts/download_modis.py) to download and extract any year or the entire collection:

```bash
# Download and extract a specific year (e.g. 2024)
python scripts/download_modis.py --year 2024 --extract

# Download all 26 yearly archives (2000-2025)
python scripts/download_modis.py --all

# Download and extract all archives into country-wise folders
python scripts/download_modis.py --all --extract
```

### 📋 Complete Dataset Inventory & Direct Download Links

| Year | Archive Filename | Compressed Size | Country CSVs | Direct Download Link | GitHub Release Asset |
|:---:|---|:---:|:---:|:---:|:---:|
| **2000** | `modis_2000_all_countries.zip` | 4.44 MB | 163 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2000/modis_2000_all_countries.zip) | [Release v1.0.0 Asset](https://github.com/nisha200726/MODIS-C6.1/releases/download/v1.0.0/modis_2000_all_countries.zip) |
| **2001** | `modis_2001_all_countries.zip` | 30.08 MB | 197 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2001/modis_2001_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2002** | `modis_2002_all_countries.zip` | 62.25 MB | 199 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2002/modis_2002_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2003** | `modis_2003_all_countries.zip` | 86.19 MB | 204 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2003/modis_2003_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2004** | `modis_2004_all_countries.zip` | 85.22 MB | 202 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2004/modis_2004_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2005** | `modis_2005_all_countries.zip` | 85.77 MB | 208 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2005/modis_2005_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2006** | `modis_2006_all_countries.zip` | 78.62 MB | 202 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2006/modis_2006_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2007** | `modis_2007_all_countries.zip` | 85.85 MB | 208 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2007/modis_2007_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2008** | `modis_2008_all_countries.zip` | 80.67 MB | 205 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2008/modis_2008_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2009** | `modis_2009_all_countries.zip` | 74.66 MB | 205 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2009/modis_2009_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2010** | `modis_2010_all_countries.zip` | 78.86 MB | 203 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2010/modis_2010_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2011** | `modis_2011_all_countries.zip` | 78.70 MB | 201 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2011/modis_2011_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2012** | `modis_2012_all_countries.zip` | 83.07 MB | 204 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2012/modis_2012_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2013** | `modis_2013_all_countries.zip` | 70.84 MB | 207 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2013/modis_2013_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2014** | `modis_2014_all_countries.zip` | 74.31 MB | 204 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2014/modis_2014_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2015** | `modis_2015_all_countries.zip` | 79.32 MB | 209 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2015/modis_2015_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2016** | `modis_2016_all_countries.zip` | 73.90 MB | 207 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2016/modis_2016_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2017** | `modis_2017_all_countries.zip` | 74.66 MB | 205 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2017/modis_2017_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2018** | `modis_2018_all_countries.zip` | 70.46 MB | 206 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2018/modis_2018_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2019** | `modis_2019_all_countries.zip` | 76.72 MB | 202 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2019/modis_2019_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2020** | `modis_2020_all_countries.zip` | 74.35 MB | 211 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2020/modis_2020_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2021** | `modis_2021_all_countries.zip` | 73.70 MB | 204 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2021/modis_2021_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2022** | `modis_2022_all_countries.zip` | 63.39 MB | 204 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2022/modis_2022_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2023** | `modis_2023_all_countries.zip` | 77.98 MB | 207 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2023/modis_2023_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2024** | `modis_2024_all_countries.zip` | 80.63 MB | 206 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2024/modis_2024_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **2025** | `modis_2025_all_countries.zip` | 61.77 MB | 202 files | [NASA FIRMS Download](https://firms.modaps.eosdis.nasa.gov/data/country/modis/2025/modis_2025_all_countries.zip) | [Release v1.0.0](https://github.com/nisha200726/MODIS-C6.1/releases/tag/v1.0.0) |
| **Total**| **26 archives** | **~1.82 GiB** | **5,275 CSVs** | **Full 2000–2025 Coverage** | [All Releases](https://github.com/nisha200726/MODIS-C6.1/releases) |

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
