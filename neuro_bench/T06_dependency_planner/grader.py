#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 6: Dependency Planner (PyTorch Compatibility)

Scoring focus:
1. A result JSON is generated in benchmark_results/T06_dependency_planner/
2. The referenced conda environment exists
3. PyTorch works in that environment (import + smoke test)
4. If host has GPU, torch must be able to use GPU
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
RESULT_DIR = ROOT / "benchmark_results" / "T06_dependency_planner"


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


def host_has_gpu() -> Tuple[bool, str]:
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        return False, "nvidia-smi not found"

    code, out, err = run_cmd([nvidia_smi, "-L"], timeout=30)
    if code == 0 and out:
        return True, "nvidia-smi"
    if code == 0 and not out:
        return False, "nvidia-smi (no listed devices)"
    return False, f"nvidia-smi failed: {err or out}"


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


def check_torch_in_env(env_name: str) -> Tuple[bool, Dict[str, Any], str]:
    conda_bin = shutil.which("conda")
    if not conda_bin:
        return False, {}, "conda not found in PATH"

    check_code = (
        "import json, torch; "
        "x=torch.tensor([1.0,2.0]); y=(x*2).sum().item(); "
        "info={"
        "'torch_version': torch.__version__,"
        "'cuda_compiled': getattr(torch.version,'cuda',None),"
        "'cuda_available': bool(torch.cuda.is_available()),"
        "'cpu_smoke': abs(y-6.0) < 1e-6"
        "}; "
        "print(json.dumps(info))"
    )

    code, out, err = run_cmd([conda_bin, "run", "-n", env_name, "python", "-c", check_code], timeout=180)
    if code != 0:
        return False, {}, f"failed to run torch check: {err or out}"

    try:
        data = json.loads(out.splitlines()[-1])
    except Exception as e:
        return False, {}, f"failed to parse torch check output: {e}, raw={out}"

    if not data.get("cpu_smoke", False):
        return False, data, "cpu smoke test failed"

    return True, data, "ok"


def check_gpu_compute(env_name: str) -> Tuple[bool, str]:
    conda_bin = shutil.which("conda")
    if not conda_bin:
        return False, "conda not found in PATH"

    gpu_code = (
        "import torch; "
        "assert torch.cuda.is_available(); "
        "x=torch.tensor([1.0,2.0], device='cuda'); "
        "y=(x*3).sum().item(); "
        "assert abs(y-9.0) < 1e-6; "
        "print('gpu_ok')"
    )

    code, out, err = run_cmd([conda_bin, "run", "-n", env_name, "python", "-c", gpu_code], timeout=180)
    if code != 0:
        return False, f"gpu compute failed: {err or out}"
    if "gpu_ok" not in out:
        return False, f"gpu check unexpected output: {out}"
    return True, "ok"


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 6: Dependency Planner (PyTorch Compatibility)")
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

    ok_torch, torch_info, msg_torch = check_torch_in_env(env_name)
    if not ok_torch:
        print(f"❌ PyTorch check failed: {msg_torch}")
        return 1

    print(f"✅ PyTorch import/smoke test passed: version={torch_info.get('torch_version')}")
    print(f"   cuda_compiled={torch_info.get('cuda_compiled')}, cuda_available={torch_info.get('cuda_available')}")

    has_gpu, gpu_reason = host_has_gpu()
    print(f"Host GPU present: {has_gpu} ({gpu_reason})")

    if has_gpu:
        if not torch_info.get("cuda_available", False):
            print("❌ Host has GPU but torch.cuda.is_available() is False")
            return 1

        ok_gpu, msg_gpu = check_gpu_compute(env_name)
        if not ok_gpu:
            print(f"❌ GPU compute check failed: {msg_gpu}")
            return 1

        print("✅ GPU compute check passed")

    print("=" * 70)
    print("✅ PASS")
    return 0


if __name__ == "__main__":
    sys.exit(grade())
