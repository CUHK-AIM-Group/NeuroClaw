# T61_dwi_full_pipeline: DWI Full Analysis Pipeline

## Objective
End-to-end DWI analysis: BIDS organization → QSIPrep → tensor → ROI → tractography → connectome

## Inputs
Local raw DWI NIfTI/bval/bvec files

## Outputs
Complete dwi_output/ with all derivatives: BIDS structure, preproc_dwi, scalar maps, roi_stats.csv, tractogram, connectome

## Key Points
- T83: Organize input files into BIDS format
- T84: Run QSIPrep preprocessing
- T85: Compute DTI scalar maps (FA, MD, AD, RD)
- T86: Extract ROI-wise diffusion features
- T87: Perform MRtrix3 tractography with ACT+SIFT
- T88: Generate structural connectome matrix
- Save all intermediate and final outputs in organized dwi_output directory
- Generate comprehensive processing log documenting all steps

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, TCK, VTK where applicable)
- CSV files must contain headers and valid numerical data
- No errors or incomplete computations during processing
