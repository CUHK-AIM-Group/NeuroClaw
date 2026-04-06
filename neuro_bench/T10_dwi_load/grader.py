#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 10: DWI Load and Consistency Check.

Manual evaluation helper.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT_DIR = ROOT / "benchmark_results" / "T10_dwi_load"


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 10: DWI Load and Consistency Check")
    print("=" * 70)

    if not RESULT_DIR.exists() or not RESULT_DIR.is_dir():
        print(f"⚠️  Result directory not found: {RESULT_DIR}")
    else:
        files = sorted([p for p in RESULT_DIR.iterdir() if p.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)
        if files:
            print(f"Found result artifact(s), latest: {files[0].name}")
        else:
            print("⚠️  No result artifact found")

    print("Manual evaluation checklist:")
    print("1. DWI/.bval/.bvec loaded")
    print("2. DWI 4D check performed")
    print("3. Gradient counts validated against volume count")
    print("4. Arrays retained in memory and result artifact recorded")
    print("\n✅ Manual evaluation mode (always exits 0).")
    return 0


if __name__ == "__main__":
    sys.exit(grade())
