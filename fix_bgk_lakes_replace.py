#!/usr/bin/env python3
"""Replace corrupted LAKES_STATE questions with unique MUSICAL_INSTRUMENTS items."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from basic_gk_wave30_facts import LAKES_STATE, MUSICAL_INSTRUMENTS
from refill_common import pick3

BASE = Path(__file__).parent
FILE = "basic_general_knowledge.json"

REAL_LAKES: set[str] = set()
REAL_STATES: set[str] = set()
for lake, state in LAKES_STATE:
    if lake == "അഫ്ഗാനിസ്ഥാൻ":
        break
    REAL_LAKES.add(lake)
    REAL_STATES.add(state)

REV_PAT = re.compile(r"'([^']+)' സംസ്ഥാനത്തുള്ള ജലാശയം\?$")
FWD_PAT = re.compile(r"'([^']+)' തടാകം ഏത് സംസ്ഥാനത്താണ്\?$")

FWD_TEMPLATES = [
    "'{a}'-ന്റെ ഉത്ഭവദേശം ഏത്?",
    "'{a}' ഏത് പ്രദേശത്ത് നിന്നാണ് ഉത്ഭവിച്ചത്?",
    "'{a}'-ന്റെ മൂലദേശം ഏത്?",
]
REV_TEMPLATES = [
    "'{b}'-ൽ നിന്ന് ഉത്ഭവിച്ച വാദ്യോപകരണം ഏത്?",
    "'{b}' ഏത് വാദ്യോപകരണത്തിന്റെ ഉത്ഭവദേശം?",
    "'{b}'-ന് ഏത് വാദ്യം?",
]

INSTRUMENT_POOL = sorted({a for a, _ in MUSICAL_INSTRUMENTS})
REGION_POOL = sorted({b for _, b in MUSICAL_INSTRUMENTS})


def is_broken_lakes(q: dict) -> bool:
    stem = q.get("question", "").strip()
    answer = q.get("answer", "").strip()
    m = REV_PAT.match(stem)
    if m:
        label = m.group(1)
        return label not in REAL_STATES or answer not in REAL_LAKES
    m = FWD_PAT.match(stem)
    if m:
        return m.group(1) not in REAL_LAKES
    return False


def _candidates(existing: set[str]) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for instrument, region in MUSICAL_INSTRUMENTS:
        for tmpl in FWD_TEMPLATES:
            stem = tmpl.format(a=instrument)
            if stem not in existing:
                out.append((stem, region, "region"))
        for tmpl in REV_TEMPLATES:
            stem = tmpl.format(b=region)
            if stem not in existing:
                out.append((stem, instrument, "instrument"))
    return out


def main() -> int:
    rng = random.Random(42)
    path = BASE / FILE
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.get("questions", [])

    existing = {q.get("question", "").strip() for q in questions if q.get("question")}
    candidates = _candidates(existing)
    rng.shuffle(candidates)

    replaced = 0
    used_stems: set[str] = set()
    cand_idx = 0

    for q in questions:
        if not is_broken_lakes(q):
            continue
        while cand_idx < len(candidates):
            stem, answer, kind = candidates[cand_idx]
            cand_idx += 1
            if stem in existing or stem in used_stems:
                continue
            pool = REGION_POOL if kind == "region" else INSTRUMENT_POOL
            opts = pick3(pool, answer, rng)
            rng.shuffle(opts)
            q["question"] = stem
            q["options"] = opts
            q["answer"] = answer
            existing.add(stem)
            used_stems.add(stem)
            replaced += 1
            break

    if replaced < sum(1 for q in questions if is_broken_lakes(q)):
        print(f"warning: only {replaced} replacements generated", file=sys.stderr)

    data["questions"] = questions
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{FILE}: replaced {replaced} corrupted lake questions with MUSICAL_INSTRUMENTS")

    result = subprocess.run(
        [sys.executable, str(BASE / "validate_questions.py"), FILE],
        cwd=BASE,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
