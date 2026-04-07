# T58_dwi_roi_features: DWI ROI-wise Diffusion Features

## Objective
Extract ROI-wise diffusion metrics using DTI scalar maps and parcellation

## Inputs
FA/MD/AD/RD maps + atlas/parcellation in DWI space

## Outputs
roi_stats.csv with mean/std diffusion metrics per ROI

## Key Points
- Register parcellation atlas to DTI space (if needed)
- Extract mean and standard deviation of FA within each ROI
- Extract mean and standard deviation of MD within each ROI
- Extract mean and standard deviation of AD within each ROI
- Extract mean and standard deviation of RD within each ROI
- Output CSV with columns: roi_label, roi_name, fa_mean, fa_std, md_mean, md_std, ad_mean, ad_std, rd_mean, rd_std

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, TCK, VTK where applicable)
- CSV files must contain headers and valid numerical data
- No errors or incomplete computations during processing
