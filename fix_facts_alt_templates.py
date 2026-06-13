#!/usr/bin/env python3
"""Strip reverse-meta alt generation from *_facts.py modules."""

from __future__ import annotations

import re
from pathlib import Path

BASE = Path(__file__).parent

ALT_BLOCK = re.compile(
    r"\n        alt = f.*?\n"
    r"        _add\(out, existing, rng, alt,.*?\n",
    re.DOTALL,
)

WH_REVERSE = re.compile(
    r"\n        _add\(out, existing, rng, f\"ലോക ചരിത്രത്തിൽ '\{ans\}' ഉത്തരമുള്ള ചോദ്യം\?\", q,.*?\n",
    re.DOTALL,
)

GENERATE_SIMPLE = """def generate_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []
    for q, ans, wrong, diff in FACTS:
        _add(out, existing, rng, q, ans, wrong + [ans], diff)
    return out
"""


def fix_module(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text

    if "def generate_candidates" not in text:
        return False

    new_text, n_alt = ALT_BLOCK.subn("\n", text)
    new_text, n_wh = WH_REVERSE.subn("\n", new_text)

    if n_alt == 0 and n_wh == 0 and "alt = f" not in new_text and "ഉത്തരമുള്ള ചോദ്യം" not in new_text:
        return False

    # Fallback: replace entire generate_candidates if alt lines remain
    if "alt = f" in new_text or "ഉത്തരമുള്ള ചോദ്യം" in new_text:
        new_text = re.sub(
            r"def generate_candidates\(existing: set\[str\], rng: random\.Random\) -> list\[Candidate\]:.*?\n    return out\n",
            GENERATE_SIMPLE,
            new_text,
            count=1,
            flags=re.DOTALL,
        )

    if new_text != orig:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def fix_wire_json_modules() -> None:
    path = BASE / "wire_json_modules.py"
    text = path.read_text(encoding="utf-8")
    old = """        _add(out, existing, rng, q, ans, wrong + [ans], diff)
        alt = f"'{{ans}}' ഏത് ചോദ്യത്തിന്റെ ഉത്തരമാണ്?".format(ans=ans)
        _add(out, existing, rng, alt, q.rstrip("?") + "?", [f[0] for f in FACTS if f[0] != q], diff)
    return out"""
    new = """        _add(out, existing, rng, q, ans, wrong + [ans], diff)
    return out"""
    if old in text:
        path.write_text(text.replace(old, new), encoding="utf-8")
        print("fixed wire_json_modules.py")


def main() -> None:
    fixed = 0
    for path in sorted(BASE.glob("*_facts.py")):
        if fix_module(path):
            print(f"fixed {path.name}")
            fixed += 1
    fix_wire_json_modules()
    print(f"Modules patched: {fixed}")


if __name__ == "__main__":
    main()
