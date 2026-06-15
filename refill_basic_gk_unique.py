#!/usr/bin/env python3
"""Remove filler from basic_general_knowledge.json and refill with wave30 unique facts."""

from __future__ import annotations

import json
import random
import subprocess
import sys
from pathlib import Path

from basic_gk_wave30_facts import generate_wave30_candidates
from refill_common import (
    SKIP_GLOBAL,
    id_width,
    interleave_candidates,
    is_filler_question,
    make_entry,
    spread_consecutive_templates,
)

BASE = Path(__file__).parent
FILENAME = "basic_general_knowledge.json"
PREFIX = "bgk_"
TARGET = 8109


def load_global_stems(exclude_file: str | None = None) -> set[str]:
    existing: set[str] = set()
    for path in BASE.glob("*.json"):
        if path.name in SKIP_GLOBAL or path.name == exclude_file:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        questions = data if isinstance(data, list) else data.get("questions", [])
        if not isinstance(questions, list):
            continue
        for q in questions:
            if not isinstance(q, dict):
                continue
            stem = q.get("question", "").strip()
            if stem:
                existing.add(stem)
    return existing


def main() -> int:
    rng = random.Random(42)
    path = BASE / FILENAME
    data = json.loads(path.read_text(encoding="utf-8"))

    kept = [q for q in data.get("questions", []) if not is_filler_question(q)]
    kept_stems: set[str] = {
        q.get("question", "").strip() for q in kept if q.get("question")
    }

    existing = load_global_stems(exclude_file=FILENAME) | kept_stems
    candidates = interleave_candidates(generate_wave30_candidates(existing, rng), rng)

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
    dupes = len(final) - len({q["question"] for q in final})
    print(f"duplicate stems: {dupes}")

    result = subprocess.run(
        [sys.executable, str(BASE / "validate_questions.py"), FILENAME],
        cwd=BASE,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
