<div align="center">

# NeuroClaw: End-to-End Intelligent System for Neuroscience Research

<div align="center">

[Features](#key-features) • [Quick Start](#quick-start) • [Project Structure](#project-structure) • [Skills](#skill-quick-reference) • [Acknowledgments](#acknowledgments)

</div>

</div>


## 📖 Overview

**NeuroClaw** is an intelligent system for neuroscience research built upon the [OpenClaw](https://github.com/openclaw/openclaw) framework. It integrates a complete research workflow spanning literature review, experimental design, data processing, model execution, and result visualization. By combining intelligent agents with a hierarchical skill architecture, NeuroClaw aims to automate and accelerate neuroscience research.

NeuroClaw emphasizes **executability** and **dataset-driven** architecture design. Every skill has real production value, dependencies are automatically resolved, and skills can work together organically.

---

## ✨ Key Features

### 🧠 Complete Research Workflow Coverage
- **Literature Review**: arXiv search, PubMed retrieval, academic resource integration
- **Experiment Design**: Scientific literature analysis, methodology evaluation, research proposal generation
- **Data Processing**: Multi-format conversion support (DICOM ↔ NIfTI), automated preprocessing pipelines
- **Model Execution**: Run published research models, deep learning framework integration
- **Result Visualization**: Scientific data visualization, statistical chart generation
- **Paper Writing**: Auto-generated drafts, format standardization

### 🔄 Dataset-Driven Architecture
Prioritize organizing capabilities around "processing which dataset" rather than "calling which tool":
- **ADNI Dataset** → Integrated ADNI standardized processing pipeline
- **UK Biobank** → Environment-aware deployment adaptation
- **Other Public Datasets** → Quick-start tool chains

Users simply specify the target dataset, and the system automatically recommends and orchestrates relevant skills.

### 🎯 Executability and Reproducibility
- **Automatic Dependency Management**: No manual installation needed; system automatically detects and resolves dependencies
- **True Model Execution**: Not just sharing SKILL.md docs, but guiding and executing model reproduction
- **Environment Isolation**: Virtual environment and containerization support to avoid system pollution
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
│   ├── academic-research-hub/
│   ├── bids-organizer/
│   ├── claw-shell/
│   ├── conda-env-manager/
│   ├── conn-tool/
│   ├── dcm2nii/
│   ├── dependency-planner/
│   ├── dipy-tool/
│   ├── docker-env-manager/
│   ├── dwi-skill/
│   ├── eeg-skill/
│   ├── experiment-controller/
│   ├── fmri-skill/
│   ├── fmriprep-tool/
│   ├── freesurfer-tool/
│   ├── fsl-tool/
│   ├── git-essentials/
│   ├── git-workflows/
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
│   ├── smri-skill/
│   └── wmh-segmentation/
│
├── materials/                      # Research materials and reference resources
│   ├── datasets/                   # Public dataset descriptions and processing guides
│   ├── models/                     # Paper models and reproduction guides
│   └── documentation/              # Detailed technical documentation
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

#### Dataset
| Skill | Function | Status |
|------|----------|--------|
| `adni-skill` | ADNI dataset automated processing workflow | ⏳ |
| `hcp-skill` | HCP-YA dataset automated processing workflow | ⏳ |
| `ukb-skill` | UKB brain imaging automated processing workflow | ⏳ |

#### Modality
| Skill | Function | Status |
|------|----------|--------|
| `eeg-skill` | EEG preprocessing and feature extraction workflows | ✅ |
| `fmri-skill` | Functional MRI preprocessing and analysis workflows | ✅ |
| `smri-skill` | Structural MRI preprocessing and analysis workflows | 🏗️ |
| `dwi-skill` | Diffusion MRI preprocessing and analysis workflows | 🏗️ |

**Legend**: ✅ Implemented | 🏗️ In Development | ⏳ Planned


---

## TODO

### Architecture & Foundation
- ✓ Hierarchical architecture design (Interface-Subagent-Base Tool)
- ☐ Complete Interface layer implementation
- ☐ Subagent coordination mechanisms
- ☐ Enhanced task orchestration

### Dataset Ecosystem
- ☐ Complete ADNI processing chain
- ☐ UK Biobank adaptation
- ☐ Public dataset navigation and discovery
- ☐ Multi-dataset workflow support

### Model Reproduction & Execution
- ☐ Automatic paper model retrieval
- ☐ Automatic environment configuration
- ☐ Reproducibility verification
- ☐ Model versioning and tracking

### Community & Extensions
- ☐ Community-contributed skill marketplace
- ☐ Multi-institution collaboration capabilities
- ☐ Plugin ecosystem for third-party skills
- ☐ Domain-specific extensions

---


## 🙏 Acknowledgments

Thanks to:
- [OpenClaw](https://github.com/openclaw/openclaw) framework contributors
- All contributors and user feedback
- Open-source neuroscience tools community (MNE-Python, FreeSurfer, FSL, etc.)
