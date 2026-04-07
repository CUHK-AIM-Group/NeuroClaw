# Benchmark Test Case 44: HCP Full Structural Pipeline

## Task Description

Load local T1w + T2w (BIDS format) and run complete HCP structural pipeline.

## Input Requirement

Required input(s):

- Local T1w image in BIDS format (required)
- Local T2w image in BIDS format (required)

If any required input is missing, return:

- Missing required input

## Constraints

- Use HCP-compatible workflow and commands.
- Save all generated artifacts to:
  - benchmark_results/T59_hcp_full_structural/
- Long-running processing is allowed to run as a background job.

## Expected Output

Expected output artifact(s):

- PreFreeSurfer + FreeSurfer + PostFreeSurfer outputs

Recommended metadata file:

- result_YYYYMMDD_HHMMSS.json

## Evaluation

- This test case is manually evaluated.
