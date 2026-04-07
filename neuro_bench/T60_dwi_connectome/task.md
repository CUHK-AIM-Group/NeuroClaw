# T60_dwi_connectome: DWI Structural Connectome

## Objective
Generate ROI-to-ROI structural connectivity matrix from tractography

## Inputs
Filtered tractogram (TCK) + parcellation atlas in subject space

## Outputs
connectome.csv and connectome_weighted.nii.gz (optional)

## Key Points
- Use tck2connectome to compute connection matrix
- Count number of tracts between each ROI pair
- Optionally weight by tract length/counts
- Ensure symmetric/undirected connectivity matrix
- Output CSV with shape (N_ROIs × N_ROIs)
- Include labels and metadata for interpretation

## Evaluation Criteria
- Task completion verified by presence of required output files
- Output files must be in correct format (NIfTI, CSV, TCK, VTK where applicable)
- CSV files must contain headers and valid numerical data
- No errors or incomplete computations during processing
