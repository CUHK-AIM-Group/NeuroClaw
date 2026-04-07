# T77_fmri_first_level_glm: fMRI First-Level Task GLM

## Objective
Run FSL FEAT first-level GLM analysis on preprocessed BOLD

## Inputs
Preprocessed BOLD data and task design matrix (EV/3-column format)

## Outputs
Z-stat maps, cope files, and contrast statistics

## Key Points
- Design FEAT analysis with task conditions
- Specify contrasts and regressors from timing files
- Include temporal derivatives for better estimation
- Add motion confounds as nuisance regressors
- Set temporal filtering and smoothing parameters
- Run FILM with AUTOCORR prewhitening
- Generate Z-stat and F-stat maps for each contrast
- Output cope and varcope images
- Produce activation clusters and statistical summary

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, TSV, NPZ where applicable)
- Statistical maps must contain valid numerical data with proper dimensions
- Connectivity matrices must be symmetric and valid (values between -1 and 1)
- No errors during processing, comprehensive logs generated
