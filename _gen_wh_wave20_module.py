#!/usr/bin/env python3
"""Generate world_history_wave20_facts.py — verified Malayalam-only data."""

from __future__ import annotations

import pprint
import re
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "world_history_wave20_facts.py"
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")
ANATOLIA = "\u0D05\u0D28\u0D3E\u0D1F\u0D4D\u0D30\u0D3E\u0D1F\u0D4B\u0D32\u0D3F\u0D2F"

HEADER = '''#!/usr/bin/env python3
"""Wave 20 world history facts — 20 PSC topic types (non-year templates)."""

from __future__ import annotations

import random
import re

from refill_common import Candidate, add_candidate

MIXED = re.compile(r"[\\u0D00-\\u0D7F][a-zA-Z]|[a-zA-Z][\\u0D00-\\u0D7F]")
ANATOLIA = "\\u0D05\\u0D28\\u0D3E\\u0D1F\\u0D4D\\u0D30\\u0D3E\\u0D1F\\u0D4B\\u0D32\\u0D3F\\u0D2F"


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

PAIR_FWD = [
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം/തടം?",
    "'{a}' സിവിലൈസേഷൻ ഏത് പ്രദേശത്താണ്?",
    "'{a}'-ന്റെ പ്രധാന ഭൂമിശാസ്ത്ര പ്രദേശം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം?",
    "'{a}' ഏത് പ്രദേശവുമായി ബന്ധപ്പെട്ട നാഗരികത?",
    "'{a}'-ന്റെ സ്ഥാനം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട തടം/പ്രദേശം?",
    "'{a}' പ്രധാനമായി ഏത് പ്രദേശത്താണ്?",
]

PAIR_REV = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട നാഗരികത?",
    "'{b}' പ്രദേശത്തിന്റെ പ്രധാന സിവിലൈസേഷൻ?",
    "'{b}'-ൽ flourished ചെയ്ത നാഗരികത?",
    "'{b}'-യുമായി ബന്ധപ്പെട്ട പുരാതന സംസ്കാരം?",
    "'{b}'-യിലെ പ്രധാന നാഗരികത?",
]

EXTRA_PAIR_FWD = [
    "'{a}'-ന്റെ പ്രധാന വിവരണം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തു?",
    "'{a}'-യുടെ പ്രധാന സ്ഥലം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട വിവരണം?",
]

EXTRA_PAIR_REV = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട വസ്തു?",
    "'{b}'-ന്റെ പേരിലുള്ള വസ്തു?",
    "'{b}'-യുമായി ബന്ധപ്പെട്ട വിവരണം?",
]

# Category-specific template sets for generate / extra
CAT_TEMPLATES: dict[str, tuple[list[str], list[str], list[str], list[str]]] = {
    "CIVILIZATION_REGION": (PAIR_FWD, PAIR_REV, EXTRA_PAIR_FWD, EXTRA_PAIR_REV),
    "MONUMENT_CITY": (
        [
            "'{a}' ഏത് നഗരത്തിലാണ്?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട നഗരം?",
            "'{a}'-ന്റെ സ്ഥാനം?",
            "'{a}' ഏത് നഗരത്തിനടുത്താണ്?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന നഗരം?",
            "'{a}' സ്ഥിതി ചെയ്യുന്ന നഗരം?",
            "'{a}'-ന്റെ നഗരം?",
            "'{a}' ഏത് നഗരത്തിലാണ് സ്ഥിതി ചെയ്യുന്നത്?",
        ],
        [
            "'{b}'-യിലെ പ്രധാന സ്മാരകം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണം?",
            "'{b}' നഗരത്തിലെ പ്രശസ്ത സ്മാരകം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സ്മാരകം?",
            "'{b}'-ലെ പ്രധാന ലാൻഡ്മാർക്ക്?",
        ],
        ["'{a}'-യുമായി ബന്ധപ്പെട്ട സ്ഥലം?", "'{a}'-ന്റെ പ്രധാന വിവരണം?"],
        ["'{b}'-യിലെ പ്രധാന സ്മാരകം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണം?"],
    ),
    "INVENTOR_INVENTION": (
        [
            "'{a}'-യുടെ കണ്ടെത്തൽ/发明?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട发明?",
            "'{a}' കണ്ടെത്തിയത്?",
            "'{a}'-ന്റെ പ്രധാന贡献?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട发明?",
            "'{a}'-ന്റെ发明?",
            "'{a}' ഏത്发明?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട贡献?",
        ],
        [
            "'{b}'-യുടെ发明者?",
            "'{b}' കണ്ടെത്തിയ വ്യക്തി?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട发明者?",
            "'{b}'-ന്റെ发明者 ആര്?",
            "'{b}' ആരുടെ发明?",
        ],
        ["'{a}'-ന്റെ发明?", "'{a}'-യുമായി ബന്ധപ്പെട്ട贡献?"],
        ["'{b}'-യുടെ发明者?", "'{b}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി?"],
    ),
}

DATA: dict[str, list] = {}

DATA["CIVILIZATION_REGION"] = [
    ("സുമേർ", "മെസോപൊട്ടാമിയ"),
    ("ബാബിലോൺ", "മെസോപൊട്ടാമിയ"),
    ("അസീറിയ", "മെസോപൊട്ടാമിയ"),
    ("ഫിനീഷ്യ", "പശ്ചിമേഷ്യ"),
    ("പുരാതന ഈജിപ്ത്", "നൈൽ തടം"),
    ("ഹാരപ്പ", "ഇന്ദസ് തടം"),
    ("മോഹഞ്ചദാരോ", "ഇന്ദസ് തടം"),
    ("ചൈനീസ് നാഗരികത", "ഹ്വാങ്ഹെ തടം"),
    ("മായ സിവിലൈസേഷൻ", "മധ്യ അമേരിക്ക"),
    ("അസ്ടെക് സാമ്രാജ്യം", "മെക്സിക്കോ"),
    ("ഇൻക സാമ്രാജ്യം", "ആൻഡസ്"),
    ("പുരാതന ഗ്രീസ്", "ഏജിയൻ"),
    ("പുരാതന റോം", "ഇറ്റലി"),
    ("പേർഷ്യൻ സാമ്രാജ്യം", "ഇറാൻ"),
    ("ഓട്ടോമൻ സാമ്രാജ്യം", ANATOLIA),
    ("ബൈzantine സാമ്രാജ്യം", "ഇസ്താംബുൾ"),
]
