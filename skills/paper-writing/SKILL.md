---
name: paper-writing
description: "Use this skill whenever the user wants to generate a full academic paper draft from existing research materials. Triggers include: 'write paper', 'generate manuscript', 'draft paper', 'paper-writing', 'hierarchical drafting', 'manuscript composer', 'create LaTeX paper', 'write research paper from IDEA METHOD EXPERIMENT', or any request to transform IDEA.md + METHOD.md + EXPERIMENT.md into a typeset-ready manuscript. This skill is the **mandatory interface-layer writer** in NeuroClaw: it strictly follows the hierarchical manuscript drafting and iterative refinement process (section 4.4 + provided flowchart), never generates the full paper in one shot, saves every intermediate step as a separate file, and produces either clean plain-text or LaTeX output."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# Paper Writing

## Overview

This skill implements the exact **Hierarchical Manuscript Drafting and Iterative Refinement** process described in section 4.4 of the NeuroClaw architecture and the accompanying flowchart.

It acts as the Manuscript Composer within an end-to-end multi-agent framework:
- Reads the latest versions of **IDEA.md**, **METHOD.md**, and **EXPERIMENT.md** from the current workspace (continuously updated by the related skills research-idea, method-design, and experiment-controller).
- If any of the three files are missing or empty, it immediately prompts the user to provide the research idea, experimental methods, and results before proceeding.
- First asks the user whether the final output should be **plain text (.md)** or **LaTeX (.tex)**.
- When LaTeX format is selected, it asks the user to provide a custom template file (e.g., `template.tex`). If none is supplied, it automatically uses the default IEEE template (conference or journal version with appropriate `\documentclass`, packages, and structure).
- When processing **EXPERIMENT.md**, if sufficient quantitative results are present (metrics, comparisons, ablation studies, numerical values, etc.), the skill automatically generates and inserts well-formatted tables (Markdown tables for plain-text mode; proper LaTeX `tabular` or `table` environment for LaTeX mode) into the Results and Discussion sections.
- Then executes the hierarchical flow **step by step** (never one-shot generation), saving the output of **every single step** as a separate Markdown file in the workspace root (e.g., 01_section_content.md, 02_ethics_review.md, ..., 10_final_draft.md). This enforces incremental execution and allows OpenClaw to resume or inspect progress at any stage.

The process preserves narrative coherence, reuses semantic anchors from previous sections, automatically generates figures from experimental logs, ensures ethical dataset citation, improves scientific storytelling, verifies cross-references, and applies self-healing compilation for LaTeX.

**Research use only** — the output is a high-quality draft ready for final human polishing and journal submission.

## Quick Reference (Hierarchical Flow)

| Step | Description | Output File |
|------|-------------|-------------|
| 1. Section Content Generation | Build each section from IDEA.md + METHOD.md + EXPERIMENT.md (auto-generate tables from results if data is sufficient) | 01_section_content.md |
| 2. Ethics Review | Verify dataset origin, license, and ethical approval | 02_ethics_review.md |
| 3. Iterative Optimization | Refine content based on previous sections | 03_iterative_optimization.md |
| 4. Narrative Storytelling | Convert technical content into coherent scientific story | 04_narrative_storytelling.md |
| 5. De-AI Polishing | Remove AI artifacts and improve natural academic tone | 05_de_ai_polishing.md |
| 6. Logic & Continuity Review | Ensure logical flow and cross-section consistency | 06_logic_continuity_review.md |
| 7. Length Control | Adjust section lengths to target journal limits | 07_length_control.md |
| 8. Reference Review & Repair | Verify and fix all citations and cross-references | 08_reference_review.md |
| 9. LaTeX Error Repair | (LaTeX only) Automatically correct compilation errors | 09_latex_error_repair.md |
| 10. Final Draft Generation | Produce and save the complete manuscript | 10_final_draft.md or 10_final_draft.tex |

## Installation

```bash
# Place files in: skills/paper-writing/
```

## Important Notes & Limitations

- The skill **never** generates the full paper in a single step.
- Every intermediate step **must** be saved as a separate numbered Markdown file (01_*.md through 10_*.md) to guarantee step-by-step execution in OpenClaw.
- If LaTeX format is chosen, the skill will ask the user to provide a custom template file. If none is provided, the default IEEE template is used automatically.
- If EXPERIMENT.md contains sufficient quantitative data, tables are automatically generated and inserted into Results/Discussion sections (Markdown tables or LaTeX `tabular` environment).
- If any source file (IDEA.md, METHOD.md, EXPERIMENT.md) is missing, the skill stops and prompts the user to provide the missing content.
- Final output is always saved as `paper_draft.md` (plain text) or `paper_draft.tex` (LaTeX) in the workspace root.
- All intermediate files remain in the workspace for inspection, editing, or resumption.

## When to Call This Skill

- After completing research-idea, method-design, and experiment-controller phases
- When the user wants a polished manuscript draft from the three core MD files
- Before final submission to a journal or arXiv

## Complementary / Related Skills

- `research-idea`         → continuously updates IDEA.md
- `method-design`         → continuously updates METHOD.md
- `experiment-controller` → continuously updates EXPERIMENT.md
- `dependency-planner`    → installs LaTeX dependencies when LaTeX output is selected
- `claw-shell`            → used internally for LaTeX compilation and file operations

## Reference & Source

Hierarchical Manuscript Drafting and Iterative Refinement (section 4.4 of NeuroClaw architecture).  
Flowchart: multi-agent section generation → ethics review → iterative optimization → narrative writing → de-AI polishing → logic/continuity/length/reference checks → LaTeX repair → final draft.

Created At: 2026-03-23  
Last Updated At: 2026-03-23  
Author: chengwang96