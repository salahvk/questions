#!/usr/bin/env python3
"""Remove reverse/meta quiz questions from all JSON banks and renumber IDs."""

from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).parent

REVERSE_META_PATTERNS = [
    re.compile(r"ഏത് ചോദ്യത്തിന്റെ ഉത്തരമാണ്"),
    re.compile(r"ഉത്തരമുള്ള ചോദ്യം"),
]


def is_reverse_meta(q: dict) -> bool:
    text = q.get("question", "")
    return any(p.search(text) for p in REVERSE_META_PATTERNS)


def renumber(questions: list[dict], prefix: str) -> None:
    width = max(3, len(str(len(questions))))
    for i, q in enumerate(questions, start=1):
        q["id"] = f"{prefix}{i:0{width}d}"


def is_malayalam_stem(q: dict) -> bool:
    return bool(re.search(r"[\u0D00-\u0D7F]", q.get("question", "")))


def clean_file(path: Path) -> tuple[int, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.get("questions", [])
    if not questions:
        return 0, 0

    kept = [q for q in questions if not is_reverse_meta(q)]
    if path.name == "english_language.json":
        kept = [q for q in kept if not is_malayalam_stem(q)]
    removed = len(questions) - len(kept)
    if removed == 0:
        return 0, len(questions)

    prefix_match = re.match(r"^([a-z]+_)", questions[0].get("id", ""))
    prefix = prefix_match.group(1) if prefix_match else "q_"
    renumber(kept, prefix)
    data["questions"] = kept
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return removed, len(kept)


def main() -> None:
    total_removed = 0
    for path in sorted(BASE.glob("*.json")):
        if path.name == "current_affairs_manifest.json":
            continue
        try:
            removed, kept = clean_file(path)
        except (json.JSONDecodeError, KeyError, IndexError) as exc:
            print(f"SKIP {path.name}: {exc}")
            continue
        if removed:
            print(f"{path.name}: removed {removed}, kept {kept}")
            total_removed += removed
    print(f"Total removed: {total_removed}")


if __name__ == "__main__":
    main()
