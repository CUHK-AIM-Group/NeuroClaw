# T64_fmriprep_preprocessing: fMRI fMRIPrep Preprocessing

## Objective
Run standardized fMRIPrep preprocessing on BIDS fMRI dataset

## Inputs
BIDS fMRI dataset with anatomical T1w/T2w

## Outputs
Preprocessed BOLD, anatomical derivatives, and HTML QC report

## Key Points
- Execute fMRIPrep with recommended parameters
- Perform anatomical segmentation and surface reconstruction
- Perform functional distortion correction and realignment
- Apply high-pass temporal filtering
- Output preprocessed BOLD in MNI152 and native space
- Generate comprehensive HTML report for visual QC
- Save confound regressors for downstream analysis

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, JSON, CSV, HTML where applicable)
- Statistical maps must contain valid numerical data
- No errors during processing, proper logs generated
