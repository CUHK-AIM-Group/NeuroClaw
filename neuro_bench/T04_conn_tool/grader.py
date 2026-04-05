#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 4: Functional Connectivity Extraction.

Scoring rule: verify generated FC matrix has valid dimensions and values.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Optional, Tuple

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
INPUT_FMRI = ROOT / "hcp-subset" / "sub-100206" / "func" / "sub-100206_task-rest_bold.nii.gz"
RESULT_DIR = ROOT / "benchmark_results" / "T04_conn_tool"


def _load_from_json(path: Path) -> Optional[np.ndarray]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return np.array(data, dtype=float)
        if isinstance(data, dict):
            for key in ["fc_matrix", "fc", "connectivity", "matrix", "data"]:
                if key in data:
                    return np.array(data[key], dtype=float)
        return None
    except Exception:
        return None


def _load_from_csv(path: Path) -> Optional[np.ndarray]:
    try:
        rows = []
        with path.open("r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                rows.append([float(x) for x in row])
        if not rows:
            return None
        return np.array(rows, dtype=float)
    except Exception:
        return None


def _load_from_text(path: Path) -> Optional[np.ndarray]:
    try:
        return np.loadtxt(path, dtype=float)
    except Exception:
        return None


def load_fc_matrix(path: Path) -> Optional[np.ndarray]:
    suffix = path.suffix.lower()

    if path.name.lower().endswith(".nii.gz"):
        return None

    if suffix == ".npy":
        try:
            arr = np.load(path)
            return np.array(arr, dtype=float)
        except Exception:
            return None

    if suffix == ".npz":
        try:
            z = np.load(path)
            if "fc_matrix" in z:
                return np.array(z["fc_matrix"], dtype=float)
            if "fc" in z:
                return np.array(z["fc"], dtype=float)
            keys = list(z.keys())
            if keys:
                return np.array(z[keys[0]], dtype=float)
            return None
        except Exception:
            return None

    if suffix in {".csv", ".tsv"}:
        return _load_from_csv(path)

    if suffix == ".json":
        return _load_from_json(path)

    if suffix in {".txt", ".dat"}:
        return _load_from_text(path)

    return None


def validate_fc(fc: np.ndarray) -> Tuple[bool, str]:
    if fc is None:
        return False, "FC matrix not found or unreadable"

    if not isinstance(fc, np.ndarray):
        return False, "FC is not a numpy array"

    if fc.ndim != 2:
        return False, f"FC matrix must be 2D, got ndim={fc.ndim}"

    n, m = fc.shape
    if n != m:
        return False, f"FC matrix must be square, got shape={fc.shape}"

    if n < 10:
        return False, f"FC dimension too small, got N={n}, expected N>=10"

    if not np.isfinite(fc).all():
        return False, "FC matrix contains NaN or Inf"

    # FC should be approximately symmetric.
    max_asym = float(np.max(np.abs(fc - fc.T)))
    if max_asym > 1e-2:
        return False, f"FC matrix is not symmetric enough, max|A-A^T|={max_asym:.6f}"

    return True, f"valid FC shape={fc.shape}, max|A-A^T|={max_asym:.6f}"


def pick_latest_fc_file(result_dir: Path) -> Optional[Path]:
    if not result_dir.exists() or not result_dir.is_dir():
        return None

    candidates = []
    for ext in ["*.npy", "*.npz", "*.csv", "*.tsv", "*.json", "*.txt", "*.dat"]:
        candidates.extend(result_dir.glob(ext))

    # Prefer files that look like FC outputs by name.
    fc_named = [p for p in candidates if "fc" in p.name.lower() or "connect" in p.name.lower()]
    pool = fc_named if fc_named else candidates

    if not pool:
        return None

    pool_sorted = sorted(pool, key=lambda p: p.stat().st_mtime, reverse=True)
    return pool_sorted[0]


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 4: Functional Connectivity Extraction")
    print("=" * 70)

    if not INPUT_FMRI.exists():
        print("❌ 任务缺少输入")
        print(f"Missing input file: {INPUT_FMRI}")
        return 1

    if not RESULT_DIR.exists() or not RESULT_DIR.is_dir():
        print(f"❌ Output directory not found: {RESULT_DIR}")
        return 1

    fc_file = pick_latest_fc_file(RESULT_DIR)
    if fc_file is None:
        print(f"❌ No FC result file found in {RESULT_DIR}")
        return 1

    print(f"Using FC file: {fc_file}")
    fc = load_fc_matrix(fc_file)
    ok, msg = validate_fc(fc)
    if not ok:
        print(f"❌ FAIL: {msg}")
        return 1

    print(f"✅ PASS: {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(grade())
