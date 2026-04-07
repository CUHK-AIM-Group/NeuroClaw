# T72_full_fmri_end2end: Complete End-to-End fMRI Analysis Pipeline

## Objective
Run complete fMRI analysis: BIDS organization → preprocessing → analysis

## Inputs
BIDS fMRI dataset with task design information

## Outputs
Complete fmri_output/ with all derivatives and QC reports

## Key Points
- T90/T91: Organize data into BIDS format
- T92 or T93: Run fMRIPrep or HCP preprocessing
- T96 or T97: Perform task-based GLM or connectivity analysis
- Generate summary statistics and activation maps
- Create group-level results (if multiple subjects)
- Production HTML QC report documenting all steps
- Save intermediate files for reproducibility
- Log all processing parameters and versions
- Final: fmri_output with organized final results

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, JSON, CSV, HTML where applicable)
- Statistical maps must contain valid numerical data
- No errors during processing, proper logs generated
