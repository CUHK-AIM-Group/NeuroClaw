# Benchmark Test Case 32: FSL Multi-fiber Modeling (BEDPOSTX)

## Task Description

Load corrected DWI and run BEDPOSTX multi-fiber modeling.

## Input Requirement

Required input(s):

- Corrected DWI (required)
- bvecs/bvals (required)
- brain mask (required)

If any required input is missing, return:

- Missing required input

## Constraints

- Use FSL-compatible workflow and commands.
- Save all generated artifacts to:
  - benchmark_results/T34_fsl_multi_fiber/
- Long-running processing is allowed to run as a background job.

## Expected Output

Expected output artifact(s):

- BEDPOSTX output folder with multi-direction fiber distribution model

Recommended metadata file:

- result_YYYYMMDD_HHMMSS.json

## Evaluation

- This test case is manually evaluated.
