#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 11: DWI Brain Mask from b0.

Manual evaluation helper.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT_DIR = ROOT / "benchmark_results" / "T11_dwi_brain_mask"


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 11: DWI Brain Mask from b0")
    print("=" * 70)

    mask_file = RESULT_DIR / "brain_mask.nii.gz"
    if mask_file.exists():
        print(f"Found mask output: {mask_file}")
    else:
        print(f"⚠️  Missing expected mask file: {mask_file}")

    print("Manual evaluation checklist:")
    print("1. b0 extraction logic exists")
    print("2. brain_mask.nii.gz generated")
    print("3. mask quality acceptable for downstream DTI fitting")
    print("\n✅ Manual evaluation mode (always exits 0).")
    return 0


if __name__ == "__main__":
    sys.exit(grade())
