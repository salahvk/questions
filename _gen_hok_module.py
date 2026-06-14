#!/usr/bin/env python3
"""Generate build_hok_wave20_module.py with full Kerala history wave20 data."""
from __future__ import annotations

import pprint
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "build_hok_wave20_module.py"
MIN_COUNT = 2400

HEADER = textwrap.dedent(
    '''\
    #!/usr/bin/env python3
    """Wave 20 Kerala history facts — 20 PSC topic types."""

    from __future__ import annotations

    import random
    import re

    from refill_common import Candidate, add_candidate, interleave_candidates

    MIXED = re.compile(r"[\\u0D00-\\u0D7F][a-zA-Z]|[a-zA-Z][\\u0D00-\\u0D7F]")


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

    '''
)

PAIR_FWD = [
    "'{a}'-യുമായി ബന്ധപ്പെട്ട വിവരണം?",
    "'{a}'-ന്റെ പ്രധാന വിവരണം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വസ്തു?",
    "'{a}'-ന്റെ പ്രധാന സവിശേഷത?",
    "'{a}' ഏത് വിവരണവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
]
PAIR_REV = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട വസ്തു/വ്യക്തി?",
    "'{b}'-ന്റെ പേരിലുള്ള/ബന്ധപ്പെട്ട വസ്തു?",
    "'{b}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വസ്തു?",
]
PLACE_FWD = [
    "'{a}' ഏത് ജില്ല/പ്രദേശവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട ജില്ല?",
    "'{a}'-ന്റെ സ്ഥാനം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം?",
    "'{a}' ഏത് ജില്ലയിലാണ്?",
]
PLACE_REV = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട പുരാവസ്തു/സ്ഥലം?",
    "'{b}'-ലെ പ്രധാന പുരാവസ്തു/സ്ഥലം?",
    "'{b}'-യുമായി ബന്ധപ്പെട്ട ചരിത്ര സ്ഥലം?",
]
PERSON_FWD = [
    "'{a}'-യുമായി ബന്ധപ്പെട്ട കേരള ചരിത്ര വിവരണം?",
    "'{a}'-ന്റെ കേരളയാത്ര/രേഖ?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വിവരണം?",
    "'{a}' കേരളത്തെക്കുറിച്ച് എന്ത് രേഖപ്പെടുത്തി?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട ചരിത്ര വിവരണം?",
]
PERSON_REV = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട വിദേശ യാത്രികൻ?",
    "'{b}'-യെക്കുറിച്ച് രേഖപ്പെടുത്തിയ വിദേശി?",
    "'{b}'-യുമായി ബന്ധപ്പെട്ട യാത്രികൻ?",
]
TERM_FWD = [
    "'{a}' എന്ന പദത്തിന്റെ അർത്ഥം?",
    "'{a}'-യുടെ പ്രധാന അർത്ഥം?",
    "'{a}' എന്നാൽ എന്ത്?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട ഭരണപദം?",
    "'{a}'-ന്റെ ചരിത്രപരമായ അർത്ഥം?",
]
TERM_REV = [
    "'{b}'-യെ സൂചിപ്പിക്കുന്ന ഭരണപദം?",
    "'{b}'-യുമായി ബന്ധപ്പെട്ട ചരിത്രപദം?",
    "'{b}'-യുടെ പേരിലുള്ള ഭരണപദം?",
]
YEAR_FWD = [
    "'{a}'-യുമായി ബന്ധപ്പെട്ട വർഷം?",
    "'{a}'-ന്റെ വർഷം?",
    "'{a}' നടന്ന വർഷം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട കാലഘട്ടം?",
    "'{a}' സംഭവിച്ച വർഷം?",
]
YEAR_REV = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട സംഭവം?",
    "'{b}'-ൽ നടന്ന പ്രധാന സംഭവം?",
    "'{b}'-യുമായി ബന്ധപ്പെട്ട ചരിത്ര സംഭവം?",
]
BATTLE_AB = [
    "'{a}' യുദ്ധത്തിന്റെ വിജയി/പ്രധാന വ്യക്തി?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട വിജയി?",
    "'{a}'-ന്റെ പ്രധാന നേതാവ്?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട രാജാവ്/നേതാവ്?",
]
BATTLE_AC = ["'{a}' യുദ്ധം നടന്ന വർഷം?", "'{a}'-യുമായി ബന്ധപ്പെട്ട വർഷം?", "'{a}'-ന്റെ വർഷം?"]
BATTLE_BC = [
    "'{b}' '{c}'-ൽ നടത്തിയ/വിജയിച്ച യുദ്ധം?",
    "'{c}'-ൽ '{b}'-യുമായി ബന്ധപ്പെട്ട യുദ്ധം?",
]
TREATY_AB = [
    "'{a}' ഉടമ്പടിയുടെ പ്രധാന ഫലം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട ഉടമ്പടി ഫലം?",
    "'{a}'-ന്റെ പ്രധാന ഫലം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട ചരിത്ര ഫലം?",
]
TREATY_AC = ["'{a}' ഉടമ്പടി ഒപ്പിട്ട വർഷം?", "'{a}'-യുമായി ബന്ധപ്പെട്ട വർഷം?", "'{a}'-ന്റെ വർഷം?"]
TREATY_BC = [
    "'{b}' '{c}'-ൽ ഒപ്പിട്ട ഉടമ്പടി?",
    "'{c}'-ൽ '{b}'-യുമായി ബന്ധപ്പെട്ട ഉടമ്പടി?",
]
MYSORE_AB = [
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം?",
    "'{a}'-ന്റെ പ്രധാന സ്ഥലം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട കോട്ട/പ്രദേശം?",
    "'{a}'-ന്റെ സ്ഥലം?",
]
MYSORE_AC = ["'{a}'-യുമായി ബന്ധപ്പെട്ട വർഷം?", "'{a}'-ന്റെ വർഷം?", "'{a}' നടന്ന വർഷം?"]
MYSORE_BC = [
    "'{b}' '{c}'-ൽ നടന്ന മൈസൂർ ആക്രമണം?",
    "'{c}'-ൽ '{b}'-യുമായി ബന്ധപ്പെട്ട ആക്രമണം?",
]
FAMINE_AB = [
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം?",
    "'{a}'-ന്റെ പ്രധാന പ്രദേശം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട ജില്ല/പ്രദേശം?",
]
FAMINE_AC = ["'{a}'-yumayi bandhappetta varsham?", "'{a}'-nte varsham?", "'{a}' nadanna varsham?"]
FAMINE_BC = [
    "'{b}' '{c}'-ൽ സംഭവിച്ച ദുരന്തം?",
    "'{c}'-ൽ '{b}'-യുമായി ബന്ധപ്പെട്ട ദുരന്തം?",
]

# fix FAMINE_AC - use Malayalam
FAMINE_AC = ["'{a}'-യുമായി ബന്ധപ്പെട്ട വർഷം?", "'{a}'-ന്റെ വർഷം?", "'{a}' നടന്ന വർഷം?"]

DATA: dict[str, list] = {}

DATA["ARCH_SITE"] = [
    ("എടക്കൽ ഗുഹ", "വയനാട്"), ("എടക്കൽ", "ശിലായുഗ ചിത്രങ്ങൾ"), ("മറയൂർ", "ഇടുക്കി"),
    ("മറയൂർ മുനിയറുകൾ", "ഡോൾമെൻ"), ("പട്ടനം", "എറണാകുളം"), ("പട്ടനം", "മുചിരി"),
    ("അരിയന്നൂർ", "തൃശ്ശൂർ"), ("അരിയന്നൂർ ശവകുടീരം", "മെഗാലിത്"),
    ("തെന്മല", "തിരുവനന്തപുരം"), ("തെന്മല ഗുഹ", "മീസോലിത്തിക്"),
    ("കാഞ്ഞിരപ്പുഴ", "പാലക്കാട്"), ("കാഞ്ഞിരപ്പുഴ", "ശിലായുഗം"),
    ("ചേവായൂർ", "കോഴിക്കോട്"), ("ചേരമാൻ പറമ്പ്", "കൊടുങ്ങല്ലൂർ"),
    ("നിലംബൂർ", "തൃശ്ശൂർ"), ("വില്വട്ടം", "തൃശ്ശൂർ"),
    ("വരന്തരപ്പിള്ളി", "തൃശ്ശൂർ"), ("ഏനാടിമംഗലം", "തൃശ്ശൂർ"),
    ("കുന്നത്തുബാലു", "മലപ്പുറം"), ("വള്ളുവശ്ശേരി", "മലപ്പുറം"),
    ("കരിമ്പുളയ്ക്കൽ", "മലപ്പുറം"), ("മാങ്ങാട്", "കൊല്ലം"),
    ("പുഴയങ്കുടി", "കൊല്ലം"), ("ഇടുക്കി മുനിയറുകൾ", "ശവകുടീരം"),
    ("കൊടുങ്ങല്ലൂർ", "വ്യാപാരകേന്ദ്രം"), ("പട്ടനം", "ചേരകാലം"),
    ("ചേരമാൻ പറമ്പ്", "ചേരരാജാക്കന്മാർ"), ("മറയൂർ", "ചോക്ക്"),
    ("എടക്കൽ ഗുഹകൾ", "നവീന ശിലായുഗം"), ("ചേവായൂർ", "മഹാശിലായുഗം"),
    ("പട്ടനം പുരാവസ്തു", "റോം-ചേര വ്യാപാരം"), ("കാഞ്ഞിരപ്പുഴ പാറ", "ശിലായുഗം"),
    ("തെന്മല പാറ", "മീസോലിത്തിക്"), ("അരിയന്നൂർ കല്ലറ", "മെഗാലിത്"),
    ("നിലംബൂർ കല്ലറ", "മെഗാലിത്"), ("വരന്തരപ്പിള്ളി കല്ലറ", "മെഗാലിത്"),
    ("കunnathubalu കല്ലറ", "മെഗാലിത്"), ("പുഴയങ്കുടി കല്ലറ", "മെഗാലിത്"),
    ("മാങ്ങാട് കല്ലറ", "മെഗാലിത്"), ("ചേരമാൻ പറമ്പ്", "ചേരരാജവംശം"),
]
DATA["ARCH_SITE"] = [(a.replace("കunnathubalu", "കunnathubalu"), b) for a, b in DATA["ARCH_SITE"]]

print("Need to complete - this is a stub generator")
