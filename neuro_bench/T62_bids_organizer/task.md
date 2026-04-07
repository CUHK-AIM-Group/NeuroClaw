# T62_bids_organizer: BIDS Dataset Organization

## Objective
Automatically organize local DICOM/NIfTI/EEG raw data into BIDS-compliant format

## Inputs
Raw DICOM, NIfTI, and/or EEG files (mixed formats)

## Outputs
BIDS-compliant dataset structure with validation report

## Key Points
- Convert DICOM to NIfTI if needed
- Create proper BIDS directory hierarchy (sub-*/ses-*/anat/func/dwi/fmap/eeg/)
- Rename files according to BIDS naming convention
- Generate dataset_description.json, README, and CHANGES files
- Create JSON sidecars with metadata
- Run bids-validator and generate validation report
- Log any conversion or organization warnings

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, JSON, CSV, HTML where applicable)
- Statistical maps must contain valid numerical data
- No errors during processing, proper logs generated
