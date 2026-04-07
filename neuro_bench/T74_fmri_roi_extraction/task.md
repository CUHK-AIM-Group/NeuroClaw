# T74_fmri_roi_extraction: fMRI ROI Timeseries Extraction

## Objective
Extract standard atlas ROI timeseries from denoised BOLD

## Inputs
Denoised BOLD data (XCP-D output)

## Outputs
Multi-atlas timeseries files (.tsv format)

## Key Points
- Load multiple standard atlases (Schaefer 100/200/400, Glasser 360, Gordon 333, Tian 96)
- Register atlases to subject space if needed
- Extract mean BOLD timeseries for each ROI
- Standardize and quality control timeseries
- Output separate .tsv files for each atlas
- Include ROI labels and coordinates in headers
- Save metadata with atlas descriptions

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, TSV, NPZ where applicable)
- Statistical maps must contain valid numerical data with proper dimensions
- Connectivity matrices must be symmetric and valid (values between -1 and 1)
- No errors during processing, comprehensive logs generated
