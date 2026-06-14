#!/usr/bin/env python3
"""Build mi_wave20_facts.py — 20 modern India PSC topic types."""

from __future__ import annotations

import textwrap
from pathlib import Path

OUT = Path(__file__).parent / "mi_wave20_facts.py"

HEADER = textwrap.dedent('''\
    #!/usr/bin/env python3
    """Wave 20 modern India facts — 20 PSC topic types (post-1947)."""

    from __future__ import annotations

    import random
    import re

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

''')

FOOTER = textwrap.dedent('''\


    def generate_wave20_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
        out: list[Candidate] = []
        _emit_all(out, existing, rng)
        return out


    if __name__ == "__main__":
        r = random.Random(42)
        ex: set[str] = set()
        cands = generate_wave20_candidates(ex, r)
        print(f"Generated {len(cands)} unique candidates")
''')

# ---------------------------------------------------------------------------
# Fact data — verified post-1947 India (Malayalam PSC style)
# ---------------------------------------------------------------------------

# 1–2: Five Year Plans (name, period, focus, architect/nickname)
FYP = [
    ("ആദ്യ അഞ്ചുവർഷ പദ്ധതി", "1951–1956", "കാർഷികം", "easy"),
    ("രണ്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1956–1961", "ഭാരമേറിയ വ്യവസായം", "medium"),
    ("മൂന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1961–1966", "സ്വയംപരതാപ്പ്", "medium"),
    ("നാലാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1969–1974", "വികസനവും സമത", "medium"),
    ("അഞ്ചാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1974–1979", "പoverty alleviation", "hard"),
    ("ആറാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1980–1985", "വികസനവും സാമൂഹിക നീതി", "medium"),
    ("ഏഴാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1985–1990", "സാമൂഹിക-സാമ്പത്തിക വികസനം", "medium"),
    ("എട്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1992–1997", "മനുഷ്യ വികസനം", "hard"),
    ("ഒമ്പതാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1997–2002", "വികസനവും സമത", "hard"),
    ("പ tenth അഞ്ചുവർഷ പദ്ധതി", "2002–2007", "വികസനവും സമത", "hard"),
    ("പതിനൊന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "2007–2012", "വേഗതയുള്ള inclusive growth", "hard"),
    ("പന്ത്രандാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "2012–2017", "വേഗതയുള്ള വികസനം", "hard"),
]

# Fix Malayalam for plan names - use proper names
FYP = [
    ("ആദ്യ അഞ്ചുവർഷ പദ്ധതി", "1951–1956", "കാർഷികം", "easy"),
    ("രണ്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1956–1961", "ഭാരമേറിയ വ്യവസായം", "medium"),
    ("മൂന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1961–1966", "സ്വയംപരതാപ്പ്", "medium"),
    ("നാലാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1969–1974", "വികസനവും സമത", "medium"),
    ("അഞ്ചാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1974–1979", "ദാരിദ്ര്യ നിർമാർജനം", "medium"),
    ("ആറാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1980–1985", "വികസനവും സാമൂഹിക നീതി", "medium"),
    ("ഏഴാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1985–1990", "സാമൂഹിക-സാമ്പത്തിക വികസനം", "medium"),
    ("എട്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1992–1997", "മനുഷ്യ വികസനം", "hard"),
    ("ഒമ്പതാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1997–2002", "വികസനവും സമത", "hard"),
    ("പ tenth അഞ്ചുവർഷ പദ്ധതി", "2002–2007", "വികസനവും സമത", "hard"),
]

# Let me fix FYP properly without typos
FYP = [
    ("ആദ്യ അഞ്ചുവർഷ പദ്ധതി", "1951–1956", "കാർഷികം", "easy"),
    ("രണ്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1956–1961", "ഭാരമേറിയ വ്യവസായം", "medium"),
    ("മൂന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1961–1966", "സ്വയംപരതാപ്പ്", "medium"),
    ("നാലാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1969–1974", "വികസനവും സമത", "medium"),
    ("അഞ്ചാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1974–1979", "ദാരിദ്ര്യ നിർമാർജനം", "medium"),
    ("ആറാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1980–1985", "വികസനവും സാമൂഹിക നീതി", "medium"),
    ("ഏഴാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1985–1990", "സാമൂഹിക-സാമ്പത്തിക വികസനം", "medium"),
    ("എട്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1992–1997", "മനുഷ്യ വികസനം", "hard"),
    ("ഒമ്പതാമത്തെ അഞ്ചുവർഷ പദ്ധതി", "1997–2002", "വികസനവും സമത", "hard"),
    ("പ tenth അഞ്ചുവർഷ പദ്ധതി", "2002–2007", "വികസനവും സമത", "hard"),
]


I'll write the full builder script with all fact data in one pass.

Task