#!/usr/bin/env python3
"""Refill natural_science.json with wave20 unique environmental facts."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from generation_targets import CATEGORY_REGISTRY
from natural_science_wave20_facts import generate_wave20_candidates
from refill_common import interleave_candidates, is_filler_question, spread_consecutive_templates

BASE = Path(__file__).parent
FILENAME = "natural_science.json"
PREFIX = CATEGORY_REGISTRY[FILENAME][0]
TARGET = CATEGORY_REGISTRY[FILENAME][1]

BAD_DISTRACTOR_POOL = frozenset({
    "പച്ചസസ്യങ്ങൾ", "ഉഷ്ണമേഖലാ മഴക്കാടുകൾ", "സ്ട്രാറ്റോസ്ഫിയർ", "കാർബൺ ഡൈഓക്സൈഡ്",
    "അനിമോമീറ്റർ", "ഹൈഗ്രോമീറ്റർ", "ബാരോമീറ്റർ", "റെയിൻ ഗേജ്",
    "എപ്പിസെന്റർ", "റിക്ടർ സ്കെയിൽ", "ലാവ", "സമുദ്രഭൂകമ്പം",
})

MIXED_SCRIPT = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")
MALAYALAM = re.compile(r"[\u0D00-\u0D7F]")


def is_bad_kept(question: str, options: list[str], answer: str) -> bool:
    if is_filler_question({"question": question, "options": options, "answer": answer}):
        return True
    if not MALAYALAM.search(question):
        return True
    for text in [question, *options, answer]:
        if MIXED_SCRIPT.search(text):
            return True
        if re.search(r"\benacted\b|\byear\b", text, re.I):
            return True
    # legacy bulk filler: unrelated climate terms as distractors
    wrong = [o for o in options if o != answer]
    if sum(1 for o in wrong if o in BAD_DISTRACTOR_POOL) >= 2:
        return True
    if len(set(options)) != 4:
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
    candidates = interleave_candidates(generate_wave20_candidates(existing, rng), rng)

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
        extra = interleave_candidates(
            generate_wave20_candidates(extra_existing, random.Random(rng.randint(0, 10**9))),
            rng,
        )
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
        for seed in range(10):
            backfill_existing = seen | load_global_existing()
            backfill = interleave_candidates(
                generate_wave20_candidates(backfill_existing, random.Random(1000 + seed)),
                rng,
            )
            for q, opts, ans, diff in backfill:
                if len(final) >= TARGET:
                    break
                if q in seen or is_bad_kept(q, opts, ans):
                    continue
                seen.add(q)
                final.append(make_entry(len(final) + 1, q, opts, ans, diff))
            if len(final) >= TARGET:
                break

    data["questions"] = final
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"{FILENAME}: {len(final)} questions "
        f"(kept {len(kept)}, added {max(0, len(final) - len(kept))}, target {TARGET})"
    )
    dupes = len(final) - len({q["question"] for q in final})
    print(f"duplicate stems: {dupes}")

    subprocess.run([sys.executable, str(BASE / "apply_malayalam_rules.py"), FILENAME], cwd=BASE)
    result = subprocess.run(
        [sys.executable, str(BASE / "validate_questions.py"), FILENAME],
        cwd=BASE,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
