# T100_hcp_full_multimodal: HCP Complete Multimodal End-to-End Pipeline

## Objective
Run complete multimodal HCP processing from download to final derivatives

## Inputs
HCP dataset specifications (download parameters and processing options)

## Outputs
Complete hcp_output/ with all multimodal derivatives and QC

## Key Points
- T123: Download specified HCP subset from ConnectomeDB
- T124: Organize raw data into BIDS staging directory
- Run T125, T126, T127 in parallel (structural, functional, diffusion)
- Coordinate across three processing streams:
-   - sMRI: surfaces, segmentation, cortical metrics
-   - fMRI: preprocessing, connectivity, network analysis
-   - DWI: tensor fitting, tractography, connectome
- Generate individual subject reports for each modality
- Create integrated multimodal QC report
- Produce summary statistics across all modalities
- Save organized hcp_output with consistent naming and metadata
- Ready for group-level multimodal analysis

## Evaluation Criteria
- Task completion verified by presence of required output files
- BIDS staging must pass bids-validator with minimal warnings
- Modality-specific outputs must match expected file formats
- QC reports must be comprehensive and readable
- Processing logs must document parameters, versions, and execution time
- Data integrity verified by file count and checksum validation
- No critical errors during processing
