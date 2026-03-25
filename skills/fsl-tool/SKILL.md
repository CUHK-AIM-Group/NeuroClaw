---
name: fsl-tool
description: "Use this skill whenever the user wants to process neuroimaging data with FSL (FMRIB Software Library), covering structural MRI, functional MRI (fMRI), and diffusion MRI (dMRI/DTI). Triggers include: 'use FSL', 'FSL processing', 'fsl_anat', 'FEAT', 'MELODIC', 'eddy', 'bedpostx', 'probtrackx', 'BET', 'FAST', 'FLIRT', 'FNIRT', 'run FSL pipeline'. This skill is the NeuroClaw interface-layer wrapper for FSL: checks installation, generates execution plan with concrete shell commands, waits for explicit confirmation, then routes all commands through claw-shell."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# FSL Tool (FMRIB Software Library)

## Overview

FSL is a comprehensive library of analysis tools for MRI, fMRI, and diffusion brain imaging. This skill provides a safe, unified interface for the three core modalities in NeuroClaw:

- Structural MRI (T1w, T2w, FLAIR)
- Functional MRI (task-based and resting-state)
- Diffusion MRI (DTI / dMRI)

**Workflow**:
1. Check if FSL is installed (`fslversion`).
2. If not installed → call `dependency-planner` to generate installation plan.
3. Analyze input files and propose concrete shell commands with parameter explanations.
4. Present full numbered plan + estimated time + risks.
5. Wait for explicit user confirmation (“YES”, “execute”, “proceed”).
6. Execute all commands safely via `claw-shell`.
7. Summarize outputs and suggest next steps.

**Research use only.**

## Core Modalities and Common Shell Commands

### 1. Structural MRI

```bash
# One-click structural preprocessing (strongly recommended)
fsl_anat -i T1w.nii.gz -o T1w_anat --clobber
# -i : 输入 T1w 文件
# -o : 输出文件夹名称
# --clobber : 覆盖已存在文件（常用）

# Brain extraction (BET)
bet T1w.nii.gz T1w_brain -m -f 0.5
# -m : 输出脑掩膜（_mask.nii.gz）
# -f : 脑提取阈值（0.3~0.7，越小保留越多脑组织，通常 0.5 较稳妥）

# Tissue segmentation + bias correction
fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -o T1w_fast T1w_brain
# -t 1 : T1 加权图像
# -n 3 : 分成 3 类（灰质、白质、脑脊液）
# -H 0.1 : 偏场校正强度（0.0~0.4，越大校正越强）
# -o : 输出前缀

# Linear + nonlinear registration to MNI152
flirt -in T1w_brain -ref $FSLDIR/data/standard/MNI152_T1_2mm_brain -out T1w_to_MNI -omat T1w_to_MNI.mat -dof 12
# -dof 12 : 12 参数仿射配准（常用）

fnirt --in=T1w_brain --aff=T1w_to_MNI.mat --cout=T1w_to_MNI_warp --config=T1_2_MNI152_2mm
# --config : 使用标准配置文件（2mm 分辨率最常用）

# Subcortical segmentation
first -i T1w_brain -o T1w_first -b
# -b : 输出所有亚皮层结构的二值化掩膜
```

### 2. Functional MRI

```bash
# Motion correction
mcflirt -in bold.nii.gz -out bold_mcf -plots -refvol 0
# -plots : 输出运动参数图
# -refvol 0 : 以第 0 帧作为参考（常用）

# Task-based fMRI full analysis (FEAT)
feat design.fsf
# 需要提前准备 design.fsf 文件（可通过 FEAT GUI 生成）

# Resting-state ICA
melodic -i bold_mcf.nii.gz -o melodic_output --report --nobet --bgthreshold=10 --tr=2.0 --mmthresh=0.5 --dim=30
# --tr : 重复时间（秒），必须与实际扫描一致
# --dim : 估计的独立成分数量（20~50 较常用）
# --report : 生成 HTML 报告（强烈推荐）

# Automatic denoising (FIX)
fix melodic_output -c $FSLDIR/training_files/Standard.RData -m -f 20
# -c : 分类器文件（Standard.RData 最常用）
# -f 20 : 运动/噪声阈值（越高越保守，通常 20~30）
```

### 3. Diffusion MRI

```bash
# Distortion and eddy current correction
topup --imain=AP_PA_b0.nii.gz --datain=acqparams.txt --out=topup_results --fout=field --iout=b0_unwarped
eddy --imain=dwi.nii.gz --mask=dwi_brain_mask.nii.gz --acqp=acqparams.txt --index=index.txt \
     --bvecs=bvecs --bvals=bvals --topup=topup_results --out=eddy_corrected --very_verbose
# --very_verbose : 输出详细日志（调试时有用）

# Tensor fitting
dtifit -k eddy_corrected.nii.gz -m dwi_brain_mask.nii.gz -r bvecs -b bvals -o dtifit
# -k : 校正后的扩散图像
# -r / -b : 梯度方向和 b 值文件

# Multi-fiber modeling
bedpostx bedpostx_input -n 3 -w 1 -b 1000
# -n 3 : 每个体素最多 3 根纤维（常用）
# -b 1000 : 燃烧采样次数（默认 1000，越大越精确但越慢）

# Automated major tract extraction
xtract -bpx bedpostx_input.bedpostX -out xtract_results -str $FSLDIR/data/xtract/tracts.txt
# -str : 使用的标准白质束列表文件
```

## Quick Reference

| Modality       | Task                        | Main Command                     | Typical Time     |
|----------------|-----------------------------|----------------------------------|------------------|
| Structural     | Full preprocessing          | `fsl_anat`                       | 10–40 min       |
| Structural     | Brain extraction            | `bet`                            | 1–3 min         |
| Structural     | Tissue segmentation         | `fast`                           | 5–15 min        |
| Functional     | Motion correction           | `mcflirt`                        | 2–10 min        |
| Functional     | Task GLM                    | `feat`                           | 15–90 min       |
| Functional     | Resting-state ICA           | `melodic`                        | 20–120 min      |
| Diffusion      | Preprocessing               | `topup + eddy`                   | 30–180 min      |
| Diffusion      | Tensor metrics              | `dtifit`                         | 5–20 min        |
| Diffusion      | Tractography                | `probtrackx2 / xtract`           | 30 min – 24 h+  |

## Installation

Use `dependency-planner` skill with one of the following requests:

- “Install latest FSL on Ubuntu using official installer”
- “Install FSL via conda-forge in a new environment”

After installation, verify with:
```bash
fslversion
echo $FSLDIR
```

## Important Notes & Limitations

- All actual execution is routed through `claw-shell`.
- Long-running commands (bedpostx, probtrackx, group FEAT, etc.) run safely in the `claw` tmux session.
- Always consider running `fsl_anat` first for structural data — it handles BET + FAST + registration automatically.
- Input must be NIfTI format. Use `dcm2nii` skill first if starting from DICOM.
- Monitor progress with `tail -f` on the log file provided by claw-shell.

## When to Call This Skill

- After `dcm2nii` conversion
- When any FSL preprocessing, registration, segmentation or advanced analysis is needed
- Before feeding quantitative results into `paper-writing` or `experiment-controller`

## Complementary / Related Skills

- `dcm2nii` / `nii2dcm`
- `dependency-planner`
- `claw-shell`
- `freesurfer-processor`
- `wmh-segmentation`

## More Advanced Features

For less common tools (ASL, FABBER, VBM, PALM, custom scripting, etc.), please refer to the official FSL documentation:

- Official FSL Website: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/
- Structural tools: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Structural
- Functional tools: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FEAT
- Diffusion tools: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT
- Full tool list: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSL

You may use the `multi-search-engine`, `academic-research-hub`, or `arxiv-cli-tools` skill anytime to find the latest FSL tutorials or example pipelines.

---

Created At: 2026-03-25  
Last Updated At: 2026-03-25  
Author: Cheng Wang