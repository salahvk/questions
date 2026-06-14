"""Sports governing-body org classification and stem/answer consistency checks."""

from __future__ import annotations

import re

# Indian national federations / bodies (answer when stem asks ഭാരതീയ അധികാര സംഘടന).
INDIAN_GOV_ORGS: frozenset[str] = frozenset({
    "BCCI",
    "AIFF",
    "BAI",
    "IOA",
    "NADA",
    "SAI",
    "PCI",
    "PKFI",
    "ഹോക്കി ഇന്ത്യ",
})

# International federations (answer when stem asks അന്താരാഷ്ട്ര സംഘടന).
INTERNATIONAL_GOV_ORGS: frozenset[str] = frozenset({
    "ICC",
    "FIFA",
    "FIH",
    "FIDE",
    "BWF",
    "ITTF",
    "ISSF",
    "UWW",
    "IBA",
    "FIVB",
    "FIBA",
    "IWF",
    "WADA",
    "IHF",
    "ലോക അത്ലറ്റിക്സ് ഫെഡറേഷൻ",
    "ലോക വില്ലുവെട്ട് ഫെഡറേഷൻ",
})

STEM_INDIAN_GOV = re.compile(r"ഭാരതീയ (അധികാര )?സംഘടന")
STEM_INTL_GOV = re.compile(r"അന്താരാഷ്ട്ര സംഘടന")
STEM_DOUBLE_PREFIX = re.compile(r"(ദേശീയ ദേശീയ|അന്താരാഷ്ട്ര അന്താരാഷ്ട്ര)")


def is_indian_gov_org(org: str) -> bool:
    return org in INDIAN_GOV_ORGS


def sports_gov_body_issue(question: str, answer: str) -> str | None:
    """Return issue code if governing-body stem contradicts the marked answer."""
    if STEM_DOUBLE_PREFIX.search(question):
        return "gov_body:double_prefix_stem"
    if STEM_INDIAN_GOV.search(question) and answer in INTERNATIONAL_GOV_ORGS:
        return f"gov_body:indian_stem_intl_answer:{answer}"
    if STEM_INTL_GOV.search(question) and answer in INDIAN_GOV_ORGS:
        return f"gov_body:intl_stem_indian_answer:{answer}"
    return None
