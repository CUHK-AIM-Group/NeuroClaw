# T97_hcp_smri_processing: HCP Structural MRI Processing

## Objective
Run complete structural MRI processing pipeline on HCP data

## Inputs
HCP structural MRI (T1w, T2w) from BIDS staging

## Outputs
Structural derivatives in smri_output/

## Key Points
- Delegate to smri-skill for multi-method processing
- Run FSL fsl_anat: brain extraction, tissue segmentation, MNI registration
- Run FreeSurfer recon-all: surface reconstruction, segmentation, statistics
- Run HCP structural pipeline: PreFreeSurfer + FreeSurfer + PostFreeSurfer
- Generate cortical thickness maps and surface atlases
- Compute cortical and subcortical statistics
- Output HCP-grade surfaces (white, pial, inflated)
- Include QC metrics and visualization
- Save transformation matrices for multimodal registration

## Evaluation Criteria
- Task completion verified by presence of required output files
- BIDS staging must pass bids-validator with minimal warnings
- Modality-specific outputs must match expected file formats
- QC reports must be comprehensive and readable
- Processing logs must document parameters, versions, and execution time
- Data integrity verified by file count and checksum validation
- No critical errors during processing
