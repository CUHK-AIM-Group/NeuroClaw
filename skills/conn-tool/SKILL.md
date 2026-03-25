---
name: conn-tool
description: "Use this skill whenever the user wants to perform advanced functional connectivity (ROI-to-ROI, seed-to-voxel, ICA) or effective connectivity (PPI, gPPI, DCM) analysis using the CONN Toolbox. Triggers include: 'conn', 'CONN toolbox', 'functional connectivity', 'effective connectivity', 'ROI-to-ROI', 'seed-to-voxel', 'PPI', 'gPPI', 'DCM', 'psychophysiological interaction', or any request for connectivity analysis after preprocessing."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# CONN Tool

## Overview

CONN is a MATLAB/SPM-based toolbox for comprehensive functional and effective connectivity analysis. It excels at ROI-to-ROI, seed-to-voxel, ICA-based network analysis, and psychophysiological interaction (PPI/gPPI) as well as Dynamic Causal Modeling (DCM).

This skill serves as the **NeuroClaw interface-layer wrapper** for the CONN Toolbox and strictly follows the hierarchical design:

1. Check whether CONN Toolbox and dependencies (MATLAB + SPM) are installed.
2. If missing → invoke `dependency-planner` to generate a safe installation plan.
3. Verify input data (typically preprocessed BOLD from `fmriprep-tool` or `hcppipeline-tool`).
4. Generate a clear, numbered execution plan with exact commands, project setup, and analysis steps.
5. Present the plan and wait for explicit user confirmation (“YES” / “execute” / “proceed”).
6. On confirmation → delegate the entire CONN project setup and analysis to `claw-shell`.
7. After completion, summarize connectivity matrices, statistical maps, and suggest next steps (e.g., visualization or `paper-writing`).

**Research use only.**

## Quick Reference

| Task                                      | What needs to be done                                                      | Delegate to which tool skill                  | Expected output                          |
|-------------------------------------------|----------------------------------------------------------------------------|-----------------------------------------------|------------------------------------------|
| Project setup                             | Create new CONN project from preprocessed data                             | `claw-shell`                                  | conn_*.mat project file                  |
| ROI definition & extraction               | Define ROIs from atlas or seed regions                                     | `claw-shell`                                  | ROI time series                          |
| Functional connectivity (ROI-to-ROI)      | ROI-to-ROI correlation analysis                                            | `claw-shell`                                  | Correlation matrices                     |
| Seed-to-voxel connectivity                | Seed-based whole-brain correlation                                         | `claw-shell`                                  | Seed-to-voxel maps                       |
| ICA network analysis                      | Group ICA + network component extraction                                   | `claw-shell`                                  | ICA components + networks                |
| PPI / gPPI                                | Psychophysiological interaction analysis                                   | `claw-shell`                                  | PPI contrast maps                        |
| Effective connectivity (DCM)              | Dynamic Causal Modeling                                                    | `claw-shell`                                  | DCM parameters & model comparison        |
| Full connectivity pipeline                | Preprocessed data → ROI definition → connectivity → statistics             | `claw-shell`                                  | Complete CONN results + figures          |

## Common Shell Command Examples

```bash
# Launch CONN in MATLAB (typical usage)
matlab -nodisplay -nosplash -r "conn; conn_batch('conn_project.mat'); exit;"
```

## Installation (Handled by dependency-planner)

Use `dependency-planner` with one of the following requests:

- “Install CONN Toolbox and SPM in MATLAB environment”
- “Install CONN Toolbox via MATLAB Add-Ons or manual download”

After installation, verify with:
```bash
matlab -batch "conn; disp('CONN version:'); conn('ver')"
```

**Prerequisites**:
- MATLAB (R2019b or newer recommended)
- SPM12 or SPM8
- Preprocessed data from `fmriprep-tool` or `hcppipeline-tool`

## NeuroClaw recommended wrapper script

```python
# conn_wrapper.py (placed inside the skill folder for reference)
import subprocess
import argparse

def run_conn_batch(project_file):
    cmd = [
        "matlab", "-nodisplay", "-nosplash", "-r",
        f"conn; conn_batch('{project_file}'); exit;"
    ]
    print("Running CONN batch:", project_file)
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Path to conn_*.mat project file")
    args = parser.parse_args()
    run_conn_batch(args.project)
```

## Important Notes & Limitations

- All actual CONN execution is routed through `claw-shell` (MATLAB calls).
- CONN requires a valid MATLAB license and SPM installation.
- Best results are obtained when input data comes from `fmriprep-tool` or `hcppipeline-tool`.
- Long-running analyses (whole-brain seed-to-voxel, DCM model comparison) are automatically run in background mode.
- Execution begins **only after explicit user confirmation** of the full numbered plan.

## When to Call This Skill

- After `fmriprep-tool` or `hcppipeline-tool` when the user needs advanced connectivity analysis.
- When the research question involves ROI-to-ROI, seed-to-voxel, PPI/gPPI, or DCM effective connectivity.
- When high-quality functional/effective connectivity results are required for `paper-writing` or `experiment-controller`.

## Complementary / Related Skills

- `fmriprep-tool` → standard preprocessing
- `hcppipeline-tool` → high-quality HCP-style preprocessing
- `fsl-tool` → basic connectivity and PPI as lighter alternative
- `dependency-planner` → install CONN + SPM + MATLAB environment
- `claw-shell` → safe execution of MATLAB/CONN commands

## Reference & Source

- Official CONN Toolbox Website: https://web.conn-toolbox.org/
- CONN Documentation: https://web.conn-toolbox.org/documentation
- Aligned with NeuroClaw modality-skill pattern (see `fmri-skill`, `eeg-skill`).

---
Created At: 2026-03-25 16:10 HKT  
Last Updated At: 2026-03-25 16:10 HKT  
Author: Cheng Wang