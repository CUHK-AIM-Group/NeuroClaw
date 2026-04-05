#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 7: Multi Search Engine Recipe Summarization.

Scoring focus:
1. Output file exists in benchmark_results/T07_multi_search_engine/
2. Generated content is a spicy chicken recipe
3. Recipe contains ordered steps (>= 3)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
RESULT_DIR = ROOT / "benchmark_results" / "T07_multi_search_engine"


def pick_latest_result_file() -> Optional[Path]:
    if not RESULT_DIR.exists() or not RESULT_DIR.is_dir():
        return None

    candidates: List[Path] = []
    for ext in ["result_*.json", "*.json", "*.md", "*.txt"]:
        candidates.extend(RESULT_DIR.glob(ext))

    if not candidates:
        return None

    candidates = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


def normalize_text(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def extract_steps_from_text(content: str) -> List[str]:
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]

    # Numbered steps: "1. ...", "1) ...", "步骤1: ..."
    step_pattern = re.compile(r"^(?:step\s*\d+|步骤\s*\d+|\d+[\.|\)|、])\s*[:：]?\s*(.+)$", re.IGNORECASE)
    steps: List[str] = []

    for ln in lines:
        m = step_pattern.match(ln)
        if m:
            body = m.group(1).strip()
            if body:
                steps.append(body)

    # Fallback: bullet list under a "steps/步骤" section
    if len(steps) < 3:
        lower = content.lower()
        marker_idx = max(lower.find("steps"), lower.find("步骤"))
        if marker_idx != -1:
            section = content[marker_idx:]
            for ln in section.splitlines()[1:]:
                ln = ln.strip()
                if not ln:
                    continue
                if re.match(r"^[-*]\s+", ln):
                    steps.append(re.sub(r"^[-*]\s+", "", ln).strip())
                elif re.match(r"^\d+[\.|\)|、]\s+", ln):
                    steps.append(re.sub(r"^\d+[\.|\)|、]\s+", "", ln).strip())
                if len(steps) >= 10:
                    break

    # Deduplicate while preserving order
    dedup = []
    seen = set()
    for s in steps:
        key = normalize_text(s)
        if key and key not in seen:
            seen.add(key)
            dedup.append(s)

    return dedup


def grade_json(path: Path) -> Tuple[bool, str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"invalid JSON: {e}"

    recipe = data.get("recipe") if isinstance(data, dict) else None
    if not isinstance(recipe, dict):
        return False, "missing key: recipe"

    title = str(recipe.get("title", "")).strip()
    ingredients = recipe.get("ingredients", [])
    steps = recipe.get("steps", [])

    if not title:
        return False, "recipe.title is empty"

    if not isinstance(ingredients, list) or len(ingredients) == 0:
        return False, "recipe.ingredients is missing or empty"

    if not isinstance(steps, list):
        return False, "recipe.steps must be a list"

    cleaned_steps = [str(s).strip() for s in steps if str(s).strip()]
    if len(cleaned_steps) < 3:
        return False, f"recipe.steps too short: {len(cleaned_steps)} (< 3)"

    joined = normalize_text(title + " " + " ".join(cleaned_steps))
    spicy_keywords = ["spicy", "chili", "pepper", "辣", "麻辣"]
    chicken_keywords = ["chicken", "鸡"]

    if not any(k in joined for k in spicy_keywords):
        return False, "recipe does not look spicy"

    if not any(k in joined for k in chicken_keywords):
        return False, "recipe does not look like chicken recipe"

    return True, f"valid JSON recipe with {len(cleaned_steps)} steps"


def grade_text(path: Path) -> Tuple[bool, str]:
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"cannot read file: {e}"

    steps = extract_steps_from_text(content)
    if len(steps) < 3:
        return False, f"not enough detected steps: {len(steps)} (< 3)"

    normalized = normalize_text(content)
    spicy_keywords = ["spicy", "chili", "pepper", "辣", "麻辣"]
    chicken_keywords = ["chicken", "鸡"]

    if not any(k in normalized for k in spicy_keywords):
        return False, "content does not look spicy"

    if not any(k in normalized for k in chicken_keywords):
        return False, "content does not look like chicken recipe"

    return True, f"valid text recipe with {len(steps)} steps"


def grade() -> int:
    print("=" * 70)
    print("Benchmark Test Case 7: Multi Search Engine Recipe Summarization")
    print("=" * 70)

    result_file = pick_latest_result_file()
    if result_file is None:
        print(f"❌ No result file found in {RESULT_DIR}")
        return 1

    print(f"Using result file: {result_file}")

    if result_file.suffix.lower() == ".json":
        ok, msg = grade_json(result_file)
    else:
        ok, msg = grade_text(result_file)

    if not ok:
        print(f"❌ FAIL: {msg}")
        return 1

    print(f"✅ PASS: {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(grade())
