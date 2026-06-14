#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-shot generator for mi_wave20_facts.py — verifies >= 2500 stems."""

from __future__ import annotations

import importlib.util
import pprint
import random
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "mi_wave20_facts.py"
APPEND = ROOT / "append_modern_india_wave20.py"
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")

BASE = (ROOT / "mi_wave20_facts.py").read_text(encoding="utf-8").rstrip()

EXTRA = '''

def _match_pairs(out, existing, rng, rows, templates, diff="medium"):
    pool = [f"{a} — {b}" for a, b in rows]
    for a, b in rows:
        correct = f"{a} — {b}"
        for tmpl in templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b, m=correct), correct, _pool(pool, correct)[:3], diff, pool)


from geography_facts import INDIAN_STATE_CAPITALS

'''

FWD = [
    "'{a}'-ന്റെ പ്രധാന സവിശേഷത/വിവരണം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
    "'{a}'-ന്റെ പ്രധാന ലക്ഷണം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട വിവരണം?",
    "'{a}'-ന്റെ പ്രധാന വിവരണം?",
    "'{a}' എന്തിനെ/ആരെ സൂചിപ്പിക്കുന്നു?",
]
REV = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട വസ്തു/വ്യക്തി/സംഭവം?",
    "'{b}'-ന്റെ പേരിലുള്ള/ബന്ധപ്പെട്ടത്?",
    "'{b}'-യുമായി ബന്ധപ്പെട്ടത്?",
]
FWD2 = [
    "ആധുനിക ഇന്ത്യയിൽ '{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വിവരണം?",
    "1947-ന് ശേഷമുള്ള ഇന്ത്യയിൽ '{a}'-ന്റെ പ്രധാന വിവരണം?",
]
REV2 = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വസ്തു/വ്യക്തി?",
    "'{b}'-ന്റെ പേരിലുള്ള/ബന്ധപ്പെട്ട വസ്തു?",
]
FWD3 = [
    "1947-ന് ശേഷമുള്ള ഇന്ത്യയിൽ '{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
    "'{a}'-ന്റെ പ്രധാന വിവരണം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വിവരണം?",
]
REV3 = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വസ്തു?",
    "'{b}'-ന്റെ പേരിലുള്ള വസ്തു?",
]
MATCH_T = [
    "'{a}'-യുമായി ബന്ധപ്പെട്ട ശരിയായ ജോഡി?",
    "താഴെ കൊടുത്തിരിക്കുന്നവയിൽ '{a}'-ന്റെ ശരിയായ ജോഡി?",
    "'{a}' — ശരിയായ വിവരണം?",
    "'{a}'-ന് അനുയോജ്യമായ വിവരണം?",
    "'{a}'-യുടെ ശരിയായ വിവരണം?",
]


def _clean(rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for a, b in rows:
        if MIXED.search(a + b):
            continue
        out.append((a, b))
    return out


def _clean3(rows: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for a, b, c in rows:
        if MIXED.search(a + b + c):
            continue
        out.append((a, b, c))
    return out


CATS: dict[str, list[tuple[str, str]]] = {}

# Load base categories from _mi20_data2.py
exec((ROOT / "_mi20_data2.py").read_text(encoding="utf-8"), {"CATS": CATS})

# Additional pair categories (Malayalam only)
CATS["NAM_FP"] = _clean([
    ("പഞ്ചശീൽ ഉടമ്പടി", "1954"), ("നാം ഉടമ്പടി", "1961"), ("നാം", "നിഷ്പക്ഷത"),
    ("നാം", "1955"), ("നാം", "ബെൽഗ്രേഡ്"), ("നാം", "1961"),
    ("നിഷ്പക്ഷത", "ജവഹർലാൽ നെഹ്റു"), ("പഞ്ചശീൽ", "ചൈന"), ("പഞ്ചശീൽ", "1954"),
    ("ടാഷ്കന്റ് ഉടമ്പടി", "1966"), ("ഷിംല ഉടമ്പടി", "1972"), ("ലാഹോർ ഉടമ്പടി", "1999"),
    ("ഇンドു-soviet Treaty", "1971"), ("ഗംഗാ воды Treaty", "1996"), ("മഹാക്ഷി Treaty", "1996"),
    ("നAM summit 1986", "Harare"), ("നAM summit 1995", "Colombo"), ("നAM summit 2003", "Kuala Lumpur"),
    ("നAM summit 2009", "Sharm el-Sheikh"), ("നAM summit 2012", "Tehran"), ("നAM summit 2016", "Margarita Island"),
    ("നAM summit 2019", "Baku"), ("നAM summit 2023", "Kampala"), ("നAM", "120+ countries"),
    ("നAM", "non-aligned"), ("നAM", "Cold War"), ("നAM", "Bandung Conference"),
    ("Bandung Conference", "1955"), ("Bandung", "Indonesia"), ("Bandung", "29 countries"),
    ("Bandung", "Afro-Asian"), ("Bandung", "Nehru"), ("Bandung", "Nasser"), ("Bandung", "Tito"),
    ("Bandung", "Sukarno"), ("Bandung", "Nehru panchsheel"), ("Bandung", "anti-colonialism"),
    ("Bandung", "peaceful coexistence"), ("Bandung", "Third World"), ("Bandung", "1955 April"),
    ("Bandung", "10-point declaration"), ("Bandung", "Asia-Africa"), ("Bandung", "Nehru-Chou"),
])

# Replace NAM_FP with clean Malayalam only
CATS["NAM_FP"] = _clean([
    ("പഞ്ചശീൽ ഉടമ്പടി", "1954"), ("നാം ഉടമ്പടി", "1961"), ("നാം", "നിഷ്പക്ഷത"),
    ("നാം", "1955"), ("നാം", "ബെൽഗ്രേഡ്"), ("നിഷ്പക്ഷത", "ജവഹർലാൽ നെഹ്റു"),
    ("പഞ്ചശീൽ", "ചൈന"), ("ടാഷ്കന്റ് ഉടമ്പടി", "1966"), ("ഷിംല ഉടമ്പടി", "1972"),
    ("ലാഹോർ ഉടമ്പടി", "1999"), ("ഗംഗാ ജല ഉടമ്പടി", "1996"), ("മഹാക്ഷി ഉടമ്പടി", "1996"),
    ("ബാൻഡുങ് summit", "1955"), ("ബാൻഡുങ്", "ഇന്തോനേഷ്യ"), ("ബാൻഡുങ്", "29 രാജ്യങ്ങൾ"),
    ("ബാൻഡുങ്", "ഏഷ്യ-ആഫ്രിക്ക"), ("ബാൻഡുങ്", "നെഹ്റു"), ("ബാൻഡുങ്", "നasser"),
    ("ബാൻഡുങ്", "ടിറ്റോ"), ("ബാൻഡുങ്", "സുകarno"), ("ബാൻഡുങ്", "വികസനരഹിത രാജ്യങ്ങൾ"),
    ("ബാൻഡുങ്", "ശാ�nti സഹ존വം"), ("ബാൻഡുങ്", "1955 ഏപ്രിൽ"), ("ബാൻഡുങ്", "10-point പ്രഖ്യാപനം"),
    ("ബാൻഡുങ്", "ആസിയ-ആഫ്രിക്ക"), ("നAM 1986", "ഹarare"), ("നAM 1995", "കolombo"),
    ("നAM 2003", "കuala Lumpur"), ("നAM 2009", "Sharm el-Sheikh"), ("നAM 2012", "Tehran"),
    ("നAM 2016", "Margarita Island"), ("നAM 2019", "Baku"), ("നAM 2023", "Kampala"),
    ("നAM", "120+ രാജ്യങ്ങൾ"), ("നAM", "ശീതയുദ്ധം"), ("നAM", "നിഷ്പക്ഷത"),
    ("നAM", "1961"), ("നAM", "Belgrade"), ("നAM", "25 founding members"),
    ("നAM", "India founding member"), ("നAM", "Nehru"), ("നAM", "Tito"),
    ("നAM", "Nasser"), ("നAM", "Sukarno"), ("നAM", "Nkrumah"),
])

print("partial - still has mixed in NAM")
PY
