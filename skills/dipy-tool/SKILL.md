---
name: dipy-tool
description: "Use this skill whenever any NeuroClaw diffusion MRI / DWI modality skill needs to execute concrete DIPY operations: load DWI (NIfTI+bvals+bvecs), optional masking, DTI fitting, compute FA/MD/AD/RD, and extract ROI statistics. This is the dedicated base/tool skill that contains all specific DIPY code and usage patterns. Never called directly by the user."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# DIPY Tool (Base/Tool Layer)

## Overview
`dipy-tool` is the **NeuroClaw base/tool skill** that provides the concrete **DIPY** implementation for diffusion MRI (DWI/DTI) processing and feature extraction.

It is **never called directly by the user**. It is delegated to by a diffusion modality-layer skill (e.g., future `dti-skill` / `dmri-skill`) and executed via `claw-shell` for safety, logging, and long-running stability.

This skill provides:
- Robust loading of **DWI NIfTI + bvals + bvecs** with sanity checks.
- Brain mask generation (`median_otsu`) or use of a provided mask.
- **DTI fitting** (optionally selecting a b-value range) and metric export:
  - **FA / MD / AD / RD** as NIfTI maps
- **ROI / atlas statistics** extraction (CSV summaries).

**Research use only** — not for clinical diagnosis.

---

## Quick Reference (Core Tasks)

| Task | What it does | Output |
|---|---|---|
| Load DWI + gradients | Validates shapes, loads NIfTI+bvals+bvecs | in-memory arrays |
| Brain mask | Auto mask (median_otsu) or use external | `brain_mask.nii.gz` |
| DTI fit | TensorModel fit on selected volumes | tensor fit object |
| Export tensor metrics | Compute & save FA/MD/AD/RD | `FA.nii.gz`, `MD.nii.gz`, `AD.nii.gz`, `RD.nii.gz` |
| ROI stats | Per-label summary (mean/median/std/p05/p95) | `roi_stats_FA.csv`, etc. |

---

## Installation (Handled by `dependency-planner`)
This tool is installed automatically when required.

Recommended isolated environment:
```bash
conda create -n neuroclaw-dipy python=3.11 -y
conda activate neuroclaw-dipy
conda install -c conda-forge dipy nibabel numpy scipy scikit-image pandas -y
# Optional:
conda install -c conda-forge matplotlib -y
```

**Recommended execution pattern (avoids shell activation pitfalls):**
- Use `conda run -n neuroclaw-dipy ...` routed through `claw-shell`.

---

## NeuroClaw recommended wrapper script: `dipy_pipeline.py`

> Place at: `skills/dipy-tool/dipy_pipeline.py`
> All real runs must be delegated to `claw-shell`.

```python
#!/usr/bin/env python3
# NeuroClaw DIPY Tool – DTI metrics + ROI statistics
# Updated: 2026-03-26

from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import nibabel as nib

from dipy.io.image import load_nifti, save_nifti
from dipy.io.gradients import read_bvals_bvecs
from dipy.core.gradients import gradient_table
from dipy.segment.mask import median_otsu
from dipy.reconst.dti import TensorModel, fractional_anisotropy


def load_dwi(dwi_path: str, bval_path: str, bvec_path: str):
    data, affine = load_nifti(dwi_path)
    bvals, bvecs = read_bvals_bvecs(bval_path, bvec_path)

    if data.ndim != 4:
        raise ValueError(f"DWI must be 4D (x,y,z,vol). Got shape={data.shape}")
    if data.shape[-1] != len(bvals) or data.shape[-1] != len(bvecs):
        raise ValueError(
            f"Volumes != gradients: data[-1]={data.shape[-1]}, "
            f"len(bvals)={len(bvals)}, len(bvecs)={len(bvecs)}"
        )

    return data.astype(np.float32), affine, bvals.astype(float), bvecs.astype(float)


def read_mask(mask_path: str) -> np.ndarray:
    m = nib.load(mask_path).get_fdata()
    return (m > 0).astype(np.uint8)


def make_mask(data: np.ndarray, bvals: np.ndarray, affine: np.ndarray,
              out_mask_path: Path, b0_thr: float = 50.0) -> np.ndarray:
    b0_idx = np.where(bvals < b0_thr)[0]
    if b0_idx.size == 0:
        raise ValueError("No b0 volumes found (bvals < b0_thr). Cannot create mask via median_otsu.")

    _, mask = median_otsu(data, vol_idx=b0_idx, numpass=4, autocrop=False)
    save_nifti(str(out_mask_path), mask.astype(np.uint8), affine)
    return mask.astype(np.uint8)


def fit_dti(data: np.ndarray, bvals: np.ndarray, bvecs: np.ndarray, mask: np.ndarray,
            b0_thr: float = 50.0, dti_bmax: float = 1200.0):
    keep = (bvals <= dti_bmax) | (bvals < b0_thr)
    data_dti = data[..., keep]
    bvals_dti = bvals[keep]
    bvecs_dti = bvecs[keep]

    gtab = gradient_table(bvals_dti, bvecs_dti, b0_threshold=b0_thr)
    tenmodel = TensorModel(gtab)
    tenfit = tenmodel.fit(data_dti, mask=mask.astype(bool))
    return tenfit


def save_dti_metrics(tenfit, affine: np.ndarray, mask: np.ndarray, outdir: Path):
    evals = np.clip(tenfit.evals, 0, None)  # guard against tiny negative eigenvalues
    fa = fractional_anisotropy(evals)
    fa[~np.isfinite(fa)] = 0.0
    fa[mask == 0] = 0.0

    md = tenfit.md
    ad = tenfit.ad
    rd = tenfit.rd

    save_nifti(str(outdir / "FA.nii.gz"), fa.astype(np.float32), affine)
    save_nifti(str(outdir / "MD.nii.gz"), md.astype(np.float32), affine)
    save_nifti(str(outdir / "AD.nii.gz"), ad.astype(np.float32), affine)
    save_nifti(str(outdir / "RD.nii.gz"), rd.astype(np.float32), affine)


def roi_stats(metric_path: Path, roi_path: Path, out_csv: Path, min_vox: int = 10):
    metric = nib.load(str(metric_path)).get_fdata()
    roi = nib.load(str(roi_path)).get_fdata().astype(int)

    labels = np.unique(roi)
    labels = labels[labels != 0]

    rows = []
    for lab in labels:
        m = (roi == lab)
        vals = metric[m]
        vals = vals[np.isfinite(vals)]
        if vals.size < min_vox:
            continue
        rows.append({
            "label": int(lab),
            "n_vox": int(vals.size),
            "mean": float(vals.mean()),
            "median": float(np.median(vals)),
            "std": float(vals.std(ddof=1)) if vals.size > 1 else 0.0,
            "p05": float(np.percentile(vals, 5)),
            "p95": float(np.percentile(vals, 95)),
        })

    pd.DataFrame(rows).sort_values("label").to_csv(out_csv, index=False)


def main():
    p = argparse.ArgumentParser("NeuroClaw DIPY DTI pipeline")
    p.add_argument("--dwi", required=True, help="DWI 4D NIfTI (.nii/.nii.gz)")
    p.add_argument("--bval", required=True, help="bvals file")
    p.add_argument("--bvec", required=True, help="bvecs file")
    p.add_argument("--outdir", default="dwi_output", help="Output directory")
    p.add_argument("--b0-thr", type=float, default=50.0, help="b0 threshold (default: 50)")
    p.add_argument("--dti-bmax", type=float, default=1200.0, help="DTI fit uses b<=this (default: 1200)")
    p.add_argument("--mask", default=None, help="Optional brain mask NIfTI (same space as DWI)")
    p.add_argument("--roi", default=None, help="Optional ROI/atlas label NIfTI (same space as FA)")
    p.add_argument("--roi-metrics", default="FA,MD,AD,RD",
                   help="Comma-separated subset of FA,MD,AD,RD (default: FA,MD,AD,RD)")
    p.add_argument("--min-roi-vox", type=int, default=10, help="Minimum voxels per label (default: 10)")
    args = p.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    data, affine, bvals, bvecs = load_dwi(args.dwi, args.bval, args.bvec)

    if args.mask:
        mask = read_mask(args.mask)
        save_nifti(str(outdir / "brain_mask.nii.gz"), mask.astype(np.uint8), affine)
    else:
        mask = make_mask(data, bvals, affine, outdir / "brain_mask.nii.gz", b0_thr=args.b0_thr)

    tenfit = fit_dti(
        data=data, bvals=bvals, bvecs=bvecs, mask=mask,
        b0_thr=args.b0_thr, dti_bmax=args.dti_bmax
    )
    save_dti_metrics(tenfit, affine, mask, outdir)

    if args.roi:
        metrics = [m.strip().upper() for m in args.roi_metrics.split(",") if m.strip()]
        metric_map = {
            "FA": outdir / "FA.nii.gz",
            "MD": outdir / "MD.nii.gz",
            "AD": outdir / "AD.nii.gz",
            "RD": outdir / "RD.nii.gz",
        }
        for m in metrics:
            if m not in metric_map:
                raise ValueError(f"Unknown metric for ROI stats: {m}")
            roi_stats(
                metric_path=metric_map[m],
                roi_path=Path(args.roi),
                out_csv=outdir / f"roi_stats_{m}.csv",
                min_vox=args.min_roi_vox
            )

    print("✅ DIPY DTI pipeline finished")
    print(f"Outputs saved in: {outdir.resolve()}")


if __name__ == "__main__":
    main()
```

---

## Example execution (must be routed via `claw-shell`)
```bash
conda run -n neuroclaw-dipy python skills/dipy-tool/dipy_pipeline.py \
  --dwi /data/sub-001_dwi.nii.gz \
  --bval /data/sub-001_dwi.bval \
  --bvec /data/sub-001_dwi.bvec \
  --outdir dwi_output/sub-001 \
  --dti-bmax 1200 \
  --roi /data/JHU_labels_in_dwi_space.nii.gz
```

---

## Important Notes & Limitations
- **Preprocessing matters**: FA/MD are highly sensitive to motion/eddy/susceptibility distortions. Best practice is to run **topup/eddy** first (e.g., via `fsl-tool` or HCP diffusion pipeline) and use the **rotated bvecs** output by eddy.
- **DTI vs multi-shell**: DTI fitting is most stable on low b-values (commonly b≤1000–1200). Higher-order models (DKI/NODDI) require separate implementations (extend this tool if needed).
- **ROI alignment**: ROI/atlas labels must be in the *same voxel space* as the DWI-derived metrics. Registration/warping is handled by other tools (e.g., FSL/ANTs/HCP pipelines).
- **Numerical stability**: small negative eigenvalues can occur; this pipeline clips them to zero before FA computation.

---

## Complementary / Related Skills
- `dependency-planner` + `conda-env-manager` → install/manage `neuroclaw-dipy`

---

## Reference & Source
- DIPY documentation: https://dipy.org/documentation/latest/
- DIPY DTI reconstruction examples (tensor fitting + FA/MD/AD/RD)
- Aligned with NeuroClaw base/tool skill pattern (`mne-eeg-tool`, etc.)

Created At: 2026-03-26 00:40 HKT
Last Updated At: 2026-03-26 00:43 HKT
Author: chengwang96