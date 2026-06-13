#!/usr/bin/env python3
"""Remove NCERT fake rows and spread same-template runs in education.json."""

from __future__ import annotations

import json
import random
import re
from pathlib import Path

from refill_common import id_width, is_filler_question, spread_consecutive_templates

BASE = Path(__file__).parent
PATH = BASE / "education.json"
PREFIX = "edu_"


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    kept = [q for q in data.get("questions", []) if not is_filler_question(q)]
    removed = len(data.get("questions", [])) - len(kept)
    rng = random.Random(42)
    spread = spread_consecutive_templates(kept, rng, max_run=2)
    width = id_width(len(spread))
    for i, q in enumerate(spread, start=1):
        q["id"] = f"{PREFIX}{i:0{width}d}"
    data["questions"] = spread
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Removed filler: {removed}, final: {len(spread)}")


if __name__ == "__main__":
    main()
