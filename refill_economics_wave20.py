#!/usr/bin/env python3
"""Append wave20 economics facts — 2200 new unique PSC questions."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from giveaway_utils import is_answer_in_stem_giveaway
from refill_common import (
    interleave_candidates,
    is_filler_question,
    load_global_stems,
    spread_consecutive_templates,
)
from economics_wave20_facts import generate_wave20_candidates

try:
    from apply_malayalam_rules import (
        BANNED_OPTION_ENGLISH,
        MALAYALAM,
        strip_for_validation,
    )
except ImportError:
    BANNED_OPTION_ENGLISH = None
    MALAYALAM = re.compile(r"[\u0D00-\u0D7F]")
    strip_for_validation = None

BASE = Path(__file__).parent
FILENAME = "economics.json"
PREFIX = "eco_"
ADD_TARGET = 2200

ENGLISH_LEAK = re.compile(r"[a-zA-Z]{4,}")
MIXED_SCRIPT = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")
ALLOWED_ENGLISH = re.compile(
    r"\b(RBI|SEBI|GST|IMF|WTO|CPI|GDP|GNP|FDI|FII|HDI|MSP|NPS|UPI|NPCI|FRBM|SEZ|PLI|"
    r"PMJDY|CRR|SLR|MSF|OMO|LAF|WPI|IIP|BSE|NSE|LIC|IRDAI|EPFO|ESI|PFRDA|NITI|"
    r"FCI|PDS|MGNREGA|LPG|BOP|IPO|Nifty|Sensex|July|January|April|March|Wealth|"
    r"General|Theory|Nations|Capital|Keynes|Smith|Marshall|Fisher|Sen)\b",
    re.I,
)


def is_bad_kept(question: str, options: list[str], answer: str) -> bool:
    if is_filler_question({"question": question, "options": options, "answer": answer}):
        return True
    if is_answer_in_stem_giveaway(question, answer):
        return True
    if strip_for_validation is None:
        return False
    if not MALAYALAM.search(question):
        return True
    for text in [question, *options, answer]:
        if MIXED_SCRIPT.search(text):
            return True
        cleaned = strip_for_validation(text)
        if ENGLISH_LEAK.search(cleaned):
            leak = ENGLISH_LEAK.search(cleaned)
            if leak and not ALLOWED_ENGLISH.search(text):
                return True
    if BANNED_OPTION_ENGLISH:
        for opt in options:
            if BANNED_OPTION_ENGLISH.search(opt):
                return True
    return False


def make_entry(num: int, q: str, opts: list[str], ans: str, diff: str, width: int) -> dict:
    shuffled = list(opts)
    random.shuffle(shuffled)
    return {
        "id": f"{PREFIX}{num:0{width}d}",
        "question": q,
        "options": shuffled,
        "answer": ans,
        "difficulty": diff,
    }


def main() -> int:
    rng = random.Random(42)
    path = BASE / FILENAME
    data = json.loads(path.read_text(encoding="utf-8"))

    kept: list[dict] = []
    kept_stems: set[str] = set()
    for q in data.get("questions", []):
        stem = q.get("question", "").strip()
        opts = q.get("options", [])
        ans = q.get("answer", "")
        if stem and stem not in kept_stems and not is_bad_kept(stem, opts, ans):
            kept.append(dict(q))
            kept_stems.add(stem)

    target = len(kept) + ADD_TARGET
    existing = load_global_stems(exclude_file=FILENAME) | kept_stems
    candidates = interleave_candidates(generate_wave20_candidates(existing, rng), rng)

    combined: list[dict] = list(kept)
    width = max(4, len(str(target)))

    for q, opts, ans, diff in candidates:
        if len(combined) >= target:
            break
        if q in kept_stems or is_bad_kept(q, opts, ans):
            continue
        combined.append(make_entry(len(combined) + 1, q, opts, ans, diff, width))
        kept_stems.add(q)

    if len(combined) < target:
        extra_existing = kept_stems | {q.get("question", "").strip() for q in combined}
        extra = interleave_candidates(
            generate_wave20_candidates(extra_existing, random.Random(rng.randint(0, 10**9))),
            rng,
        )
        for q, opts, ans, diff in extra:
            if len(combined) >= target:
                break
            if q in kept_stems or is_bad_kept(q, opts, ans):
                continue
            combined.append(make_entry(len(combined) + 1, q, opts, ans, diff, width))
            kept_stems.add(q)

    combined = spread_consecutive_templates(combined, rng, max_run=2)

    final: list[dict] = []
    seen: set[str] = set()
    for q in combined:
        stem = q.get("question", "").strip()
        if not stem or stem in seen or is_bad_kept(stem, q.get("options", []), q.get("answer", "")):
            continue
        seen.add(stem)
        entry = dict(q)
        entry["id"] = f"{PREFIX}{len(final) + 1:0{width}d}"
        final.append(entry)

    data["questions"] = final
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    added = len(final) - len(kept)
    print(
        f"{FILENAME}: {len(final)} questions "
        f"(kept {len(kept)}, added {added}, target +{ADD_TARGET})"
    )
    dupes = len(final) - len({q["question"] for q in final})
    print(f"duplicate stems: {dupes}")

    if added < ADD_TARGET:
        print(f"WARNING: shortfall of {ADD_TARGET - added} questions")

    print("\n--- apply_malayalam_rules.py ---")
    subprocess.run([sys.executable, str(BASE / "apply_malayalam_rules.py"), FILENAME], cwd=BASE)

    print("\n--- validate_questions.py ---")
    result = subprocess.run(
        [sys.executable, str(BASE / "validate_questions.py"), FILENAME],
        cwd=BASE,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
