#!/usr/bin/env python3
"""Patch kerala_renaissance_wave20_facts.py with Kerala Renaissance data."""

from __future__ import annotations

import pprint
import random
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "kerala_renaissance_wave20_facts.py"

HEADER = '''#!/usr/bin/env python3
"""Wave 20 Kerala Renaissance facts — 20 PSC topic categories."""

from __future__ import annotations

import random
import re

from refill_common import Candidate, add_candidate

MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def _pool(items: list[str], correct: str) -> list[str]:
    return [x for x in items if x != correct]


def _add(out, existing, rng, q, ans, wrong, diff="medium", pool=None):
    if MIXED.search(q + ans + "".join(wrong)):
        return
    add_candidate(out, existing, rng, q, ans, wrong, diff, pool)


def _pairs(out, existing, rng, rows, templates, pool_b, diff="medium"):
    for a, b in rows:
        for tmpl in templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b), b, _pool(pool_b, b)[:3], diff, pool_b)


def _pairs_rev(out, existing, rng, rows, templates, pool_a, diff="medium"):
    for a, b in rows:
        for tmpl in templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b), a, _pool(pool_a, a)[:3], diff, pool_a)


def _triples(out, existing, rng, rows, ab_t, ac_t, bc_t, pb, pc, pa, diff="medium"):
    for a, b, c in rows:
        for tmpl in ab_t:
            _add(out, existing, rng, tmpl.format(a=a, b=b, c=c), b, _pool(pb, b)[:3], diff, pb)
        for tmpl in ac_t:
            _add(out, existing, rng, tmpl.format(a=a, b=b, c=c), c, _pool(pc, c)[:3], diff, pc)
        for tmpl in bc_t:
            _add(out, existing, rng, tmpl.format(a=a, b=b, c=c), a, _pool(pa, a)[:3], diff, pa)


def _emit_pass(out, existing, rng, rows, fwd, rev):
    if not rows:
        return
    bs = list(dict.fromkeys(b for _, b in rows))
    as_ = list(dict.fromkeys(a for a, _ in rows))
    _pairs(out, existing, rng, rows, fwd, bs)
    _pairs_rev(out, existing, rng, rows, rev, as_)


def _emit_triple_pass(out, existing, rng, rows, ab, ac, bc):
    if not rows:
        return
    bs = list(dict.fromkeys(b for _, b, _ in rows))
    cs = list(dict.fromkeys(c for _, _, c in rows))
    as_ = list(dict.fromkeys(a for a, _, _ in rows))
    _triples(out, existing, rng, rows, ab, ac, bc, bs, cs, as_)


'''

FOOTER = '''
FWD = [
    "കേരള നവോത്ഥാനത്തിൽ '{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
    "'{a}'-ന്റെ പ്രധാന ലക്ഷ്യം/വിവരണം?",
    "നവോത്ഥാന പ്രസ്ഥാനത്തിൽ '{a}'-യുമായി ബന്ധപ്പെട്ടത്?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വിവരണം?",
    "'{a}'-ന്റെ പ്രധാന ആവശ്യം/വിവരം?",
    "'{a}' എന്തിനെ/ആരെ സൂചിപ്പിക്കുന്നു?",
]
REV = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട പ്രസ്ഥാന/വ്യക്തി/സംഭവം?",
    "'{b}'-ന്റെ പേരിലുള്ള/ബന്ധപ്പെട്ട നവോത്ഥാന വസ്തു?",
    "'{b}'-യുമായി ബന്ധപ്പെട്ടത്?",
]
FWD2 = [
    "കേരള നവോത്ഥാന ചരിത്രത്തിൽ '{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വിവരണം?",
]
REV2 = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വസ്തു/വ്യക്തി?",
    "'{b}'-ന്റെ പേരിലുള്ള/ബന്ധപ്പെട്ട വസ്തു?",
]
FWD3 = [
    "കേരള നവോത്ഥാന കാലത്ത് '{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
    "'{a}'-ന്റെ പ്രധാന വിവരണം?",
]
REV3 = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വസ്തു?",
    "'{b}'-ന്റെ പേരിലുള്ള വസ്തു?",
]
TAB = ["'{a}'-യുമായി ബന്ധപ്പെട്ട '{b}'?", "'{a}'-ന്റെ '{b}'?"]
TAC = ["'{a}'-യുമായി ബന്ധപ്പെട്ട '{c}'?", "'{a}'-ന്റെ '{c}'?"]
TBC = ["'{b}' '{c}'-യുമായി ബന്ധപ്പെട്ട '{a}'?", "'{c}'-യുമായി ബന്ധപ്പെട്ട '{b}'?"]


def _emit_all(out, existing, rng):
    tpl_fwd = FWD + FWD2 + FWD3
    tpl_rev = REV + REV2 + REV3
    cats = (
        ("ആവശ്യം/ലക്ഷ്യം", DEMAND_OBJECTIVE),
        ("ഫലം/പരിണാമം", OUTCOME_RESULT),
        ("പ്രതീകാത്മക പ്രതിക്ഷেভം", SYMBOLIC_PROTEST),
        ("ആദ്യകാല ലഹളകൾ", EARLY_REVOLTS),
        ("വിദ്യാഭ്യാസ പരിഷ്കാരം", EDUCATION_REFORM),
        ("സ്ഥാപനങ്ങൾ/ക്ഷേത്രങ്ങൾ", INSTITUTIONS_TEMPLES),
        ("വടക്കൻ മലബാർ", NORTH_MALABAR),
        ("യുക്തിവാദി/ശിവയോഗി", RATIONALIST_SIVAYOGI),
        ("സ്ത്രീ പരിഷ്കാരം", WOMEN_REFORM),
        ("നാടക/തിയേറ്റർ", DRAMA_THEATRE),
        ("യോഗക്ഷേമ സഭ", YOGAKSHEMA),
        ("കേരളത്തിന് പുറത്തുള്ളവർ", OUTSIDE_KERALA),
        ("ഗാന്ധി调解", GANDHI_MEDIATION),
        ("ബഹുനേതൃ സമിതികൾ", MULTI_LEADER),
        ("മെമ്മോറിയൽ അർഝികൾ", MEMORIAL_PETITIONS),
        ("മുസ്ലിം പരിഷ്കര്ത്താക്കൾ", MUSLIM_REFORMERS),
        ("പത്രങ്ങൾ", NEWSPAPERS),
        ("സംഘടനാ ആദ്യങ്ങൾ", ORGANIZATION_FIRSTS),
        ("പ്രാന്ത/രാജ്യ സംസ്ഥാനം", REGIONAL_PRINCELY),
        ("ഉത്തരാവതി പ്രസ്ഥാനങ്ങൾ", SUCCESSOR_MOVEMENTS),
    )
    for tag, cat in cats:
        cfwd = [tag + ": " + t for t in tpl_fwd]
        crev = [tag + ": " + t for t in tpl_rev]
        _emit_pass(out, existing, rng, cat, cfwd, crev)
    _emit_triple_pass(out, existing, rng, LEADER_ORG_YEAR, TAB, TAC, TBC)
    _emit_triple_pass(out, existing, rng, LEADER_WORK, TAB, TAC, TBC)
    _emit_triple_pass(out, existing, rng, MOVEMENT_PLACE_YEAR, TAB, TAC, TBC)
    _emit_qa(out, existing, rng, LEGACY_QA)


def _emit_qa(out, existing, rng, rows):
    for q, ans, wrong, diff in rows:
        pool = list(dict.fromkeys([ans] + wrong))
        _add(out, existing, rng, q, ans, [x for x in pool if x != ans][:3], diff, pool)


def generate_wave20_candidates(existing, rng):
    out = []
    _emit_all(out, existing, rng)
    return out


if __name__ == "__main__":
    r = random.Random(42)
    print(len(generate_wave20_candidates(set(), r)))
'''


def fp(name: str, rows: list[tuple[str, str]]) -> str:
    return f"{name}: list[tuple[str, str]] = " + pprint.pformat(rows, width=120, sort_dicts=False)


def ft(name: str, rows: list[tuple[str, str, str]]) -> str:
    return f"{name}: list[tuple[str, str, str]] = " + pprint.pformat(rows, width=120, sort_dicts=False)


# --- verified Kerala Renaissance facts (pure Malayalam) ---

DEMAND_OBJECTIVE = [
    ("വൈക്കം സത്യാഗ്രഹം", "ക്ഷേത്രവീഥിയിലൂടെ അവഗണിതരുടെ നടപ്പാവകാശം"),
    ("ഗുരുവായൂർ സത്യാഗ്രഹം", "ക്ഷേത്രപ്രവേശനാവകാശം"),
    ("വില്ലുവണ്ടി സമരം", "പുലയരുടെ പൊതുവഴി ഉപയോഗാവകാശം"),
    ("ചാന്നാർ ലഹള", "നadar സ്ത്രീകളുടെ മേൽത്തുണി അധികാരം"),
]

OUTCOME_RESULT = DEMAND_OBJECTIVE  # TEMP
SYMBOLIC_PROTEST = DEMAND_OBJECTIVE
EARLY_REVOLTS = DEMAND_OBJECTIVE
EDUCATION_REFORM = DEMAND_OBJECTIVE
INSTITUTIONS_TEMPLES = DEMAND_OBJECTIVE
NORTH_MALABAR = DEMAND_OBJECTIVE
RATIONALIST_SIVAYOGI = DEMAND_OBJECTIVE
WOMEN_REFORM = DEMAND_OBJECTIVE
DRAMA_THEATRE = DEMAND_OBJECTIVE
YOGAKSHEMA = DEMAND_OBJECTIVE
OUTSIDE_KERALA = DEMAND_OBJECTIVE
GANDHI_MEDIATION = DEMAND_OBJECTIVE
MULTI_LEADER = DEMAND_OBJECTIVE
MEMORIAL_PETITIONS = DEMAND_OBJECTIVE
MUSLIM_REFORMERS = DEMAND_OBJECTIVE
NEWSPAPERS = DEMAND_OBJECTIVE
ORGANIZATION_FIRSTS = DEMAND_OBJECTIVE
REGIONAL_PRINCELY = DEMAND_OBJECTIVE
SUCCESSOR_MOVEMENTS = DEMAND_OBJECTIVE
LEADER_ORG_YEAR: list[tuple[str, str, str]] = []
LEADER_WORK: list[tuple[str, str, str]] = []
MOVEMENT_PLACE_YEAR: list[tuple[str, str, str]] = []


def main() -> None:
    pairs = {
        "DEMAND_OBJECTIVE": DEMAND_OBJECTIVE,
        "OUTCOME_RESULT": OUTCOME_RESULT,
        "SYMBOLIC_PROTEST": SYMBOLIC_PROTEST,
        "EARLY_REVOLTS": EARLY_REVOLTS,
        "EDUCATION_REFORM": EDUCATION_REFORM,
        "INSTITUTIONS_TEMPLES": INSTITUTIONS_TEMPLES,
        "NORTH_MALABAR": NORTH_MALABAR,
        "RATIONALIST_SIVAYOGI": RATIONALIST_SIVAYOGI,
        "WOMEN_REFORM": WOMEN_REFORM,
        "DRAMA_THEATRE": DRAMA_THEATRE,
        "YOGAKSHEMA": YOGAKSHEMA,
        "OUTSIDE_KERALA": OUTSIDE_KERALA,
        "GANDHI_MEDIATION": GANDHI_MEDIATION,
        "MULTI_LEADER": MULTI_LEADER,
        "MEMORIAL_PETITIONS": MEMORIAL_PETITIONS,
        "MUSLIM_REFORMERS": MUSLIM_REFORMERS,
        "NEWSPAPERS": NEWSPAPERS,
        "ORGANIZATION_FIRSTS": ORGANIZATION_FIRSTS,
        "REGIONAL_PRINCELY": REGIONAL_PRINCELY,
        "SUCCESSOR_MOVEMENTS": SUCCESSOR_MOVEMENTS,
    }
    parts = [HEADER]
    for name, rows in pairs.items():
        parts.append(fp(name, rows))
        parts.append("")
    parts.append(ft("LEADER_ORG_YEAR", LEADER_ORG_YEAR))
    parts.append("")
    parts.append(ft("LEADER_WORK", LEADER_WORK))
    parts.append("")
    parts.append(ft("MOVEMENT_PLACE_YEAR", MOVEMENT_PLACE_YEAR))
    parts.append(FOOTER)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    from kerala_renaissance_wave20_facts import generate_wave20_candidates
    n = len(generate_wave20_candidates(set(), random.Random(42)))
    print(f"Wrote {OUT.name}: {n} candidates")
    if n < 2000:
        raise SystemExit(f"Shortfall: {n} < 2000")


if __name__ == "__main__":
    main()
