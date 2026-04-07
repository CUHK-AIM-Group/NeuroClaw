# T86_smri_fmriprep_anat: Structural MRI fMRIPrep Anatomical Processing

## Objective
Run fMRIPrep anatomical-only mode on BIDS structural dataset

## Inputs
BIDS structural MRI dataset

## Outputs
Standardized anatomical derivatives and HTML QC report

## Key Points
- Execute fMRIPrep with --anat-only flag
- Perform T1w/T2w preprocessing and segmentation
- Generate brain masks and tissue probability maps
- Perform registration to MNI152 template
- Generate surface reconstruction derivatives
- Compute individual template spaces
- Output normalized anatomical maps in MNI and native space
- Produce comprehensive HTML QC report

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, statistics files)
- Structural maps must have proper dimensions and valid data ranges
- CSV files must contain headers and valid numerical data
- No errors during processing, comprehensive logs generated
