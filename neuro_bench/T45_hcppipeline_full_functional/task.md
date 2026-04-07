# Benchmark Test Case 45: HCP Full Functional Pipeline

## Task Description

Load local BOLD data (task or resting-state) and run complete HCP functional pipeline with ICA-FIX.

## Input Requirement

Required input(s):

- Local BOLD image (task or resting-state, required)

If any required input is missing, return:

- Missing required input

## Constraints

- Use HCP-compatible workflow and commands.
- Save all generated artifacts to:
  - benchmark_results/T60_hcp_full_functional/
- Long-running processing is allowed to run as a background job.

## Expected Output

Expected output artifact(s):

- fMRIVolume + fMRISurface + ICA-FIX outputs

Recommended metadata file:

- result_YYYYMMDD_HHMMSS.json

## Evaluation

- This test case is manually evaluated.
