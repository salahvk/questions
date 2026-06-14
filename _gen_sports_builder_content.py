#!/usr/bin/env python3
"""Internal: emit build_sports_wave20_module.py source."""
from __future__ import annotations

import pprint
import textwrap
from pathlib import Path

OUT = Path(__file__).parent / "build_sports_wave20_module.py"

HEADER = textwrap.dedent('''\
    #!/usr/bin/env python3
    """Build sports_wave20_facts.py — 20 Malayalam PSC sports categories, 4600+ stems."""

    from __future__ import annotations

    import importlib.util
    import pprint
    import random
    import textwrap
    from pathlib import Path

    OUT = Path(__file__).parent / "sports_wave20_facts.py"

    HEADER = textwrap.dedent(\'\'\'\\
        #!/usr/bin/env python3
        """Wave 20 sports facts — 20 Malayalam PSC topic categories."""

        from __future__ import annotations

        import random

        from refill_common import Candidate, add_candidate, interleave_candidates

        Fact = tuple[str, str, list[str], str]


        def _pool(items: list[str], correct: str) -> list[str]:
            return [x for x in items if x != correct]


        def _emit(
            out: list[Candidate],
            existing: set[str],
            rng: random.Random,
            prefix: str,
            facts: list[Fact],
            *,
            function_entity: str | None = None,
        ) -> None:
            terms = list(dict.fromkeys(t for t, _, _, _ in facts))
            answers = list(dict.fromkeys(a for _, a, _, _ in facts))
            for term, ans, wrong, diff in facts:
                add_candidate(
                    out, existing, rng,
                    f"{prefix} \\'{term}\\'?",
                    ans, wrong, diff, pool=answers,
                )
                add_candidate(
                    out, existing, rng,
                    f"\\'{ans}\\' ഏതിനെ സൂചിപ്പിക്കുന്നു?",
                    term, _pool(terms, term)[:6], diff, pool=terms,
                )
                if function_entity:
                    add_candidate(
                        out, existing, rng,
                        f"\\'{ans}\\' ഏത് {function_entity}-ന്റെ പ്രവർത്തനമാണ്?",
                        term, _pool(terms, term)[:6], diff, pool=terms,
                    )


        def _emit_pairs(
            out: list[Candidate],
            existing: set[str],
            rng: random.Random,
            prefix: str,
            rows: list[tuple[str, str]],
            templates_ab: list[str],
            templates_ba: list[str] | None = None,
            diff: str = "medium",
        ) -> None:
            bs = list(dict.fromkeys(b for _, b in rows))
            as_ = list(dict.fromkeys(a for a, _ in rows))
            for a, b in rows:
                for tmpl in templates_ab:
                    add_candidate(
                        out, existing, rng,
                        prefix + tmpl.format(a=a, b=b),
                        b, _pool(bs, b)[:3], diff, pool=bs,
                    )
                if templates_ba:
                    for tmpl in templates_ba:
                        add_candidate(
                            out, existing, rng,
                            prefix + tmpl.format(a=a, b=b),
                            a, _pool(as_, a)[:3], diff, pool=as_,
                        )


        def _emit_triples(
            out: list[Candidate],
            existing: set[str],
            rng: random.Random,
            rows: list[tuple[str, str, str]],
            ab_templates: list[str],
            ac_templates: list[str],
            pool_b: list[str],
            pool_c: list[str],
            diff: str = "medium",
        ) -> None:
            for a, b, c in rows:
                for tmpl in ab_templates:
                    add_candidate(
                        out, existing, rng,
                        tmpl.format(a=a, b=b, c=c),
                        b, _pool(pool_b, b)[:3], diff, pool=pool_b,
                    )
                for tmpl in ac_templates:
                    add_candidate(
                        out, existing, rng,
                        tmpl.format(a=a, b=b, c=c),
                        c, _pool(pool_c, c)[:3], diff, pool=pool_c,
                    )

    \'\'\')

    FOOTER = textwrap.dedent(\'\'\'\\

        def generate_wave20_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
            out: list[Candidate] = []
            _emit_all_categories(out, existing, rng)
            return interleave_candidates(out, rng)


        if __name__ == "__main__":
            print(len(generate_wave20_candidates(set(), random.Random(42))))
    \'\'\')

''')

# Data building happens in build_sports_wave20_module.py itself - this file only documents structure
print("Use Write tool for full builder")
