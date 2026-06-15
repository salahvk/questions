#!/usr/bin/env python3
"""Fix INVENTION_COUNTRY template corruption in basic_general_knowledge.json."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from basic_gk_wave30_facts import COUNTRY_CAPITAL, FOOD_CROP_ORIGIN, INVENTIONS as INVENTION_ROWS
from giveaway_utils import is_answer_in_stem_giveaway
from refill_common import pick3

BASE = Path(__file__).parent
FILE = "basic_general_knowledge.json"

FOOD = {a: b for a, b in FOOD_CROP_ORIGIN}
INVENTIONS = {a: b for a, b in INVENTION_ROWS}
CAPITALS = {a: b for a, b in COUNTRY_CAPITAL}
CAPITAL_BY_CITY = {v: k for k, v in CAPITALS.items()}

COUNTRY_POOL = sorted(set(INVENTIONS.values()))
CAPITAL_POOL = sorted(set(CAPITALS.values()))
INVENTION_POOL = sorted(INVENTIONS.keys())
COUNTRY_NAME_POOL = sorted(CAPITALS.keys())
CITY_STATES = sorted([country for country, capital in CAPITALS.items() if country == capital])
CITY_STATE_STEMS: dict[str, str] = {
    "മോണാക്കോ": "യൂറോപ്യൻ മൈക്രോസ്റ്റേറ്റ്; തലസ്ഥാനവും രാജ്യപ്പേരും ഒന്നുതന്നെ — ഏത് രാജ്യം?",
    "ലക്സംബർഗ്": "പശ്ചിമ യൂറോപ്യൻ ലാൻഡ്ലോക്ക് മൈക്രോസ്റ്റേറ്റ്; തലസ്ഥാനവും രാജ്യപ്പേരും ഒന്നുതന്നെ — ഏത് രാജ്യം?",
    "ജിബൂട്ടി": "ആഫ്രിക്കൻ ഹോൺ ഓഫ് ആഫ്രിക്കയിലെ രാജ്യം; തലസ്ഥാനവും രാജ്യപ്പേരും ഒന്നുതന്നെ — ഏത്?",
    "സിംഗപ്പൂർ": "ദക്ഷിണപൂർവേഷ്യൻ ദ്വീപുരാജ്യം; തലസ്ഥാനവും രാജ്യപ്പേരും ഒന്നുതന്നെ — ഏത്?",
}

CAP_FWD_STEMS = [
    "'{country}' രാജ്യത്തിന്റെ തലസ്ഥാനം ഏത്?",
    "'{country}'-ന്റെ തലസ്ഥാന നഗരം ഏത്?",
    "'{country}'-ന്റെ തലസ്ഥാനം ഏത്?",
]
CAP_REV_STEMS = [
    "'{city}' ഏത് രാജ്യത്തിന്റെ തലസ്ഥാനം?",
    "തലസ്ഥാനം '{city}' ആയ രാജ്യം ഏത്?",
]
INV_FWD_STEMS = [
    "'{item}'-ന്റെ ഉത്ഭവദേശം ഏത്?",
    "'{item}' ഏത് രാജ്യത്തിൽ നിന്നാണ് ഉത്ഭവിച്ചത്?",
]
INV_REV_STEMS = [
    "'{country}' ഏത് കണ്ടുപിടിത്തത്തിന്റെ ഉത്ഭവദേശം?",
    "'{country}'-ൽ നിന്ന് ഉത്ഭവിച്ച കണ്ടുപിടിത്തം ഏത്?",
]


def _inventions_for_country(country: str) -> list[str]:
    return [item for item, origin in INVENTIONS.items() if origin == country]


def _plan_fix(stem: str, answer: str) -> tuple[str, str, str, list[str]] | None:
    """Return (kind, new_stem_template_key, answer, option_pool) or None."""

    m = re.match(r"'([^']+)'-ന്റെ ഉത്ഭവദേശം\?$", stem)
    if m and m.group(1) in FOOD:
        return None

    label: str | None = None

    m = re.match(r"'([^']+)' എവിടെ നിന്നാണ് കണ്ടെത്തിയത്\?$", stem)
    if m:
        label = m.group(1)

    if not label:
        m = re.match(r"'([^']+)'-ന്റെ കണ്ടെത്തിയ രാജ്യം\?$", stem)
        if m:
            label = m.group(1)

    if not label:
        m = re.match(r"'([^']+)'-ന്റെ ഉത്ഭവദേശം\?$", stem)
        if m:
            label = m.group(1)

    if label:
        if label.endswith("തലസ്ഥാനം"):
            country = label.replace(" തലസ്ഥാനം", "")
            if country not in CAPITALS:
                return None
            return ("cap_fwd", country, CAPITALS[country], CAPITAL_POOL)
        if label in INVENTIONS:
            return ("inv_fwd", label, INVENTIONS[label], COUNTRY_POOL)
        if label in CAPITALS:
            return ("cap_fwd", label, CAPITALS[label], CAPITAL_POOL)

    m = re.match(r"'([^']+)'-ൽ നിന്ന് ഉത്ഭവിച്ച കണ്ടുപിടിത്തം\?$", stem)
    if m:
        label = m.group(1)
        if answer.endswith("തലസ്ഥാനം") and label in CAPITAL_BY_CITY:
            country = answer.replace(" തലസ്ഥാനം", "")
            return ("cap_rev", label, country, COUNTRY_NAME_POOL)
        if answer in INVENTIONS:
            return ("inv_rev", label, answer, INVENTION_POOL)

    m = re.match(r"'([^']+)' ഏത് കണ്ടുപിടിത്തത്തിന്റെ ഉത്ഭവദേശം\?$", stem)
    if m:
        label = m.group(1)
        if answer.endswith("തലസ്ഥാനം") and label in CAPITAL_BY_CITY:
            country = answer.replace(" തലസ്ഥാനം", "")
            return ("cap_rev", label, country, COUNTRY_NAME_POOL)
        if answer in INVENTIONS:
            return ("inv_rev", label, answer, INVENTION_POOL)

    m = re.match(r"'([^']+)'-ന് ഏത് കണ്ടുപിടിത്തം\?$", stem)
    if m:
        label = m.group(1)
        if answer.endswith("തലസ്ഥാനം") and label in CAPITAL_BY_CITY:
            country = answer.replace(" തലസ്ഥാനം", "")
            return ("cap_rev", label, country, COUNTRY_NAME_POOL)
        if answer in INVENTIONS:
            return ("inv_rev", label, answer, INVENTION_POOL)

    return None


def _stem_for(kind: str, key: str, alt: int) -> str:
    if kind == "cap_fwd":
        templates = CAP_FWD_STEMS
        return templates[alt % len(templates)].format(country=key)
    if kind == "cap_rev":
        templates = CAP_REV_STEMS
        return templates[alt % len(templates)].format(city=key)
    if kind == "inv_fwd":
        templates = INV_FWD_STEMS
        return templates[alt % len(templates)].format(item=key)
    templates = INV_REV_STEMS
    return templates[alt % len(templates)].format(country=key)


def _fix_city_state_giveaways(questions: list[dict], rng: random.Random) -> tuple[int, int]:
    fixed = 0
    removed = 0
    seen_stems: set[str] = {q.get("question", "").strip() for q in questions}
    kept: list[dict] = []
    for q in questions:
        answer = q.get("answer", "").strip()
        stem = q.get("question", "").strip()
        if answer not in CITY_STATES or not is_answer_in_stem_giveaway(stem, answer):
            kept.append(q)
            continue
        new_stem = CITY_STATE_STEMS.get(answer)
        if not new_stem or new_stem in seen_stems:
            removed += 1
            continue
        q = dict(q)
        q["question"] = new_stem
        q["options"] = pick3(CITY_STATES, answer, rng)
        rng.shuffle(q["options"])
        q["answer"] = answer
        seen_stems.add(new_stem)
        kept.append(q)
        fixed += 1
    questions[:] = kept
    return fixed, removed


def _dedupe_stems(questions: list[dict]) -> int:
    seen: set[str] = set()
    kept: list[dict] = []
    removed = 0
    for q in questions:
        stem = q.get("question", "").strip()
        if not stem or stem in seen:
            removed += 1
            continue
        seen.add(stem)
        kept.append(q)
    questions[:] = kept
    return removed


def main() -> int:
    rng = random.Random(42)
    path = BASE / FILE
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.get("questions", [])

    seen_stems: set[str] = set()
    used_pairs: dict[tuple[str, str], int] = {}
    fixed = 0
    removed = 0
    kept: list[dict] = []

    for q in questions:
        stem = q.get("question", "").strip()
        answer = q.get("answer", "").strip()
        plan = _plan_fix(stem, answer)
        if not plan:
            kept.append(q)
            if stem:
                seen_stems.add(stem)
            continue

        kind, key, new_answer, pool = plan
        pair = (kind, key, new_answer)
        alt = used_pairs.get(pair, 0)
        templates_count = {
            "cap_fwd": len(CAP_FWD_STEMS),
            "cap_rev": len(CAP_REV_STEMS),
            "inv_fwd": len(INV_FWD_STEMS),
            "inv_rev": len(INV_REV_STEMS),
        }[kind]

        new_stem = None
        for attempt in range(templates_count):
            candidate = _stem_for(kind, key, alt + attempt)
            if candidate not in seen_stems:
                new_stem = candidate
                alt += attempt
                break

        if not new_stem:
            removed += 1
            continue

        used_pairs[pair] = alt + 1
        seen_stems.add(new_stem)
        opts = pick3(pool, new_answer, rng)
        rng.shuffle(opts)
        entry = dict(q)
        entry["question"] = new_stem
        entry["options"] = opts
        entry["answer"] = new_answer
        kept.append(entry)
        fixed += 1

    data["questions"] = kept
    city_fixed, city_removed = _fix_city_state_giveaways(kept, rng)
    removed += city_removed
    deduped = _dedupe_stems(kept)
    removed += deduped
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"{FILE}: fixed {fixed}, removed {removed} duplicate rows, "
        f"city-state giveaways {city_fixed}, deduped {deduped}, total {len(kept)}"
    )
    result = subprocess.run(
        [sys.executable, str(BASE / "validate_questions.py"), FILE],
        cwd=BASE,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
