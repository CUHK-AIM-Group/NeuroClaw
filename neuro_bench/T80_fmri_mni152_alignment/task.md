# T80_fmri_mni152_alignment: fMRI MNI152 Standard Space Alignment

## Objective
Complete atlas-based alignment of preprocessed BOLD to MNI152

## Inputs
Preprocessed BOLD data and anatomical reference

## Outputs
MNI152-normalized BOLD images and derivative files

## Key Points
- Register T1w anatomical to MNI152 template
- Generate and apply normalization transformation to BOLD
- Apply inverse transformations for native-to-standard mapping
- Verify alignment quality with checkerboard plots
- Generate Jacobian determinant maps for VBM analysis
- Output normalized BOLD in standard space
- Save transformation matrices (forward and inverse)
- Generate alignment QC visualizations

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, TSV, NPZ where applicable)
- Statistical maps must contain valid numerical data with proper dimensions
- Connectivity matrices must be symmetric and valid (values between -1 and 1)
- No errors during processing, comprehensive logs generated
