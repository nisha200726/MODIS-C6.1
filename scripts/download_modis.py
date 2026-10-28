"""
NASA MODIS C6.1 Automated Data Downloader & Extractor
Directly fetches official NASA FIRMS MODIS Collection 6.1 yearly country archives (2000–2025).
"""

import os
import sys
import argparse
import zipfile
import urllib.request
import urllib.error

BASE_URL = "https://firms.modaps.eosdis.nasa.gov/data/country/modis/{year}/modis_{year}_all_countries.zip"
ALL_YEARS = list(range(2000, 2026))


def download_year(year: int, target_dir: str = ".", extract: bool = False) -> str:
    """Download yearly archive from NASA FIRMS and optionally extract."""
    if year not in ALL_YEARS:
        raise ValueError(f"Year {year} is not in range 2000-2025.")

    url = BASE_URL.format(year=year)
    zip_filename = f"modis_{year}_all_countries.zip"
    zip_path = os.path.join(target_dir, zip_filename)

    if os.path.exists(zip_path) and os.path.getsize(zip_path) > 1000:
        print(f"[{year}] Local archive already exists: {zip_path}")
    else:
        print(f"[{year}] Downloading from NASA FIRMS: {url}")
        try:
            urllib.request.urlretrieve(url, zip_path)
            size_mb = os.path.getsize(zip_path) / (1024 * 1024)
            print(f"[{year}] Download complete: {size_mb:.2f} MB")
        except Exception as e:
            print(f"[{year}] Download failed: {e}")
            return ""

    if extract:
        extract_folder = os.path.join(target_dir, f"modis_{year}_all_countries")
        print(f"[{year}] Extracting to: {extract_folder} ...")
        os.makedirs(extract_folder, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_folder)
        csv_count = sum(len(files) for _, _, files in os.walk(extract_folder) if any(f.endswith('.csv') for f in files))
        print(f"[{year}] Extracted {csv_count} CSV files successfully.")

    return zip_path


def main():
    parser = argparse.ArgumentParser(description="Download and extract NASA MODIS C6.1 Country Datasets")
    parser.add_argument("--year", "-y", type=int, default=None,
                        help="Specific year to download (2000-2025)")
    parser.add_argument("--all", action="store_true",
                        help="Download all 26 years (2000-2025)")
    parser.add_argument("--extract", "-x", action="store_true",
                        help="Extract downloaded archives into country CSV folders")
    parser.add_argument("--output-dir", "-o", type=str, default=".",
                        help="Target output directory (default: current directory)")

    args = parser.parse_args()

    if not args.year and not args.all:
        print("Please specify a year with --year <YYYY> (2000-2025) or use --all.")
        parser.print_help()
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    years_to_process = ALL_YEARS if args.all else [args.year]
    for y in years_to_process:
        download_year(y, target_dir=args.output_dir, extract=args.extract)


if __name__ == "__main__":
    main()
