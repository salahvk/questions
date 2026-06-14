#!/usr/bin/env python3
"""Generate coi_wave20_facts.py from verified constitution data."""

from __future__ import annotations

import pprint
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "coi_wave20_facts.py"

HEADER = '''#!/usr/bin/env python3
"""Wave 20 Indian Constitution facts — 20 PSC topic categories."""

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

EMIT = '''
def _emit_all(out: list[Candidate], existing: set[str], rng: random.Random) -> None:
    part_subjects = list({b for _, b in PARTS})
    part_names = list({a for a, _ in PARTS})
    _pairs(
        out, existing, rng, PARTS,
        [
            "'{a}'-ന്റെ വിഷയം/ഉള്ളടക്കം?",
            "ഭരണഘടനയിലെ '{a}' എന്തിനെ കുറിക്കുന്നു?",
            "'{a}'-ൽ പ്രധാനമായി ഉൾപ്പെടുന്നത്?",
            "'{a}'-ന്റെ പ്രധാന വിഷയം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഭരണഘടനാ വിഷയം?",
            "'{a}' എന്തിനെ/ഏതിനെ സൂചിപ്പിക്കുന്നു?",
        ],
        part_subjects,
    )
    _pairs_rev(
        out, existing, rng, PARTS,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ഭാഗം?",
            "'{b}'-യെ കുറിക്കുന്ന ഭരണഘടനാ ഭാഗം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ഭാഗം ഏത്?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന ഭാഗം?",
        ],
        part_names,
    )

    fs_states = list({b for _, b in FIRST_SCHEDULE})
    fs_items = list({a for a, _ in FIRST_SCHEDULE})
    _pairs(
        out, existing, rng, FIRST_SCHEDULE,
        [
            "ഒന്നാം ഷെഡ്യൂളിലെ '{a}'-യുടെ വിവരണം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഒന്നാം ഷെഡ്യൂൾ വിവരം?",
            "ഒന്നാം ഷെഡ്യൂളിൽ '{a}'-ന്റെ പ്രധാന വിവരം?",
            "'{a}' ഒന്നാം ഷെഡ്യൂളിൽ എന്തിനെ സൂചിപ്പിക്കുന്നു?",
        ],
        fs_states,
    )
    _pairs_rev(
        out, existing, rng, FIRST_SCHEDULE,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ഒന്നാം ഷെഡ്യൂൾ വസ്തു?",
            "'{b}'-യെ ഒന്നാം ഷെഡ്യൂളിൽ കാണുന്ന വസ്തു?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ഒന്നാം ഷെഡ്യൂൾ പദം?",
        ],
        fs_items,
    )

    ss_offices = list({b for _, b in SECOND_SCHEDULE})
    ss_items = list({a for a, _ in SECOND_SCHEDULE})
    _pairs(
        out, existing, rng, SECOND_SCHEDULE,
        [
            "രണ്ടാം ഷെഡ്യൂളിൽ '{a}'-യുമായി ബന്ധപ്പെട്ട വ്യവസ്ഥ?",
            "'{a}'-ന്റെ ശമ്പള/ആനുകൂല്യം രണ്ടാം ഷെഡ്യൂളിൽ?",
            "രണ്ടാം ഷെഡ്യൂളിലെ '{a}'-യുടെ പ്രധാന വിവരം?",
        ],
        ss_offices,
    )
    _pairs_rev(
        out, existing, rng, SECOND_SCHEDULE,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട രണ്ടാം ഷെഡ്യൂൾ വ്യക്തി/പദവി?",
            "'{b}'-യുടെ ശമ്പള വ്യവസ്ഥ രണ്ടാം ഷെഡ്യൂളിൽ?",
        ],
        ss_items,
    )

    ts_oaths = list({b for _, b in THIRD_SCHEDULE})
    ts_items = list({a for a, _ in THIRD_SCHEDULE})
    _pairs(
        out, existing, rng, THIRD_SCHEDULE,
        [
            "മൂന്നാം ഷെഡ്യൂളിലെ '{a}'-യുടെ സത്യപ്രതിജ്ഞ?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട സത്യപ്രതിജ്ഞ (മൂന്നാം ഷെഡ്യൂൾ)?",
            "മൂന്നാം ഷെഡ്യൂളിൽ '{a}'-ന്റെ പ്രധാന വിവരം?",
        ],
        ts_oaths,
    )
    _pairs_rev(
        out, existing, rng, THIRD_SCHEDULE,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സത്യപ്രതിജ്ഞ നടക്കുന്ന പദവി?",
            "'{b}' സത്യപ്രതിജ്ഞ മൂന്നാം ഷെഡ്യൂളിലെ ഏത് പദവിയുമായി?",
        ],
        ts_items,
    )

    rs_seats = list({b for _, b in RS_SEATS})
    rs_states = list({a for a, _ in RS_SEATS})
    _pairs(
        out, existing, rng, RS_SEATS,
        [
            "നാലാം ഷെഡ്യൂളിൽ '{a}'-യുടെ രാജ്യസഭാ സീറ്റുകൾ?",
            "'{a}'-യ്ക്ക് നാലാം ഷെഡ്യൂളിൽ നൽകിയിട്ടുള്ള രാജ്യസഭാ സീറ്റ്?",
            "'{a}'-യുടെ രാജ്യസഭാ പ്രതിനിധിത്വം (നാലാം ഷെഡ്യൂൾ)?",
            "നാലാം ഷെഡ്യൂളിലെ '{a}'-യുടെ പ്രധാന വിവരം?",
        ],
        rs_seats,
    )
    _pairs_rev(
        out, existing, rng, RS_SEATS,
        [
            "'{b}' രാജ്യസഭാ സീറ്റുകൾ നൽകിയിട്ടുള്ള സംസ്ഥാനം/പ്രദേശം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നാലാം ഷെഡ്യൂൾ സംസ്ഥാനം?",
        ],
        rs_states,
    )

    f56_topics = list({b for _, b in FIFTH_SIXTH})
    f56_items = list({a for a, _ in FIFTH_SIXTH})
    _pairs(
        out, existing, rng, FIFTH_SIXTH,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഷെഡ്യൂൾ വ്യവസ്ഥ?",
            "'{a}'-ന്റെ പ്രധാന ഉള്ളടക്കം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഗിരിജന/അനുബന്ധിത പ്രദേശ വ്യവസ്ഥ?",
        ],
        f56_topics,
    )
    _pairs_rev(
        out, existing, rng, FIFTH_SIXTH,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ഷെഡ്യൂൾ?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന ഷെഡ്യൂൾ?",
        ],
        f56_items,
    )

    n9_topics = list({b for _, b in NINTH_SCHEDULE})
    n9_items = list({a for a, _ in NINTH_SCHEDULE})
    _pairs(
        out, existing, rng, NINTH_SCHEDULE,
        [
            "ഒൻപതാം ഷെഡ്യൂളുമായി '{a}'-യുടെ ബന്ധം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഒൻപതാം ഷെഡ്യൂൾ വിവരം?",
            "ഒൻപതാം ഷെഡ്യൂളിലെ '{a}'-ന്റെ പ്രധാന വിവരം?",
        ],
        n9_topics,
    )
    _pairs_rev(
        out, existing, rng, NINTH_SCHEDULE,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ഒൻപതാം ഷെഡ്യൂൾ വസ്തു/വിവരം?",
            "'{b}'-യെ ഒൻപതാം ഷെഡ്യൂളുമായി ബന്ധപ്പെടുത്തുന്ന വസ്തു?",
        ],
        n9_items,
    )

    case_topics = list({b for _, b in CASES})
    case_names = list({a for a, _ in CASES})
    _pairs(
        out, existing, rng, CASES,
        [
            "'{a}' കേസിന്റെ പ്രധാന തീർപ്പ്/പ്രാധാന്യം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഭരണഘടനാ വിധി?",
            "പ്രശസ്ത കേസ് '{a}'-ന്റെ പ്രധാന വിവരം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട സുപ്രീംകോടതി വിധി?",
        ],
        case_topics,
    )
    _pairs_rev(
        out, existing, rng, CASES,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പ്രശസ്ത കേസ്?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന ചരിത്രപ്രസിദ്ധ കേസ്?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സുപ്രീംകോടതി കേസ്?",
        ],
        case_names,
    )

    bs_topics = list({b for _, b in BASIC_STRUCTURE})
    bs_items = list({a for a, _ in BASIC_STRUCTURE})
    _pairs(
        out, existing, rng, BASIC_STRUCTURE,
        [
            "അടിസ്ഥാന ഘടനാ സിദ്ധാന്തത്തിൽ '{a}'-യുടെ സ്ഥാനം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട അടിസ്ഥാന ഘടന?",
            "'{a}'-ന്റെ അടിസ്ഥാന ഘടനാ പ്രാധാന്യം?",
        ],
        bs_topics,
    )
    _pairs_rev(
        out, existing, rng, BASIC_STRUCTURE,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട അടിസ്ഥാന ഘടനാ ഘടകം/കേസ്?",
            "'{b}'-യെ സംബന്ധിച്ച അടിസ്ഥാന ഘടനാ വിവരം?",
        ],
        bs_items,
    )

    at_types = list({b for _, b in AMEND_TYPES})
    at_items = list({a for a, _ in AMEND_TYPES})
    _pairs(
        out, existing, rng, AMEND_TYPES,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഭേദഗതി നടപടിക്രമം?",
            "'{a}'-ന്റെ ഭരണഘടനാ ഭേദഗതി തരം?",
            "ഭേദഗതി '{a}'-യുടെ നടപടിക്രമ തരം?",
        ],
        at_types,
    )
    _pairs_rev(
        out, existing, rng, AMEND_TYPES,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ഭേദഗതി/അനുച്ഛേദം?",
            "'{b}' നടപടിക്രമം ആവശ്യപ്പെടുന്ന ഭേദഗതി?",
        ],
        at_items,
    )

    cs_topics = list({b for _, b in CENTRE_STATE})
    cs_items = list({a for a, _ in CENTRE_STATE})
    _pairs(
        out, existing, rng, CENTRE_STATE,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട കേന്ദ്ര-സംസ്ഥാന ബന്ധം?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം (കേന്ദ്ര-സംസ്ഥാന)?",
            "കേന്ദ്ര-സംസ്ഥാന ബന്ധത്തിൽ '{a}'-യുടെ പങ്ക്?",
        ],
        cs_topics,
    )
    _pairs_rev(
        out, existing, rng, CENTRE_STATE,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട അനുച്ഛേദം/സംവിധാനം?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന കേന്ദ്ര-സംസ്ഥാന വ്യവസ്ഥ?",
        ],
        cs_items,
    )

    fin_topics = list({b for _, b in FINANCE})
    fin_items = list({a for a, _ in FINANCE})
    _pairs(
        out, existing, rng, FINANCE,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ധനകാര്യ/നികുതി വ്യവസ്ഥ?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം (ധനകാര്യ)?",
            "ധനകാര്യ ഭാഗത്തിൽ '{a}'-യുടെ പ്രാധാന്യം?",
        ],
        fin_topics,
    )
    _pairs_rev(
        out, existing, rng, FINANCE,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട അനുച്ഛേദം/ഭേദഗതി?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന ധനകാര്യ വ്യവസ്ഥ?",
        ],
        fin_items,
    )

    tr_topics = list({b for _, b in TRADE})
    tr_items = list({a for a, _ in TRADE})
    _pairs(
        out, existing, rng, TRADE,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വ്യാപാര/വാണിജ്യ വ്യവസ്ഥ?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം (ഭാഗം XIII)?",
            "വ്യാപാര-വാണിജ്യ ഭാഗത്തിൽ '{a}'-യുടെ പ്രാധാന്യം?",
        ],
        tr_topics,
    )
    _pairs_rev(
        out, existing, rng, TRADE,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട അനുച്ഛേദം?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന വ്യാപാര വ്യവസ്ഥ?",
        ],
        tr_items,
    )

    lang_topics = list({b for _, b in LANGUAGES})
    lang_items = list({a for a, _ in LANGUAGES})
    _pairs(
        out, existing, rng, LANGUAGES,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഔദ്യോഗിക ഭാഷാ വ്യവസ്ഥ?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം (ഭാഗം XVII)?",
            "ഔദ്യോഗിക ഭാഷാ ഭാഗത്തിൽ '{a}'-യുടെ പ്രാധാന്യം?",
        ],
        lang_topics,
    )
    _pairs_rev(
        out, existing, rng, LANGUAGES,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട അനുച്ഛേദം/ഷെഡ്യൂൾ?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന ഭാഷാ വ്യവസ്ഥ?",
        ],
        lang_items,
    )

    res_topics = list({b for _, b in RESERVATION})
    res_items = list({a for a, _ in RESERVATION})
    _pairs(
        out, existing, rng, RESERVATION,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട സംവരണ വ്യവസ്ഥ?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം (സംവരണ)?",
            "സംവരണ വ്യവസ്ഥയിൽ '{a}'-യുടെ പ്രാധാന്യം?",
        ],
        res_topics,
    )
    _pairs_rev(
        out, existing, rng, RESERVATION,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട അനുച്ഛേദം/ഭേദഗതി?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന സംവരണ വ്യവസ്ഥ?",
        ],
        res_items,
    )

    a371_topics = list({b for _, b in ART371_SERIES})
    a371_items = list({a for a, _ in ART371_SERIES})
    _pairs(
        out, existing, rng, ART371_SERIES,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രത്യേക സംസ്ഥാന വ്യവസ്ഥ?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം (371 ശ്രേണി)?",
            "പ്രത്യേക സംസ്ഥാന വ്യവസ്ഥയിൽ '{a}'-യുടെ പ്രാധാന്യം?",
        ],
        a371_topics,
    )
    _pairs_rev(
        out, existing, rng, ART371_SERIES,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട അനുച്ഛേദം/സംസ്ഥാനം?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന പ്രത്യേക വ്യവസ്ഥ?",
        ],
        a371_items,
    )

    coop_topics = list({b for _, b in COOPERATIVE})
    coop_items = list({a for a, _ in COOPERATIVE})
    _pairs(
        out, existing, rng, COOPERATIVE,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട സഹകരണ വ്യവസ്ഥ?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം (ഭാഗം IX-B)?",
            "സഹകരണ സമിതി വ്യവസ്ഥയിൽ '{a}'-യുടെ പ്രാധാന്യം?",
        ],
        coop_topics,
    )
    _pairs_rev(
        out, existing, rng, COOPERATIVE,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട അനുച്ഛേദം/ഭാഗം?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന സഹകരണ വ്യവസ്ഥ?",
        ],
        coop_items,
    )

    trib_topics = list({b for _, b in TRIBUNALS})
    trib_items = list({a for a, _ in TRIBUNALS})
    _pairs(
        out, existing, rng, TRIBUNALS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ധികാരണ/ട്രിബ്യunal വ്യവസ്ഥ?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം (ഭാഗം XIV-A)?",
            "ധികാരണ വ്യവസ്ഥയിൽ '{a}'-യുടെ പ്രാധാന്യം?",
        ],
        trib_topics,
    )
    _pairs_rev(
        out, existing, rng, TRIBUNALS,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട അനുച്ഛേദം/ഭേദഗതി?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന ധികാരണ വ്യവസ്ഥ?",
        ],
        trib_items,
    )

    parl_topics = list({b for _, b in PARLIAMENT})
    parl_items = list({a for a, _ in PARLIAMENT})
    _pairs(
        out, existing, rng, PARLIAMENT,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട പാർലമെന്റ് നടപടിക്രമം?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം (പാർലമെന്റ്)?",
            "പാർലമെന്റ് സംവിധാനത്തിൽ '{a}'-യുടെ പ്രാധാന്യം?",
        ],
        parl_topics,
    )
    _pairs_rev(
        out, existing, rng, PARLIAMENT,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട അനുച്ഛേദം/നടപടി?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന പാർലമെന്റ് വ്യവസ്ഥ?",
        ],
        parl_items,
    )

    feat_topics = list({b for _, b in FEATURES})
    feat_items = list({a for a, _ in FEATURES})
    _pairs(
        out, existing, rng, FEATURES,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഭരണഘടനാ സവിശേഷത?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം (ഭരണഘടന)?",
            "ഇന്ത്യൻ ഭരണഘടനയിൽ '{a}'-യുടെ പ്രാധാന്യം?",
        ],
        feat_topics,
    )
    _pairs_rev(
        out, existing, rng, FEATURES,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സവിശേഷത/മൂലാധാരം?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന ഭരണഘടനാ സവിശേഷത?",
        ],
        feat_items,
    )

    amend_years = list({b for _, b, _ in AMENDMENTS})
    amend_changes = list({c for _, _, c in AMENDMENTS})
    amend_nums = list({a for a, _, _ in AMENDMENTS})
    _triples(
        out, existing, rng, AMENDMENTS,
        [
            "'{a}'-യുടെ വർഷം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വർഷം?",
            "ഭരണഘടനാ '{a}'-യുടെ പ്രാബല്യ/നടപ്പാക്കൽ വർഷം?",
        ],
        [
            "'{a}'-യുടെ പ്രധാന മാറ്റം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന മാറ്റം?",
            "ഭരണഘടനാ '{a}'-യുടെ പ്രധാന ഉള്ളടക്കം?",
        ],
        [
            "'{c}'-യുമായി ബന്ധപ്പെട്ട ഭേദഗതി?",
            "'{c}'-യെ ഉൾക്കൊള്ളുന്ന ഭരണഘടനാ ഭേദഗതി?",
            "'{c}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന ഭേദഗതി?",
        ],
        amend_years,
        amend_changes,
        amend_nums,
    )

    art_topics = list({b for _, b in ARTICLES})
    art_nums = list({a for a, _ in ARTICLES})
    _pairs(
        out, existing, rng, ARTICLES,
        [
            "'{a}'-യുടെ വിഷയം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വ്യവസ്ഥ?",
            "ഭരണഘടനയിലെ '{a}'-ന്റെ പ്രധാന ഉള്ളടക്കം?",
            "'{a}'-യെ കുറിക്കുന്ന വിഷയം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഭരണഘടനാ വ്യവസ്ഥ?",
        ],
        art_topics,
    )
    _pairs_rev(
        out, existing, rng, ARTICLES,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട അനുച്ഛേദം?",
            "'{b}'-യെ ഉൾക്കൊള്ളുന്ന അനുച്ഛേദം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ലേഖനം?",
        ],
        art_nums,
    )


def generate_wave20_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []
    _emit_all(out, existing, rng)
    return interleave_candidates(out, rng)


if __name__ == "__main__":
    print(len(generate_wave20_candidates(set(), random.Random(0))))
'''

# Data will be appended below in DATA dict
DATA: dict[str, list] = {}


def main() -> None:
    import coi20_data as d
    import random

    parts = [HEADER]
    names = [
        "PARTS", "FIRST_SCHEDULE", "SECOND_SCHEDULE", "THIRD_SCHEDULE", "RS_SEATS",
        "FIFTH_SIXTH", "NINTH_SCHEDULE", "CASES", "BASIC_STRUCTURE", "AMEND_TYPES",
        "CENTRE_STATE", "FINANCE", "TRADE", "LANGUAGES", "RESERVATION", "ART371_SERIES",
        "COOPERATIVE", "TRIBUNALS", "PARLIAMENT", "FEATURES", "AMENDMENTS", "ARTICLES",
    ]
    for name in names:
        val = getattr(d, name)
        parts.append(f"{name}: list = ")
        parts.append(pprint.pformat(val, width=120, sort_dicts=False))
        parts.append("\n\n")
    parts.append(EMIT)
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
    ns: dict = {}
    exec(OUT.read_text(encoding="utf-8"), ns)
    print("pool", len(ns["generate_wave20_candidates"](set(), random.Random(1))))


if __name__ == "__main__":
    main()
