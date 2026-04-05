#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 2: BIDS Organizer (HCP Subset)

Checks whether ./hcp-subset exists and follows a minimum BIDS layout
for T1w (anat) and fMRI BOLD (func).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
HCP_SUBSET = ROOT / "hcp-subset"


def find_subject_dirs(root: Path) -> List[Path]:
    return sorted([p for p in root.glob("sub-*") if p.is_dir()])


def has_t1w_pair(sub_dir: Path) -> Tuple[bool, str]:
    anat_dir = sub_dir / "anat"
    if not anat_dir.is_dir():
        return False, "missing anat/"

    sid = sub_dir.name
    nii_matches = list(anat_dir.glob(f"{sid}_T1w.nii")) + list(anat_dir.glob(f"{sid}_T1w.nii.gz"))
    json_match = anat_dir / f"{sid}_T1w.json"

    if not nii_matches:
        return False, f"missing {sid}_T1w.nii(.gz)"
    if not json_match.is_file():
        return False, f"missing {sid}_T1w.json"

    return True, "ok"


def has_bold_pair(sub_dir: Path) -> Tuple[bool, str]:
    func_dir = sub_dir / "func"
    if not func_dir.is_dir():
        return False, "missing func/"

    sid = sub_dir.name
    nii_pattern = re.compile(rf"^{re.escape(sid)}_task-[A-Za-z0-9]+_bold\\.nii(\\.gz)?$")
    json_pattern = re.compile(rf"^{re.escape(sid)}_task-[A-Za-z0-9]+_bold\\.json$")

    nii_files = [p.name for p in func_dir.iterdir() if p.is_file() and nii_pattern.match(p.name)]
    json_files = [p.name for p in func_dir.iterdir() if p.is_file() and json_pattern.match(p.name)]

    if not nii_files:
        return False, f"missing {sid}_task-<task>_bold.nii(.gz)"
    if not json_files:
        return False, f"missing {sid}_task-<task>_bold.json"

    return True, "ok"


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 2: BIDS Organizer (HCP Subset)")
    print("=" * 70)

    if not HCP_SUBSET.exists():
        print("❌ 任务缺少输入")
        print(f"Missing input folder: {HCP_SUBSET}")
        return 1

    if not HCP_SUBSET.is_dir():
        print("❌ ./hcp-subset exists but is not a directory")
        return 1

    dataset_desc = HCP_SUBSET / "dataset_description.json"
    if not dataset_desc.is_file():
        print("❌ Missing dataset_description.json")
        return 1

    subjects = find_subject_dirs(HCP_SUBSET)
    if not subjects:
        print("❌ No BIDS subject folders found (sub-*)")
        return 1

    print(f"Found {len(subjects)} subject folder(s)")

    failed = False
    for sub in subjects:
        print(f"\nChecking {sub.name}:")

        ok_t1w, msg_t1w = has_t1w_pair(sub)
        if ok_t1w:
            print("  ✅ anat T1w pair")
        else:
            print(f"  ❌ anat T1w pair: {msg_t1w}")
            failed = True

        ok_bold, msg_bold = has_bold_pair(sub)
        if ok_bold:
            print("  ✅ func BOLD pair")
        else:
            print(f"  ❌ func BOLD pair: {msg_bold}")
            failed = True

    print("\n" + "=" * 70)
    if failed:
        print("❌ FAIL: BIDS structure is not valid for all subjects")
        return 1

    print("✅ PASS: BIDS structure is valid")
    return 0


if __name__ == "__main__":
    sys.exit(grade())
