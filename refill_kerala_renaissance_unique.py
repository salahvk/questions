#!/usr/bin/env python3
"""Refill kerala_renaissance.json with unique factual Malayalam PSC-style questions."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from kerala_renaissance_facts import generate_candidates
from refill_common import (
    id_width,
    interleave_candidates,
    is_filler_question,
    load_global_stems,
    make_entry,
    spread_consecutive_templates,
)

BASE = Path(__file__).parent
FILENAME = "kerala_renaissance.json"
PREFIX = "kr_"
TARGET = 2213  # 213 existing + 2000 new

MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")
YEAR = re.compile(r"^\d{4}$")


def _normalize_stem(q: str, ans: str) -> str:
    q = q.replace("SNDP", "എസ്.എൻ.ഡി.പി.").replace("PRDS", "പി.ആർ.ഡി.എസ്.")
    q = q.replace(" ആരാണ്/എതാണ്?", " ഏത്?").replace(" ആരാണ്/എതാണ്", " ഏത്")
    while " — ഏത്?" in q and q.count(" — ഏത്?") > 1:
        q = q.replace(" — ഏത്?", "", 1)
    return q.strip()


def is_bad_kept(q: dict) -> bool:
    if is_filler_question(q):
        return True
    stem = q.get("question", "").strip()
    ans = q.get("answer", "").strip()
    opts = q.get("options", [])
    if MIXED.search(stem + ans + " ".join(opts)):
        return True
    if "ആരാണ്/എതാണ്" in stem:
        return True
    if any("ഓപ്ഷൻ" in str(o) for o in opts):
        return True
    if stem.count(" — ഏത്?") > 1:
        return True
    if YEAR.match(ans) and "ആരാണ്?" in stem and "വർഷം" in stem:
        return True
    if YEAR.match(ans) and all(YEAR.match(str(o).strip()) for o in opts):
        if "ആരാണ്" in stem:
            return True
    return False


def main() -> int:
    rng = random.Random(42)
    path = BASE / FILENAME
    data = json.loads(path.read_text(encoding="utf-8"))

    kept_raw = [q for q in data.get("questions", []) if not is_filler_question(q)]
    kept: list[dict] = []
    kept_stems: set[str] = set()
    for q in kept_raw:
        stem = _normalize_stem(q.get("question", ""), q.get("answer", ""))
        entry = dict(q)
        entry["question"] = stem
        if is_bad_kept(entry) or not stem or stem in kept_stems:
            continue
        kept.append(entry)
        kept_stems.add(stem)

    existing = load_global_stems(exclude_file=FILENAME) | kept_stems
    candidates = interleave_candidates(generate_candidates(existing, rng), rng)

    combined: list[dict] = list(kept)
    width = id_width(TARGET)

    for q, opts, ans, diff in candidates:
        if len(combined) >= TARGET:
            break
        if q in kept_stems:
            continue
        combined.append(make_entry(PREFIX, len(combined) + 1, q, opts, ans, diff, width))
        kept_stems.add(q)

    combined = spread_consecutive_templates(combined, rng, max_run=2)

    final: list[dict] = []
    seen: set[str] = set()
    for i, q in enumerate(combined[:TARGET], start=1):
        stem = q.get("question", "").strip()
        if not stem or stem in seen or is_filler_question(q):
            continue
        seen.add(stem)
        entry = dict(q)
        entry["id"] = f"{PREFIX}{i:0{width}d}"
        final.append(entry)

    data["questions"] = final
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"{FILENAME}: {len(final)} questions "
        f"(kept {len(kept)}, added {max(0, len(final) - len(kept))}, target {TARGET})"
    )
    if len(final) < TARGET:
        print(
            f"ERROR: shortfall {TARGET - len(final)} — add verified facts, never pad.",
            file=sys.stderr,
        )

    dupes = len(final) - len({q["question"] for q in final})
    print(f"duplicate stems: {dupes}")

    result = subprocess.run(
        [sys.executable, str(BASE / "validate_questions.py"), FILENAME],
        cwd=BASE,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
