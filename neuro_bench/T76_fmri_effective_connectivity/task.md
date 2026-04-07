# T76_fmri_effective_connectivity: fMRI Effective Connectivity (PPI/DCM)

## Objective
Compute effective connectivity using PPI, gPPI, or DCM

## Inputs
Preprocessed BOLD and task design/seed ROI info

## Outputs
PPI maps, causal matrices, or DCM parameters

## Key Points
- Extract seed ROI timeseries
- Compute Psychophysiological Interaction (PPI)
- Optional: Generalized PPI (gPPI) with multiple seeds
- Optional: Dynamic Causal Modeling (DCM) for causal inference
- Generate statistical maps for connectivity changes
- Compute interaction effects between task and connectivity
- Save results in standard formats (NIfTI, CSV, MAT)
- Generate connectivity parameter estimates and t-statistics

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, TSV, NPZ where applicable)
- Statistical maps must contain valid numerical data with proper dimensions
- Connectivity matrices must be symmetric and valid (values between -1 and 1)
- No errors during processing, comprehensive logs generated
