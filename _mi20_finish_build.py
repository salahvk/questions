#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Finish MI wave-20 data files and run _finish_mi20.py."""

from __future__ import annotations

import pprint
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def dp(rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    out, seen = [], set()
    for a, b in rows:
        if MIXED.search(a + b):
            continue
        t = (a.strip(), b.strip())
        if t in seen:
            continue
        seen.add(t)
        out.append(t)
    return out


def dt(rows: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    out, seen = [], set()
    for a, b, c in rows:
        if MIXED.search(a + b + c):
            continue
        t = (a.strip(), b.strip(), c.strip())
        if t in seen:
            continue
        seen.add(t)
        out.append(t)
    return out


CATS: dict[str, list[tuple[str, str]]] = {}
code = (ROOT / "_write_mi20_modules.py").read_text(encoding="utf-8")
code = code.replace("Path(__file__).parent", f"Path({str(ROOT)!r})")
code = code.split('CATS["JUDICIAL"]')[0]
g: dict = {"CATS": CATS, "dp": dp, "Path": Path, "re": re, "sys": sys, "pprint": pprint, "ROOT": ROOT}
exec(code, g)  # noqa: S102
CATS = g["CATS"]

# Fix JUDICIAL — unique pairs only
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
    ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "1975"), ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "കർണാടക"),
    ("എ.ഡി.എം. ജബ്ബൽപൂർ വാദം", "1976"), ("എ.ഡി.എം. ജബ്ബൽപൂർ വാദം", "അടിയന്തരാവസ്ഥ"),
    ("എ.ഡി.എം. ജബ്ബൽപൂർ വാദം", "മൗലിക അവകാശങ്ങൾ"), ("എ.ഡി.എം. ജബ്ബൽപൂർ വാദം", "സുപ്രീം കോടതി"),
    ("മനേക്ക ഗാന്ധി വാദം", "1978"), ("മനേക്ക ഗാന്ധി വാദം", "മൗലിക അവകാശം"),
    ("മനേക്ക ഗാന്ധി വാദം", "പാസ്പോർട്ട്"), ("മനേക്ക ഗാന്ധി വാദം", "നീതി"),
    ("ബെറുബാരി വാദം", "1960"), ("ബെറുബാരി വാദം", "അതിർത്തി"),
    ("ബെറുബാരി വാദം", "പശ്ചിമ ബംഗാൾ"), ("ബെറുബാരി വാദം", "ഭൂപ്രദേശം"),
    ("ഇന്ദിരാ ഗാന്ധി വാദം", "1975"), ("ഇന്ദിരാ ഗാന്ധി വാദം", "തിരഞ്ഞെടുപ്പ്"),
    ("ഇന്ദിരാ ഗാന്ധി വാദം", "രാജ് നാരായൺ"), ("ഇന്ദിരാ ഗാന്ധി വാദം", "അടിയന്തരാവസ്ഥ"),
    ("ഷഹ് ബാനു വാദം", "1985"), ("ഷഹ് ബാനു വാദം", "മുസ്ലിം വ്യക്തിനിയമം"),
    ("ഷഹ് ബാനു വാദം", "സ്ത്രീകൾ"), ("ഷഹ് ബാനു വാദം", "വിവാഹമോചനം"),
    ("റംജിത്ത് സർക്കാർ വാദം", "2007"), ("റംജിത്ത് സർക്കാർ വാദം", "സാമൂഹിക നീതി"),
    ("റംജിത്ത് സർക്കാർ വാദം", "പിന്നാക്ക വിഭാഗങ്ങൾ"), ("റംജിത്ത് സർക്കാർ വാദം", "സംവരണം"),
    ("വി.വി. ഗിരി വാദം", "1971"), ("വി.വി. ഗിരി വാദം", "തിരഞ്ഞെടുപ്പ്"),
    ("അശോക കുമാർ വാദം", "1991"), ("അശോക കുമാർ വാദം", "സി.ബി.ഐ."),
    ("ഉൾത്തർ പ്രദേശ് കമ്മീഷണറി വാദം", "1991"), ("ഉൾത്തർ പ്രദേശ് കമ്മീഷണറി വാദം", "പഞ്ചായത്ത് രാജ്"),
    ("സബ്പിജി വാദം", "1993"), ("സബ്പിജി വാദം", "ഭരണഘടന"),
    ("ചമ്പകം ദൊർവൈർ വാദം", "1971"), ("ചമ്പകം ദൊർവൈർ വാദം", "ശബരിമല"),
    ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "സുപ്രീം കോടതി"), ("എം.എച്ച്. ഹൊസ്ബെറ്റ് വാദം", "കർണാടക"),
])

exec((ROOT / "_mi20_cats_rest.py").read_text(encoding="utf-8"), {"CATS": CATS, "dp": dp, "dt": dt})  # noqa: S102

MATCH_ROWS: list[tuple[str, str]] = []
exec((ROOT / "_mi20_match_data.py").read_text(encoding="utf-8"), {"MATCH_ROWS": MATCH_ROWS, "dp": dp})  # noqa: S102

TRIPLES: dict[str, list[tuple[str, str, str]]] = {}
exec((ROOT / "_mi20_triples_data.py").read_text(encoding="utf-8"), {"TRIPLES": TRIPLES, "dt": dt})  # noqa: S102

data2 = "# -*- coding: utf-8 -*-\n\"\"\"Extended pair categories — exec into CATS.\"\"\"\n\n"
for name, rows in CATS.items():
    data2 += f"CATS['{name}'] = {pprint.pformat(rows, width=120)}\n\n"
(ROOT / "_mi20_data2.py").write_text(data2, encoding="utf-8")

match_py = "# -*- coding: utf-8 -*-\n\"\"\"Match pairs — exec into MATCH_ROWS.\"\"\"\n\n"
match_py += "MATCH_ROWS.extend(" + pprint.pformat(MATCH_ROWS, width=120) + ")\n"
(ROOT / "_mi20_match.py").write_text(match_py, encoding="utf-8")

triples_py = "# -*- coding: utf-8 -*-\n\"\"\"Triple rows — exec into TRIPLES.\"\"\"\n\n"
for name, rows in TRIPLES.items():
    triples_py += f"TRIPLES['{name}'] = {pprint.pformat(rows, width=120)}\n\n"
(ROOT / "_mi20_triples.py").write_text(triples_py, encoding="utf-8")

print("CATS counts:", {k: len(v) for k, v in CATS.items()})
print("MATCH_ROWS:", len(MATCH_ROWS))
print("TRIPLES PARTIES:", len(TRIPLES.get("PARTIES", [])))

r = subprocess.run([sys.executable, str(ROOT / "_finish_mi20.py")], cwd=ROOT)
sys.exit(r.returncode)
