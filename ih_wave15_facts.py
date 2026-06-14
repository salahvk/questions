#!/usr/bin/env python3
"""Wave 15 Indian history facts — 15 PSC topic types."""

from __future__ import annotations

import random
import re

from refill_common import Candidate, add_candidate

MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def _pool(items: list[str], correct: str) -> list[str]:
    return [x for x in items if x != correct]


def _add(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    q: str,
    ans: str,
    wrong: list[str],
    diff: str = "medium",
    pool: list[str] | None = None,
) -> None:
    if MIXED.search(q + ans + "".join(wrong)):
        return
    add_candidate(out, existing, rng, q, ans, wrong, diff, pool)


def _pairs(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    rows: list[tuple[str, str]],
    templates: list[str],
    pool_b: list[str],
    diff: str = "medium",
) -> None:
    for a, b in rows:
        for tmpl in templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b), b, _pool(pool_b, b)[:3], diff, pool_b)


def _pairs_rev(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    rows: list[tuple[str, str]],
    templates: list[str],
    pool_a: list[str],
    diff: str = "medium",
) -> None:
    for a, b in rows:
        for tmpl in templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b), a, _pool(pool_a, a)[:3], diff, pool_a)


def _triples(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    rows: list[tuple[str, str, str]],
    ab_templates: list[str],
    ac_templates: list[str],
    bc_templates: list[str],
    pool_b: list[str],
    pool_c: list[str],
    pool_a: list[str],
    diff: str = "medium",
) -> None:
    for a, b, c in rows:
        for tmpl in ab_templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b, c=c), b, _pool(pool_b, b)[:3], diff, pool_b)
        for tmpl in ac_templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b, c=c), c, _pool(pool_c, c)[:3], diff, pool_c)
        for tmpl in bc_templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b, c=c), a, _pool(pool_a, a)[:3], diff, pool_a)


def _quads(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    rows: list[tuple[str, str, str, str]],
    year_templates: list[str],
    region_templates: list[str],
    leader_templates: list[str],
    name_templates: list[str],
    years: list[str],
    regions: list[str],
    leaders: list[str],
    names: list[str],
    diff: str = "medium",
) -> None:
    for name, year, region, leader in rows:
        for tmpl in year_templates:
            _add(out, existing, rng, tmpl.format(n=name, y=year, r=region, l=leader), year, _pool(years, year)[:3], diff, years)
        for tmpl in region_templates:
            _add(out, existing, rng, tmpl.format(n=name, y=year, r=region, l=leader), region, _pool(regions, region)[:3], diff, regions)
        for tmpl in leader_templates:
            _add(out, existing, rng, tmpl.format(n=name, y=year, r=region, l=leader), leader, _pool(leaders, leader)[:3], diff, leaders)
        for tmpl in name_templates:
            _add(out, existing, rng, tmpl.format(n=name, y=year, r=region, l=leader), name, _pool(names, name)[:3], diff, names)


# 1 — Bhakti / Sufi (saint, movement, region)
BHAKTI: list[tuple[str, str, str]] = [
    ("കബീർ", "നിർഗുണ ഭക്തി", "വാരണാസി"),
    ("തുക്കാരാം", "വാർകരി", "മഹാരാഷ്ട്ര"),
    ("നാമദേവ്", "വാർകരി", "മഹാരാഷ്ട്ര"),
    ("ജ്ഞാനേശ്വർ", "വാർകരി", "മഹാരാഷ്ട്ര"),
    ("ഏകനാഥ്", "വാർകരി", "മഹാരാഷ്ട്ര"),
    ("സന്ത് റാമദാസ്", "രാമ ഭക്തി", "മഹാരാഷ്ട്ര"),
    ("ചൈതന്യ മഹാപ്രഭു", "ഗൗഡീയ വൈഷ്ണവം", "ബംഗാൾ"),
    ("ഹരിദാസ് ഠാക്കൂർ", "ഹരി കീർത്തന", "ബംഗാൾ"),
    ("സൂർദാസ്", "കൃഷ്ണ ഭക്തി", "മഥുര"),
    ("മീരാബായി", "കൃഷ്ണ ഭക്തി", "മേവാർ"),
    ("റാമാനുജർ", "ശ്രീവൈഷ്ണവം", "തമിഴ്നാട്"),
    ("നമ്മാഴ്വാർ", "ആഴ്വാർ", "തമിഴ്നാട്"),
    ("ബസവണ്ണ", "വീരശൈവം", "കർണാടക"),
    ("അക്കka മഹാദേvi", "വീരശൈവം", "കർണാടക"),
    ("ശങ്കaradeva", "നeo-വൈഷ്ണവം", "അസം"),
    ("മധusudhan", "വൈഷ്ണവം", "ബംഗാൾ"),
    ("വല്ലabhacharya", "പushtimarg", "മഥura"),
    ("രavidas", "നiർഗുണ ഭക്തി", "വാരണasi"),
    ("ഗuru നanak", "സikh", "പഞ്ചab"),
    ("തulsidas", "രamcharitmanas", "അyodhya"),
    ("വidyapati", "maithili", "ബihar"),
    ("jayadeva", "gita govinda", "ഒdisha"),
    ("narsinh mehta", "gujarati", "ഗujarat"),
    ("ramananda", "ram bhakti", "വാരണasi"),
    ("ഖ്വാജാ മൗinുദ്ദീൻ ചിശ്തി", "ചിശ്തി", "അജ്മീർ"),
    ("നിസാമുദ്ദീൻ ഔലിയ", "ചിശ്തി", "ദilli"),
    ("അമീർ ഖusrau", "ചിശ്തി", "ദilli"),
    ("ശേഖ് ഫarid", "ചിശ്തി", "പഞ്ചab"),
    ("ബulleh Shah", "സufi", "പഞ്ചab"),
    ("ശേഖ് അhmad Sirhindi", "naqshbandi", "പഞ്ചab"),
    ("ബande Nawaz", "ചിശ്തി", "ഗulbarga"),
    ("ലal Shahbaz", "സufi", "സindh"),
    ("സalim Chishti", "ചിശ്തി", "ഫത്തേhpur"),
    ("ബahauddin Zakariya", "suhrawardi", "മultan"),
    ("qutbuddin Bakhtiyar Kaki", "ചിശ്തി", "ദilli"),
    ("nasiruddin Chiragh", "ചിശ്തി", "ദilli"),
    ("shah abdul latif", "സufi", "സindh"),
    ("waris shah", "സufi", "പഞ്ചab"),
    ("nooruddin wali", "rishism", "കashmir"),
    ("lal ded", "kashmir shaivism", "കashmir"),
    ("poigai alvar", "alvar", "തamil"),
    ("boothathalvar", "alvar", "തamil"),
    ("peyalvar", "alvar", "തamil"),
    ("thirumalisai alvar", "alvar", "തamil"),
    ("thondaradippodi alvar", "alvar", "തamil"),
    ("thiruppaan alvar", "alvar", "തamil"),
    ("thirumangai alvar", "alvar", "തamil"),
    ("periyalvar", "alvar", "തamil"),
    ("kulasekhara alvar", "alvar", "കerala"),
    ("and al", "alvar", "തamil"),
    ("madhurakavi alvar", "alvar", "തamil"),
    ("nammalvar", "alvar", "തamil"),
    ("saint dnyaneshwar", "warkari", "മaharashtra"),
    ("sant chokhamela", "warkari", "മaharashtra"),
    ("sant muktabai", "warkari", "മaharashtra"),
    ("sant sopan", "warkari", "മaharashtra"),
    ("sant kanhopatra", "warkari", "മaharashtra"),
    ("sant janabai", "warkari", "മaharashtra"),
    ("sant bahinabai", "warkari", "മaharashtra"),
    ("sant sena", "warkari", "മaharashtra"),
    ("sant goroba", "warkari", "മaharashtra"),
]

# PLACEHOLDER_REMOVE
