# T68_fsl_feat_glm: FSL FEAT Task-based GLM

## Objective
Run FEAT first-level task GLM analysis on preprocessed fMRI

## Inputs
Preprocessed BOLD data, task design file (EV/3col format)

## Outputs
Z-stat maps, cope files, and statistical results

## Key Points
- Set up FEAT analysis with proper design specifications
- Specify contrasts and regressors from task design
- Include confound regressors (motion, etc.)
- Apply temporal smoothing and high-pass filtering
- Run GLM using FILM with AUTOCORR prewhitening
- Generate Z-statistic maps for each contrast
- Produce cope and varcope files
- Output summary statistics and activation clusters

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, JSON, CSV, HTML where applicable)
- Statistical maps must contain valid numerical data
- No errors during processing, proper logs generated
