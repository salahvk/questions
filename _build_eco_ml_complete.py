#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble complete _gen_economics_ml_rest.py from head + tail."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "_gen_economics_ml_rest.py"

ALLOWED = re.compile(
    r"\b(RBI|SEBI|GST|IMF|WTO|CPI|GDP|FDI|FII|HDI|MSP|NPS|UPI|NPCI|FRBM|SEZ|PLI|PMJDY|"
    r"FCI|NABARD|APMC|PMFBY|CACP|KCC|NPOP|EPFO|ESIC|PMKVY|PLFS|NSDL|CDSL|"
    r"IPO|FPO|ETF|QIP|ADR|GDR|LIC|IRDAI|ULIP|PFRDA|PMJJBY|PMSBY|PMJAY|GIC|"
    r"CCI|STPI|EOU|CGST|SGST|IGST|GSTN|CBDT|CBIC|GAAR|DTAA|UIDAI|DBT|OCEN|ONDC|"
    r"PMKISAN)\b",
    re.I,
)
LATIN4 = re.compile(r"[a-zA-Z]{4,}")
E, M, H = "ലളിതം", "മധ്യം", "കഠിനം"


def validate(row, name: str) -> None:
    s = ALLOWED.sub("", "".join(map(str, row)))
    m = LATIN4.search(s)
    if m:
        raise SystemExit(f"LEAK {name} {m.group()!r} in {row!r}")


def emit(name: str, hint: str, rows: list) -> str:
    for r in rows:
        validate(r, name)
    lines = [f"{name}: list[{hint}] = ["]
    lines += [f"    {r!r}," for r in rows]
    lines.append("]")
    return "\n".join(lines)


# --- tail data (pure Malayalam) ---
INSURANCE_INST = [
    ("LIC", " ജീവിത ഇൻഷുറൻസ്"),
    ("IRDAI", " ഇൻഷുറൻസ് നിയന്ത്രണം"),
    ("EPFO", " തൊഴിലാളി ഭവിഷ്യ നിധി"),
    ("NPS", " ദേശീയ പെൻഷൻ"),
    ("PFRDA", " പെൻഷൻ നിയന്ത്രണം"),
    ("PMJJBY", " ജീവൻ ഇൻഷുറൻസ് പദ്ധതി"),
    ("PMSBY", " അപകട ഇൻ shutil"),
    ("PMJAY", " ആരോഗ്യ ഇൻ shutil"),
    ("GIC", " പുനരിശ്വാസന"),
    ("ULIP", " യൂണിറ്റ് ലിങ്ക് ഇൻ shutil"),
]
INSURANCE_INST = [(a, b.replace("shutil", "ഷുറൻസ്")) for a, b in INSURANCE_INST]

ECONOMIC_THINKERS = [
    ("ദേശത്തിന്റെ സമ്പത്ത് രചിച്ചത്?", "ആഡം സ്മിത്ത്", ["കാൾ മാർക്സ്", "ജോൺ മെയിൻാർഡ് കെയ്ൻസ്", "ഡേവിഡ് റിക്കാർഡോ"], M),
    ("മൂലധനം രചിച്ചത്?", "കാൾ മാർക്സ്", ["ആഡം സ്മിത്ത്", "ആൽഫ്രഡ് മാർഷൽ", "മിൽട്ടൺ ഫ്രീഡ്മാൻ"], M),
    ("പൊതു സിദ്ധാന്തം രചിച്ചത്?", "ജോൺ മെയിൻാർഡ് കെയ്ൻസ്", ["ആഡം സ്മിത്ത്", "ഡേവിഡ് റിക്കാർഡോ", "ഫ്രെഡറിക് ഹയേക്ക്"], M),
    ("സാമ്പത്തികശാസ്ത്രത്തിന്റെ തത്വങ്ങൾ രചിച്ചത്?", "ആൽഫ്രഡ് മാർഷൽ", ["ആഡം സ്മിത്ത്", "കാൾ മാർക്സ്", "തോമസ് മാൽത്തസ്"], H),
    ("താരതമ്യ മേന്മ സിദ്ധാന്തം?", "ഡേവിഡ് റിക്കാർഡോ", ["ആഡം സ്മിത്ത്", "കാൾ മാർക്സ്", "ജോൺ മെയിൻാർഡ് കെയ്ൻസ്"], M),
    ("അദൃശ്യ കൈ ആശയം?", "ആഡം സ്മിത്ത്", ["കാൾ മാർക്സ്", "ജോൺ മെയിൻാർഡ് കെയ്ൻസ്", "അമർത്യ സെൻ"], M),
    ("കുറഞ്ഞ ഇടപെടൽ വാദി?", "ആഡം സ്മിത്ത്", ["കാൾ മാർക്സ്", "ജോൺ മെയിൻാർഡ് കെയ്ൻസ്", "ദാദാഭായി നൗറോജി"], H),
    ("അധികമൂല്യ സിദ്ധാന്തം?", "കാൾ മാർക്സ്", ["ആഡം സ്മിത്ത്", "ആൽഫ്രഡ് മാർഷൽ", "മിൽട്ടൺ ഫ്രീഡ്മാൻ"], H),
    ("നാണയവാദത്തിന്റെ വക്താവ്?", "മിൽട്ടൺ ഫ്രീഡ്മാൻ", ["ജോൺ മെയിൻാർഡ് കെയ്ൻസ്", "കാൾ മാർക്സ്", "അമർത്യ സെൻ"], M),
    ("അടിമത്വത്തിലേക്കുള്ള വഴി രചിച്ചത്?", "ഫ്രെഡറിക് ഹയേക്ക്", ["ജോൺ മെയിൻാർഡ് കെയ്ൻസ്", "കാൾ മാർക്സ്", "ആഡം സ്മിത്ത്"], H),
    ("പൊതു നാശം സിദ്ധാന്തം?", "ഗാരെറ്റ് ഹാർഡിൻ", ["ആഡം സ്മിത്ത്", "കാൾ മാർക്സ്", "ഡേവിഡ് റിക്കാർഡോ"], H),
    ("തടവുകാരന്റെ ദുരന്തം?", "ഗെയിം തിയറി ആശയം", ["നാണയ സിദ്ധാന്തം", "വ്യാപാര സിദ്ധാന്തം", "തൊഴിൽ സിദ്ധാന്തം"], H),
    ("സാമർത്ഥ്യ സമീപനം?", "അമർത്യ സെൻ", ["ജോൺ മെയിൻാർഡ് കെയ്ൻസ്", "ആഡം സ്മിത്ത്", "കാൾ മാർക്സ്"], H),
    ("ഹിന്ദ് സ്വരാജ് സാമ്പത്തിക വിമർശനം?", "മഹാത്മാ ഗാന്ധി", ["ജവഹർലാൽ നെഹru", "സി. രാജഗോപാലാചാരി", "ബി. ആർ. അംbedkar"], H),
]

print(len(ECONOMIC_THINKERS))
