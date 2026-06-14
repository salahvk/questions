#!/usr/bin/env python3
"""Refill cinema.json with unique factual Malayalam PSC-style questions."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from cinema_facts import generate_candidates
from cinema_ml_check import passes_malayalam_qc
from giveaway_utils import is_answer_in_stem_giveaway
from refill_common import interleave_candidates, spread_consecutive_templates

BASE = Path(__file__).parent
TARGET = 2886  # 186 existing + 2700 new
PREFIX = "cin_"

FILLER_PATTERNS = [
    re.compile(r"സിനിമ-\d+"),
    re.compile(r"ചിത്രം-\d+"),
    re.compile(r"വസ്തുത-\d+"),
    re.compile(r"പ്രദേശം-\d+"),
    re.compile(r"ഏത് ചോദ്യത്തിന്റെ ഉത്തരമാണ്"),
]


def is_filler(question: str) -> bool:
    return any(p.search(question) for p in FILLER_PATTERNS)


def is_bad_kept(question: str, options: list[str], answer: str) -> bool:
    if is_filler(question):
        return True
    if is_answer_in_stem_giveaway(question, answer):
        return True
    if not passes_malayalam_qc(question, options, answer):
        return True
    if re.search(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]", question + answer + " ".join(options)):
        return True
    return False


def load_global_existing() -> set[str]:
    existing: set[str] = set()
    for path in BASE.glob("*.json"):
        if path.name == "cinema.json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for q in data.get("questions", []):
            stem = q.get("question", "").strip()
            if stem:
                existing.add(stem)
    return existing


def make_entry(num: int, q: str, opts: list[str], ans: str, diff: str) -> dict:
    shuffled = list(opts)
    random.shuffle(shuffled)
    width = max(4, len(str(TARGET)))
    return {
        "id": f"{PREFIX}{num:0{width}d}",
        "question": q,
        "options": shuffled,
        "answer": ans,
        "difficulty": diff,
    }


def main() -> int:
    rng = random.Random(42)
    path = BASE / "cinema.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    kept = [
        q for q in data.get("questions", [])
        if not is_bad_kept(q.get("question", ""), q.get("options", []), q.get("answer", ""))
    ]
    existing: set[str] = {q.get("question", "").strip() for q in kept if q.get("question")}
    existing.update(load_global_existing())

    candidates = interleave_candidates(generate_candidates(existing, rng), rng)
    rng.shuffle(candidates)

    combined: list[dict] = list(kept)
    seen = {q.get("question", "").strip() for q in combined}

    for q, opts, ans, diff in candidates:
        if len(combined) >= TARGET:
            break
        if q in seen:
            continue
        combined.append(make_entry(len(combined) + 1, q, opts, ans, diff))
        seen.add(q)

    if len(combined) < TARGET:
        print(
            f"ERROR: only {len(combined)} questions (target {TARGET}); "
            f"shortfall {TARGET - len(combined)} — add verified facts, never pad.",
            file=sys.stderr,
        )
        return 1

    # dedupe + re-id
    final: list[dict] = []
    seen_stems: set[str] = set()
    width = max(4, len(str(TARGET)))
    for i, q in enumerate(combined[:TARGET], start=1):
        stem = q.get("question", "").strip()
        if not stem or stem in seen_stems:
            continue
        seen_stems.add(stem)
        entry = dict(q)
        entry["id"] = f"{PREFIX}{i:0{width}d}"
        final.append(entry)

    final = spread_consecutive_templates(final, rng, max_run=2)
    for i, q in enumerate(final, start=1):
        q["id"] = f"{PREFIX}{i:0{width}d}"

    data["questions"] = final
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    added = len(final) - len(kept)
    print(f"cinema.json: kept {len(kept)}, added {added}, total {len(final)} (target {TARGET})")

    subprocess.run([sys.executable, str(BASE / "apply_malayalam_rules.py"), "cinema.json"], cwd=BASE, check=False)
    result = subprocess.run([sys.executable, str(BASE / "validate_questions.py"), "cinema.json"], cwd=BASE)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
