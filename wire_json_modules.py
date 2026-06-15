#!/usr/bin/env python3
"""Create fact modules from existing JSON banks + alternate templates; wire all categories."""

from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).parent

WIRE = [
    "constitution_of_india.json",
    "cinema.json",
    "natural_science.json",
    "arts.json",
    "history_of_kerala.json",
    "education.json",
    "english_language.json",
    "kerala_renaissance.json",
    "communication_journalism.json",
    "important_institutions.json",
    "continents_of_the_world.json",
    "historical_monuments_of_kerala.json",
    "information_technology.json",
    "sports.json",
    "literature.json",
    "malayalam.json",
]

MODULE_TEMPLATE = '''#!/usr/bin/env python3
"""Auto-generated facts from {filename}."""

from __future__ import annotations
import random

Candidate = tuple[str, list[str], str, str]

def _pick(pool, correct, rng):
    wrong = list(dict.fromkeys(x for x in pool if x != correct))
    rng.shuffle(wrong)
    opts = [correct] + wrong[:3]
    while len(opts) < 4:
        opts.append("ഒന്നുമില്ല")
    return opts[:4]

def _add(out, existing, rng, q, ans, pool, diff="medium"):
    q = q.strip()
    if not q or q in existing:
        return
    opts = _pick(pool, ans, rng)
    if len(set(opts)) != 4 or ans not in opts:
        return
    out.append((q, opts, ans, diff))
    existing.add(q)

FACTS: list[tuple[str, str, list[str], str]] = {facts!r}

def generate_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    import re

    out: list[Candidate] = []
    year_pool = sorted({{a[:4] for _, a, _, _ in FACTS if re.match(r"^\\d{{4}}", a)}})
    name_pool = [a for _, a, _, _ in FACTS if not re.match(r"^\\d{{4}}", a)]

    for q, ans, wrong, diff in FACTS:
        _add(out, existing, rng, q, ans, wrong + [ans], diff)

        ym = re.match(r"^(\\d{{4}})", ans)
        qm = re.search(r"'([^']+)'", q)
        if ym and qm and year_pool:
            year = ym.group(1)
            entity = qm.group(1)
            alt = f"'{{entity}}' സംബന്ധിച്ച പ്രധാന വർഷം?"
            if alt != q:
                pool = [y for y in year_pool if y != year][:3] + [year]
                _add(out, existing, rng, alt, year, pool, diff)
            alt2 = f"{{year}}-ൽ '{{entity}}'?"
            if alt2 != q and alt2 != alt:
                ents = [a for a in name_pool if a != entity][:3] + [entity]
                _add(out, existing, rng, alt2, entity, ents, diff)

        if ("ആരാണ്" in q or "ആരായിരുന്നു" in q) and qm and name_pool:
            entity = qm.group(1)
            alt3 = f"'{{entity}}' ആരെ സൂചിപ്പിക്കുന്നു?"
            if alt3 != q:
                pool = [n for n in name_pool if n != ans][:3] + [ans]
                _add(out, existing, rng, alt3, ans, pool, diff)

    return out
'''


def load_facts(path: Path) -> list[tuple[str, str, list[str], str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows: list[tuple[str, str, list[str], str]] = []
    seen: set[str] = set()
    for item in data.get("questions", []):
        q = item.get("question", "").strip()
        ans = item.get("answer", "").strip()
        opts = item.get("options", [])
        diff = item.get("difficulty", "medium")
        wrong = [o for o in opts if o != ans][:3]
        if not q or q in seen or len(wrong) < 3:
            continue
        seen.add(q)
        rows.append((q, ans, wrong, diff))
    return rows


def mod_name(fn: str) -> str:
    return fn.replace(".json", "_facts").replace("-", "_")


created: dict[str, str] = {}
for fn in WIRE:
    path = BASE / fn
    if not path.exists():
        continue
    facts = load_facts(path)
    if not facts:
        continue
    mod = mod_name(fn)
    text = MODULE_TEMPLATE.format(filename=fn, facts=facts)
    out_path = BASE / f"{mod}.py"
    out_path.write_text(text, encoding="utf-8")
    created[fn] = mod
    print(f"{mod}.py: {len(facts)} facts")

# Update generate_all_questions.py FACT_MODULES
gen_path = BASE / "generate_all_questions.py"
gen = gen_path.read_text(encoding="utf-8")
for fn, mod in created.items():
    line = f'    "{fn}": "{mod}",'
    if line not in gen:
        gen = gen.replace(
            '    "economics.json": "economics_facts",',
            f'    "economics.json": "economics_facts",\n{line}',
        )

# Remove wired items from FILL_UNIQUE_MAP if duplicated
for fn in ("sports.json", "literature.json", "malayalam.json"):
    if fn in created:
        gen = re.sub(rf'    "{fn}": \([^)]+\),\n', "", gen)

gen_path.write_text(gen, encoding="utf-8")
print("Updated generate_all_questions.py")
