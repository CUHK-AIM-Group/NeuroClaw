# NeuroClaw: End-to-End Intelligent System for Neuroscience Research

<div align="center">

**An end-to-end intelligent agent system for neuroscience research workflows**

[Features](#key-features) • [Quick Start](#quick-start) • [Project Structure](#project-structure) • [Skills](#skill-quick-reference) • [Acknowledgments](#acknowledgments)

</div>

---

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
├── skills/                         # Skill collection (hierarchical architecture)
│   ├── [interface-skills]/         # Interface layer skills
│   │   ├── task-planner/
│   │   ├── dependency-manager/
│   │   └── skill-discovery/
│   │
│   ├── [subagent-skills]/          # Subagent layer skills
│   │   ├── research-workflow/
│   │   ├── experiment-design/
│   │   ├── data-processing-pipeline/
│   │   └── model-execution/
│   │
│   └── [base-tool-skills]/         # Base tool layer skills
│       ├── file-operations/
│       ├── data-conversion/
│       ├── eeg-processing/
│       └── ...
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

### Interface Layer (Task Orchestration & Environment Management)
| Skill | Function | Status |
|------|----------|--------|
| `dependency-planner` | Plans and manages all dependency installations with safety checks | ✅ |
| `claw-shell` | Central safe shell execution layer for all commands | ✅ |
| `conda-env-manager` | Creates, manages, and exports isolated conda environments | ✅ |
| `research-idea` | Brainstorms and generates research ideas from literature | ✅ |
| `method-design` | Formalizes network architecture and derives theoretical components | ✅ |
| `experiment-controller` | Finds and executes reproducible research experiments | ✅ |
| `paper-writing` | Generates hierarchical manuscript drafts from IDEA/METHOD/EXPERIMENT | ✅ |
| `overleaf-skill` | Syncs LaTeX manuscripts to Overleaf with version control | ✅ |

### Subagent & Modality Layer (Research Workflows)
| Skill | Function | Status |
|------|----------|--------|
| `eeg-skill` | EEG data loading, preprocessing, feature extraction | ✅ |
| `mne-eeg-tool` | Base-layer MNE-Python implementation for EEG | ✅ |
| `freesurfer-skill` | Automated brain surface segmentation and parcellation | ✅ |
| `wmh-segmentation` | White matter hyperintensity segmentation (MARS-WMH nnU-Net) | ✅ |

### Data Conversion & Format Tools
| Skill | Function | Status |
|------|----------|--------|
| `dcm2nii` | DICOM → NIfTI conversion with quality validation | ✅ |
| `nii2dcm` | NIfTI → DICOM conversion with metadata preservation | ✅ |

### Literature & Knowledge Search
| Skill | Function | Status |
|------|----------|--------|
| `academic-research-hub` | Multi-source academic paper search and download | ✅ |
| `arxiv-cli-tools` | Command-line interface for arXiv search and retrieval | ✅ |
| `multi-search-engine` | Multi-engine web search (17 engines, no API keys needed) | ✅ |

### Version Control & Collaboration
| Skill | Function | Status |
|------|----------|--------|
| `git-essentials` | Basic Git workflows: clone, commit, push, branch | ✅ |
| `git-workflows` | Advanced Git operations: rebase, bisect, worktree, reflog | ✅ |

**Legend**: ✅ Implemented | 🏗️ In Development | ⏳ Planned


---

## Acknowledgment

**NeuroClaw** design is inspired by the following systems and research:
- **[OpenClaw](https://github.com/openclaw/openclaw)**: Open-source agent framework foundation
- **BioClaw / STELLA**: Self-Evolving LLM Agents
- **ClawBio**: End-to-end biological research system (lessons learned while maintaining compatibility)

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
