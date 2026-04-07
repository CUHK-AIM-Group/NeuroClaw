# Benchmark Test Case 34: HCP Structural PreFreeSurfer

## Task Description

Load local T1w + T2w (BIDS format) and run HCP PreFreeSurfer structural preprocessing.

## Input Requirement

Required input(s):

- Local T1w image in BIDS format (required)
- Local T2w image in BIDS format (required)

If any required input is missing, return:

- Missing required input

## Constraints

- Use HCP-compatible workflow and commands.
- Save all generated artifacts to:
  - benchmark_results/T49_hcp_structural_pre_fs/
- Long-running processing is allowed to run as a background job.

## Expected Output

Expected output artifact(s):

- PreFreeSurfer processing outputs

Recommended metadata file:

- result_YYYYMMDD_HHMMSS.json

## Evaluation

- This test case is manually evaluated.
