#!/usr/bin/env python3
"""Append 1000 wave-4 geography questions to geography.json."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from geo_wave4_facts import generate_wave4_candidates
from refill_common import load_global_stems, max_id_num, spread_consecutive_templates

BASE = Path(__file__).parent
FILE = "geography.json"
PREFIX = "geo_"
TARGET = 1000
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def main() -> int:
    path = BASE / FILE
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.setdefault("questions", [])
    global_stems = load_global_stems(path)
    existing = {q["question"].strip() for q in questions}
    existing.update(global_stems)
    n = max_id_num(questions, PREFIX)

    rng = random.Random(42)
    pool = generate_wave4_candidates(set(existing), rng)
    rng.shuffle(pool)

    picked: list[dict] = []
    seen: set[str] = set()
    for q, opts, ans, diff in pool:
        if len(picked) >= TARGET:
            break
        if q in existing or q in seen:
            continue
        if len(set(opts)) != 4 or ans not in opts:
            continue
        if MIXED.search(q + "".join(opts) + ans):
            continue
        picked.append({"question": q, "options": opts, "answer": ans, "difficulty": diff})
        seen.add(q)

    spread = spread_consecutive_templates(picked, rng, max_run=2)
    added = 0
    for item in spread:
        n += 1
        entry = {
            "id": f"{PREFIX}{n:04d}",
            "question": item["question"],
            "options": item["options"],
            "answer": item["answer"],
            "difficulty": item["difficulty"],
        }
        questions.append(entry)
        existing.add(item["question"])
        added += 1

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{FILE}: +{added} (pool={len(pool)}, picked={len(picked)})")
    subprocess.run([sys.executable, "apply_malayalam_rules.py", FILE], cwd=BASE, check=False)
    r = subprocess.run([sys.executable, "validate_questions.py", FILE], cwd=BASE)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
