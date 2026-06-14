#!/usr/bin/env python3
"""Keep valid arts.json questions and refill with wave20 + legacy unique facts."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from arts_wave20_facts import generate_wave20_candidates
from refill_common import (
    interleave_candidates,
    is_filler_question,
    spread_consecutive_templates,
)

try:
    from arts_facts import generate_candidates as generate_legacy_candidates
except ImportError:
    generate_legacy_candidates = None  # type: ignore[misc, assignment]

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

ENGLISH_LEAK = re.compile(r"[a-zA-Z]{4,}")
MIXED_SCRIPT = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")
_ALLOWED_STEM_LATIN = re.compile(r"\b(GI|NGMA|UNESCO|MoMA)\b", re.I)

BASE = Path(__file__).parent
FILENAME = "arts.json"
PREFIX = "art_"
TARGET = 3102


def _has_stray_latin(text: str) -> bool:
    cleaned = _ALLOWED_STEM_LATIN.sub("", text)
    if strip_for_validation is not None:
        cleaned = strip_for_validation(cleaned)
    return bool(ENGLISH_LEAK.search(cleaned))


def is_bad_kept(question: str, options: list[str], answer: str) -> bool:
    """Drop legacy rows with English leaks, filler, or malformed stems."""
    if is_filler_question({"question": question, "options": options, "answer": answer}):
        return True
    if answer not in options:
        return True
    if not MALAYALAM.search(question):
        return True
    if _has_stray_latin(question):
        return True
    for text in [question, *options, answer]:
        if MIXED_SCRIPT.search(text):
            return True
        if _has_stray_latin(text) and MALAYALAM.search(text):
            return True
    if BANNED_OPTION_ENGLISH:
        for opt in options:
            if BANNED_OPTION_ENGLISH.search(opt):
                return True
    return False


def make_entry(num: int, q: str, opts: list[str], ans: str, diff: str) -> dict:
    shuffled = list(opts)
    random.shuffle(shuffled)
    return {
        "id": f"{PREFIX}{num:04d}",
        "question": q,
        "options": shuffled,
        "answer": ans,
        "difficulty": diff,
    }


def load_global_existing() -> set[str]:
    existing: set[str] = set()
    for path in BASE.glob("*.json"):
        if path.name == FILENAME:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, list):
            continue
        for q in data.get("questions", []):
            stem = q.get("question", "").strip()
            if stem:
                existing.add(stem)
    return existing


def collect_candidates(existing: set[str], rng: random.Random) -> list:
    wave = generate_wave20_candidates(existing, rng)
    if generate_legacy_candidates is None:
        return wave
    legacy = generate_legacy_candidates(existing, rng)
    return interleave_candidates(wave + legacy, rng)


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
            kept.append(q)
            kept_stems.add(stem)

    existing = load_global_existing() | kept_stems
    candidates = collect_candidates(existing, rng)

    combined: list[dict] = list(kept)
    for q, opts, ans, diff in candidates:
        if len(combined) >= TARGET:
            break
        if q in kept_stems or is_bad_kept(q, opts, ans):
            continue
        combined.append(make_entry(len(combined) + 1, q, opts, ans, diff))
        kept_stems.add(q)

    if len(combined) < TARGET:
        extra_existing = kept_stems | {q.get("question", "").strip() for q in combined}
        extra = collect_candidates(extra_existing, random.Random(rng.randint(0, 10**9)))
        for q, opts, ans, diff in extra:
            if len(combined) >= TARGET:
                break
            if q in kept_stems or is_bad_kept(q, opts, ans):
                continue
            combined.append(make_entry(len(combined) + 1, q, opts, ans, diff))
            kept_stems.add(q)

    combined = spread_consecutive_templates(combined, rng, max_run=2)

    final: list[dict] = []
    seen: set[str] = set()
    for q in combined:
        if len(final) >= TARGET:
            break
        stem = q.get("question", "").strip()
        if not stem or stem in seen or is_bad_kept(stem, q.get("options", []), q.get("answer", "")):
            continue
        seen.add(stem)
        entry = dict(q)
        entry["id"] = f"{PREFIX}{len(final) + 1:04d}"
        final.append(entry)

    if len(final) < TARGET:
        backfill_existing = seen | load_global_existing()
        backfill = collect_candidates(backfill_existing, random.Random(rng.randint(0, 10**9)))
        for q, opts, ans, diff in backfill:
            if len(final) >= TARGET:
                break
            if q in seen or is_bad_kept(q, opts, ans):
                continue
            seen.add(q)
            final.append(make_entry(len(final) + 1, q, opts, ans, diff))

    data["questions"] = final
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"{FILENAME}: {len(final)} questions "
        f"(kept {len(kept)}, added {max(0, len(final) - len(kept))}, target {TARGET})"
    )
    dupes = len(final) - len({q["question"] for q in final})
    print(f"duplicate stems: {dupes}")

    result = subprocess.run(
        [sys.executable, str(BASE / "validate_questions.py"), FILENAME],
        cwd=BASE,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
