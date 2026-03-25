---
name: fmriprep-tool
description: "Use this skill whenever the user wants to perform standardized preprocessing of functional MRI (fMRI) and anatomical MRI data using fMRIPrep. Triggers include: 'fmriprep', 'fMRIPrep', 'fMRI preprocessing', 'BIDS fMRI', 'run fmriprep', 'preprocess bold', 'BOLD preprocessing', 'anatomical preprocessing', or any request involving BIDS-organized fMRI datasets."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# fMRIPrep Tool

## Overview

fMRIPrep is a robust, standardized preprocessing pipeline for BIDS-compliant functional and anatomical MRI data. It performs best-practice steps including anatomical segmentation, functional motion correction, susceptibility distortion correction, coregistration, normalization to standard space, and generates comprehensive QC reports.

This skill serves as the **NeuroClaw interface-layer wrapper** for fMRIPrep and strictly follows the hierarchical design:

1. Check whether fMRIPrep and its dependencies (Docker or Singularity) are installed.
2. If missing → invoke `dependency-planner` to generate a safe installation plan.
3. Detect input BIDS dataset structure and confirm output directory.
4. Generate a clear, numbered execution plan with exact command, flags, estimated runtime, and risks.
5. Present the plan and wait for explicit user confirmation (“YES” / “execute” / “proceed”).
6. On confirmation → delegate the entire pipeline execution to `claw-shell`.
7. After completion, summarize outputs, highlight QC reports, and suggest next steps (e.g., feeding results into analysis or paper-writing).

**Research use only.**

## Quick Reference

| Task                          | Recommended Command / Approach                                      | Typical Runtime (per subject) |
|-------------------------------|---------------------------------------------------------------------|-------------------------------|
| Full fMRIPrep pipeline        | `fmriprep bids_dir output_dir participant --fs-license-file license.txt` | 2–8 hours                    |
| Anatomical only               | `--anat-only`                                                       | 30–90 min                    |
| Functional only (after anat)  | `--bold-only`                                                       | 1–4 hours                    |
| Use FreeSurfer recon-all      | `--fs-subjects-dir /path/to/fs`                                     | +2–6 hours                   |
| Skip susceptibility distortion| `--ignore fieldmaps`                                                | Reduces time                 |
| Low memory mode               | `--mem-mb 8000 --nthreads 4`                                        | For limited resources        |
| Generate detailed QC reports  | Default behavior (outputs in `sub-*/figures/` and `reports/`)       | Included                     |

## Common Shell Command Examples

```bash
# Standard full pipeline (most common)
fmriprep \
  /data/bids \
  /data/fmriprep_output \
  participant \
  --participant-label sub-001 sub-002 \
  --fs-license-file /home/cwang/clawd/license.txt \
  --nthreads 8 \
  --mem-mb 16000 \
  --output-spaces MNI152NLin2009cAsym \
  --clean-workdir

# Anatomical preprocessing only
fmriprep /data/bids /data/fmriprep_output participant --anat-only

# Use Singularity instead of Docker (common on clusters)
singularity run --cleanenv \
  /path/to/fmriprep.simg \
  /data/bids /data/fmriprep_output participant \
  --fs-license-file /license.txt
```

## Installation (Handled by dependency-planner)

Use `dependency-planner` with one of the following requests:
- “Install latest fMRIPrep using Docker”
- “Install latest fMRIPrep using Singularity”
- “Install fMRIPrep via conda/mamba in neuroclaw-fmriprep environment”

After installation, verify with:
```bash
fmriprep --version
```

**Prerequisites**:
- Valid FreeSurfer license (`license.txt`)
- Docker or Singularity
- Sufficient disk space (~10–30 GB per subject) and RAM (≥16 GB recommended)

## NeuroClaw recommended wrapper script

```python
# fmriprep_wrapper.py (placed inside the skill folder for reference)
import subprocess
import argparse
from pathlib import Path

def run_fmriprep(bids_dir, output_dir, participant_labels=None, nthreads=8, mem_mb=16000):
    cmd = [
        "fmriprep",
        str(bids_dir),
        str(output_dir),
        "participant",
        "--fs-license-file", "/home/cwang/clawd/license.txt",
        "--nthreads", str(nthreads),
        "--mem-mb", str(mem_mb),
        "--output-spaces", "MNI152NLin2009cAsym",
        "--clean-workdir"
    ]
    
    if participant_labels:
        cmd.extend(["--participant-label"] + participant_labels)
    
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bids-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--subjects", nargs="+", default=None)
    args = parser.parse_args()
    
    run_fmriprep(args.bids_dir, args.output_dir, args.subjects)
```

## Important Notes & Limitations

- All actual fMRIPrep execution is routed through `claw-shell` (especially important for long-running pipelines).
- fMRIPrep is computationally intensive and disk-heavy. Always run with appropriate resource limits.
- A valid FreeSurfer license file is required if surface reconstruction is enabled.
- Outputs include preprocessed BOLD, anatomical derivatives, and rich HTML QC reports in `sub-*/figures/`.
- Work directory can become very large; use `--clean-workdir` when possible.

## When to Call This Skill

- User has a BIDS-organized dataset and wants standardized fMRI preprocessing.
- Before advanced analysis (GLM, connectivity, MVPA, etc.).
- After `dcm2nii` when converting raw scanner data to BIDS format.

## Complementary / Related Skills

- `dcm2nii` → convert DICOM to NIfTI and organize into BIDS
- `dependency-planner` → install fMRIPrep and dependencies
- `claw-shell` → safe execution of long-running pipeline
- `fsl-tool` / `freesurfer-tool` → post-fMRIPrep analysis

## More Advanced Features

For advanced options (custom templates, surface-based processing, ICA-AROMA, etc.), please refer to the official fMRIPrep documentation:
- Official Documentation: https://fmriprep.org/
- User Guide: https://fmriprep.org/en/stable/
- BIDS App specification: https://bids-apps.neuroimaging.io/

You may use the `multi-search-engine` or `academic-research-hub` skill to retrieve the latest best practices or example commands.

---

Created At: 2026-03-25 17:10 HKT  
Last Updated At: 2026-03-25 23:37 HKT  
Author: Cheng Wang