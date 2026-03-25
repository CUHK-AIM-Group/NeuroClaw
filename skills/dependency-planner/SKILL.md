---

name: dependency-planner  
description: "Use this skill whenever a NeuroClaw skill, model, or sub-agent reports a missing dependency (e.g. ImportError, ModuleNotFoundError, command not found), or when the user explicitly requests to install, setup, configure, or fix any library, package, compiler, CUDA toolkit, conda environment, system tool, or git-based repository. Triggers include: 'install', 'setup', 'missing dependency', 'fix import error', 'install torch cuda', 'conda create environment', 'pip install from git', 'install nnU-Net', 'setup gcc nvcc', 'prepare environment for deep learning', 'handle dep error', or any phrase indicating the need to prepare or install software components. This skill is the **mandatory gatekeeper**: it ALWAYS plans first, never installs anything without explicit user confirmation."  
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)  

---

# Dependency Installation Planner

## Overview

Many NeuroClaw skills (especially deep-learning, neuroimaging, and custom model execution skills) fail due to missing dependencies — a key pain point identified in the MedicalClaw / OpenClaw-Medical-Skills evaluation.  

This skill acts as the **interface-layer planner** that ensures safe, reproducible, auditable, and user-approved installations across the entire NeuroClaw hierarchy (interface → subagent → base tool).

**Strict workflow (never bypassed):**

1. Parse the exact dependency/dependencies from the user request or error message.
2. Automatically detect the local environment: OS family & version, architecture, Python version, conda/pip/virtualenv status, GCC version, NVCC/CUDA version (if GPU-relevant), available disk space & RAM.
3. For each required package/tool, invoke the already-existing `multi-search-engine` skill (with **Google search priority**) to retrieve the **latest official installation instructions** from the authoritative source (e.g. pytorch.org, conda-forge, nvidia.com, github.com releases page, official docs).
4. Perform compatibility analysis against the detected local system (CUDA/driver match, Python version support, gcc/nvcc requirements, OS limitations) and highlight potential failure risks (version conflict, missing sudo, large download, Windows WSL issues, etc.).
5. Construct a clear, numbered, executable step-by-step plan, routing git-based installations through `git-essentials` and `git-workflows` when needed.
6. Present the full plan, estimated time/size, risks, and exact commands to the user → wait for explicit confirmation (“YES”, “execute”, “proceed”, etc.).
7. On confirmation: execute the plan safely (using conda/pip wrappers, environment isolation, logging), capture output, and provide success/failure report + rollback suggestions.

**Core safety principles**  
- Never install silently  
- Prefer conda / virtual environments over global installs  
- Always version-pin where possible  
- Log every command and output  
- Offer dry-run / plan-only mode  
- Integrate tightly with NeuroClaw’s self-evolution and safety strategy

## Quick Reference

| Task                                | Recommended Strategy (after detection + multi-search-engine)                     |
|-------------------------------------|-----------------------------------------------------------------------------------|
| Install PyTorch with correct CUDA   | Detect nvcc → search “pytorch get started locally cuda XX.X” → use exact wheel   |
| Git + pip install from source       | git-essentials clone → git-workflows checkout → pip install -e . or setup.py     |
| Create isolated conda environment   | Match Python version → `conda create -n neuroclaw-xxx python=X.Y` → bulk install |
| System-level package (Linux/macOS)  | Detect OS → search official guide → apt/brew/yum/dnf install                     |
| CUDA Toolkit / cuDNN                | Strict version match to nvcc → official NVIDIA installer instructions            |
| Large/risky installs (FSL, ANTs, nnU-Net) | Warn about size/time, suggest --dry-run or offline mirror first                 |

## Installation

This skill is **pure Python orchestration** — it has no external binary dependencies beyond already-available NeuroClaw skills.

**Required prerequisites (must exist before this skill can be used):**

- `multi-search-engine` (for Google-first official documentation lookup)
- `git-essentials` & `git-workflows` (for any source-code cloning & branch management)
- Basic shell/subprocess access

To register in NeuroClaw:

```bash
# Place files in: skills/dependency-planner/
# Update SOUL.md and/or USER.md to include trigger phrases and skill name
```

## Usage Examples

### Example 1: “My model says torch is missing and I have an RTX 4090”

```text
# Internal flow:
# 1. Detect: nvcc --version → CUDA 12.4
# 2. multi-search-engine query: "pytorch official installation cuda 12.4 conda"
# 3. Generated plan:
Step 1: conda create -n neuroclaw-dl python=3.11 -y
Step 2: conda activate neuroclaw-dl
Step 3: conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
Risk: low (version match confirmed)
Estimated time: ~8 min
# 4. Prompt: “Execute this plan? Reply YES to proceed.”
```

### Example 2: “Install latest nnU-Net from github for segmentation skill”

```text
# Flow:
# 1. Detects git requirement
# 2. Uses git-essentials to clone https://github.com/MIC-DKFZ/nnUNet
# 3. multi-search-engine: "nnunetv2 install from source latest"
# 4. Plan:
Step 1: git clone https://github.com/MIC-DKFZ/nnUNet.git
Step 2: cd nnUNet && git checkout latest_release_tag
Step 3: pip install -e .
Risk: medium (may conflict with existing torch)
```

## NeuroClaw recommended wrapper script (placed inside the skill folder)

```python
# dependency_planner.py
import subprocess
import platform
import argparse
import sys
from pathlib import Path

def get_system_info():
    info = {}
    info["os"] = platform.system() + " " + platform.release()
    info["machine"] = platform.machine()
    info["python"] = sys.version.split()[0]
    try:
        info["gcc"] = subprocess.check_output(["gcc", "--version"]).decode().splitlines()[0].strip()
    except:
        info["gcc"] = "Not found"
    try:
        info["nvcc"] = subprocess.check_output(["nvcc", "--version"]).decode().splitlines()[0].strip()
    except:
        info["nvcc"] = "Not found"
    return info

# In real implementation, this would call multi-search-engine via agent API / subprocess
def placeholder_search_instructions(dep_name):
    return f"(Simulated) Official instructions for {dep_name} retrieved from Google."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NeuroClaw Dependency Planner")
    parser.add_argument("--request", required=True, help="User request or error message")
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()

    sys_info = get_system_info()
    print("System snapshot:")
    for k, v in sys_info.items():
        print(f"  {k:10}: {v}")

    print("\nPlanning dependencies for:", args.request)
    print("→ Invoking multi-search-engine for official instructions...")
    print("→ Compatibility check in progress...")
    print("\nPlan would be presented here + user confirmation step.")
    if not args.plan_only:
        print("Awaiting explicit user confirmation before any execution.")
```

## Important Notes & Limitations

- **User confirmation is mandatory** — no auto-execution
- Full transcript saved: `./logs/install_YYYYMMDD_HHMMSS.log`
- CUDA installs are **strictly version-matched** to prevent driver/kernel panics
- Windows support exists but **strongly recommends WSL2** for serious NeuroClaw usage
- Large downloads include size/time estimate + warning
- Rollback support: conda env export, git stash / reset
- Git operations are always delegated to `git-essentials` / `git-workflows`

## When to Call This Skill

- Any error contains “No module”, “command not found”, “missing”, “dependency”
- User says “install”, “setup”, “prepare environment”, “fix”
- Before activating deep-learning, model-training, or compiled-tool skills
- When `scientific-brainstorming` or `deep-research` recommends new software

## Complementary / Related Skills

- `multi-search-engine`        → official docs retrieval (Google priority)
- `git-essentials` / `git-workflows` → source code management
- `conda-env-manager`                → planned subagent for env creation & export

## Reference & Source

Custom interface-layer skill created for NeuroClaw to close the dependency-management gap highlighted in the MedicalClaw / OpenClaw evaluation report.

Created At: 2026-03-19 01:15 HKT  
Last Updated At: 2026-03-19 01:15 HKT  
Author: chengwang96