---

name: experiment-controller
description: "Use this skill whenever the user wants to execute experiments based on a finalized method and record results. Triggers include: 'run experiment', 'experiment controller', 'implement experiment', 'run model', 'execute training', 'experiment-controller', 'record results', 'ablation study', or any request to turn METHOD.md into concrete runs and output to EXPERIMENT.md. This skill is the **mandatory interface-layer experiment executor** in NeuroClaw: it searches literature/GitHub for matching experimental setups and codebases, proposes one scheme + repo after user discussion, uses git skills to download and setup, runs the experiment(s), and iteratively appends every result + observation to EXPERIMENT.md."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)

---

# Experiment Controller
## Overview
This skill implements the **Literature/GitHub Search → Scheme Confirmation → Git Execution → Iterative Logging** process for the NeuroClaw experiment-controller phase.

It acts as the Experiment Manager within the multi-agent framework:
- Reads the latest **IDEA.md** and **METHOD.md** from the workspace.
- Searches recent literature (multi-search-engine, arxiv-search, pubmed-search) and GitHub for reproducible experimental setups and open-source repositories that match the proposed architecture.
- Summarizes candidate schemes (hyperparameters, datasets, baselines, training protocols) and proposes the most suitable GitHub repo.
- Iteratively discusses with the user to confirm the exact scheme/repo.
- After confirmation: uses git-essentials/git-workflows to clone, dependency-planner to install environment, claw-shell to run the experiment (training/inference/ablation).
- After every run (or ablation), automatically records: setup details, metrics, logs, observations, and any issues.
- Saves everything in **EXPERIMENT.md** (with dated sections for each run).

**Research use only** — the output is a complete, reproducible EXPERIMENT.md ready for paper-writing and future replication.

## Quick Reference (Experiment Flow)
| Step | Description                              | Output File               |
|------|------------------------------------------|---------------------------|
| 1. Read & Parse | Load IDEA.md + METHOD.md                | 01_idea_method_summary.md |
| 2. Literature & GitHub Search | Find matching setups & repos            | 02_search_results.md      |
| 3. Proposal | Recommend best scheme + repo            | 03_proposal.md            |
| 4. User Discussion | Confirm scheme/repo                     | 04_discussion.md          |
| 5. Git Clone & Setup | Clone + install dependencies            | 05_setup_log.md           |
| 6. Run Experiment | Execute training/inference/ablation     | 06_run_log_*.md (per run) |
| 7. Record Results | Append metrics + observations           | EXPERIMENT.md             |

## Installation
```bash
# Place files in: skills/experiment-controller/
```

## Important Notes & Limitations
- Always starts from latest IDEA.md + METHOD.md; stops and prompts if missing.
- Every step and every run is saved as numbered Markdown files for full transparency and resumption.
- Git clone uses git-essentials/git-workflows (never manual commands outside skills).
- Dependencies are handled exclusively by dependency-planner.
- Multiple runs (e.g., ablations) are supported; results are appended with timestamps.
- Final output always saved/updated as `EXPERIMENT.md` in workspace root.
- Logs include: command executed, hyperparameters, metrics (accuracy, loss, Dice, etc.), runtime, observations, and any errors.

## When to Call This Skill
- Immediately after method-design completes METHOD.md
- When the user wants to run, reproduce, or compare experiments
- Before paper-writing (to populate quantitative results)

## Complementary / Related Skills
- `research-idea` → provides IDEA.md
- `method-design` → provides METHOD.md (input)
- `multi-search-engine` → literature & GitHub search
- `git-essentials` / `git-workflows` → clone and manage repositories
- `dependency-planner` → environment & dependency installation
- `claw-shell` → internal execution of training scripts
- `paper-writing` → consumes EXPERIMENT.md for results/tables

## Reference & Source
NeuroClaw architecture (section 1.7 experiment-controller skill).  
Flow: literature/GitHub search → user-confirmed scheme → git clone → dependency setup → iterative execution → EXPERIMENT.md logging.  
Created At: 2026-03-24  
Last Updated At: 2026-03-24  
Author: chengwang96