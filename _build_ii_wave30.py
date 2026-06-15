#!/usr/bin/env python3
"""Build important_institutions_wave30_facts.py from ii_wave30_data."""

from __future__ import annotations

import random
import re
from pathlib import Path

from ii_wave30_data import DIRECT_FACTS, PAIRS

ROOT = Path(__file__).parent
OUT = ROOT / "important_institutions_wave30_facts.py"

MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")

CATEGORY_MAP = [
    ("HQ_PAIRS", "POOL_INSTITUTIONS", "POOL_CITIES"),
    ("KERALA_HQ_PAIRS", "POOL_KERALA_INST", "POOL_KERALA_CITIES"),
    ("ESTABLISH_YEAR", "POOL_INSTITUTIONS", "POOL_YEARS"),
    ("ESTABLISH_ACT", "POOL_INSTITUTIONS", "POOL_ACTS"),
    ("PARENT_MINISTRY", "POOL_INSTITUTIONS", "POOL_MINISTRIES"),
    ("MANDATE", "POOL_INSTITUTIONS", "POOL_MANDATES"),
    ("KERALA_UNIV_HQ", "POOL_KERALA_UNIV", "POOL_KERALA_CITIES"),
    ("PREMIER_INST_HQ", "POOL_PREMIER", "POOL_CITIES"),
    ("REGULATOR_HQ", "POOL_REGULATORS", "POOL_CITIES"),
    ("KERALA_COMMISSION_HQ", "POOL_KERALA_COMM", "POOL_KERALA_CITIES"),
    ("RESEARCH_HQ", "POOL_RESEARCH", "POOL_CITIES"),
    ("MEDICAL_COLLEGE_HQ", "POOL_MEDICAL", "POOL_KERALA_CITIES"),
    ("BANK_HQ", "POOL_BANKS", "POOL_BANK_CITIES"),
    ("TRIBUNAL_HQ", "POOL_TRIBUNALS", "POOL_CITIES"),
    ("PLANNING_BODY", "POOL_PLANNING", "POOL_PLANNING_FACTS"),
    ("KERALA_PSU_HQ", "POOL_KERALA_PSU", "POOL_KERALA_CITIES"),
    ("CONSTITUTIONAL_BODY", "POOL_CONST_BODY", "POOL_CONST_DUTIES"),
    ("STATUTORY_BODY", "POOL_STATUTORY", "POOL_STAT_DUTIES"),
    ("KERALA_TRIBUNAL", "POOL_KERALA_TRIB", "POOL_KERALA_CITIES"),
    ("ABBREVIATION", "POOL_ABBR_SHORT", "POOL_ABBR_FULL"),
    ("PSU_HQ", "POOL_PSU", "POOL_CITIES"),
    ("COURT_BENCH", "POOL_COURTS", "POOL_CITIES"),
    ("FINANCIAL_INST", "POOL_FINANCIAL", "POOL_CITIES"),
    ("SCIENCE_TECH", "POOL_SCIENCE", "POOL_CITIES"),
    ("KERALA_CULTURAL", "POOL_CULTURAL", "POOL_KERALA_CITIES"),
    ("PUBLIC_SERVICE", "POOL_PUBLIC_SVC", "POOL_KERALA_CITIES"),
    ("INSURANCE_PENSION", "POOL_INSURANCE", "POOL_CITIES"),
    ("EDUCATION_BODY", "POOL_EDU_BODY", "POOL_EDU_DUTIES"),
    ("CHAIRMAN_ROLE", "POOL_CHAIR_INST", "POOL_CHAIR_AUTH"),
]


def pool(rows: list[tuple[str, str]], idx: int) -> list[str]:
    return list(dict.fromkeys(r[idx] for r in rows))


def fmt_pairs(name: str, rows: list[tuple[str, str]]) -> str:
    lines = [f"{name}: list[tuple[str, str]] = ["]
    for a, b in rows:
        lines.append(f'    ("{a}", "{b}"),')
    lines.append("]")
    return "\n".join(lines)


def fmt_pool(name: str, items: list[str]) -> str:
    lines = [f"{name}: list[str] = ["]
    for x in items:
        lines.append(f'    "{x}",')
    lines.append("]")
    return "\n".join(lines)


def fmt_direct(facts: list[tuple[str, str, list[str], str]]) -> str:
    lines = ["DIRECT_FACTS: list[tuple[str, str, list[str], str]] = ["]
    for q, ans, wrong, diff in facts:
        w = ", ".join(f'"{x}"' for x in wrong)
        lines.append(f'    ("{q}", "{ans}", [{w}], "{diff}"),')
    lines.append("]")
    return "\n".join(lines)


EMIT = '''
def generate_wave30_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []

    emit_category(out, existing, rng, HQ_PAIRS,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത് നഗരം?", "'{a}' എവിടെ സ്ഥിതി ചെയ്യുന്നു?", "'{a}'-ന്റെ പ്രധാന കേന്ദ്രം?"],
        ["'{b}' ഏത് സ്ഥാപനത്തിന്റെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള പ്രധാന സ്ഥാപനം ഏത്?", "'{b}' നഗരത്തിലെ പ്രധാന സ്ഥാപനം?"],
        POOL_INSTITUTIONS, POOL_CITIES)

    emit_category(out, existing, rng, KERALA_HQ_PAIRS,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത്?", "'{a}' കേരളത്തിൽ എവിടെ സ്ഥിതി ചെയ്യുന്നു?", "'{a}'-ന്റെ പ്രധാന കേന്ദ്രം?"],
        ["'{b}' ഏത് കേരള സ്ഥാപനത്തിന്റെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള പ്രധാന കേരള സ്ഥാപനം ഏത്?", "'{b}' നഗരത്തിലെ കേരള സ്ഥാപനം?"],
        POOL_KERALA_INST, POOL_KERALA_CITIES)

    emit_category(out, existing, rng, ESTABLISH_YEAR,
        ["'{a}' സ്ഥാപിതമായ വർഷം ഏത്?", "'{a}'-ന്റെ സ്ഥാപന വർഷം?", "'{a}' രൂപീകരിച്ച വർഷം?"],
        ["'{b}' വർഷം സ്ഥാപിതമായ സ്ഥാപനം ഏത്?", "'{b}'-ൽ ആരംഭിച്ച സ്ഥാപനം ഏത്?", "'{b}' വർഷത്തിൽ രൂപീകരിച്ച സ്ഥാപനം?"],
        POOL_INSTITUTIONS, POOL_YEARS)

    emit_category(out, existing, rng, ESTABLISH_ACT,
        ["'{a}'-ന്റെ നിയമപരമായ അടിസ്ഥാനം ഏത്?", "'{a}' ഏത് നിയമം/ആക്റ്റിന് കീഴിലാണ്?", "'{a}'-ന്റെ സ്ഥാപന നിയമം?"],
        ["'{b}' അടിസ്ഥാനമാക്കിയ സ്ഥാപനം ഏത്?", "'{b}' നിയമത്തിന് കീഴിലുള്ള സ്ഥാപനം ഏത്?", "'{b}' ആക്റ്റിന് കീഴിലുള്ള സ്ഥാപനം?"],
        POOL_INSTITUTIONS, POOL_ACTS)

    emit_category(out, existing, rng, PARENT_MINISTRY,
        ["'{a}' ഏത് മന്ത്രാലയത്തിന് കീഴിലാണ്?", "'{a}'-ന്റെ നോഡൽ മന്ത്രാലയം ഏത്?", "'{a}' നടപ്പാക്കുന്ന മന്ത്രാലയം?"],
        ["'{b}' മന്ത്രാലയത്തിന് കീഴിലുള്ള പ്രധാന സ്ഥാപനം ഏത്?", "'{b}' നോഡൽ മന്ത്രാലയമായ സ്ഥാപനം ഏത്?", "'{b}'-ന് കീഴിലുള്ള സ്ഥാപനം?"],
        POOL_INSTITUTIONS, POOL_MINISTRIES)

    emit_category(out, existing, rng, MANDATE,
        ["'{a}'-ന്റെ പ്രധാന ലക്ഷ്യം/മാൻഡേറ്റ് ഏത്?", "'{a}' പ്രധാനമായി എന്ത് ചെയ്യുന്നു?", "'{a}'-ന്റെ പ്രധാന കർത്തവ്യം?"],
        ["'{b}' ലക്ഷ്യം നേടുന്ന സ്ഥാപനം ഏത്?", "'{b}' മേഖലയിലെ പ്രധാന സ്ഥാപനം ഏത്?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സ്ഥാപനം?"],
        POOL_INSTITUTIONS, POOL_MANDATES)

    emit_category(out, existing, rng, KERALA_UNIV_HQ,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത്?", "'{a}' കേരളത്തിൽ എവിടെ സ്ഥിതി ചെയ്യുന്നു?", "'{a}'-ന്റെ പ്രധാന കാമ്പസ്?"],
        ["'{b}' ഏത് കേരള സർവകലാശാലയുടെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള കേരള സർവകലാശാല ഏത്?", "'{b}' നഗരത്തിലെ സർവകലാശാല?"],
        POOL_KERALA_UNIV, POOL_KERALA_CITIES)

    emit_category(out, existing, rng, PREMIER_INST_HQ,
        ["'{a}' സ്ഥിതി ചെയ്യുന്ന നഗരം ഏത്?", "'{a}'-ന്റെ ആസ്ഥാന/പ്രധാന കാമ്പസ്?", "'{a}' എവിടെയാണ്?"],
        ["'{b}' നഗരത്തിലെ പ്രധാന ഉന്നത വിദ്യാഭ്യാസ സ്ഥാപനം ഏത്?", "'{b}'-ലുള്ള ഐ.ഐ.ടി/ഐ.ഐ.എം/എൻ.ഐ.ടി ഏത്?", "'{b}' നഗരത്തിലെ പ്രമുഖ സ്ഥാപനം?"],
        POOL_PREMIER, POOL_CITIES)

    emit_category(out, existing, rng, REGULATOR_HQ,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത്?", "'{a}' എവിടെ സ്ഥിതി ചെയ്യുന്നു?", "'{a}'-ന്റെ പ്രധാന കേന്ദ്രം?"],
        ["'{b}' ഏത് നിയന്ത്രണ സ്ഥാപനത്തിന്റെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള ധന/ടെലികോം നിയന്ത്രക സ്ഥാപനം ഏത്?", "'{b}' നഗരത്തിലെ നിയന്ത്രക സ്ഥാപനം?"],
        POOL_REGULATORS, POOL_CITIES)

    emit_category(out, existing, rng, KERALA_COMMISSION_HQ,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത്?", "'{a}' കേരളത്തിൽ എവിടെ പ്രവർത്തിക്കുന്നു?", "'{a}'-ന്റെ പ്രധാന കേന്ദ്രം?"],
        ["'{b}' ഏത് കേരള കമ്മീഷന്റെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള കേരള സംസ്ഥാന കമ്മീഷൻ ഏത്?", "'{b}' നഗരത്തിലെ കമ്മീഷൻ?"],
        POOL_KERALA_COMM, POOL_KERALA_CITIES)

    emit_category(out, existing, rng, RESEARCH_HQ,
        ["'{a}' സ്ഥിതി ചെയ്യുന്ന നഗരം ഏത്?", "'{a}'-ന്റെ ആസ്ഥാനം?", "'{a}' എവിടെയാണ്?"],
        ["'{b}' നഗരത്തിലെ പ്രധാന ഗവേഷണ സ്ഥാപനം ഏത്?", "'{b}'-ലുള്ള സി.എസ്.ഐ.ആർ/ഐ.എസ്.ആർ.ഒ സ്ഥാപനം ഏത്?", "'{b}' നഗരത്തിലെ ഗവേഷണ കേന്ദ്രം?"],
        POOL_RESEARCH, POOL_CITIES)

    emit_category(out, existing, rng, MEDICAL_COLLEGE_HQ,
        ["'{a}' സ്ഥിതി ചെയ്യുന്ന നഗരം ഏത്?", "'{a}' എവിടെയാണ്?", "'{a}'-ന്റെ സ്ഥലം?"],
        ["'{b}' നഗരത്തിലെ ഗവൺമെന്റ് മെഡിക്കൽ കോളേജ് ഏത്?", "'{b}'-ലുള്ള മെഡിക്കൽ കോളേജ് ഏത്?", "'{b}' നഗരത്തിലെ ജി.എം.സി?"],
        POOL_MEDICAL, POOL_KERALA_CITIES)

    emit_category(out, existing, rng, BANK_HQ,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത്?", "'{a}' ബാങ്കിന്റെ ഹെഡ്ക്വാർട്ടർ?", "'{a}' എവിടെ സ്ഥിതി ചെയ്യുന്നു?"],
        ["'{b}' ഏത് ബാങ്കിന്റെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള പ്രധാന ബാങ്ക് ഏത്?", "'{b}' നഗരത്തിലെ ബാങ്ക് ആസ്ഥാനം?"],
        POOL_BANKS, POOL_BANK_CITIES)

    emit_category(out, existing, rng, TRIBUNAL_HQ,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത്?", "'{a}' എവിടെ പ്രവർത്തിക്കുന്നു?", "'{a}'-ന്റെ പ്രധാന കേന്ദ്രം?"],
        ["'{b}' ഏത് ട്രൈബ്യൂണലിന്റെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള ട്രൈബ്യൂണൽ ഏത്?", "'{b}' നഗരത്തിലെ ട്രൈബ്യൂണൽ?"],
        POOL_TRIBUNALS, POOL_CITIES)

    emit_category(out, existing, rng, PLANNING_BODY,
        ["'{a}'-ന്റെ പ്രധാന വസ്തുത/പശ്ചാത്തലം?", "'{a}' സംബന്ധിച്ച പ്രധാന വിവരം?", "'{a}'-ന്റെ പ്രധാന സവിശേഷത?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട ആസൂത്രണ സ്ഥാപനം ഏത്?", "'{b}' സംബന്ധിച്ച സ്ഥാപനം ഏത്?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സ്ഥാപനം?"],
        POOL_PLANNING, POOL_PLANNING_FACTS)

    emit_category(out, existing, rng, KERALA_PSU_HQ,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത്?", "'{a}' കേരളത്തിൽ എവിടെ സ്ഥിതി ചെയ്യുന്നു?", "'{a}'-ന്റെ പ്രധാന കേന്ദ്രം?"],
        ["'{b}' ഏത് കേരള പൊതുമേഖലാ സ്ഥാപനത്തിന്റെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള കേരള സർക്കാർ സ്ഥാപനം ഏത്?", "'{b}' നഗരത്തിലെ കേരള സ്ഥാപനം?"],
        POOL_KERALA_PSU, POOL_KERALA_CITIES)

    emit_category(out, existing, rng, CONSTITUTIONAL_BODY,
        ["'{a}'-ന്റെ പ്രധാന കർത്തവ്യം?", "'{a}' ഭരണഘടനയിൽ ഏത് അനുച്ഛേദവുമായി ബന്ധപ്പെട്ടത്?", "'{a}'-ന്റെ മാൻഡേറ്റ്?"],
        ["'{b}' കർത്തവ്യം നിർവഹിക്കുന്ന ഭരണഘടനാ സ്ഥാപനം ഏത്?", "'{b}'-യുമായി ബന്ധപ്പെട്ട ഭരണഘടനാ സ്ഥാപനം?", "'{b}' നിർവഹിക്കുന്ന സ്ഥാപനം?"],
        POOL_CONST_BODY, POOL_CONST_DUTIES)

    emit_category(out, existing, rng, STATUTORY_BODY,
        ["'{a}'-ന്റെ പ്രധാന ലക്ഷ്യം?", "'{a}' ഏത് മേഖലയിൽ പ്രവർത്തിക്കുന്നു?", "'{a}'-ന്റെ മാൻഡേറ്റ്?"],
        ["'{b}' ലക്ഷ്യം നേടുന്ന സ്ഥാപനം ഏത്?", "'{b}' മേഖലയിലെ സ്ഥാപനം ഏത്?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സ്ഥാപനം?"],
        POOL_STATUTORY, POOL_STAT_DUTIES)

    emit_category(out, existing, rng, KERALA_TRIBUNAL,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത്?", "'{a}' കേരളത്തിൽ എവിടെ പ്രവർത്തിക്കുന്നു?", "'{a}'-ന്റെ പ്രധാന കേന്ദ്രം?"],
        ["'{b}' ഏത് കേരള ട്രൈബ്യൂണലിന്റെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള കേരള ട്രൈബ്യൂണൽ ഏത്?", "'{b}' നഗരത്തിലെ ട്രൈബ്യൂണൽ?"],
        POOL_KERALA_TRIB, POOL_KERALA_CITIES)

    emit_category(out, existing, rng, ABBREVIATION,
        ["'{a}' എന്ന സംക്ഷേപത്തിന്റെ പൂർണ്ണരൂപം?", "'{a}'-ന്റെ വിപുലീകരണം?", "'{a}' എന്തിനെ സൂചിപ്പിക്കുന്നു?"],
        ["'{b}'-ന്റെ സംക്ഷേപം?", "'{b}' ഏത് ചുരുക്കെഴുത്തിൽ?", "'{b}'-ന് ഏത് സംക്ഷേപം?"],
        POOL_ABBR_SHORT, POOL_ABBR_FULL)

    emit_category(out, existing, rng, PSU_HQ,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത്?", "'{a}' എവിടെ സ്ഥിതി ചെയ്യുന്നു?", "'{a}'-ന്റെ ഹെഡ്ക്വാർട്ടർ?"],
        ["'{b}' ഏത് പൊതുമേഖലാ സ്ഥാപനത്തിന്റെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള പ്രധാന പി.എസ്.യു. ഏത്?", "'{b}' നഗരത്തിലെ പൊതുമേഖലാ സ്ഥാപനം?"],
        POOL_PSU, POOL_CITIES)

    emit_category(out, existing, rng, COURT_BENCH,
        ["'{a}'-ന്റെ പ്രധാന ബെഞ്ച്/ആസ്ഥാനം ഏത്?", "'{a}' എവിടെ പ്രവർത്തിക്കുന്നു?", "'{a}'-ന്റെ പ്രധാന കേന്ദ്രം?"],
        ["'{b}' ഏത് നീതിമന്ദിരത്തിന്റെ പ്രധാന ബെഞ്ച്?", "'{b}'-ലുള്ള ഉന്നത നീതിമന്ദിരം ഏത്?", "'{b}' നഗരത്തിലെ നീതിമന്ദിര ബെഞ്ച്?"],
        POOL_COURTS, POOL_CITIES)

    emit_category(out, existing, rng, FINANCIAL_INST,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത്?", "'{a}' എവിടെ സ്ഥിതി ചെയ്യുന്നു?", "'{a}'-ന്റെ പ്രധാന കേന്ദ്രം?"],
        ["'{b}' ഏത് സാമ്പത്തിക സ്ഥാപനത്തിന്റെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള വികസന ബാങ്ക്/സ്ഥാപനം ഏത്?", "'{b}' നഗരത്തിലെ സാമ്പത്തിക സ്ഥാപനം?"],
        POOL_FINANCIAL, POOL_CITIES)

    emit_category(out, existing, rng, SCIENCE_TECH,
        ["'{a}' സ്ഥിതി ചെയ്യുന്ന നഗരം ഏത്?", "'{a}'-ന്റെ ആസ്ഥാനം?", "'{a}' എവിടെയാണ്?"],
        ["'{b}' നഗരത്തിലെ ബഹിരാകാശ/ആണവ/പ്രതിരോധ സ്ഥാപനം ഏത്?", "'{b}'-ലുള്ള പ്രമുഖ ശാസ്ത്ര സ്ഥാപനം ഏത്?", "'{b}' നഗരത്തിലെ സാങ്കേതിക സ്ഥാപനം?"],
        POOL_SCIENCE, POOL_CITIES)

    emit_category(out, existing, rng, KERALA_CULTURAL,
        ["'{a}' സ്ഥിതി ചെയ്യുന്ന സ്ഥലം ഏത്?", "'{a}' കേരളത്തിൽ എവിടെയാണ്?", "'{a}'-ന്റെ സ്ഥാനം?"],
        ["'{b}' ഏത് കേരള സാംസ്കാരിക സ്ഥാപനത്തിന്റെ സ്ഥലമാണ്?", "'{b}'-ലുള്ള കലാ/സാംസ്കാരിക സ്ഥാപനം ഏത്?", "'{b}' നഗരത്തിലെ സാംസ്കാരിക കേന്ദ്രം?"],
        POOL_CULTURAL, POOL_KERALA_CITIES)

    emit_category(out, existing, rng, PUBLIC_SERVICE,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത്?", "'{a}' എവിടെ പ്രവർത്തിക്കുന്നു?", "'{a}'-ന്റെ പ്രധാന കേന്ദ്രം?"],
        ["'{b}' ഏത് പൊതുസേവന സ്ഥാപനത്തിന്റെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള പി.എസ്.സി/പരിശീലന കേന്ദ്രം ഏത്?", "'{b}' നഗരത്തിലെ പൊതുസേവന സ്ഥാപനം?"],
        POOL_PUBLIC_SVC, POOL_KERALA_CITIES)

    emit_category(out, existing, rng, INSURANCE_PENSION,
        ["'{a}'-ന്റെ ആസ്ഥാനം ഏത്?", "'{a}' എവിടെ സ്ഥിതി ചെയ്യുന്നു?", "'{a}'-ന്റെ പ്രധാന കേന്ദ്രം?"],
        ["'{b}' ഏത് ഇൻഷുറൻസ്/പെൻഷൻ സ്ഥാപനത്തിന്റെ ആസ്ഥാനമാണ്?", "'{b}'-ലുള്ള സാമൂഹിക സുരക്ഷാ സ്ഥാപനം ഏത്?", "'{b}' നഗരത്തിലെ ഇൻഷുറൻസ് സ്ഥാപനം?"],
        POOL_INSURANCE, POOL_CITIES)

    emit_category(out, existing, rng, EDUCATION_BODY,
        ["'{a}'-ന്റെ പ്രധാന കർത്തവ്യം?", "'{a}' ഏത് വിദ്യാഭ്യാസ മേഖലയിൽ?", "'{a}'-ന്റെ മാൻഡേറ്റ്?"],
        ["'{b}' കർത്തവ്യം നിർവഹിക്കുന്ന വിദ്യാഭ്യാസ സ്ഥാപനം ഏത്?", "'{b}'-യുമായി ബന്ധപ്പെട്ട വിദ്യാഭ്യാസ സ്ഥാപനം?", "'{b}' മേഖലയിലെ സ്ഥാപനം?"],
        POOL_EDU_BODY, POOL_EDU_DUTIES)

    emit_category(out, existing, rng, CHAIRMAN_ROLE,
        ["'{a}'-ന്റെ മുഖ്യസ്ഥനെ/അധ്യക്ഷനെ നിയമിക്കുന്നത് ആര്?", "'{a}'-ന്റെ ഗവർണർ/ചെയർമാൻ നിയമന അധികാരം ആരുടേതാണ്?", "'{a}' മുഖ്യസ്ഥനെ നിയമിക്കുന്നത്?"],
        ["'{b}' നിയമിക്കുന്ന സ്ഥാപനം ഏത്?", "'{b}' അധികാരമുള്ള സ്ഥാപനം ഏത്?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സ്ഥാപനം?"],
        POOL_CHAIR_INST, POOL_CHAIR_AUTH)

    emit_direct(out, existing, rng, DIRECT_FACTS)

    return out


if __name__ == "__main__":
    print(len(generate_wave30_candidates(set(), random.Random(0))))
'''


def build_pools() -> dict[str, list[str]]:
    pools: dict[str, list[str]] = {}
    for key, pa, pb in CATEGORY_MAP:
        rows = PAIRS[key]
        pools[pa] = pool(rows, 0)
        pools[pb] = pool(rows, 1)
    # shared city pools
    all_cities = list(dict.fromkeys(
        pool(PAIRS["HQ_PAIRS"], 1)
        + pool(PAIRS["PREMIER_INST_HQ"], 1)
        + pool(PAIRS["REGULATOR_HQ"], 1)
        + pool(PAIRS["RESEARCH_HQ"], 1)
        + pool(PAIRS["PSU_HQ"], 1)
        + pool(PAIRS["SCIENCE_TECH"], 1)
        + pool(PAIRS["FINANCIAL_INST"], 1)
        + pool(PAIRS["INSURANCE_PENSION"], 1)
        + pool(PAIRS["TRIBUNAL_HQ"], 1)
        + pool(PAIRS["COURT_BENCH"], 1)
    ))
    pools["POOL_CITIES"] = all_cities
    pools["POOL_INSTITUTIONS"] = list(dict.fromkeys(
        pool(PAIRS["HQ_PAIRS"], 0)
        + pool(PAIRS["ESTABLISH_YEAR"], 0)
        + pool(PAIRS["PARENT_MINISTRY"], 0)
        + pool(PAIRS["MANDATE"], 0)
    ))
    pools["POOL_KERALA_CITIES"] = list(dict.fromkeys(
        pool(PAIRS["KERALA_HQ_PAIRS"], 1)
        + pool(PAIRS["KERALA_UNIV_HQ"], 1)
        + pool(PAIRS["MEDICAL_COLLEGE_HQ"], 1)
        + pool(PAIRS["KERALA_COMMISSION_HQ"], 1)
        + pool(PAIRS["KERALA_PSU_HQ"], 1)
        + pool(PAIRS["KERALA_CULTURAL"], 1)
        + pool(PAIRS["PUBLIC_SERVICE"], 1)
        + pool(PAIRS["KERALA_TRIBUNAL"], 1)
    ))
    pools["POOL_KERALA_INST"] = list(dict.fromkeys(
        pool(PAIRS["KERALA_HQ_PAIRS"], 0) + pool(PAIRS["KERALA_PSU_HQ"], 0)
    ))
    pools["POOL_BANK_CITIES"] = pool(PAIRS["BANK_HQ"], 1)
    return pools


def check_mixed(text: str) -> bool:
    return bool(MIXED.search(text))


def main() -> None:
    pools = build_pools()
    parts = [
        '#!/usr/bin/env python3\n"""Wave 30 important institutions facts — 30 Malayalam PSC topic types."""\n\n',
        "from __future__ import annotations\n\nimport random\n\n",
        "from refill_common import Candidate\nfrom wave30_emit import emit_category, emit_direct\n\n",
    ]
    for key in PAIRS:
        parts.append(fmt_pairs(key, PAIRS[key]) + "\n\n")
    for name, items in sorted(pools.items()):
        parts.append(fmt_pool(name, items) + "\n\n")
    parts.append(fmt_direct(DIRECT_FACTS) + "\n\n")
    parts.append(EMIT)
    content = "".join(parts)
    OUT.write_text(content, encoding="utf-8")
    # verify count
    ns: dict = {}
    exec(compile(content, str(OUT), "exec"), ns)
    count = len(ns["generate_wave30_candidates"](set(), random.Random(0)))
    print(f"Wrote {OUT} — {count} candidates")
    if count < 800:
        raise SystemExit(f"Count {count} < 800")


if __name__ == "__main__":
    main()
