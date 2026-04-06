#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 8: Git Workflow.

Scoring rule:
- Pull/clone the submitted repository.
- Confirm README.md content is exactly: NeuroBench Task 8
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
RESULT_DIR = ROOT / "benchmark_results" / "T08_git"


def run_cmd(cmd: List[str], cwd: Optional[Path] = None, timeout: int = 120) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def pick_latest_result_file() -> Optional[Path]:
    if not RESULT_DIR.exists() or not RESULT_DIR.is_dir():
        return None
    files = sorted(RESULT_DIR.glob("result_*.json"), reverse=True)
    if not files:
        files = sorted(RESULT_DIR.glob("*.json"), reverse=True)
    return files[0] if files else None


def load_result(path: Path) -> Tuple[Optional[Dict[str, Any]], str]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f), ""
    except Exception as e:
        return None, str(e)


def resolve_branch(data: Dict[str, Any]) -> str:
    branch = data.get("git", {}).get("branch")
    if isinstance(branch, str) and branch.strip():
        return branch.strip()
    return "main"


def resolve_repo_url(data: Dict[str, Any]) -> Optional[str]:
    git_obj = data.get("git", {}) if isinstance(data, dict) else {}
    repo_url = git_obj.get("repo_url")
    if isinstance(repo_url, str) and repo_url.strip():
        return repo_url.strip()
    return None


def readme_content(repo_dir: Path) -> Tuple[bool, str]:
    readme = repo_dir / "README.md"
    if not readme.exists() or not readme.is_file():
        return False, "README.md not found in pulled repository"

    try:
        content = readme.read_text(encoding="utf-8").strip()
    except Exception as e:
        return False, f"failed to read README.md: {e}"

    if content != "NeuroBench Task 8":
        return False, f"README.md content mismatch: got '{content}'"

    return True, "README.md content is correct"


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 8: Git Workflow")
    print("=" * 70)

    git_bin = shutil.which("git")
    if not git_bin:
        print("❌ git not found in PATH")
        return 1

    result_file = pick_latest_result_file()
    if result_file is None:
        print(f"❌ No result JSON found in {RESULT_DIR}")
        return 1

    print(f"Using result file: {result_file}")
    data, err = load_result(result_file)
    if data is None:
        print(f"❌ Failed to load result JSON: {err}")
        return 1

    repo_url = resolve_repo_url(data)
    if not repo_url:
        print("❌ Missing key: git.repo_url")
        return 1

    branch = resolve_branch(data)

    with tempfile.TemporaryDirectory(prefix="t08_git_grade_") as tmp:
        tmp_path = Path(tmp)
        clone_dir = tmp_path / "repo"

        # Clone first, then pull to follow the scoring description.
        print(f"Cloning repository: {repo_url}")
        code, out, err = run_cmd([git_bin, "clone", "-b", branch, repo_url, str(clone_dir)], timeout=180)
        if code != 0:
            print(f"❌ git clone failed: {err or out}")
            return 1

        code, out, err = run_cmd([git_bin, "pull"], cwd=clone_dir, timeout=120)
        if code != 0:
            print(f"❌ git pull failed: {err or out}")
            return 1

        ok, msg = readme_content(clone_dir)
        if not ok:
            print(f"❌ FAIL: {msg}")
            return 1

        print(f"✅ PASS: {msg}")
        return 0


if __name__ == "__main__":
    sys.exit(grade())
