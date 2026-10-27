"""
NASA MODIS C6.1 Active Fire / Hotspot Data Processing & Analysis Tool
Dataset: MODIS Collection 6.1 (Terra / Aqua) Near Real-Time & Standard Fire Products
Works with standard Python library (csv) or Pandas if available.
"""

import os
import sys
import csv
import argparse
from datetime import datetime
from collections import Counter


def load_modis_records(filepath: str) -> tuple[list[str], list[dict]]:
    """Load MODIS fire data CSV into list of dictionaries."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    records = []
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            records.append(row)
    return fieldnames, records


def analyze_records(records: list[dict]) -> dict:
    """Analyze MODIS fire records using standard library."""
    total = len(records)
    if total == 0:
        return {'total_detections': 0}

    dates = set()
    satellites = Counter()
    daynights = Counter()
    brightness_vals = []
    frp_vals = []
    conf_low = 0
    conf_nom = 0
    conf_high = 0

    for r in records:
        # Date
        d_str = r.get('acq_date', '')
        if d_str:
            dates.add(d_str)

        # Satellite
        sat = r.get('satellite', 'Unknown')
        satellites[sat] += 1

        # Day / Night
        dn = r.get('daynight', 'Unknown')
        daynights[dn] += 1

        # Brightness
        try:
            b = float(r.get('brightness', '0'))
            brightness_vals.append(b)
        except ValueError:
            pass

        # FRP
        try:
            f = float(r.get('frp', '0'))
            frp_vals.append(f)
        except ValueError:
            pass

        # Confidence
        try:
            c = float(r.get('confidence', '0'))
            if c < 30:
                conf_low += 1
            elif c < 80:
                conf_nom += 1
            else:
                conf_high += 1
        except ValueError:
            pass

    sorted_dates = sorted(dates)
    min_date = sorted_dates[0] if sorted_dates else "N/A"
    max_date = sorted_dates[-1] if sorted_dates else "N/A"

    mean_b = sum(brightness_vals) / len(brightness_vals) if brightness_vals else 0
    max_b = max(brightness_vals) if brightness_vals else 0

    mean_f = sum(frp_vals) / len(frp_vals) if frp_vals else 0
    max_f = max(frp_vals) if frp_vals else 0

    return {
        'total_detections': total,
        'unique_dates': len(dates),
        'date_range': (min_date, max_date),
        'brightness_mean': round(mean_b, 2),
        'brightness_max': round(max_b, 2),
        'frp_mean': round(mean_f, 2),
        'frp_max': round(max_f, 2),
        'satellites': dict(satellites),
        'day_night_distribution': dict(daynights),
        'confidence_stats': {
            'low (<30%)': conf_low,
            'nominal (30-79%)': conf_nom,
            'high (>=80%)': conf_high
        }
    }


def print_summary(summary: dict) -> None:
    """Print formatted summary of analysis."""
    print("=" * 60)
    print("       NASA MODIS C6.1 FIRE DATA ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Total Detections       : {summary['total_detections']:,}")
    print(f"Unique Dates Count     : {summary.get('unique_dates', 0)}")
    date_range = summary.get('date_range', ('N/A', 'N/A'))
    print(f"Date Range             : {date_range[0]} to {date_range[1]}")
    print(f"Mean Brightness (K)    : {summary.get('brightness_mean', 'N/A')}")
    print(f"Max Brightness (K)     : {summary.get('brightness_max', 'N/A')}")
    print(f"Mean FRP (MW)          : {summary.get('frp_mean', 'N/A')}")
    print(f"Max FRP (MW)           : {summary.get('frp_max', 'N/A')}")
    print(f"Satellites             : {summary.get('satellites', {})}")
    print(f"Day / Night Detections : {summary.get('day_night_distribution', {})}")

    if 'confidence_stats' in summary:
        print("\nConfidence Breakdown:")
        total = summary['total_detections']
        for cat, count in summary['confidence_stats'].items():
            pct = (count / total * 100) if total > 0 else 0
            print(f"  - {cat:<18}: {count:,} ({pct:.1f}%)")
    print("=" * 60)


def filter_records(records: list[dict], min_conf: float) -> list[dict]:
    """Filter records by confidence."""
    res = []
    for r in records:
        try:
            if float(r.get('confidence', '0')) >= min_conf:
                res.append(r)
        except ValueError:
            pass
    return res


def save_records(filepath: str, fieldnames: list[str], records: list[dict]) -> None:
    """Save records to CSV."""
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main():
    parser = argparse.ArgumentParser(description="Process NASA MODIS C6.1 Fire Hotspot Data")
    parser.add_argument("--file", "-f", type=str, default="sample_data/modis_2000_Afghanistan.csv",
                        help="Path to MODIS CSV file")
    parser.add_argument("--min-confidence", "-c", type=float, default=None,
                        help="Minimum confidence threshold (0-100)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Path to save filtered results")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: Specified file does not exist: {args.file}")
        sys.exit(1)

    print(f"Loading MODIS fire dataset from: {args.file}")
    fieldnames, records = load_modis_records(args.file)
    summary = analyze_records(records)
    print_summary(summary)

    if args.min_confidence is not None:
        filtered = filter_records(records, args.min_confidence)
        print(f"\nFiltered {len(filtered)} detections with confidence >= {args.min_confidence}%")
        if args.output:
            save_records(args.output, fieldnames, filtered)
            print(f"Saved filtered results to: {args.output}")


if __name__ == "__main__":
    main()
