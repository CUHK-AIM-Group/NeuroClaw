---
name: hcppipeline-tool
description: "Use this skill whenever the user wants to perform high-quality, HCP-style preprocessing of multimodal MRI data (structural, functional, diffusion) using the official HCP Pipelines. Triggers include: 'HCP pipeline', 'HCP preprocessing', 'hcp-fmri', 'hcp-dwi', 'hcp-structural', 'MSMAll', 'ICA-FIX', 'bedpostx', 'probtrackx', or any request to run the Human Connectome Project preprocessing pipelines."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# HCP Pipeline Tool

## Overview
The HCP Pipelines are the official, highly optimized preprocessing pipelines developed by the Human Connectome Project. They provide state-of-the-art processing for structural (T1w/T2w), functional (task/resting-state fMRI with ICA-FIX), and diffusion MRI (topup + eddy + bedpostx + probtrackx + MSMAll surface alignment).

This skill serves as the **NeuroClaw interface-layer wrapper** for the HCP Pipelines and strictly follows the hierarchical design:

1. Check whether HCP Pipelines and dependencies are installed.
2. If missing → invoke `dependency-planner` to generate a safe installation plan.
3. Detect input data (preferably BIDS or HCP-style organized) and confirm processing stages.
4. Generate a clear, numbered execution plan with exact commands, flags, estimated runtime, and risks.
5. Present the plan and wait for explicit user confirmation (“YES” / “execute” / “proceed”).
6. On confirmation → delegate all pipeline stages to `claw-shell`.
7. After completion, summarize outputs and suggest next steps (e.g., connectivity analysis via `fmri-skill` or `fsl-tool`).

**Research use only.**

## Quick Reference

| Task                              | Recommended Pipeline Stage                          | Typical Runtime (per subject) |
|-----------------------------------|-----------------------------------------------------|-------------------------------|
| Structural preprocessing          | PreFreeSurfer + FreeSurfer + PostFreeSurfer         | 4–12 hours                    |
| Functional preprocessing          | fMRIVolume + fMRISurface + ICA-FIX                  | 2–6 hours                     |
| Diffusion preprocessing           | DiffusionPreprocessing + bedpostx + probtrackx      | 6–24 hours                    |
| Surface-based registration        | MSMAll                                              | 2–4 hours                     |
| Full HCP-style multimodal pipeline| All stages combined                                 | 12–36+ hours                  |

## Common Shell Command Examples

```bash
# Structural pipeline (most commonly used first)
${HCPPIPEDIR}/PreFreeSurfer/PreFreeSurferPipeline.sh \
  --path=/data/hcp_output \
  --subject=sub-001 \
  --t1=/data/bids/sub-001/anat/sub-001_T1w.nii.gz \
  --t2=/data/bids/sub-001/anat/sub-001_T2w.nii.gz

# Functional pipeline with ICA-FIX
${HCPPIPEDIR}/fMRIVolume/fMRIVolumePipeline.sh \
  --path=/data/hcp_output \
  --subject=sub-001 \
  --fmriname=rfMRI_REST1 \
  --fmritcs=/data/bids/sub-001/func/sub-001_task-rest_bold.nii.gz

# Diffusion pipeline
${HCPPIPEDIR}/DiffusionPreprocessing/DiffusionPreprocessing.sh \
  --path=/data/hcp_output \
  --subject=sub-001
```

## Installation (Handled by dependency-planner)
Use `dependency-planner` with one of the following requests:
- “Install official HCP Pipelines from GitHub”
- “Install HCP Pipelines and dependencies (FSL, FreeSurfer, CUDA if needed)”

After installation, verify with:
```bash
echo $HCPPIPEDIR
```

**Prerequisites**:
- FSL, FreeSurfer (with valid license)
- MATLAB (for some legacy parts) or Octave
- Sufficient disk space (20–100 GB per subject) and RAM (≥32 GB recommended)

## NeuroClaw recommended wrapper script
```python
# hcppipeline_wrapper.py (placed inside the skill folder for reference)
import subprocess
import argparse

def run_hcp_stage(stage, subject, bids_dir, output_dir):
    env = {"HCPPIPEDIR": "/opt/HCP-Pipelines"}
    cmd = [
        f"{env['HCPPIPEDIR']}/{stage}/{stage}Pipeline.sh",
        "--path", output_dir,
        "--subject", subject
    ]
    print("Running HCP stage:", stage)
    subprocess.run(cmd, env=env, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True, help="PreFreeSurfer, fMRIVolume, DiffusionPreprocessing, etc.")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--bids-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    
    run_hcp_stage(args.stage, args.subject, args.bids_dir, args.output_dir)
```

## Important Notes & Limitations
- All actual pipeline execution is routed through `claw-shell` due to extremely long runtimes.
- HCP Pipelines are very resource-intensive and disk-heavy.
- Requires well-organized input data (preferably BIDS via `bids-organizer` first).
- ICA-FIX denoising is one of the strongest features of HCP functional pipeline.
- Surface-based MSMAll registration provides superior alignment compared to volume-based methods.

## When to Call This Skill
- User wants the highest-quality, HCP-style preprocessing for multimodal data.
- When research requires accurate surface-based alignment, ICA-FIX cleaned resting-state fMRI, or advanced diffusion modeling.
- After `bids-organizer` when preparing data for connectomics or high-precision analysis.

## Complementary / Related Skills
- `bids-organizer` → organize raw data into BIDS before running HCP
- `fmriprep-tool` → lighter and faster alternative to HCP preprocessing
- `fsl-tool` → post-HCP connectivity and ROI analysis
- `dependency-planner` → install HCP Pipelines and dependencies
- `claw-shell` → safe execution of long-running pipelines
- `multi-search-engine` / `academic-research-hub` → retrieve latest HCP best practices

## Reference & Source
Official HCP Pipelines integration for NeuroClaw high-precision multimodal preprocessing.  
Official repository: https://github.com/Washington-University/HCPpipelines

Created At: 2026-03-25 19:30 HKT  
Last Updated At: 2026-03-26 00:12 HKT  
Author: chengwang96