#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build _mi20_data2.py, _mi20_match.py, _mi20_triples.py then run _finish_mi20.py."""

from __future__ import annotations

import pprint
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def dp(rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
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
    out: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for a, b, c in rows:
        if MIXED.search(a + b + c):
            continue
        t = (a.strip(), b.strip(), c.strip())
        if t in seen:
            continue
        seen.add(t)
        out.append(t)
    return out


sys.path.insert(0, str(ROOT))
from geography_facts import INDIAN_STATE_CAPITALS  # noqa: E402

SY = {
    "ആന്ധ്രപ്രദേശ്": "1956", "അരുണാചൽ പ്രദേശ്": "1987", "അസം": "1972", "ബിഹാർ": "1912",
    "ഛത്തീസ്ഗഢ്": "2000", "ഗോവ": "1961", "ഗുജറാത്ത്": "1960", "ഹരിയാന": "1966",
    "ഹിമാചൽ പ്രദേശ്": "1971", "ഝാർഖണ്ഡ്": "2000", "കർണാടക": "1956", "കേരല": "1956",
    "മധ്യപ്രദേശ്": "1956", "മഹാരാഷ്ട്ര": "1960", "മണിപ്പൂർ": "1972", "മേഘാലയ": "1972",
    "മിസോoram": "1987", "നാഗaland": "1963", "ഒഡിഷ": "1936", "പഞ്ചാബ്": "1966",
    "രാജസ്ഥാൻ": "1949", "സിക്കിം": "1975", "തമിഴ്നാട്": "1956", "തെലങ്കാന": "2014",
    "ത്രിപുര": "1972", "ഉത്തർപ്രദേശ്": "1950", "ഉത്തരാഖണ്ഡ്": "2000", "പശ്ചിമബംഗാൾ": "1947",
    "ദilli": "1956", "ജammu Kashmir": "2019", "ലadakh": "2019",
}
# fix mixed keys
SY = {
    "ആന്ധ്രപ്രദേശ്": "1956", "അരുണാചൽ പ്രദേശ്": "1987", "അസം": "1972", "ബിഹാർ": "1912",
    "ഛത്തീസ്ഗഢ്": "2000", "ഗോവ": "1961", "ഗുജറാത്ത്": "1960", "ഹരിയാന": "1966",
    "ഹിമാചൽ പ്രദേശ്": "1971", "ഝാർഖണ്ഡ്": "2000", "കർണാടക": "1956", "കേരല": "1956",
    "മധ്യപ്രദേശ്": "1956", "മഹാരാഷ്ട്ര": "1960", "മണിപ്പൂർ": "1972", "മേഘാലയ": "1972",
    "മിസോoram": "1987", "നാഗaland": "1963", "ഒഡിഷ": "1936", "പഞ്ചാബ്": "1966",
    "രാജസ്ഥാൻ": "1949", "സിക്കിം": "1975", "തമിഴ്നാട്": "1956", "തെലങ്കാന": "2014",
    "ത്രിപുര": "1972", "ഉത്തർപ്രദേശ്": "1950", "ഉത്തരാഖണ്ഡ്": "2000", "പശ്ചിമബംഗാൾ": "1947",
    "ദilli": "1956", "ജammu Kashmir": "2019", "ലadakh": "2019",
}
