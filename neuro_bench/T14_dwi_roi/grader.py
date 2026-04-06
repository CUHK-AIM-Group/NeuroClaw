#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 14: DWI ROI Statistics.

Automatic checks:
1. At least one roi_stats_*.csv exists
2. Required columns exist
3. Rows are sorted by label
4. n_vox >= 10
5. p05 <= median <= p95 and std >= 0
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[2]
RESULT_DIR = ROOT / "benchmark_results" / "T14_dwi_roi"

REQUIRED_COLUMNS = ["label", "n_vox", "mean", "median", "std", "p05", "p95"]


def parse_float(v: str) -> float:
    return float(v.strip())


def parse_int(v: str) -> int:
    return int(float(v.strip()))


def check_csv(path: Path) -> bool:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            print(f"❌ {path.name}: missing header")
            return False

        missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        if missing:
            print(f"❌ {path.name}: missing columns {missing}")
            return False

        labels: List[int] = []
        row_count = 0

        for row in reader:
            row_count += 1
            try:
                label = parse_int(row["label"])
                n_vox = parse_int(row["n_vox"])
                mean = parse_float(row["mean"])
                median = parse_float(row["median"])
                std = parse_float(row["std"])
                p05 = parse_float(row["p05"])
                p95 = parse_float(row["p95"])
            except Exception as e:
                print(f"❌ {path.name}: parse error in row {row_count}: {e}")
                return False

            if n_vox < 10:
                print(f"❌ {path.name}: n_vox < 10 at label {label}")
                return False

            if std < 0:
                print(f"❌ {path.name}: std < 0 at label {label}")
                return False

            if not (p05 <= median <= p95):
                print(f"❌ {path.name}: percentile relation invalid at label {label}")
                return False

            labels.append(label)

        if row_count == 0:
            print(f"❌ {path.name}: empty data rows")
            return False

        if labels != sorted(labels):
            print(f"❌ {path.name}: labels are not sorted ascending")
            return False

    print(f"✅ {path.name}: valid ({row_count} rows)")
    return True


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 14: DWI ROI Statistics")
    print("=" * 70)

    if not RESULT_DIR.exists() or not RESULT_DIR.is_dir():
        print(f"❌ Result directory not found: {RESULT_DIR}")
        return 1

    files = sorted(RESULT_DIR.glob("roi_stats_*.csv"))
    if not files:
        print("❌ No roi_stats_*.csv files found")
        return 1

    ok_all = True
    for p in files:
        if not check_csv(p):
            ok_all = False

    if not ok_all:
        print("❌ FAIL: ROI statistics validation failed")
        return 1

    print("✅ PASS: ROI statistics files are valid")
    return 0


if __name__ == "__main__":
    sys.exit(grade())
