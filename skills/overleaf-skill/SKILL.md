---

name: overleaf-skill
description: "Use this skill whenever the user wants to synchronize NeuroClaw-generated LaTeX manuscripts with Overleaf, read/write .tex files, download/upload projects, create/rename/archive projects, compare versions, or manage project structure. Triggers include: 'sync to Overleaf', 'upload paper to Overleaf', 'Overleaf project', 'LaTeX sync', 'push draft', 'download Overleaf', 'create Overleaf project', 'tex file to Overleaf', or any request involving paper_draft.tex / collaboration. This skill is the **mandatory interface-layer LaTeX collaborator** in NeuroClaw: it strictly enforces pull-first workflow with diff reporting and per-operation user authorization for any write/create/delete action, uses pyoverleaf (cookie-based), preserves Overleaf version history, integrates directly after paper-writing, and never performs unauthorized modifications."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)

---

# Overleaf Skill

## Overview

This skill provides secure, audited access to Overleaf projects using the pyoverleaf library (Python API + CLI), enabling full round-trip collaboration for NeuroClaw manuscripts.

Role in NeuroClaw multi-agent system:
- Acts as the dedicated Overleaf Collaborator.
- Authentication: manual cookie string provided by the user (recommended for headless/server environments).
- Default behavior: pull + diff + report changes → require user confirmation before any local overwrite or merge.
- Write / create / delete / rename operations: **strictly forbidden** without explicit, single-use user authorization per operation.
- Preferred method: Python API (more reliable than CLI in agent sessions).
- Preserves full Overleaf version history for easy human review and revert.
- Supports listing projects, file/folder management, ZIP download/upload, and limited project creation/renaming/archiving.

**Research use only** — keeps manuscripts clean, typeset-ready, and suitable for co-author feedback or journal submission.

## Supported Operations

| Operation                  | Method                  | CLI Example                                      | Python API Example                                                                 | Safety Requirement                   |
|----------------------------|-------------------------|--------------------------------------------------|------------------------------------------------------------------------------------|--------------------------------------|
| List projects              | API / CLI               | `pyoverleaf ls`                                  | `api.get_projects()`                                                               | Safe (read-only)                     |
| Download project (ZIP)     | API / CLI               | `pyoverleaf download-project "My Paper" out.zip` | `api.download_project(project_id, "out.zip")`                                      | Safe                                 |
| Read file content          | CLI / ProjectIO         | `pyoverleaf read "My Paper/main.tex"`            | `with io.open("main.tex", "r") as f: content = f.read()`                           | Safe                                 |
| Write / Update file        | CLI / ProjectIO         | `echo "..." | pyoverleaf write "My Paper/main.tex"`      | `with io.open("main.tex", "w") as f: f.write(new_content)`                         | Explicit user authorization required |
| Upload binary file         | ProjectIO / API         | `cat fig.png | pyoverleaf write "My Paper/figures/fig.png"` | `api.project_upload_file(project_id, parent_id, "fig.png", file_bytes)`            | Explicit user authorization required |
| Create folder              | CLI / API               | `pyoverleaf mkdir -p "My Paper/chapters"`        | `api.project_create_folder(project_id, parent_id, "chapters")` or `io.mkdir(...)` | Explicit user authorization required |
| Delete file/folder         | CLI / API               | `pyoverleaf rm "My Paper/old.tex"`               | `api.project_delete_entity(project_id, entity)`                                    | Explicit user authorization required |
| Create new project         | API (limited)           | (web recommended first)                          | (internal call or ZIP upload simulation)                                           | Double confirmation + auth required  |
| Rename / Archive project   | API                     | —                                                | (API supports; method may vary)                                                    | Explicit user authorization required |
| Pull + diff + review       | Skill logic + claw-shell| Auto: download → diff → summarize → ask user     | Skill combines API download + local diff                                           | Core safety workflow                 |

## Authentication (Important – Headless/Server Friendly)

This skill **cannot log in automatically**. It requires the user to manually provide the full cookie string from their browser.

**How to get the cookie string:**
1. Log in to https://www.overleaf.com in Chrome or Firefox (do not use incognito).
2. Open DevTools (F12) → Network tab → refresh the page.
3. Click any request (e.g. to /project) → Headers → Request Headers → Copy the entire value of the `Cookie:` line.
   Example:
   ```
   overleaf_session2=s%3Ap85XgMaybdjaWutDHogKReuvzjg1DZlhgkZZI08q9cYNf0m%2B3B3OfhBgnFddQ2bsiQ6us... (full long string)
   ```

**Important implementation note:** `pyoverleaf.Api.login_from_cookies()` does **not** accept the raw browser cookie string directly. The browser-style `Cookie:` header must first be parsed into a Python `dict` (or `CookieJar`) before calling the API.

Correct pattern:
```python
raw = "overleaf_session2=...; oa=1; ..."
cookie_dict = {}
for part in raw.split(';'):
    part = part.strip()
    if not part or '=' not in part:
        continue
    k, v = part.split('=', 1)
    cookie_dict[k.strip()] = v.strip()

api.login_from_cookies(cookie_dict)
```

**Do not do this:**
```python
api.login_from_cookies("overleaf_session2=...; oa=1; ...")
```
This will raise an `AssertionError` in current pyoverleaf versions because the method expects a `dict` or `CookieJar`, not a string.

- Cookie usually lasts several months.
- If it expires or login fails, the skill should ask again:  
  **"Overleaf authentication failed. Please provide a fresh cookie string from your browser."**
- For self-hosted Overleaf: set `export PYOVERLEAF_HOST=your-domain.com`

## Quick Workflows (NeuroClaw Integrated)

1. After `paper-writing` finishes → suggest: “Would you like to sync paper_draft.tex to Overleaf? (pull-first recommended)”
2. Pull & Review → download ZIP → unzip to /tmp → diff local files → summarize changes → ask: “Merge changes? Overwrite local? Cancel?”
3. Authorized Push → user explicitly says “yes push”, “overwrite Overleaf”, etc. → one-time authorization → use ProjectIO or upload_file → report success + link to Overleaf history
4. Create Project → if no suitable project exists: recommend user creates one via web first (safest), or attempt API creation only if the installed pyoverleaf version actually exposes project creation support
5. Full Sync → pull latest → apply NeuroClaw edits locally → authorized push

## Installation (in NeuroClaw environment)

```bash
# Install pyoverleaf in isolated environment
pip install pyoverleaf

# Quick test (user runs once in terminal)
python -c "import pyoverleaf; api=pyoverleaf.Api(); print(api.get_projects())"
```

## Operational Notes from Real Server Usage

### 1. Use the correct Python interpreter
In multi-environment NeuroClaw setups, `pyoverleaf` may be installed in a specific conda environment while the system `python3` does not have it.

Example:
```bash
/home/cwang/anaconda3/envs/claw/bin/python script.py
```

Do not assume `python3` points to the intended environment.

### 2. Avoid approval-loop pain by not using inline heredoc Python for Overleaf writes
On OpenClaw / gateway-host exec, commands such as:
```bash
python3 - <<'PY'
...
PY
```
can repeatedly trigger fresh approval prompts because they are treated as interpreter/runtime commands with conservative approval semantics. Even if the user clicks approval in the popup, re-running the command creates a new approval request.

**Preferred pattern:**
- write a real local script file first
- run that script file with the exact intended Python interpreter
- split read-only checks and write operations into separate steps

Recommended flow:
1. write `overleaf_login_check.py`
2. run read-only login/list-projects check
3. write `overleaf_upload_only.py`
4. run upload only after explicit user authorization

This reduces approval churn and makes failures easier to diagnose.

### 3. Separate read-only checks from write actions
Before any create/upload/delete action:
- first verify `pyoverleaf` import
- then verify login
- then verify the target project exists
- only then perform write actions

This isolates:
- environment issues
- authentication issues
- project lookup issues
- upload API issues

### 4. Project creation is not reliably supported by current pyoverleaf deployments
Even if the skill conceptually supports project creation, the installed `pyoverleaf.Api` may not expose `new_project` or `create_project`.

Observed behavior in real usage:
- login worked
- listing projects worked
- project creation was **unsupported by pyoverleaf Api**

Therefore, the safest default remains:
- **ask the user to create a blank Overleaf project via the web UI first**
- then use the skill to upload files into that existing project

### 5. Upload requires a real folder id, not `None`
Calling:
```python
api.project_upload_file(project_id, None, filename, file_bytes)
```
may fail with:
- HTTP 422

The correct approach is:
1. call `api.project_get_files(project_id)`
2. retrieve the returned root folder id
3. pass that folder id into `project_upload_file`

Correct pattern:
```python
root_folder = api.project_get_files(project_id)
folder_id = root_folder.id
api.project_upload_file(project_id, folder_id, filename, file_bytes)
```

### 6. Confirm project existence immediately before upload
After the user creates a project in the browser, do a fresh read-only project listing again to confirm the new project is visible before attempting upload.

### 7. Keep credentials local and temporary
If a cookie must be written to disk for scripting, keep it in a dedicated local secrets path such as:
```bash
.secrets/overleaf_cookie.txt
```
and avoid committing it. After the workflow completes, recommend that the user refresh or rotate their browser session cookie.

## Safety & Limitations

- **No automatic writes**: Every create/update/delete/rename/push requires explicit single-operation user confirmation.
- **Cookie must be provided by user**: Agent never assumes or stores credentials long-term.
- **Version history preserved**: API operations appear in Overleaf History for easy review/revert.
- **CLI limitations**: Occasional websocket instability → prefer Python API + ProjectIO.
- **Project creation**: API support is inconsistent across pyoverleaf versions; safest to create blank project via web first, then fill with this skill.
- **Approval behavior**: On OpenClaw gateway/node exec, write operations may need host approval. Use real script files and split steps to minimize repeated prompts.

## When to Trigger

- Immediately after `paper-writing` completes paper_draft.tex / .md
- User mentions sync / push / pull / Overleaf / create project / LaTeX collaboration
- During manuscript polishing, arXiv, or journal submission phase
- When co-authors need an editable Overleaf link

## Related Skills

- `paper-writing` → generates paper_draft.tex / .md
- `claw-shell` → handles unzip / diff / mv / local file ops
- `dependency-planner` → installs pyoverleaf and LaTeX dependencies

## References

- pyoverleaf GitHub: https://github.com/jkulhanek/pyoverleaf
- Original inspiration: Eason’s overleaf-skill workflow
- Core principle: pull → diff → report → confirm; push only with explicit per-operation authorization

Created At: 2026-03-23  
Last Updated At: 2026-03-24  
Author: Cheng Wang
