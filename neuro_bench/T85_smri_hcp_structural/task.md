# T85_smri_hcp_structural: Structural MRI HCP-Style Processing

## Objective
Run HCP-style structural preprocessing on BIDS anatomical data

## Inputs
BIDS structural MRI dataset (T1w and/or T2w)

## Outputs
HCP-grade cortical surfaces, registrations, and derivatives

## Key Points
- PreFreeSurfer: Anatomical preprocessing and alignment
- Perform brain extraction and normalization
- Bias field correction and tissue segmentation
- FreeSurfer: Surface reconstruction and segmentation
- PostFreeSurfer: Surface registration and refinement
- MSMAll surface registration to standard templates
- Generate HCP-style aparc atlases
- Output high-quality surfaces (white, pial, inflated)
- Save transformation matrices for multimodal registration

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, statistics files)
- Structural maps must have proper dimensions and valid data ranges
- CSV files must contain headers and valid numerical data
- No errors during processing, comprehensive logs generated
