# T87_smri_wmh_segmentation: Structural MRI WMH Segmentation

## Objective
Automatic white matter hyperintensity segmentation using MARS-WMH nnU-Net

## Inputs
FLAIR and T1w anatomical NIfTI files

## Outputs
WMH segmentation mask in NIfTI format with statistics

## Key Points
- Prepare FLAIR and T1w images in native space
- Register to MNI152 for model consistency (optional)
- Run pre-trained MARS-WMH nnU-Net model
- Generate binary WMH segmentation mask
- Compute probability map for uncertain voxels
- Calculate WMH volume and spatial statistics
- Produce QC report with lesion maps overlaid
- Save results in BIDS derivatives format

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, statistics files)
- Structural maps must have proper dimensions and valid data ranges
- CSV files must contain headers and valid numerical data
- No errors during processing, comprehensive logs generated
