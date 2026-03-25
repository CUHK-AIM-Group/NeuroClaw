---
name: fmri-skill
description: "Use this skill whenever the user wants to perform fMRI preprocessing, first-level analysis, ROI extraction, functional connectivity, effective connectivity, or atlas-based alignment to MNI152 space using either fMRIPrep, HCP-style pipelines, or CONN Toolbox. Triggers include: 'fmri', 'fMRI analysis', 'functional connectivity', 'effective connectivity', 'ROI extraction', 'seed-based correlation', 'PPI', 'DCM', 'atlas alignment', 'MNI152', 'HCP pipeline', 'CONN toolbox', or any request involving BOLD data."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# fMRI Skill (Modality Layer)

## Overview

`fmri-skill` is the NeuroClaw **modality-layer** interface skill responsible for all fMRI data processing and analysis tasks.

It strictly follows the NeuroClaw hierarchical design principles:
- This skill **only describes WHAT needs to be done** and **which tool skill to delegate to**.
- It contains **no implementation code or concrete commands**.
- All concrete execution is delegated to existing base/tool skills: `fmriprep-tool`, `hcppipeline-tool`, `conn-tool`, `fsl-tool`, `bids-organizer`, and `claw-shell`.

**Core workflow (never bypassed):**
1. Identify input data (BIDS dataset or preprocessed BOLD files).
2. Generate a **numbered execution plan** that clearly states WHAT needs to be done and which tool skill will handle each step.
3. Present the full plan, estimated runtime, resource requirements, and risks to the user and wait for explicit confirmation (“YES” / “execute” / “proceed”).
4. On confirmation, delegate every step to the appropriate skill via `claw-shell`.
5. After execution, save all outputs in a clean directory structure (`fmri_output/`).

**Research use only.**

## Quick Reference (Common fMRI Tasks – Updated 2026-03-25)

| Task                                      | What needs to be done                                                      | Delegate to which tool skill                                      | Expected output                          |
|-------------------------------------------|----------------------------------------------------------------------------|-------------------------------------------------------------------|------------------------------------------|
| BIDS organization                         | Convert raw DICOM/NIfTI into valid BIDS structure                          | `bids-organizer`                                                  | BIDS-compliant dataset                   |
| Standardized preprocessing (fMRIPrep)     | Motion correction, distortion correction, coregistration, normalization   | `fmriprep-tool`                                                   | Preprocessed BOLD + anatomical derivatives |
| High-quality HCP-style preprocessing      | Structural + functional (ICA-FIX) + diffusion + MSMAll surface alignment  | `hcppipeline-tool`                                                | HCP-style preprocessed data              |
| Atlas alignment to MNI152                 | Register functional/anatomical data to MNI152 template                     | `fmriprep-tool` or `hcppipeline-tool` or `fsl-tool`               | Data in MNI152 space                     |
| ROI-data extraction                       | Extract mean time series from atlas-defined ROIs                           | `fsl-tool`                                                        | ROI time-series (CSV / .npy)             |
| Functional connectivity                   | Seed-based correlation, whole-brain functional connectivity, network analysis | `fsl-tool` or `conn-tool`                                         | Correlation matrices, connectivity maps  |
| Effective connectivity                    | Psychophysiological Interaction (PPI/gPPI), Granger causality, Dynamic Causal Modeling (DCM) | `fsl-tool` or `conn-tool`                                         | PPI maps, causality matrices, DCM parameters |
| First-level GLM (task-based)              | Task regressors + contrast estimation                                      | `fsl-tool` (FEAT)                                                 | Z-stat maps, cope files                  |
| Group-level analysis                      | Second-level statistics across subjects                                    | `fsl-tool` (randomise / FEAT)                                     | Group statistical maps                   |
| Advanced connectivity analysis (CONN)     | ROI-to-ROI, seed-to-voxel, ICA networks, PPI/gPPI, DCM                    | `conn-tool`                                                       | Comprehensive connectivity results       |
| Full end-to-end pipeline                  | BIDS → preprocessing (fMRIPrep or HCP) → alignment → ROI → connectivity   | `bids-organizer` + `fmriprep-tool` or `hcppipeline-tool` + `fsl-tool` or `conn-tool` | Complete results + QC report             |

## Installation (Handled by dependency-planner)

No manual installation required at this layer.  
When first used, `fmri-skill` automatically calls `dependency-planner` to ensure `fmriprep-tool`, `hcppipeline-tool`, `conn-tool`, `fsl-tool`, and `bids-organizer` are ready.

## NeuroClaw recommended wrapper script

No wrapper script is needed at the modality layer.  
All execution is routed through `bids-organizer`, `fmriprep-tool`, `hcppipeline-tool`, `conn-tool`, `fsl-tool`, and `claw-shell`.

## Important Notes & Limitations

- This SKILL.md contains **only high-level task descriptions and delegation instructions**.
- Users can choose between `fmriprep-tool` (faster, more flexible), `hcppipeline-tool` (higher quality, surface-based), or `conn-tool` (advanced connectivity & effective connectivity).
- Atlas alignment to MNI152 is primarily handled by `fmriprep-tool` or `hcppipeline-tool`.
- Long-running operations (HCP full pipeline, whole-brain connectivity, DCM model comparison) are automatically routed to background mode in the `claw` tmux session.
- Execution begins **only after explicit user confirmation** of the full numbered plan.
- All outputs are saved in `./fmri_output/` with clear subfolders (bids/, preproc/, hcp/, roi/, connectivity/, effective/, stats/, etc.).

## When to Call This Skill

- After `bids-organizer` when raw data needs structured preprocessing.
- When the user wants either standard fMRIPrep, high-quality HCP-style preprocessing, or advanced connectivity analysis via CONN Toolbox.
- When the research requires ROI time-series, functional connectivity, effective connectivity (PPI/gPPI/DCM), or accurate MNI152 / surface alignment.
- After `research-idea` or `method-design` when the experiment involves fMRI data.

## Complementary / Related Skills

- `bids-organizer` → organize raw data into BIDS
- `fmriprep-tool` → faster standardized preprocessing + MNI152 alignment
- `hcppipeline-tool` → high-quality HCP-style preprocessing (ICA-FIX, MSMAll, advanced diffusion)
- `conn-tool` → advanced functional & effective connectivity (ROI-to-ROI, seed-to-voxel, PPI/gPPI, DCM)
- `fsl-tool` → ROI extraction, basic connectivity, PPI, FEAT GLM
- `dependency-planner` → environment management
- `claw-shell` → safe execution of long-running pipelines
- `paper-writing` → generate tables and figures from connectivity matrices and statistical maps

## Reference & Source

Aligned with NeuroClaw modality-skill pattern (see `eeg-skill`, `freesurfer-processor`, etc.).  
Core tools used: `fmriprep-tool` (standard preprocessing), `hcppipeline-tool` (HCP-style high-quality processing), `conn-tool` (advanced connectivity), `fsl-tool` (connectivity + ROI + GLM), `bids-organizer` (data structuring).

Created At: 2026-03-25 16:02 HKT  
Last Updated At: 2026-03-25 16:10 HKT  
Author: Cheng Wang