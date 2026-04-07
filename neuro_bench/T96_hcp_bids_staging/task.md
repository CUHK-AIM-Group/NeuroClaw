# T96_hcp_bids_staging: HCP BIDS Data Staging and Organization

## Objective
Organize and standardize raw HCP data into BIDS-style directory structure

## Inputs
Raw HCP data from hcp_output/raw/

## Outputs
Standardized BIDS staging directory with validation report

## Key Points
- Parse raw HCP directory structure and identify modalities
- Organize structural MRI (T1w, T2w)
- Organize functional MRI (fMRI resting-state and task)
- Organize diffusion MRI (DWI, bvals, bvecs)
- Create BIDS-compliant directory layout: sub-*/ses-01/anat|func|dwi/
- Generate JSON sidecars with HCP parameters
- Create dataset_description.json for HCP
- Run bids-validator to verify compliance
- Generate staging validation report (warnings, errors)

## Evaluation Criteria
- Task completion verified by presence of required output files
- BIDS staging must pass bids-validator with minimal warnings
- Modality-specific outputs must match expected file formats
- QC reports must be comprehensive and readable
- Processing logs must document parameters, versions, and execution time
- Data integrity verified by file count and checksum validation
- No critical errors during processing
