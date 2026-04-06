# Benchmark Test Case 10: DWI Load and Consistency Check

## Task Description

Load local DWI inputs:

- 4D NIfTI file (DWI)
- `.bval`
- `.bvec`

Then perform consistency checks:

1. DWI is 4D
2. Spatial/volume shape is valid
3. Number of diffusion volumes equals gradient count
4. `bval` count matches DWI 4th dimension
5. `bvec` direction count matches DWI 4th dimension

Finally, keep arrays in memory for downstream workflow.

## Input Requirement

Required files (example naming):

- `dwi.nii` or `dwi.nii.gz`
- `dwi.bval`
- `dwi.bvec`

If any required input is missing, return:

- `任务缺少输入`

## Constraints

- No interactive input required.
- Must complete shape/dimension/gradient consistency checks.
- Save execution artifact(s) to:
  - `benchmark_results/T10_dwi_load/`

## Expected Output

Recommended output file:

- `result_YYYYMMDD_HHMMSS.json`

Recommended JSON fields:

```json
{
  "metadata": {
    "task": "T10_dwi_load",
    "timestamp": "ISO-8601",
    "status": "success or fail"
  },
  "input": {
    "dwi_path": "string",
    "bval_path": "string",
    "bvec_path": "string"
  },
  "checks": {
    "is_4d": true,
    "dwi_shape": [128, 128, 70, 96],
    "n_volumes": 96,
    "n_bvals": 96,
    "n_bvecs": 96,
    "counts_consistent": true
  }
}
```

## Evaluation

- This test case is **manually evaluated**.
