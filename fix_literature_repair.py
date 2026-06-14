#!/usr/bin/env python3
"""Remove invalid literature questions and backfill from wave facts."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from apply_malayalam_rules import validate_file
from giveaway_utils import is_answer_in_stem_giveaway
from literature_wave_facts import generate_wave_candidates
from refill_common import load_global_stems, spread_consecutive_templates

BASE = Path(__file__).parent
FILE = "literature.json"
PREFIX = "lit_"
TARGET_TOTAL = 3093  # 93 original + 3000 new
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def is_bad(q: dict) -> bool:
    stem = q.get("question", "").strip()
    opts = q.get("options", [])
    ans = q.get("answer", "")
    if not stem or len(opts) != 4 or ans not in opts or len(set(opts)) != 4:
        return True
    if is_answer_in_stem_giveaway(stem, ans):
        return True
    if MIXED.search(stem + "".join(opts) + ans):
        return True
    return False


def main() -> int:
    path = BASE / FILE
    data = json.loads(path.read_text(encoding="utf-8"))
    kept = [q for q in data.get("questions", []) if not is_bad(q)]
    removed = len(data.get("questions", [])) - len(kept)
    print(f"Removed {removed} invalid rows")

    existing = load_global_stems(FILE)
    existing.update(q.get("question", "").strip() for q in kept if q.get("question"))

    rng = random.Random(99)
    pool = generate_wave_candidates(set(existing), rng)
    rng.shuffle(pool)

    need = TARGET_TOTAL - len(kept)
    added = 0
    seen = {q.get("question", "").strip() for q in kept}
    new_rows: list[dict] = []
    for q, opts, ans, diff in pool:
        if added >= need:
            break
        if q in existing or q in seen:
            continue
        if len(set(opts)) != 4 or ans not in opts:
            continue
        if is_bad({"question": q, "options": opts, "answer": ans}):
            continue
        new_rows.append({"question": q, "options": opts, "answer": ans, "difficulty": diff})
        seen.add(q)
        added += 1

    combined = kept + spread_consecutive_templates(new_rows, rng, max_run=2)
    final: list[dict] = []
    seen_stems: set[str] = set()
    for i, q in enumerate(combined, start=1):
        stem = q.get("question", "").strip()
        if not stem or stem in seen_stems or is_bad(q):
            continue
        seen_stems.add(stem)
        entry = dict(q)
        entry["id"] = f"{PREFIX}{i:04d}"
        final.append(entry)

    data["questions"] = final
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{FILE}: {len(final)} questions (backfilled {added}, target {TARGET_TOTAL})")

    subprocess.run([sys.executable, "apply_malayalam_rules.py", FILE], cwd=BASE, check=False)
    issues = validate_file(FILE)
    if issues:
        print(f"Remaining issues: {len(issues)}")
        for qid, code, detail in issues[:20]:
            print(f"  [{qid}] {code}: {detail}")
        return 1

    r = subprocess.run([sys.executable, "validate_questions.py", FILE], cwd=BASE)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
