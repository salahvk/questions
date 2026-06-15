#!/usr/bin/env python3
"""Build arts_wave20_facts.py — 20 Malayalam PSC art/culture categories, 2300+ stems."""

from __future__ import annotations

import importlib.util
import pprint
import random
import textwrap
from pathlib import Path

OUT = Path(__file__).parent / "arts_wave20_facts.py"
MIN_COUNT = 2300

HEADER = textwrap.dedent("""
    #!/usr/bin/env python3
    \"\"\"Wave 20 arts & culture facts — 20 Malayalam PSC topic categories.\"\"\"

    from __future__ import annotations

    import random

    from refill_common import Candidate, add_candidate, interleave_candidates

    Fact = tuple[str, str, list[str], str]


    def _pool(items: list[str], correct: str) -> list[str]:
        return [x for x in items if x != correct]


    def _emit(
        out: list[Candidate],
        existing: set[str],
        rng: random.Random,
        prefix: str,
        facts: list[Fact],
        *,
        function_entity: str | None = None,
    ) -> None:
        terms = list(dict.fromkeys(t for t, _, _, _ in facts))
        answers = list(dict.fromkeys(a for _, a, _, _ in facts))
        for term, ans, wrong, diff in facts:
            add_candidate(
                out, existing, rng,
                f"{prefix} '{term}'?",
                ans, wrong, diff, pool=answers,
            )
            if function_entity:
                add_candidate(
                    out, existing, rng,
                    f"'{ans}' ഏത് {function_entity}-ന്റെ പ്രവർത്തനമാണ്?",
                    term, _pool(terms, term)[:6], diff, pool=terms,
                )


    def _emit_pairs(
        out: list[Candidate],
        existing: set[str],
        rng: random.Random,
        prefix: str,
        rows: list[tuple[str, str]],
        templates_ab: list[str],
        templates_ba: list[str] | None = None,
        diff: str = "medium",
    ) -> None:
        bs = list(dict.fromkeys(b for _, b in rows))
        as_ = list(dict.fromkeys(a for a, _ in rows))
        for a, b in rows:
            for tmpl in templates_ab:
                add_candidate(
                    out, existing, rng,
                    prefix + tmpl.format(a=a, b=b),
                    b, _pool(bs, b)[:3], diff, pool=bs,
                )
            if templates_ba:
                for tmpl in templates_ba:
                    add_candidate(
                        out, existing, rng,
                        prefix + tmpl.format(a=a, b=b),
                        a, _pool(as_, a)[:3], diff, pool=as_,
                    )


    def _emit_person_event(
        out: list[Candidate],
        existing: set[str],
        rng: random.Random,
        rows: list[tuple[str, str, str]],
        who_templates: list[str],
        event_templates: list[str],
        detail_templates: list[str] | None,
        pool_persons: list[str],
        pool_events: list[str],
        pool_details: list[str],
        diff: str = "medium",
    ) -> None:
        for person, event, detail in rows:
            for tmpl in who_templates:
                add_candidate(
                    out, existing, rng,
                    tmpl.format(a=person, b=event, c=detail),
                    person, _pool(pool_persons, person)[:3], diff, pool=pool_persons,
                )
            for tmpl in event_templates:
                add_candidate(
                    out, existing, rng,
                    tmpl.format(a=person, b=event, c=detail),
                    event, _pool(pool_events, event)[:3], diff, pool=pool_events,
                )
            if detail_templates:
                for tmpl in detail_templates:
                    add_candidate(
                        out, existing, rng,
                        tmpl.format(a=person, b=event, c=detail),
                        detail, _pool(pool_details, detail)[:3], diff, pool=pool_details,
                    )

""")

FOOTER = textwrap.dedent("""

    def generate_wave20_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
        out: list[Candidate] = []
        _emit_all_categories(out, existing, rng)
        return interleave_candidates(out, rng)


    if __name__ == "__main__":
        print(len(generate_wave20_candidates(set(), random.Random(42))))
""")

PAIR_AB = [
    "'{a}' ഏത് സംസ്ഥാന/പ്രദേശവുമായി ബന്ധപ്പെട്ട പാരമ്പര്യ കലാരൂപമാണ്?",
    "'{a}' ഏത് പ്രദേശത്തിന്റെ പാരമ്പര്യ കല/തൊഴിലുമായി ബന്ധപ്പെട്ടതാണ്?",
    "PSC കലാ-സംസ്കൃതി വിജ്ഞാനത്തിൽ '{a}'?",
    "'{a}' ഏത് പ്രദേശത്തിന്റെ പ്രതിനിധി കലാരൂപമാണ്?",
    "'{a}' ഏത് സംസ്ഥാനത്തിന്റെ പാരമ്പര്യ കലയുമായി ബന്ധപ്പെട്ടതാണ്?",
    "ഇന്ത്യൻ കലാ-സംസ്കൃതിയിൽ '{a}'?",
]
PAIR_BA = [
    "{b} സംസ്ഥാന/പ്രദേശത്തിന്റെ പ്രധാന പാരമ്പര്യ കല '{a}'?",
    "{b} പ്രതിനിധാനം ചെയ്യുന്ന കലാരൂപം ഏത്?",
    "{b} പ്രദേശവുമായി ബന്ധപ്പെട്ട കല '{a}'?",
]
PAIR_AB_SITE = [
    "'{a}' ഏത് സംസ്ഥാന/പ്രദേശത്തിലാണ് സ്ഥിതി ചെയ്യുന്നത്?",
    "'{a}' ഏത് പ്രദേശത്തിന്റെ പ്രധാന കലാസ്മാരകമാണ്?",
    "PSC കലാ-സംസ്കൃതിയിൽ '{a}'?",
    "'{a}' ഏത് സംസ്ഥാനവുമായി ബന്ധപ്പെട്ട കലാസ്ഥലമാണ്?",
]
PAIR_BA_SITE = [
    "{b} സംസ്ഥാന/പ്രദേശത്തിലെ പ്രധാന കലാസ്ഥല '{a}'?",
    "{b} പ്രദേശത്തിന്റെ പ്രശസ്ത കലാസ്മാരകം?",
]
PAIR_AB_SCHOOL = [
    "'{a}' ഏത് ചിത്രകലാ ശൈലി/പരമ്പരയുമായി ബന്ധപ്പെട്ടതാണ്?",
    "'{a}' ഏത് ചിത്രകലാ പരമ്പരയുടെ പ്രതിനിധിത്വം?",
    "PSC ചിത്രകലയിൽ '{a}'?",
]
PAIR_BA_SCHOOL = [
    "{b} ചിത്രകലാ ശൈലി/പരമ്പരയുടെ പ്രധാന ഉദാഹരണം?",
    "{b} ശൈലിയുമായി ബന്ധപ്പെട്ട കലാരൂപം?",
]
PAIR_AB_COMMUNITY = [
    "'{a}' ഏത് സമുദായവുമായി ബന്ധപ്പെട്ട കലാരൂപമാണ്?",
    "'{a}' ഏത് സമുദായത്തിന്റെ പാരമ്പര്യ കലയുമായി ബന്ധപ്പെട്ടതാണ്?",
    "കേരളത്തിലെ സമുദായ കലയിൽ '{a}'?",
    "'{a}' ഏത് സമുദായത്തിന്റെ പ്രതിനിധി കലാരൂപമാണ്?",
    "'{a}' ഏത് സമുദായവുമായി ബന്ധപ്പെട്ട പാരമ്പര്യ കലയാണ്?",
]
PAIR_BA_COMMUNITY = [
    "{b} സമുദായത്തിന്റെ പ്രധാന കലാരൂപം '{a}'?",
    "{b} സമുദായവുമായി ബന്ധപ്പെട്ട കല '{a}'?",
    "{b} സമുദായത്തിന്റെ പാരമ്പര്യ കലാരൂപം?",
]
PAIR_AB_DYNASTY = [
    "'{a}' ഏത് കാലഘട്ടം/രാജവംശവുമായി ബന്ധപ്പെട്ടതാണ്?",
    "'{a}' ഏത് പുരാതന കാലഘട്ടവുമായി ബന്ധപ്പെട്ട കലാവസ്തുവാണ്?",
    "പുരാതന ഇന്ത്യൻ കലയിൽ '{a}'?",
    "'{a}' ഏത് സംസ്കാരകാലവുമായി ബന്ധപ്പെട്ടതാണ്?",
    "'{a}' ഏത് രാജവംശ കാലഘട്ടവുമായി ബന്ധപ്പെട്ടതാണ്?",
]
PAIR_BA_DYNASTY = [
    "{b} കാലഘട്ടത്തിലെ പ്രധാന കലാവസ്തു '{a}'?",
    "{b} സമ്പർക്കത്തിൽ പ്രധാന കലാവസ്തു '{a}'?",
    "{b} കാലഘട്ടവുമായി ബന്ധപ്പെട്ട കല '{a}'?",
]

EMIT_BODY = r'''
def _emit_shadow_puppetry(out, existing, rng):
    _emit_pairs(out, existing, rng, "തോൽക്കൂത്ത്/നിശാകൂത്ത് കലയിൽ ", SHADOW_PUPPETRY, PAIR_AB, PAIR_BA)

def _emit_martial_arts(out, existing, rng):
    _emit_pairs(out, existing, rng, "ഇന്ത്യൻ പാരമ്പര്യ പോരാട്ട കലയിൽ ", MARTIAL_ARTS, PAIR_AB, PAIR_BA)

def _emit_kerala_communal(out, existing, rng):
    _emit_pairs(out, existing, rng, "കേരളത്തിലെ സമുദായ കലാരൂപങ്ങളിൽ ", KERALA_COMMUNAL, PAIR_AB_COMMUNITY, PAIR_BA_COMMUNITY)
    _emit(out, existing, rng, "കേരളത്തിലെ സമുദായ കലയിൽ", KERALA_COMMUNAL_FACTS)

def _emit_floor_drawing(out, existing, rng):
    _emit_pairs(out, existing, rng, "നില/ശരീര ചിത്രകലയിൽ ", FLOOR_DRAWING, PAIR_AB, PAIR_BA)

def _emit_metal_crafts(out, existing, rng):
    _emit_pairs(out, existing, rng, "ലോഹ/വെങ്കല ഹസ്തകലയിൽ ", METAL_CRAFTS, PAIR_AB, PAIR_BA)

def _emit_textile(out, existing, rng):
    _emit_pairs(out, existing, rng, "നെയ്ത്ത/വസ്ത്ര കലയിൽ ", TEXTILE_WEAVING, PAIR_AB, PAIR_BA)

def _emit_pottery(out, existing, rng):
    _emit_pairs(out, existing, rng, "കളിമൺ/മൺവണ്ണ കലയിൽ ", POTTERY, PAIR_AB, PAIR_BA)

def _emit_wood_crafts(out, existing, rng):
    _emit_pairs(out, existing, rng, "മര/ആനക്കൊമ്പ്/കളിപ്പാട ഹസ്തകലയിൽ ", WOOD_CRAFTS, PAIR_AB, PAIR_BA)

def _emit_miniature_schools(out, existing, rng):
    _emit_pairs(out, existing, rng, "മിനിയേച്ചർ ചിത്രകലാ പരമ്പരയിൽ ", MINIATURE_SCHOOLS, PAIR_AB_SCHOOL, PAIR_BA_SCHOOL)
    _emit(out, existing, rng, "മിനിയേച്ചർ ചിത്രകലയിൽ", MINIATURE_FACTS)

def _emit_folk_painting(out, existing, rng):
    _emit_pairs(out, existing, rng, "ജനപദ/scroll ചിത്രകലയിൽ ", FOLK_PAINTING, PAIR_AB, PAIR_BA)

def _emit_rock_cave(out, existing, rng):
    _emit_pairs(out, existing, rng, "ഗുഹാചിത്ര/ശിലാചിത്ര കലയിൽ ", ROCK_CAVE, PAIR_AB_SITE, PAIR_BA_SITE)

def _emit_indus_mauryan(out, existing, rng):
    _emit(out, existing, rng, "സിന്ധു-മൗര്യ കലയിൽ", INDUS_MAURYAN_FACTS)
    _emit_pairs(out, existing, rng, "പുരാതന ഇന്ത്യൻ കലയിൽ ", INDUS_MAURYAN_PAIRS, PAIR_AB_DYNASTY, PAIR_BA_DYNASTY)

def _emit_buddhist_jain(out, existing, rng):
    _emit(out, existing, rng, "ബൗദ്ധ-ജൈന കലയിൽ", BUDDHIST_JAIN_FACTS)
    _emit_pairs(out, existing, rng, "ബൗദ്ധ-ജൈന കലാപരമ്പരയിൽ ", BUDDHIST_JAIN_PAIRS, PAIR_AB, PAIR_BA)

def _emit_temple_terms(out, existing, rng):
    _emit(out, existing, rng, "ക്ഷേത്ര വാസ്തു/ശില്പശാസ്ത്രത്തിൽ", TEMPLE_TERMS, function_entity="ക്ഷേത്ര ഭാഗം")
    _emit_pairs(out, existing, rng, "ക്ഷേത്ര ശില്പത്തിൽ ", TEMPLE_MUDRA_PAIRS,
        ["'{a}' ഏത് മുദ്ര/സങ്കേതമാണ്?", "'{a}' ഏത് ശില്പ സങ്കേതവുമായി ബന്ധപ്പെട്ടതാണ്?"],
        ["{b} മുദ്ര/സങ്കേതത്തിന്റെ പേര് '{a}'?"])

def _emit_numismatics(out, existing, rng):
    _emit(out, existing, rng, "ഇന്ത്യൻ നാണയശാസ്ത്രത്തിൽ", NUMISMATICS_FACTS)
    _emit_pairs(out, existing, rng, "പുരാതന ഇന്ത്യൻ നാണയങ്ങളിൽ ", NUMISMATICS_PAIRS, PAIR_AB_DYNASTY, PAIR_BA_DYNASTY)

def _emit_manuscript(out, existing, rng):
    _emit(out, existing, rng, "യന്ത്രലിപി/കൈയെഴുത്ത് കലയിൽ", MANUSCRIPT_FACTS)
    _emit_pairs(out, existing, rng, "യന്ത്രലിപി/കൈയെഴുത്ത് പരമ്പരയിൽ ", MANUSCRIPT_PAIRS, PAIR_AB, PAIR_BA)

def _emit_photography(out, existing, rng):
    pp = list(dict.fromkeys(a for a, _, _ in PHOTOGRAPHY))
    pe = list(dict.fromkeys(b for _, b, _ in PHOTOGRAPHY))
    pd = list(dict.fromkeys(c for _, _, c in PHOTOGRAPHY))
    _emit_person_event(out, existing, rng, PHOTOGRAPHY,
        ["{b} സംബന്ധിച്ച പ്രധാന ഇന്ത്യൻ ഫോട്ടോഗ്രാഫർ ആരാണ്?", "{b} — പ്രധാന ഇന്ത്യൻ ഫോട്ടോഗ്രാഫർ?"],
        ["{a} ഏതുമായി ബന്ധപ്പെട്ട പ്രധാന ഫോട്ടോഗ്രാഫി നേട്ടം?", "{a} ഏത് മേഖല/സ്ഥാപനവുമായി ബന്ധപ്പെട്ട ഫോട്ടോഗ്രാഫർ?"],
        ["{b} സംബന്ധിച്ച പ്രധാന വിവരം/സ്ഥാപനം?"],
        pp, pe, pd)
    _emit(out, existing, rng, "ഇന്ത്യൻ ഫോട്ടോഗ്രാഫിയിൽ", PHOTOGRAPHY_FACTS)

def _emit_modern_art(out, existing, rng):
    ap = list(dict.fromkeys(a for a, _, _ in MODERN_ARTISTS))
    ae = list(dict.fromkeys(b for _, b, _ in MODERN_ARTISTS))
    ad = list(dict.fromkeys(c for _, _, c in MODERN_ARTISTS))
    _emit_person_event(out, existing, rng, MODERN_ARTISTS,
        ["{b} സംബന്ധിച്ച പ്രധാന ഇന്ത്യൻ ചിത്രകാരൻ/കലാകാരി ആരാണ്?", "{b} — പ്രധാന ആധുനിക ഇന്ത്യൻ കലാകാരി?"],
        ["{a} ഏത് കലാ പ്രസ്ഥാന/ശൈലിയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?", "{a} ഏത് കലാ പരമ്പരയുമായി ബന്ധപ്പെട്ട കലാകാരി?"],
        ["{b} സംബന്ധിച്ച പ്രധാന കലാ പ്രസ്ഥാനം/ശൈലി?"],
        ap, ae, ad)
    _emit_pairs(out, existing, rng, "ആധുനിക ഇന്ത്യൻ ചിത്രകലയിൽ ", MODERN_MOVEMENTS, PAIR_AB, PAIR_BA)
    _emit(out, existing, rng, "ആധുനിക ഇന്ത്യൻ ചിത്രകലയിൽ", MODERN_ART_FACTS)

def _emit_gi_crafts(out, existing, rng):
    _emit_pairs(out, existing, rng, "GI ടാഗ് ഹസ്തകലയിൽ ", GI_CRAFTS, PAIR_AB, PAIR_BA)

def _emit_folk_music(out, existing, rng):
    _emit_pairs(out, existing, rng, "പ്രാദേശിക ജനപദ സംഗീതത്തിൽ ", FOLK_MUSIC, PAIR_AB, PAIR_BA)
    _emit(out, existing, rng, "ജനപദ സംഗീതത്തിൽ", FOLK_MUSIC_FACTS)

def _emit_all_categories(out, existing, rng):
    _emit_shadow_puppetry(out, existing, rng)
    _emit_martial_arts(out, existing, rng)
    _emit_kerala_communal(out, existing, rng)
    _emit_floor_drawing(out, existing, rng)
    _emit_metal_crafts(out, existing, rng)
    _emit_textile(out, existing, rng)
    _emit_pottery(out, existing, rng)
    _emit_wood_crafts(out, existing, rng)
    _emit_miniature_schools(out, existing, rng)
    _emit_folk_painting(out, existing, rng)
    _emit_rock_cave(out, existing, rng)
    _emit_indus_mauryan(out, existing, rng)
    _emit_buddhist_jain(out, existing, rng)
    _emit_temple_terms(out, existing, rng)
    _emit_numismatics(out, existing, rng)
    _emit_manuscript(out, existing, rng)
    _emit_photography(out, existing, rng)
    _emit_modern_art(out, existing, rng)
    _emit_gi_crafts(out, existing, rng)
    _emit_folk_music(out, existing, rng)
'''


from arts_wave20_data import build_all_data


def main() -> None:
    data = build_all_data()
    parts = [HEADER]
    for name in sorted(data):
        parts.append(f"{name} = {pprint.pformat(data[name], width=120)}\n")
    for const in (
        "PAIR_AB", "PAIR_BA", "PAIR_AB_SITE", "PAIR_BA_SITE",
        "PAIR_AB_SCHOOL", "PAIR_BA_SCHOOL", "PAIR_AB_COMMUNITY", "PAIR_BA_COMMUNITY",
        "PAIR_AB_DYNASTY", "PAIR_BA_DYNASTY",
    ):
        parts.append(f"{const} = {pprint.pformat(globals()[const], width=120)}\n")
    parts.append(EMIT_BODY)
    parts.append(FOOTER)
    source = "\n".join(parts)

    test_path = OUT.parent / "_aw20_count_test.py"
    test_path.write_text(source, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("aw20t", test_path)
    if spec is None or spec.loader is None:
        raise SystemExit("Failed to load test module")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    count = len(mod.generate_wave20_candidates(set(), random.Random(42)))
    test_path.unlink()

    if count < MIN_COUNT:
        raise SystemExit(f"FAIL: only {count} candidates (need {MIN_COUNT}+)")

    OUT.write_text(source, encoding="utf-8")
    print(f"Wrote {OUT} — {count} candidates verified")


if __name__ == "__main__":
    main()
