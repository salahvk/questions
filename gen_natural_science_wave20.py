#!/usr/bin/env python3
"""Generate natural_science_wave20_facts.py — 20 env-science categories, 2400+ stems."""

from __future__ import annotations

import importlib.util
import pprint
import random
import textwrap
from pathlib import Path

OUT = Path(__file__).parent / "natural_science_wave20_facts.py"
MIN_COUNT = 2000

HEADER = textwrap.dedent('''
    #!/usr/bin/env python3
    """Wave 20 natural science facts — 20 Malayalam PSC environmental categories."""

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
    ) -> None:
        terms = list(dict.fromkeys(t for t, _, _, _ in facts))
        answers = list(dict.fromkeys(a for _, a, _, _ in facts))
        for term, ans, wrong, diff in facts:
            add_candidate(
                out, existing, rng,
                f"{prefix} '{term}'?",
                ans, wrong, diff, pool=answers,
            )
            add_candidate(
                out, existing, rng,
                f"'{ans}' ഏതിനെ സൂചിപ്പിക്കുന്നു?",
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


    def _emit_triples(
        out: list[Candidate],
        existing: set[str],
        rng: random.Random,
        rows: list[tuple[str, str, str]],
        ab_templates: list[str],
        ac_templates: list[str],
        pool_b: list[str],
        pool_c: list[str],
        diff: str = "medium",
    ) -> None:
        for a, b, c in rows:
            for tmpl in ab_templates:
                add_candidate(
                    out, existing, rng,
                    tmpl.format(a=a, b=b, c=c),
                    b, _pool(pool_b, b)[:3], diff, pool=pool_b,
                )
            for tmpl in ac_templates:
                add_candidate(
                    out, existing, rng,
                    tmpl.format(a=a, b=b, c=c),
                    c, _pool(pool_c, c)[:3], diff, pool=pool_c,
                )

''')

FOOTER = textwrap.dedent('''

    def generate_wave20_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
        out: list[Candidate] = []
        _emit_all_categories(out, existing, rng)
        return interleave_candidates(out, rng)


    if __name__ == "__main__":
        print(len(generate_wave20_candidates(set(), random.Random(42))))
''')


def build_all_data() -> dict:
    """Return category name -> data for wave20 module."""
    from nsc_wave20_data import load_data
    return load_data()


EMIT_BODY = r'''
PAIR_AB = [
    "'{a}' ഏതുമായി ബന്ധപ്പെട്ട പ്രധാന വിവരം?",
    "പരിസ്ഥിതി ശാസ്ത്രത്തിൽ '{a}' സംബന്ധിച്ച പ്രധാന വിവരം?",
    "'{a}' ഏത് വിഭാഗത്തിലേക്ക് പെടുന്നു?",
    "PSC പരിസ്ഥിതി വിജ്ഞാനത്തിൽ '{a}'-യുമായി ബന്ധപ്പെട്ട വിവരം?",
]
PAIR_BA = [
    "'{b}' സംബന്ധിച്ച പ്രധാന പരിസ്ഥിതി വിവരം '{a}'?",
    "'{b}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന പരിസ്ഥിതി വിവരം '{a}'?",
]

def _emit_trophic(out, existing, rng):
    _emit_pairs(out, existing, rng, "ഭക്ഷ്യശൃംഖലയിൽ ", TROPHIC_ROWS,
        ["'{a}' ഏത് ഭക്ഷ്യശൃംഖല നിലയിൽ പെടുന്നു?", "'{a}' ഏത് ട്രോഫിക് നിലയിലാണ്?",
         "ഇക്കോസിസ്റ്റത്തിൽ '{a}' ഏത് ഭക്ഷണശൃംഖല സ്തരത്തിൽ പെടുന്നു?"],
        ["'{b}' ഭക്ഷ്യശൃംഖല നിലയിലെ പ്രതിനിധി ജീവി ഏത്?",
         "'{b}' സ്തരത്തിലെ പ്രധാന ജീവി ഏത്?"])

def _emit_biogeo(out, existing, rng):
    _emit_pairs(out, existing, rng, "ജൈവഭൗതിക ചക്രങ്ങളിൽ ", BIOGEO_ROWS,
        ["'{a}' ചക്രത്തിൽ '{b}' പ്രധാനമായി എന്തിനാണ്?", "'{a}' ചക്രവുമായി ബന്ധപ്പെട്ട പ്രക്രിയ '{b}'?",
         "'{a}' ചക്രത്തിൽ പ്രധാന ഘടകം/പ്രക്രിയ '{b}'?"],
        ["'{b}' ഏത് ജൈവഭൗതിക ചക്രവുമായി ബന്ധപ്പെട്ടതാണ്?",
         "'{b}' പ്രക്രിയ പ്രധാനമായി ഏത് ചക്രവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"])
    _emit(out, existing, rng, "ജൈവഭൗതിക ചക്രങ്ങളിൽ", BIOGEO_FACTS)

def _emit_succession(out, existing, rng):
    _emit_pairs(out, existing, rng, "പാരിസ്ഥിതിക അനുക്രമണത്തിൽ ", SUCCESSION_ROWS,
        ["'{a}' അനുക്രമണത്തിൽ '{b}' ഏത് ഘട്ടമാണ്?", "'{a}'-ൽ '{b}' എന്തിനെ സൂചിപ്പിക്കുന്നു?",
         "'{a}' അനുക്രമണത്തിന്റെ പ്രധാന ഘട്ടം '{b}'?"],
        ["'{b}' ഏത് അനുക്രമണ തരവുമായി ബന്ധപ്പെട്ടതാണ്?",
         "'{b}' ഘട്ടം ഏത് പാരിസ്ഥിതിക അനുക്രമണത്തിൽ കാണപ്പെടുന്നു?"])
    _emit(out, existing, rng, "പാരിസ്ഥിതിക അനുക്രമണത്തിൽ", SUCCESSION_FACTS)

def _emit_plant_groups(out, existing, rng):
    _emit_pairs(out, existing, rng, "സസ്യ പാരിസ്ഥിതിക ഗ്രൂപ്പുകളിൽ ", PLANT_GROUP_ROWS,
        ["'{a}' ഏത് പാരിസ്ഥിതിക സസ്യ ഗ്രൂപ്പിലേക്ക് പെടുന്നു?", "'{a}' ഏത് തരം സസ്യങ്ങളുടെ ഉദാഹരണമാണ്?",
         "പരിസ്ഥിതി പഠനത്തിൽ '{a}' ഏത് സസ്യ വിഭാഗമാണ്?"],
        ["'{b}' ഗ്രൂപ്പിലെ പ്രതിനിധി സസ്യം/ഉദാഹരണം ഏത്?",
         "'{b}' സസ്യങ്ങളുടെ ഉദാഹരണം ഏത്?"])

def _emit_hotspots(out, existing, rng):
    _emit_pairs(out, existing, rng, "ജൈവവൈവിധ്യ ഹോട്ട്‌സ്പോട്ടുകളിൽ ", HOTSPOT_ROWS,
        ["'{a}' ഹോട്ട്‌സ്പോട്ട് പ്രധാനമായി ഏത് പ്രദേശവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{a}' ജൈവവൈവിധ്യ ഹോട്ട്‌സ്പോട്ട് ഏത് ഭൂപ്രദേശമാണ്?",
         "ഇന്ത്യയിലെ '{a}' ഹോട്ട്‌സ്പോട്ട് ഏത് പ്രദേശമാണ്?"],
        ["'{b}' പ്രദേശം ഏത് ജൈവവൈവിധ്യ ഹോട്ട്‌സ്പോട്ടുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' ഏത് ഹോട്ട്‌സ്പോട്ടിന്റെ ഭാഗമാണ്?"])

def _emit_parks(out, existing, rng):
    _emit_pairs(out, existing, rng, "ദേശീയോദ്യാനങ്ങളിൽ ", PARK_ROWS,
        ["'{a}' ദേശീയോദ്യാനം ഏത് സംസ്ഥാനത്താണ്?", "'{a}' ഏത് സംസ്ഥാനത്തിന്റെ ദേശീയോദ്യാനമാണ്?",
         "പരിസ്ഥിതി പഠനത്തിൽ '{a}' ദേശീയോദ്യാനം സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം ഏത്?"],
        ["'{b}' സംസ്ഥാനത്തിലെ പ്രശസ്ത ദേശീയോദ്യാനം ഏത്?",
         "'{b}' സംസ്ഥാനത്തിലെ ദേശീയോദ്യാനം ഏത്?"])

def _emit_ramsar(out, existing, rng):
    _emit_pairs(out, existing, rng, "റാംസർ ചതുപ്പുപ്രദേശങ്ങളിൽ ", RAMSAR_ROWS,
        ["'{a}' റാംസർ സൈറ്റ് ഏത് സംസ്ഥാനത്താണ്?", "'{a}' ഏത് സംസ്ഥാനത്തിലെ റാംസർ ചതുപ്പുപ്രദേശമാണ്?",
         "'{a}' റാംസർ സൈറ്റ് സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം ഏത്?"],
        ["'{b}' സംസ്ഥാനത്തിലെ റാംസർ ചതുപ്പുപ്രദേശം ഏത്?",
         "'{b}' സംസ്ഥാനത്തിലെ റാംസർ സൈറ്റ് ഏത്?"])

def _emit_iucn(out, existing, rng):
    _emit(out, existing, rng, "IUCN റെഡ് ലിസ്റ്റിൽ", IUCN_FACTS)
    _emit_pairs(out, existing, rng, "IUCN വിഭാഗങ്ങളിൽ ", IUCN_ROWS,
        ["'{a}' IUCN വിഭാഗം '{b}'-നെ എന്തിനെ സൂചിപ്പിക്കുന്നു?", "'{a}' വിഭാഗത്തിലെ സ്പീഷിസ് സ്ഥിതി '{b}'?",
         "'{a}' ഏത് തരം സംരക്ഷണ സ്ഥിതിയാണ്?"],
        ["'{b}' സ്ഥിതി ഏത് IUCN വിഭാഗത്തിലാണ്?",
         "'{b}' ഏത് IUCN വിഭാഗവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"])

def _emit_wpa(out, existing, rng):
    _emit_pairs(out, existing, rng, "വന്യജീവി സംരക്ഷണ നിയമത്തിൽ ", WPA_ROWS,
        ["'{a}' ഏത് ഷെഡ്യൂളിൽ പെടുന്നു?", "'{a}' വന്യജീവി സംരക്ഷണ നിയമപ്രകാരം ഏത് ഷെഡ്യൂളിലാണ്?",
         "വന്യജീവി നിയമത്തിൽ '{a}' ഏത് ഷെഡ്യൂളിൽ ഉൾപ്പെടുന്നു?"],
        ["'{b}' ഷെഡ്യൂളിലെ പ്രതിനിധി വന്യജീവി ഏത്?",
         "'{b}' ഷെഡ്യൂളിൽ പെടുന്ന പ്രധാന വന്യജീവി ഏത്?"])

def _emit_laws(out, existing, rng):
    _emit_pairs(out, existing, rng, "പരിസ്ഥിതി നിയമങ്ങളിൽ ", LAW_ROWS,
        ["'{a}' നിയമം/നിയമവിഭാഗം '{b}'-യുമായി എന്തിനെ ബന്ധപ്പെടുത്തുന്നു?",
         "'{a}' ഏത് പരിസ്ഥിതി നിയമവിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "ഇന്ത്യയിൽ '{a}' ഏത് നിയമവിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"],
        ["'{b}' വിഷയം ഏത് പരിസ്ഥിതി നിയമവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' ഏത് നിയമത്തിന്റെ പ്രധാന ലക്ഷ്യമാണ്?"])
    _emit(out, existing, rng, "പരിസ്ഥിതി നിയമങ്ങളിൽ", LAW_FACTS)

def _emit_agencies(out, existing, rng):
    _emit_pairs(out, existing, rng, "പരിസ്ഥിതി ഏജൻസികളിൽ ", AGENCY_ROWS,
        ["'{a}' ഏജൻസി/ബോർഡ് '{b}'-യുമായി എന്തിനെ ബന്ധപ്പെടുത്തുന്നു?",
         "'{a}' ഏത് പരിസ്ഥിതി ഏജൻസിയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "പരിസ്ഥിതി നിയന്ത്രണത്തിൽ '{a}' ഏത് സ്ഥാപനവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"],
        ["'{b}' പ്രവർത്തനം/നിയന്ത്രണം ഏത് ഏജൻസിയുടെ പൊതുവായ പങ്കാണ്?",
         "'{b}' ഏത് പരിസ്ഥിതി ഏജൻസിയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"])

def _emit_conventions(out, existing, rng):
    _emit_pairs(out, existing, rng, "അന്താരാഷ്ട്ര പരിസ്ഥിതി കരാറുകളിൽ ", CONVENTION_ROWS,
        ["'{a}' കരാർ/ഉടമ്പടി '{b}'-യുമായി എന്തിനെ ബന്ധപ്പെടുത്തുന്നു?",
         "'{a}' ഏത് പരിസ്ഥിതി പ്രശ്നവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "അന്താരാഷ്ട്ര പരിസ്ഥിതി കരാറിൽ '{a}' പ്രധാന ലക്ഷ്യം '{b}'?"],
        ["'{b}' പ്രശ്നം ഏത് അന്താരാഷ്ട്ര കരാറുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' ഏത് കരാറിന്റെ പ്രധാന ലക്ഷ്യമാണ്?"])
    _emit(out, existing, rng, "അന്താരാഷ്ട്ര പരിസ്ഥിതി കരാറുകളിൽ", CONVENTION_FACTS)

def _emit_un_agencies(out, existing, rng):
    _emit_pairs(out, existing, rng, "അന്താരാഷ്ട്ര പരിസ്ഥിതി സംഘടനകളിൽ ", UN_AGENCY_ROWS,
        ["'{a}' സംഘടന '{b}'-യുമായി എന്തിനെ ബന്ധപ്പെടുത്തുന്നു?",
         "'{a}' ഏത് പരിസ്ഥിതി മേഖലയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "അന്താരാഷ്ട്ര പരിസ്ഥിതി സംഘടന '{a}' പ്രധാന പങ്ക് '{b}'?"],
        ["'{b}' മേഖല/പ്രശ്നം ഏത് അന്താരാഷ്ട്ര സംഘടനയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' ഏത് സംഘടനയുടെ പ്രധാന ലക്ഷ്യമാണ്?"])

def _emit_noise(out, existing, rng):
    _emit(out, existing, rng, "ശബ്ദ മലിനീകരണത്തിൽ", NOISE_FACTS)
    _emit_pairs(out, existing, rng, "ശബ്ദ മലിനീകരണത്തിൽ ", NOISE_ROWS,
        ["'{a}' ശബ്ദ മലിനീകരണവുമായി ബന്ധപ്പെട്ട വിവരം '{b}'?",
         "'{a}' ഏത് ശബ്ദ മലിനീകരണ വിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "ശബ്ദ മലിനീകരണത്തിൽ '{a}' പ്രധാന വിവരം '{b}'?"],
        ["'{b}' ഏത് ശബ്ദ മലിനീകരണ വിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' ശബ്ദ മലിനീകരണത്തിൽ പ്രധാനമായി എന്തിനെ സൂചിപ്പിക്കുന്നു?"])

def _emit_soil(out, existing, rng):
    _emit_pairs(out, existing, rng, "മണ്ണ് മലിനീകരണത്തിലും മണ്ണിന്റെ തരത്തിലും ", SOIL_ROWS,
        ["'{a}' മണ്ണ്/മണ്ണ് പ്രശ്നം '{b}'-യുമായി എന്തിനെ ബന്ധപ്പെടുത്തുന്നു?",
         "'{a}' ഏത് മണ്ണ് വിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "മണ്ണ് പഠനത്തിൽ '{a}' പ്രധാന വിവരം '{b}'?"],
        ["'{b}' ഏത് മണ്ണ് വിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' മണ്ണ് പഠനത്തിൽ പ്രധാനമായി എന്തിനെ സൂചിപ്പിക്കുന്നു?"])
    _emit(out, existing, rng, "മണ്ണ് പഠനത്തിൽ", SOIL_FACTS)

def _emit_marine(out, existing, rng):
    _emit_pairs(out, existing, rng, "ജല/സമുദ്ര മലിനീകരണത്തിൽ ", MARINE_ROWS,
        ["'{a}' ജല മലിനീകരണവുമായി ബന്ധപ്പെട്ട വിവരം '{b}'?",
         "'{a}' ഏത് ജല മലിനീകരണ വിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "ജല മലിനീകരണത്തിൽ '{a}' പ്രധാന വിവരം '{b}'?"],
        ["'{b}' ഏത് ജല മലിനീകരണ വിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' ജല മലിനീകരണത്തിൽ പ്രധാനമായി എന്തിനെ സൂചിപ്പിക്കുന്നു?"])
    _emit(out, existing, rng, "ജല മലിനീകരണത്തിൽ", MARINE_FACTS)

def _emit_ewaste(out, existing, rng):
    _emit(out, existing, rng, "ഇ-വേസ്റ്റ്/അപകടകര മാലിന്യത്തിൽ", EWASTE_FACTS)
    _emit_pairs(out, existing, rng, "മാലിന്യ കൈകാര്യം ചെയ്യലിൽ ", EWASTE_ROWS,
        ["'{a}' മാലിന്യ തരം '{b}'-യുമായി എന്തിനെ ബന്ധപ്പെടുത്തുന്നു?",
         "'{a}' ഏത് മാലിന്യ വിഭാഗവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "മാലിന്യ നിയന്ത്രണത്തിൽ '{a}' പ്രധാന വിവരം '{b}'?"],
        ["'{b}' ഏത് മാലിന്യ തരവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' മാലിന്യ കൈകാര്യം ചെയ്യലിൽ പ്രധാനമായി എന്തിനെ സൂചിപ്പിക്കുന്നു?"])

def _emit_eia(out, existing, rng):
    _emit(out, existing, rng, "പരിസ്ഥിതി പ്രഭാവ മൂല്യനിർണയത്തിൽ", EIA_FACTS)
    _emit_pairs(out, existing, rng, "EIA-യിൽ ", EIA_ROWS,
        ["'{a}' EIA ഘട്ടം/ആശയം '{b}'-യുമായി എന്തിനെ ബന്ധപ്പെടുത്തുന്നു?",
         "'{a}' ഏത് EIA വിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "പരിസ്ഥിതി പ്രഭാവ മൂല്യനിർണയത്തിൽ '{a}' പ്രധാന വിവരം '{b}'?"],
        ["'{b}' ഏത് EIA ഘട്ടവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' EIA പ്രക്രിയയിൽ പ്രധാനമായി എന്തിനെ സൂചിപ്പിക്കുന്നു?"])

def _emit_climate_strategy(out, existing, rng):
    _emit_pairs(out, existing, rng, "കാലാവസ്ഥാ നടപടികളിൽ ", CLIMATE_STRATEGY_ROWS,
        ["'{a}' കാലാവസ്ഥാ നടപടി '{b}' തരത്തിൽ പെടുന്നു?", "'{a}' ഏത് കാലാവസ്ഥാ തന്ത്രവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "കാലാവസ്ഥാ മാറ്റത്തിൽ '{a}' പ്രധാന വിവരം '{b}'?"],
        ["'{b}' തരം കാലാവസ്ഥാ നടപടിയുടെ ഉദാഹരണം ഏത്?",
         "'{b}' ഏത് കാലാവസ്ഥാ തന്ത്രവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"])
    _emit(out, existing, rng, "കാലാവസ്ഥാ നടപടികളിൽ", CLIMATE_STRATEGY_FACTS)

def _emit_green_tech(out, existing, rng):
    _emit_pairs(out, existing, rng, "പരിസ്ഥിതി സൗഹൃദ സാങ്കേതികവിദ്യയിൽ ", GREEN_TECH_ROWS,
        ["'{a}' സാങ്കേതികവിദ്യ '{b}'-യുമായി എന്തിനെ ബന്ധപ്പെടുത്തുന്നു?",
         "'{a}' ഏത് പരിസ്ഥിതി പ്രയോഗവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "പരിസ്ഥിതി നിരീക്ഷണത്തിൽ '{a}' പ്രധാന വിവരം '{b}'?",
         "'{a}' ഏത് പരിസ്ഥിതി സാങ്കേതികവിദ്യയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"],
        ["'{b}' പ്രയോഗം ഏത് സാങ്കേതികവിദ്യയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' ഏത് പരിസ്ഥിതി സാങ്കേതികവിദ്യയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' സംബന്ധിച്ച പരിസ്ഥിതി സാങ്കേതികവിദ്യ ഏത്?"])
    _emit(out, existing, rng, "പരിസ്ഥിതി സൗഹൃദ സാങ്കേതികവിദ്യയിൽ", GREEN_TECH_FACTS)

def _emit_env_days(out, existing, rng):
    _emit_pairs(out, existing, rng, "അന്താരാഷ്ട്ര പരിസ്ഥിതി ദിനങ്ങളിൽ ", ENV_DAY_ROWS,
        ["'{a}' ഏത് തീയതിയിലാണ്?", "'{a}' എപ്പോൾ ആചരിക്കുന്നു?",
         "പരിസ്ഥിതി ദിനങ്ങളിൽ '{a}' തീയതി '{b}'?"],
        ["'{b}' തീയതിയിലെ പ്രധാന പരിസ്ഥിതി ദിനം ഏത്?",
         "'{b}' ആചരിക്കുന്ന പരിസ്ഥിതി ദിനം ഏത്?"])

def _emit_scientists(out, existing, rng):
    _emit_pairs(out, existing, rng, "പരിസ്ഥിതി ശാസ്ത്ര ചരിത്രത്തിൽ ", SCIENTIST_ROWS,
        ["'{a}' ഏത് പ്രവർത്തനവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?", "'{a}' ഏത് പരിസ്ഥിതി സംഭാവനയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "പരിസ്ഥിതി ശാസ്ത്രത്തിൽ '{a}' പ്രധാന സംഭാവന '{b}'?"],
        ["'{b}' സംബന്ധിച്ച പ്രധാന പരിസ്ഥിതി ശാസ്ത്രജ്ഞൻ ആരാണ്?",
         "'{b}' സംബന്ധിച്ച പ്രധാന വ്യക്തി ആരാണ്?"])


def _emit_conservation(out, existing, rng):
    _emit_pairs(out, existing, rng, "പരിസ്ഥിതി സംരക്ഷണത്തിൽ ", CONSERVATION_ROWS,
        ["'{a}' ഏത് പരിസ്ഥിതി പ്രശ്നവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?", "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന പരിഹാരം/വിഷയം '{b}'?",
         "പരിസ്ഥിതി സംരക്ഷണത്തിൽ '{a}' പ്രധാനമായി '{b}'?",
         "'{a}' ഏത് സംരക്ഷണ രീതിയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "PSC പരിസ്ഥിതി പഠനത്തിൽ '{a}'-യുമായി ബന്ധപ്പെട്ട വിവരം '{b}'?"],
        ["'{b}' ഏത് പരിസ്ഥിതി സംരക്ഷണ വിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' സംബന്ധിച്ച പ്രധാന പരിസ്ഥിതി സംരക്ഷണ വിവരം '{a}'?",
         "'{b}' ഏത് സംരക്ഷണ പ്രശ്നവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"])

def _emit_all_categories(out, existing, rng):
    _emit_trophic(out, existing, rng)
    _emit_biogeo(out, existing, rng)
    _emit_succession(out, existing, rng)
    _emit_plant_groups(out, existing, rng)
    _emit_hotspots(out, existing, rng)
    _emit_parks(out, existing, rng)
    _emit_ramsar(out, existing, rng)
    _emit_iucn(out, existing, rng)
    _emit_wpa(out, existing, rng)
    _emit_laws(out, existing, rng)
    _emit_agencies(out, existing, rng)
    _emit_conventions(out, existing, rng)
    _emit_un_agencies(out, existing, rng)
    _emit_noise(out, existing, rng)
    _emit_soil(out, existing, rng)
    _emit_marine(out, existing, rng)
    _emit_ewaste(out, existing, rng)
    _emit_eia(out, existing, rng)
    _emit_climate_strategy(out, existing, rng)
    _emit_green_tech(out, existing, rng)
    _emit_env_days(out, existing, rng)
    _emit_conservation(out, existing, rng)
    _emit_scientists(out, existing, rng)
    _emit_pairs(out, existing, rng, "കാലാവസ്ഥ/ഭൂമിയിൽ ", WEATHER_ROWS,
        ["'{a}' അളക്കാൻ/അറിയാൻ ഉപയോഗിക്കുന്നത് '{b}'?", "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വിവരം '{b}'?",
         "പരിസ്ഥിതി പഠനത്തിൽ '{a}' പ്രധാനമായി '{b}'?"],
        ["'{b}' ഏത് കാലാവസ്ഥാ/ഭൂമി വിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' സംബന്ധിച്ച പ്രധാന കാലാവസ്ഥാ/ഭൂമി വിവരം '{a}'?"])
    _emit_pairs(out, existing, rng, "മാലിന്യങ്ങളിലും മലിനീകരണത്തിലും ", POLLUTION_ROWS,
        ["'{a}' ഏത് മലിനീകരണ വിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?", "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വിവരം '{b}'?",
         "മാലിന്യ പഠനത്തിൽ '{a}' പ്രധാനമായി '{b}'?"],
        ["'{b}' ഏത് മലിനീകരണ വിഷയവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "'{b}' സംബന്ധിച്ച പ്രധാന മാലിന്യം/മലിനീകരണം '{a}'?"])
    _emit_pairs(out, existing, rng, "കേരള പരിസ്ഥിതിയിൽ ", KERALA_ENV_ROWS,
        ["'{a}' ഏത് സംസ്ഥാനവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?", "'{a}' പ്രധാനമായി ഏത് സംസ്ഥാനത്താണ്?",
         "കേരള പരിസ്ഥിതി പഠനത്തിൽ '{a}' ഏത് സംസ്ഥാനവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"],
        ["'{b}' സംസ്ഥാനത്തിലെ പ്രധാന പരിസ്ഥിതി സ്ഥലം/സ്ഥാപനം '{a}'?",
         "'{b}' സംസ്ഥാനവുമായി ബന്ധപ്പെട്ട പ്രധാന പരിസ്ഥിതി വിവരം '{a}'?"])
'''


def main() -> None:
    data = build_all_data()
    parts = [HEADER]
    for name in sorted(data):
        parts.append(f"{name} = {pprint.pformat(data[name], width=120)}\n")
    parts.append(EMIT_BODY)
    parts.append(FOOTER)
    source = "\n".join(parts)

    test_path = OUT.parent / "_nsc20_count_test.py"
    test_path.write_text(source, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("nsc20t", test_path)
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
