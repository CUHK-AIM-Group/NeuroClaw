<div align="center">

<img src="materials/logo.png" alt="NeuroClaw Logo" width="200" />

# NeuroClaw: From Raw Brain Data to Auditable Experiment Loops

[中文版 README](README_zh.md)

<div align="center">

[Features](#-key-features) • [Quick Start](#-quick-start) • [Project Structure](#-project-structure) • [Skills](#%EF%B8%8F-skill-quick-reference) • [Acknowledgments](#-acknowledgments)

</div>

</div>


## 📖 Overview

**NeuroClaw** is a neuroscience-first platform built on the [OpenClaw](https://github.com/openclaw/openclaw) framework. Its core strength is **neuroimaging dataset and model adaptation**: turning raw scans into usable inputs quickly, and enabling medical practitioners to run deep learning models with minimal setup.

Neuroimaging datasets demand specialized preprocessing, and preprocessing quality directly determines model validity. Many workflows assume curated datasets, while MedicalClaw provides limited automation for open-source model execution (primarily large projects like TimesFM and AlphaFold), leaving users to spend significant time on environment configuration.

NeuroClaw prioritizes **data processing** and **model configuration/execution**. It remains an end-to-end Claw system, but for neuroscience its center of gravity is data and models.

**Notes**
- We constructed **NeuroBench** to benchmark multi-agent performance across neuroimaging workflows, especially raw data processing and model execution, and plan to refine and evaluate existing medical and general claw systems.
- Each SKILL.md ends with the author information; please open an issue to the corresponding author if you have questions.


## 🚀 Updates

- **[2026.04.22]**: v1.0 released — stable release with improvements and full documentation.
- **[2026.04.17]**: Our project homepage is now live. Welcome to visit: https://cuhk-aim-group.github.io/NeuroClaw/
- **[2026.04.15]**: Added CLI batch benchmark execution, expanded benchmark metrics and scoring utilities.
- **[2026.04.08]**: We have completed the dataset part of NeuroBench; our NeuroClaw now runs independently and offers a Web UI.
- **[2026.04.06]**: We begin constructing NeuroBench for multi-agent framework evaluation.
- **[2026.04.02]**: v0.1 released with complete NeuroClaw framework and core functionality.

<a id="key-features"></a>
## ✨ Key Features

<div align="center">
  <img src="materials/framework.png" alt="NeuroClaw Framework Overview" style="width: 95%; max-width: 100%;" />
</div>

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

### 🧠 End-to-End Research Coverage
- **Literature Review**: arXiv search, PubMed retrieval, academic resource integration
- **Experiment Design**: Scientific literature analysis, methodology evaluation, research proposal generation
- **Data Processing**: Multi-format conversion (DICOM ↔ NIfTI), automated preprocessing pipelines
- **Model Execution**: Run published research models, deep learning framework integration
- **Result Visualization**: Scientific data visualization, statistical chart generation
- **Paper Writing**: Auto-generated drafts, format standardization

### 🤝 OpenClaw Compatibility
- **NeuroClaw is now self-contained** — OpenClaw does not need to be installed separately.
  The bundled `core/` engine provides the same agent loop, skill loader, and tool runtime.
- `skills/`, `materials/`, `USER.md`, and `SOUL.md` remain fully compatible with existing
  OpenClaw workspaces if you still want to use NeuroClaw as an add-on.
- Non-neuroscience connectors (WhatsApp, Telegram, Slack, calendar, e-commerce, SaaS auth)
  are disabled by default via `core/config/features.json` and can be re-enabled if needed.

---

<a id="quick-start"></a>
## 🚀 Quick Start

### Prerequisites
- Python >= 3.10
- Git
- *(Optional)* Conda/Mamba for environment isolation
- *(Optional)* `nvidia-smi` / `nvcc` for GPU support
- *(Recommended for Web UI attachments)* `pypdf`, `python-docx`, `openpyxl`, `python-pptx`

> **NeuroClaw is now self-contained** — OpenClaw does not need to be installed separately.
> The bundled installer configures everything, including your Python environment,
> CUDA version, neuroimaging toolchain, and LLM backend.

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/CUHK-AIM-Group/NeuroClaw.git
   cd NeuroClaw
   ```

2. **Run the Setup Wizard**
   ```bash
   python installer/setup.py
   ```
  The wizard will walk you through:
  - Python runtime (system / conda / Docker)
  - CUDA / GPU configuration and optional PyTorch install
  - Neuroscience toolchain paths (FSL, FreeSurfer, dcm2niix, etc.)
  - LLM backend selection (OpenAI, Anthropic, or local model)
  - Default BIDS and output directories
  - Web UI dependencies and attachment parsers (PDF/DOCX/XLSX/PPTX)

   Settings are saved to `neuroclaw_environment.json` and loaded automatically on every future session.
   Setup does not ask for an API key. Pass the key only at runtime with `--api-key`, or export the configured environment variable before startup.

   For a quick non-interactive setup with auto-detected defaults:
   ```bash
   python installer/setup.py --non-interactive
   ```

    If you skipped optional Web UI dependencies, install them manually:
    ```bash
    pip install "fastapi[standard]" uvicorn pypdf python-docx openpyxl python-pptx
    ```

3. **Start NeuroClaw**

   **Option A — Interactive REPL (terminal)**
   ```bash
  python core/agent/main.py --api-key "$OPENAI_API_KEY"
   ```

   **Option B — Browser Web UI** *(recommended)*
   ```bash
  python core/agent/main.py --web --api-key "$OPENAI_API_KEY"
   ```
   Then open **http://localhost:7080** in your browser. The Web UI features a chat interface, skills sidebar, markdown rendering, and code syntax highlighting.

  If you prefer environment variables, export the provider-specific key first and start NeuroClaw without `--api-key`.

    Web UI attachment parsing currently supports these file types:
    - Text/config/code: `.txt`, `.md`, `.markdown`, `.json`, `.yaml`, `.yml`, `.csv`, `.tsv`, `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.sh`, `.bash`, `.zsh`, `.sql`, `.html`, `.css`, `.xml`, `.log`, `.rst`, `.ini`, `.toml`, `.cfg`
    - Documents: `.pdf`, `.docx`, `.xlsx`, `.pptx`

    The file picker in the Web UI only allows these supported formats.

   To use a custom port or bind to all interfaces (e.g., for remote access):
   ```bash
  python core/agent/main.py --web --port 8080 --host 0.0.0.0 --api-key "$OPENAI_API_KEY"
   ```

<div align="center">
  <img src="materials/index.png" alt="NeuroClaw Feature Overview" style="width: 80%; max-width: 100%;" />
</div>

> Note: We provide benchmark run results and per-model outputs under `materials/benchmark_results/`. These artifacts can be used as practical references when running NeuroClaw benchmarks or reproducing model outputs.

### Verify Installation
```bash
# Check that the environment file is valid
python installer/setup.py --check

# List registered neuroscience skills (Python)
python -c "
from core.skill_loader.loader import SkillLoader
from pathlib import Path
skills = SkillLoader(Path('skills')).load_all()
for s in skills:
    print(s['name'])
"
```

### Benchmark Evaluation

NeuroBench tasks live under `neuro_bench/`, and each task directory contains a `task.md` instruction file.

NeuroBench currently accepts these benchmark configurations:
- `with-skills`: the agent can use the skills loaded from `skills/`
- `no-skills`: the baseline run without skills
- `with-skills` + `no-skills` paired comparison: enable `--benchmark-compare-skills` to run both variants for the same task set

Benchmark scoring is handled separately with `--score-benchmark`: it reads reports in `output/`, applies a GPT-5.4 weighted rubric, and generates numeric scores for planning completeness, tool/skill reasonableness, and command/code correctness. For fairness, each task case is scored in one batch across all comparable models to reduce scoring-standard drift. Skill-call counts are recorded separately and used for efficiency analysis.

To score existing benchmark reports:
```bash
python core/agent/main.py --score-benchmark
```

To speed up scoring on larger runs:
```bash
python core/agent/main.py --score-benchmark --score-workers 8
```

**Web benchmark mode**
```bash
python core/agent/main.py --web --benchmark
```

**CLI benchmark batch runner**
```bash
python core/agent/main.py --benchmark
```

To run the paired skill comparison in CLI mode:
```bash
python core/agent/main.py --benchmark --benchmark-compare-skills
```

In CLI benchmark mode, NeuroClaw will ask for:
- the benchmark directory path
- the benchmark model name

Then it will:
- read all `task.md` files recursively from that directory
- sort tasks alphabetically by task folder name
- run tasks one by one without asking for intermediate confirmation
- print progress in the terminal only
- save reports under `output/<model_name>/`, with one markdown report per case and run

The benchmark reports include the solution thinking, skills used, skill-call counts, and the commands or code that were used or suggested.

---

<a id="project-structure"></a>
## 📁 Project Structure

```
NeuroClaw/
├── README.md                       # This file
├── USER.md                         # User-defined configurations and preferences
├── SOUL.md                         # System behavior guidelines and principles
│
├── core/                           # Self-contained NeuroClaw engine (no OpenClaw required)
│   ├── agent/                      # LLM conversation loop and tool-call dispatcher
│   │   └── main.py                 # Entry point; --web flag starts the Web UI
│   ├── web/                        # Browser-based Web UI (FastAPI + WebSocket)
│   │   ├── server.py               # FastAPI app: WebSocket chat, /api/skills, /api/env
│   │   └── static/
│   │       └── index.html          # Dark-theme chat interface (markdown + syntax highlight)
│   ├── skill-loader/               # Skill scanner: reads skills/*/SKILL.md and registers tools
│   │   └── loader.py
│   ├── tool-runtime/               # Executes handler.js / Python handlers
│   │   └── runtime.py
│   ├── session/                    # Session persistence and context-window compression
│   │   └── manager.py
│   └── config/
│       └── features.json           # Feature toggles (disable WhatsApp/Slack/etc.; enable web_ui)
│
├── installer/                      # Custom setup wizard (replaces OpenClaw's default installer)
│   ├── setup.py                    # Entry point: python installer/setup.py
│   ├── config_wizard.py            # Interactive 6-step configuration wizard (incl. Web UI deps)
│   └── neuro_defaults.json         # Neuroscience-specific default template
│
├── skills/                         # Flat skill directory
│   ├── academic-research-hub/
│   ├── adni-skill/
│   ├── bids-organizer/
│   ├── beautiful-log/
│   ├── brain-visualization/
│   ├── claw-shell/
│   ├── conda-env-manager/
│   ├── conn-tool/
│   ├── dcm2nii/
│   ├── dependency-planner/
│   ├── dipy-tool/
│   ├── docker-env-manager/
│   ├── nibabel-skill/
│   ├── dwi-skill/
│   ├── eeg-skill/
│   ├── experiment-controller/
│   ├── fmri-skill/
│   ├── fmriprep-tool/
│   ├── freesurfer-tool/
│   ├── fsl-tool/
│   ├── git-essentials/
│   ├── git-workflows/
│   ├── hcp-skill/
│   ├── ukb-skill/
│   ├── harness-core/
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
│   ├── skill-updater/
│   ├── smri-skill/
│   └── wmh-segmentation/
│
├── neuro_bench/                    # NeuroBench evaluation tasks (T00–T100)
│   ├── T00_installer_validation/   # Validates installer output
│   └── …
│
├── materials/                      # Research materials, benchmark run results, and model outputs
│   ├── CVPR_2026/
│   └── benchmark_results/
│
└── LICENSE                         # License

```

---

<a id="skill-quick-reference"></a>
## 🛠️ Skill Quick Reference

> **Tip**: Click the ℹ️ icon on any skill card in the Web UI to view expanded documentation, usage examples, and recent execution logs.

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
| `beautiful-log` | Export clean User/NeuroClaw dialogue into beautiful HTML logs | ✅ |
| `skill-updater` | Skill updater and management utilities | ✅ |

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
| `brain-visualization` | Publication-ready figures and 3D assets (connectomes, atlas summaries, FreeSurfer PLY) | ✅ |
| `harness-core` | Core harness SDK: verification, checkpointing, drift detection, audit logging | ✅ |
| `mne-eeg-tool` | Base-layer MNE-Python implementation for EEG | ✅ |
| `fsl-tool` | FSL-based sMRI/fMRI/DWI processing utilities | ✅ |
| `fmriprep-tool` | fMRIPrep pipeline wrapper and execution | ✅ |
| `qsiprep-tool` | qsiPrep pipeline wrapper for diffusion MRI | ✅ |
| `hcppipeline-tool` | HCP-style processing pipeline utilities | ✅ |
| `dipy-tool` | Diffusion MRI processing via DIPY | ✅ |
| `nibabel-skill` | Low-level neuroimaging I/O and geometry handling (NIfTI, affine, FreeSurfer I/O) | ✅ |
| `nilearn-tool` | Fast neuroimaging feature extraction and decoding prep | ✅ |
| `conn-tool` | Functional connectivity computation and analysis | ✅ |
| `freesurfer-tool` | FreeSurfer-based MRI processing and segmentation | ✅ |

#### Model
| Skill | Function | Status |
|------|----------|--------|
| `wmh-segmentation` | White matter hyperintensity segmentation (MARS-WMH nnU-Net) | ✅ |
| `brain_gnn` | BrainGNN: graph neural network for fMRI classification | ✅ |
| `fm_app` | FM-APP: multi-stage phenotype prediction with fMRI+sMRI | ✅ |
| `neurostorm` | NeuroStorm: neuroimaging foundation model | ✅ |
| `glm` | Classical first-level and second-level GLM for task-fMRI activation and group inference | ✅ |
| `ica` | Resting-state network decomposition via independent component analysis | ✅ |
| `dictlearning` | Sparse resting-state network decomposition via dictionary learning | ✅ |
| `svm` | Classical neuroimaging disease classification with ROI/tabular features | ✅ |
| `spacenet` | Voxel-wise neuroimaging disease classification with sparse coefficient maps | ✅ |
| `kmeans` | Brain parcellation via K-means clustering | ✅ |
| `hierarchical` | Multi-scale brain parcellation via hierarchical clustering | ✅ |
| `filtering` | Temporal filtering for neuroimaging signal denoising | ✅ |
| `detrending` | Temporal drift removal for neuroimaging signal denoising | ✅ |

#### Dataset
| Skill | Function | Status |
|------|----------|--------|
| `adni-skill` | ADNI dataset automated processing workflow | ✅ |
| `hcp-skill` | HCP-YA dataset automated processing workflow | ✅ |
| `ukb-skill` | UKB brain imaging automated processing workflow | ✅ |

#### Modality
| Skill | Function | Status |
|------|----------|--------|
| `eeg-skill` | EEG preprocessing and feature extraction workflows | ✅ |
| `fmri-skill` | Functional MRI preprocessing and analysis workflows | ✅ |
| `smri-skill` | Structural MRI preprocessing and analysis workflows | ✅ |
| `dwi-skill` | Diffusion MRI preprocessing and analysis workflows | ✅ |

**Legend**: ✅ Implemented | 🏗️ In Development | ⏳ Planned


---

## TODO List

### Architecture & Foundation
- ✓ Hierarchical architecture design (Interface-Subagent-Base Tool)
- ✓ Complete Interface layer implementation
- ✓ Subagent coordination mechanisms

### Dataset Ecosystem
- ✓ Complete ADNI processing chain
- ✓ HCP dataset adaptation
- ☐ UK Biobank adaptation
- ☐ Multi-dataset workflow support

### Model Reproduction & Execution
- ✓ Automatic paper model retrieval
- ✓ Automatic environment configuration
- ✓ Full Harness Engineering for Reproducibility

### Community & Extensions
- ☐ Multi-institution collaboration capabilities
- ☐ Plugin ecosystem for third-party skills

---


<a id="acknowledgments"></a>
## 🙏 Acknowledgments

Thanks to:
- [OpenClaw](https://github.com/openclaw/openclaw) framework contributors
- [Karcen/rs-fMRI-Pipeline-Tutorial](https://github.com/Karcen/rs-fMRI-Pipeline-Tutorial) for the brain visualization workflow inspiration
- All contributors and user feedback
- Open-source neuroscience tools community (MNE-Python, FreeSurfer, FSL, etc.)
