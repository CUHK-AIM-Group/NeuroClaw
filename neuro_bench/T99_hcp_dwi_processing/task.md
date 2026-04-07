# T99_hcp_dwi_processing: HCP Diffusion MRI Processing

## Objective
Run diffusion MRI preprocessing, tensor metrics, and tractography on HCP data

## Inputs
HCP diffusion MRI (DWI, bvals, bvecs) from BIDS staging

## Outputs
Diffusion derivatives in dwi_output/

## Key Points
- Delegate to dwi-skill for preprocessing and analysis
- Run QSIPrep: motion correction, distortion correction, preprocessing
- Fit diffusion tensor model: compute FA, MD, AD, RD maps
- Run MRtrix3 tractography: ACT-based fiber tracking with SIFT filtering
- Extract ROI-wise diffusion features
- Generate structural connectome matrices
- Compute network topology metrics
- Output DTI scalar maps in MNI and native space
- Include diffusion metrics and tractography statistics

## Evaluation Criteria
- Task completion verified by presence of required output files
- BIDS staging must pass bids-validator with minimal warnings
- Modality-specific outputs must match expected file formats
- QC reports must be comprehensive and readable
- Processing logs must document parameters, versions, and execution time
- Data integrity verified by file count and checksum validation
- No critical errors during processing
