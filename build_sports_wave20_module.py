#!/usr/bin/env python3
"""Build sports_wave20_facts.py — 20 Malayalam PSC sports categories, 4600+ stems."""

from __future__ import annotations

import importlib.util
import pprint
import random
import textwrap
from pathlib import Path

OUT = Path(__file__).parent / "sports_wave20_facts.py"
MIN_COUNT = 4600

HEADER = textwrap.dedent("""
    #!/usr/bin/env python3
    \"\"\"Wave 20 sports facts — 20 Malayalam PSC topic categories.\"\"\"

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
        # rows = (person, event/milestone, detail). who->person, event->b, detail->c.
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
    "കായികനിയന്ത്രണത്തിൽ '{a}' ഏത് കായിക ഇനവുമായി ബന്ധപ്പെട്ടതാണ്?",
    "'{a}' നിയന്ത്രിക്കുന്ന പ്രധാന കായിക ഇനം ഏത്?",
    "'{a}' ഏത് കായിക ഇനത്തിന്റെ അന്താരാഷ്ട്ര/ദേശീയ സംഘടനയാണ്?",
    "PSC കായിക വിജ്ഞാനത്തിൽ '{a}'-യുമായി ബന്ധപ്പെട്ട കായിക ഇനം?",
    "'{a}' ഏത് കായിക മേഖലയുമായി ബന്ധപ്പെട്ട സംഘടനയാണ്?",
    "കായിക സംഘടന '{a}' ഏത് ഇനത്തെ നിയന്ത്രിക്കുന്നു?",
    "'{a}' ഏത് കായിക ഇനവുമായി ബന്ധപ്പെട്ട അധികാര സംഘടനയാണ്?",
]
PAIR_AB_INDIAN = [
    "'{a}' ഏത് കായിക ഇനവുമായി ബന്ധപ്പെട്ട ഭാരതീയ സംഘടനയാണ്?",
]
PAIR_BA_NEUTRAL = [
    "{b} കായിക ഇനത്തിന്റെ പ്രധാന നിയന്ത്രണ സംഘടന ഏത്?",
    "{b} കായിക ഇനവുമായി ബന്ധപ്പെട്ട സംഘടന ഏത്?",
    "{b} നിയന്ത്രിക്കുന്ന സംഘടന ഏത്?",
]
PAIR_BA_INDIAN = [
    "{b} കായികത്തിലെ ഭാരതീയ അധികാര സംഘടന ഏത്?",
]
PAIR_BA_INTL = [
    "{b} കായിക ഇനവുമായി ബന്ധപ്പെട്ട അന്താരാഷ്ട്ര സംഘടന ഏത്?",
]


from build_sports_data import build_all_data

EMIT_BODY = r'''
def _emit_governing_bodies(out, existing, rng):
    indian_rows = [(a, b) for a, b in GOV_BODY_SPORT if is_indian_gov_org(a)]
    intl_rows = [(a, b) for a, b in GOV_BODY_SPORT if not is_indian_gov_org(a)]
    _emit_pairs(out, existing, rng, "", indian_rows, PAIR_AB + PAIR_AB_INDIAN, PAIR_BA_NEUTRAL + PAIR_BA_INDIAN)
    _emit_pairs(out, existing, rng, "", intl_rows, PAIR_AB, PAIR_BA_NEUTRAL + PAIR_BA_INTL)

def _emit_first_indian(out, existing, rng):
    milestones = list(dict.fromkeys(b for _, b, _ in FIRST_INDIAN))
    details = list(dict.fromkeys(c for _, _, c in FIRST_INDIAN))
    persons = list(dict.fromkeys(a for a, _, _ in FIRST_INDIAN))
    _emit_person_event(out, existing, rng, FIRST_INDIAN,
        ["ഇന്ത്യൻ കായിക ചരിത്രത്തിൽ {b} സംബന്ധിച്ച പ്രധാന വ്യക്തി ആരാണ്?",
         "{b} നേട്ടവുമായി ബന്ധപ്പെട്ട ഇന്ത്യൻ കായിക താരം ആരാണ്?",
         "PSC കായിക ചരിത്രത്തിൽ {b} — ആരുടെ നേട്ടമാണ്?"],
        ["{a} ഏത് കായിക നേട്ടവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
         "{a} ഏത് കായിക ഇവന്റുമായി ബന്ധപ്പെട്ട പ്രശസ്ത നേട്ടം?",
         "ഇന്ത്യൻ കായിക താരം {a} ഏത് നേട്ടവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"],
        ["ഇന്ത്യൻ കായിക ചരിത്രത്തിൽ {b} സംബന്ധിച്ച വിവരം?",
         "{b} സംബന്ധിച്ച പ്രധാന കായിക വിവരം?"],
        persons, milestones, details)
    for person, milestone, detail in FIRST_INDIAN:
        add_candidate(out, existing, rng,
            f"ഇന്ത്യൻ കായിക ചരിത്രത്തിൽ {milestone} സംബന്ധിച്ച വിവരം?",
            detail, _pool(details, detail)[:3], "medium", pool=details)
        add_candidate(out, existing, rng,
            f"{milestone} നേട്ടം കൈവരിച്ച ഇന്ത്യൻ കായിക താരം ആരാണ്?",
            person, _pool(persons, person)[:3], "medium", pool=persons)
        add_candidate(out, existing, rng,
            f"ഇന്ത്യൻ കായിക താരം {person} ഏത് നേട്ടവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
            milestone, _pool(milestones, milestone)[:3], "medium", pool=milestones)

def _emit_hockey_wc(out, existing, rng):
    _emit_pairs(out, existing, rng, "ഹോക്കി ലോകകപ്പിൽ ", HOCKEY_WC_HOST,
        ["{a} ആതിഥ്യം വഹിച്ച നഗരം/രാജ്യം?", "{a} നടന്ന വേദി?", "{a} ആതിഥ്യ വേദി?", "{a} സംഘടിപ്പിച്ച നഗരം?"],
        ["{b} ഹോക്കി ലോകകപ്പ് ആതിഥ്യം വഹിച്ച വർഷം/പതിപ്പ്?", "{b} ഹോക്കി ലോകകപ്പ് ആതിഥ്യ പതിപ്പ്?"])
    _emit_pairs(out, existing, rng, "ഹോക്കി ലോകകപ്പിൽ ", HOCKEY_WC_WINNER,
        ["{a} വിജയിച്ച രാജ്യം?", "{a} ചാമ്പ്യൻ?", "{a} കപ്പ് നേടിയ രാജ്യം?", "{a} വിജയി രാജ്യം?"],
        ["{b} ഹോക്കി ലോകകപ്പ് വിജയിച്ച വർഷം/പതിപ്പ്?", "{b} ഹോക്കി ലോകകപ്പ് വിജയ പതിപ്പ്?"])
    _emit_pairs(out, existing, rng, "ഹോക്കി ചാമ്പ്യൻസ് ട്രോഫിയിൽ ", HOCKEY_CT,
        ["{a} വിജയി?", "{a} നേടിയ രാജ്യം?"],
        ["{b} ഹോക്കി ചാമ്പ്യൻസ് ട്രോഫി വിജയിച്ച വർഷം?"])

def _emit_kabaddi(out, existing, rng):
    _emit(out, existing, rng, "കബഡി നിയമങ്ങളിൽ", KABADDI_RULES)
    _emit_pairs(out, existing, rng, "പ്രോ കബഡി ലീഗിൽ ", PKL_TEAMS,
        ["{a} ഏത് നഗരത്തെ പ്രതിനിധീകരിക്കുന്നു?", "PKL ടീം {a} ഏത് നഗരവുമായി ബന്ധപ്പെട്ടതാണ്?",
         "{a} ഏത് നഗരത്തിലെ PKL ഫ്രാഞ്ചൈസിയാണ്?"],
        ["{b} നഗരത്തെ PKL-ൽ പ്രതിനിധീകരിക്കുന്ന ടീം?"])

def _emit_shooting_archery(out, existing, rng):
    sp = list(dict.fromkeys(a for a, _, _ in SHOOTING_MEDALS))
    se = list(dict.fromkeys(b for _, b, _ in SHOOTING_MEDALS))
    sm = list(dict.fromkeys(c for _, _, c in SHOOTING_MEDALS))
    _emit_person_event(out, existing, rng, SHOOTING_MEDALS,
        ["{b} ഒളിമ്പിക് മെഡൽ നേടിയ ഇന്ത്യൻ ഷൂട്ടർ ആരാണ്?", "{b} ഇവന്റിൽ ഒളിമ്പിക് മെഡൽ നേടിയ ഇന്ത്യൻ താരം?"],
        ["{a} ഏത് ഒളിമ്പിക് ഷൂട്ടിംഗ് ഇവന്റിൽ മെഡൽ നേടി?", "{a} ഏത് ഒളിമ്പിക് ഇവന്റുമായി ബന്ധപ്പെട്ട മെഡൽ നേട്ടം?"],
        ["{b} ഒളിമ്പിക് മെഡൽ നേടിയ ഇന്ത്യൻ ഷൂട്ടറിന്റെ മെഡൽ വിഭാഗം?"],
        sp, se, sm)
    ap = list(dict.fromkeys(a for a, _, _ in ARCHERY_MEDALS))
    ae = list(dict.fromkeys(b for _, b, _ in ARCHERY_MEDALS))
    am = list(dict.fromkeys(c for _, _, c in ARCHERY_MEDALS))
    _emit_person_event(out, existing, rng, ARCHERY_MEDALS,
        ["{b} ഒളിമ്പിക് മെഡൽ നേടിയ ഇന്ത്യൻ വില്ലുവെട്ട് താരം ആരാണ്?", "{b} ഇവന്റിൽ മെഡൽ നേടിയ ഇന്ത്യൻ വില്ലുവെട്ട് താരം?"],
        ["{a} ഏത് ഒളിമ്പിക് വില്ലുവെട്ട് ഇവന്റിൽ മെഡൽ നേടി?", "{a} ഏത് ഇവന്റുമായി ബന്ധപ്പെട്ട വില്ലുവെട്ട് മെഡൽ?"],
        None, ap, ae, am)

def _emit_wrestling_boxing(out, existing, rng):
    wp = list(dict.fromkeys(a for a, _, _ in WRESTLING_OLY))
    we = list(dict.fromkeys(b for _, b, _ in WRESTLING_OLY))
    wm = list(dict.fromkeys(c for _, _, c in WRESTLING_OLY))
    _emit_person_event(out, existing, rng, WRESTLING_OLY,
        ["{b} ഒളിമ്പിക് മല്ലയുദ്ധ ഇവന്റ് — പ്രധാന ഇന്ത്യൻ മെഡലിസ്റ്റ്?", "{b} ഭാരവിഭാഗത്തിൽ ഒളിമ്പിക് മെഡൽ നേടിയ ഇന്ത്യൻ മല്ലയുദ്ധക്കാരൻ?"],
        ["{a} ഏത് ഒളിമ്പിക് മല്ലയുദ്ധ ഭാരവിഭാഗത്തിൽ മെഡൽ നേടി?", "{a} ഏത് ഭാരവിഭാഗ/ഇവന്റുമായി ബന്ധപ്പെട്ട മെഡൽ?"],
        None, wp, we, wm)
    bp = list(dict.fromkeys(a for a, _, _ in BOXING_OLY))
    be = list(dict.fromkeys(b for _, b, _ in BOXING_OLY))
    bm = list(dict.fromkeys(c for _, _, c in BOXING_OLY))
    _emit_person_event(out, existing, rng, BOXING_OLY,
        ["{b} ഒളിമ്പിക് ബോക്സിംഗ് ഇവന്റ് — പ്രധാന ഇന്ത്യൻ മെഡലിസ്റ്റ്?", "{b} ഭാരവിഭാഗത്തിൽ ഒളിമ്പിക് ബോക്സിംഗ് മെഡൽ?"],
        ["{a} ഏത് ഒളിമ്പിക് ബോക്സിംഗ് ഭാരവിഭാഗത്തിൽ മെഡൽ നേടി?", "{a} ഏത് ബോക്സിംഗ് ഇവന്റുമായി ബന്ധപ്പെട്ട മെഡൽ?"],
        None, bp, be, bm)

def _emit_chess_fide(out, existing, rng):
    _emit_pairs(out, existing, rng, "ചെസ്സിൽ ", CHESS_TITLES,
        ["{a} ചെസ്സ് ശീർഷകം/ബഹുമതി ഏത് താരവുമായി ബന്ധപ്പെട്ടതാണ്?", "{a} — ചെസ്സ് ചരിത്രത്തിൽ പ്രധാന വ്യക്തി?"],
        ["{b} നേടിയ/സംബന്ധിച്ച ചെസ്സ് ശീർഷകം/ബഹുമതി?"])
    _emit(out, existing, rng, "FIDE-യിൽ", FIDE_FACTS, function_entity="ചെസ്സ് നിയമം")

def _emit_domestic_cricket(out, existing, rng):
    _emit_pairs(out, existing, rng, "ഇന്ത്യൻ ക്രിക്കറ്റിൽ ", CRICKET_TROPHIES,
        ["{a} ഏത് ക്രിക്കറ്റ് ട്രോഫി/കപ്പ്?", "{a} ഏത് ദേശീയ ക്രിക്കറ്റ് മത്സരവുമായി ബന്ധപ്പെട്ടതാണ്?",
         "{a} ഏത് ക്രിക്കറ്റ് ടൂർണമെന്റുമായി ബന്ധപ്പെട്ടതാണ്?", "{a} ഏത് ട്രോഫി/കപ്പുമായി ബന്ധപ്പെട്ടതാണ്?"],
        ["{b} ഏത് ക്രിക്കറ്റ് ട്രോഫിയുടെ/കപ്പിന്റെ പേര്?", "{b} ഏത് ട്രോഫിയുടെ പേര്?"])

def _emit_bilateral_trophies(out, existing, rng):
    _emit_pairs(out, existing, rng, "അന്താരാഷ്ട്ര ക്രിക്കറ്റിൽ ", BILATERAL_TROPHIES,
        ["{a} ഏത് രണ്ട് രാജ്യങ്ങൾക്കിടയിലെ ക്രിക്കറ്റ് ട്രോഫി?", "{a} ഏത് ബൈലാറ്ററൽ ക്രിക്കറ്റ് പരമ്പരയുമായി ബന്ധപ്പെട്ടതാണ്?"],
        ["{b} ഏത് ബൈലാറ്ററൽ ക്രിക്കറ്റ് ട്രോഫിയുടെ പേര്?"])

def _emit_stadiums(out, existing, rng):
    _emit_pairs(out, existing, rng, "കായിക സ്റ്റേഡിയങ്ങളിൽ ", STADIUM_CITY,
        ["{a} ഏത് നഗരത്തിലാണ് സ്ഥിതി ചെയ്യുന്നത്?", "{a} സ്റ്റേഡിയം ഏത് നഗരവുമായി ബന്ധപ്പെട്ടതാണ്?",
         "{a} ഏത് നഗരത്തിലെ പ്രധാന കായിക സ്റ്റേഡിയമാണ്?", "{a} സ്ഥിതി ചെയ്യുന്ന നഗരം?"],
        ["{b} നഗരത്തിലെ പ്രശസ്ത കായിക സ്റ്റേഡിയം?", "{b} നഗരത്തിലെ പ്രധാന സ്റ്റേഡിയം?"])
    _emit_pairs(out, existing, rng, "കായിക സ്റ്റേഡിയങ്ങളിൽ ", STADIUM_NICK,
        ["{a} സ്റ്റേഡിയത്തിന്റെ വിളിപ്പേര്/പേരുകേട്ട പേര്?", "{a} ഏത് സ്റ്റേഡിയത്തിന്റെ അപരനാമമാണ്?"],
        ["{b} വിളിപ്പേരുള്ള സ്റ്റേഡിയം?"])

def _emit_player_counts(out, existing, rng):
    facts = []
    for sport, n, wrong in PLAYER_COUNTS:
        facts.append((f"{sport} ഒരു ടീമിലെ കളിക്കാരുടെ എണ്ണം", n, wrong, "easy"))
        facts.append((f"{sport} ടീമിൽ മൈതാനത്ത് കളിക്കാവുന്ന പരമാവധി കളിക്കാർ", n, wrong, "medium"))
        facts.append((f"{sport} മത്സരത്തിൽ ഒരു ടീമിലെ കളിക്കാരുടെ എണ്ണം", n, wrong, "easy"))
        facts.append((f"{sport} ടീമിലെ സാധാരണ കളിക്കാരുടെ എണ്ണം", n, wrong, "medium"))
    _emit(out, existing, rng, "കായിക നിയമങ്ങളിൽ", facts)

def _emit_scoring_terms(out, existing, rng):
    _emit(out, existing, rng, "കായിക സ്കോറിംഗിൽ", SCORING_TERMS, function_entity="കായിക പദം")
    _emit_pairs(out, existing, rng, "കായിക സ്കോറിംഗിൽ ", SCORING_SPORT,
        ["{a} ഏത് കായിക ഇനവുമായി ബന്ധപ്പെട്ട സ്കോറിംഗ് പദമാണ്?", "{a} ഏത് കളിയിലെ സ്കോറിംഗ്/പദപ്രയോഗമാണ്?"],
        ["{b} കായിക ഇനത്തിലെ സ്കോറിംഗ് പദം/പ്രയോഗം?"])

def _emit_penalty_cards(out, existing, rng):
    _emit(out, existing, rng, "കായിക നിയമങ്ങളിൽ", PENALTY_RULES)
    _emit_pairs(out, existing, rng, "കായിക നിയമങ്ങളിൽ ", CARD_SPORTS,
        ["{a} ഏത് കായിക ഇനവുമായി ബന്ധപ്പെട്ട കാർഡ്/പെനാൽറ്റി നിയമമാണ്?", "{a} ഏത് കളിയിലെ റെഡ്/യെല്ലോ കാർഡ്/പെനാൽറ്റി?"],
        ["{b} കായിക ഇനത്തിലെ കാർഡ്/പെനാൽറ്റി നിയമം?"])

def _emit_womens_leagues(out, existing, rng):
    _emit_pairs(out, existing, rng, "വനിതാ കായിക ലീഗുകളിൽ ", WOMENS_LEAGUES,
        ["{a} ഏത് കായിക ഇനവുമായി ബന്ധപ്പെട്ട വനിതാ ലീഗാണ്?", "{a} ഏത് വനിതാ പ്രൊഫഷണൽ ലീഗാണ്?"],
        ["{b} കായിക ഇനത്തിലെ വനിതാ ലീഗ്?"])

def _emit_cwg_asian(out, existing, rng):
    _emit_pairs(out, existing, rng, "കോമൺവെൽത്ത്/ഏഷ്യൻ ഗെയിമ്സിൽ ", CWG_ASIAN,
        ["{a} മേള/പതിപ്പ് — ഇന്ത്യയുമായി ബന്ധപ്പെട്ട പ്രധാന വിവരം?", "{a} സംബന്ധിച്ച ഇന്ത്യൻ കായിക വിവരം?",
         "{a} മേളയുമായി ബന്ധപ്പെട്ട വിവരം?", "{a} — ഇന്ത്യൻ കായിക മേളാ വിവരം?"],
        ["{b} സംബന്ധിച്ച മേള/പതിപ്പ്?", "{b} മേളയുടെ പതിപ്പ്/വർഷം?"])
    _emit_triples(out, existing, rng, CWG_ASIAN_MEDALS,
        ["{b} മേളയിൽ ഇന്ത്യ നേടിയ പ്രധാന മെഡൽ/നേട്ടം — ഏത് ഇവന്റ്?", "{b} ഇന്ത്യയുടെ മേളാ നേട്ടവുമായി ബന്ധപ്പെട്ട ഇവന്റ്?"],
        ["{a} ഏത് മേളയിൽ/വർഷത്തിൽ ഇന്ത്യ ഈ നേട്ടം കൈവരിച്ചു?", "{a} ഏത് മേളവുമായി ബന്ധപ്പെട്ട ഇന്ത്യൻ നേട്ടം?"],
        list(dict.fromkeys(b for _, b, _ in CWG_ASIAN_MEDALS)), list(dict.fromkeys(c for _, _, c in CWG_ASIAN_MEDALS)))

def _emit_paralympics(out, existing, rng):
    pp = list(dict.fromkeys(a for a, _, _ in PARALYMPIC_MEDALS))
    pe = list(dict.fromkeys(b for _, b, _ in PARALYMPIC_MEDALS))
    pm = list(dict.fromkeys(c for _, _, c in PARALYMPIC_MEDALS))
    _emit_person_event(out, existing, rng, PARALYMPIC_MEDALS,
        ["{b} പാരാലിമ്പിക് മെഡൽ നേടിയ ഇന്ത്യൻ താരം ആരാണ്?", "{b} ഇവന്റിൽ പാരാലിമ്പിക് മെഡൽ നേടിയ ഇന്ത്യൻ താരം?"],
        ["{a} ഏത് പാരാലിമ്പിക് ഇവന്റിൽ മെഡൽ നേടി?", "{a} ഏത് ഇവന്റുമായി ബന്ധപ്പെട്ട പാരാലിമ്പിക് മെഡൽ?"],
        None, pp, pe, pm)
    _emit(out, existing, rng, "പാരാലിമ്പിക്സിൽ", PARALYMPIC_FACTS)

def _emit_winter_olympics(out, existing, rng):
    wp = list(dict.fromkeys(a for a, _, _ in WINTER_INDIA))
    we = list(dict.fromkeys(b for _, b, _ in WINTER_INDIA))
    wm = list(dict.fromkeys(c for _, _, c in WINTER_INDIA))
    _emit_person_event(out, existing, rng, WINTER_INDIA,
        ["{b} ശീതകാല ഒളിമ്പിക്സ് ഇവന്റ് — ഇന്ത്യയുടെ പ്രതിനിധി?", "{b} ഇവന്റിൽ ഇന്ത്യ പ്രതിനിധീകരിച്ച താരം?"],
        ["{a} ഏത് ശീതകാല ഒളിമ്പിക് ഇവന്റിൽ ഇന്ത്യ പ്രതിനിധീകരിച്ചു?", "{a} ഏത് ഇവന്റുമായി ബന്ധപ്പെട്ട ശീതകാല ഒളിമ്പിക് പ്രതിനിധിത്വം?"],
        None, wp, we, wm)
    _emit(out, existing, rng, "ശീതകാല ഒളിമ്പിക്സിൽ", WINTER_FACTS)

def _emit_motorsport(out, existing, rng):
    _emit_pairs(out, existing, rng, "മോട്ടോർസ്പോർട്ടിൽ ", F1_FACTS,
        ["{a} — ഫോർമുലാ വൺ/മോട്ടോർസ്പോർട്ട് വിവരം?", "{a} സംബന്ധിച്ച പ്രധാന വിവരം?"],
        ["{b} സംബന്ധിച്ച ടീം/ട്രാക്ക്/വിവരം?"])
    _emit(out, existing, rng, "മോട്ടോർസ്പോർട്ടിൽ", MOTORSPORT_TERMS)

def _emit_kerala_traditional(out, existing, rng):
    _emit(out, existing, rng, "കേരളത്തിലെ പാരമ്പര്യ കായികങ്ങളിൽ", KERALA_SPORTS)
    _emit_pairs(out, existing, rng, "കേരളത്തിലെ പാരമ്പര്യ കായികങ്ങളിൽ ", KERALA_SPORT_EVENT,
        ["{a} ഏത് കായിക ഇനവുമായി ബന്ധപ്പെട്ടതാണ്?", "{a} ഏത് പാരമ്പര്യ കായിക മേഖലയുമായി ബന്ധപ്പെട്ടതാണ്?"],
        ["{b} കായിക ഇനത്തിലെ കേരള പാരമ്പര്യ വിവരം?"])

def _emit_policy_schemes(out, existing, rng):
    _emit(out, existing, rng, "കായിക നയത്തിലും പദ്ധതികളിലും", POLICY_SCHEMES)
    _emit_pairs(out, existing, rng, "കായിക പദ്ധതികളിൽ ", AWARD_POLICY,
        ["{a} ഏതിനാണ് നൽകുന്നത്/ഏതുമായി ബന്ധപ്പെട്ടതാണ്?", "{a} കായിക പുരസ്കാരം/പദ്ധതിയുടെ പ്രധാന ലക്ഷ്യം?"],
        ["{b} ലക്ഷ്യമുള്ള കായിക പുരസ്കാരം/പദ്ധതി?"])

def _emit_all_categories(out, existing, rng):
    _emit_governing_bodies(out, existing, rng)
    _emit_first_indian(out, existing, rng)
    _emit_hockey_wc(out, existing, rng)
    _emit_kabaddi(out, existing, rng)
    _emit_shooting_archery(out, existing, rng)
    _emit_wrestling_boxing(out, existing, rng)
    _emit_chess_fide(out, existing, rng)
    _emit_domestic_cricket(out, existing, rng)
    _emit_bilateral_trophies(out, existing, rng)
    _emit_stadiums(out, existing, rng)
    _emit_player_counts(out, existing, rng)
    _emit_scoring_terms(out, existing, rng)
    _emit_penalty_cards(out, existing, rng)
    _emit_womens_leagues(out, existing, rng)
    _emit_cwg_asian(out, existing, rng)
    _emit_paralympics(out, existing, rng)
    _emit_winter_olympics(out, existing, rng)
    _emit_motorsport(out, existing, rng)
    _emit_kerala_traditional(out, existing, rng)
    _emit_policy_schemes(out, existing, rng)
'''


def main() -> None:
    data = build_all_data()
    parts = [HEADER]
    for name in sorted(data):
        parts.append(f"{name} = {pprint.pformat(data[name], width=120)}\n")
    parts.append(f"PAIR_AB = {pprint.pformat(PAIR_AB, width=120)}\n")
    parts.append(f"PAIR_AB_INDIAN = {pprint.pformat(PAIR_AB_INDIAN, width=120)}\n")
    parts.append(f"PAIR_BA_NEUTRAL = {pprint.pformat(PAIR_BA_NEUTRAL, width=120)}\n")
    parts.append(f"PAIR_BA_INDIAN = {pprint.pformat(PAIR_BA_INDIAN, width=120)}\n")
    parts.append(f"PAIR_BA_INTL = {pprint.pformat(PAIR_BA_INTL, width=120)}\n")
    parts.append("from sports_gov_utils import is_indian_gov_org\n")
    parts.append(EMIT_BODY)
    parts.append(FOOTER)
    source = "\n".join(parts)

    test_path = OUT.parent / "_sw20_count_test.py"
    test_path.write_text(source, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("sw20t", test_path)
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
