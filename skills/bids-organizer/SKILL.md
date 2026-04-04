---
name: bids-organizer
description: "Use this skill whenever the user wants to automatically organize raw neuroimaging data (DICOM, NIfTI, EEG, etc.) into a valid BIDS (Brain Imaging Data Structure) dataset. Triggers include: 'organize to BIDS', 'BIDS organizer', 'convert to BIDS', 'BIDS conversion', 'bidsify', 'create BIDS dataset', 'raw data to BIDS', or any request to structure data according to BIDS specification."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# BIDS Organizer

## Overview

BIDS Organizer is the NeuroClaw interface-layer skill that automatically converts raw or semi-organized neuroimaging data into a standardized BIDS-compliant dataset.

It supports DICOM → NIfTI conversion + BIDS naming, existing NIfTI reorganization, EEG (.set/.edf/.bdf/.fif), and basic metadata handling. The skill generates a clear execution plan, waits for user confirmation, then delegates all heavy work to appropriate base tools.

**Core workflow (never bypassed):**
1. Scan input directory and detect data types (DICOM, NIfTI, EEG, etc.).
2. Generate a numbered execution plan with proposed BIDS structure and subject/session labels.
3. Present the plan, estimated time, and risks; wait for explicit confirmation (“YES” / “execute” / “proceed”).
4. On confirmation, delegate tasks to `dcm2nii`, `mne-eeg-tool`, and `claw-shell`.
5. After completion, run BIDS validation and generate a summary report.

**Research use only.**

## Quick Reference

| Task                              | What needs to be done                                      | Delegate to which tool skill          | Expected output                     |
|-----------------------------------|------------------------------------------------------------|---------------------------------------|-------------------------------------|
| DICOM to BIDS                     | Convert DICOM → NIfTI + apply BIDS naming                  | `dcm2nii` + `claw-shell`              | BIDS-compliant NIfTI + JSON sidecars|
| Existing NIfTI to BIDS            | Rename and reorganize NIfTI files into BIDS hierarchy      | `claw-shell`                          | Properly named BIDS dataset         |
| EEG to BIDS                       | Convert .set/.edf/.bdf/.fif to BIDS EEG format             | `mne-eeg-tool` + `claw-shell`         | BIDS EEG files + events             |
| Create dataset_description.json   | Generate required BIDS metadata files                      | `claw-shell`                          | dataset_description.json            |
| Validate BIDS dataset             | Run bids-validator and generate report                     | `claw-shell`                          | validation report                   |
| Full automatic organization       | End-to-end raw data → valid BIDS dataset                   | All above tools                       | Complete BIDS dataset + QC report   |

## Common Shell Command Examples

```bash
# DICOM to BIDS (most common)
dcm2niix -o ./bids/sub-001/ses-01/anat -f "%p_%s" -b y -z y /path/to/dicom/T1

# Validate the resulting BIDS dataset
bids-validator /path/to/bids_dataset
```

## Installation (Handled by dependency-planner)

Use `dependency-planner` with requests such as:
- “Install dcm2niix and bids-validator”
- “Install MNE-Python for EEG to BIDS conversion”

After installation, verify with:
```bash
dcm2niix --version
bids-validator --version
```

## NeuroClaw recommended wrapper script

```python
# bids_organizer_wrapper.py (placed inside the skill folder for reference)
import subprocess
from pathlib import Path

def organize_to_bids(raw_dir, bids_dir, subject_id, session_id="01"):
    bids_dir = Path(bids_dir)
    bids_dir.mkdir(parents=True, exist_ok=True)
    
    # DICOM to BIDS example
    cmd = [
        "dcm2niix", "-o", str(bids_dir / f"sub-{subject_id}" / f"ses-{session_id}" / "anat"),
        "-f", "%p_%s", "-b", "y", "-z", "y", str(raw_dir)
    ]
    
    print("Executing:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    
    # Create basic dataset_description.json
    desc = {
        "Name": "NeuroClaw BIDS Dataset",
        "BIDSVersion": "1.8.0",
        "DatasetType": "raw"
    }
    (bids_dir / "dataset_description.json").write_text(str(desc))
    
    print(f"BIDS dataset created at: {bids_dir}")
```

## Important Notes & Limitations

- This skill only generates the plan and delegates; actual file operations are performed via `claw-shell`.
- DICOM conversion relies on `dcm2nii`.
- EEG conversion is delegated to `mne-eeg-tool`.
- Always review the proposed BIDS structure (subject/session labels, run numbers) before confirmation.
- Large datasets may require significant disk space and time.

## When to Call This Skill

- Raw scanner data (DICOM) needs to be converted and organized into BIDS
- Existing NIfTI/EEG files need proper BIDS naming and folder structure
- Preparing data for `fmriprep-tool`, `hcppipeline-tool`, `fsl-tool`, or `fmri-skill`
- Before running any standardized preprocessing pipeline

## Post-Execution Verification (Harness Integration)

After BIDS organization completes, this skill **automatically invokes harness-core's VerificationRunner** to validate output integrity:

**Integrated verification checks**:

```python
from skills.harness_core import VerificationRunner, AuditLogger

verifier = VerificationRunner(task_type="bids_organization")

# 1. BIDS structure compliance
verifier.add_check("bids_structure", 
    checker=lambda: verify_bids_structure(bids_dir),
    severity="error"
)

# 2. Dataset description file
verifier.add_check("dataset_description",
    checker=lambda: verify_dataset_description_exists(bids_dir),
    severity="error"
)

# 3. Subject/session naming convention
verifier.add_check("naming_convention",
    checker=lambda: verify_bids_naming(bids_dir),
    severity="error"
)

# 4. Metadata JSON sidecar completeness
verifier.add_check("json_sidecars",
    checker=lambda: verify_json_sidecars(bids_dir),
    severity="warning"
)

# 5. Required BIDS files presence
verifier.add_check("required_files",
    checker=lambda: verify_required_files(bids_dir),
    severity="error"
)

report = verifier.run(bids_dir)

# Log verification results
logger = AuditLogger(log_file=f"{bids_dir}/bids_verification.jsonl")
logger.log_validation(
    task_name="bids_organization",
    checks_passed=len([r for r in report.results if r.passed]),
    checks_failed=len([r for r in report.results if not r.passed]),
    warnings=len([r for r in report.results if r.severity == "warning" and not r.passed]),
    report_summary=report.to_dict()
)

if report.failed:
    raise ValueError(f"BIDS verification failed: {report.summary}")
```

**Output files generated**:
- `{bids_dir}/bids_verification.jsonl` — structured audit log
- `{bids_dir}/.bids_validation_timestamp` — verification completion marker

## Complementary / Related Skills

- `dependency-planner` → install required tools
- `claw-shell` → safe execution of all commands
- `harness-core` → automated verification and audit logging

## More Advanced Features

For complex BIDS cases (multi-session, multi-run, custom metadata, HEUDICONV heuristics, etc.), please refer to the official BIDS specification:

- Official BIDS Website: https://bids.neuroimaging.io/
- BIDS Specification: https://bids-specification.readthedocs.io/

You may use the `multi-search-engine` or `academic-research-hub` skill to find the latest BIDS conversion best practices.

---
Created At: 2026-03-25 16:00 HKT  
Last Updated At: 2026-04-05 02:01 HKT
Author: chengwang96