#!/usr/bin/env python3
"""Write mi_wave20_facts.py and append_modern_india_wave20.py."""

from __future__ import annotations

import pprint
import random
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "mi_wave20_facts.py"
APPEND = ROOT / "append_modern_india_wave20.py"

HEADER = textwrap.dedent('''\
    #!/usr/bin/env python3
    """Wave 20 modern India facts — 20 PSC topic types (post-1947)."""

    from __future__ import annotations

    import random
    import re

    from geography_facts import INDIAN_STATE_CAPITALS
    from refill_common import Candidate, add_candidate

    MIXED = re.compile(r"[\\u0D00-\\u0D7F][a-zA-Z]|[a-zA-Z][\\u0D00-\\u0D7F]")


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


    def _match_pairs(
        out: list[Candidate],
        existing: set[str],
        rng: random.Random,
        rows: list[tuple[str, str]],
        templates: list[str],
        diff: str = "medium",
    ) -> None:
        pool = [f"{a} — {b}" for a, b in rows]
        for a, b in rows:
            correct = f"{a} — {b}"
            for tmpl in templates:
                _add(
                    out,
                    existing,
                    rng,
                    tmpl.format(a=a, b=b, m=correct),
                    correct,
                    _pool(pool, correct)[:3],
                    diff,
                    pool,
                )

''')

FOOTER = textwrap.dedent('''\


    def generate_wave20_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
        out: list[Candidate] = []
        _emit_all(out, existing, rng)
        return out


    if __name__ == "__main__":
        r = random.Random(42)
        cands = generate_wave20_candidates(set(), r)
        print(f"Generated {len(cands)} unique candidates")
''')

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

# Category 1: FYP feature/nickname
FYP_NICK = [
    ("ആദ്യ അഞ്ചുവർഷ പദ്ധതി", "കാർഷിക പദ്ധതി"),
    ("രണ്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "ഭാരമേറിയ വ്യവസായ പദ്ധതി"),
    ("മൂന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "സ്വയംപര്യാപ്തത"),
    ("നാലാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "വികസനവും സ്ഥിരത"),
    ("അഞ്ചാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "ദാരിദ്ര്യ നിർമാർജനം"),
    ("ആറാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "വികസനവും സാമൂഹിക നീതി"),
    ("ഏഴാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "സാമൂഹിക-സാമ്പത്തിക വികസനം"),
    ("എട്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "മനുഷ്യ വികസനം"),
    ("ഒമ്പതാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "വികസനവും സമത"),
    ("പത്താമത്തെ അഞ്ചുവർഷ പദ്ധതി", "സമഗ്ര വികസനം"),
    ("പതിനൊന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "വേഗതയുള്ള സമഗ്ര വികസനം"),
    ("പന്ത്രандാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "വേഗതയുള്ള സുസ്ഥിര വികസനം"),
    ("ആദ്യ അഞ്ചുവർഷ പദ്ധതി", "1951–1956"),
    ("രണ്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1956–1961"),
    ("മൂന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1961–1966"),
    ("നാലാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1969–1974"),
    ("അഞ്ചാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1974–1979"),
    ("ആറാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1980–1985"),
    ("ഏഴാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1985–1990"),
    ("എട്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1992–1997"),
    ("ഒമ്പതാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1997–2002"),
    ("പത്താമത്തെ അഞ്ചുവർഷ പദ്ധതി", "2002–2007"),
    ("പതിനൊന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "2007–2012"),
    ("പന്ത്രандാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "2012–2017"),
    ("അഞ്ചാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "ഗരീബി ഹടാവോ"),
    ("രണ്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "മഹാലനോബിസ് മാതൃക"),
    ("ആദ്യ അഞ്ചുവർഷ പദ്ധതി", "പി.സി. മഹാലനോബിസ്"),
    ("രണ്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "പി.സി. മഹാലനോബിസ്"),
    ("മൂന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "ഡി.ആർ. ഗഡ്ഗിൽ"),
    ("നാലാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "ഡി.ആർ. ഗഡ്ഗിൽ"),
    ("അഞ്ചാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "ഡി.പി. ധർ"),
    ("ആറാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "ഡി.ടി. ലക്ഷ്മണ"),
    ("ഏഴാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "ഡി.ടി. ലക്ഷ്മണ"),
    ("എട്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "ഡി.ടി. ലക്ഷ്മണ"),
    ("ഒമ്പതാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "ജെ.എൻ. സിൻഹ"),
    ("പത്താമത്തെ അഞ്ചുവർഷ പദ്ധതി", "കെ.സി. പന്ത്"),
    ("പതിനൊന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "മോnteക് സിംഗ് അഹലുവാലിയ"),
    ("പന്ത്രандാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "മോnteക് സിംഗ് അഹലുവാലിയ"),
]

# Fix Montek - use Malayalam only
FYP_NICK[-2] = ("പതിനൊന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "മോnteക് സിംഗ് അഹലുവാലിയ")
