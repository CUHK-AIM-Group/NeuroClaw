# T81_smri_bids_organize: Structural MRI BIDS Organization

## Objective
Automatically organize local DICOM/NIfTI structural MRI data into BIDS-compliant format

## Inputs
Raw structural MRI DICOM or NIfTI files (T1w, T2w, FLAIR)

## Outputs
BIDS-compliant structural MRI dataset with validation report

## Key Points
- Convert DICOM to NIfTI if needed
- Create BIDS directory structure (sub-*/ses-*/anat/)
- Rename files to BIDS standard: sub-*_ses-*_T1w.nii.gz, _T2w.nii.gz, _FLAIR.nii.gz
- Generate JSON sidecars with MRI acquisition parameters
- Create dataset_description.json, README, and CHANGES files
- Handle multiple sequences (T1w, T2w, FLAIR) per subject
- Run bids-validator and generate validation report
- Log conversion statistics and warnings

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, statistics files)
- Structural maps must have proper dimensions and valid data ranges
- CSV files must contain headers and valid numerical data
- No errors during processing, comprehensive logs generated
