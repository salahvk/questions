#!/usr/bin/env python3
"""Build education_wave20_facts.py from verified PSC education facts."""

from __future__ import annotations

import textwrap

HEADER = textwrap.dedent(
    '''\
    #!/usr/bin/env python3
    """Wave-20 education facts — 20 PSC topic types for education.json expansion."""

    from __future__ import annotations

    import random

    from refill_common import Candidate, add_candidate

    '''
)

HELPERS = textwrap.dedent(
    '''\

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
        base = pool if pool else wrong + [ans]
        add_candidate(out, existing, rng, q, ans, _pool(base, ans)[:3], diff, base)


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


    def _emit(
        out: list[Candidate],
        existing: set[str],
        rng: random.Random,
        rows: list[tuple[str, str]],
        fwd: list[str],
        rev: list[str],
        pool_a: list[str],
        pool_b: list[str],
        diff: str = "medium",
    ) -> None:
        _pairs(out, existing, rng, rows, fwd, pool_b, diff)
        _pairs_rev(out, existing, rng, rows, rev, pool_a, diff)


    def _emit_qa(
        out: list[Candidate],
        existing: set[str],
        rng: random.Random,
        rows: list[tuple[str, str, list[str], str]],
        pool: list[str] | None = None,
    ) -> None:
        for q, ans, wrong, diff in rows:
            base = pool if pool else wrong + [ans]
            _add(out, existing, rng, q, ans, wrong, diff, base)

    '''
)

# Each category: list of (label_a, label_b) pairs for _emit, plus standalone QA rows
CATEGORIES: dict[str, dict] = {}

def cat(name: str, pairs: list[tuple[str, str]], fwd: list[str], rev: list[str], diff: str = "medium"):
    pool_a = [a for a, _ in pairs]
    pool_b = [b for _, b in pairs]
    CATEGORIES[name] = {"pairs": pairs, "fwd": fwd, "rev": rev, "pool_a": pool_a, "pool_b": pool_b, "diff": diff}

# --- 1 British colonial ---
cat("british", [
    ("മക്കാലെ മിനിറ്റ്", "1835"),
    ("വുഡ്\u200cസ് ഡിസ്പാച്ച്", "1854"),
    ("ഹണ്ടർ കമ്മീഷൻ", "1882"),
    ("ചാർട്ടർ ആക്റ്റ് (1813)", "1813"),
    ("ഇന്ത്യൻ യൂണിവേഴ്സിറ്റി ആക്റ്റ്", "1857"),
    ("സാർജന്റ് പ്ലാൻ", "1944"),
    ("ഇന്ത്യൻ യൂണിവേഴ്സിറ്റി ആക്റ്റ്", "1857"),
    ("ഇംഗ്ലീഷ് വിദ്യാഭ്യാസ നയം", "1835"),
    ("വുഡ്\u200cസ് ഡിസ്പാച്ച്", "1854"),
    ("ഹണ്ടർ കമ്മീഷൻ", "1882-83"),
    ("മക്ഔളി", "1835"),
    ("ചാർട്ടർ ആക്റ്റ്", "1813"),
    ("സാർജന്റ് പ്ലാൻ", "1944"),
    ("ഇന്ത്യൻ യൂണിവേഴ്സിറ്റി ആക്റ്റ്", "1857"),
    ("വുഡ്\u200cസ് ഡിസ്പാച്ച്", "1854"),
    ("ഹണ്ടർ കമ്മീഷൻ", "1882"),
    ("മക്കാലെ മിനിറ്റ്", "1835"),
    ("ചാർട്ടർ ആക്റ്റ്", "1813"),
    ("സാർജന്റ് പ്ലാൻ", "1944"),
    ("മക്ഔളി മിനിറ്റ്", "1835"),
    ("വുഡ്\u200cസ് ഡിസ്പാച്ച്", "1854"),
    ("ഹണ്ടർ കമ്മീഷൻ", "1882"),
    ("ഇന്ത്യൻ യൂണിവേഴ്സിറ്റി ആക്റ്റ്", "1857"),
    ("ചാർട്ടർ ആക്റ്റ്", "1813"),
    ("സാർജന്റ് പ്ലാൻ", "1944"),
    ("മക്കാലെ മിനിറ്റ്", "1835"),
    ("വുഡ്\u200cസ് ഡിസ്പാച്ച്", "1854"),
    ("ഹണ്ടർ കമ്മീഷൻ", "1882"),
    ("ഇന്ത്യൻ യൂണിവേഴ്സിറ്റി ആക്റ്റ്", "1857"),
    ("ചാർട്ടർ ആക്റ്റ്", "1813"),
], [
    "'{a}' പ്രസിദ്ധമായ/നിർദ്ദേശിച്ച വർഷം?",
    "ബ്രിട്ടീഷ് കാലത്തെ '{a}' ഏത് വർഷവുമായി ബന്ധപ്പെട്ടത്?",
    "ഇന്ത്യൻ വിദ്യാഭ്യാസ ചരിത്രത്തിൽ '{a}'-ന്റെ വർഷം?",
], [
    "'{b}'-ൽ നടന്ന/പ്രഖ്യാപിച്ച പ്രധാന വിദ്യാഭ്യാസ события/നയം?",
    "'{b}' വർഷവുമായി ബന്ധപ്പെട്ട ബ്രിട്ടീഷ് കാല വിദ്യാഭ്യാസ события?",
    "'{b}'-ൽ പ്രാബല്യത്തിൽ വന്ന പ്രധാന വിദ്യാഭ്യാസ നടപടി?",
], "hard")

# Fix duplicate pairs - use unique pairs only
CATEGORIES["british"]["pairs"] = list(dict.fromkeys(CATEGORIES["british"]["pairs"]))

# I'll build the full module in the output script differently - use a data-driven approach
print("Use education_wave20_facts.py directly")

PYEOF
