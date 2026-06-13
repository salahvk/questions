#!/usr/bin/env python3
"""Repo-wide fix: remove filler, fix structure, apply Malayalam rules, refill geography."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from apply_malayalam_rules import process_file, validate_file
from validate_questions import FILLER_PATTERNS, load_questions

BASE = Path(__file__).parent
SKIP = {"english_language.json", "current_affairs_manifest.json"}

DUPLICATE_OPTION_FIXES: dict[str, list[str]] = {
    "phy_047": ["വാട്ട്", "ജൂൾ", "ന്യൂട്ടൺ", "കെൽവിൻ"],
    "phy_051": ["ജൂൾ", "ന്യൂട്ടൺ", "വാട്ട്", "ആംപിയർ"],
    "phy_053": ["വാട്ട്", "ന്യൂട്ടൺ", "ജൂൾ", "കൂളോം"],
}


def is_filler_question(q: dict) -> bool:
    text = (
        q.get("question", "")
        + " "
        + " ".join(q.get("options", []))
        + " "
        + q.get("answer", "")
    )
    return any(p.search(text) for p in FILLER_PATTERNS)


def remove_filler(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    before = len(data.get("questions", []))
    kept = [q for q in data.get("questions", []) if not is_filler_question(q)]
    removed = before - len(kept)
    if removed:
        data["questions"] = kept
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return removed


def fix_duplicate_options(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    fixed = 0
    for q in data.get("questions", []):
        qid = q.get("id", "")
        if qid in DUPLICATE_OPTION_FIXES:
            q["options"] = DUPLICATE_OPTION_FIXES[qid]
            fixed += 1
            continue
        opts = q.get("options", [])
        if len(opts) == 4 and len(set(opts)) < 4:
            seen: set[str] = set()
            new_opts: list[str] = []
            for opt in opts:
                if opt in seen:
                    continue
                seen.add(opt)
                new_opts.append(opt)
            pool = ["ഒന്നും അല്ല", "ബന്ധമില്ല", "വ്യത്യസ്തം", "മറ്റൊന്ന്"]
            i = 0
            while len(new_opts) < 4 and i < len(pool):
                if pool[i] not in new_opts and pool[i] != q.get("answer"):
                    new_opts.append(pool[i])
                i += 1
            q["options"] = new_opts[:4]
            fixed += 1
    if fixed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return fixed


def run_script(name: str) -> None:
    script = BASE / name
    if not script.exists():
        return
    subprocess.run([sys.executable, str(script)], cwd=BASE, check=True)


def main() -> int:
    paths = sorted(p for p in BASE.glob("*.json") if p.name not in SKIP)

    print("Step 1: Remove filler questions")
    total_removed = 0
    for path in paths:
        n = remove_filler(path)
        if n:
            print(f"  {path.name}: removed {n} filler")
            total_removed += n
    print(f"  Total filler removed: {total_removed}\n")

    print("Step 2: Fix duplicate options")
    for path in paths:
        n = fix_duplicate_options(path)
        if n:
            print(f"  {path.name}: fixed {n}")

    print("\nStep 3: Fix economics filler")
    run_script("fix_economics_questions.py")

    print("\nStep 4: Apply Malayalam rules to all files")
    for path in paths:
        if path.exists():
            stats = process_file(path.name)
            issues = len(validate_file(path.name))
            print(
                f"  {path.name}: {stats['total']} q, "
                f"{stats['updated']} updated, {issues} malayalam issues"
            )

    print("\nStep 5: Refill geography")
    run_script("refill_geography_unique.py")

    print("\nStep 6: Re-apply Malayalam rules after geography refill")
    process_file("geography.json")

    print("\nStep 7: Validate all")
    result = subprocess.run(
        [sys.executable, str(BASE / "validate_questions.py")],
        cwd=BASE,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
