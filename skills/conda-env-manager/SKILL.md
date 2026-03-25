---

name: conda-env-manager  
description: "Use this skill whenever the user wants to create, activate, list, export, update, clone, remove, or otherwise manage conda environments, or when a deep-learning / model skill requires a clean, isolated conda environment (e.g. 'create conda env for torch 2.3 cuda', 'export current env to yml', 'list all my conda envs', 'update packages in neuroclaw-dl', 'remove old env', 'clone env for reproducibility', 'install pytorch in new env'). Triggers include: 'conda create', 'conda env', 'make new environment', 'export yml', 'activate env', 'conda list envs', 'update conda env', 'clean environment', 'reproduce env', 'conda remove'. This skill is the **mandatory gatekeeper for conda operations**: it ALWAYS plans first, shows commands + risks + best practices, and waits for explicit user confirmation before executing anything."  
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)  

---

# Conda Environment Manager

## Overview

Conda is the backbone for reproducible, cross-platform environments in NeuroClaw — especially when dealing with CUDA-dependent deep learning stacks (PyTorch, TensorFlow, MONAI, nnU-Net), neuroimaging tools (ANTs, FSL wrappers, nipype), and scientific computing packages.

This skill acts as the **interface-layer orchestrator** for all common conda operations, preventing accidental modification of the base environment, reducing version conflicts, and enforcing best practices (isolated envs per project, environment.yml for reproducibility, explicit version pinning where critical, dry-run previews).

**Strict workflow (never skipped):**

1. Parse user intent from request or context (create / export / update / remove / clone / list / activate guidance).
2. Detect current conda setup: `conda info`, active env, available disk space, conda version.
3. Propose a safe, best-practice plan:
   - Prefer `--name` over `--prefix` for readability (unless user specifies prefix)
   - Always suggest creating new env instead of polluting base or existing ones
   - Recommend `environment.yml` export/import for reproducibility & sharing
   - Use `--yes` only after user confirmation
   - Warn about large downloads (CUDA stacks, large models)
   - Suggest channel priority: conda-forge > pytorch/nvidia > defaults
4. Show numbered plan + exact commands + estimated time/size + risks.
5. Wait for explicit user confirmation (“YES”, “execute”, “proceed”).
6. On approval: execute safely (subprocess with logging), capture output, report success/failure, suggest next steps (e.g. activate, install via dependency-planner).

**Core safety & best-practice rules**  
- Never modify base unless explicitly requested (and double-warned)  
- Prefer `conda env export --from-history > environment.yml` for clean, reproducible specs  
- Use `--dry-run` / plan preview by default  
- Integrate with dependency-planner for post-creation package installs  
- Log all actions to `./logs/conda_YYYYMMDD_HHMMSS.log`

## Quick Reference (Common NeuroClaw Tasks)

| Task                                      | Recommended Approach (after user confirmation)                          |
|-------------------------------------------|-------------------------------------------------------------------------|
| Create ML env with specific Python + CUDA | `conda create -n neuroclaw-dl python=3.11` then install pytorch-cuda via dependency-planner |
| Export current env for reproducibility    | `conda env export --from-history > env-neuroclaw.yml`                  |
| Create env from yml file                  | `conda env create -f environment.yml`                                   |
| List all environments                     | `conda env list` or `conda info --envs`                                 |
| Clone env for testing / branching         | `conda create --name neuroclaw-test --clone neuroclaw-dl`               |
| Update packages safely                    | `conda update --all --dry-run` → confirm → execute                      |
| Remove unused env                         | `conda env remove -n old-env`                                           |
| Activate / switch env (guidance only)     | Print instructions: `conda activate neuroclaw-dl`                       |

## Installation

This skill is **pure Python orchestration** — no external binaries needed beyond a working conda installation.

**Required prerequisites (must exist before activation):**

- Working conda / mamba / micromamba installation
- `dependency-planner` (recommended companion for package installation after env creation)
- Basic subprocess / shell access

To register in NeuroClaw:

```bash
# Place files in: skills/conda-env-manager/
# Update SOUL.md and/or USER.md with trigger phrases
```

## Usage Examples

### Example 1: “Create a new conda env for PyTorch 2.3 with CUDA 12.4 and Python 3.11”

```text
# Skill flow:
# 1. Detect conda version & disk space
# 2. Plan:
Step 1: conda create -n neuroclaw-pytorch python=3.11 -y --dry-run   # preview
Step 2: conda activate neuroclaw-pytorch   # (guidance only — user runs manually)
Step 3: Hand over to dependency-planner for: pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
Risk: medium (CUDA download ~3-5 GB)
Estimated time: 5–12 min
# 3. Prompt: “Execute Step 1? Reply YES to proceed.”
```

### Example 2: “Export current environment to yml for sharing”

```text
# Flow:
# 1. Detect active env
# 2. Plan:
Step 1: conda env export --from-history > neuroclaw-20260319.yml
Step 2: (Optional) git add & commit via git-workflows
# 3. Execute after confirmation
```

## NeuroClaw recommended wrapper script (placed inside skill folder)

```python
# conda_env_manager.py
import subprocess
import argparse
import sys
from pathlib import Path
from datetime import datetime

def run_conda_cmd(cmd, dry_run=False):
    full_cmd = ["conda"] + cmd
    if dry_run:
        full_cmd.insert(1, "--dry-run")
    print("Would run:", " ".join(full_cmd))
    # In real impl: subprocess.run(full_cmd, check=True) after confirmation

def get_conda_info():
    try:
        out = subprocess.check_output(["conda", "info", "--json"]).decode()
        return out
    except:
        return "Conda not found or error."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NeuroClaw Conda Environment Manager")
    parser.add_argument("--request", required=True, help="User request (create/export/update/remove...)")
    parser.add_argument("--dry-run", action="store_true", help="Only show plan")
    args = parser.parse_args()

    print("Conda snapshot:")
    print(get_conda_info()[:500], "...")  # truncated

    print("\nRequest:", args.request)
    print("Generating safe conda plan following NeuroClaw best practices...")
    print("Plan preview would appear here.")
    print("Waiting for explicit user confirmation before any real execution.")
```

## Important Notes & Limitations

- **User confirmation mandatory** — no silent destructive actions  
- Prefer `--from-history` exports for minimal, reproducible yml files  
- Large envs / CUDA stacks → warn about disk space & time  
- Windows users encouraged to use WSL2 for best compatibility  
- If mamba is detected, can suggest faster `mamba` drop-in replacement  
- Rollback: keep yml backups before major updates  
- Do **not** auto-activate envs — print instructions only (shell session safety)

## When to Call This Skill

- Any request containing “conda”, “environment”, “env create”, “yml”, “export env”  
- Before running deep-learning skills that require specific package versions  
- When dependency-planner detects conflicts best solved by new env  
- Reproducibility / sharing / team collaboration tasks  

## Complementary / Related Skills

- `dependency-planner`       → package installation after env creation  
- `multi-search-engine`      → lookup latest conda channel / solver advice  
- `git-essentials` / `git-workflows` → commit environment.yml  

## Reference & Source

Custom interface-layer skill for NeuroClaw, addressing environment setup gaps identified in MedicalClaw / OpenClaw reports and aligned with 2025–2026 conda best practices (isolated envs, yml reproducibility, dry-run safety).

Created At: 2026-03-19 01:45 HKT  
Last Updated At: 2026-03-19 01:45 HKT  
Author: chengwang96