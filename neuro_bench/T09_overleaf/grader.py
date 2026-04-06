#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 9: Overleaf Upload.

This benchmark is manually evaluated.
This script is a helper that checks whether a result artifact exists
and then exits with code 0 while reminding reviewer to do manual scoring.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT_DIR = ROOT / "benchmark_results" / "T09_overleaf"


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 9: Overleaf Upload")
    print("=" * 70)

    if not RESULT_DIR.exists() or not RESULT_DIR.is_dir():
        print(f"⚠️  Result directory not found: {RESULT_DIR}")
        print("Manual evaluation required; no automatic fail enforced.")
        return 0

    files = sorted([p for p in RESULT_DIR.iterdir() if p.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)

    if not files:
        print(f"⚠️  No result files found in {RESULT_DIR}")
        print("Manual evaluation required; no automatic fail enforced.")
        return 0

    print(f"Found result artifact(s), latest: {files[0].name}")
    print("Manual evaluation checklist:")
    print("1. User cookie interaction occurred")
    print("2. Project 'cvpr_paper' lookup attempted")
    print("3. If missing, project creation attempted")
    print("4. On creation failure, process exited")
    print("5. Upload from ./cvpr_paper was attempted and outcome recorded")
    print("\n✅ Manual evaluation mode (always exits 0).")
    return 0


if __name__ == "__main__":
    sys.exit(grade())
