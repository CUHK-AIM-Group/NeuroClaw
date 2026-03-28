---
name: adni-skill
description: "Use this skill whenever the user wants an end-to-end workflow for ADNI data (fMRI + T1), including BIDS preparation, fMRIPrep preprocessing, and DK68 ROI pipeline. This is the NeuroClaw dataset-orchestration layer for ADNI."
license: MIT License (NeuroClaw custom skill - freely modifiable within the project)
---

# ADNI Skill (Dataset-Orchestration Layer)

## Overview
`adni-skill` is the NeuroClaw orchestration skill for ADNI subject-level fMRI + T1 workflows.

It coordinates a fixed two-stage pipeline:
1. Prepare ADNI data into BIDS and run fMRIPrep.
2. Run DK68 ROI extraction with QC.

This skill follows NeuroClaw hierarchy:
- Defines **WHAT to do**, not low-level implementation details.
- Does **not** execute direct shell commands itself.
- Delegates all execution via `claw-shell` to tool skills.

**Research use only.**

---

## Core Workflow (Never Bypassed)
1. Confirm subject ID and modalities (T1 + fMRI).
2. Generate a numbered plan with tools, outputs, runtime, storage, and risks.
3. Wait for explicit confirmation (`YES` / `execute` / `proceed`).
4. On confirmation, prepare BIDS staging and run fMRIPrep.
5. After fMRIPrep success, run DK68 ROI pipeline with QC.
6. Save outputs into an ADNI-centered structure under `adni_output/`.

---

## Input Layout (Example)

Subject `130_S_0969` (fMRI + T1):

```
nifti/130_S_0969/T1/I10308298_..._3.nii.gz
nifti/130_S_0969/T1/I10308298_..._3.json
nifti/130_S_0969/fMRI/I10308297_..._8.nii.gz
nifti/130_S_0969/fMRI/I10308297_..._8.json
```

---

## BIDS Preparation (Stage A-C)

### Stage A: Prepare BIDS root metadata
Create `dataset_description.json` under the BIDS root:

```json
{
  "Name": "ADNI rsfMRI T1 subset",
  "BIDSVersion": "1.8.0",
  "DatasetType": "raw"
}
```

### Stage B: Create BIDS directories

```bash
mkdir -p bids/sub-130S0969/ses-M00/anat
mkdir -p bids/sub-130S0969/ses-M00/func
```

### Stage C: Copy and rename NIfTI + JSON

T1w:

```bash
cp "nifti/130_S_0969/T1/"*.nii.gz \
  "bids/sub-130S0969/ses-M00/anat/sub-130S0969_ses-M00_T1w.nii.gz"

cp "nifti/130_S_0969/T1/"*.json \
  "bids/sub-130S0969/ses-M00/anat/sub-130S0969_ses-M00_T1w.json"
```

fMRI:

```bash
cp "nifti/130_S_0969/fMRI/"*.nii.gz \
  "bids/sub-130S0969/ses-M00/func/sub-130S0969_ses-M00_task-rest_bold.nii.gz"

cp "nifti/130_S_0969/fMRI/"*.json \
  "bids/sub-130S0969/ses-M00/func/sub-130S0969_ses-M00_task-rest_bold.json"
```

---

## fMRIPrep Stage (Stage D)

### Typical Docker run

```bash
docker run --rm -it \
  -v /path/to/ADNI_Datasets/bids:/data:ro \
  -v /path/to/ADNI_Datasets/fmriprep_out:/out \
  -v /path/to/ADNI_Datasets/fmriprep_work:/work \
  -v /path/to/freesurfer:/fs \
  nipreps/fmriprep:23.2.1 \
  /data /out participant \
  --participant-label 130S0969 \
  --fs-license-file /fs/license.txt \
  --output-spaces T1w \
  --work-dir /work \
  --clean-workdir
```

fMRIPrep handles:
- BIDS ingestion and validation
- T1/fMRI pairing checks
- FreeSurfer surface reconstruction
- fMRI preprocessing (slice timing, motion correction)
- BOLD-to-T1 registration
- T1w-space outputs

---

## DK68 Pipeline Stage

Pipeline behavior:
1. TR auto-read from `desc-preproc_bold.json` and used for band-pass timing
2. Drop initial TRs (default `drop-first-trs = 4`, configurable)
3. Confounds auto-select: `trans_*`, `rot_*`, `white_matter`, `csf`, `framewise_displacement`
   - Fallback: motion-only columns if missing
4. DK68 ROI order fixed: left hemisphere then right hemisphere
5. Resample DK labels to BOLD space with nearest-neighbor
6. ROI-level regression of confounds (motion/WM/CSF)
7. ROI-level band-pass filtering: 0.01 - 0.08 Hz
8. ROI-level z-score normalization over time
   - $z(t) = (x(t) - mu) / sigma$
9. QC output: mean FD / max FD (after TR drop), optional DVARS

Run command:

```bash
python run_dk68_pipeline_qc.py \
  --base /path/to/ADNI_Datasets \
  --sub 130S0969 \
  --ses M00 \
  --drop-first-trs 4
```

---

## Recommended Output Layout
All assets should be organized under `./adni_output/`:
- `adni_output/bids/` (staged BIDS data)
- `adni_output/fmriprep/` (fMRIPrep derivatives)
- `adni_output/dk68/` (ROI CSVs)
- `adni_output/qc/` (QC metrics)
- `adni_output/logs/`

---

## Safety and Execution Policy
- No execution before explicit plan confirmation.
- All execution must be routed via `claw-shell`.
- Missing dependencies must be resolved by `dependency-planner` before running.

---

## Important Notes and Limitations
- ADNI subject naming must be normalized (e.g., `130_S_0969` -> `130S0969`).
- fMRIPrep requires FreeSurfer license and sufficient disk space.
- DK68 pipeline assumes `aparc+aseg.mgz` is available in fMRIPrep outputs.

---

## When to Call This Skill
- User asks for ADNI end-to-end processing (fMRI + T1).
- User needs BIDS staging + fMRIPrep + DK68 ROI outputs.

---

## Complementary / Related Skills
- `bids-organizer`
- `fmriprep-tool`
- `freesurfer-tool`
- `fmri-skill`
- `smri-skill`
- `dependency-planner`
- `conda-env-manager`
- `claw-shell`

---

## Reference
- fMRIPrep: https://fmriprep.org/
- BIDS spec: https://bids.neuroimaging.io/

Created At: 2026-03-28 20:38 HKT
Last Updated At: 2026-03-28 20:38 HKT
Author: chengwang96