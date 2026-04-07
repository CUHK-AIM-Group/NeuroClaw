# T79_fmri_adni_rsfmri_full_pipeline: fMRI ADNI-Style Resting-State Pipeline

## Objective
End-to-end ADNI-like resting-state fMRI analysis from raw data

## Inputs
Raw fMRI data (T1w + BOLD) in BIDS or native format

## Outputs
Complete fmri_output/ with all derivatives and QC reports

## Key Points
- T90/T91: Organize data into BIDS format
- T92: Run fMRIPrep anatomical and functional preprocessing
- T101: Execute XCP-D denoising with motion scrubbing
- T102: Extract ROI timeseries from multiple atlases
- T103: Compute functional connectivity matrices
- Identify resting-state networks (RSN analytical components)
- Generate group connectivity templates
- Produce comprehensive QC report documenting all steps
- Save final outputs in fmri_output directory

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, TSV, NPZ where applicable)
- Statistical maps must contain valid numerical data with proper dimensions
- Connectivity matrices must be symmetric and valid (values between -1 and 1)
- No errors during processing, comprehensive logs generated
