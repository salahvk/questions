#!/usr/bin/env python3
"""Write complete ML_BLOCK to _eco_ml_patch_data.py."""
from __future__ import annotations

from pathlib import Path

import _build_eco_ml_block as blk

Fact = tuple[str, str, list[str], str]
Pair = tuple[str, str]
Triple = tuple[str, str, str]


def _line(stem: str, ans: str, wrong: list[str], diff: str = "medium") -> str:
    return f'    _f({stem!r}, {ans!r}, {wrong!r}, {diff!r}),'


def _cat(name: str, facts: list[Fact]) -> str:
    lines = [f"{name}: list[Fact] = ["]
    lines.extend(_line(*f) for f in facts)
    lines.append("]")
    return "\n".join(lines)


def _pairs(name: str, rows: list[Pair]) -> str:
    lines = [f"{name}: list[Pair] = ["]
    for a, b in rows:
        lines.append(f"    ({a!r}, {b!r}),")
    lines.append("]")
    return "\n".join(lines)


def _triples(name: str, rows: list[Triple]) -> str:
    lines = [f"{name}: list[Triple] = ["]
    for a, b, c in rows:
        lines.append(f"    ({a!r}, {b!r}, {c!r}),")
    lines.append("]")
    return "\n".join(lines)


# Fix FISCAL english stems in imported data
FISCAL_FIXED: list[Fact] = []
for stem, ans, wrong, diff in blk.FISCAL_DEFICIT:
    fixes = {
        "ധനകാര്യ konsolidation?": "ധനകാര്യ ഏകീകരണം?",
        "crowding out?": "സർക്കാർ വായ്പയുടെ crowding out?",
        "crowding in?": "സർക്കാർ ചെലവിന്റെ crowding in?",
        "പ retrogressive നികുതി?": "പ retrogressive നികുതി?",
        "Appropriation Bill?": "Appropriation Bill?",
        "Consolidated Fund?": "Consolidated Fund?",
        "Public Account?": "Public Account?",
        "അ contingencies Fund?": "അ contingencies Fund?",
    }
    # rewrite problematic rows entirely below instead
    FISCAL_FIXED.append((stem, ans, wrong, diff))

FISCAL_DEFICIT: list[Fact] = [
    ("ധനകമ്മി എന്നാൽ?", "മൊത്ത ചെലവ് − മൊത്ത വരുമാനം (വായ്പ ഒഴികെ)", ["വരുമാന കമ്മി മാത്രം", "പ്രാഥമിക കമ്മി മാത്രം", "വ്യാപാര കമ്മി"], "medium"),
    ("വരുമാന കമ്മി എന്നാൽ?", "വരുമാന ചെലവ് − വരുമാന വരുമാനം", ["മൂലധന കമ്മി", "ധനകമ്മി മിച്ചം", "വ്യാപാര കമ്മി"], "medium"),
    ("പ്രാഥമിക കമ്മി?", "ധനകമ്മി − പലിശ ചെലവ്", ["ധനകമ്മി + പലിശ", "വരുമാന കമ്മി മാത്രം", "മൂലധന കമ്മി മാത്രം"], "hard"),
    ("FRBM നിയമത്തിന്റെ ലക്ഷ്യം?", "ധനകാര്യ ശാസ്ത്രബദ്ധത", ["വ്യാപാര പ്രോത്സാഹനം", "നാണയ വിപുലീകരണം", "സ്വകാര്യവൽക്കരണം മാത്രം"], "medium"),
    ("FRBM ധനകമ്മി ലക്ഷ്യം?", "GDP-യുടെ 3%", ["GDP-യുടെ 10%", "GDP-യുടെ 0%", "GDP-യുടെ 20%"], "hard"),
    ("മൂലധന ചെലവിന്റെ ഉദാഹരണം?", "അടിസ്ഥാന സൗകര്യ ചെലവ്", ["ശമ്പളം", "സബ്സിഡി", "പലിശ"], "medium"),
    ("വരുമാന ചെലവിന്റെ ഉദാഹരണം?", "ശമ്പളം", ["റോഡ് നിർമ്മാണം", "അണക്കെട്ട്", "റെയിൽവേ മൂലധന"], "easy"),
    ("മൂലധന വരുമാനത്തിന്റെ ഉദാഹരണം?", "സ്വത്ത് വിൽപ്പന", ["വരുമാന നികുതി", "GST", "കസ്റ്റംസ്"], "medium"),
    ("വരുമാന വരുമാനത്തിന്റെ ഉദാഹരണം?", "നികുതി വരുമാനം", ["വായ്പ", "സ്വത്ത് വിൽപ്പന", "വായ്പാ തിരിച്ചെടുപ്പ്"], "easy"),
    ("ധനകാര്യ ഏകീകരണം?", "ധനകമ്മി കുറയ്ക്കൽ", ["കമ്മി വർദ്ധന", "വായ്പ മാത്രം വർദ്ധന", "നികുതി നീക്കം"], "medium"),
    ("സർക്കാർ വായ്പയുടെ തള്ളിക്ക挤出?", "പലിശ നിരക്ക് ഉയരൽ", ["പലിശ കുറവ്", "സ്വകാര്യ നിക്ഷേപം എപ്പോഴും വർദ്ധന", "പണപ്പെരുപ്പം എപ്പോഴും കുറവ്"], "hard"),
    ("സർക്കാർ ചെലവിന്റെ പ്രേരണ?", "സ്വകാര്യ നിക്ഷേപം പ്രോത്സാഹനം", ["സ്വകാര്യ നിക്ഷേപം കുറവ്", "പലിശ എപ്പോഴും ഉയരൽ", "GDP കുറവ്"], "hard"),
    ("പൊതു കടം?", "സർക്കാർ സഞ്ചിത വായ്പ", ["സ്വകാര്യ കടം", "വ്യാപാര കടം", "ഗാർഹിക സമ്പാദ്യം"], "medium"),
    ("കട-GDP അനുപാതം?", "പൊതു കടം GDP-യോട് ബന്ധപ്പെട്ട്", ["വ്യാപാര-GDP", "CPI-GDP", "HDI-GDP"], "medium"),
    ("ബജറ്റ് പുറത്തുള്ള വായ്പ?", "ബജറ്റിൽ ഉൾപ്പെടാത്ത ബാധ്യത", ["ബജറ്റിൽ മാത്രം", "നികുതി വരുമാനം", "GST ശേഖരണം"], "hard"),
    ("സബ്സിഡി?", "വില കുറയ്ക്കാൻ സർക്കാർ പണം", ["നികുതി വർദ്ധന", "തീരുവ വർദ്ധന", "പലിശ"], "easy"),
    ("നേരിട്ടുള്ള നികുതിയുടെ ഉദാഹരണം?", "വരുമാന നികുതി", ["GST", "കസ്റ്റംസ്", "Excise"], "easy"),
    ("പരോക്ഷ നികുതിയുടെ ഉദാഹരണം?", "GST", ["വരുമാന നികുതി", "കorporat നികുതി", "സമ്പത്ത് നികുതി"], "easy"),
    ("പുരോഗമന നികുതി?", "വരുമാനം കൂടുമ്പോൾ നിരക്ക് കൂടും", ["ഫ്ലാറ്റ് നിരക്ക്", "പ retrogressive", "നികുതിയില്ല"], "medium"),
    ("പ retrogressive നികുതി?", "ഭാരം ദരിദ്രരിൽ കൂടുതൽ", ["സമ്പന്നരിൽ കൂടുതൽ", "ആനുപാതിക", "നികുതിയില്ല"], "medium"),
]
