# Benchmark Test Case 31: FSL Tensor Fitting (DTIFIT)

## Task Description

Load corrected DWI and run tensor fitting.

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
  - benchmark_results/T33_fsl_tensor_fit/
- Long-running processing is allowed to run as a background job.

## Expected Output

Expected output artifact(s):

- FA map
- MD map
- Principal diffusion direction outputs

Recommended metadata file:

- result_YYYYMMDD_HHMMSS.json

## Evaluation

- This test case is manually evaluated.
