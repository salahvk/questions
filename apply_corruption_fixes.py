#!/usr/bin/env python3
"""Fast corruption-only pass on all JSON question banks (no malayalamize)."""

from __future__ import annotations

import json
from pathlib import Path

from apply_malayalam_rules import fix_corruptions

BASE = Path(__file__).parent
SKIP = {"english_language.json", "current_affairs_manifest.json"}


def main() -> None:
    updated_files = 0
    updated_fields = 0
    for path in sorted(BASE.glob("*.json")):
        if path.name in SKIP:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for q in data.get("questions", []):
            for field in ("question", "answer"):
                old = q.get(field, "")
                new = fix_corruptions(old)
                if new != old:
                    q[field] = new
                    updated_fields += 1
                    changed = True
            opts = q.get("options", [])
            new_opts = []
            for opt in opts:
                new_opt = fix_corruptions(opt)
                if new_opt != opt:
                    updated_fields += 1
                    changed = True
                new_opts.append(new_opt)
            q["options"] = new_opts
        if changed:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            updated_files += 1
            print(f"  {path.name}: corruption fixes applied")
    print(f"Done: {updated_files} files, {updated_fields} fields")


if __name__ == "__main__":
    main()
