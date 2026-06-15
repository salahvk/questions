#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate mi_wave20_facts.py and append_modern_india_wave20.py."""

from __future__ import annotations

import importlib.util
import pprint
import random
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "mi_wave20_facts.py"
APPEND = ROOT / "append_modern_india_wave20.py"

# Keep only helper block (lines 1–44) so re-runs do not duplicate generated content.
BASE = "\n".join(
    (ROOT / "mi_wave20_facts.py").read_text(encoding="utf-8").splitlines()[:44]
).rstrip()

EXTRA = '''

def _match_pairs(out, existing, rng, rows, templates, diff="medium"):
    pool = [f"{a} — {b}" for a, b in rows]
    for a, b in rows:
        correct = f"{a} — {b}"
        for tmpl in templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b, m=correct), correct, _pool(pool, correct)[:3], diff, pool)


from geography_facts import INDIAN_STATE_CAPITALS

'''

FWD = [
    "'{a}'-ന്റെ പ്രധാന സവിശേഷത/വിവരണം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
    "'{a}'-ന്റെ പ്രധാന ലക്ഷണം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട വിവരണം?",
    "'{a}'-ന്റെ പ്രധാന വിവരണം?",
    "'{a}' എന്തിനെ/ആരെ സൂചിപ്പിക്കുന്നു?",
]
REV = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട വസ്തു/വ്യക്തി/സംഭവം?",
    "'{b}'-ന്റെ പേരിലുള്ള/ബന്ധപ്പെട്ടത്?",
    "'{b}'-യുമായി ബന്ധപ്പെട്ടത്?",
]
FWD2 = [
    "ആധുനിക ഇന്ത്യയിൽ '{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വിവരണം?",
    "1947-ന് ശേഷമുള്ള ഇന്ത്യയിൽ '{a}'-ന്റെ പ്രധാന വിവരണം?",
]
REV2 = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വസ്തു/വ്യക്തി?",
    "'{b}'-ന്റെ പേരിലുള്ള/ബന്ധപ്പെട്ട വസ്തു?",
]
FWD3 = [
    "1947-ന് ശേഷമുള്ള ഇന്ത്യയിൽ '{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
    "'{a}'-ന്റെ പ്രധാന വിവരണം?",
    "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വിവരണം?",
]
REV3 = [
    "'{b}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന വസ്തു?",
    "'{b}'-ന്റെ പേരിലുള്ള വസ്തു?",
]
MATCH_T = [
    "'{a}'-യുമായി ബന്ധപ്പെട്ട ശരിയായ ജോഡി?",
    "താഴെ കൊടുത്തിരിക്കുന്നവയിൽ '{a}'-ന്റെ ശരിയായ ജോഡി?",
    "'{a}' — ശരിയായ വിവരണം?",
    "'{a}'-ന് അനുയോജ്യമായ വിവരണം?",
    "'{a}'-യുടെ ശരിയായ വിവരണം?",
]

CATS: dict[str, list[tuple[str, str]]] = {
"FYP_NICK": [
("ആദ്യ അഞ്ചുവർഷ പദ്ധതി","കാർഷിക പദ്ധതി"),("രണ്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി","ഭാരമേറിയ വ്യവസായ പദ്ധതി"),
("മൂന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി","സ്വയംപര്യാപ്തത"),("നാലാമത്തെ അഞ്ചുവർഷ പദ്ധതി","വികസനവും സ്ഥിരത"),
("അഞ്ചാമത്തെ അഞ്ചുവർഷ പദ്ധതി","ദാരിദ്ര്യ നിർമാർജനം"),("ആറാമത്തെ അഞ്ചുവർഷ പദ്ധതി","വികസനവും സാമൂഹിക നീതി"),
("ഏഴാമത്തെ അഞ്ചുവർഷ പദ്ധതി","സാമൂഹിക-സാമ്പത്തിക വികസനം"),("എട്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി","മനുഷ്യ വികസനം"),
("ഒമ്പതാമത്തെ അഞ്ചുവർഷ പദ്ധതി","വികസനവും സമത"),("പത്താമത്തെ അഞ്ചുവർഷ പദ്ധതി","സമഗ്ര വികസനം"),
("പതിനൊന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി","വേഗതയുള്ള സമഗ്ര വികസനം"),("പന്ത്രандാമത്തെ അഞ്ചുവർഷ പദ്ധതി","വേഗതയുള്ള സുസ്ഥിര വികസനം"),
("ആദ്യ അഞ്ചുവർഷ പദ്ധതി","1951–1956"),("രണ്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി","1956–1961"),
("മൂന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി","1961–1966"),("നാലാമത്തെ അഞ്ചുവർഷ പദ്ധതി","1969–1974"),
("അഞ്ചാമത്തെ അഞ്ചുവർഷ പദ്ധതി","1974–1979"),("ആറാമത്തെ അഞ്ചുവർഷ പദ്ധതി","1980–1985"),
("ഏഴാമത്തെ അഞ്ചുവർഷ പദ്ധതി","1985–1990"),("എട്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി","1992–1997"),
("ഒമ്പതാമത്തെ അഞ്ചുവർഷ പദ്ധതി","1997–2002"),("പത്താമത്തെ അഞ്ചുവർഷ പദ്ധതി","2002–2007"),
("പതിനൊന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി","2007–2012"),("പന്ത്രандാമത്തെ അഞ്ചുവർഷ പദ്ധതി","2012–2017"),
("അഞ്ചാമത്തെ അഞ്ചുവർഷ പദ്ധതി","ഗരീബി ഹടാവോ"),("രണ്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി","മഹാലനോബിസ് മാതൃക"),
("ആദ്യ അഞ്ചുവർഷ പദ്ധതി","പി.സി. മഹാലനോബിസ്"),("രണ്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി","പി.സി. മഹാലനോബിസ്"),
("മൂന്നാമത്തെ അഞ്ചുവർഷ പദ്ധതി","ഡി.ആർ. ഗഡ്ഗിൽ"),("നാലാമത്തെ അഞ്ചുവർഷ പദ്ധതി","ഡി.ആർ. ഗഡ്ഗിൽ"),
("അഞ്ചാമത്തെ അഞ്ചുവർഷ പദ്ധതി","ഡി.പി. ധർ"),("ആറാമത്തെ അഞ്ചുവർഷ പദ്ധതി","ഡി.ടി. ലക്ഷ്മണ"),
("ഏഴാമത്തെ അഞ്ചുവർഷ പദ്ധതി","ഡി.ടി. ലക്ഷ്മണ"),("എട്ടാമത്തെ അഞ്ചുവർഷ പദ്ധതി","ഡി.ടി. ലക്ഷ്മണ"),
("ഒമ്പതാമത്തെ അഞ്ചുവർഷ പദ്ധതി","ജെ.എൻ. സിൻഹ"),("പത്താമത്തെ അഞ്ചുവർഷ പദ്ധതി","കെ.സി. പന്ത്"),
],
}

# load extended categories
exec((ROOT / "_mi20_data2.py").read_text(encoding="utf-8"), {"CATS": CATS})

MATCH_ROWS: list[tuple[str, str]] = []
exec((ROOT / "_mi20_match.py").read_text(encoding="utf-8"), {"MATCH_ROWS": MATCH_ROWS})

TRIPLES: dict[str, list[tuple[str, str, str]]] = {}
exec((ROOT / "_mi20_triples.py").read_text(encoding="utf-8"), {"TRIPLES": TRIPLES})

DATA_BLOCK = "\n".join(
    f"{name}: list[tuple[str, str]] = " + pprint.pformat(rows, width=120)
    for name, rows in CATS.items()
)
TRIPLE_BLOCK = "\n".join(
    f"{name}: list[tuple[str, str, str]] = " + pprint.pformat(rows, width=120)
    for name, rows in TRIPLES.items()
)
MATCH_BLOCK = "MATCH_ROWS: list[tuple[str, str]] = " + pprint.pformat(MATCH_ROWS, width=120)

EMIT = textwrap.dedent(f"""
FWD = {FWD!r}
REV = {REV!r}
FWD2 = {FWD2!r}
REV2 = {REV2!r}
FWD3 = {FWD3!r}
REV3 = {REV3!r}
MATCH_T = {MATCH_T!r}


def _emit_pass(out, existing, rng, rows, fwd, rev):
    if not rows:
        return
    bs = list(dict.fromkeys(b for _, b in rows))
    as_ = list(dict.fromkeys(a for a, _ in rows))
    _pairs(out, existing, rng, rows, fwd, bs)
    _pairs_rev(out, existing, rng, rows, rev, as_)


def _emit_triple_pass(out, existing, rng, rows, ab, ac, bc):
    if not rows:
        return
    bs = list(dict.fromkeys(b for _, b, _ in rows))
    cs = list(dict.fromkeys(c for _, _, c in rows))
    as_ = list(dict.fromkeys(a for a, _, _ in rows))
    _triples(out, existing, rng, rows, ab, ac, bc, bs, cs, as_)


def _emit_all(out, existing, rng):
""")

for name in CATS:
    EMIT += f"    _emit_pass(out, existing, rng, {name}, FWD + FWD2 + FWD3, REV + REV2 + REV3)\n"
EMIT += "    _emit_pass(out, existing, rng, INDIAN_STATE_CAPITALS, FWD + FWD2 + FWD3, REV + REV2 + REV3)\n"
for name in TRIPLES:
    ab = [
        "'{a}'-യുമായി ബന്ധപ്പെട്ട '{b}'?",
        "'{a}'-ന്റെ '{b}'?",
        "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന '{b}'?",
        "'{a}'-യുമായി ബന്ധപ്പെട്ട '{b}'?",
    ]
    ac = [
        "'{a}'-യുമായി ബന്ധപ്പെട്ട '{c}'?",
        "'{a}'-ന്റെ '{c}'?",
        "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന '{c}'?",
    ]
    bc = [
        "'{b}'-യുമായി ബന്ധപ്പെട്ട '{a}'?",
        "'{c}'-യുമായി ബന്ധപ്പെട്ട '{a}'?",
        "'{b}' '{c}'-യുമായി ബന്ധപ്പെട്ട '{a}'?",
    ]
    EMIT += f"    _emit_triple_pass(out, existing, rng, {name}, {ab!r}, {ac!r}, {bc!r})\n"

EMIT += textwrap.dedent("""
    _match_pairs(out, existing, rng, MATCH_ROWS, MATCH_T)
    _match_pairs(out, existing, rng, MATCH_ROWS, MATCH_T[:3])


def generate_wave20_candidates(existing, rng):
    out = []
    _emit_all(out, existing, rng)
    return out


if __name__ == "__main__":
    r = random.Random(42)
    cands = generate_wave20_candidates(set(), r)
    print(f"Generated {len(cands)} unique candidates")
""")

content = BASE + EXTRA + DATA_BLOCK + "\n\n" + TRIPLE_BLOCK + "\n\n" + MATCH_BLOCK + "\n" + EMIT
OUT.write_text(content, encoding="utf-8")
print(f"Wrote {OUT} ({len(content)} bytes)")

APPEND.write_text(textwrap.dedent('''\
#!/usr/bin/env python3
"""Append wave-20 modern India questions (20 PSC topic types only)."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from mi_wave20_facts import generate_wave20_candidates
from refill_common import load_global_stems, max_id_num, spread_consecutive_templates

BASE = Path(__file__).parent
FILE = "modern_india.json"
PREFIX = "mi_"
TARGET = 2000
MIXED = re.compile(r"[\\u0D00-\\u0D7F][a-zA-Z]|[a-zA-Z][\\u0D00-\\u0D7F]")


def main() -> int:
    path = BASE / FILE
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.setdefault("questions", [])
    global_stems = load_global_stems(FILE)
    existing = {q["question"].strip() for q in questions}
    existing.update(global_stems)
    n = max_id_num(questions, PREFIX)

    rng = random.Random(42)
    pool = generate_wave20_candidates(set(existing), rng)
    rng.shuffle(pool)

    picked: list[dict] = []
    seen: set[str] = set()
    for q, opts, ans, diff in pool:
        if len(picked) >= TARGET:
            break
        if q in existing or q in seen:
            continue
        if len(set(opts)) != 4 or ans not in opts:
            continue
        if MIXED.search(q + "".join(opts) + ans):
            continue
        picked.append({"question": q, "options": opts, "answer": ans, "difficulty": diff})
        seen.add(q)

    spread = spread_consecutive_templates(picked, rng, max_run=2)
    added = 0
    for item in spread:
        n += 1
        questions.append(
            {
                "id": f"{PREFIX}{n:04d}",
                "question": item["question"],
                "options": item["options"],
                "answer": item["answer"],
                "difficulty": item["difficulty"],
            }
        )
        existing.add(item["question"])
        added += 1

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(f"{FILE}: +{added} (pool={len(pool)}, picked={len(picked)}, target={TARGET})")
    if added < TARGET:
        print(f"SHORTFALL: need {TARGET - added} more unique candidates")
        return 1

    subprocess.run([sys.executable, "apply_malayalam_rules.py", FILE], cwd=BASE, check=False)
    r = subprocess.run([sys.executable, "validate_questions.py", FILE], cwd=BASE)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
'''), encoding="utf-8")
print(f"Wrote {APPEND}")

spec = importlib.util.spec_from_file_location("mi_wave20_facts", OUT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
n = len(mod.generate_wave20_candidates(set(), random.Random(42)))
print(f"Candidate count: {n}")
if n < 2500:
    raise SystemExit(f"Pool too small: {n} < 2500")
