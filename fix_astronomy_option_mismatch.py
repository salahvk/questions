#!/usr/bin/env python3
"""Fix astronomy.json option type mismatches (mixed periods, years, directions, AU)."""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

from option_type_utils import (
    astronomy_option_mismatch,
    build_options,
    option_type_mismatch,
)

BASE = Path(__file__).parent
RNG = random.Random(42)


def fix_json(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    fixed = 0
    for q in data.get("questions", []):
        stem = q.get("question", "")
        ans = q.get("answer", "")
        opts = q.get("options", [])
        if not option_type_mismatch(stem, opts, ans):
            continue
        new_opts = build_options(stem, ans, None, RNG)
        if len(new_opts) == 4 and ans in new_opts and new_opts != opts:
            q["options"] = new_opts
            fixed += 1
    if fixed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return fixed


def main(argv: list[str]) -> int:
    path = BASE / "astronomy.json"
    n = fix_json(path)
    print(f"Fixed {n} astronomy questions")

    remaining = 0
    data = json.loads(path.read_text(encoding="utf-8"))
    for q in data.get("questions", []):
        if astronomy_option_mismatch(q.get("question", ""), q.get("options", []), q.get("answer", "")):
            remaining += 1
    if remaining:
        print(f"WARNING: {remaining} astronomy mismatches remain")
        return 1
    print("All astronomy option type mismatches resolved.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
