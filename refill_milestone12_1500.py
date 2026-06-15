#!/usr/bin/env python3
"""Refill 12 milestone banks to 1,500 unique questions each using wave30 fact modules."""

from __future__ import annotations

import importlib
import random
import subprocess
import sys
from pathlib import Path

from refill_common import interleave_candidates, load_global_stems, refill_file

BASE = Path(__file__).parent
TARGET = 1500

WAVE30_MODULES: dict[str, tuple[str, str]] = {
    "english_language.json": ("eng_", "english_wave30_facts"),
    "national_schemes.json": ("ns_", "national_schemes_wave30_facts"),
    "international_organizations.json": ("io_", "international_organizations_wave30_facts"),
    "information_technology.json": ("it_", "information_technology_wave30_facts"),
    "social_welfare_schemes.json": ("sws_", "social_welfare_schemes_wave30_facts"),
    "indian_industries.json": ("ind_", "indian_industries_wave30_facts"),
    "important_institutions.json": ("ii_", "important_institutions_wave30_facts"),
    "continents_of_the_world.json": ("cow_", "continents_wave30_facts"),
    "kerala_through_districts.json": ("ktd_", "kerala_through_districts_wave30_facts"),
    "politics_of_kerala.json": ("pok_", "politics_of_kerala_wave30_facts"),
    "philosophy.json": ("phi_", "philosophy_wave30_facts"),
    "communication_journalism.json": ("cj_", "communication_journalism_wave30_facts"),
}


def candidates_for(module_name: str, existing: set[str], rng: random.Random):
    mod = importlib.import_module(module_name)
    raw = mod.generate_wave30_candidates(set(existing), rng)
    return interleave_candidates(raw, rng)


def main() -> int:
    rng = random.Random(42)
    shortfalls: list[str] = []

    print("=" * 60)
    print(f"WAVE30 REFILL — target {TARGET} per file (12 banks)")
    print("=" * 60)

    for filename, (prefix, module) in WAVE30_MODULES.items():
        existing = load_global_stems(exclude_file=filename)
        candidates = candidates_for(module, existing, rng)
        print(f"{filename}: {len(candidates)} candidates")
        rep = refill_file(filename, prefix, TARGET, candidates, rng)
        print(
            f"  → {rep['final']}/{TARGET} "
            f"(kept {rep['kept']}, +{rep['added']}, shortfall {rep['shortfall']})"
        )
        if rep["shortfall"]:
            shortfalls.append(f"{filename}: need {rep['shortfall']} more verified facts")

    print("\n" + "=" * 60)
    if shortfalls:
        print("SHORTFALLS:")
        for s in shortfalls:
            print(f"  • {s}")
        print("=" * 60)
        return 1

    print("All 12 banks reached target.")
    print("=" * 60)

    print("\n--- apply_malayalam_rules.py ---")
    subprocess.run([sys.executable, str(BASE / "apply_malayalam_rules.py")], cwd=BASE, check=True)
    print("\n--- validate_questions.py ---")
    result = subprocess.run([sys.executable, str(BASE / "validate_questions.py")], cwd=BASE)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
