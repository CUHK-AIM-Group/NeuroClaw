# T69_conn_connectivity: CONN Functional/Effective Connectivity Analysis

## Objective
Run CONN Toolbox advanced connectivity analyses on preprocessed BOLD

## Inputs
Preprocessed BOLD data with ROI definitions

## Outputs
Connectivity matrices (ROI-to-ROI, seed-to-voxel) and statistical maps

## Key Points
- Load preprocessed BOLD into CONN
- Perform seed-to-voxel functional connectivity
- Compute ROI-to-ROI correlation matrices
- Run psychophysiological interaction (PPI) analyses
- Perform generalized PPI (gPPI) if required
- Optional: Dynamic causal modeling (DCM)
- Generate statistical maps and connectivity strength measures
- Output results in standard formats (NIfTI, CSV, MAT)

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, JSON, CSV, HTML where applicable)
- Statistical maps must contain valid numerical data
- No errors during processing, proper logs generated
