---
name: eeg-skill
description: "Use this skill whenever the user wants to load, preprocess, epoch, filter, or extract features from EEG data (resting-state, task-based, BCI, clinical, motor imagery, emotion, epilepsy, fatigue, etc.). Triggers include: 'eeg', 'EEG preprocessing', 'EEG feature extraction', 'band power', 'downsample to frequency bands', 'motor imagery BCI', 'emotion EEG', 'epilepsy detection', or any request involving .set/.edf/.bdf/.fif/.bids files."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# EEG Skill (Modality Layer)

## Overview

`eeg-skill` is the NeuroClaw **modality-layer** interface skill responsible for all EEG data processing tasks.

It strictly follows the NeuroClaw hierarchical design principles:
- This skill **only describes WHAT needs to be done** and **which tool skill to delegate to**.
- It contains **no implementation code, commands, or tool-specific usage details**.
- All concrete execution (environment setup, MNE-Python calls, file I/O, etc.) is delegated to the dedicated base/tool skill `mne-eeg-tool`.
- MNE-Python is the core library for EEG processing; its specific implementation lives exclusively in `mne-eeg-tool`.

**Core workflow (never bypassed):**
1. Identify the user-provided EEG files (BIDS, .set, .edf, .bdf, .fif, etc.).
2. Generate a **numbered execution plan** that clearly states WHAT needs to be done and which tool skill will handle each step.
3. Present the full plan, estimated runtime, resource requirements, and risks to the user and wait for explicit confirmation (“YES” / “execute” / “proceed”).
4. On confirmation, delegate every step to the appropriate base/tool skill (`mne-eeg-tool` via `claw-shell`).
5. After execution, save all outputs in a clean directory structure (`eeg_output/`).

**Research use only** — outputs are for scientific analysis only.

## Quick Reference (Common EEG Tasks – Updated 2026-03-25)

| Task                                      | What needs to be done                                              | Delegate to which tool skill                  | Expected output                          |
|-------------------------------------------|--------------------------------------------------------------------|-----------------------------------------------|------------------------------------------|
| Load & basic validation                   | Read raw EEG + channel locations + events + validation             | `claw-shell` (via `mne-eeg-tool`)            | Validation report + raw object           |
| Bad-channel detection & interpolation     | Auto-detect + interpolate noisy channels                           | `claw-shell` (via `mne-eeg-tool`)            | Cleaned raw data                         |
| Downsampling + filtering                  | Resample, high-pass, notch, bandpass filtering                     | `claw-shell` (via `mne-eeg-tool`)            | Filtered .fif files                      |
| Artifact removal                          | ICA + AutoReject + EOG/ECG regression                              | `claw-shell` (via `mne-eeg-tool`)            | Cleaned data                             |
| Continuous data cleaning                  | Resting-state pipeline (no events)                                 | `claw-shell` (via `mne-eeg-tool`)            | Cleaned continuous data                  |
| Re-referencing & epoching                 | Average reference (CAR) / REST + epoching + baseline correction    | `claw-shell` (via `mne-eeg-tool`)            | Epoched .fif files                       |
| Frequency-band extraction                 | Split into δ/θ/α/β/γ bands and compute power                       | `claw-shell` (via `mne-eeg-tool`)            | Per-band .fif files + power matrices     |
| Feature extraction (core)                 | Band power, CSP, Hjorth, sample entropy                            | `claw-shell` (via `mne-eeg-tool`)            | Feature matrices (CSV / .npy / .npz)     |
| Advanced features                         | Functional connectivity, ERP peaks/latency/AUC, frontal alpha asymmetry, microstates | `claw-shell` (via `mne-eeg-tool`)            | Connectivity matrices, ERP CSV, asymmetry .npy, microstates .fif |
| Full end-to-end pipeline                  | Any combination of the above for BCI, emotion, epilepsy, etc.      | `claw-shell` + `dependency-planner`          | Complete processed dataset + QC report   |

## Installation (Handled by dependency-planner)

No manual installation required.  
When first used, `eeg-skill` automatically calls `dependency-planner` to create the isolated `neuroclaw-eeg` conda environment containing MNE-Python and all required packages.

## NeuroClaw recommended wrapper script

No wrapper script is needed at the modality layer.  
All execution is routed through `mne-eeg-tool` → `claw-shell`.

## Important Notes & Limitations

- This SKILL.md contains **only task descriptions and delegation instructions** — no MNE-Python code or concrete commands (implementation lives in `mne-eeg-tool`).
- Long-running operations (ICA on long recordings, connectivity matrices, microstate analysis) are automatically routed to background mode in the `claw` tmux session.
- Execution begins **only after explicit user confirmation** of the full numbered plan.
- All outputs are saved in `./eeg_output/` with clear subfolders.

## When to Call This Skill

- The user provides raw or partially processed EEG data and requests preprocessing, frequency-band extraction, feature engineering, or a full pipeline.
- After `research-idea` or `method-design` when the experiment involves EEG data.

## Complementary / Related Skills

- `dependency-planner` + `conda-env-manager` → environment and MNE-Python installation
- `claw-shell` → all actual execution
- `mne-eeg-tool` → stores all specific MNE-Python usage and code (base/tool layer)

## Reference & Source

Aligned with NeuroClaw modality-skill pattern (see `freesurfer-processor`, `wmh-segmentation`, etc.).  
MNE-Python is the standard core library for EEG; its concrete implementation lives in the dedicated `mne-eeg-tool` skill.

Created At: 2026-03-25 14:30 HKT  
Last Updated At: 2026-03-25 14:30 HKT  
Author: Cheng Wang