---
name: docker-env-manager
description: "Use this skill whenever the user wants to pull, run, build, compose, list, prune, manage, or otherwise handle Docker containers, images, volumes, networks, or Docker Compose projects, or when a NeuroClaw skill (e.g. wmh-segmentation, freesurfer-processor in container mode) requires a clean, isolated, GPU-enabled Docker environment (e.g. 'pull mars-wmh image', 'run container with GPU', 'docker compose up', 'prune unused images', 'build custom dockerfile', 'manage nvidia docker'). Triggers include: 'docker run', 'docker pull', 'docker compose', 'docker build', 'docker env', 'manage container', 'nvidia docker', 'pull image', 'docker prune', 'containerize'. This skill is the **mandatory gatekeeper for all Docker operations** in NeuroClaw: it ALWAYS plans first, shows commands + risks + best practices, and waits for explicit user confirmation before executing anything. All actual Docker execution is routed through `claw-shell`."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# Docker Environment Manager

## Overview

Docker is the backbone for reproducible, containerized, GPU-accelerated environments in NeuroClaw — especially for deep-learning and neuroimaging skills (MARS-WMH nnU-Net, future nnU-Net models, containerized FreeSurfer, etc.) that require exact runtime isolation, NVIDIA GPU passthrough, and large pre-built images.

This skill acts as the **interface-layer orchestrator** for all common Docker operations, preventing permission issues, GPU misconfiguration, port conflicts, and storage bloat while enforcing best practices (named containers, volume mounts, `--gpus all`, docker-compose for multi-service stacks, dry-run previews, and safe pruning).

**Strict workflow (never skipped):**
1. Parse user intent from the request or context (pull / run / build / compose / prune / list / cleanup).
2. Detect current Docker setup (`docker --version`, `docker info`, NVIDIA Container Toolkit via `nvidia-smi` through `claw-shell`, available disk space, GPU status).
3. Propose a safe, best-practice plan:
   - Always prefer named containers/volumes over anonymous ones
   - Suggest `--gpus all` + volume mounts for NeuroClaw GPU skills
   - Recommend `docker-compose.yml` for reproducible multi-container stacks
   - Use `--dry-run` equivalents and plan preview by default
   - Warn about large image pulls (several GB), permission issues (`chmod -R 777` on data dirs), and GPU driver mismatches
   - Route **all** actual `docker run/pull/build` commands through `claw-shell`
4. Show numbered plan + exact commands + estimated time/size + risks.
5. Wait for explicit user confirmation (“YES”, “execute”, “proceed”).
6. On approval: delegate execution safely to `claw-shell` (with logging), capture output, report success/failure, and suggest next steps.

**Core safety & best-practice rules**
- Never run destructive commands (`docker system prune -a`, `docker rm -f`) without double confirmation
- All shell-level Docker commands **must** go through `claw-shell` (centralized logging + safety gate)
- Prefer `docker compose` over legacy `docker-compose`
- Integrate with `dependency-planner` for installing Docker + NVIDIA Container Toolkit
- Log all actions to `./logs/docker_YYYYMMDD_HHMMSS.log`

## Quick Reference (Common NeuroClaw Tasks)

| Task                                      | Recommended Approach (after user confirmation)                          |
|-------------------------------------------|-------------------------------------------------------------------------|
| Pull latest model image                   | `docker pull ghcr.io/miac-research/wmh-nnunet:latest` (then tag)       |
| Run GPU container with data mount         | `docker run --rm --gpus all -v $(pwd)/data:/data image ...`            |
| Docker Compose stack                      | `docker compose -f docker-compose.yml up -d`                           |
| Build custom Dockerfile                   | `docker build -t neuroclaw-custom .`                                   |
| List containers / images                  | `docker ps -a` / `docker images`                                       |
| Safe cleanup of unused resources          | `docker system prune --dry-run` → confirm → execute via claw-shell     |
| Fix common permission issues              | `chmod -R 777 output_dir` (auto-included in plans)                     |
| GPU check & NVIDIA Toolkit install        | Hand over to `dependency-planner` if `nvidia-smi` fails               |

## Installation

This skill is pure Python orchestration — no external binaries needed beyond a working Docker installation.

**Required prerequisites (must exist before activation):**
- Working Docker Engine (with NVIDIA Container Toolkit for GPU skills)
- `claw-shell` (mandatory — all Docker commands are routed here)
- `dependency-planner` (recommended companion for installing Docker + NVIDIA Container Toolkit)
- Basic shell access

To register in NeuroClaw:
```bash
# Place files in: skills/docker-env-manager/
# Update SOUL.md and/or USER.md with trigger phrases
```

## NeuroClaw recommended wrapper script

```python
# docker_env_manager.py
import subprocess
import argparse
import sys
from pathlib import Path
from datetime import datetime

def run_docker_cmd(cmd, dry_run=False):
    full_cmd = ["docker"] + cmd
    print("Would run (via claw-shell):", " ".join(full_cmd))
    # In real implementation: delegate to claw-shell skill after user confirmation
    # e.g. tool_call("claw_shell_run", {"command": " ".join(full_cmd)})

def get_docker_info():
    try:
        version = subprocess.check_output(["docker", "--version"]).decode().strip()
        info = subprocess.check_output(["docker", "info", "--format", "{{.ServerVersion}}"]).decode().strip()
        return f"Docker {version} | Engine {info}"
    except:
        return "Docker not found or error."

def check_gpu():
    try:
        return subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"]).decode().strip()
    except:
        return "No NVIDIA GPU detected or NVIDIA Container Toolkit missing"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NeuroClaw Docker Environment Manager")
    parser.add_argument("--request", required=True, help="User request (pull/run/compose/prune...)")
    parser.add_argument("--dry-run", action="store_true", help="Only show plan")
    args = parser.parse_args()

    print("Docker snapshot:")
    print(get_docker_info())
    print("GPU status:", check_gpu())

    print("\nRequest:", args.request)
    print("Generating safe Docker plan following NeuroClaw best practices...")
    print("All execution will be routed through claw-shell.")
    print("Plan preview would appear here.")
    print("Waiting for explicit user confirmation before any real execution.")
```

## Important Notes & Limitations

- **User confirmation is mandatory** — no silent destructive actions
- All actual Docker commands are **delegated to `claw-shell`** for centralized logging and safety
- Large image pulls (e.g. nnU-Net models) → warn about size/time and disk space
- Common fixes (`chmod -R 777` on mounted directories, `newgrp docker`) are automatically included in plans
- Windows users are encouraged to use WSL2 + Docker Desktop for best compatibility
- GPU passthrough requires NVIDIA Container Toolkit (installed via `dependency-planner`)
- Rollback support: keep `docker-compose.yml` + image tags as backups

## When to Call This Skill

- Any request containing “docker”, “container”, “pull image”, “run with GPU”, “docker compose”, “prune”, “build Dockerfile”
- Before running Docker-based skills (wmh-segmentation, future containerized models)
- When `dependency-planner` detects missing Docker/NVIDIA toolkit
- Reproducibility, sharing, or team collaboration tasks involving containers

## Complementary / Related Skills

- `claw-shell` → **mandatory** safe execution of all Docker commands (tmux `claw` session)
- `dependency-planner` → install Docker Engine + NVIDIA Container Toolkit
- `multi-search-engine` → lookup latest Docker Hub / GitHub Container Registry instructions
- `git-essentials` / `git-workflows` → clone repositories containing Dockerfiles

## Reference & Source

Custom interface-layer skill for NeuroClaw, addressing containerized environment setup gaps identified in the MedicalClaw / OpenClaw evaluation and aligned with 2026 Docker + NVIDIA best practices (GPU passthrough, compose reproducibility, claw-shell routing).

---
Created At: 2026-03-25 23:08 HKT  
Last Updated At: 2026-03-25 23:08 HKT  
Author: Cheng Wang