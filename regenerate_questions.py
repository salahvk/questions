#!/usr/bin/env python3
"""Restore corrupted JSON questions from git HEAD base + malayalamized build candidates."""

import json
import random
import re
import subprocess
from pathlib import Path

import fill_unique
from malayalamize_questions import malayalamize_text

BASE = Path(__file__).parent


def git_head_json(filename: str) -> dict | None:
    try:
        raw = subprocess.check_output(["git", "show", f"HEAD:{filename}"], cwd=BASE)
        return json.loads(raw)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def max_id_num(questions: list[dict], prefix: str) -> int:
    pat = re.compile(rf"^{re.escape(prefix)}(\d+)$")
    mx = 0
    for q in questions:
        m = pat.match(q.get("id", ""))
        if m:
            mx = max(mx, int(m.group(1)))
    return mx


def ml_question(q: str, opts: list[str], ans: str, diff: str) -> tuple[str, list[str], str, str]:
    return (
        malayalamize_text(q),
        [malayalamize_text(o) for o in opts],
        malayalamize_text(ans),
        diff,
    )


def regenerate_file(filename: str, prefix: str, candidates: list, target_total: int) -> int:
    path = BASE / filename
    head_data = git_head_json(filename)
    if head_data:
        questions = list(head_data.get("questions", []))
        existing = {q.get("question", "").strip() for q in questions if q.get("question")}
        start = max_id_num(questions, prefix) + 1
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
        questions = []
        existing = set()
        start = 1

    needed = max(0, target_total - len(questions))
    added = 0
    random.seed(42)

    for q_text, opts, ans, diff in candidates:
        if added >= needed:
            break
        mq, mopts, mans, mdiff = ml_question(q_text, opts, ans, diff)
        if mq.strip() in existing:
            continue
        if mans not in mopts:
            raise ValueError(f"Answer not in options: {mq!r}")
        shuffled = list(mopts)
        random.shuffle(shuffled)
        entry = {
            "id": f"{prefix}{start + added:03d}",
            "question": mq,
            "options": shuffled,
            "answer": mans,
            "difficulty": mdiff,
        }
        questions.append(entry)
        existing.add(mq.strip())
        added += 1

    out = {"questions": questions}
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added, len(questions)


def main() -> None:
    print("Regenerating post-HEAD questions with safe Malayalam...\n")
    for filename, prefix, candidates, target_total in fill_unique.TARGETS:
        added, total = regenerate_file(filename, prefix, candidates, target_total)
        print(f"  {filename}: {total} total ({added} regenerated from candidates)")


if __name__ == "__main__":
    main()
