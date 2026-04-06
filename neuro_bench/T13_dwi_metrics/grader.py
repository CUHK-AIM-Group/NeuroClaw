#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 13: DTI Core Metrics.

Automatic checks:
1. FA/MD/AD/RD NIfTI outputs exist
2. Shapes are consistent and 3D
3. Values are finite
4. Negative values are not present (with tolerance)
5. If mask exists in output folder, outside-mask voxels are zero
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np

try:
    import nibabel as nib
except Exception:
    nib = None

ROOT = Path(__file__).resolve().parents[2]
RESULT_DIR = ROOT / "benchmark_results" / "T13_dwi_metrics"
METRICS = ["FA", "MD", "AD", "RD"]


def find_metric_file(name: str) -> Optional[Path]:
    candidates = list(RESULT_DIR.glob(f"{name}.nii")) + list(RESULT_DIR.glob(f"{name}.nii.gz"))
    if candidates:
        return sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]

    loose = list(RESULT_DIR.glob(f"*{name}*.nii")) + list(RESULT_DIR.glob(f"*{name}*.nii.gz"))
    if loose:
        return sorted(loose, key=lambda p: p.stat().st_mtime, reverse=True)[0]

    return None


def load_nifti(path: Path) -> np.ndarray:
    img = nib.load(str(path))
    data = np.asarray(img.get_fdata(dtype=np.float32))
    return data


def find_mask() -> Optional[Path]:
    for name in ["brain_mask.nii.gz", "brain_mask.nii", "mask.nii.gz", "mask.nii"]:
        p = RESULT_DIR / name
        if p.exists():
            return p
    return None


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 13: DTI Core Metrics")
    print("=" * 70)

    if nib is None:
        print("❌ nibabel is required for this grader but not installed")
        return 1

    if not RESULT_DIR.exists() or not RESULT_DIR.is_dir():
        print(f"❌ Result directory not found: {RESULT_DIR}")
        return 1

    paths: Dict[str, Path] = {}
    for m in METRICS:
        p = find_metric_file(m)
        if p is None:
            print(f"❌ Missing metric file for {m}")
            return 1
        paths[m] = p
        print(f"Found {m}: {p.name}")

    arrays: Dict[str, np.ndarray] = {}
    ref_shape: Optional[Tuple[int, ...]] = None

    for m, p in paths.items():
        arr = load_nifti(p)
        arrays[m] = arr

        if arr.ndim != 3:
            print(f"❌ {m} is not 3D: shape={arr.shape}")
            return 1

        if ref_shape is None:
            ref_shape = arr.shape
        elif arr.shape != ref_shape:
            print(f"❌ Shape mismatch: {m} shape={arr.shape}, expected={ref_shape}")
            return 1

        if not np.isfinite(arr).all():
            print(f"❌ {m} contains NaN/Inf")
            return 1

        # Safety check: should not contain meaningful negative values.
        if float(arr.min()) < -1e-6:
            print(f"❌ {m} contains negative values below tolerance: min={arr.min()} ")
            return 1

    # FA additional range sanity (allow small numerical tolerance)
    fa = arrays["FA"]
    if float(fa.max()) > 1.2:
        print(f"❌ FA max too large: {fa.max()} (expected <= 1.2)")
        return 1

    # Optional mask-outside-zero check
    mask_path = find_mask()
    if mask_path is not None:
        mask = load_nifti(mask_path)
        if mask.shape != ref_shape:
            print(f"❌ Mask shape mismatch: mask={mask.shape}, metrics={ref_shape}")
            return 1

        outside = mask <= 0
        for m, arr in arrays.items():
            outside_abs_max = float(np.max(np.abs(arr[outside]))) if np.any(outside) else 0.0
            if outside_abs_max > 1e-6:
                print(f"❌ {m} has non-zero values outside mask: max_abs={outside_abs_max}")
                return 1
        print("Mask outside-zero check: passed")
    else:
        print("Mask not found in result directory; outside-zero check skipped")

    print("✅ PASS: DTI metrics outputs are valid")
    return 0


if __name__ == "__main__":
    sys.exit(grade())
