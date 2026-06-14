#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Complete MI wave-20 data files and run _finish_mi20.py."""

from __future__ import annotations

import pprint
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def dp(rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    out, seen = [], set()
    for a, b in rows:
        if MIXED.search(a + b):
            continue
        t = (a.strip(), b.strip())
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def dt(rows: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    out, seen = [], set()
    for a, b, c in rows:
        if MIXED.search(a + b + c):
            continue
        t = (a.strip(), b.strip(), c.strip())
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


# Load partial CATS from _write_mi20_modules.py (through AMENDMENTS)
CATS: dict[str, list[tuple[str, str]]] = {}
ns = {"CATS": CATS, "dp": dp, "ORD": {}, "AMEND_YEARS": {}, "INDIAN_STATE_CAPITALS": []}
src = (ROOT / "_write_mi20_modules.py").read_text(encoding="utf-8")
# exec only up to AMENDMENTS block end
cut = src.split('CATS["JUDICIAL"]')[0]
exec(cut, ns)  # noqa: S102
CATS = ns["CATS"]

CATS["JUDICIAL"] = dp([
    ("കേശവാനന്ദ ഭാരതി വാദം", "1973"), ("കേശവാനന്ദ ഭാരതി വാദം", "മൗലിക ഘടന"),
    ("ഗോൾക്ക് നാഥ് വാദം", "1967"), ("ഗോൾക്ക് നാഥ് വാദം", "ഭരണഘടനാ ഭേദഗതി"),
    ("മിനർവ പന്നീർസെൽഫൻ വാദം", "1974"), ("മിനർവ പന്നീർസെൽഫൻ വാദം", "മൗലിക ഘടന"),
    ("എസ്.ആർ. ബോമ്മൈ വാദം", "1994"), ("എസ്.ആർ. ബോമ്മൈ വാദം", "സംസ്ഥാന ഭരണം"),
    ("വിശാഖാ വാദം", "1997"), ("വിശാഖാ വാദം", "ലൈംഗികാതിക്രമം"),
    ("അയോധ്യാ വാദം", "2019"), ("അയോധ്യാ വാദം", "രാമജന്മഭൂമി"),
    ("എ.കെ. ഗോപാലൻ വാദം", "1950"), ("എ.കെ. ഗോപാലൻ വാദം", "നിയമപാലനം"),
    ("മാണിക്കം വാദം", "1978"), ("മാണിക്കം വാദം", "അടിയന്തരാവസ്ഥ"),
    ("എം.സി. മെഹ്താ വാദം", "1986"), ("എം.സി. മെഹ്താ വാദം", "പരിസ്ഥിതി"),
    ("ഓള ഫാക്ടറി വാദം", "1986"), ("ഓള ഫാക്ടറി വാദം", "പരിസ്ഥിതി"),
    ("ഇന്ത്യാ സീമൻസ് വാദം", "1986"), ("ഇന്ത്യാ സീമൻസ് വാദം", "പരിസ്ഥിതി"),
    ("എം.സി. മെഹ്താ വാദം", "ഗംഗാ"), ("എം.സി. മെഹ്താ വാദം", "താജ്മഹൽ"),
    ("എം.സി. മെഹ്താ വാദം", "വാഹനം"), ("എം.സി. മെഹ്താ വാദം", "വായു മലിനീകരണം"),
    ("എം.സി. മെഹ്താ വാദം", "ജല മലിനീകരണം"), ("എം.സി. മെഹ്താ വാദം", "കടൽ മലിനീകരണം"),
    ("എം.സി. മെഹ്താ വാദം", "കടൽ തീരം"), ("എം.സി. മെഹ്താ വാദം", "കടൽ"),
    ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "1978"), ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "അടിയന്തരാവസ്ഥ"),
    ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "1975"), ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "അടിയന്തരാവസ്ഥ"),
    ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "1975"), ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "അടിയന്തരാവസ്ഥ"),
    ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "1975"), ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "അടിയന്തരാവസ്ഥ"),
    ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "1975"), ("എം.എച്ച്. ഹൊസ്ബെറ്റt വാദം", "അടിയന്തരാവസ്ഥ"),
])

print("loaded", {k: len(v) for k, v in CATS.items()})
