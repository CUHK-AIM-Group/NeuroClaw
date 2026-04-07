# T55_dwi_bids_organize: DWI BIDS Organization

## Objective
Organize local DWI NIfTI/bval/bvec files into BIDS-compliant dataset structure

## Inputs
Local DWI NIfTI, bval, and bvec files (raw format)

## Outputs
BIDS-compliant DWI structure with proper directory layout and file naming

## Key Points
- Create BIDS directory structure (sub-*/ses-*/dwi/)
- Rename files to BIDS standard: sub-*_ses-*_dwi.nii.gz, .bval, .bvec
- Generate dataset_description.json and README
- Include JSON sidecars with DWI metadata (EchoTime, RepetitionTime, etc.)
- Validate BIDS compliance using bids-validator

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, TCK, VTK where applicable)
- CSV files must contain headers and valid numerical data
- No errors or incomplete computations during processing
