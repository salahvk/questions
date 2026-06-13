#!/usr/bin/env python3
"""Sort questions by numeric ID suffix and renumber sequentially in every JSON bank."""

from __future__ import annotations

import json
import re
from pathlib import Path

from refill_common import id_width

BASE = Path(__file__).parent
SKIP = {"current_affairs_manifest.json"}


def parse_id(id_str: str) -> tuple[str, int]:
    match = re.match(r"^(.*?)(\d+)$", id_str)
    if not match:
        return "", 0
    return match.group(1), int(match.group(2))


def sort_and_renumber(path: Path) -> tuple[int, bool]:
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.get("questions", [])
    if not questions:
        return 0, False

    original_ids = [q.get("id", "") for q in questions]
    prefix = parse_id(original_ids[0])[0]
    if not prefix:
        prefix_match = re.match(r"^([a-z]+_)", original_ids[0])
        prefix = prefix_match.group(1) if prefix_match else "q_"

    questions.sort(key=lambda q: parse_id(q.get("id", ""))[1])

    width = id_width(len(questions))
    for i, q in enumerate(questions, start=1):
        q["id"] = f"{prefix}{i:0{width}d}"

    new_ids = [q["id"] for q in questions]
    changed = original_ids != new_ids
    if changed:
        data["questions"] = questions
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(questions), changed


def main() -> None:
    updated = 0
    for path in sorted(BASE.glob("*.json")):
        if path.name in SKIP:
            continue
        try:
            count, changed = sort_and_renumber(path)
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            print(f"SKIP {path.name}: {exc}")
            continue
        if changed:
            print(f"{path.name}: sorted and renumbered {count} questions")
            updated += 1
        else:
            print(f"{path.name}: already ordered ({count})")
    print(f"Updated {updated} file(s)")


if __name__ == "__main__":
    main()
