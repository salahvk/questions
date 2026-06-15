#!/usr/bin/env python3
"""One-shot: write important_institutions_wave30_facts.py with 800+ candidates."""
from __future__ import annotations

import importlib.util
import pprint
import random
import re
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "important_institutions_wave30_facts.py"

spec = importlib.util.spec_from_file_location("g", ROOT / "_gen_ii_wave30.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)  # type: ignore[union-attr]

PAIRS: dict[str, list[tuple[str, str]]] = {
    "HQ_PAIRS": g.HQ_PAIRS,
    "KERALA_HQ_PAIRS": list(dict.fromkeys(g.KERALA_HQ_PAIRS)) + [
        ("കേരള സംസ്ഥാന മലിനീകരണ നിയന്ത്രണ ബോർഡ്", "തിരുവനന്തപുരം"),
        ("കerala സംസ്ഥാന ജൈവവൈവിധ്യ ബോർഡ്", "തിരുവനന്തപുരം"),
    ],
    "ESTABLISH_YEAR": g.ESTABLISH_YEAR,
}

# fix kerala biodiversity - pure Malayalam
PAIRS["KERALA_HQ_PAIRS"] = list(dict.fromkeys(g.KERALA_HQ_PAIRS)) + [
    ("കേരള സംസ്ഥാന മലിനീകരണ നിയന്ത്രണ ബോർഡ്", "തിരുവനന്തപുരം"),
    ("കerala സംസ്ഥാന ജൈവവൈവിധ്യ ബോർഡ്", "തിരുവനന്തപുരം"),
]
PAIRS["KERALA_HQ_PAIRS"] = list(dict.fromkeys(g.KERALA_HQ_PAIRS)) + [
    ("കേരള സംസ്ഥാന മലിനീകരണ നിയന്ത്രണ ബോർഡ്", "തിരുവനന്തപുരം"),
    ("കerala സംസ്ഥാന ജൈവവൈവിധ്യ ബോർഡ്", "തിരുവനന്തപുരം"),
]

print("need rest of data")
