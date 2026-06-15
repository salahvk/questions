#!/usr/bin/env python3
"""Parse generation_targets.txt into per-file milestone targets."""

from __future__ import annotations

import re
from pathlib import Path

BASE = Path(__file__).parent
TARGETS_FILE = BASE / "generation_targets.txt"
MILESTONE_TOTAL = 101_000
EXCLUDED = {"current_affairs_manifest.json"}

# filename -> (id_prefix, target_count)
CATEGORY_REGISTRY: dict[str, tuple[str, int]] = {
    "geography.json": ("geo_", 8441),
    "indian_history.json": ("ih_", 6752),
    "mathematics.json": ("mat_", 6752),
    "biology.json": ("bio_", 5627),
    "physics.json": ("phy_", 5627),
    "world_history.json": ("wh_", 5627),
    "chemistry.json": ("che_", 5627),
    "economics.json": ("eco_", 4501),
    "literature.json": ("lit_", 2813),
    "sports.json": ("sca_", 2813),
    "constitution_of_india.json": ("coi_", 2813),
    "cinema.json": ("cin_", 2813),
    "modern_india.json": ("mi_", 2251),
    "natural_science.json": ("nsc_", 2251),
    "arts.json": ("art_", 2813),
    "history_of_kerala.json": ("hok_", 2251),
    "awards.json": ("awd_", 2813),
    "education.json": ("edu_", 2251),
    "malayalam.json": ("mal_", 1688),
    "english_language.json": ("eng_", 1688),
    "kerala_renaissance.json": ("kr_", 1688),
    "social_welfare_schemes.json": ("sws_", 1407),
    "national_schemes.json": ("ns_", 1407),
    "international_organizations.json": ("io_", 1407),
    "indian_industries.json": ("ii_", 1407),
    "information_technology.json": ("it_", 1407),
    "important_institutions.json": ("ii2_", 1407),
    "continents_of_the_world.json": ("cotw_", 1407),
    "kerala_through_districts.json": ("ktd_", 1125),
    "politics_of_kerala.json": ("pok_", 1125),
    "philosophy.json": ("phi_", 1125),
    "communication_journalism.json": ("cj_", 1125),
    "basic_general_knowledge.json": ("bgk_", 1125),
    "astronomy.json": ("ast_", 4501),
    "historical_monuments_of_kerala.json": ("hmk_", 1125),
}


def parse_targets_file() -> dict[str, int]:
    """Read generation_targets.txt table; fall back to CATEGORY_REGISTRY."""
    if not TARGETS_FILE.exists():
        return {k: v[1] for k, v in CATEGORY_REGISTRY.items()}

    targets: dict[str, int] = {}
    row = re.compile(r"^(\S+\.json)\s+[\d,]+\s+([\d,]+)\s+[\d,]+")
    for line in TARGETS_FILE.read_text(encoding="utf-8").splitlines():
        m = row.match(line.strip())
        if m:
            targets[m.group(1)] = int(m.group(2).replace(",", ""))
    return targets or {k: v[1] for k, v in CATEGORY_REGISTRY.items()}


def get_prefix(filename: str) -> str:
    if filename in CATEGORY_REGISTRY:
        return CATEGORY_REGISTRY[filename][0]
    # infer from existing JSON ids
    return ""


def milestone_files() -> list[str]:
    """All JSON banks counted toward 1,01,000 (excludes current affairs)."""
    targets = parse_targets_file()
    return sorted(targets.keys())


def summary() -> dict[str, object]:
    import json

    targets = parse_targets_file()
    total_have = 0
    per_file: dict[str, dict[str, int]] = {}
    for fn, target in targets.items():
        path = BASE / fn
        if not path.exists():
            have = 0
        else:
            data = json.loads(path.read_text(encoding="utf-8"))
            have = len(data.get("questions", []))
        per_file[fn] = {"have": have, "target": target, "add": max(0, target - have)}
        total_have += have
    return {
        "milestone_total": MILESTONE_TOTAL,
        "current": total_have,
        "still_add": max(0, MILESTONE_TOTAL - total_have),
        "files": per_file,
    }


if __name__ == "__main__":
    s = summary()
    print(f"Milestone: {s['current']:,} / {s['milestone_total']:,}  (add {s['still_add']:,})")
