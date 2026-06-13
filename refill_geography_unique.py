#!/usr/bin/env python3
"""Remove geography filler and refill to 1000+ unique factual questions."""

from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

from geography_facts import generate_candidates

BASE = Path(__file__).parent
TARGET = 1001
PREFIX = "geo_"

FILLER_PATTERNS = [
    re.compile(r"പ്രദേശം-\d+"),
    re.compile(r"ലോക ഭൂമിശാസ്ത്രത്തിൽ '\d+' എന്ന സംഖ്യയുമായി"),
]


def is_filler(q: dict) -> bool:
    text = q.get("question", "") + " " + " ".join(q.get("options", [])) + q.get("answer", "")
    return any(p.search(text) for p in FILLER_PATTERNS)


def load_global_existing() -> set[str]:
    existing: set[str] = set()
    for path in BASE.glob("*.json"):
        if path.name == "geography.json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for q in data.get("questions", []):
            stem = q.get("question", "").strip()
            if stem:
                existing.add(stem)
    return existing


def make_entry(num: int, q: str, opts: list[str], ans: str, diff: str) -> dict:
    shuffled = list(opts)
    random.shuffle(shuffled)
    return {"id": f"{PREFIX}{num:03d}", "question": q, "options": shuffled, "answer": ans, "difficulty": diff}


def main() -> int:
    rng = random.Random(42)
    path = BASE / "geography.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    kept = [q for q in data.get("questions", []) if not is_filler(q)]
    existing: set[str] = {q.get("question", "").strip() for q in kept if q.get("question")}
    existing.update(load_global_existing())

    candidates = generate_candidates(existing, rng)
    rng.shuffle(candidates)

    combined: list[dict] = list(kept)
    for q, opts, ans, diff in candidates:
        if len(combined) >= TARGET:
            break
        combined.append(make_entry(len(combined) + 1, q, opts, ans, diff))

    seen_stems = {x.get("question", "").strip() for x in combined}
    extra_rounds = 0
    while len(combined) < TARGET and candidates and extra_rounds < 3:
        added = 0
        rng.shuffle(candidates)
        for q, opts, ans, diff in candidates:
            if len(combined) >= TARGET:
                break
            if q in seen_stems:
                continue
            combined.append(make_entry(len(combined) + 1, q, opts, ans, diff))
            seen_stems.add(q)
            added += 1
        if not added:
            break
        extra_rounds += 1

    final: list[dict] = []
    seen: set[str] = set()
    for i, q in enumerate(combined[:TARGET], start=1):
        stem = q.get("question", "").strip()
        if stem in seen:
            continue
        seen.add(stem)
        entry = dict(q)
        entry["id"] = f"{PREFIX}{i:03d}"
        final.append(entry)

    data["questions"] = final
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"geography.json: {len(final)} questions (kept {len(kept)}, added {len(final) - len(kept)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
