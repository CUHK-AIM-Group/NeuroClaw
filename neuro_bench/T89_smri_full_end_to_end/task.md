# T89_smri_full_end_to_end: Structural MRI Complete End-to-End Pipeline

## Objective
End-to-end structural MRI analysis from raw data to feature extraction

## Inputs
Raw structural MRI data (DICOM or NIfTI with T1w and optional T2w/FLAIR)

## Outputs
Complete smri_output/ with all derivatives and QC reports

## Key Points
- T109: Organize data into BIDS format
- T110: Convert DICOM to NIfTI with metadata
- T111: Run FSL fsl_anat preprocessing
- T112: Run FreeSurfer recon-all surface reconstruction
- T113 or T114: Optional HCP or fMRIPrep preprocessing
- T115: Run WMH segmentation if FLAIR available
- T116: Extract ROI-wise morphological features
- Generate comprehensive processing report documenting all steps
- Save all intermediate and final outputs in organized smri_output directory
- Produce combined HTML QC report showing all processing stages

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, statistics files)
- Structural maps must have proper dimensions and valid data ranges
- CSV files must contain headers and valid numerical data
- No errors during processing, comprehensive logs generated
