#!/usr/bin/env python3
"""Keep valid education.json questions and refill with wave20 + legacy unique facts."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from education_facts import generate_candidates as generate_legacy_candidates
from education_wave20_facts import generate_wave20_candidates
from refill_common import (
    SKIP_GLOBAL,
    id_width,
    interleave_candidates,
    is_filler_question,
    is_filler_text,
    make_entry,
    spread_consecutive_templates,
    stem_template,
)

BASE = Path(__file__).parent
FILENAME = "education.json"
PREFIX = "edu_"
ADD_TARGET = 1700

DEFINITION_WRAPPER = re.compile(r"^വിദ്യാഭ്യാസത്തിൽ\s*'.*'\s*എന്തിന")
MALAYALAM = re.compile(r"[\u0D00-\u0D7F]")
_ALLOWED_STEM_LATIN = re.compile(
    r"\b(RTE|NEP|UNESCO|SDG|IIT|IISc|TIFR|IIST|NCERT|UGC|AICTE|NCTE|"
    r"BCI|NMC|PCI|CABE|DIET|NUEPA|SCERT|DPEP|RUSA|NIPUN|NSQF|NTSE|NMMS|"
    r"ASER|UDISE|NIRF|NAAC|SQAAF|PARAKH|APAAR|CTET|IGNOU|JNV|KV|PMKVY|"
    r"SWAYAM|DIKSHA|NISHTHA|PM|SHRI|JRF|NET|SET|KVPY|INSPIRE|NEET|JEE|"
    r"GATE|CAT|MBA|CBSE|ICSE|NIOS|SSA|RMSA|HECI|PM|POSHAN|ICAR|IIM|NIT|"
    r"IIIT|BHU|TISS|AMU|JNU|AIIMS|MBBS|BDS|PhD|M\.Ed|B\.Ed)\b",
    re.I,
)
_LATIN4 = re.compile(r"[a-zA-Z]{4,}")
_MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def _has_stray_latin(text: str) -> bool:
    return bool(_LATIN4.search(_ALLOWED_STEM_LATIN.sub("", text)))


SKIP_LEGACY_TEMPLATES = {
    "univ_city",
    "iit_city",
    "state_school_board",
    "exam_purpose",
    "scheme_purpose",
    "scheme_sector",
    "ncert_fake",
}


def is_bad_candidate(question: str, options: list[str], answer: str) -> bool:
    if is_filler_text(question) or DEFINITION_WRAPPER.search(question):
        return True
    if not MALAYALAM.search(question):
        return True
    parts = [question, answer, *options]
    if any(_MIXED.search(p) for p in parts):
        return True
    if any(_has_stray_latin(p) for p in parts):
        return True
    if "വിഷയം-" in answer:
        return True
    if stem_template(question) in SKIP_LEGACY_TEMPLATES:
        return True
    return False


def is_bad_kept(q: dict) -> bool:
    """Drop filler, NCERT fake rows, definition-wrapper stems, and template clusters."""
    if is_filler_question(q):
        return True
    stem = q.get("question", "").strip()
    if not stem:
        return True
    if DEFINITION_WRAPPER.search(stem):
        return True
    if is_filler_text(stem):
        return True
    if stem_template(stem) in SKIP_LEGACY_TEMPLATES:
        return True
    ans = str(q.get("answer", ""))
    if "വിഷയം-" in ans or ans.startswith("വിഷയം"):
        return True
    if is_bad_candidate(stem, q.get("options", []), ans):
        return True
    return False


def load_global_stems(exclude_file: str | None = None) -> set[str]:
    existing: set[str] = set()
    for path in BASE.glob("*.json"):
        if path.name in SKIP_GLOBAL or path.name == exclude_file:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        questions = data if isinstance(data, list) else data.get("questions", [])
        if not isinstance(questions, list):
            continue
        for q in questions:
            if not isinstance(q, dict):
                continue
            stem = q.get("question", "").strip()
            if stem:
                existing.add(stem)
    return existing


def main() -> int:
    rng = random.Random(42)
    path = BASE / FILENAME
    data = json.loads(path.read_text(encoding="utf-8"))

    kept = [q for q in data.get("questions", []) if not is_bad_kept(q)]
    kept_stems: set[str] = {
        q.get("question", "").strip() for q in kept if q.get("question")
    }

    existing = load_global_stems(exclude_file=FILENAME) | kept_stems
    target = len(kept) + ADD_TARGET

    legacy = [
        c for c in generate_legacy_candidates(set(existing), rng)
        if stem_template(c[0]) not in SKIP_LEGACY_TEMPLATES
    ]
    wave = generate_wave20_candidates(set(existing) | {s for s, *_ in legacy}, rng)
    candidates = interleave_candidates(wave + legacy, rng)

    combined: list[dict] = list(kept)
    width = id_width(target)

    for q, opts, ans, diff in candidates:
        if len(combined) >= target:
            break
        if q in kept_stems or is_bad_candidate(q, opts, ans):
            continue
        combined.append(make_entry(PREFIX, len(combined) + 1, q, opts, ans, diff, width))
        kept_stems.add(q)

    if len(combined) < target:
        for seed in range(5):
            extra_existing = kept_stems | load_global_stems(exclude_file=FILENAME)
            extra = interleave_candidates(
                generate_wave20_candidates(extra_existing, random.Random(rng.randint(0, 10**9))),
                random.Random(seed),
            )
            for q, opts, ans, diff in extra:
                if len(combined) >= target:
                    break
                if q in kept_stems or is_bad_candidate(q, opts, ans):
                    continue
                combined.append(make_entry(PREFIX, len(combined) + 1, q, opts, ans, diff, width))
                kept_stems.add(q)
            if len(combined) >= target:
                break

    combined = spread_consecutive_templates(combined, rng, max_run=2)

    final: list[dict] = []
    seen: set[str] = set()
    for q in combined:
        stem = q.get("question", "").strip()
        if not stem or stem in seen or is_bad_kept(q) or is_bad_candidate(stem, q.get("options", []), q.get("answer", "")):
            continue
        seen.add(stem)
        entry = dict(q)
        entry["id"] = f"{PREFIX}{len(final) + 1:0{width}d}"
        final.append(entry)

    data["questions"] = final
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    added = max(0, len(final) - len(kept))
    shortfall = max(0, target - len(final))
    print(
        f"{FILENAME}: {len(final)} questions "
        f"(kept {len(kept)}, added {added}, target {target}, shortfall {shortfall})"
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
