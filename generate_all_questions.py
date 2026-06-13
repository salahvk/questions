#!/usr/bin/env python3
"""
Generate questions to reach 1,01,000 milestone per generation_targets.txt.

Before generating, enforces .cursor/rules/malayalam-questions.mdc:
  - No filler templates (refill_common.is_filler_text)
  - Global question-stem uniqueness
  - Verified fact modules only (never numbered fake entities)
  - Fail loudly on shortfall (reports gaps; never pads with templates)

Post-run (mandatory):
  python3 apply_malayalam_rules.py
  python3 validate_questions.py
"""

from __future__ import annotations

import importlib
import random
import subprocess
import sys
from pathlib import Path

import fill_unique
from generation_targets import parse_targets_file, summary
from refill_common import Candidate, load_global_stems, refill_file

BASE = Path(__file__).parent

# Actual ID prefixes in JSON files (must match existing banks)
PREFIXES: dict[str, str] = {
    "geography.json": "geo_",
    "indian_history.json": "ih_",
    "mathematics.json": "mat_",
    "biology.json": "bio_",
    "physics.json": "phy_",
    "world_history.json": "wh_",
    "chemistry.json": "che_",
    "economics.json": "eco_",
    "literature.json": "lit_",
    "sports.json": "sca_",
    "constitution_of_india.json": "coi_",
    "cinema.json": "cin_",
    "modern_india.json": "mi_",
    "natural_science.json": "nsc_",
    "arts.json": "art_",
    "history_of_kerala.json": "hok_",
    "awards.json": "aca_",
    "education.json": "edu_",
    "malayalam.json": "mal_",
    "english_language.json": "eng_",
    "kerala_renaissance.json": "kr_",
    "social_welfare_schemes.json": "sws_",
    "national_schemes.json": "ns_",
    "international_organizations.json": "io_",
    "indian_industries.json": "ind_",
    "information_technology.json": "it_",
    "important_institutions.json": "ii_",
    "continents_of_the_world.json": "cow_",
    "kerala_through_districts.json": "ktd_",
    "politics_of_kerala.json": "pok_",
    "philosophy.json": "phi_",
    "communication_journalism.json": "cj_",
    "basic_general_knowledge.json": "bgk_",
    "astronomy.json": "ast_",
    "historical_monuments_of_kerala.json": "hmk_",
}

# Fact-module driven categories
FACT_MODULES: dict[str, str] = {
    "geography.json": "geography_facts",
    "indian_history.json": "indian_history_facts",
    "mathematics.json": "mathematics_facts",
    "chemistry.json": "chemistry_facts",
    "biology.json": "biology_facts",
    "physics.json": "physics_facts",
    "world_history.json": "world_history_facts",
    "economics.json": "economics_facts",
    "malayalam.json": "malayalam_facts",
    "literature.json": "literature_facts",
    "sports.json": "sports_facts",
    "information_technology.json": "information_technology_facts",
    "historical_monuments_of_kerala.json": "historical_monuments_of_kerala_facts",
    "continents_of_the_world.json": "continents_of_the_world_facts",
    "important_institutions.json": "important_institutions_facts",
    "communication_journalism.json": "communication_journalism_facts",
    "kerala_renaissance.json": "kerala_renaissance_facts",
    "english_language.json": "english_language_facts",
    "education.json": "education_facts",
    "history_of_kerala.json": "history_of_kerala_facts",
    "arts.json": "arts_facts",
    "natural_science.json": "natural_science_facts",
    "cinema.json": "cinema_facts",
    "constitution_of_india.json": "constitution_of_india_facts",
}

# fill_unique builders for smaller banks
FILL_UNIQUE_MAP: dict[str, tuple[str, object]] = {
    "modern_india.json": ("mi_", fill_unique.build_modern_india),
    "national_schemes.json": ("ns_", fill_unique.build_national_schemes),
    "social_welfare_schemes.json": ("sws_", fill_unique.build_social_welfare),
    "indian_industries.json": ("ind_", fill_unique.build_indian_industries),
    "international_organizations.json": ("io_", fill_unique.build_international_orgs),
    "philosophy.json": ("phi_", fill_unique.build_philosophy),
    "basic_general_knowledge.json": ("bgk_", fill_unique.build_basic_gk),
    "politics_of_kerala.json": ("pok_", fill_unique.build_politics_kerala),
    "kerala_through_districts.json": ("ktd_", fill_unique.build_kerala_districts),
}

SPECIAL_SCRIPTS = {
    "astronomy.json": "refill_astronomy_unique.py",
    "awards.json": "refill_awards_unique.py",
}


def candidates_from_module(module_name: str, existing: set[str], rng: random.Random) -> list[Candidate]:
    mod = importlib.import_module(module_name)
    return mod.generate_candidates(existing, rng)


def run_special_scripts() -> None:
    for script in SPECIAL_SCRIPTS.values():
        path = BASE / script
        if path.exists():
            print(f"\n--- Running {script} ---")
            subprocess.run([sys.executable, str(path)], cwd=BASE, check=False)


def generate_all(*, skip_validation: bool = False) -> int:
    rng = random.Random(42)
    targets = parse_targets_file()

    print("=" * 60)
    print("QUESTION GENERATION — milestone 1,01,000")
    print("Rules: .cursor/rules/malayalam-questions.mdc")
    print("=" * 60)
    before = summary()
    print(f"Before: {before['current']:,} / {before['milestone_total']:,}\n")

    shortfalls: list[str] = []

    # 1. Fact-module categories (MEGA sciences + geography)
    for filename, module in FACT_MODULES.items():
        target = targets.get(filename, 0)
        prefix = PREFIXES[filename]
        existing = load_global_stems(exclude_file=filename)
        candidates = candidates_from_module(module, existing, rng)
        print(f"{filename}: {len(candidates)} candidates available, target {target}")
        rep = refill_file(filename, prefix, target, candidates, rng)
        print(f"  → {rep['final']} questions (+{rep['added']}, shortfall {rep['shortfall']})")
        if rep["shortfall"]:
            shortfalls.append(f"{filename}: need {rep['shortfall']} more verified facts")

    # 2. fill_unique categories
    for filename, (prefix, builder) in FILL_UNIQUE_MAP.items():
        target = targets.get(filename, 0)
        existing = load_global_stems(exclude_file=filename)
        candidates: list[Candidate] = builder()
        rep = refill_file(filename, prefix, target, candidates, rng)
        print(f"{filename}: +{rep['added']} → {rep['final']}/{target} (shortfall {rep['shortfall']})")
        if rep["shortfall"]:
            shortfalls.append(f"{filename}: need {rep['shortfall']} more curated facts")

    # 3. Special refill scripts (astronomy, awards)
    run_special_scripts()

    after = summary()
    print("\n" + "=" * 60)
    print(f"After:  {after['current']:,} / {after['milestone_total']:,}")
    print(f"Added:  {after['current'] - before['current']:,}")
    print(f"Still:  {after['still_add']:,} to milestone")
    print("=" * 60)

    if shortfalls:
        print("\nSHORTFALLS (add more verified facts — never template-pad):")
        for s in shortfalls:
            print(f"  • {s}")

    if not skip_validation:
        print("\n--- apply_malayalam_rules.py ---")
        subprocess.run([sys.executable, str(BASE / "apply_malayalam_rules.py")], cwd=BASE)
        print("\n--- validate_questions.py ---")
        result = subprocess.run([sys.executable, str(BASE / "validate_questions.py")], cwd=BASE)
        return result.returncode

    return 1 if after["still_add"] else 0


def main() -> int:
    skip = "--skip-validation" in sys.argv
    return generate_all(skip_validation=skip)


if __name__ == "__main__":
    raise SystemExit(main())
