#!/usr/bin/env python3
"""Build awards_wave20_facts.py — 20 Malayalam PSC awards categories, 2500+ stems."""

from __future__ import annotations

import importlib.util
import pprint
import random
import textwrap
from pathlib import Path

from awards_wave20_data import build_all_data

OUT = Path(__file__).parent / "awards_wave20_facts.py"
MIN_COUNT = 2500

HEADER = textwrap.dedent('''\
    #!/usr/bin/env python3
    """Wave 20 awards facts — 20 Malayalam PSC topic categories."""

    from __future__ import annotations

    import random

    from awards_facts import (
        AWARD_METADATA,
        BHARAT_RATNA,
        BOOKER_PRIZE,
        DADASAHEB_PHALKE,
        INDIAN_NOBEL,
        JNANPITH,
        NATIONAL_FILM_BEST_ACTOR,
    )
    from refill_common import Candidate, add_candidate, interleave_candidates

    Fact = tuple[str, str, list[str], str]

    MALAYALAM_MONTHS = [
        "ജനുവരി", "ഫെബ്രുവരി", "മാർച്ച്", "ഏപ്രിൽ", "മേയ്", "ജൂൺ",
        "ജൂലൈ", "ആഗസ്റ്റ്", "സെപ്റ്റംബർ", "ഒക്ടോബർ", "നവംബർ", "ഡിസംബർ",
    ]

    COUNTRIES = [
        "നോർവേ", "സ്വീഡൻ", "ഡെൻമാർക്ക്", "ഫിൻലാന്റ്", "അമേരിക്ക", "ബ്രിട്ടൻ",
        "ഫ്രാൻസ്", "ജർമ്മനി", "ഇറ്റലി", "സ്പെയിൻ", "ജപ്പാൻ", "ചൈന",
        "ഓസ്ട്രേലിയ", "കനഡ", "റഷ്യ", "ഇന്ത്യ", "പാകിസ്ഥാൻ", "ശ്രീലങ്ക",
        "ബംഗ്ലാദേശ്", "നേപ്പാൾ", "ഇറാൻ", "ഇറാഖ്", "സൗദി അറേബ്യ",
        "എജിപ്ത്", "ദക്ഷിണാഫ്രിക്ക", "ബ്രസീൽ", "അർജന്റീന", "മെക്സിക്കോ",
        "സ്വിറ്റ്സർലാന്റ്", "ഓസ്ട്രിയ", "ബെൽജിയം", "നെതർലാന്റ്സ്", "ഇസ്രായേൽ",
        "ഫിലിപ്പീൻസ്",
    ]

    CITIES = [
        "സ്റ്റോക്ക്ഹോം", "ഒസ്ലോ", "ലണ്ടൻ", "പാരിസ്", "വാഷിംഗ്ടൺ", "ന്യൂയോർക്ക്",
        "ലോസ് ആഞ്ചൽസ്", "മുംബൈ", "ന്യൂഡൽഹി", "കൊൽക്കത്ത", "ചെന്നൈ", "തിരുവനന്തപുരം",
        "കാന്സ്", "വെനീസ്", "ബെർലിൻ", "ടോക്കിയോ", "ഓസ്ക", "കോപ്പൻഹേഗൻ",
        "ആംസ്റ്റർഡാം", "ജനീവ", "റോം", "മാഡ്രിഡ്", "സിഡ്നി", "ടോറോണ്ടോ",
        "മനില", "ഹ്യൂസ്റ്റൺ", "സാൻ ഫ്രാൻസിസ്കോ", "ഗോവ",
    ]

    AWARD_NAMES = [
        "ഭാരതരത്ന", "പത്മവിഭൂഷൺ", "പത്മഭൂഷൺ", "പത്മശ്രീ", "ജ്ഞാനപീഠ പുരസ്കാരം",
        "നാഷണൽ ഫിലിം അവാർഡ്", "അർജുന അവാർഡ്", "മേജർ ധ്യാൻചന്ദ് ഖേൽരത്ന",
        "ദാദാസാഹേബ് ഫാൽക്കെ അവാർഡ്", "നോബൽ സമ്മാനം", "ബുക്കർ പ്രൈസ്",
        "ഓസ്കാർ അവാർഡ്", "ഗ്രാമി അവാർഡ്", "പുലിറ്റ്സർ സമ്മാനം", "ഫീൽഡ്സ് മെഡൽ",
        "ട്യൂറിംഗ് അവാർഡ്", "ശാന്തി സ്വരൂപ് ഭട്നാഗർ പുരസ്കാരം", "പരമവീര ചക്രം",
        "അശോക ചക്രം", "സംഗീത നാടക അക്കാദമി അവാർഡ്", "ലളിത കലാ അക്കാദമി അവാർഡ്",
        "മൂർത്തിദേവി പുരസ്കാരം", "റാമോൺ മാഗ്സസേ അവാർഡ്", "ദ്രോണാചാര്യ അവാർഡ്",
    ]

    DEFINITION_AWARDS = {
        "ഭാരതരത്ന", "പത്മവിഭൂഷൺ", "പത്മഭൂഷൺ", "പത്മശ്രീ",
        "ജ്ഞാനപീഠ പുരസ്കാരം", "കേരള ജ്യോതി", "മേജർ ധ്യാൻചന്ദ് ഖേൽരത്ന",
    }

    RANK_FIELDS = [
        "പരമോന്നത സിവിലിയൻ ബഹുമതി",
        "രണ്ടാമത്തെ ഉയർന്ന സിവിലിയൻ ബഹുമതി",
        "മൂന്നാമത്തെ ഉയർന്ന സിവിലിയൻ ബഹുമതി",
        "നാലാമത്തെ ഉയർന്ന സിവിലിയൻ ബഹുമതി",
        "ഉയർന്ന സാഹിത്യ ബഹുമതി",
        "ഉയർന്ന കായിക ബഹുമതി",
        "പരമോന്നത സംസ്ഥാന ബഹുമതി",
    ]


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
            add_candidate(
                out, existing, rng,
                f"'{ans}' ഏതിനെ സൂചിപ്പിക്കുന്നു?",
                term, _pool(terms, term)[:6], diff, pool=terms,
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


    def _emit_quads(
        out: list[Candidate],
        existing: set[str],
        rng: random.Random,
        rows: list[tuple[str, str, str, str]],
        who_templates: list[str],
        year_templates: list[str],
        field_templates: list[str],
        tier_templates: list[str],
        pool_names: list[str],
        pool_years: list[str],
        pool_fields: list[str],
        pool_tiers: list[str],
        diff: str = "medium",
    ) -> None:
        for name, year, field, tier in rows:
            for tmpl in who_templates:
                add_candidate(
                    out, existing, rng,
                    tmpl.format(n=name, y=year, f=field, t=tier),
                    name, _pool(pool_names, name)[:3], diff, pool=pool_names,
                )
            for tmpl in year_templates:
                add_candidate(
                    out, existing, rng,
                    tmpl.format(n=name, y=year, f=field, t=tier),
                    year, _pool(pool_years, year)[:3], diff, pool=pool_years,
                )
            for tmpl in field_templates:
                add_candidate(
                    out, existing, rng,
                    tmpl.format(n=name, y=year, f=field, t=tier),
                    field, _pool(pool_fields, field)[:3], diff, pool=pool_fields,
                )
            for tmpl in tier_templates:
                add_candidate(
                    out, existing, rng,
                    tmpl.format(n=name, y=year, f=field, t=tier),
                    tier, _pool(pool_tiers, tier)[:3], diff, pool=pool_tiers,
                )

''')

FOOTER = textwrap.dedent('''\

    def generate_wave20_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
        out: list[Candidate] = []
        _emit_all_categories(out, existing, rng)
        return interleave_candidates(out, rng)


    if __name__ == "__main__":
        print(len(generate_wave20_candidates(set(), random.Random(42))))
''')

PAIR_AB = [
    "'{a}'-ന്റെ പുരസ്കാര തുക/സമ്മാന തുക എത്ര?",
    "'{a}'-ന് നൽകുന്ന പണത്തിന്റെ തുക?",
    "PSC അവാർഡ് വിജ്ഞാനത്തിൽ '{a}'-ന്റെ സമ്മാന തുക?",
    "'{a}' പുരസ്കാരത്തിന്റെ പണമൂല്യം?",
    "'{a}'-ന് ലഭിക്കുന്ന സാമ്പത്തിക സമ്മാനം?",
    "'{a}'-ന്റെ സമ്മാന തുക PSC-യിൽ?",
    "പുരസ്കാരം '{a}' — പണമൂല്യം?",
]

PAIR_BA = [
    "'{b}' സമ്മാന തുക നൽകുന്ന പുരസ്കാരം ഏത്?",
    "'{b}' പണമൂല്യമുള്ള അവാർഡ് ഏത്?",
    "'{b}' ലഭിക്കുന്ന പുരസ്കാരം?",
]

CAP_AB = [
    "'{a}'-ൽ വർഷത്തിൽ പരമാവധി എത്ര പേർക്ക് നൽകാം?",
    "'{a}'-ന്റെ വാർഷിക പരമാവധി ഗ്രഹീതാക്കളുടെ എണ്ണം?",
    "'{a}' പുരസ്കാരത്തിന്റെ വാർഷിക പരിധി?",
    "PSC അവാർഡ് '{a}'-ന്റെ വാർഷിക പരമാവധി?",
]

CAP_BA = [
    "'{b}' പരിധിയുള്ള പുരസ്കാരം ഏത്?",
    "'{b}' വാർഷിക പരിധി നിശ്ചയിച്ച അവാർഡ്?",
]

SYMBOL_AB = [
    "'{a}'-ന്റെ ചിഹ്നം/പതാക ഏത്?",
    "'{a}'-ൽ ഉപയോഗിക്കുന്ന ചിഹ്നം?",
    "'{a}' പുരസ്കാരത്തിന്റെ പ്രതീകം?",
    "PSC അവാർഡ് '{a}'-ന്റെ ചിഹ്നം?",
]

SYMBOL_BA = [
    "'{b}' ചിഹ്നമുള്ള പുരസ്കാരം ഏത്?",
    "'{b}' പ്രതീകമുള്ള അവാർഡ്?",
]

MONTH_AB = [
    "'{a}' സാധാരണ ഏത് മാസം?",
    "'{a}'-ന് ബന്ധപ്പെട്ട മാസം?",
    "'{a}' നടക്കുന്ന/പ്രഖ്യാപിക്കുന്ന മാസം?",
    "PSC അവാർഡ് '{a}'-ന്റെ മാസം?",
]

COUNTRY_AB = [
    "'{a}'-ന്റെ ഉത്ഭവ/സ്ഥാന രാജ്യം ഏത്?",
    "'{a}' നൽകുന്ന/നടത്തുന്ന രാജ്യം?",
    "'{a}'-ന് ബന്ധപ്പെട്ട രാജ്യം?",
    "PSC അവാർഡ് '{a}'-ന്റെ രാജ്യം?",
]

CITY_AB = [
    "'{a}'-ന്റെ പ്രധാന ചടങ്ങ്/വിതരണ നഗരം?",
    "'{a}' സാധാരണ നടക്കുന്ന നഗരം?",
    "'{a}'-ന് ബന്ധപ്പെട്ട നഗരം?",
    "PSC അവാർഡ് '{a}'-ന്റെ നഗരം?",
]

JURY_AB = [
    "'{a}' തിരഞ്ഞെടുക്കുന്ന/നൽകുന്ന സ്ഥാപനം?",
    "'{a}'-ന്റെ ജൂറി/നിയമിക്കുന്ന സ്ഥാപനം?",
    "'{a}'-ന് ബന്ധപ്പെട്ട സ്ഥാപനം?",
    "PSC അവാർഡ് '{a}'-ന്റെ നിയമിക്കുന്ന സ്ഥാപനം?",
]

JURY_BA = [
    "'{b}' സ്ഥാപനം തിരഞ്ഞെടുക്കുന്ന/നൽകുന്ന പുരസ്കാരം?",
    "'{b}'-ന് ബന്ധപ്പെട്ട അവാർഡ്?",
]

REN_AB = [
    "'{a}' എന്ന പേരിൽ നിന്ന് {c}-ൽ '{b}' എന്ന് പുനർനാമകരണം ചെയ്ത അവാർഡ്?",
    "'{a}'-ന്റെ പുതിയ പേര് {c}-ൽ '{b}'?",
    "{c}-ൽ '{a}' -> '{b}' പുനർനാമകരണം?",
]

REN_AC = [
    "'{b}' എന്ന പേര് {c}-ൽ '{a}'-ൽ നിന്ന് മാറ്റിയ അവാർഡ്?",
    "{c}-ൽ '{b}' ആയി പുനർനാമകരണം ചെയ്ത '{a}'?",
]

SNA_WHO = [
    "സംഗീത നാടക അക്കാദമി അവാർഡ് {c}-ൽ {b} വിഭാഗത്തിൽ ലഭിച്ചത്?",
    "{c} സംഗീത നാടക അക്കാദമി അവാർഡ് {b} വിഭാഗത്തിൽ?",
    "PSC: {c} SNA അവാർഡ് {b} — ആരാണ്?",
]

SNA_FIELD = [
    "'{a}' ലഭിച്ച SNA അവാർഡ് വിഭാഗം?",
    "'{a}'-ന്റെ SNA അവാർഡ് മേഖല?",
]

SNA_YEAR = [
    "'{a}' SNA അവാർഡ് ലഭിച്ച വർഷം?",
    "SNA അവാർഡ് '{a}'-ന്റെ വർഷം?",
]

FEL_WHO = [
    "സംഗീത നാടക അക്കാദമി ഫെലോഷിപ്പ് {b}-ൽ ലഭിച്ചത്?",
    "{b} SNA ഫെലോഷിപ്പ് — ആരാണ്?",
    "PSC: SNA ഫെലോഷിപ്പ് {b} — ആരാണ്?",
]

FEL_YEAR = [
    "'{a}' SNA ഫെലോഷിപ്പ് ലഭിച്ച വർഷം?",
    "SNA ഫെലോഷിപ്പ് '{a}'-ന്റെ വർഷം?",
]

LK_WHO = [
    "ലളിത കലാ അക്കാദമി അവാർഡ് {c}-ൽ {b} മാധ്യമത്തിൽ ലഭിച്ചത്?",
    "{c} ലളിത കലാ അവാർഡ് {b} — ആരാണ്?",
]

LK_MED = [
    "'{a}' ലഭിച്ച ലളിത കലാ അവാർഡ് മാധ്യമം?",
    "'{a}'-ന്റെ ലളിത കലാ മാധ്യമം?",
]

LK_YEAR = [
    "'{a}' ലളിത കലാ അവാർഡ് ലഭിച്ച വർഷം?",
]

MOOR_WHO = [
    "മൂർത്തിദേവി പുരസ്കാരം {c}-ൽ '{b}' എന്ന കൃതിക്ക് ലഭിച്ചത്?",
    "{c} മൂർത്തിദേവി '{b}' — ആരാണ്?",
]

MOOR_WORK = [
    "'{a}'-ന്റെ മൂർത്തിദേവി പുരസ്കാര കൃതി?",
    "മൂർത്തിദേവി '{a}'-ന് ലഭിച്ച കൃതി?",
]

MOOR_YEAR = [
    "'{a}' മൂർത്തിദേവി പുരസ്കാരം ലഭിച്ച വർഷം?",
]

NFA_WHO = [
    "നാഷണൽ ഫിലിം അവാർഡ് {c}-ൽ '{b}'-ന് മികച്ച നടൻ?",
    "{c} NFA മികച്ച നടൻ '{b}'?",
    "PSC: {c} NFA മികച്ച നടൻ — ആരാണ്?",
]

NFA_FILM = [
    "'{a}' NFA മികച്ച നടൻ ചിത്രം '{b}'?",
    "NFA മികച്ച നടൻ '{a}'-ന്റെ ചിത്രം?",
]

NFA_YEAR = [
    "'{a}' NFA മികച്ച നടൻ വർഷം?",
]

NFD_WHO = [
    "നാഷണൽ ഫിലിം അവാർഡ് {c}-ൽ '{b}'-ന് മികച്ച സംവിധായകൻ?",
    "{c} NFA മികച്ച സംവിധായകൻ '{b}'?",
]

NFD_FILM = [
    "'{a}' NFA മികച്ച സംവിധായകൻ ചിത്രം '{b}'?",
]

NFA_ACT_WHO = [
    "നാഷണൽ ഫിലിം അവാർഡ് {c}-ൽ '{b}'-ന് മികച്ച നടി?",
    "{c} NFA മികച്ച നടി '{b}'?",
]

NFF_WHO = [
    "നാഷണൽ ഫിലിം അവാർഡ് {c}-ൽ മികച്ച ചിത്രം '{b}'?",
    "{c} NFA മികച്ച ചിത്രം?",
]

PAD_WHO = [
    "{t} {y}-ൽ {f} മേഖലയിൽ ലഭിച്ചത്?",
    "{y} {t} {f} — ആരാണ്?",
]

PAD_YEAR = [
    "'{n}' {t} ലഭിച്ച വർഷം?",
]

PAD_FIELD = [
    "'{n}' {t} ലഭിച്ച മേഖല?",
]

PAD_TIER = [
    "'{n}' {y}-ൽ ലഭിച്ച പത്മ ബഹുമതി?",
]

IB_WHO = [
    "ഇന്റർനാഷണൽ ബുക്കർ പ്രൈസ് {c}-ൽ '{b}'-ന്?",
    "{c} ഇന്റർനാഷണൽ ബുക്കർ '{b}' — ആരാണ്?",
]

IB_BOOK = [
    "'{a}'-ന്റെ ഇന്റർനാഷണൽ ബുക്കർ വിജയ കൃതി?",
]

IB_YEAR = [
    "'{a}' ഇന്റർനാഷണൽ ബുക്കർ ലഭിച്ച വർഷം?",
]

GGB_WHO = [
    "{c}-ൽ '{b}'-ന് {a} ബഹുമതി?",
    "PSC: {c} {a} '{b}' — ആരാണ്/ഏത്?",
]

GGB_AWARD = [
    "'{a}'-ന് ബന്ധപ്പെട്ട {c} ബഹുമതി?",
]

YOUTH_WHO = [
    "'{b}' {c}-ൽ ലഭിച്ചത്?",
    "{c} '{b}' — ആരാണ്?",
]

YOUTH_AWARD = [
    "'{a}'-ന് ലഭിച്ച യുവ/ബ്രാവറി പുരസ്കാരം?",
]

SCI_WHO = [
    "{c}-ൽ {a} പുരസ്കാരം ലഭിച്ച ഇന്ത്യൻ ശാസ്ത്രജ്ഞൻ?",
    "PSC: {a} {c} — ആരാണ്?",
]

SCI_PRIZE = [
    "'{a}'-ന് ലഭിച്ച ശാസ്ത്ര പുരസ്കാരം?",
]

ORG_WHO = [
    "{c}-ൽ നോബൽ സമാധാന പുരസ്കാരം ലഭിച്ച സംഘടന?",
    "PSC: {c} നോബൽ സമാധാനം — ഏത് സംഘടന?",
]

ORG_YEAR = [
    "'{a}' നോബൽ സമാധാനം ലഭിച്ച വർഷം?",
]

EMIT_BODY = r'''
def _emit_prize_money(out, existing, rng):
    _emit_pairs(out, existing, rng, "പുരസ്കാര സമ്മാന തുകയിൽ ", PRIZE_MONEY, PAIR_AB, PAIR_BA)

def _emit_recipient_cap(out, existing, rng):
    _emit_pairs(out, existing, rng, "പുരസ്കാര പരിധിയിൽ ", RECIPIENT_CAP, CAP_AB, CAP_BA)

def _emit_medal_symbol(out, existing, rng):
    _emit_pairs(out, existing, rng, "പുരസ്കാര ചിഹ്നത്തിൽ ", MEDAL_SYMBOL, SYMBOL_AB, SYMBOL_BA)

def _emit_nobel_month(out, existing, rng):
    for a, b in NOBEL_MONTH:
        for tmpl in MONTH_AB:
            add_candidate(out, existing, rng, tmpl.format(a=a, b=b), b,
                _pool(MALAYALAM_MONTHS, b)[:3], "medium", pool=MALAYALAM_MONTHS)

def _emit_origin_country(out, existing, rng):
    _emit_pairs(out, existing, rng, "അന്താരാഷ്ട്ര പുരസ്കാരത്തിൽ ", ORIGIN_COUNTRY, COUNTRY_AB, None)

def _emit_ceremony_city(out, existing, rng):
    _emit_pairs(out, existing, rng, "പുരസ്കാര ചടങ്ങുകളിൽ ", CEREMONY_CITY, CITY_AB, None)

def _emit_jury_body(out, existing, rng):
    _emit_pairs(out, existing, rng, "പുരസ്കാര നിയമനത്തിൽ ", JURY_BODY, JURY_AB, JURY_BA)

def _emit_renaming(out, existing, rng):
    pool_new = list(dict.fromkeys(b for _, b, _ in RENAMING))
    pool_old = list(dict.fromkeys(a for a, _, _ in RENAMING))
    pool_yr = list(dict.fromkeys(c for _, _, c in RENAMING))
    _emit_triples(out, existing, rng, RENAMING, REN_AB, REN_AC, pool_new, pool_old)
    for a, b, c in RENAMING:
        add_candidate(out, existing, rng,
            f"'{a}' -> '{b}' പുനർനാമകരണം നടന്ന വർഷം?",
            c, _pool(pool_yr, c)[:3], "medium", pool=pool_yr)

def _emit_gallantry_hierarchy(out, existing, rng):
    facts = [(a, b, _pool([x[1] for x in GALLANTRY_HIERARCHY], b)[:6], "medium")
             for a, b in GALLANTRY_HIERARCHY]
    _emit(out, existing, rng, "വീരത ബഹുമതി ശ്രേണിയിൽ", facts)

def _emit_sangeet_natak(out, existing, rng):
    names = list(dict.fromkeys(a for a, _, _ in SANGEET_NATAK_WINNERS))
    fields = list(dict.fromkeys(b for _, b, _ in SANGEET_NATAK_WINNERS))
    years = list(dict.fromkeys(c for _, _, c in SANGEET_NATAK_WINNERS))
    _emit_triples(out, existing, rng, SANGEET_NATAK_WINNERS, SNA_WHO, SNA_FIELD, names, fields)
    _emit_triples(out, existing, rng, SANGEET_NATAK_WINNERS, SNA_YEAR, SNA_FIELD, years, fields)

def _emit_sna_fellowship(out, existing, rng):
    rows = [(a, str(b)) for a, b in SNA_FELLOWSHIP]
    _emit_pairs(out, existing, rng, "SNA ഫെലോഷിപ്പിൽ ", rows, FEL_WHO, FEL_YEAR)

def _emit_lalit_kala(out, existing, rng):
    names = list(dict.fromkeys(a for a, _, _ in LALIT_KALA))
    meds = list(dict.fromkeys(b for _, b, _ in LALIT_KALA))
    years = list(dict.fromkeys(c for _, _, c in LALIT_KALA))
    _emit_triples(out, existing, rng, LALIT_KALA, LK_WHO, LK_MED, names, meds)
    _emit_triples(out, existing, rng, LALIT_KALA, LK_YEAR, LK_MED, years, meds)

def _emit_moortidevi(out, existing, rng):
    names = list(dict.fromkeys(a for a, _, _ in MOORTIDEVI))
    works = list(dict.fromkeys(b for _, b, _ in MOORTIDEVI))
    years = list(dict.fromkeys(c for _, _, c in MOORTIDEVI))
    _emit_triples(out, existing, rng, MOORTIDEVI, MOOR_WHO, MOOR_WORK, names, works)
    _emit_triples(out, existing, rng, MOORTIDEVI, MOOR_YEAR, MOOR_WORK, years, works)

def _emit_nfa_categories(out, existing, rng):
    d_rows = [(a, b, str(c)) for a, b, c in NATIONAL_FILM_BEST_DIRECTOR]
    a_rows = [(a, b, str(c)) for a, b, c in NATIONAL_FILM_BEST_ACTRESS]
    f_rows = [(a, b, str(c)) for a, b, c in NATIONAL_FILM_BEST_FILM]
    for rows, who_t, film_t in [
        (d_rows, NFD_WHO, NFD_FILM),
        (a_rows, NFA_ACT_WHO, NFA_FILM),
        (f_rows, NFF_WHO, NFA_FILM),
    ]:
        names = list(dict.fromkeys(a for a, _, _ in rows))
        films = list(dict.fromkeys(b for _, b, _ in rows))
        years = list(dict.fromkeys(c for _, _, c in rows))
        _emit_triples(out, existing, rng, rows, who_t, film_t, names, films)
        _emit_triples(out, existing, rng, rows, NFA_YEAR, film_t, years, films)
    act_rows = [(a, b, str(c)) for a, b, c in NATIONAL_FILM_BEST_ACTOR]
    names = list(dict.fromkeys(a for a, _, _ in act_rows))
    films = list(dict.fromkeys(b for _, b, _ in act_rows))
    years = list(dict.fromkeys(c for _, _, c in act_rows))
    _emit_triples(out, existing, rng, act_rows, NFA_WHO, NFA_FILM, names, films)
    _emit_triples(out, existing, rng, act_rows, NFA_YEAR, NFA_FILM, years, films)

def _emit_padma(out, existing, rng):
    pool_names = list(dict.fromkeys(a for a, _, _, _ in PADMA_BHUSHAN_SHRI))
    pool_years = list(dict.fromkeys(b for _, b, _, _ in PADMA_BHUSHAN_SHRI))
    pool_fields = list(dict.fromkeys(c for _, _, c, _ in PADMA_BHUSHAN_SHRI))
    pool_tiers = list(dict.fromkeys(d for _, _, _, d in PADMA_BHUSHAN_SHRI))
    _emit_quads(out, existing, rng, PADMA_BHUSHAN_SHRI,
        PAD_WHO, PAD_YEAR, PAD_FIELD, PAD_TIER,
        pool_names, pool_years, pool_fields, pool_tiers)

def _emit_international_booker(out, existing, rng):
    names = list(dict.fromkeys(a for a, _, _ in INTERNATIONAL_BOOKER))
    books = list(dict.fromkeys(b for _, b, _ in INTERNATIONAL_BOOKER))
    years = list(dict.fromkeys(c for _, _, c in INTERNATIONAL_BOOKER))
    _emit_triples(out, existing, rng, INTERNATIONAL_BOOKER, IB_WHO, IB_BOOK, names, books)
    _emit_triples(out, existing, rng, INTERNATIONAL_BOOKER, IB_YEAR, IB_BOOK, years, books)

def _emit_golden_globe_bafta(out, existing, rng):
    names = list(dict.fromkeys(a for a, _, _ in GOLDEN_GLOBE_BAFTA))
    awards = list(dict.fromkeys(b for _, b, _ in GOLDEN_GLOBE_BAFTA))
    years = list(dict.fromkeys(c for _, _, c in GOLDEN_GLOBE_BAFTA))
    _emit_triples(out, existing, rng, GOLDEN_GLOBE_BAFTA, GGB_WHO, GGB_AWARD, names, awards)
    _emit_triples(out, existing, rng, GOLDEN_GLOBE_BAFTA, GGB_AWARD, GGB_WHO, awards, names)

def _emit_youth_awards(out, existing, rng):
    names = list(dict.fromkeys(a for a, _, _ in YOUTH_AWARDS))
    awards = list(dict.fromkeys(b for _, b, _ in YOUTH_AWARDS))
    years = list(dict.fromkeys(c for _, _, c in YOUTH_AWARDS))
    _emit_triples(out, existing, rng, YOUTH_AWARDS, YOUTH_WHO, YOUTH_AWARD, names, awards)
    _emit_triples(out, existing, rng, YOUTH_AWARDS, YOUTH_AWARD, YOUTH_WHO, awards, names)

def _emit_science_prizes(out, existing, rng):
    names = list(dict.fromkeys(a for a, _, _ in SCIENCE_PRIZES))
    prizes = list(dict.fromkeys(b for _, b, _ in SCIENCE_PRIZES))
    years = list(dict.fromkeys(c for _, _, c in SCIENCE_PRIZES))
    _emit_triples(out, existing, rng, SCIENCE_PRIZES, SCI_WHO, SCI_PRIZE, names, prizes)
    _emit_triples(out, existing, rng, SCIENCE_PRIZES, SCI_PRIZE, SCI_WHO, prizes, names)

def _emit_org_nobel_peace(out, existing, rng):
    orgs = list(dict.fromkeys(a for a, _ in ORG_NOBEL_PEACE))
    years = list(dict.fromkeys(str(b) for _, b in ORG_NOBEL_PEACE))
    for org, yr in ORG_NOBEL_PEACE:
        yr = str(yr)
        for tmpl in ORG_WHO:
            add_candidate(out, existing, rng, tmpl.format(a=org, b=org, c=yr), org,
                _pool(orgs, org)[:3], "medium", pool=orgs)
        for tmpl in ORG_YEAR:
            add_candidate(out, existing, rng, tmpl.format(a=org, b=org, c=yr), yr,
                _pool(years, yr)[:3], "medium", pool=years)

def _emit_imported_facts(out, existing, rng):
    br_names = list(dict.fromkeys(a for a, _ in BHARAT_RATNA))
    br_years = list(dict.fromkeys(str(b) for _, b in BHARAT_RATNA))
    for name, year in BHARAT_RATNA:
        add_candidate(out, existing, rng,
            f"{year}-ൽ ഭാരതരത്ന നേടിയത് ആരാണ്?",
            name, _pool(br_names, name)[:3], "medium", pool=br_names)
        add_candidate(out, existing, rng,
            f"ഭാരതരത്ന ലഭിച്ച '{name}'-ന്റെ വർഷം?",
            str(year), _pool(br_years, str(year))[:3], "hard", pool=br_years)
    jp_names = list(dict.fromkeys(a for a, _, _ in JNANPITH))
    jp_langs = list(dict.fromkeys(c for _, _, c in JNANPITH))
    for name, year, lang in JNANPITH:
        add_candidate(out, existing, rng,
            f"{year}-ൽ ജ്ഞാനപീഠ പുരസ്കാരം നേടിയത് ആരാണ്?",
            name, _pool(jp_names, name)[:3], "medium", pool=jp_names)
        add_candidate(out, existing, rng,
            f"'{name}' ജ്ഞാനപീഠ പുരസ്കാരം നേടിയ ഭാഷ?",
            lang, _pool(jp_langs, lang)[:3], "medium", pool=jp_langs)
    for award, inst, started, field in AWARD_METADATA:
        if award in DEFINITION_AWARDS:
            add_candidate(out, existing, rng,
                f"'{award}' എന്താണ്?",
                field, _pool(RANK_FIELDS, field)[:3], "medium", pool=RANK_FIELDS)
        else:
            sectors = ["ചലച്ചിത്രം", "സംഗീതം", "സാഹിത്യം", "ശാസ്ത്രം", "കായിക നേട്ടം", "ഗണിതശാസ്ത്രം"]
            add_candidate(out, existing, rng,
                f"'{award}' ഏത് മേഖലയിലെ പ്രധാന ബഹുമതിയാണ്?",
                field, _pool(sectors, field)[:3], "medium", pool=sectors)
    dp_names = list(dict.fromkeys(a for a, _ in DADASAHEB_PHALKE))
    for name, year in DADASAHEB_PHALKE:
        add_candidate(out, existing, rng,
            f"{year}-ൽ ദാദാസാഹേബ് ഫാൽക്കെ അവാർഡ് നേടിയത്?",
            name, _pool(dp_names, name)[:3], "medium", pool=dp_names)
    bk_authors = list(dict.fromkeys(a for a, _, _ in BOOKER_PRIZE))
    bk_books = list(dict.fromkeys(b for _, b, _ in BOOKER_PRIZE))
    for author, book, year in BOOKER_PRIZE:
        add_candidate(out, existing, rng,
            f"{year} ബുക്കർ പ്രൈസ് '{book}'-ന്?",
            author, _pool(bk_authors, author)[:3], "medium", pool=bk_authors)
        add_candidate(out, existing, rng,
            f"'{author}'-ന്റെ ബുക്കർ വിജയ കൃതി?",
            book, _pool(bk_books, book)[:3], "medium", pool=bk_books)
    nob_names = list(dict.fromkeys(a for a, _, _ in INDIAN_NOBEL))
    nob_cats = list(dict.fromkeys(b for _, b, _ in INDIAN_NOBEL))
    for name, cat, year in INDIAN_NOBEL:
        add_candidate(out, existing, rng,
            f"{year} ഇന്ത്യൻ നോബൽ ലോറിയേറ്റ് '{name}'-ന്റെ വിഭാഗം?",
            cat, _pool(nob_cats, cat)[:3], "medium", pool=nob_cats)
        add_candidate(out, existing, rng,
            f"നോബൽ {cat} {year}-ൽ ഇന്ത്യയിൽ നിന്ന്?",
            name, _pool(nob_names, name)[:3], "medium", pool=nob_names)

def _emit_all_categories(out, existing, rng):
    _emit_prize_money(out, existing, rng)
    _emit_recipient_cap(out, existing, rng)
    _emit_medal_symbol(out, existing, rng)
    _emit_nobel_month(out, existing, rng)
    _emit_origin_country(out, existing, rng)
    _emit_ceremony_city(out, existing, rng)
    _emit_jury_body(out, existing, rng)
    _emit_renaming(out, existing, rng)
    _emit_gallantry_hierarchy(out, existing, rng)
    _emit_sangeet_natak(out, existing, rng)
    _emit_sna_fellowship(out, existing, rng)
    _emit_lalit_kala(out, existing, rng)
    _emit_moortidevi(out, existing, rng)
    _emit_nfa_categories(out, existing, rng)
    _emit_padma(out, existing, rng)
    _emit_international_booker(out, existing, rng)
    _emit_golden_globe_bafta(out, existing, rng)
    _emit_youth_awards(out, existing, rng)
    _emit_science_prizes(out, existing, rng)
    _emit_org_nobel_peace(out, existing, rng)
    _emit_imported_facts(out, existing, rng)
'''


def main() -> None:
    data = build_all_data()
    parts = [HEADER]
    for name in sorted(data):
        parts.append(f"{name} = {pprint.pformat(data[name], width=120)}\n")
    for var in [
        "PAIR_AB", "PAIR_BA", "CAP_AB", "CAP_BA", "SYMBOL_AB", "SYMBOL_BA",
        "MONTH_AB", "COUNTRY_AB", "CITY_AB", "JURY_AB", "JURY_BA",
        "REN_AB", "REN_AC", "SNA_WHO", "SNA_FIELD", "SNA_YEAR",
        "FEL_WHO", "FEL_YEAR", "LK_WHO", "LK_MED", "LK_YEAR",
        "MOOR_WHO", "MOOR_WORK", "MOOR_YEAR",
        "NFA_WHO", "NFA_FILM", "NFA_YEAR", "NFD_WHO", "NFD_FILM",
        "NFA_ACT_WHO", "NFF_WHO",
        "PAD_WHO", "PAD_YEAR", "PAD_FIELD", "PAD_TIER",
        "IB_WHO", "IB_BOOK", "IB_YEAR", "GGB_WHO", "GGB_AWARD",
        "YOUTH_WHO", "YOUTH_AWARD", "SCI_WHO", "SCI_PRIZE",
        "ORG_WHO", "ORG_YEAR",
    ]:
        parts.append(f"{var} = {pprint.pformat(globals()[var], width=120)}\n")
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
