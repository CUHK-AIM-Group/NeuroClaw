---
name: qsiprep-tool
description: "Use this skill whenever the user wants to run QSIPrep (BIDS App) for diffusion MRI (DWI) preprocessing with best-practice workflows (topup/eddy, denoising/unringing options, susceptibility/motion correction, coregistration/normalization, QC reports) on BIDS datasets. This skill is the NeuroClaw interface-layer wrapper for QSIPrep: it checks installation (Docker/Singularity/conda), generates an execution plan with exact commands and resource estimates, waits for explicit confirmation, then routes all execution through claw-shell."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# QSIPrep Tool (Interface Layer)

## Overview
QSIPrep is a BIDS-App pipeline for **diffusion MRI (DWI) preprocessing** that emphasizes:
- Robust distortion/motion/eddy-current correction
- Interoperable derivatives for downstream modeling (DTI/DKI/CSD, tractography, connectome, etc.)
- Strong QC reporting (HTML)

This skill is the **NeuroClaw interface-layer wrapper** for QSIPrep and strictly follows the NeuroClaw safety pattern:

1. Check whether QSIPrep is available (preferred: Docker/Singularity image; alternative: conda).
2. If missing → invoke `dependency-planner` to produce an installation plan.
3. Verify inputs (must be BIDS-compliant; detect DWI + fieldmaps/reverse-PE b0 if present).
4. Generate a clear numbered plan with **exact commands**, runtime/resource estimates, and risks.
5. Wait for explicit user confirmation (“YES” / “execute” / “proceed”).
6. On confirmation → delegate all commands to `claw-shell`.
7. Summarize outputs (derivatives paths + QC report location) and suggest next steps.

**Research use only.**

---

## What QSIPrep Typically Does (High-Level)
- Validates BIDS layout (or skips if requested)
- Creates brain mask(s)
- Denoising (optional), Gibbs unringing (optional)
- Susceptibility distortion correction (e.g., reverse phase-encoded b0 via topup-style approach)
- Eddy-current + motion correction (FSL eddy family behavior within containerized workflow)
- Gradient/bvec handling (rotation after motion correction)
- Coregistration to anatomical (and optionally standard space outputs)
- Produces derivatives + QC HTML reports

---

## Quick Reference

| Task | Recommended Approach | Typical Output |
|---|---|---|
| Standard DWI preprocessing | QSIPrep BIDS-App `participant` | `derivatives/qsiprep/sub-*/dwi/*preproc_dwi.nii.gz` |
| Multi-subject run | `--participant-label sub-001 sub-002 ...` | per-subject derivatives |
| HPC / cluster | Singularity `.sif` execution | same derivatives |
| QC | Default QSIPrep reports | `derivatives/qsiprep/sub-*/figures/*.html` |

Typical runtime (very data-dependent): **~0.5–4+ hours per subject**.

---

## Installation (Handled by `dependency-planner`)
Preferred: **Docker** (workstations) or **Singularity/Apptainer** (HPC).

Ask `dependency-planner` for one of:
- “Install Docker and pull latest QSIPrep image”
- “Install Apptainer/Singularity and pull QSIPrep .sif”
- “Install QSIPrep via conda (not recommended unless container is unavailable)”

Verification examples:
```bash
docker --version
docker image ls | grep -i qsiprep
# or
apptainer --version
apptainer exec qsiprep.sif qsiprep --version
```

**FreeSurfer license**: QSIPrep often requires a FreeSurfer license file.
- Usually passed with: `--fs-license-file /path/to/license.txt`
- This skill will request it if not provided.

---

## Common Command Templates (Executed via `claw-shell`)

### A) Docker (Recommended on workstations)
```bash
# Inputs:
BIDS_DIR=/data/bids
OUT_DIR=/data/derivatives
WORK_DIR=/data/work/qsiprep
FS_LICENSE=/data/license.txt

mkdir -p "$OUT_DIR" "$WORK_DIR"

docker run --rm -t \
  -v "$BIDS_DIR":/data:ro \
  -v "$OUT_DIR":/out \
  -v "$WORK_DIR":/work \
  -v "$FS_LICENSE":/opt/freesurfer/license.txt:ro \
  pennbbl/qsiprep:latest \
  /data /out participant \
  --participant-label sub-001 \
  --work-dir /work \
  --fs-license-file /opt/freesurfer/license.txt \
  --nthreads 16 --omp-nthreads 8 --mem-mb 64000
```

### B) Singularity / Apptainer (Recommended on HPC)
```bash
BIDS_DIR=/data/bids
OUT_DIR=/data/derivatives
WORK_DIR=/data/work/qsiprep
FS_LICENSE=/data/license.txt
IMG=/images/qsiprep.sif

mkdir -p "$OUT_DIR" "$WORK_DIR"

apptainer run --cleanenv \
  -B "$BIDS_DIR":/data:ro \
  -B "$OUT_DIR":/out \
  -B "$WORK_DIR":/work \
  -B "$FS_LICENSE":/opt/freesurfer/license.txt:ro \
  "$IMG" \
  /data /out participant \
  --participant-label sub-001 \
  --work-dir /work \
  --fs-license-file /opt/freesurfer/license.txt \
  --nthreads 16 --omp-nthreads 8 --mem-mb 64000
```

> Notes:
> - Image name (`pennbbl/qsiprep:latest`) should be verified by `dependency-planner` against the latest official docs/releases.
> - Some flags vary by QSIPrep version; this skill will always generate commands after checking installed version.

---

## NeuroClaw recommended wrapper script (Reference): `qsiprep_wrapper.py`

> This wrapper only *builds and prints* a plan; actual execution must be routed through `claw-shell` by the calling skill.

```python
# qsiprep_wrapper.py (reference template)
import argparse
from pathlib import Path
from datetime import datetime

def build_qsiprep_cmd(engine, bids_dir, out_dir, work_dir, participant_labels, fs_license, img):
    labels = " ".join(participant_labels) if participant_labels else ""
    if engine == "docker":
        cmd = f"""
mkdir -p "{out_dir}" "{work_dir}"
docker run --rm -t \
  -v "{bids_dir}":/data:ro \
  -v "{out_dir}":/out \
  -v "{work_dir}":/work \
  -v "{fs_license}":/opt/freesurfer/license.txt:ro \
  {img} \
  /data /out participant \
  {"--participant-label " + labels if labels else ""} \
  --work-dir /work \
  --fs-license-file /opt/freesurfer/license.txt
""".strip()
    else:
        cmd = f"""
mkdir -p "{out_dir}" "{work_dir}"
apptainer run --cleanenv \
  -B "{bids_dir}":/data:ro \
  -B "{out_dir}":/out \
  -B "{work_dir}":/work \
  -B "{fs_license}":/opt/freesurfer/license.txt:ro \
  "{img}" \
  /data /out participant \
  {"--participant-label " + labels if labels else ""} \
  --work-dir /work \
  --fs-license-file /opt/freesurfer/license.txt
""".strip()
    return cmd

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--engine", choices=["docker", "apptainer"], required=True)
    p.add_argument("--bids-dir", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--work-dir", required=True)
    p.add_argument("--fs-license", required=True)
    p.add_argument("--img", required=True, help="Docker image (e.g., pennbbl/qsiprep:latest) or .sif path")
    p.add_argument("--participants", nargs="*", default=None)
    args = p.parse_args()

    cmd = build_qsiprep_cmd(
        engine=args.engine,
        bids_dir=Path(args.bids_dir).resolve(),
        out_dir=Path(args.out_dir).resolve(),
        work_dir=Path(args.work_dir).resolve(),
        participant_labels=args.participants,
        fs_license=Path(args.fs_license).resolve(),
        img=args.img
    )

    tag = f"qsiprep_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print("Execution plan (delegate to claw-shell):")
    print(cmd)
    print("\nLog tag suggestion:", tag)
```

---

## Important Notes & Limitations
- **BIDS input is strongly recommended**. If you only have raw NIfTI/DICOM, use `bids-organizer` (and `dcm2nii`) first.
- QSIPrep benefits a lot from having **reverse phase-encoded b0 images (AP/PA)** or valid fieldmaps; otherwise distortion correction may be limited.
- Ensure adequate resources:
  - RAM commonly **16–64 GB**
  - Disk: work directory can be large (tens of GB)
- All execution must go through `claw-shell` due to long runtime and logging requirements.
- This skill does not replace downstream modeling (DTI/CSD/NODDI). After preprocessing, delegate to:
  - `dipy-tool` for Python-based metrics/ROI features
  - MRtrix/FSL-based workflows (future tool skills) for tractography/connectomes

---

## When to Call This Skill
- User requests “run QSIPrep”, “preprocess DWI with QSIPrep”, “BIDS diffusion preprocessing”, “topup/eddy style pipeline with QC reports”.
- Before any quantitative diffusion features (FA/MD/tractometry/connectome) are extracted.

---

## Complementary / Related Skills
- `bids-organizer` → make dataset BIDS-compliant
- `dcm2nii` → DICOM → NIfTI (with bval/bvec export)
- `fsl-tool` → alternative / additional diffusion preprocessing and registration
- `hcppipeline-tool` → HCP-style diffusion preprocessing alternative
- `dipy-tool` → post-QSIPrep tensor metrics + ROI feature extraction in Python
- `dependency-planner` → install Docker/Apptainer + QSIPrep image
- `docker-env-manager` → safe Docker operations (pull/run/prune) when needed
- `claw-shell` → mandatory safe execution layer

---

## Reference & Source
- QSIPrep documentation and BIDS App usage (official docs; version-dependent)
- NeuroClaw interface-layer pattern aligned with `fmriprep-tool` and `hcppipeline-tool`

Created At: 2026-03-26 00:45 HKT
Last Updated At: 2026-03-26 00:49 HKT
Author: chengwang96