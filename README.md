<div align="center">

# NeuroClaw: Data-and-Model Centric Platform for Neuroscience Research

<div align="center">

[Features](#key-features) • [Quick Start](#quick-start) • [Project Structure](#project-structure) • [Skills](#skill-quick-reference) • [Acknowledgments](#acknowledgments)

</div>

</div>


## 📖 Overview

**NeuroClaw** is a neuroscience-first platform built on the [OpenClaw](https://github.com/openclaw/openclaw) framework. Its core strength is **neuroimaging dataset and model adaptation**: turning raw scans into usable inputs quickly, and enabling medical practitioners to run deep learning models with minimal setup.

Neuroimaging datasets demand specialized preprocessing, and preprocessing quality directly determines model validity. Many workflows assume curated datasets, while MedicalClaw provides limited automation for open-source model execution (primarily large projects like TimesFM and AlphaFold), leaving users to spend significant time on environment configuration.

NeuroClaw prioritizes **data processing** and **model configuration/execution**. It remains an end-to-end Claw system, but for neuroscience its center of gravity is data and models.

---

## ✨ Key Features

### 🧠 End-to-End Research Coverage
- **Literature Review**: arXiv search, PubMed retrieval, academic resource integration
- **Experiment Design**: Scientific literature analysis, methodology evaluation, research proposal generation
- **Data Processing**: Multi-format conversion (DICOM ↔ NIfTI), automated preprocessing pipelines
- **Model Execution**: Run published research models, deep learning framework integration
- **Result Visualization**: Scientific data visualization, statistical chart generation
- **Paper Writing**: Auto-generated drafts, format standardization

### 🔄 Dataset-First Architecture
Organize capabilities around "which dataset to process" instead of "which tool to call":
- **ADNI Dataset** → Integrated ADNI standardized processing pipeline
- **UK Biobank** → Environment-aware deployment adaptation
- **Other Public Datasets** → Quick-start tool chains

Users simply specify the target dataset, and the system automatically recommends and orchestrates relevant skills.

### 🎯 Executability and Reproducibility
- **Automatic Dependency Management**: No manual installation needed; the system detects and resolves dependencies
- **True Model Execution**: Beyond sharing docs, it guides and executes model reproduction
- **Environment Isolation**: Virtual environments and containerization avoid system pollution
- **Verifiable Processes**: Complete logging and result tracking

### 🤝 OpenClaw Compatibility
- Fully compatible with [OpenClaw](https://github.com/openclaw/openclaw) framework, can be installed directly into existing OpenClaw environments
- skills, materials, USER.md, SOUL.md files integrate seamlessly
- No forced binding to specific versions or platforms

---

## 🚀 Quick Start

### Prerequisites
- Python >= 3.8
- OpenClaw framework installed
- Git

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-org/NeuroClaw.git
   cd NeuroClaw
   ```

2. **Integrate NeuroClaw into OpenClaw**
   ```bash
   # Assume OpenClaw workspace is at $OPENCLAW_HOME
   cp -r skills/* $OPENCLAW_HOME/skills/
   cp -r materials/* $OPENCLAW_HOME/materials/
   cp USER.md $OPENCLAW_HOME/
   cp SOUL.md $OPENCLAW_HOME/
   ```

3. **First Use: Automatic Environment Detection**
   
   After launching OpenClaw, the system automatically detects installed skills and dynamically installs dependencies as needed.

### Verify Installation
```bash
# View loaded neuroscience skills
openclaw list-skills | grep -i eeg
```

---

## 📁 Project Structure

```
NeuroClaw/
├── README.md                       # This file
├── USER.md                         # User-defined configurations and preferences
├── SOUL.md                         # System behavior guidelines and principles
├── skills/                         # Flat skill directory (logical grouping in docs)
│   ├── adni-skill/
│   ├── academic-research-hub/
│   ├── bids-organizer/
│   ├── claw-shell/
│   ├── conda-env-manager/
│   ├── conn-tool/
│   ├── dcm2nii/
│   ├── dependency-planner/
│   ├── dipy-tool/
│   ├── docker-env-manager/
│   ├── dti-skill/
│   ├── eeg-skill/
│   ├── experiment-controller/
│   ├── fmri-skill/
│   ├── fmriprep-tool/
│   ├── freesurfer-tool/
│   ├── fsl-tool/
│   ├── git-essentials/
│   ├── git-workflows/
│   ├── hcp-skill/
│   ├── hcppipeline-tool/
│   ├── method-design/
│   ├── mne-eeg-tool/
│   ├── multi-search-engine/
│   ├── nii2dcm/
│   ├── nilearn-tool/
│   ├── overleaf-skill/
│   ├── paper-writing/
│   ├── qsiprep-tool/
│   ├── research-idea/
│   ├── run_models/
│   ├── smri-skill/
│   └── wmh-segmentation/
│
├── materials/                      # Research materials and reference resources
│   └── CVPR_2026/
│
└── LICENSE                         # License

```

---

## 🛠️ Skill Quick Reference

### Base Layer
| Skill | Function | Status |
|------|----------|--------|
| `dcm2nii` | DICOM → NIfTI conversion with metadata support | ✅ |
| `nii2dcm` | NIfTI → DICOM conversion for clinical interoperability | ✅ |
| `git-essentials` | Core Git commands for collaboration | ✅ |
| `git-workflows` | Advanced Git workflows (rebase/worktree/bisect) | ✅ |
| `multi-search-engine` | Multi-engine web search without API keys | ✅ |
| `conda-env-manager` | Conda environment lifecycle management | ✅ |
| `docker-env-manager` | Docker environment management | ✅ |
| `dependency-planner` | Dependency planning and safe installation workflow | ✅ |
| `claw-shell` | Safe shell execution gateway via dedicated session | ✅ |
| `overleaf-skill` | Overleaf sync and collaborative manuscript operations | ✅ |
| `academic-research-hub` | Multi-source academic search and paper retrieval | ✅ |
| `bids-organizer` | Base skill for organizing raw data into BIDS structure | ✅ |
| `auto-qc` | Automated quality control for newly added skills | ⏳ |

### Interface Layer (Task Orchestration)
| Skill | Function | Status |
|------|----------|--------|
| `research-idea` | Brainstorms and generates research ideas from literature | ✅ |
| `method-design` | Formalizes network architecture and derives theoretical components | ✅ |
| `experiment-controller` | Finds and executes reproducible research experiments | ✅ |
| `paper-writing` | Generates hierarchical manuscript drafts from IDEA/METHOD/EXPERIMENT | ✅ |
| `run_models` | Model registry and model execution orchestration | ✅ |

### Subagent Layer
Subagent in NeuroClaw includes four categories: **tool**, **model**, **dataset**, and **modality**.

#### Tool
| Skill | Function | Status |
|------|----------|--------|
| `mne-eeg-tool` | Base-layer MNE-Python implementation for EEG | ✅ |
| `fsl-tool` | FSL-based sMRI/fMRI/DWI processing utilities | ✅ |
| `fmriprep-tool` | fMRIPrep pipeline wrapper and execution | ✅ |
| `qsiprep-tool` | qsiPrep pipeline wrapper for diffusion MRI | ✅ |
| `hcppipeline-tool` | HCP-style processing pipeline utilities | ✅ |
| `dipy-tool` | Diffusion MRI processing via DIPY | ✅ |
| `nilearn-tool` | Fast neuroimaging feature extraction and decoding prep | ✅ |
| `conn-tool` | Functional connectivity computation and analysis | ✅ |
| `freesurfer-tool` | FreeSurfer-based MRI processing and segmentation | ✅ |

#### Model
| Skill | Function | Status |
|------|----------|--------|
| `wmh-segmentation` | White matter hyperintensity segmentation (MARS-WMH nnU-Net) | ✅ |
| `brain_gnn` | BrainGNN: graph neural network for fMRI classification | ✅ |
| `fm_app` | FM-APP: multi-stage phenotype prediction with fMRI+sMRI | ✅ |

#### Dataset
| Skill | Function | Status |
|------|----------|--------|
| `adni-skill` | ADNI dataset automated processing workflow | ✅ |
| `hcp-skill` | HCP-YA dataset automated processing workflow | ✅ |
| `ukb-skill` | UKB brain imaging automated processing workflow | ⏳ |

#### Modality
| Skill | Function | Status |
|------|----------|--------|
| `eeg-skill` | EEG preprocessing and feature extraction workflows | ✅ |
| `fmri-skill` | Functional MRI preprocessing and analysis workflows | ✅ |
| `smri-skill` | Structural MRI preprocessing and analysis workflows | ✅ |
| `dti-skill` | Diffusion MRI preprocessing and analysis workflows | ✅ |

**Legend**: ✅ Implemented | 🏗️ In Development | ⏳ Planned


---

## TODO List

### Architecture & Foundation
- ✓ Hierarchical architecture design (Interface-Subagent-Base Tool)
- ✓ Complete Interface layer implementation
- ✓ Subagent coordination mechanisms
- ☐ Enhanced task orchestration

### Dataset Ecosystem
- ☐ Complete ADNI processing chain
- ✓ HCP dataset adaptation
- ☐ UK Biobank adaptation
- ☐ Multi-dataset workflow support

### Model Reproduction & Execution
- ✓ Automatic paper model retrieval
- ✓ Automatic environment configuration
- ☐ Reproducibility verification
- ☐ Model versioning and tracking

### Community & Extensions
- ☐ Multi-institution collaboration capabilities
- ☐ Plugin ecosystem for third-party skills

---


## 🙏 Acknowledgments

Thanks to:
- [OpenClaw](https://github.com/openclaw/openclaw) framework contributors
- All contributors and user feedback
- Open-source neuroscience tools community (MNE-Python, FreeSurfer, FSL, etc.)
