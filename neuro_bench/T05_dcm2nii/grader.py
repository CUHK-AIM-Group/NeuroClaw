#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 5: DICOM to NIfTI Conversion.

Scoring focus:
1. Input ./201 exists and has DICOM files.
2. Output contains at least one NIfTI file.
3. Generated NIfTI is consistent with source DICOM metadata
   (dimensions and voxel spacing, with practical tolerance).
"""

from __future__ import annotations

import gzip
import struct
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import pydicom
except Exception:
    pydicom = None


ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = ROOT / "201"
RESULT_DIR = ROOT / "benchmark_results" / "T05_dcm2nii"


@dataclass
class DicomSeriesInfo:
    series_uid: str
    file_count: int
    rows: int
    cols: int
    pixel_spacing: Optional[Tuple[float, float]]
    slice_spacing: Optional[float]


@dataclass
class NiftiInfo:
    path: Path
    shape: Tuple[int, int, int, int]
    pixdim: Tuple[float, float, float, float]


def find_dicom_files(folder: Path) -> List[Path]:
    files = []
    for p in folder.rglob("*"):
        if p.is_file():
            files.append(p)
    return files


def parse_dicom_series(folder: Path) -> Tuple[Optional[DicomSeriesInfo], str]:
    if pydicom is None:
        return None, "pydicom is not installed"

    all_files = find_dicom_files(folder)
    if not all_files:
        return None, "no files found in input folder"

    grouped: Dict[str, List[Path]] = defaultdict(list)
    first_ds: Dict[str, object] = {}

    for f in all_files:
        try:
            ds = pydicom.dcmread(str(f), stop_before_pixels=True, force=True)
        except Exception:
            continue

        series_uid = str(getattr(ds, "SeriesInstanceUID", ""))
        if not series_uid:
            continue

        grouped[series_uid].append(f)
        if series_uid not in first_ds:
            first_ds[series_uid] = ds

    if not grouped:
        return None, "no valid DICOM series found"

    # Use the largest series as reference.
    best_uid = max(grouped.keys(), key=lambda k: len(grouped[k]))
    ds = first_ds[best_uid]

    rows = int(getattr(ds, "Rows", 0) or 0)
    cols = int(getattr(ds, "Columns", 0) or 0)

    pixel_spacing = None
    ps = getattr(ds, "PixelSpacing", None)
    if ps and len(ps) >= 2:
        try:
            pixel_spacing = (float(ps[0]), float(ps[1]))
        except Exception:
            pixel_spacing = None

    slice_spacing = None
    for tag_name in ["SpacingBetweenSlices", "SliceThickness"]:
        val = getattr(ds, tag_name, None)
        if val is not None:
            try:
                slice_spacing = float(val)
                break
            except Exception:
                pass

    info = DicomSeriesInfo(
        series_uid=best_uid,
        file_count=len(grouped[best_uid]),
        rows=rows,
        cols=cols,
        pixel_spacing=pixel_spacing,
        slice_spacing=slice_spacing,
    )
    return info, "ok"


def _read_nifti_header(path: Path) -> Optional[bytes]:
    try:
        if path.suffix == ".gz":
            with gzip.open(path, "rb") as f:
                return f.read(348)
        with path.open("rb") as f:
            return f.read(348)
    except Exception:
        return None


def parse_nifti(path: Path) -> Optional[NiftiInfo]:
    header = _read_nifti_header(path)
    if not header or len(header) < 348:
        return None

    # Detect endian from sizeof_hdr (must be 348)
    little = struct.unpack("<I", header[0:4])[0]
    big = struct.unpack(">I", header[0:4])[0]

    if little == 348:
        e = "<"
    elif big == 348:
        e = ">"
    else:
        return None

    dim = struct.unpack(e + "8h", header[40:56])
    pixdim = struct.unpack(e + "8f", header[76:108])

    # dim[0] is number of dims. Use safe extraction.
    d1 = int(dim[1]) if len(dim) > 1 else 1
    d2 = int(dim[2]) if len(dim) > 2 else 1
    d3 = int(dim[3]) if len(dim) > 3 else 1
    d4 = int(dim[4]) if len(dim) > 4 else 1

    p1 = float(pixdim[1]) if len(pixdim) > 1 else 0.0
    p2 = float(pixdim[2]) if len(pixdim) > 2 else 0.0
    p3 = float(pixdim[3]) if len(pixdim) > 3 else 0.0
    p4 = float(pixdim[4]) if len(pixdim) > 4 else 0.0

    return NiftiInfo(path=path, shape=(d1, d2, d3, d4), pixdim=(p1, p2, p3, p4))


def pick_best_nifti(result_dir: Path) -> Optional[NiftiInfo]:
    if not result_dir.exists() or not result_dir.is_dir():
        return None

    nii_files = sorted(result_dir.rglob("*.nii")) + sorted(result_dir.rglob("*.nii.gz"))
    if not nii_files:
        return None

    parsed = [parse_nifti(p) for p in nii_files]
    parsed = [x for x in parsed if x is not None]
    if not parsed:
        return None

    # Prefer the largest voxel count in first 3 dims.
    parsed.sort(key=lambda x: x.shape[0] * x.shape[1] * x.shape[2], reverse=True)
    return parsed[0]


def close(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def validate_consistency(dcm: DicomSeriesInfo, nii: NiftiInfo) -> Tuple[bool, str]:
    nx, ny, nz, nt = nii.shape

    if nx <= 0 or ny <= 0 or nz <= 0:
        return False, f"invalid NIfTI shape: {nii.shape}"

    # Dimension consistency (DICOM Rows/Cols -> NIfTI X/Y).
    # Allow row/col swap because orientation handling may differ.
    dims_match_direct = (nx == dcm.cols and ny == dcm.rows)
    dims_match_swapped = (nx == dcm.rows and ny == dcm.cols)

    if dcm.rows > 0 and dcm.cols > 0 and not (dims_match_direct or dims_match_swapped):
        return False, (
            f"XY dims mismatch: DICOM rows/cols=({dcm.rows},{dcm.cols}), "
            f"NIfTI xy=({nx},{ny})"
        )

    # Z/T consistency: for 3D/4D NIfTI, total frames should be close to file_count.
    total_frames = nz * max(nt, 1)
    if dcm.file_count > 1:
        # Some converters may drop localizers or merge small differences, allow loose tolerance.
        if abs(total_frames - dcm.file_count) > max(5, int(dcm.file_count * 0.15)):
            return False, (
                f"slice/time count mismatch: DICOM files={dcm.file_count}, "
                f"NIfTI z*t={total_frames}"
            )

    # Spacing consistency (if DICOM spacing available).
    px, py, pz, _ = nii.pixdim
    if dcm.pixel_spacing is not None:
        sy, sx = dcm.pixel_spacing  # DICOM PixelSpacing is [row, col]

        # Compare with swap allowance.
        spacing_direct = close(px, sx, 0.3) and close(py, sy, 0.3)
        spacing_swapped = close(px, sy, 0.3) and close(py, sx, 0.3)
        if not (spacing_direct or spacing_swapped):
            return False, (
                f"pixel spacing mismatch: DICOM=({sy:.4f},{sx:.4f}), "
                f"NIfTI=({px:.4f},{py:.4f})"
            )

    if dcm.slice_spacing is not None and pz > 0:
        if not close(pz, dcm.slice_spacing, 1.0):
            return False, (
                f"slice spacing mismatch: DICOM={dcm.slice_spacing:.4f}, "
                f"NIfTI={pz:.4f}"
            )

    return True, "NIfTI is consistent with DICOM metadata"


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 5: DICOM to NIfTI Conversion")
    print("=" * 70)

    if not INPUT_DIR.exists() or not INPUT_DIR.is_dir():
        print("❌ 任务缺少输入")
        print(f"Missing input folder: {INPUT_DIR}")
        return 1

    dcm_info, msg = parse_dicom_series(INPUT_DIR)
    if dcm_info is None:
        print("❌ 任务缺少输入")
        print(f"Unable to parse DICOM input: {msg}")
        return 1

    print(f"Reference DICOM series: {dcm_info.series_uid}")
    print(f"DICOM files: {dcm_info.file_count}, rows={dcm_info.rows}, cols={dcm_info.cols}")

    nii_info = pick_best_nifti(RESULT_DIR)
    if nii_info is None:
        print(f"❌ No valid NIfTI file found in: {RESULT_DIR}")
        return 1

    print(f"Checking NIfTI: {nii_info.path}")
    print(f"NIfTI shape: {nii_info.shape}, pixdim: {nii_info.pixdim}")

    ok, reason = validate_consistency(dcm_info, nii_info)
    if not ok:
        print(f"❌ FAIL: {reason}")
        return 1

    print(f"✅ PASS: {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(grade())
