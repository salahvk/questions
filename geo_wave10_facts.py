#!/usr/bin/env python3
"""Wave 10 geography facts — 10 PSC topic types (climate, soils, physiography, passes, minerals, energy, transport, ocean, maps, wetlands)."""

from __future__ import annotations

import random
import re
from collections import defaultdict

import geo_wave4_facts as w4
from geography_facts import INDIAN_DAMS, INDIA_PORTS, WORLD_FACTS, INDIAN_NATIONAL_PARKS, MOUNTAIN_PEAKS, ISLAND_SEAS
from refill_common import Candidate, add_candidate

MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")

EXTRA_PASSES: list[tuple[str, str]] = [
    ("\u0d2a\u0d3e\u0d32\u0d15\u0d4d\u0d15\u0d3e\u0d1f\u0d4d \u0d1a\u0d41\u0d30\u0d02", "\u0d15\u0d47\u0d30\u0d33"),
    ("\u0d37\u0d46\u0d02\u0d15\u0d4b\u0d1f\u0d4d\u0d1f \u0d1a\u0d41\u0d30\u0d02", "\u0d24\u0d2e\u0d3f\u0d34\u0d4d\u0d28\u0d3e\u0d1f\u0d4d"),
    ("\u0d38\u0d47\u0d32\u0d3e \u0d15\u0d4b\u0d1f\u0d41\u0d15\u0d4d\u0d15\u0d4d", "\u0d05\u0d30\u0d41\u0d23\u0d3e\u0d1a\u0d32 \u0d07\u0d30\u0d26\u0d47\u0d36\u0d02"),
    ("\u0d28\u0d40\u0d24\u0d3f \u0d15\u0d4b\u0d1f\u0d41\u0d15\u0d4d\u0d15\u0d4d", "\u0d09\u0d24\u0d4d\u0d24\u0d30\u0d3e\u0d16\u0d23\u0d4d\u0d1f\u0d4d"),
    ("\u0d2c\u0d3e\u0d30\u0d32\u0d3e\u0d1a\u0d4d\u0d1a \u0d32\u0d3e", "\u0d39\u0d3f\u0d2e\u0d3e\u0d1a\u0d32 \u0d07\u0d30\u0d26\u0d47\u0d36\u0d02"),
    ("\u0d2e\u0d3e\u0d7c\u0d38\u0d3f\u0d2e\u0d3f\u0d15\u0d4d \u0d32\u0d3e", "\u0d32\u0d26\u0d3e\u0d15\u0d4d\u0d15\u0d4d"),
    ("\u0d2b\u0d4b\u0d1f\u0d41 \u0d32\u0d3e", "\u0d32\u0d26\u0d3e\u0d15\u0d4d\u0d15\u0d4d"),
    ("\u0d2f\u0d02\u0d17\u0d4d\u0d2f\u0d3e\u0d2a\u0d4d \u0d32\u0d3e", "\u0d38\u0d3f\u0d15\u0d4d\u0d15\u0d3f\u0d02"),
]

CLIMATE_TYPES: list[tuple[str, str]] = [
    ("\u0d09\u0d37\u0d4d\u0d23\u0d2e\u0d47\u0d18\u0d32", "\u0d15\u0d47\u0d30\u0d33"),
    ("\u0d36\u0d40\u0d24\u0d4b\u0d37\u0d4d\u0d23", "\u0d39\u0d3f\u0d2e\u0d3e\u0d1a\u0d32 \u0d07\u0d30\u0d26\u0d47\u0d36\u0d02"),
    ("\u0d35\u0d30\u0d23\u0d4d\u0d1f", "\u0d30\u0d3e\u0d1c\u0d38\u0d4d\u0d25\u0d3e\u0d7a"),
    ("\u0d06\u0d32\u0d4d\u0d2a\u0d48\u0d7b", "\u0d32\u0d26\u0d3e\u0d15\u0d4d\u0d15\u0d4d"),
    ("\u0d09\u0d2a\u0d4b\u0d2a\u0d30\u0d26\u0d47\u0d36", "\u0d2a\u0d1e\u0d4d\u0d1a\u0d3e\u0d2c\u0d4d"),
    ("\u0d38\u0d41\u0d37\u0d4d\u0d15", "\u0d17\u0d41\u0d1c\u0d30\u0d3e\u0d24\u0d4d\u0d24\u0d4d"),
]

SOIL_REGIONS: list[tuple[str, str]] = [
    ("\u0d32\u0d3e\u0d31\u0d4d\u0d31\u0d30\u0d48\u0d1f\u0d4d", "\u0d15\u0d47\u0d30\u0d33"),
    ("\u0d05\u0d32\u0d41\u0d35\u0d3f\u0d2f\u0d32\u0d4d", "\u0d2a\u0d1e\u0d4d\u0d1a\u0d3e\u0d2c\u0d4d"),
    ("\u0d15\u0d31\u0d41\u0d24\u0d4d\u0d24 \u0d2e\u0d23\u0d4d\u0d23\u0d4d", "\u0d2e\u0d39\u0d3e\u0d30\u0d3e\u0d37\u0d4d\u0d1f\u0d4d\u0d30"),
    ("\u0d1a\u0d41\u0d35\u0d28\u0d4d\u0d28 \u0d2e\u0d23\u0d4d\u0d23\u0d4d", "\u0d24\u0d2e\u0d3f\u0d34\u0d4d\u0d28\u0d3e\u0d1f\u0d4d"),
    ("\u0d30\u0d46\u0d17\u0d42\u0d30\u0d4d", "\u0d2e\u0d39\u0d3e\u0d30\u0d3e\u0d37\u0d4d\u0d1f\u0d4d\u0d30"),
    ("\u0d09\u0d2a\u0d4d\u0d2a\u0d4d \u0d2e\u0d23\u0d4d\u0d23\u0d4d", "\u0d17\u0d41\u0d1c\u0d30\u0d3e\u0d24\u0d4d\u0d24\u0d4d"),
    ("\u0d35\u0d28 \u0d2e\u0d23\u0d4d\u0d23\u0d4d", "\u0d05\u0d38\u0d02"),
    ("\u0d2a\u0d40\u0d1f\u0d4d \u0d2e\u0d23\u0d4d\u0d23\u0d4d", "\u0d15\u0d47\u0d30\u0d33"),
    ("\u0d2a\u0d30\u0d4d\u0d35\u0d24 \u0d2e\u0d23\u0d4d\u0d23\u0d4d", "\u0d39\u0d3f\u0d2e\u0d3e\u0d1a\u0d32 \u0d07\u0d30\u0d26\u0d47\u0d36\u0d02"),
    ("\u0d32\u0d3e\u0d31\u0d4d\u0d31\u0d30\u0d48\u0d1f\u0d4d", "\u0d15\u0d30\u0d4d\u0d23\u0d3e\u0d1f\u0d15"),
    ("\u0d05\u0d32\u0d41\u0d35\u0d3f\u0d2f\u0d32\u0d4d", "\u0d09\u0d24\u0d4d\u0d24\u0d30\u0d3e\u0d07\u0d30\u0d4d\u0d1f\u0d4d"),
    ("\u0d1a\u0d41\u0d35\u0d28\u0d4d\u0d28 \u0d2e\u0d23\u0d4d\u0d23\u0d4d", "\u0d06\u0d28\u0d4d\u0d27\u0d4d\u0d30\u0d2a\u0d4d\u0d30\u0d26\u0d47\u0d36\u0d02"),
    ("\u0d32\u0d3e\u0d31\u0d4d\u0d31\u0d30\u0d48\u0d1f\u0d4d", "\u0d12\u0d21\u0d3f\u0d37"),
    ("\u0d05\u0d32\u0d41\u0d35\u0d3f\u0d2f\u0d32\u0d4d", "\u0d05\u0d38\u0d02"),
    ("\u0d15\u0d31\u0d41\u0d24\u0d4d\u0d24 \u0d2e\u0d23\u0d4d\u0d23\u0d4d", "\u0d17\u0d41\u0d1c\u0d30\u0d3e\u0d24\u0d4d\u0d24\u0d4d"),
    ("\u0d1a\u0d41\u0d35\u0d28\u0d4d\u0d28 \u0d2e\u0d23\u0d4d\u0d23\u0d4d", "\u0d24\u0d46\u0d32\u0d02\u0d15\u0d3e\u0d28"),
    ("\u0d32\u0d3e\u0d31\u0d4d\u0d31\u0d30\u0d48\u0d1f\u0d4d", "\u0d17\u0d42\u0d35"),
    ("\u0d05\u0d32\u0d41\u0d35\u0d3f\u0d2f\u0d32\u0d4d", "\u0d2c\u0d3f\u0d39\u0d3e\u0d7a"),
    ("\u0d15\u0d31\u0d41\u0d24\u0d4d\u0d24 \u0d2e\u0d23\u0d4d\u0d23\u0d4d", "\u0d2e\u0d27\u0d4d\u0d2f\u0d2a\u0d4d\u0d30\u0d26\u0d47\u0d36\u0d02"),
]

NH_ROUTES: list[tuple[str, str]] = [
    ("NH 44", "\u0d09\u0d24\u0d4d\u0d24\u0d30\u0d3e\u0d2f\u0d02\u0d1a\u0d46\u0d28\u0d4d\u0d28\u0d48-\u0d15\u0d28\u0d4d\u0d2f\u0d3e\u0d15\u0d41\u0d2e\u0d3e\u0d30\u0d3f"),
    ("NH 27", "\u0d09\u0d24\u0d4d\u0d24\u0d30\u0d3e\u0d2f\u0d02\u0d1a\u0d46\u0d28\u0d4d\u0d28\u0d48-\u0d17\u0d41\u0d35\u0d39\u0d3e\u0d1f\u0d3f"),
    ("NH 48", "\u0d09\u0d24\u0d4d\u0d24\u0d30\u0d3e\u0d2f\u0d02\u0d1a\u0d46\u0d28\u0d4d\u0d28\u0d48-\u0d09\u0d2e\u0d26\u0d3e\u0d35\u0d3e\u0d26\u0d4d"),
    ("NH 52", "\u0d09\u0d24\u0d4d\u0d24\u0d30\u0d3e\u0d2f\u0d02\u0d1a\u0d46\u0d28\u0d4d\u0d28\u0d48-\u0d38\u0d3e\u0d2e\u0d3e\u0d30\u0d3e"),
    ("NH 19", "\u0d09\u0d24\u0d4d\u0d24\u0d30\u0d3e\u0d2f\u0d02\u0d1a\u0d46\u0d28\u0d4d\u0d28\u0d48-\u0d15\u0d2a\u0d4d\u0d2a\u0d42\u0d30\u0d4d\u0d24\u0d32"),
    ("NH 16", "\u0d09\u0d24\u0d4d\u0d24\u0d30\u0d3e\u0d2f\u0d02\u0d1a\u0d46\u0d28\u0d4d\u0d28\u0d48-\u0d15\u0d2a\u0d4d\u0d2a\u0d42\u0d30\u0d4d\u0d24\u0d32"),
    ("NH 7", "\u0d09\u0d24\u0d4d\u0d24\u0d30\u0d3e\u0d2f\u0d02\u0d1a\u0d46\u0d28\u0d4d\u0d28\u0d48-\u0d15\u0d2a\u0d4d\u0d2a\u0d42\u0d30\u0d4d\u0d24\u0d32"),
    ("NH 31", "\u0d09\u0d24\u0d4d\u0d24\u0d30\u0d3e\u0d2f\u0d02\u0d1a\u0d46\u0d28\u0d4d\u0d28\u0d48-\u0d15\u0d2a\u0d4d\u0d2a\u0d42\u0d30\u0d4d\u0d24\u0d32"),
    ("NH 66", "\u0d09\u0d24\u0d4d\u0d24\u0d30\u0d3e\u0d2f\u0d02\u0d1a\u0d46\u0d28\u0d4d\u0d28\u0d48-\u0d15\u0d2a\u0d4d\u0d2a\u0d42\u0d30\u0d4d\u0d24\u0d32"),
    ("NH 75", "\u0d09\u0d24\u0d4d\u0d24\u0d30\u0d3e\u0d2f\u0d02\u0d1a\u0d46\u0d28\u0d4d\u0d28\u0d48-\u0d15\u0d2a\u0d4d\u0d2a\u0d42\u0d30\u0d4d\u0d24\u0d32"),
]

METRO_CITIES: list[tuple[str, str]] = [
    ('കൊൽക്കത്ത', 'പശ്ചിമബംഗാൾ'),
    ('ചെന്നൈ', 'തമിഴ്നാട്'),
    ('ബെംഗളൂരു', 'കർണാടക'),
    ('ഹൈദരാബാദ്', 'തെലങ്കാന'),
    ('മുംബൈ', 'മഹാരാഷ്ട്ര'),
    ('ന്യൂഡൽഹി', 'ദില്ലി'),
    ('അഹമദാബാദ്', 'ഗുജറാത്ത്'),
    ('പുണെ', 'മഹാരാഷ്ട്ര'),
    ('ജയ്പൂർ', 'രാജസ്ഥാൻ'),
    ('ലക്നൗ', 'ഉത്തരപ്രദേശ്'),
]

HYDRO_RIVER_STEMS = [
    "'{a}' ജലവൈദ്യുത അണക്കെട്ട് ഏത് നദിയിലാണ്?",
    "'{a}' ഹൈഡ്രോ പവർ പദ്ധതി ഏത് നദിയിൽ?",
    "'{a}' അണക്കെട്ട് നിർമ്മിച്ച നദി?",
    "'{a}' ജലസംഭരണ അണക്കെട്ട് ഏത് നദിയിലാണ്?",
]

ROCK_TYPES: list[tuple[str, str]] = [
    ("\u0d17\u0d4d\u0d30\u0d3e\u0d28\u0d48\u0d1f\u0d4d", "\u0d05\u0d17\u0d4d\u0d28\u0d3f \u0d36\u0d3f\u0d32"),
    ("\u0d2c\u0d38\u0d3e\u0d33\u0d4d\u0d32\u0d4d\u0d1f\u0d4d", "\u0d05\u0d17\u0d4d\u0d28\u0d3f \u0d36\u0d3f\u0d32"),
    ("\u0d1a\u0d41\u0d23\u0d4d\u0d23\u0d3e\u0d02\u0d2a\u0d4d \u0d36\u0d3f\u0d32", "\u0d09\u0d2a\u0d4d\u0d2a\u0d1f\u0d4d\u0d1f\u0d3f\u0d15 \u0d36\u0d3f\u0d32"),
    ("\u0d2e\u0d3e\u0d7c\u0d2c\u0d3f\u0d33\u0d4d", "\u0d30\u0d42\u0d2a\u0d3e\u0d28\u0d4d\u0d24\u0d30 \u0d36\u0d3f\u0d32"),
    ("\u0d06\u0d32\u0d4d\u0d2a\u0d48\u0d7b \u0d36\u0d3f\u0d32", "\u0d05\u0d17\u0d4d\u0d28\u0d3f \u0d36\u0d3f\u0d32"),
    ("\u0d36\u0d3f\u0d32\u0d3e\u0d15\u0d43\u0d24", "\u0d05\u0d17\u0d4d\u0d28\u0d3f \u0d36\u0d3f\u0d32"),
]

_STATE_NORM = {"കേരളം": "കേരള"}


def _norm_state(name: str) -> str:
    return _STATE_NORM.get(name, name)


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


def _state_pick(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    rows: list[tuple[str, str]],
    template: str,
    diff: str = "hard",
) -> None:
    by_st: dict[str, list[str]] = defaultdict(list)
    for name, state in rows:
        by_st[_norm_state(state)].append(name)
    for state, names in by_st.items():
        uniq = list(dict.fromkeys(names))
        if len(uniq) < 2:
            continue
        for name in uniq:
            _add(
                out,
                existing,
                rng,
                template.format(state=state),
                name,
                [x for x in uniq if x != name][:3],
                diff,
                uniq,
            )


ATMOSPHERE_DIRECT: list[tuple[str, str, list[str], str]] = [
    (q, a, w, d)
    for q, a, w, d in WORLD_FACTS
    if any(k in q for k in ("അന്തരീക്ഷ", "മൺസൂൺ", "കാറ്റ", "കാലാവസ്ഥ", "മഴ"))
]

ROCK_DIRECT: list[tuple[str, str, list[str], str]] = [
    (q, a, w, d)
    for q, a, w, d in WORLD_FACTS
    if "ശില" in q or "ഗ്രാനൈറ്റ്" in q or "മാർബിൾ" in q
]

HYDRO_STEMS = [
    "'{a}' ജലവൈദ്യുത അണക്കെട്ട് ഏത് സംസ്ഥാനത്താണ്?",
    "'{a}' ഹൈഡ്രോ ഇലക്ട്രിക് അണക്കെട്ടിന്റെ സംസ്ഥാനം?",
    "'{a}' ജലസംഭരണ/വൈദ്യുത അണക്കെട്ട് ഏത് സംസ്ഥാനത്ത്?",
    "'{a}' ബഹുമുഖ ആസൂത്രണ അണക്കെട്ട് ഏത് സംസ്ഥാനത്താണ്?",
    "'{a}' ഹൈഡ്രോ പവർ പദ്ധതി ഏത് സംസ്ഥാനത്താണ്?",
    "'{a}' അണക്കെട്ട് സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം?",
    "'{a}' ജലാശയ അണക്കെട്ട് ഏത് സംസ്ഥാനത്താണ്?",
    "'{a}' ഡാം ഏത് സംസ്ഥാനത്താണ്?",
    "ഏത് സംസ്ഥാനത്താണ് '{a}' ജലവൈദ്യുത കേന്ദ്രം?",
    "'{a}' അണക്കെട്ട് നിർമ്മിച്ച സംസ്ഥാനം?",
    "'{a}' ഊർജ്ജ/ജലസംഭരണ അണക്കെട്ട് ഏത് സംസ്ഥാനത്ത്?",
    "'{a}' അണക്കെട്ട് ആസ്ഥാനപ്പെട്ടിരിക്കുന്ന സംസ്ഥാനം?",
]


def generate_wave10_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []

    # 1 — atmosphere & climate
    climate_states = list({s for _, s in w4.CLIMATE_PLACES})
    _pairs(
        out,
        existing,
        rng,
        w4.CLIMATE_PLACES,
        [
            "'{a}' ഏത് സംസ്ഥാനത്തിലെ പ്രശസ്ത കാലാവസ്ഥാ പ്രദേശം?",
            "'{a}' കാലാവസ്ഥാ പ്രദേശം ഏത് സംസ്ഥാനത്താണ്?",
            "ഏത് സംസ്ഥാനത്താണ് '{a}' സ്ഥിതി ചെയ്യുന്നത്?",
            "'{a}' സംബന്ധിച്ച സംസ്ഥാനം ഏത്?",
            "'{a}' പ്രദേശം ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' കാലാവസ്ഥാ സ്ഥലം ഏത് സംസ്ഥാനത്ത്?",
        ],
        climate_states,
    )
    ctype_names = list({c for c, _ in CLIMATE_TYPES})
    _pairs(
        out,
        existing,
        rng,
        CLIMATE_TYPES,
        [
            "'{b}' സംസ്ഥാനത്തിന്റെ പ്രധാന കാലാവസ്ഥാ തരം ഏത്?",
            "'{b}'-ൽ പ്രധാനമായി കാണപ്പെടുന്ന കാലാവസ്ഥ '{a}' — '{a}' ഏത്?",
        ],
        ctype_names,
    )
    _state_pick(
        out,
        existing,
        rng,
        w4.CLIMATE_PLACES,
        "'{state}' സംസ്ഥാനത്തിലെ പ്രശസ്ത കാലാവസ്ഥാ പ്രദേശം?",
    )
    for q, a, w, d in ATMOSPHERE_DIRECT:
        _add(out, existing, rng, q, a, w, d, w + [a])

    # 2 — soils & rocks
    soil_names = list({s for s, _ in SOIL_REGIONS})
    soil_states = list({st for _, st in SOIL_REGIONS})
    _pairs(
        out,
        existing,
        rng,
        SOIL_REGIONS,
        [
            "'{a}' മണ്ണ് പ്രധാനമായി ഏത് സംസ്ഥാനത്ത്/പ്രദേശത്ത്?",
            "'{a}' മണ്ണ് കൂടുതൽ കാണപ്പെടുന്ന പ്രദേശം?",
            "'{a}' മണ്ണിന്റെ പ്രധാന പ്രദേശം?",
        ],
        soil_states,
    )
    for soil, region in SOIL_REGIONS:
        _add(
            out,
            existing,
            rng,
            f"'{region}' പ്രദേശത്ത് പ്രധാനമായി കാണപ്പെടുന്ന മണ്ണ്?",
            soil,
            _pool(soil_names, soil)[:3],
            "medium",
            soil_names,
        )
    for q, a, w, d in ROCK_DIRECT:
        _add(out, existing, rng, q, a, w, d, w + [a])

    # 3 — physiography
    plat_names = list({p for p, _ in w4.INDIAN_PLATEAUS})
    plat_regs = list({r for _, r in w4.INDIAN_PLATEAUS})
    _pairs(
        out,
        existing,
        rng,
        w4.INDIAN_PLATEAUS,
        [
            "'{a}' ഏത് ഭാഗത്ത്/പ്രദേശത്താണ്?",
            "'{a}' ഭൂമിശാസ്ത്രപരമായ പ്രദേശം ഏത് ഭാഗത്ത്?",
            "'{a}' സ്ഥിതി ചെയ്യുന്ന ഭൂമിശാസ്ത്ര മേഖല?",
        ],
        plat_regs,
    )
    _pairs(
        out,
        existing,
        rng,
        w4.INDIAN_PLATEAUS,
        ["'{b}' ഭാഗത്ത് സ്ഥിതി ചെയ്യുന്ന പീഠഭൂമി/പ്രദേശം?"],
        plat_names,
    )

    # 4 — mountain passes
    all_passes = list(w4.HIMALAYAN_PASSES) + EXTRA_PASSES
    pass_states = list({s for _, s in all_passes})
    _pairs(
        out,
        existing,
        rng,
        all_passes,
        [
            "'{a}' ഏത് സംസ്ഥാനത്തിലെ പർവത കൊടുക്ക്?",
            "'{a}' കൊടുക്ക് സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം?",
            "ഏത് സംസ്ഥാനത്താണ് '{a}' കൊടുക്ക്?",
            "'{a}' പർവത കയറ്റം ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' ചുരം/കൊടുക്ക് ഏത് സംസ്ഥാനത്ത്?",
        ],
        pass_states,
    )
    _state_pick(
        out,
        existing,
        rng,
        all_passes,
        "'{state}' സംസ്ഥാനത്തിലെ പ്രധാന പർവത കൊടുക്ക്?",
    )

    # 5 — minerals
    mineral_states = list({s for _, s in w4.MINERAL_REGIONS})
    _pairs(
        out,
        existing,
        rng,
        w4.MINERAL_REGIONS,
        [
            "'{a}' ഏത് സംസ്ഥാനത്തിലെ ഖനി/ധാതു പ്രദേശം?",
            "'{a}' ഖനി കേന്ദ്രം ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' ഖനി/വ്യവസായ പ്രദേശം ഏത് സംസ്ഥാനത്ത്?",
            "'{a}' പ്രധാന ഖനി മേഖല ഏത് സംസ്ഥാനത്താണ്?",
        ],
        mineral_states,
    )
    _state_pick(
        out,
        existing,
        rng,
        w4.MINERAL_REGIONS,
        "'{state}' സംസ്ഥാനത്തിലെ പ്രധാന ഖനി/വ്യവസായ കേന്ദ്രം?",
    )

    # 6 — energy (nuclear/thermal + hydro dams)
    power_states = list({s for _, s in w4.POWER_STATIONS})
    _pairs(
        out,
        existing,
        rng,
        w4.POWER_STATIONS,
        [
            "'{a}' ഏത് സംസ്ഥാനത്തിലെ വൈദ്യുത/ഊർജ്ജ കേന്ദ്രം?",
            "'{a}' ആണവ/താപ വൈദ്യുത കേന്ദ്രം ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' ഊർജ്ജ കേന്ദ്രം ഏത് സംസ്ഥാനത്ത്?",
        ],
        power_states,
    )
    _state_pick(
        out,
        existing,
        rng,
        w4.POWER_STATIONS,
        "'{state}' സംസ്ഥാനത്തിലെ പ്രധാന വൈദ്യുത/ഊർജ്ജ കേന്ദ്രം?",
    )
    dam_states = list({_norm_state(s) for _, _, s in INDIAN_DAMS})
    for dam, _river, state in INDIAN_DAMS:
        st = _norm_state(state)
        for tmpl in HYDRO_STEMS:
            _add(
                out,
                existing,
                rng,
                tmpl.format(a=dam),
                st,
                _pool(dam_states, st)[:3],
                "medium",
                dam_states,
            )

    # 7 — transport
    zones = list({z for z, _ in w4.RAILWAY_ZONES})
    hqs = list({h for _, h in w4.RAILWAY_ZONES})
    _pairs(
        out,
        existing,
        rng,
        w4.RAILWAY_ZONES,
        [
            "'{a}' റെയിൽവേ സോണിന്റെ ആസ്ഥാനം?",
            "'{b}' ഏത് റെയിൽവേ സോണിന്റെ ആസ്ഥാനമാണ്?",
            "'{a}' സോണിന്റെ ആസ്ഥാന നഗരം?",
        ],
        hqs,
    )
    for zone, hq in w4.RAILWAY_ZONES:
        _add(
            out,
            existing,
            rng,
            f"'{hq}' ഏത് റെയിൽവേ സോണിന്റെ ആസ്ഥാനമാണ്?",
            zone,
            _pool(zones, zone)[:3],
            "medium",
            zones,
        )
    port_states = list({_norm_state(s) for _, s in INDIA_PORTS})
    for port, state in INDIA_PORTS:
        st = _norm_state(state)
        _add(
            out,
            existing,
            rng,
            f"'{port}' തുറമുഖം സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം?",
            st,
            _pool(port_states, st)[:3],
            "medium",
            port_states,
        )
    _state_pick(
        out,
        existing,
        rng,
        [(p, s) for p, s in INDIA_PORTS],
        "'{state}' സംസ്ഥാനത്തിലെ പ്രധാന തുറമുഖം?",
    )

    # 8 — oceanography
    strait_names = [s for s, _ in w4.STRAITS]
    strait_conn = list({c for _, c in w4.STRAITS})
    for name, conn in w4.STRAITS:
        _add(
            out,
            existing,
            rng,
            f"ഏത് കടലിടുക്ക് {conn} ബന്ധിപ്പിക്കുന്നു?",
            name,
            _pool(strait_names, name)[:3],
            "medium",
            strait_names,
        )
        _add(
            out,
            existing,
            rng,
            f"'{name}' കടലിടുക്ക് ബന്ധിപ്പിക്കുന്ന പ്രദേശങ്ങൾ?",
            conn,
            _pool(strait_conn, conn)[:3],
            "hard",
            strait_conn,
        )
    for q, a, w, d in WORLD_FACTS:
        if any(k in q for k in ("സമുദ്ര", "കടൽ", "ധാര", "ട്രെഞ്ച്", "കടലിടുക്ക്")):
            _add(out, existing, rng, q, a, w, d, w + [a])

    # 9 — maps (minimal direct; expand via WORLD if present)
    for q, a, w, d in WORLD_FACTS:
        if "മാപ്പ" in q or "ടോപ്പോ" in q:
            _add(out, existing, rng, q, a, w, d, w + [a])

    # 10 — wetlands & environmental sites
    bio_states = list({s for _, s in w4.BIOSPHERE_RESERVES})
    _pairs(
        out,
        existing,
        rng,
        w4.BIOSPHERE_RESERVES,
        [
            "'{a}' ജൈവവൈവിധ്യ സംരക്ഷിത പ്രദേശം ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' ബയോസ്ഫിയർ റിസർവ് ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' ജൈവവൈവിധ്യ റിസർവ് ഏത് സംസ്ഥാനത്ത്?",
        ],
        bio_states,
    )
    lake_states = list({s for _, s in w4.INDIAN_LAKES})
    _pairs(
        out,
        existing,
        rng,
        w4.INDIAN_LAKES,
        [
            "'{a}' പ്രധാന തടാകം ഏത് സംസ്ഥാനത്ത്?",
            "'{a}' റാംസർ/നെല്ല് തടാകം ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' തടാകം/ജലാശയം ഏത് സംസ്ഥാനത്ത്?",
        ],
        lake_states,
    )
    sanct_states = list({s for _, s in w4.WILDLIFE_SANCTUARIES})
    _pairs(
        out,
        existing,
        rng,
        w4.WILDLIFE_SANCTUARIES,
        [
            "'{a}' വന്യജീവി സങ്കേതം ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' വന്യജീവി/നെല്ല് സംരക്ഷണ കേന്ദ്രം ഏത് സംസ്ഥാനത്ത്?",
        ],
        sanct_states,
    )
    _state_pick(
        out,
        existing,
        rng,
        w4.BIOSPHERE_RESERVES,
        "'{state}' സംസ്ഥാനത്തിലെ ജൈവവൈവിധ്യ സംരക്ഷിത പ്രദേശം?",
    )
    _state_pick(
        out,
        existing,
        rng,
        w4.INDIAN_LAKES,
        "'{state}' സംസ്ഥാനത്തിലെ പ്രധാന തടാകം/ജലാശയം?",
    )


    dam_rivers = list({r for _, r, _ in INDIAN_DAMS})
    for dam, river, _state in INDIAN_DAMS:
        for tmpl in HYDRO_RIVER_STEMS:
            _add(
                out,
                existing,
                rng,
                tmpl.format(a=dam),
                river,
                _pool(dam_rivers, river)[:3],
                "medium",
                dam_rivers,
            )

    rock_types = list({t for _, t in ROCK_TYPES})
    _pairs(
        out,
        existing,
        rng,
        ROCK_TYPES,
        [
            "'{a}' ഏത് തരം ശിലയാണ്?",
            "'{a}' ശില '{b}' തരത്തിൽ പെടുന്നു — '{b}'?",
        ],
        rock_types,
    )

    nh_names = list({n for n, _ in NH_ROUTES})
    nh_routes = list({r for _, r in NH_ROUTES})
    _pairs(
        out,
        existing,
        rng,
        NH_ROUTES,
        [
            "'{a}' ദേശീയ ഹൈവേ ബന്ധിപ്പിക്കുന്ന പ്രധാന നഗരങ്ങൾ?",
            "'{a}' NH ഏത് പ്രദേശങ്ങൾ ബന്ധിപ്പിക്കുന്നു?",
        ],
        nh_routes,
    )
    for nh, route in NH_ROUTES:
        _add(
            out,
            existing,
            rng,
            f"ഏത് ദേശീയ ഹൈവേ {route} ബന്ധിപ്പിക്കുന്നു?",
            nh,
            _pool(nh_names, nh)[:3],
            "hard",
            nh_names,
        )

    metro_cities = list({c for c, _ in METRO_CITIES})
    metro_states = list({s for _, s in METRO_CITIES})
    _pairs(
        out,
        existing,
        rng,
        METRO_CITIES,
        [
            "'{a}' ഏത് സംസ്ഥാനത്തിലെ പ്രധാന മെട്രോ/ഗതാഗത നഗരം?",
            "'{a}' നഗരം ഏത് സംസ്ഥാനത്താണ്?",
        ],
        metro_states,
    )

    park_states = list({_norm_state(s) for _, s in INDIAN_NATIONAL_PARKS})
    for park, state in INDIAN_NATIONAL_PARKS:
        st = _norm_state(state)
        _add(
            out,
            existing,
            rng,
            f"'{park}' പരിസ്ഥിതി/വന സംരക്ഷിത പ്രദേശം ഏത് സംസ്ഥാനത്താണ്?",
            st,
            _pool(park_states, st)[:3],
            "medium",
            park_states,
        )
    _state_pick(
        out,
        existing,
        rng,
        [(p, s) for p, s in INDIAN_NATIONAL_PARKS],
        "'{state}' സംസ്ഥാനത്തിലെ പ്രധാന ദേശീയോദ്യാനം/സംരക്ഷിത വനം?",
    )


    for park, state in INDIAN_NATIONAL_PARKS:
        st = _norm_state(state)
        _add(
            out,
            existing,
            rng,
            f"'{park}' ദേശീയോദ്യാനം/വന്യജീവി സംരക്ഷണ പ്രദേശം ഏത് സംസ്ഥാനത്താണ്?",
            st,
            _pool(park_states, st)[:3],
            "medium",
            park_states,
        )
        _add(
            out,
            existing,
            rng,
            f"'{park}' സംരക്ഷിത വനമേഖല ഏത് സംസ്ഥാനത്ത്?",
            st,
            _pool(park_states, st)[:3],
            "medium",
            park_states,
        )

    hill_states = list({s for _, s in w4.HILL_STATIONS})
    _pairs(
        out,
        existing,
        rng,
        w4.HILL_STATIONS,
        [
            "'{a}' ഏത് സംസ്ഥാനത്തിലെ ഹിൽ സ്റ്റേഷൻ/ശീതോഷ്ണ കേന്ദ്രം?",
            "'{a}' ഹിൽ സ്റ്റേഷൻ ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' കാലാവസ്ഥാ/പർവത കേന്ദ്രം ഏത് സംസ്ഥാനത്ത്?",
        ],
        hill_states,
    )

    fall_states = list({s for _, s in w4.WATERFALLS})
    _pairs(
        out,
        existing,
        rng,
        w4.WATERFALLS,
        [
            "'{a}' ജലപാതം/മലിനീര്‍പാതം ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' പ്രശസ്ത ജലപാതം ഏത് സംസ്ഥാനത്ത്?",
        ],
        fall_states,
    )

    extra_hydro = [
        "'{a}' അണക്കെട്ട് ഏത് നദിയുടെ ഊർജ്ജ പദ്ധതിയാണ്?",
        "'{a}' ജലവൈദ്യുത പദ്ധതി സ്ഥിതി ചെയ്യുന്ന നദി?",
    ]
    for dam, river, _state in INDIAN_DAMS:
        for tmpl in extra_hydro:
            _add(
                out,
                existing,
                rng,
                tmpl.format(a=dam),
                river,
                _pool(dam_rivers, river)[:3],
                "medium",
                dam_rivers,
            )


    for ctype, state in CLIMATE_TYPES:
        _add(
            out,
            existing,
            rng,
            f"'{state}' സംസ്ഥാനത്തിന്റെ പ്രധാന കാലാവസ്ഥാ തരം?",
            ctype,
            _pool(ctype_names, ctype)[:3],
            "easy",
            ctype_names,
        )

    for name, conn in w4.STRAITS:
        _add(
            out,
            existing,
            rng,
            f"'{name}' കടലിടുക്ക് ഏത് പ്രദേശങ്ങളെ ബന്ധിപ്പിക്കുന്നു?",
            conn,
            _pool(strait_conn, conn)[:3],
            "hard",
            strait_conn,
        )

    for lake, state in w4.INDIAN_LAKES:
        st = _norm_state(state)
        _add(
            out,
            existing,
            rng,
            f"'{lake}' തടാകം/ജലാശയം സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം?",
            st,
            _pool(lake_states, st)[:3],
            "medium",
            lake_states,
        )

    for bio, state in w4.BIOSPHERE_RESERVES:
        st = _norm_state(state)
        _add(
            out,
            existing,
            rng,
            f"'{bio}' ജൈവവൈവിധ്യ ഹോട്ട്സ്പോട്ട് ഏത് സംസ്ഥാനത്താണ്?",
            st,
            _pool(bio_states, st)[:3],
            "medium",
            bio_states,
        )


    unesco_states = list({s for _, s in w4.UNESCO_SITES})
    _pairs(
        out,
        existing,
        rng,
        w4.UNESCO_SITES,
        [
            "'{a}' പരിസ്ഥിതി/പൈതൃക സംരക്ഷണ കേന്ദ്രം ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' യുനെസ്കോ ലോക പൈതൃക സ്ഥലം ഏത് സംസ്ഥാനത്ത്?",
        ],
        unesco_states,
    )

    desert_regs = list({r for _, r in w4.WORLD_DESERTS})
    _pairs(
        out,
        existing,
        rng,
        w4.WORLD_DESERTS,
        [
            "'{a}' മരുഭൂമി ഏത് ഭാഗത്ത്/ഖണ്ഡത്താണ്?",
            "'{a}' മരുഭൂമി സ്ഥിതി ചെയ്യുന്ന പ്രദേശം?",
        ],
        desert_regs,
    )

    beach_states = list({s for _, s in w4.INDIAN_BEACHES})
    _pairs(
        out,
        existing,
        rng,
        w4.INDIAN_BEACHES,
        [
            "'{a}' പ്രശസ്ത കടൽത്തീരം/ബീച്ച് ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' ബീച്ച് ഏത് സംസ്ഥാനത്ത്?",
        ],
        beach_states,
    )

    for zone, hq in w4.RAILWAY_ZONES:
        _add(
            out,
            existing,
            rng,
            f"'{zone}' റെയിൽവേ സോണിന്റെ ആസ്ഥാന നഗരം?",
            hq,
            _pool(hqs, hq)[:3],
            "medium",
            hqs,
        )


    for station, state in w4.POWER_STATIONS:
        st = _norm_state(state)
        _add(
            out,
            existing,
            rng,
            f"'{station}' നാഷണൽ/താപ വൈദ്യുത കേന്ദ്രം ഏത് സംസ്ഥാനത്താണ്?",
            st,
            _pool(power_states, st)[:3],
            "medium",
            power_states,
        )
        _add(
            out,
            existing,
            rng,
            f"'{station}' ഊർജ്ജ ഉത്പാദന കേന്ദ്രം ഏത് സംസ്ഥാനത്ത്?",
            st,
            _pool(power_states, st)[:3],
            "medium",
            power_states,
        )

    for pname, pstate in w4.CLIMATE_PLACES:
        st = _norm_state(pstate)
        _add(
            out,
            existing,
            rng,
            f"'{pname}' പ്രദേശം ഏത് സംസ്ഥാനത്തിന്റെ കാലാവസ്ഥാ സ്ഥലമാണ്?",
            st,
            _pool(climate_states, st)[:3],
            "medium",
            climate_states,
        )

    for mineral, mstate in w4.MINERAL_REGIONS:
        st = _norm_state(mstate)
        _add(
            out,
            existing,
            rng,
            f"'{mineral}' പ്രദേശം ഏത് സംസ്ഥാനത്തിലെ ഖനി/വ്യവസായ മേഖല?",
            st,
            _pool(mineral_states, st)[:3],
            "medium",
            mineral_states,
        )


    for p, s in all_passes:
        _add(
            out,
            existing,
            rng,
            f"'{p}' പർവത കൊടുക്ക് കൊടുക്ക് ഏത് സംസ്ഥാനത്താണ്?",
            _norm_state(s),
            _pool(pass_states, _norm_state(s))[:3],
            "medium",
            pass_states,
        )


    for port, state in INDIA_PORTS:
        st = _norm_state(state)
        _add(
            out,
            existing,
            rng,
            f"'{port}' കപ്പൽ തുറമുഖം ഏത് സംസ്ഥാനത്താണ്?",
            st,
            _pool(port_states, st)[:3],
            "medium",
            port_states,
        )

    return out

HYDRO_STEMS_W2 = [
    "'{a}' എന്ന അണക്കെട്ട് സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം?",
    "'{a}' അണക്കെട്ട് കാണപ്പെടുന്ന ഇന്ത്യൻ സംസ്ഥാനം?",
    "'{a}' ജലസംഭരണ കേന്ദ്രം ഏത് സംസ്ഥാനത്ത്?",
    "'{a}' അണക്കെട്ട് ഏതു സംസ്ഥാന ഭൂപ്രദേശത്താണ്?",
    "'{a}' ഹൈഡ്രോ ഇലക്ട്രിക് ഡാം സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം?",
    "'{a}' അണക്കെട്ട് നിർമ്മിച്ച സംസ്ഥാനം ഏതാണ്?",
    "'{a}' ജലവൈദ്യുത പദ്ധതിയുടെ സംസ്ഥാനം?",
    "'{a}' അണക്കെട്ട് സ്ഥിതി ചെയ്യുന്ന ഇന്ത്യൻ സംസ്ഥാനം?",
    "'{a}' ഡാമിന്റെ സംസ്ഥാനം?",
    "'{a}' ജലാശയ പദ്ധതി ഏത് സംസ്ഥാനത്താണ്?",
    "'{a}' അണക്കെട്ട് ഏത് ഭാഗത്ത് നിർമ്മിച്ചിട്ടുണ്ട്?",
    "'{a}' വൈദ്യുത അണക്കെട്ട് സംസ്ഥാനം?",
    "'{a}' ജലസംഭരണ-വൈദ്യുത അണക്കെട്ട് ഏത് സംസ്ഥാനത്ത്?",
    "'{a}' അണക്കെട്ട് കെട്ടിയ സംസ്ഥാനം?",
    "'{a}' ഹൈഡ്രോ പ്രോജക്റ്റ് സംസ്ഥാനം?",
]

HYDRO_RIVER_W2 = [
    "'{a}' അണക്കെട്ട് ഏത് നദിയുടെ തീരത്താണ്?",
    "'{a}' ജലവൈദ്യുത പദ്ധതി ഏത് നദിയിൽ കെട്ടിയിരിക്കുന്നു?",
    "'{a}' ഡാം കെട്ടിയിരിക്കുന്ന നദി?",
    "'{a}' അണക്കെട്ട് നിർമ്മിച്ച നദിയുടെ പേര്?",
    "'{a}' ജലസംഭരണ അണക്കെട്ട് ഏത് നദിയിൽ?",
    "'{a}' ഹൈഡ്രോ ഇലക്ട്രിക് അണക്കെട്ട് ഏത് നദിയിലാണ്?",
    "'{a}' അണക്കെട്ട് സ്ഥിതി ചെയ്യുന്ന നദി?",
    "'{a}' വൈദ്യുത അണക്കെട്ട് ഏത് നദിയിൽ?",
]

PARK_STEMS_W2 = [
    "'{a}' ദേശീയോദ്യാനം ഏത് സംസ്ഥാന ഭൂപ്രദേശത്താണ്?",
    "'{a}' വന്യജീവി സംരക്ഷണ പാർക്ക് ഏത് സംസ്ഥാനത്ത്?",
    "'{a}' പരിസ്ഥിതി സംരക്ഷിത വനം ഏത് സംസ്ഥാനത്താണ്?",
    "'{a}' ദേശീയോദ്യാന/വന്യജീവി മേഖല ഏത് സംസ്ഥാനത്ത്?",
    "'{a}' സംരക്ഷിത വനപ്രദേശം ഏത് സംസ്ഥാനത്താണ്?",
]

PEAK_STEMS_W2 = [
    "'{a}' കൊടുമുടി/പീക്ക് ഏത് ഭൂമിശാസ്ത്ര മേഖലയിലാണ്?",
    "'{a}' ഉച്ചനം/പീക്ക് സ്ഥിതി ചെയ്യുന്ന മേഖല?",
    "'{a}' പർവത ശിഖരം ഏത് ഭാഗത്താണ്?",
]

ISLAND_SEA_STEMS_W2 = [
    "'{a}' ദ്വീപ്/പ്രദേശം ഏത് സമുദ്രത്തിലാണ്?",
    "'{a}' സ്ഥിതി ചെയ്യുന്ന സമുദ്രം/കടൽ?",
]

MINERAL_STEMS_W2 = [
    "'{a}' ഖനി/ധാതു പ്രദേശം ഏത് സംസ്ഥാന ഭൂപ്രദേശത്താണ്?",
    "'{a}' പ്രധാന ഖനി മേഖല ഏത് സംസ്ഥാനത്ത്?",
    "'{a}' വ്യവസായ-ഖനി കേന്ദ്രം ഏത് സംസ്ഥാനത്താണ്?",
]

PASS_STEMS_W2 = [
    "'{a}' പർവത കൊടുക്ക് ഏത് സംസ്ഥാന ഭൂപ്രദേശത്താണ്?",
    "'{a}' ചുരം/ലാ കൊടുക്ക് ഏത് സംസ്ഥാനത്ത്?",
]

POWER_STEMS_W2 = [
    "'{a}' വൈദ്യുത/ആണവ കേന്ദ്രം ഏത് സംസ്ഥാനത്താണ്?",
    "'{a}' ഊർജ്ജ ഉത്പാദന യൂണിറ്റ് ഏത് സംസ്ഥാനത്ത്?",
]

RAIL_STEMS_W2 = [
    "'{a}' റെയിൽവേ സോൺ ആസ്ഥാനം '{b}' — '{b}' ഏത് സോണിന്റെ?",
    "'{a}' സോണിന്റെ ആസ്ഥാന നഗരം?",
]

CLIMATE_STEMS_W2 = [
    "'{a}' പ്രദേശം ഏത് സംസ്ഥാനത്തിന്റെ ഭാഗമാണ്?",
    "'{a}' കാലാവസ്ഥാ പ്രദേശം സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം?",
]

SOIL_STEMS_W2 = [
    "'{b}'-ൽ പ്രധാനമായി കാണപ്പെടുന്ന മണ്ണ്?",
]

BIOS_STEMS_W2 = [
    "'{a}' ജൈവവൈവിധ്യ സംരക്ഷണ കേന്ദ്രം ഏത് സംസ്ഥാനത്ത്?",
    "'{a}' ബയോസ്ഫിയർ റിസർവ് ഏത് സംസ്ഥാനത്താണ്?",
]

LAKE_STEMS_W2 = [
    "'{a}' തടാകം ഏത് സംസ്ഥാന ഭൂപ്രദേശത്താണ്?",
    "'{a}' ജലാശയം സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം?",
]

SANCT_STEMS_W2 = [
    "'{a}' വന്യജീവി സങ്കേതം ഏത് സംസ്ഥാന ഭൂപ്രദേശത്താണ്?",
    "'{a}' വന്യജീവി ആവാസകേന്ദ്രം ഏത് സംസ്ഥാനത്ത്?",
]

PORT_STEMS_W2 = [
    "'{a}' തുറമുഖ നഗരം ഏത് സംസ്ഥാനത്താണ്?",
    "'{a}' കപ്പൽ തുറമുഖം സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം?",
]

STRAIT_STEMS_W2 = [
    "ഏത് കടലിടുക്കാണ് {b} ബന്ധിപ്പിക്കുന്നത്?",
    "'{a}' കടലിടുക്ക് ബന്ധിപ്പിക്കുന്ന പ്രദേശം?",
]


def generate_wave10_wave2_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    """Second-wave templates — unique stems for 10 PSC topic types."""
    out: list[Candidate] = []
    all_passes = list(w4.HIMALAYAN_PASSES) + EXTRA_PASSES
    dam_states = list({_norm_state(s) for _, _, s in INDIAN_DAMS})
    dam_rivers = list({r for _, r, _ in INDIAN_DAMS})

    for dam, _river, state in INDIAN_DAMS:
        st = _norm_state(state)
        for tmpl in HYDRO_STEMS_W2:
            _add(out, existing, rng, tmpl.format(a=dam), st, _pool(dam_states, st)[:3], "medium", dam_states)

    for dam, river, _state in INDIAN_DAMS:
        for tmpl in HYDRO_RIVER_W2:
            _add(out, existing, rng, tmpl.format(a=dam), river, _pool(dam_rivers, river)[:3], "medium", dam_rivers)

    park_states = list({_norm_state(s) for _, s in INDIAN_NATIONAL_PARKS})
    for park, state in INDIAN_NATIONAL_PARKS:
        st = _norm_state(state)
        for tmpl in PARK_STEMS_W2:
            _add(out, existing, rng, tmpl.format(a=park), st, _pool(park_states, st)[:3], "medium", park_states)

    peak_regions = list({r for _, r, _ in MOUNTAIN_PEAKS})
    for peak, region, _h in MOUNTAIN_PEAKS:
        for tmpl in PEAK_STEMS_W2:
            _add(out, existing, rng, tmpl.format(a=peak), region, _pool(peak_regions, region)[:3], "hard", peak_regions)

    by_region: dict[str, list[str]] = defaultdict(list)
    for peak, region, _h in MOUNTAIN_PEAKS:
        by_region[region].append(peak)
    for region, peaks in by_region.items():
        uniq = list(dict.fromkeys(peaks))
        if len(uniq) < 2:
            continue
        for peak in uniq:
            _add(
                out,
                existing,
                rng,
                f"'{region}' മേഖലയിലെ പ്രധാന കൊടുമുടി/പീക്ക്?",
                peak,
                [x for x in uniq if x != peak][:3],
                "hard",
                uniq,
            )

    seas = list({s for _, s in ISLAND_SEAS})
    _pairs(out, existing, rng, ISLAND_SEAS, ISLAND_SEA_STEMS_W2, seas)
    for island, sea in ISLAND_SEAS:
        _add(
            out,
            existing,
            rng,
            f"ഏത് ദ്വീപ്/പ്രദേശം {sea}-ൽ സ്ഥിതി ചെയ്യുന്നു?",
            island,
            _pool([i for i, _ in ISLAND_SEAS], island)[:3],
            "medium",
            [i for i, _ in ISLAND_SEAS],
        )

    mineral_states = list({s for _, s in w4.MINERAL_REGIONS})
    _pairs(out, existing, rng, w4.MINERAL_REGIONS, MINERAL_STEMS_W2, mineral_states)

    pass_states = list({s for _, s in all_passes})
    _pairs(out, existing, rng, all_passes, PASS_STEMS_W2, pass_states)

    power_states = list({s for _, s in w4.POWER_STATIONS})
    for station, state in w4.POWER_STATIONS:
        st = _norm_state(state)
        for tmpl in POWER_STEMS_W2:
            _add(out, existing, rng, tmpl.format(a=station), st, _pool(power_states, st)[:3], "medium", power_states)

    zones = list({z for z, _ in w4.RAILWAY_ZONES})
    hqs = list({h for _, h in w4.RAILWAY_ZONES})
    for zone, hq in w4.RAILWAY_ZONES:
        _add(out, existing, rng, f"'{zone}' റെയിൽവേ സോണിന്റെ ആസ്ഥാനം '{hq}' — '{hq}' ഏത് സോണിന്റെ?", zone, _pool(zones, zone)[:3], "medium", zones)
        _add(out, existing, rng, f"'{hq}' നഗരം ഏത് റെയിൽവേ സോണിന്റെ ആസ്ഥാനമാണ്?", zone, _pool(zones, zone)[:3], "medium", zones)

    climate_states = list({s for _, s in w4.CLIMATE_PLACES})
    _pairs(out, existing, rng, w4.CLIMATE_PLACES, CLIMATE_STEMS_W2, climate_states)

    soil_names = list({s for s, _ in SOIL_REGIONS})
    for soil, region in SOIL_REGIONS:
        _add(
            out,
            existing,
            rng,
            SOIL_STEMS_W2[0].format(a=soil, b=region),
            soil,
            _pool(soil_names, soil)[:3],
            "medium",
            soil_names,
        )

    bio_states = list({s for _, s in w4.BIOSPHERE_RESERVES})
    _pairs(out, existing, rng, w4.BIOSPHERE_RESERVES, BIOS_STEMS_W2, bio_states)

    lake_states = list({s for _, s in w4.INDIAN_LAKES})
    _pairs(out, existing, rng, w4.INDIAN_LAKES, LAKE_STEMS_W2, lake_states)

    sanct_states = list({s for _, s in w4.WILDLIFE_SANCTUARIES})
    _pairs(out, existing, rng, w4.WILDLIFE_SANCTUARIES, SANCT_STEMS_W2, sanct_states)

    port_states = list({_norm_state(s) for _, s in INDIA_PORTS})
    _pairs(out, existing, rng, [(p, s) for p, s in INDIA_PORTS], PORT_STEMS_W2, port_states)

    strait_names = [s for s, _ in w4.STRAITS]
    strait_conn = list({c for _, c in w4.STRAITS})
    for name, conn in w4.STRAITS:
        _add(out, existing, rng, STRAIT_STEMS_W2[0].format(a=name, b=conn), name, _pool(strait_names, name)[:3], "medium", strait_names)
        _add(out, existing, rng, STRAIT_STEMS_W2[1].format(a=name, b=conn), conn, _pool(strait_conn, conn)[:3], "hard", strait_conn)

    plat_regs = list({r for _, r in w4.INDIAN_PLATEAUS})
    plats = list({p for p, _ in w4.INDIAN_PLATEAUS})
    _pairs(
        out,
        existing,
        rng,
        w4.INDIAN_PLATEAUS,
        [
            "'{a}' ഭൂമിശാസ്ത്രപരമായി ഏത് ഭാഗത്ത്?",
            "'{a}' പീഠഭൂമി/പ്രദേശം ഏത് ഭാഗത്താണ്?",
        ],
        plat_regs,
    )
    _pairs(out, existing, rng, w4.INDIAN_PLATEAUS, ["'{b}' ഭാഗത്തുള്ള പീഠഭൂമി/പ്രദേശം?"], plats)

    rock_types = list({t for _, t in ROCK_TYPES})
    _pairs(out, existing, rng, ROCK_TYPES, ["'{a}' ഏത് ശിലാ വിഭാഗത്തിൽ പെടുന്നു?", "'{a}' — '{b}' ശില?"], rock_types)

    for q, a, w, d in WORLD_FACTS:
        if any(k in q for k in ("അന്തരീക്ഷ", "മൺസൂൺ", "കാലാവസ്ഥ", "മഴ", "കാറ്റ")):
            alt = q[:-1] + " — ഭൂമിശാസ്ത്രം?" if q.endswith("?") else q + "?"
            if alt not in existing:
                _add(out, existing, rng, alt, a, w, d, w + [a])

    _add(out, existing, rng, "ടോപ്പോഗ്രാഫിക് മാപ്പിൽ നീല നിറം സൂചിപ്പിക്കുന്നത്?", "ജലാശയങ്ങൾ", ["കെട്ടിടങ്ങൾ", "വനം", "പാത"], "medium", ["ജലാശയങ്ങൾ", "കെട്ടിടങ്ങൾ", "വനം", "പാത"])
    _add(out, existing, rng, "ടോപ്പോഗ്രാഫിക് മാപ്പിൽ പച്ച നിറം സൂചിപ്പിക്കുന്നത്?", "വനം/പച്ചപ്പ്", ["ജലം", "പാത", "മണൽ"], "medium", ["വനം/പച്ചപ്പ്", "ജലം", "പാത", "മണൽ"])
    _add(out, existing, rng, "ഭൂമിശാസ്ത്ര മാപ്പിൽ തവിട്ട് നിറം സൂചിപ്പിക്കുന്നത്?", "നഗര/മണ്ണ്", ["ജലം", "വനം", "മഞ്ഞ്"], "medium", ["നഗര/മണ്ണ്", "ജലം", "വനം", "മഞ്ഞ്"])
    _add(out, existing, rng, "അക്ഷാംശ രേഖകൾ മാപ്പിൽ കിഴക്ക്-പടിഞ്ഞാറ് സൂചിപ്പിക്കുന്നത്?", "ദേശാന്തര", ["സമാന്തര", "ധ്രുവ", "മധ്യ"], "hard", ["ദേശാന്തര", "സമാന്തര", "ധ്രുവ", "മധ്യ"])

    return out

