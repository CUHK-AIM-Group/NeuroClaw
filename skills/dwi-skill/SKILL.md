---
name: dwi-skill
description: "Use this skill whenever the user wants to preprocess diffusion MRI / DWI data, compute diffusion metrics (FA/MD/AD/RD, etc.), extract ROI-wise diffusion features, or run tractography/connectome-related workflows. Triggers include: 'DWI', 'DTI', 'diffusion MRI', 'FA', 'MD', 'AD', 'RD', 'eddy', 'topup', 'QSIPrep', 'tractography', 'connectome', 'TBSS', 'white matter microstructure'. This is the NeuroClaw modality-layer interface: it plans WHAT to do and delegates execution to tool skills."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# DWI Skill (Modality Layer)

## Overview
`dwi-skill` is the NeuroClaw **modality-layer** interface skill responsible for diffusion MRI (DWI/DTI) preprocessing and feature extraction.

It strictly follows NeuroClaw hierarchical design principles:
- This skill defines **WHAT needs to be done** and **which tool skill to delegate to**.
- It contains **no implementation code** and **no concrete shell commands**.
- All concrete execution is delegated to tool skills and routed through `claw-shell`.

**Core workflow (never bypassed):**
1. Identify input type (DICOM / NIfTI / BIDS), single-shell vs multi-shell, reverse phase-encoded b0/fieldmaps availability.
2. Generate a **numbered execution plan** (steps, tools, outputs, runtime, risks).
3. Present the plan and wait for explicit user confirmation (“YES” / “execute” / “proceed”).
4. On confirmation, delegate each step to the relevant tool skill via `claw-shell`.
5. Save outputs into `dwi_output/`.

**Research use only.**

---

## Quick Reference (Common DWI Tasks → Delegation Map)

| Task | What needs to be done (high level) | Delegate to which skill | Expected outputs |
|---|---|---|---|
| DICOM → NIfTI | Convert DICOM series to NIfTI + bval/bvec (+json) | `dcm2nii` | `*.nii.gz`, `*.bval`, `*.bvec`, `*.json` |
| Organize to BIDS | Build BIDS-compliant diffusion dataset | `bids-organizer` | `bids/sub-*/dwi/...` |
| **Best-practice DWI preprocessing (recommended)** | Run containerized BIDS-App with robust workflows + QC | **`qsiprep-tool`** | `derivatives/qsiprep/.../*preproc_dwi.nii.gz`, QC HTML |
| Manual FSL preprocessing | topup/eddy pipeline (expert/manual control) | `fsl-tool` | corrected DWI, rotated bvecs, QC (`eddy_quad`) |
| HCP-grade diffusion preprocessing | HCP diffusion pipeline end-to-end | `hcppipeline-tool` | HCP-style diffusion outputs |
| Tensor metrics | Fit DTI and compute FA/MD/AD/RD | `dipy-tool` (or `fsl-tool` dtifit) | `FA/MD/AD/RD.nii.gz` |
| ROI-wise diffusion features | Extract ROI stats from FA/MD/etc maps | `nilearn-tool` (or `fsl-tool`) | `roi_stats_*.csv` |
| Tractography / connectome (if requested) | Streamlines + ROI×ROI connectivity (tool-dependent) | `hcppipeline-tool` / `fsl-tool` / (future MRtrix tool) | tractograms, connectome matrices |

---

## Recommended Default Strategy (Decision Logic)
- If input is **BIDS** (or can be organized into BIDS) and the user wants robust preprocessing + QC:
  → **delegate preprocessing to `qsiprep-tool`**.
- If the user explicitly requests **FSL eddy/topup** steps or needs low-level control:
  → delegate to `fsl-tool`.
- If the user requests **HCP-style** diffusion preprocessing or needs HCP-compatible derivatives:
  → delegate to `hcppipeline-tool`.
- After preprocessing, for quantitative features:
  - DTI metrics → `dipy-tool`
  - ROI/atlas feature tables from scalar maps → `nilearn-tool`

---

## Standard Output Layout (Recommended)
All outputs must be written under `./dwi_output/`:
- `dwi_output/bids/`        (optional local BIDS copy/staging)
- `dwi_output/preproc/`     (QSIPrep/FSL/HCP outputs + QC pointers)
- `dwi_output/dti/`         (FA/MD/AD/RD maps)
- `dwi_output/roi/`         (ROI summary CSVs)
- `dwi_output/logs/`        (claw-shell logs/tags)

---

## Important Notes & Limitations
- **Preprocessing is critical**: diffusion metrics are highly sensitive to motion, eddy currents, and susceptibility distortions.
- **bvec correctness**: after motion/eddy correction you must use **rotated bvecs** (QSIPrep/FSL handle this; downstream fitting must use the corrected bvecs).
- **Reverse PE b0 (AP/PA)** or fieldmaps strongly improve distortion correction; without them, correction may be limited.
- Single-shell vs multi-shell impacts feasible models (DTI vs higher-order microstructure).
- This skill is for research feature extraction; not a clinical workflow.

---

## When to Call This Skill
- The user requests DWI/DTI preprocessing (especially QSIPrep / eddy/topup) or diffusion feature extraction (FA/MD/etc).
- The user wants ROI-based diffusion statistics, tractography, or connectome outputs.

---

## Complementary / Related Skills
- `qsiprep-tool` → recommended BIDS-App diffusion preprocessing + QC reports
- `dipy-tool` → tensor metrics (FA/MD/AD/RD) + diffusion scalar map handling
- `nilearn-tool` → ROI/atlas feature extraction from diffusion scalar maps (NIfTI)
- `fsl-tool` → topup/eddy, dtifit, bedpostx/probtrackx, diffusion utilities
- `hcppipeline-tool` → HCP diffusion preprocessing alternative
- `bids-organizer` → create/validate BIDS dataset
- `dependency-planner` + `conda-env-manager` → installation/environment management
- `docker-env-manager` → used when QSIPrep runs via Docker and container ops need planning

---

## Reference & Source
Aligned with NeuroClaw modality-skill pattern (see `fmri-skill`, `eeg-skill`).
Tool stack: QSIPrep (BIDS-App), FSL (eddy/topup), HCP pipelines, DIPY (Python diffusion modeling), Nilearn (ROI feature extraction on scalar maps).

Created At: 2026-03-26 1:01 HKT
Last Updated At: 2026-03-26 1:01 HKT
Author: chengwang96