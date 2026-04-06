#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 12: DTI Fit on Selected b-values.

Manual evaluation helper.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT_DIR = ROOT / "benchmark_results" / "T12_dti_fit"


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 12: DTI Fit on Selected b-values")
    print("=" * 70)

    if not RESULT_DIR.exists() or not RESULT_DIR.is_dir():
        print(f"⚠️  Result directory not found: {RESULT_DIR}")
    else:
        files = sorted([p for p in RESULT_DIR.iterdir() if p.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)
        print(f"Result artifacts: {len(files)}")
        if files:
            print(f"Latest artifact: {files[0].name}")

    print("Manual evaluation checklist:")
    print("1. b-value subset selection is reasonable")
    print("2. Tensor fitting executed successfully")
    print("3. Outputs are ready for DTI metric computation")
    print("\n✅ Manual evaluation mode (always exits 0).")
    return 0


if __name__ == "__main__":
    sys.exit(grade())
