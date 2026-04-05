#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 3: Conda Env Manager (Install htop)

Scoring focus:
1. A result JSON is generated in benchmark_results/T03_conda_env_manager/
2. The referenced conda environment exists
3. htop is available and runnable in that environment
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
RESULT_DIR = ROOT / "benchmark_results" / "T03_conda_env_manager"


def run_cmd(cmd: List[str], timeout: int = 120) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def get_latest_result_file() -> Optional[Path]:
    if not RESULT_DIR.exists() or not RESULT_DIR.is_dir():
        return None
    files = sorted(RESULT_DIR.glob("result_*.json"), reverse=True)
    if not files:
        files = sorted(RESULT_DIR.glob("*.json"), reverse=True)
    return files[0] if files else None


def load_result_json(path: Path) -> Tuple[Optional[Dict[str, Any]], str]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f), ""
    except Exception as e:
        return None, str(e)


def conda_env_exists(env_name: str) -> Tuple[bool, str]:
    conda_bin = shutil.which("conda")
    if not conda_bin:
        return False, "conda not found in PATH"

    code, out, err = run_cmd([conda_bin, "env", "list", "--json"], timeout=60)
    if code != 0:
        return False, f"conda env list failed: {err or out}"

    try:
        data = json.loads(out)
        env_paths = data.get("envs", [])
        names = {Path(p).name for p in env_paths}
        return env_name in names, "ok" if env_name in names else f"env '{env_name}' not found"
    except Exception as e:
        return False, f"failed to parse conda env list json: {e}"


def check_htop_in_env(env_name: str) -> Tuple[bool, Dict[str, Any], str]:
    conda_bin = shutil.which("conda")
    if not conda_bin:
        return False, {}, "conda not found in PATH"

    # Check executable path first
    code_which, out_which, err_which = run_cmd(
        [conda_bin, "run", "-n", env_name, "which", "htop"],
        timeout=60,
    )
    if code_which != 0:
        return False, {}, f"'which htop' failed: {err_which or out_which}"

    # Check version
    code_ver, out_ver, err_ver = run_cmd(
        [conda_bin, "run", "-n", env_name, "htop", "--version"],
        timeout=60,
    )
    if code_ver != 0:
        return False, {}, f"'htop --version' failed: {err_ver or out_ver}"

    version_text = out_ver.splitlines()[0].strip() if out_ver else "unknown"

    return True, {
        "which": out_which,
        "version": version_text,
    }, "ok"


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 3: Conda Env Manager (Install htop)")
    print("=" * 70)

    result_file = get_latest_result_file()
    if result_file is None:
        print(f"❌ No result json found in {RESULT_DIR}")
        return 1

    print(f"Using result file: {result_file}")
    result_data, err = load_result_json(result_file)
    if result_data is None:
        print(f"❌ Failed to load result json: {err}")
        return 1

    env_name = (
        result_data.get("environment", {}).get("name")
        if isinstance(result_data, dict)
        else None
    )
    if not env_name:
        print("❌ Missing key: environment.name")
        return 1

    ok_env, msg_env = conda_env_exists(env_name)
    if not ok_env:
        print(f"❌ Conda environment check failed: {msg_env}")
        return 1
    print(f"✅ Conda environment exists: {env_name}")

    ok_htop, htop_info, msg_htop = check_htop_in_env(env_name)
    if not ok_htop:
        print(f"❌ htop check failed: {msg_htop}")
        return 1

    print(f"✅ htop runnable: {htop_info.get('version')}")
    print(f"   path: {htop_info.get('which')}")

    print("=" * 70)
    print("✅ PASS")
    return 0


if __name__ == "__main__":
    sys.exit(grade())
