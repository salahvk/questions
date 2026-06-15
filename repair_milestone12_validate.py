#!/usr/bin/env python3
"""Purge invalid rows from 12 milestone banks and backfill to 1,500 validated questions."""

from __future__ import annotations

import importlib
import json
import random
import re
import subprocess
import sys
from pathlib import Path

from apply_malayalam_rules import (
    BANNED_OPTION_ENGLISH,
    MALAYALAM,
    SKIP_FILES,
    WORK_TITLE_OPTION,
    strip_for_validation,
)
from refill_common import (
    id_width,
    interleave_candidates,
    is_filler_question,
    load_global_stems,
    make_entry,
    spread_consecutive_templates,
)
from refill_milestone12_1500 import TARGET, WAVE30_MODULES, candidates_for
from validate_questions import (
    english_language_issues,
    fact_trap_issues,
    filler_issues,
    option_mismatch_issues,
    structural_issues,
)

BASE = Path(__file__).parent


def malayalam_row_issues(q: dict, filename: str) -> list[str]:
    if filename in SKIP_FILES:
        return []
    qid = q.get("id", "?")
    question = q.get("question", "")
    opts = q.get("options", [])
    ans = q.get("answer", "")
    issues: list[str] = []

    if not MALAYALAM.search(question):
        issues.append("english_only_question")
    elif re.search(r"[a-zA-Z]{4,}", strip_for_validation(question)):
        issues.append("mixed_language_stem")

    has_malayalam_option = any(MALAYALAM.search(o) for o in opts)
    all_options_english_titles = (
        not any(MALAYALAM.search(o) for o in opts)
        and all(re.search(r"[a-zA-Z]", o) for o in opts)
    )
    for opt in opts:
        if BANNED_OPTION_ENGLISH.search(opt):
            issues.append("english_option_leak")
        elif (
            has_malayalam_option
            and not all_options_english_titles
            and not MALAYALAM.search(opt)
            and WORK_TITLE_OPTION.match(opt.strip())
        ):
            pass
        elif (
            has_malayalam_option
            and not all_options_english_titles
            and not MALAYALAM.search(opt)
            and re.search(r"[a-zA-Z]{4,}", opt)
            and not re.fullmatch(r"[\d%./\s\-+()A-Za-z]+", opt)
            and not re.search(
                r"\b(?:Front|Forum|Force|Defence|Development|Union|Liberal|Local|Left|Unified)\b",
                opt,
            )
        ):
            issues.append("mixed_language_options")

    from apply_malayalam_rules import PRESERVE

    for text in [question, *opts, ans]:
        cleaned = strip_for_validation(text)
        cleaned = PRESERVE.sub("", cleaned)
        if re.search(r"[a-zA-Z]{4,}", cleaned) and MALAYALAM.search(text):
            issues.append("english_leak")
            break

    return [f"malayalam:{x}" for x in issues]


def row_issues(q: dict, filename: str) -> list[str]:
    qid = q.get("id", "?")
    out: list[str] = []
    for _, code in (
        structural_issues(q, qid)
        + filler_issues(q, qid)
        + option_mismatch_issues(q, qid)
        + fact_trap_issues(q, qid, filename)
        + english_language_issues(q, qid, filename)
    ):
        out.append(code)
    out.extend(malayalam_row_issues(q, filename))
    return out


def is_valid_row(q: dict, filename: str) -> bool:
    if is_filler_question(q):
        return False
    return not row_issues(q, filename)


def repair_file(filename: str, prefix: str, module: str, rng: random.Random) -> dict:
    path = BASE / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    global_stems = load_global_stems(exclude_file=filename)

    kept: list[dict] = []
    local_stems: set[str] = set()
    for q in data.get("questions", []):
        stem = q.get("question", "").strip()
        if not stem or stem in global_stems or stem in local_stems:
            continue
        if not is_valid_row(q, filename):
            continue
        kept.append(q)
        local_stems.add(stem)

    removed = len(data.get("questions", [])) - len(kept)
    existing = global_stems | local_stems
    width = id_width(TARGET)

    def try_add(candidates: list) -> int:
        added = 0
        for q_text, opts, ans, diff in candidates:
            if len(kept) >= TARGET:
                break
            if q_text in existing:
                continue
            entry = make_entry(prefix, len(kept) + 1, q_text, opts, ans, diff, width)
            if not is_valid_row(entry, filename):
                continue
            kept.append(entry)
            existing.add(q_text)
            added += 1
        return added

    seed_rng = random.Random(rng.randint(0, 10**9))
    added = try_add(candidates_for(module, existing, seed_rng))
    rounds = 0
    while len(kept) < TARGET and rounds < 8:
        rounds += 1
        seed_rng = random.Random(rng.randint(0, 10**9))
        extra = try_add(candidates_for(module, existing, seed_rng))
        if extra == 0:
            break
        added += extra

    final = spread_consecutive_templates(kept[:TARGET], rng, max_run=2)
    for i, q in enumerate(final[:TARGET], start=1):
        q["id"] = f"{prefix}{i:0{width}d}"

    data["questions"] = final[:TARGET]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "file": filename,
        "removed": removed,
        "added": added,
        "final": len(final[:TARGET]),
        "shortfall": max(0, TARGET - len(final[:TARGET])),
    }


def main() -> int:
    rng = random.Random(99)
    print("=" * 60)
    print("REPAIR milestone 12 banks — validated refill to 1500")
    print("=" * 60)

    shortfalls: list[str] = []
    for filename, (prefix, module) in WAVE30_MODULES.items():
        rep = repair_file(filename, prefix, module, rng)
        print(
            f"{filename}: removed {rep['removed']}, +{rep['added']} "
            f"→ {rep['final']}/{TARGET} (shortfall {rep['shortfall']})"
        )
        if rep["shortfall"]:
            shortfalls.append(f"{filename}: need {rep['shortfall']} more valid facts")

    print("\n--- apply_malayalam_rules.py (12 files) ---")
    files = list(WAVE30_MODULES.keys())
    subprocess.run(
        [sys.executable, str(BASE / "apply_malayalam_rules.py"), *files],
        cwd=BASE,
        check=True,
    )

    print("\n--- validate_questions.py (12 files) ---")
    result = subprocess.run(
        [sys.executable, str(BASE / "validate_questions.py"), *files],
        cwd=BASE,
    )

    if shortfalls:
        print("\nSHORTFALLS:")
        for s in shortfalls:
            print(f"  • {s}")
    return result.returncode if not shortfalls else 1


if __name__ == "__main__":
    raise SystemExit(main())
