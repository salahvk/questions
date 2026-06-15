#!/usr/bin/env python3
"""Remove formula-filler biology questions and refill with unique factual items."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from biology_facts import generate_candidates
from refill_common import interleave_candidates, spread_consecutive_templates

BASE = Path(__file__).parent
PREFIX = "bio_"

# Random-parameter calculation spam — not PSC-style unique facts
FILLER_PATTERNS = [
    re.compile(r"^diploid: n=\d+, m=\d+ — ആകെ ക്രോമോസോം എണ്ണം\?$"),
    re.compile(r"^DNA \d+ bp, GC \d+% — GC bp എണ്ണം\?$"),
]

ENGLISH_STEM = re.compile(
    r"^[A-Za-z0-9 ,.'?()-]+$|"
    r"\b(function|production|storage|synthesis|lifespan|donor|recipient|temp|chambers)\?|"
    r"funcion|funkcion|microorganism|universal donor|organ system|plant cell wall|Koch postulates|"
    r"അർtery|അർtery|chromosome\?|"
    r"ക്രോമosome|അയodine|കാൽcium|"
    r"ഏറ്റവും (വലിയ|ചെറിയ) (organ|cell|protein|molecule|atom|element|tissue|gland|artery|vein|nerve|joint|cavity)"
)


def has_english_leak_options(options: list[str], answer: str) -> bool:
    text = " ".join(options) + " " + answer
    if re.search(r"\b(skin|liver|lung|heart|femur|stapes|aorta|capillary|circulatory|digestive|"
                 r"nervous|respiratory|endocrine|abdominal|thoracic|cranial|pelvic|middle ear|"
                 r"egg cell|sperm|neuron|muscle|hemoglobin|collagen|insulin|titin|glucose|"
                 r"oxygen transport|ATP production|photosynthesis|DNA storage|protein synthesis|"
                 r"scurvy|rickets|beriberi|anemia|osteoporosis|goiter)\b", text, re.I):
        return True
    if re.search(r"\b(survey|beriberi)\b", text, re.I):
        return True
    return False


def is_formula_filler(question: str) -> bool:
    return any(p.search(question.strip()) for p in FILLER_PATTERNS)


def is_bad_kept(question: str, options: list[str], answer: str) -> bool:
    if is_formula_filler(question):
        return True
    if ENGLISH_STEM.search(question.strip()):
        return True
    if "funkcion" in question or "funcion" in question:
        return True
    if " അ gland?" in question:
        return True
    if re.search(r"Watson-Crick\?$|RBC lifespan", question):
        return True
    if any("mRNA " in o for o in options):
        return True
    if any(re.search(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]", o) for o in options + [answer]):
        return True
    if "ക人工" in question:
        return True
    if has_english_leak_options(options, answer):
        return True
    return False


def load_global_existing() -> set[str]:
    existing: set[str] = set()
    for path in BASE.glob("*.json"):
        if path.name == "biology.json":
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
    return {"id": f"{PREFIX}{num:04d}", "question": q, "options": shuffled, "answer": ans, "difficulty": diff}


def main() -> int:
    rng = random.Random(42)
    path = BASE / "biology.json"
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
    candidates = interleave_candidates(generate_candidates(existing, rng), rng)

    combined: list[dict] = list(kept)
    for q, opts, ans, diff in candidates:
        if q in kept_stems:
            continue
        combined.append(make_entry(len(combined) + 1, q, opts, ans, diff))
        kept_stems.add(q)

    combined = spread_consecutive_templates(combined, rng, max_run=2)

    final: list[dict] = []
    seen: set[str] = set()
    for i, q in enumerate(combined, start=1):
        stem = q.get("question", "").strip()
        if stem in seen or is_bad_kept(stem, q.get("options", []), q.get("answer", "")):
            continue
        seen.add(stem)
        entry = dict(q)
        entry["id"] = f"{PREFIX}{i:04d}"
        final.append(entry)

    data["questions"] = final
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    formula_left = sum(1 for q in final if is_formula_filler(q["question"]))
    print(f"biology.json: {len(final)} questions (kept {len(kept)}, removed formula filler)")
    print(f"formula patterns remaining: {formula_left}")
    dupes = len(final) - len({q["question"] for q in final})
    print(f"duplicate stems: {dupes}")

    result = subprocess.run(
        [sys.executable, str(BASE / "validate_questions.py"), "biology.json"],
        cwd=BASE,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
