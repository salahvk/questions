#!/usr/bin/env python3
"""Generate economics_wave20_facts.py with 20 PSC categories — 2200+ unique stems."""

from __future__ import annotations

import pprint
import random
import textwrap
from pathlib import Path

OUT = Path(__file__).parent / "economics_wave20_facts.py"
MIN_COUNT = 2200

HEADER = textwrap.dedent('''
    #!/usr/bin/env python3
    """Wave 20 economics facts — 20 Malayalam PSC topic categories."""

    from __future__ import annotations

    import random

    from refill_common import Candidate, add_candidate, interleave_candidates

    Fact = tuple[str, str, list[str], str]


    def _pool(items: list[str], correct: str) -> list[str]:
        return [x for x in items if x != correct]


    def _emit_direct(
        out: list[Candidate],
        existing: set[str],
        rng: random.Random,
        facts: list[Fact],
    ) -> None:
        answers = list(dict.fromkeys(a for _, a, _, _ in facts))
        for stem, ans, wrong, diff in facts:
            add_candidate(out, existing, rng, stem, ans, wrong, diff, pool=answers)


    def _emit_pairs(
        out: list[Candidate],
        existing: set[str],
        rng: random.Random,
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
                    tmpl.format(a=a, b=b),
                    b, _pool(bs, b)[:3], diff, pool=bs,
                )
            if templates_ba:
                for tmpl in templates_ba:
                    add_candidate(
                        out, existing, rng,
                        tmpl.format(a=a, b=b),
                        a, _pool(as_, a)[:3], diff, pool=as_,
                    )


    def _emit_person_work(
        out: list[Candidate],
        existing: set[str],
        rng: random.Random,
        rows: list[tuple[str, str, str]],
        who_templates: list[str],
        work_templates: list[str],
        pool_persons: list[str],
        pool_works: list[str],
        diff: str = "medium",
    ) -> None:
        for person, work, field in rows:
            for tmpl in who_templates:
                add_candidate(
                    out, existing, rng,
                    tmpl.format(person=person, work=work, field=field),
                    person, _pool(pool_persons, person)[:3], diff, pool=pool_persons,
                )
            for tmpl in work_templates:
                add_candidate(
                    out, existing, rng,
                    tmpl.format(person=person, work=work, field=field),
                    work, _pool(pool_works, work)[:3], diff, pool=pool_works,
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

# Pair templates for institution-sector / org-function
PAIR_AB = [
    "ഇന്ത്യൻ സാമ്പത്തിക സ്ഥാപനങ്ങളിൽ '{a}' ഏത് മേഖലയുമായി പ്രധാനമായും ബന്ധപ്പെട്ടിരിക്കുന്നു?",
    "'{a}' ഏത് സാമ്പത്തിക മേഖലയുടെ പ്രധാന സ്ഥാപനമാണ്?",
    "PSC സാമ്പത്തിക വിജ്ഞാനത്തിൽ '{a}'-യുമായി ബന്ധപ്പെട്ട മേഖല ഏത്?",
]
PAIR_BA = [
    "{b} മേഖലയുടെ പ്രധാന നിയന്ത്രണ/സഹായ സ്ഥാപനം ഏത്?",
    "{b} മേഖലയുമായി ബന്ധപ്പെട്ട പ്രധാന സ്ഥാപനം ഏത്?",
    "ഇന്ത്യയിൽ {b} മേഖലയുടെ പ്രധാന സ്ഥാപനം ഏത്?",
]

WHO_T = [
    "സാമ്പത്തിക ശാസ്ത്രത്തിൽ '{work}' രചിച്ചത് ആരാണ്?",
    "'{work}' ഏത് സാമ്പത്തിക ശാസ്ത്രജ്ഞന്റെ രചനയാണ്?",
    "PSC സാമ്പത്തിക ചരിത്രത്തിൽ '{work}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി ആരാണ്?",
]
WORK_T = [
    "സാമ്പത്തിക ശാസ്ത്രജ്ഞൻ {person} ഏത് പ്രധാന രചന/സിദ്ധാന്തവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
    "{person} ഏത് സാമ്പത്തിക ഗ്രന്ഥവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
]

EMIT_BODY = r'''
def _emit_macro_indicators(out, existing, rng):
    _emit_direct(out, existing, rng, MACRO_INDICATORS)

def _emit_rbi_monetary(out, existing, rng):
    _emit_direct(out, existing, rng, RBI_MONETARY)

def _emit_plans_niti(out, existing, rng):
    _emit_direct(out, existing, rng, PLANS_NITI)

def _emit_reforms_1991(out, existing, rng):
    _emit_direct(out, existing, rng, REFORMS_1991)

def _emit_finance_commission(out, existing, rng):
    _emit_direct(out, existing, rng, FINANCE_COMMISSION)

def _emit_bop_trade(out, existing, rng):
    _emit_direct(out, existing, rng, BOP_TRADE)

def _emit_intl_institutions(out, existing, rng):
    _emit_direct(out, existing, rng, INTL_INSTITUTIONS)
    _emit_pairs(out, existing, rng, INTL_HQ, PAIR_AB, PAIR_BA)

def _emit_kerala_economy(out, existing, rng):
    _emit_direct(out, existing, rng, KERALA_ECONOMY)

def _emit_microeconomics(out, existing, rng):
    _emit_direct(out, existing, rng, MICROECONOMICS)

def _emit_market_structures(out, existing, rng):
    _emit_direct(out, existing, rng, MARKET_STRUCTURES)

def _emit_inflation_cycles(out, existing, rng):
    _emit_direct(out, existing, rng, INFLATION_CYCLES)

def _emit_fiscal_deficit(out, existing, rng):
    _emit_direct(out, existing, rng, FISCAL_DEFICIT)

def _emit_agriculture_food(out, existing, rng):
    _emit_direct(out, existing, rng, AGRICULTURE_FOOD)
    _emit_pairs(out, existing, rng, AGRI_INST, PAIR_AB, PAIR_BA)

def _emit_labour_employment(out, existing, rng):
    _emit_direct(out, existing, rng, LABOUR_EMPLOYMENT)

def _emit_capital_markets(out, existing, rng):
    _emit_direct(out, existing, rng, CAPITAL_MARKETS)

def _emit_insurance_pension(out, existing, rng):
    _emit_direct(out, existing, rng, INSURANCE_PENSION)
    _emit_pairs(out, existing, rng, INSURANCE_INST, PAIR_AB, PAIR_BA)

def _emit_economic_thinkers(out, existing, rng):
    persons = list(dict.fromkeys(p for p, _, _ in ECONOMIC_THINKERS))
    works = list(dict.fromkeys(w for _, w, _ in ECONOMIC_THINKERS))
    _emit_person_work(out, existing, rng, ECONOMIC_THINKERS, WHO_T, WORK_T, persons, works)
    _emit_direct(out, existing, rng, THINKER_EXTRA)

def _emit_industrial_sez(out, existing, rng):
    _emit_direct(out, existing, rng, INDUSTRIAL_SEZ)

def _emit_public_finance_tax(out, existing, rng):
    _emit_direct(out, existing, rng, PUBLIC_FINANCE_TAX)

def _emit_digital_consumer(out, existing, rng):
    _emit_direct(out, existing, rng, DIGITAL_CONSUMER)

def _emit_all_categories(out, existing, rng):
    _emit_macro_indicators(out, existing, rng)
    _emit_rbi_monetary(out, existing, rng)
    _emit_plans_niti(out, existing, rng)
    _emit_reforms_1991(out, existing, rng)
    _emit_finance_commission(out, existing, rng)
    _emit_bop_trade(out, existing, rng)
    _emit_intl_institutions(out, existing, rng)
    _emit_kerala_economy(out, existing, rng)
    _emit_microeconomics(out, existing, rng)
    _emit_market_structures(out, existing, rng)
    _emit_inflation_cycles(out, existing, rng)
    _emit_fiscal_deficit(out, existing, rng)
    _emit_agriculture_food(out, existing, rng)
    _emit_labour_employment(out, existing, rng)
    _emit_capital_markets(out, existing, rng)
    _emit_insurance_pension(out, existing, rng)
    _emit_economic_thinkers(out, existing, rng)
    _emit_industrial_sez(out, existing, rng)
    _emit_public_finance_tax(out, existing, rng)
    _emit_digital_consumer(out, existing, rng)
'''

# Import partial data already written + generate rest programmatically
from build_economics_wave20_data import (
    MACRO_INDICATORS,
    RBI_MONETARY,
    PLANS_NITI,
    REFORMS_1991,
)
