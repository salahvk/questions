#!/usr/bin/env python3
"""Add programmatic candidate generation to science modules + world history facts."""

from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).parent

# --- Physics programmatic block ---
PHYSICS_PATCH = '''
    # --- programmatic numeric problems ---
    for mass in range(2, 55):
        for acc in range(1, 12):
            f_val = mass * acc
            wrong = [str(f_val + k) for k in (1, 2, 3, mass) if f_val + k != f_val][:3]
            _add(out, existing, rng,
                f"F = ma: m = {mass} kg, a = {acc} m/s² ആയാൽ F എത്ര N?",
                str(f_val), wrong, "medium")

    for vel in range(5, 45, 5):
        for mass in range(2, 30, 2):
            ke = vel * vel * mass // 2
            wrong = [str(ke + k) for k in (vel, mass, 10, 50) if ke + k != ke][:3]
            _add(out, existing, rng,
                f"KE = ½mv²: m = {mass} kg, v = {vel} m/s ആയാൽ KE എത്ര J?",
                str(ke), wrong, "hard")

    for volt in range(2, 25):
        for curr in range(1, 11):
            p_val = volt * curr
            wrong = [str(p_val + k) for k in (1, 2, volt, curr) if p_val + k != p_val][:3]
            _add(out, existing, rng,
                f"P = VI: V = {volt} V, I = {curr} A ആയാൽ P എത്ര W?",
                str(p_val), wrong, "medium")

    v_sound = 340
    for freq in range(170, 3401, 170):
        if v_sound % freq != 0:
            continue
        lam = v_sound // freq
        if lam < 1 or lam > 20:
            continue
        wrong = [str(lam + k) for k in (1, 2, -1) if lam + k > 0 and lam + k != lam][:3]
        _add(out, existing, rng,
            f"ശബ്ദവേഗം 340 m/s, ആവൃത്തി {freq} Hz ആയാൽ തരംഗദൈർഘ്യം എത്ര m?",
            str(lam), wrong, "hard")

    for dist in range(10, 200, 10):
        for time in range(2, 21, 2):
            if dist % time != 0:
                continue
            spd = dist // time
            wrong = [str(spd + k) for k in (1, 2, -1) if spd + k > 0 and spd + k != spd][:3]
            _add(out, existing, rng,
                f"ദൂരം {dist} m, സമയം {time} s ആയാൽ വേഗം എത്ര m/s?",
                str(spd), wrong, "easy")
'''

phys_path = BASE / "physics_facts.py"
phys_src = phys_path.read_text(encoding="utf-8")
if "# --- programmatic numeric problems ---" not in phys_src:
    phys_src = phys_src.replace("    return out\n", PHYSICS_PATCH + "\n    return out\n")
    phys_path.write_text(phys_src, encoding="utf-8")
    print("Patched physics_facts.py")

# --- Chemistry reverse compounds + group questions ---
CHEM_PATCH = '''
    for name, formula in COMPOUNDS:
        names = [n for n, _ in COMPOUNDS]
        formulas = [f for _, f in COMPOUNDS]
        _add(out, existing, rng,
            f"രാസസൂത്രം '{formula}' ഏത് ചേർമ്മിന്റെതാണ്?",
            name, [n for n in names if n != name][:6], "medium")

    for z, ml, sym in ELEMENTS:
        _add(out, existing, rng,
            f"'{ml}' മൂലകത്തിന്റെ രാസ ചിഹ്നം ഏതാണ്?",
            sym, [s for _, _, s in ELEMENTS if s != sym][:6], "easy")
'''

chem_path = BASE / "chemistry_facts.py"
chem_src = chem_path.read_text(encoding="utf-8")
if "രാസസൂത്രം '" not in chem_src:
    # chemistry uses add_candidate not _add - patch before return
    chem_src = chem_src.replace(
        "    return out\n",
        CHEM_PATCH.replace("_add", "add_candidate").replace(
            ', diff)', ', diff, pool=names if "names" in dir() else None)'
        ) + "\n    return out\n",
    )
    # Fix: chemistry uses add_candidate with different signature
    CHEM_BLOCK = '''
    for name, formula in COMPOUNDS:
        cnames = [n for n, _ in COMPOUNDS]
        cforms = [f for _, f in COMPOUNDS]
        add_candidate(out, existing, rng,
            f"രാസസൂത്രം '{formula}' ഏത് ചേർമ്മിന്റെതാണ്?",
            name, [n for n in cnames if n != name][:6], "medium", pool=cnames)
        add_candidate(out, existing, rng,
            f"'{name}'-ന്റെ രാസസൂത്രം '{formula}' അല്ലാത്തത് ഏത്?",
            formula, [f for f in cforms if f != formula][:6], "hard", pool=cforms)

    for z, ml, sym in ELEMENTS:
        add_candidate(out, existing, rng,
            f"'{ml}' മൂലകത്തിന്റെ രാസ ചിഹ്നം ഏതാണ്?",
            sym, [s for _, _, s in ELEMENTS if s != sym][:6], "easy", pool=symbols)
'''
    chem_src = chem_path.read_text(encoding="utf-8")
    if "രാസസൂത്രം '" not in chem_src:
        chem_src = chem_src.replace("    return out\n", CHEM_BLOCK + "\n    return out\n")
        chem_path.write_text(chem_src, encoding="utf-8")
        print("Patched chemistry_facts.py")

# --- World history facts module from JSON + extra data ---
WH_EXTRA = [
    ("1917-ലെ റഷ്യൻ വിപ്ലവം?", "1917", ["1914", "1920", "1939"], "medium"),
    ("1789-ലെ ഫ്രഞ്ച് വിപ്ലവം?", "1789", ["1776", "1815", "1848"], "easy"),
    ("1945-ൽ ജർമ്മൻ സമർപ്പം?", "1945", ["1944", "1946", "1943"], "easy"),
    ("1969-ൽ ചന്ദ്രനിലanding?", "1969", ["1968", "1970", "1972"], "easy"),
    ("1989-ൽ ബർлин മതിൽ തകർച്ച?", "1989", ["1987", "1991", "1985"], "medium"),
    ("2001-ൽ സെപ്റ്റംബർ 11 ആക്രമണം?", "2001", ["2000", "2003", "1999"], "easy"),
    ("1492-ൽ Columbus അമേരിക്ക കണ്ടെത്തൽ?", "1492", ["1488", "1500", "1510"], "medium"),
    ("1861-1865 അമേരിക്കൻ ഗ്രഹമഹായുദ്ധം?", "1861", ["1857", "1870", "1776"], "medium"),
    ("1947-ൽ ഇന്ത്യ-പാകിസ്ഥാൻ വിഭജനം?", "1947", ["1945", "1950", "1942"], "easy"),
    ("1950-ൽ കൊറിയൻ യുദ്ധം?", "1950", ["1945", "1960", "1939"], "medium"),
    ("1979-ൽ ഇറാൻൻ വിപ്ലവം?", "1979", ["1975", "1985", "1969"], "hard"),
    ("1991-ൽ സോവിയറ്റ് യൂണിയൻ വിഘടനം?", "1991", ["1989", "1993", "1985"], "medium"),
    ("1215-ൽ മാഗ്ന കാർട്ട?", "1215", ["1066", "1492", "1776"], "hard"),
    ("1066-ൽ നോർമൻ征服?", "1066", ["1215", "1492", "1776"], "hard"),
    ("1453-ൽ കോൺസ്റ്റാന്റിനോപ്പിൾ падение?", "1453", ["1492", "1066", "1215"], "hard"),
    ("1649-ൽ ചാർൾസ് I വധം?", "1649", ["1688", "1776", "1789"], "hard"),
    ("1688-ൽ ഗ്ലോറിയസ് വിപ്ലവം?", "1688", ["1649", "1776", "1789"], "hard"),
    ("1776-ൽ അമേരിക്കൻ സ്വാതന്ത്ര്യം?", "1776", ["1789", "1812", "1861"], "easy"),
    ("1815-ൽ വാട്ടർloo യുദ്ധം?", "1815", ["1789", "1805", "1914"], "medium"),
    ("1848-ൽ യൂറോപ്പിലെ വിപ്ലവ വർഷം?", "1848", ["1789", "1917", "1939"], "hard"),
    ("1867-ൽ അമേരിക്കൻ കൊളonial expansion Alaska?", "1867", ["1848", "1776", "1914"], "hard"),
    ("1905-ൽ റഷ്യൻ-ജപ്പാൻ യുദ്ധം?", "1905", ["1914", "1898", "1939"], "hard"),
    ("1914-ൽ WWI ആരംഭം?", "1914", ["1939", "1905", "1945"], "easy"),
    ("1939-ൽ WWII ആരംഭം?", "1939", ["1914", "1945", "1929"], "easy"),
    ("1941-ൽ Pearl Harbor?", "1941", ["1939", "1945", "1950"], "medium"),
    ("1945-ൽ Hiroshima?", "1945", ["1944", "1946", "1941"], "medium"),
    ("1957-ൽ Sputnik?", "1957", ["1969", "1945", "1961"], "medium"),
    ("1961-ൽ Berlin Wall?", "1961", ["1989", "1957", "1945"], "medium"),
    ("1975-ൽ Vietnam War അവസാനം?", "1975", ["1969", "1980", "1950"], "hard"),
    ("1986-ൽ Chernobyl?", "1986", ["1989", "1991", "1979"], "hard"),
]

WH_EXTRA = [e for e in WH_EXTRA if not any("a" <= c <= "z" or "A" <= c <= "Z" for c in e[0] + e[1])]

WARS = [
    ("ഒന്നാം ലോകമഹായുദ്ധം", "1914-1918"),
    ("രണ്ടാം ലോകമഹായുദ്ധം", "1939-1945"),
    ("നാപോളിയൻ യുദ്ധങ്ങൾ", "1803-1815"),
    ("അമേരിക്കൻ ഗ്രഹമഹായുദ്ധം", "1861-1865"),
    ("കൊറിയൻ യുദ്ധം", "1950-1953"),
    ("വിയറ്റ്നാം യുദ്ധം", "1955-1975"),
    ("ഗൾഫ് യുദ്ധം", "1990-1991"),
    ("ക്രിമിയൻ യുദ്ധം", "1853-1856"),
    ("റഷ്യൻ-ജപ്പാൻ യുദ്ധം", "1904-1905"),
    ("ബൂർ യുദ്ധം", "1899-1902"),
]

REVOLUTIONS = [
    ("ഫ്രഞ്ച് വിപ്ലവം", "1789"),
    ("റഷ്യൻ വിപ്ലവം", "1917"),
    ("അമേരിക്കൻ വിപ്ലവം", "1776"),
    ("ചൈനീസ് വിപ്ലവം", "1949"),
    ("ക്യൂബൻ വിപ്ലവം", "1959"),
    ("ഇറാൻ വിപ്ലവം", "1979"),
    ("1848 വിപ്ലവങ്ങൾ", "1848"),
    ("ഒക്ടോബർ വിപ്ലവം", "1917"),
]

TREATIES = [
    ("വേഴ്സailles ഉടമ്പടി", "1919"),
    ("യാൽത്താ ഉടമ്പടി", "1945"),
    ("പോട്സdam ഉടമ്പടി", "1945"),
    ("NATO സ്ഥാപനം", "1949"),
    ("EU സ്ഥാപനം (Maastricht)", "1993"),
    ("ലോക تجارت സംഘടന", "1995"),
]

def load_wh_static() -> list[tuple[str, str, list[str], str]]:
    path = BASE / "world_history.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    rows: list[tuple[str, str, list[str], str]] = []
    seen: set[str] = set()
    for q in data.get("questions", []):
        stem = q.get("question", "").strip()
        ans = q.get("answer", "").strip()
        opts = q.get("options", [])
        diff = q.get("difficulty", "medium")
        wrong = [o for o in opts if o != ans][:3]
        if not stem or stem in seen:
            continue
        if any("a" <= c <= "z" or "A" <= c <= "Z" for c in stem + ans + "".join(wrong)):
            continue
        seen.add(stem)
        rows.append((stem, ans, wrong, diff))
    for row in WH_EXTRA:
        if row[0] not in seen:
            seen.add(row[0])
            rows.append(row)
    return rows

STATIC = load_wh_static()

WH_MODULE = f'''#!/usr/bin/env python3
"""Verified world history facts for unique Malayalam PSC question generation."""

from __future__ import annotations

import random

Candidate = tuple[str, list[str], str, str]


def _pick(pool: list[str], correct: str, rng: random.Random) -> list[str]:
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

STATIC_FACTS: list[tuple[str, str, list[str], str]] = {STATIC!r}

WARS: list[tuple[str, str]] = {WARS!r}

REVOLUTIONS: list[tuple[str, str]] = {REVOLUTIONS!r}

TREATIES: list[tuple[str, str]] = {TREATIES!r}


def generate_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []
    for q, ans, wrong, diff in STATIC_FACTS:
        _add(out, existing, rng, q, ans, wrong + [ans], diff)

    war_names = [w for w, _ in WARS]
    war_years = [y for _, y in WARS]
    for war, years in WARS:
        _add(out, existing, rng, f"'{{war}}' നടന്ന കാലഘട്ടം?", years, war_years, "medium")
        _add(out, existing, rng, f"'{{years}}' കാലഘട്ടത്തിലെ യുദ്ധം?", war, war_names, "medium")

    rev_names = [r for r, _ in REVOLUTIONS]
    rev_years = [y for _, y in REVOLUTIONS]
    for rev, year in REVOLUTIONS:
        _add(out, existing, rng, f"'{{rev}}' നടന്ന വർഷം?", year, rev_years, "medium")
        _add(out, existing, rng, f"'{{year}}'-ലെ പ്രധാന വിപ്ലവം?", rev, rev_names, "medium")

    treaty_names = [t for t, _ in TREATIES]
    treaty_years = [y for _, y in TREATIES]
    for treaty, year in TREATIES:
        _add(out, existing, rng, f"'{{treaty}}' ഉടമ്പടി/സംഘടന വർഷം?", year, treaty_years, "hard")
        _add(out, existing, rng, f"'{{year}}'-ലെ പ്രധാന അന്താരാഷ്ട്ര ഉടമ്പടി?", treaty, treaty_names, "hard")

    return out
'''

(BASE / "world_history_facts.py").write_text(WH_MODULE, encoding="utf-8")
print(f"Created world_history_facts.py: {len(STATIC)} static facts")

# Patch generate_all_questions.py
gen_path = BASE / "generate_all_questions.py"
gen_src = gen_path.read_text(encoding="utf-8")
if '"world_history.json": "world_history_facts"' not in gen_src:
    gen_src = gen_src.replace(
        '"physics_facts": "physics_facts",\n}',
        '"physics_facts": "physics_facts",\n    "world_history.json": "world_history_facts",\n}',
    )
    gen_src = gen_src.replace(
        '    "physics.json": "physics_facts",\n}',
        '    "physics.json": "physics_facts",\n    "world_history.json": "world_history_facts",\n}',
    )
    if '"world_history.json": "world_history_facts"' not in gen_src:
        gen_src = gen_src.replace(
            '"physics.json": "physics_facts",',
            '"physics.json": "physics_facts",\n    "world_history.json": "world_history_facts",',
        )
    gen_path.write_text(gen_src, encoding="utf-8")
    print("Wired world_history_facts in generate_all_questions.py")

import random
import importlib

for mod in ["physics_facts", "chemistry_facts", "world_history_facts"]:
    m = importlib.import_module(mod)
    importlib.reload(m)
    n = len(m.generate_candidates(set(), random.Random(42)))
    print(f"{mod} candidates: {n}")
