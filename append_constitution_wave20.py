#!/usr/bin/env python3
"""Append wave-20 constitution questions (20 PSC topic types only)."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from coi_wave20_facts import generate_wave20_candidates
from refill_common import load_global_stems, max_id_num, spread_consecutive_templates

BASE = Path(__file__).parent
FILE = "constitution_of_india.json"
PREFIX = "coi_"
TARGET = 3000
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def main() -> int:
    path = BASE / FILE
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.setdefault("questions", [])
    global_stems = load_global_stems(FILE)
    existing = {q["question"].strip() for q in questions}
    existing.update(global_stems)
    n = max_id_num(questions, PREFIX)

    rng = random.Random(42)
    pool = generate_wave20_candidates(set(existing), rng)
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
        questions.append(
            {
                "id": f"{PREFIX}{n:04d}",
                "question": item["question"],
                "options": item["options"],
                "answer": item["answer"],
                "difficulty": item["difficulty"],
            }
        )
        existing.add(item["question"])
        added += 1

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{FILE}: +{added} (pool={len(pool)}, picked={len(picked)}, target={TARGET})")
    if added < TARGET:
        print(f"SHORTFALL: need {TARGET - added} more unique candidates")
        return 1

    subprocess.run([sys.executable, "apply_malayalam_rules.py", FILE], cwd=BASE, check=False)
    r = subprocess.run([sys.executable, "validate_questions.py", FILE], cwd=BASE)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
