---
name: harness-engineering
description: "Use this skill whenever the user wants to validate, smoke-test, or regression-test any NeuroClaw skill or neuroimaging pipeline output. Triggers include: 'harness', 'test skill', 'smoke test', 'regression test', 'validate output', 'check pipeline', 'output validity', 'harness-engineering', 'QC pipeline', 'assert NIfTI', 'auto-qc', or any request to verify correctness of a skill run or neuroimaging file output. This skill is the **mandatory quality-assurance layer** in NeuroClaw: it reads a skill's harness.yaml spec, executes minimal-input test runs via claw-shell, applies neuroimaging-specific assertions, and produces a HARNESS_REPORT.md."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# Harness Engineering

## Overview

`harness-engineering` is the NeuroClaw **base-layer quality-assurance skill** for automated skill validation and neuroimaging pipeline output checking.

It bridges the gap left by the previously-planned `auto-qc` entry and implements three test types:

| Test Type | Purpose |
|-----------|---------|
| `smoke` | Verify the skill's core execution path completes without errors using minimal inputs |
| `regression` | Re-run a reference execution and compare outputs against a stored baseline |
| `output-validity` | Assert neuroimaging-specific properties (shape, voxel size, value range, file completeness) on any output file without re-running the skill |

**Architecture placement**: Base Layer — this skill is invoked by Interface-layer skills (`experiment-controller`, `skill-updater`) and may be called directly by the user.

**Research use only.** This skill does not make clinical judgments.

---

## Core Workflow (Never Bypassed)

1. **Parse request** — identify target skill name and test type (`smoke` / `regression` / `output-validity`).
2. **Locate harness spec** — read `skills/<target-skill>/harness.yaml`. If missing, stop and report: "No harness.yaml found for `<skill>`. Create one following the Harness Spec format below."
3. **Dependency pre-check** — verify `claw-shell` and `dependency-planner` are available; check that sample inputs listed in `harness.yaml` exist on disk.
4. **Generate numbered execution plan** — list every assertion step, estimated runtime, and risks.
5. **Present plan and wait for explicit user confirmation** ("YES" / "execute" / "proceed").
6. **On confirmation** — delegate all execution to `claw-shell`; run harness runner script.
7. **Collect results** — parse assertion outcomes (PASS / FAIL / SKIP), capture logs.
8. **Write HARNESS_REPORT.md** in the workspace root (append if already present, with dated section).
9. **Summarize** — print a final pass/fail table to the user and recommend follow-up actions for any failures.

---

## Harness Spec Format (`harness.yaml`)

Every skill that supports harness testing must include a `harness.yaml` in its skill directory. The file follows this schema:

```yaml
skill: <skill-name>            # matches the skills/ folder name
version: "1.0"
test_cases:
  - name: <test_case_name>     # short, unique identifier (no spaces)
    type: smoke | regression | output-validity
    description: <human-readable description>
    inputs:
      - key: <input_key>       # logical name used by the skill
        path: <relative_or_absolute_path_to_sample_file>
    expected_outputs:
      - path: <expected_output_path>   # relative to workspace root
        assertions:
          exists: true | false
          shape: [d0, d1, d2, d3]      # optional, for NIfTI/array files
          dtype: float32 | int16 | ...  # optional
          voxel_size_mm:               # optional, neuroimaging-specific
            min: 0.5
            max: 3.0
          value_range:                 # optional
            min: <number>
            max: <number>
          min_nonzero_voxels: <int>    # optional, ensures mask is non-trivial
          file_size_bytes:             # optional
            min: <int>
          required_keys: [key1, key2]  # optional, for JSON/CSV outputs
    timeout_seconds: 300
    env_requires: [nibabel, numpy]     # Python packages needed for assertions
```

A skill may define multiple test cases (e.g., one smoke test and one output-validity test).

---

## Neuroimaging-Specific Assertions

The harness runner evaluates the following assertion types, implemented via `nibabel` and `numpy`:

| Assertion | Description | Applicable to |
|-----------|-------------|---------------|
| `exists` | Output file exists and is non-empty | All output files |
| `shape` | NIfTI data array has exact expected shape | NIfTI (.nii / .nii.gz) |
| `dtype` | NIfTI data dtype matches expected type | NIfTI (.nii / .nii.gz) |
| `voxel_size_mm` | Voxel dimensions in mm are within [min, max] range | NIfTI (.nii / .nii.gz) |
| `value_range` | All data values fall within [min, max] | NIfTI, CSV, .npy |
| `min_nonzero_voxels` | At least N non-zero voxels present (guards against empty masks) | NIfTI segmentation masks |
| `file_size_bytes` | Output file is at least N bytes (guards against truncated writes) | All output files |
| `required_keys` | JSON or CSV output contains all expected column/key names | JSON, CSV |

**Dimension convention for neuroimaging modalities:**

| Modality | Expected NIfTI shape |
|----------|---------------------|
| sMRI (T1w, FLAIR) | 3D — `(X, Y, Z)` |
| fMRI (BOLD) | 4D — `(X, Y, Z, T)` |
| DWI | 4D — `(X, Y, Z, volumes)` |
| WMH mask | 3D — `(X, Y, Z)`, binary (0/1) |
| EEG feature matrix | 2D — `(channels, features)` or `(epochs, channels, features)` |

---

## Harness Runner Script

The following Python script is executed inside `claw-shell` to evaluate assertions defined in `harness.yaml`:

```python
# harness_runner.py — executed via claw-shell
# Usage: python harness_runner.py --spec skills/<skill>/harness.yaml --case <test_case_name>
import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

import yaml
import numpy as np
import nibabel as nib

def assert_nifti(path, assertions):
    results = []
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return [{"assertion": "exists", "status": "FAIL", "detail": f"{path} not found or empty"}]
    results.append({"assertion": "exists", "status": "PASS", "detail": str(path)})

    img = nib.load(str(p))
    data = img.get_fdata()
    zooms = img.header.get_zooms()

    if "shape" in assertions:
        expected = tuple(assertions["shape"])
        actual = data.shape
        status = "PASS" if actual == expected else "FAIL"
        results.append({"assertion": "shape", "status": status,
                         "detail": f"expected {expected}, got {actual}"})

    if "voxel_size_mm" in assertions:
        vmin = assertions["voxel_size_mm"].get("min", 0.0)
        vmax = assertions["voxel_size_mm"].get("max", float("inf"))
        spatial_zooms = zooms[:3]
        ok = all(vmin <= z <= vmax for z in spatial_zooms)
        results.append({"assertion": "voxel_size_mm", "status": "PASS" if ok else "FAIL",
                         "detail": f"voxel sizes {list(spatial_zooms)}, expected [{vmin}, {vmax}]"})

    if "value_range" in assertions:
        vmin = assertions["value_range"].get("min", -float("inf"))
        vmax = assertions["value_range"].get("max", float("inf"))
        ok = float(data.min()) >= vmin and float(data.max()) <= vmax
        results.append({"assertion": "value_range", "status": "PASS" if ok else "FAIL",
                         "detail": f"data range [{data.min():.4f}, {data.max():.4f}], expected [{vmin}, {vmax}]"})

    if "min_nonzero_voxels" in assertions:
        nz = int(np.count_nonzero(data))
        threshold = int(assertions["min_nonzero_voxels"])
        ok = nz >= threshold
        results.append({"assertion": "min_nonzero_voxels", "status": "PASS" if ok else "FAIL",
                         "detail": f"{nz} non-zero voxels, required >= {threshold}"})

    return results


def run_case(spec_path, case_name):
    with open(spec_path) as f:
        spec = yaml.safe_load(f)

    case = next((c for c in spec["test_cases"] if c["name"] == case_name), None)
    if case is None:
        print(f"ERROR: test case '{case_name}' not found in {spec_path}")
        sys.exit(1)

    all_results = []
    for out in case.get("expected_outputs", []):
        path = out["path"]
        assertions = out.get("assertions", {})
        suffix = Path(path).suffix.lower()
        if suffix in (".nii", ".gz"):
            results = assert_nifti(path, assertions)
        else:
            exists = Path(path).exists()
            results = [{"assertion": "exists", "status": "PASS" if exists else "FAIL",
                         "detail": str(path)}]
        all_results.extend(results)

    passed = sum(1 for r in all_results if r["status"] == "PASS")
    failed = sum(1 for r in all_results if r["status"] == "FAIL")
    print(f"\n=== Harness Results: {spec['skill']} / {case_name} ===")
    for r in all_results:
        icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"  {icon} [{r['assertion']}] {r['detail']}")
    print(f"\nSummary: {passed} passed, {failed} failed")
    return all_results, passed, failed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--output", default="HARNESS_REPORT.md")
    args = parser.parse_args()

    results, passed, failed = run_case(args.spec, args.case)

    report_path = Path(args.output)
    with open(report_path, "a") as f:
        f.write(f"\n## Harness Run — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")
        f.write(f"**Spec**: `{args.spec}`  **Case**: `{args.case}`\n\n")
        f.write("| Assertion | Status | Detail |\n|-----------|--------|--------|\n")
        for r in results:
            icon = "✅ PASS" if r["status"] == "PASS" else "❌ FAIL"
            f.write(f"| `{r['assertion']}` | {icon} | {r['detail']} |\n")
        f.write(f"\n**Total**: {passed} passed, {failed} failed\n")

    print(f"\nReport appended to {report_path}")
    sys.exit(0 if failed == 0 else 1)
```

---

## Quick Reference (Harness Commands)

```bash
# Smoke test for fmri-skill
python harness_runner.py --spec skills/fmri-skill/harness.yaml --case smoke_bold_validity

# Output-validity check for wmh-segmentation
python harness_runner.py --spec skills/wmh-segmentation/harness.yaml --case output_mask_validity

# EEG feature matrix check
python harness_runner.py --spec skills/eeg-skill/harness.yaml --case smoke_eeg_features

# Append results to a named report
python harness_runner.py --spec skills/fmri-skill/harness.yaml --case smoke_bold_validity --output results/fmri_harness_report.md
```

---

## Integration Points

| Calling Skill | When to Invoke Harness | What to Check |
|---------------|------------------------|---------------|
| `experiment-controller` | After every experiment run (step 7 in its workflow) | Output files exist, metrics are in valid range |
| `skill-updater` | Before proposing skill diffs | Smoke test still passes after proposed change |
| `bids-organizer` | After BIDS conversion | Required JSON sidecars exist, no forbidden files |
| `wmh-segmentation` | After Docker inference run | Mask is 3D, binary, non-empty |
| `fmri-skill` | After preprocessing or ROI extraction | BOLD is 4D, voxel size is reasonable |
| `eeg-skill` | After feature extraction | Feature matrix shape and value range |

---

## Creating a harness.yaml for a New Skill

When a new skill is added to NeuroClaw, create a matching `harness.yaml` by:

1. Identifying the skill's smallest valid input (a synthetic or real minimal-size sample).
2. Defining at least one `smoke` test case that exercises the main execution path.
3. Adding `output-validity` assertions for every primary output file.
4. Placing the file at `skills/<skill-name>/harness.yaml`.
5. Confirming it parses without error: `python -c "import yaml; yaml.safe_load(open('skills/<skill>/harness.yaml'))"`.

---

## Important Notes & Limitations

- **Execution via `claw-shell` only** — no direct subprocess calls outside the skill.
- **User confirmation is mandatory** before any test run.
- Harness runner requires `nibabel`, `numpy`, and `pyyaml`; install via `dependency-planner` if missing.
- Regression tests require a stored baseline; if none exists, the harness prompts the user to approve saving the current output as the new baseline.
- Large NIfTI files may take 10–60 seconds to load for assertion; estimate is shown in the plan.
- Report is always **appended** (never overwritten) to preserve history across runs.

---

## When to Call This Skill

- After any skill run completes successfully (optional but recommended).
- When debugging unexpected output from a neuroimaging pipeline.
- Before merging a skill update (regression safety check).
- When `experiment-controller` flags anomalous results.
- When the user explicitly asks to "test", "validate", "QC", or "check" any skill output.

---

## Complementary / Related Skills

- `claw-shell` → executes harness runner commands
- `dependency-planner` → installs nibabel, numpy, pyyaml
- `experiment-controller` → calls harness after experiment runs
- `skill-updater` → records harness results in skill update diffs
- `bids-organizer` → BIDS compliance checks

---

Created At: 2026-04-02 HKT
Last Updated At: 2026-04-02 HKT
Author: NeuroClaw Harness Engineering
