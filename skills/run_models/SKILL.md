---
name: run_models
description: "Use this skill whenever the user wants to run phenotype-prediction models, browse model cards, map model inputs/outputs, or choose an execution route for fMRI/sMRI based models. This is a model-entry orchestration skill: it routes requests to model-specific docs and delegates preprocessing to modality skills."
license: MIT License (NeuroClaw custom skill - freely modifiable within the project)
---

# Run Models Skill (Model Entry Layer)

## Overview
`run_models` is the NeuroClaw entry skill for model-level inference workflows.

This skill is responsible for:
- Maintaining a model registry (name, paper, source code, input/output, doc file path)
- Selecting the correct model document under `run_models/models/`
- Coordinating required data preparation before model execution
- Delegating modality preprocessing to `fmri-skill` and `smri-skill`

This skill does not hardcode detailed install/run commands for each model. Those details are stored in model-specific markdown files.

**Research use only.**

---

## Core Workflow (Never Bypassed)
1. Identify requested model and task (classification/regression phenotype prediction).
2. Locate the corresponding model document under `run_models/models/`.
3. Verify required inputs (ROI features, optional sMRI features).
4. If inputs are not ready, delegate preprocessing to modality skills:
	 - `fmri-skill` for ROI extraction from fMRI
	 - `smri-skill` when model additionally requires structural features
5. Generate a numbered execution plan and wait for explicit user confirmation (`YES` / `execute` / `proceed`).
6. On confirmation, execute via `claw-shell` following model doc instructions.

---

## Model Registry (Current)

| Model | Paper | Code | Input | Output | Model Doc |
|---|---|---|---|---|---|
| BrainGNN | Li et al., 2020, *Braingnn: Interpretable brain graph neural network for fmri analysis* | https://github.com/xxlya/BrainGNN_Pytorch/tree/main | fMRI ROI features (graph/node-level ROI representation) | Phenotype prediction (classification/regression) + interpretable graph indicators | `run_models/models/brain_gnn.md` |
| FM-APP | He et al., 2024, *FM-APP: Foundation model for any phenotype prediction via fMRI to sMRI knowledge transfer* | https://github.com/ZhibinHe/FM-APP | fMRI ROI features + sMRI features | Phenotype prediction (any-phenotype setting) | `run_models/models/fm_app.md` |
| NeuroStorm | NeuroClaw model entry for storm-related phenotype prediction workflows | see `run_models/models/neurostorm.md` | Multi-modal neuroimaging features as specified in the model doc | Phenotype prediction / downstream inference as specified in the model doc | `run_models/models/neurostorm.md` |

### Citation Notes
- BrainGNN:
	- Li X, Zhou Y, Dvornek N, Zhang M, Gao S, Zhuang J, Scheinost D, Staib L, Ventola P, Duncan J. 2020.
- FM-APP:
	- He Z, Li W, Liu Y, et al. FM-APP. IEEE TMI, 2024, 44(10): 4010-4022.
- NeuroStorm:
	- See `run_models/models/neurostorm.md` for the current model card, citation, and execution details.

## Harness-Aware Model Registration (Declarative + Testing + Drift Detection)

### Model Specification Format (Extended)
Every model integrated into run_models **must** include a **model specification file** in JSON format alongside its Markdown documentation:

**File**: `run_models/models/{model_name}_spec.json`

```json
{
  "model_name": "brain_gnn",
  "version": "1.0.0",
  "paper": "Li et al., 2020",
  "code_repo": "https://github.com/xxlya/BrainGNN_Pytorch",
  "required_dependencies": {
    "torch": ">=1.9.0,<2.1.0",
    "numpy": ">=1.21.0",
    "scipy": ">=1.7.0",
    "networkx": ">=2.6.0"
  },
  "input_spec": {
    "modality": "fMRI",
    "format": "ROI time-series (N_nodes, T_timepoints)",
    "expected_shape": [116, null],
    "value_range": [-5.0, 5.0],
    "required_preprocessing": ["z-score normalization"]
  },
  "output_spec": {
    "type": "classification|regression",
    "classes": null,
    "value_range": null
  },
  "validation_checksums": {
    "weights_sha256": "abc123...",
    "test_data_sha256": "def456..."
  }
}
```

### Test Suite Requirements
Every model **must** include an automated test suite covering:

1. **Input validation**: verify input dimensions, data types, value ranges
2. **Determinism check**: seed control + verify identical outputs with same seed (tolerance: 1e-6)
3. **Performance regression**: compare inference speed and memory usage against baseline
4. **Output coherence**: verify outputs lie within expected value range, no NaN/Inf values
5. **Backward compatibility**: test model against previous version checksum (if available)

**Test execution**:
```bash
python -m pytest run_models/tests/test_{model_name}.py -v --harness-report
```

Output: `run_models_test_report_{model_name}_{timestamp}.json` with pass/fail status and metrics

### Drift Detection Protocol
Monitor production/inference results for concept drift (distribution shift in data or model behavior):

**Automated monitoring per 100 inferences**:
- **Input distribution shift** (KL divergence against reference data): flag if deviation > 0.1
- **Output distribution shift** (prediction probability / regression output quantiles): flag if shift detected
- **Latency drift** (average inference time): alert if >20% increase
- **Failure rate monitoring** (predictions with NaN/Inf / out-of-range): flag if >1% failures

**Logging output**: `run_models_drift_log.json` (append-only, timestamped entries)

Example entry:
```json
{
  "timestamp": "2026-04-05T14:32:00Z",
  "model": "brain_gnn",
  "inference_count": 100,
  "input_kl_divergence": 0.045,
  "output_mean_shift": 0.002,
  "latency_ms": 45.2,
  "failure_rate": 0.0,
  "status": "healthy"
}
```

**Alert thresholds**: 
- KL divergence > 0.1 → generate warning
- Output shift > 5% std dev → investigation recommended
- Latency drift > 20% → check computational resource bottleneck
- Failure rate > 1% → stop inference, require manual review

### Model Card Template (Minimum Required Metadata)
Each model must include a model card in `run_models/models/{model_name}.md` documenting:

```markdown
## Model Card: {model_name}

### Model Details
- **Model name**: {name}
- **Version**: {X.Y.Z}
- **Date**: {YYYY-MM-DD}
- **Source repository**: {repo_url}
- **Paper**: {citation}

### Intended Use
- **Primary use case**: [e.g., fMRI-based phenotype classification]
- **Input modalities**: [fMRI, sMRI, etc.]
- **Supported tasks**: [classification, regression, interpretability]

### Known Limitations
- [e.g., "Trained on N subjects aged 18-65; generalization to pediatric/geriatric populations not validated"]
- [e.g., "Sensitive to head motion artifacts; recommend ICA-FIX preprocessing"]

### Validation Results
- **Test set performance**: [accuracy/AUC/RMSE with confidence intervals]
- **Cross-site validation**: [performance on held-out sites, if applicable]
- **Robustness checks**: [drift detection history, adversarial perturbation results]

### Dependencies & Versioning
- **Required libraries**: [see {model_name}_spec.json]
- **Hash (model weights)**: {SHA256}
- **Last verified**: {date}
```

---

## Delegation Rules

### BrainGNN Route
- Required modality preprocessing: `fmri-skill`
- Typical upstream outputs expected: ROI matrices/time-series converted to model-required feature tensors

### FM-APP Route
- Required modality preprocessing: `fmri-skill` + `smri-skill`
- Typical upstream outputs expected: fMRI ROI features plus structural MRI-derived features

### NeuroStorm Route
- Required modality preprocessing: follow the model doc in `run_models/models/neurostorm.md`
- Typical upstream outputs expected: inputs and features specified by the NeuroStorm model card

### Shared Execution Routing
- Environment/dependency planning: `dependency-planner` + `conda-env-manager`
- Actual model run command execution: `claw-shell`

---

## Input and Output Contract (Entry-Level)

### Inputs expected by this skill
- Model selection (`brain_gnn`, `fm_app`, or `neurostorm`)
- Data split / subject list
- Phenotype target definition
- Optional compute constraints (GPU/CPU, memory, batch size)

### Outputs produced by this skill
- A confirmed, numbered run plan
- Pointers to the model-specific instruction file
- Delegated preprocessing plan for required modalities
- Structured output location recommendations

---

## Recommended Output Layout
All model-running artifacts should be managed under `./run_models_output/`:
- `run_models_output/preprocessed/`
	- `fmri/` (from `fmri-skill`)
	- `smri/` (from `smri-skill`, if required)
- `run_models_output/brain_gnn/`
- `run_models_output/fm_app/`
- `run_models_output/neurostorm/`
- `run_models_output/logs/`
- `run_models_output/reports/`

---

## Safety and Execution Policy
- No execution before explicit user confirmation of the numbered plan.
- All run/install actions must go through `claw-shell`.
- If model docs are missing in `run_models/models/`, stop and request or create them before execution.
- Keep train/val/test split and target definition explicit to avoid leakage.

---

## When to Call This Skill
- User asks to run BrainGNN or FM-APP.
- User asks to run NeuroStorm.
- User asks which phenotype model to use for fMRI/sMRI ROI data.
- User asks for a unified entry point to model introduction + run routing.

---

## Complementary / Related Skills
- `fmri-skill`
- `smri-skill`
- `dependency-planner`
- `conda-env-manager`
- `claw-shell`

---

## Reference
- BrainGNN paper and code:
	- https://github.com/xxlya/BrainGNN_Pytorch/tree/main
- FM-APP paper and code:
	- https://github.com/ZhibinHe/FM-APP

Created At: 2026-03-28 20:38 HKT
Last Updated At: 2026-04-05 02:01 HKT
Author: chengwang96