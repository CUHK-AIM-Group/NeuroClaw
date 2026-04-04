---
name: academic-research-hub
description: "Use this skill when users need to search academic papers, download research documents, extract citations, or gather scholarly information. Triggers include: requests to \"find papers on\", \"search research about\", \"download academic articles\", \"get citations for\", or any request involving academic databases like arXiv, PubMed, Semantic Scholar, or Google Scholar. Also use for literature reviews, bibliography generation, and research discovery."
license: Proprietary
---

# Academic Research Hub

## Overview

Academic Research Hub provides unified access to multiple academic databases (arXiv, PubMed, Semantic Scholar, etc.) for searching papers, downloading PDFs, extracting citations, and generating bibliographies. It is the recommended tool for literature review and reference management in NeuroClaw.

**Prerequisite:** Install [OpenClawCLI](https://clawhub.ai/) (Windows, MacOS)

## Installation

**Best Practices:**

```bash
# Standard installation
pip install arxiv scholarly pubmed-parser semanticscholar requests

# If you encounter permission errors, use a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install arxiv scholarly pubmed-parser semanticscholar requests
```

**Never use `--break-system-packages`** as it can damage your system's Python installation.

## Quick Reference

| Task                    | Command                                              |
|-------------------------|------------------------------------------------------|
| Search arXiv            | `python scripts/research.py arxiv "quantum computing"` |
| Search PubMed           | `python scripts/research.py pubmed "covid vaccine"`  |
| Search Semantic Scholar | `python scripts/research.py semantic "machine learning"` |
| Download papers         | `python scripts/research.py arxiv "topic" --download` |
| Get citations           | `python scripts/research.py arxiv "topic" --citations` |
| Generate bibliography   | `python scripts/research.py arxiv "topic" --format bibtex` |
| Save results            | `python scripts/research.py arxiv "topic" --output results.json` |

## Core Features

- Multi-source search (arXiv, PubMed, Semantic Scholar, Google Scholar)
- Full-text PDF download
- Citation extraction (BibTeX, RIS, JSON, plain text)
- Comprehensive metadata retrieval (title, authors, abstract, DOI, citation count, etc.)

## When to Call This Skill

- Need to search for recent papers on a specific topic
- Build literature reviews or bibliographies
- Download PDFs for local reading
- Extract citations for `paper-writing`
- Use inside `research-idea` or `method-design` workflows

## Complementary / Related Skills

- `multi-search-engine` → general web/academic search

## Reference & Source

- Official documentation and APIs: arXiv, PubMed, Semantic Scholar
- OpenClawCLI: https://clawhub.ai/

---
Created At: 2026-03-25 18:20 HKT  
Last Updated At: 2026-03-25 18:20 HKT  
Author: chengwang96