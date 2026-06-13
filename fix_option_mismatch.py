#!/usr/bin/env python3
"""Fix option type mismatches in JSON banks and source *_facts.py modules."""

from __future__ import annotations

import ast
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

from option_type_utils import (
    build_options,
    option_type_mismatch,
)

BASE = Path(__file__).parent
SKIP = {"english_language.json", "current_affairs_manifest.json"}
RNG = random.Random(42)

FACTS_MODULES = [
    "world_history_facts",
    "indian_history_facts",
]


def load_facts_tuples(module_name: str) -> dict[str, tuple[str, list[str], str]]:
    """question -> (answer, wrong_options, difficulty) from all list constants."""
    path = BASE / f"{module_name}.py"
    if not path.exists():
        return {}
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    out: dict[str, tuple[str, list[str], str]] = {}
    for name in dir(mod):
        if name.startswith("_"):
            continue
        val = getattr(mod, name)
        if not isinstance(val, list):
            continue
        for row in val:
            if not isinstance(row, tuple) or len(row) < 4:
                continue
            q, ans, wrong, diff = row[0], row[1], row[2], row[3]
            if isinstance(q, str) and isinstance(ans, str) and isinstance(wrong, list):
                out[q.strip()] = (ans, list(wrong), diff)
    return out


def fix_json_file(path: Path, facts_lookup: dict[str, tuple[str, list[str], str]]) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    fixed = 0
    for q in data.get("questions", []):
        stem = q.get("question", "").strip()
        ans = q.get("answer", "")
        opts = q.get("options", [])
        if not stem or not ans:
            continue
        code = option_type_mismatch(stem, opts, ans)
        if not code:
            continue

        if stem in facts_lookup:
            fact_ans, fact_wrong, _ = facts_lookup[stem]
            new_opts = build_options(stem, fact_ans, fact_wrong, RNG)
            q["answer"] = fact_ans
        else:
            new_opts = build_options(stem, ans, None, RNG)

        if len(set(new_opts)) == 4 and ans in new_opts or q.get("answer") in new_opts:
            q["options"] = new_opts
            q["answer"] = q.get("answer") or ans
            if q["answer"] not in new_opts:
                q["answer"] = ans
                new_opts = build_options(stem, ans, None, RNG)
                q["options"] = new_opts
            fixed += 1
    if fixed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return fixed


def _fix_tuple_row(row: tuple) -> tuple | None:
    if len(row) < 4:
        return None
    q, ans, wrong, diff = row[0], row[1], row[2], row[3]
    if not isinstance(q, str) or not isinstance(ans, str) or not isinstance(wrong, list):
        return None
    opts = wrong + [ans]
    if not option_type_mismatch(q, opts, ans):
        return None
    new_wrong = build_options(q, ans, None, RNG)
    new_wrong = [o for o in new_wrong if o != ans][:3]
    while len(new_wrong) < 3:
        extra = build_options(q, ans, None, RNG)
        for e in extra:
            if e != ans and e not in new_wrong:
                new_wrong.append(e)
            if len(new_wrong) >= 3:
                break
        break
    return (q, ans, new_wrong[:3], diff)


def fix_facts_module(module_name: str) -> int:
    path = BASE / f"{module_name}.py"
    src = path.read_text(encoding="utf-8")
    mod = ast.parse(src)
    fixed = 0

    for node in mod.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            name = target.id
            if not name.isupper():
                continue
            try:
                rows = ast.literal_eval(node.value)
            except (ValueError, SyntaxError):
                continue
            if not isinstance(rows, list):
                continue
            changed = False
            new_rows = []
            for row in rows:
                if not isinstance(row, tuple):
                    new_rows.append(row)
                    continue
                fixed_row = _fix_tuple_row(row)
                if fixed_row:
                    new_rows.append(fixed_row)
                    changed = True
                    fixed += 1
                else:
                    new_rows.append(row)
            if changed:
                new_src = f"{name}: list = {repr(new_rows)}\n\n"
                pat = re.compile(
                    rf"^{re.escape(name)}:\s*list\s*=\s*\[",
                    re.MULTILINE,
                )
                m = pat.search(src)
                if not m:
                    continue
                start = m.start()
                # find matching end of list assignment (line ends with ]\n)
                depth = 0
                i = m.end() - 1
                while i < len(src):
                    if src[i] == "[":
                        depth += 1
                    elif src[i] == "]":
                        depth -= 1
                        if depth == 0:
                            end = i + 1
                            break
                    i += 1
                else:
                    continue
                src = src[:start] + new_src.rstrip() + src[end:]

    if fixed:
        path.write_text(src, encoding="utf-8")
    return fixed


def main(argv: list[str]) -> int:
    # 1. Fix source facts modules
    facts_fixed = 0
    for mod in FACTS_MODULES:
        facts_fixed += fix_facts_module(mod)
    print(f"Fixed {facts_fixed} fact rows in *_facts.py")

    # 2. Build lookup from fixed facts
    facts_lookup: dict[str, tuple[str, list[str], str]] = {}
    for mod in FACTS_MODULES:
        facts_lookup.update(load_facts_tuples(mod))

    # 3. Fix JSON files
    paths = sorted(BASE.glob("*.json"))
    if len(argv) > 1:
        names = {Path(a).name for a in argv[1:]}
        paths = [p for p in paths if p.name in names]

    total = 0
    for path in paths:
        if path.name in SKIP:
            continue
        n = fix_json_file(path, facts_lookup)
        if n:
            print(f"  {path.name}: fixed {n} questions")
            total += n

    print(f"Total JSON questions fixed: {total}")

    # 4. Report remaining
    remaining = 0
    for path in paths:
        if path.name in SKIP:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for q in data.get("questions", []):
            code = option_type_mismatch(
                q.get("question", ""),
                q.get("options", []),
                q.get("answer", ""),
            )
            if code:
                remaining += 1
    if remaining:
        print(f"WARNING: {remaining} mismatches remain — review manually")
        return 1
    print("All option type mismatches resolved.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
