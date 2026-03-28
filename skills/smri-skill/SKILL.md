---
name: smri-skill
description: "Use this skill whenever the user wants to process structural MRI (sMRI) such as T1w/T2w/FLAIR for brain extraction, bias correction, tissue segmentation (GM/WM/CSF), registration to MNI, cortical/subcortical parcellation, cortical thickness/volumetry (FreeSurfer), HCP-style structural preprocessing, WMH lesion segmentation (FLAIR+T1), ROI-wise feature extraction, or converting results back to DICOM. This is the NeuroClaw modality-layer interface: it plans WHAT to do and delegates execution to tool skills."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# sMRI Skill (Modality Layer)

## Overview
`smri-skill` is the NeuroClaw **modality-layer** interface skill responsible for **structural MRI** processing (T1w/T2w/FLAIR) and feature extraction.

It strictly follows NeuroClaw hierarchical design principles:
- This skill describes **WHAT needs to be done** and **which tool skill to delegate to**.
- It contains **no implementation code** and **no direct shell commands**.
- All concrete execution is delegated to tool skills and routed through `claw-shell`.

**Core workflow (never bypassed):**
1. Identify input type (DICOM / NIfTI / BIDS), modalities available (T1w only vs T1w+T2w vs T1w+FLAIR).
2. Generate a **numbered execution plan** (steps, tools, outputs, runtime, risks).
3. Present the plan and wait for explicit user confirmation (“YES” / “execute” / “proceed”).
4. On confirmation, delegate each step via `claw-shell`.
5. Save outputs into a clean folder structure (`smri_output/`).

**Research use only.**

---

## Quick Reference (Common sMRI Tasks → Delegation Map)

| Task | What needs to be done (high level) | Delegate to which skill | Expected outputs |
|---|---|---|---|
| DICOM → NIfTI | Convert DICOM series to NIfTI (+ JSON) | `dcm2nii` | `*_T1w.nii.gz`, `*_T2w.nii.gz`, `*_FLAIR.nii.gz`, `*.json` |
| Organize to BIDS | Create valid BIDS layout (anat/) | `bids-organizer` | `bids/sub-*/anat/sub-*_T1w.nii.gz` etc. |
| Fast structural preprocessing | Brain extraction, bias correction, tissue segmentation, MNI registration | `fsl-tool` (`fsl_anat`, BET/FAST/FLIRT/FNIRT) | brain mask, tissue maps, transforms, QC |
| Surface-based morphometry | Cortical surfaces, parcellation, thickness, aseg/aparc stats | `freesurfer-tool` | FreeSurfer subject dir, stats tables |
| HCP-grade structural pipeline | PreFreeSurfer → FreeSurfer → PostFreeSurfer | `hcppipeline-tool` | HCP-style derivatives, surfaces, QC |
| BIDS anatomical derivatives (standardized) | Run BIDS-App anatomical-only workflow | `fmriprep-tool` (`--anat-only`) | BIDS derivatives + QC report |
| WMH lesion segmentation | Segment WMH from FLAIR+T1 | `wmh-segmentation` (+ `docker-env-manager` if Docker ops needed) | WMH mask NIfTI + run log |
| ROI-wise feature extraction | Extract ROI stats from derived maps (GM prob, WMH mask, thickness maps in NIfTI, etc.) | `nilearn-tool` (or `fsl-tool` `fslstats`) | `roi_stats_*.csv` |
| Export results to DICOM | Convert final NIfTI outputs back to DICOM series | `nii2dcm` | DICOM series for PACS/viewers |

---

## Recommended Strategy (Decision Logic)
- If the goal is **quick brain extraction + tissue segmentation + MNI alignment** (fast baseline):
  - Prefer `fsl-tool` (`fsl_anat`).
- If the goal is **cortical thickness / surface parcellation / aseg-aparc volumetry**:
  - Prefer `freesurfer-tool` (`recon-all`).
- If the goal is **highest-quality, HCP-style surfaces and multimodal alignment**:
  - Prefer `hcppipeline-tool` (structural stages).
- If the dataset is already **BIDS** and you want **standardized derivatives + QC** (and future fMRI integration):
  - Prefer `fmriprep-tool --anat-only` (or full fMRIPrep if fMRI exists).
- If the goal is **WMH lesion segmentation** (vascular burden, aging, MS-like WM lesions):
  - Use `wmh-segmentation` (Docker-based); ensure Docker readiness via `docker-env-manager` if needed.
- If the goal is **ROI-level tables** from any NIfTI scalar map:
  - Use `nilearn-tool` to generate reproducible CSV feature tables.

---

## Standard Output Layout (Recommended)
All outputs must be written under `./smri_output/`:
- `smri_output/nifti/`        (converted inputs if needed)
- `smri_output/bids/`         (optional staging BIDS)
- `smri_output/fsl_anat/`     (FSL structural outputs)
- `smri_output/freesurfer/`   (FreeSurfer SUBJECTS_DIR or symlink)
- `smri_output/hcp/`          (HCP structural outputs)
- `smri_output/fmriprep/`     (fMRIPrep derivatives/QC pointers)
- `smri_output/wmh/`          (WMH masks + logs)
- `smri_output/roi/`          (ROI feature CSVs)
- `smri_output/logs/`         (claw-shell log tags / pointers)

---

## Safety / Execution Rules (NeuroClaw)
- **No execution without explicit user confirmation** of the full numbered plan.
- All execution must be routed through `claw-shell`.
- If a required dependency is missing, delegate installation planning to `dependency-planner`.
- If Docker is required (e.g., WMH segmentation containers), coordinate via `docker-env-manager` (plan → confirm → run).

---

## Important Notes & Limitations
- Structural pipelines can be long-running (especially FreeSurfer/HCP). Always provide runtime + disk estimates in the plan.
- FreeSurfer requires a valid license; fMRIPrep/HCP may require it depending on configuration.
- ROI extraction requires atlas alignment (same space/grid as the target map). Registration is handled by `fsl-tool`, `fmriprep-tool`, or `hcppipeline-tool`.
- This skill is for research workflows; not for clinical decision-making.

---

## When to Call This Skill
- Any request involving: T1w/T2w/FLAIR preprocessing, brain extraction, tissue segmentation, MNI registration, cortical thickness, FreeSurfer recon-all, HCP structural pipeline, WMH segmentation, or ROI-wise structural features.

---

## Complementary / Related Skills
- `dcm2nii` → DICOM → NIfTI
- `fsl-tool` → fsl_anat / BET / FAST / FIRST / registration utilities
- `freesurfer-tool` → cortical & subcortical morphometry + thickness/parcellation
- `hcppipeline-tool` → HCP-style structural pipeline
- `fmriprep-tool` → standardized BIDS-App anatomical-only derivatives + QC
- `wmh-segmentation` → WMH lesion mask from FLAIR+T1 (Docker)
- `docker-env-manager` → safe Docker operations (when needed)
- `nilearn-tool` → ROI feature extraction from structural-derived NIfTI maps
- `nii2dcm` → export final NIfTI results back to DICOM
- `dependency-planner` + `conda-env-manager` → installation/environment management
- `claw-shell` → mandatory safe execution layer

---

## Reference & Source
Aligned with NeuroClaw modality-skill pattern (see `fmri-skill`, `dwi-skill`, `eeg-skill`).
Common sMRI toolchain: FSL (fast structural utilities), FreeSurfer (surface morphometry), HCP pipelines (HCP-grade structural processing), fMRIPrep (BIDS anatomical derivatives), Nilearn (ROI features on NIfTI maps), MARS-WMH (WMH segmentation via Docker).

Created At: 2026-03-26 1:09 HKT
Last Updated At: 2026-03-26 1:09 HKT
Author: chengwang96