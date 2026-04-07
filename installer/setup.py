#!/usr/bin/env python3
"""
NeuroClaw Setup Entry Point

Usage:
    python installer/setup.py          # Interactive wizard
    python installer/setup.py --check  # Validate existing neuroclaw_environment.json
    python installer/setup.py --non-interactive  # Write defaults without prompting

This script is the primary entry point for installing and configuring NeuroClaw
as a self-contained system. It does NOT require OpenClaw to be pre-installed.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
ENV_FILE = REPO_ROOT / "neuroclaw_environment.json"
FEATURES_FILE = REPO_ROOT / "core" / "config" / "features.json"
DEFAULTS_FILE = Path(__file__).parent / "neuro_defaults.json"

# Minimum Python version required by NeuroClaw
MIN_PYTHON = (3, 10)


def _check_python_version() -> None:
    if sys.version_info < MIN_PYTHON:
        print(
            f"ERROR: NeuroClaw requires Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+. "
            f"Current: {sys.version_info.major}.{sys.version_info.minor}"
        )
        sys.exit(1)


def _check_existing_config() -> int:
    """Validate an existing neuroclaw_environment.json. Returns 0 on success."""
    if not ENV_FILE.exists():
        print(f"No configuration found at {ENV_FILE}.")
        print("Run:  python installer/setup.py  to create one.")
        return 1

    with ENV_FILE.open() as f:
        config = json.load(f)

    issues: list[str] = []

    # Python path
    python_path = config.get("python_path")
    if python_path and not Path(python_path).exists():
        py_path_display = str(python_path)
        issues.append(f"python_path not found: {py_path_display}")

    # LLM backend key env var
    llm = config.get("llm_backend", {})
    key_env = llm.get("api_key_env")
    if key_env and not os.environ.get(key_env) and llm.get("provider") in ("openai", "anthropic"):
        issues.append(
            f"LLM API key env var '{key_env}' is not set. "
            f"Export it before running NeuroClaw."
        )

    # Toolchain paths (warn only)
    toolchain = config.get("toolchain", {})
    for name, path in toolchain.items():
        if path and not Path(path).exists():
            issues.append(f"toolchain.{name} path not found: {path}  (warning — optional)")

    if issues:
        print("Configuration check — issues found:")
        for issue in issues:
            print(f"  ⚠  {issue}")
        return 1

    print(f"Configuration at {ENV_FILE} looks valid.")
    _print_summary(config)
    return 0


def _write_defaults() -> None:
    """Write neuro_defaults.json template as neuroclaw_environment.json without prompting."""
    if not DEFAULTS_FILE.exists():
        print(f"ERROR: defaults template not found at {DEFAULTS_FILE}")
        sys.exit(1)

    with DEFAULTS_FILE.open() as f:
        config = json.load(f)

    # Fill in detected values
    config["python_path"] = sys.executable

    # Detect CUDA
    nvcc = shutil.which("nvcc")
    if nvcc:
        result = subprocess.run(
            ["nvcc", "--version"], capture_output=True, text=True
        )
        for token in result.stdout.replace(",", " ").split():
            if "." in token and token.replace(".", "").isdigit():
                config["cuda"]["version"] = token
                short = "".join(token.split(".")[:2])
                config["cuda"]["torch_build"] = f"cu{short}"
                config["cuda"]["device"] = "cuda:0"
                break

    ENV_FILE.write_text(json.dumps(config, indent=2) + "\n")
    print(f"Default configuration written to {ENV_FILE}")
    print("Edit the file or re-run the interactive wizard to customise settings.")


def _print_summary(config: dict) -> None:
    print("\n── NeuroClaw Environment Summary ──────────────────────────")
    print(f"  Setup type  : {config.get('setup_type')}")
    print(f"  Python      : {config.get('python_path')}")
    if config.get("conda_env"):
        print(f"  Conda env   : {config.get('conda_env')}")
    cuda = config.get("cuda", {})
    if cuda.get("version"):
        print(f"  CUDA        : {cuda.get('version')}  build={cuda.get('torch_build')}  device={cuda.get('device')}")
    else:
        print("  CUDA        : cpu-only")
    llm = config.get("llm_backend", {})
    print(f"  LLM backend : {llm.get('provider')} / {llm.get('model')}")
    tc = config.get("toolchain", {})
    enabled_tools = [k for k, v in tc.items() if v]
    if enabled_tools:
        print(f"  Toolchain   : {', '.join(enabled_tools)}")
    print("────────────────────────────────────────────────────────────\n")


def main() -> None:
    _check_python_version()

    parser = argparse.ArgumentParser(
        description="NeuroClaw Setup — configure the self-contained neuroscience AI assistant."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate existing neuroclaw_environment.json and exit.",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Write default configuration without interactive prompts.",
    )
    args = parser.parse_args()

    if args.check:
        sys.exit(_check_existing_config())

    if args.non_interactive:
        _write_defaults()
        sys.exit(0)

    # Default: run the interactive wizard
    wizard_path = Path(__file__).parent / "config_wizard.py"
    result = subprocess.run([sys.executable, str(wizard_path)], check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
