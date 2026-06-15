#!/usr/bin/env python3
"""Second wave: chemistry mole math, world history expansion, geography state areas."""

from __future__ import annotations

from pathlib import Path

BASE = Path(__file__).parent

# --- Chemistry: massive mole/mass calculations ---
chem_path = BASE / "chemistry_facts.py"
chem = chem_path.read_text(encoding="utf-8")
if "mol-ന്റെ പിണ്ഡം" not in chem:
    block = '''
    compounds_mm = [
        ("ജലം", "H₂O", 18), ("കarbon dioxide", "CO₂", 44), ("ഉപ്പ്", "NaCl", 58),
        ("അമോണിയ", "NH₃", 17), ("മീഥേൻ", "CH₄", 16), ("ഗ്ലൂക്കോസ്", "C₆H₁₂O₆", 180),
        ("സൾഫ്യൂറിക് അമ്ലം", "H₂SO₄", 98), ("നൈട്രിക് അമ്ലം", "HNO₃", 63),
        ("ഹൈഡ്രോക്ലോറിക് അമ്ലം", "HCl", 36), ("സോഡിയം ഹൈഡ്രോക്സൈഡ്", "NaOH", 40),
        ("ഓക്സിജൻ", "O₂", 32), ("നൈട്രജൻ", "N₂", 28), ("ഹൈഡ്രജൻ പെറോക്സൈഡ്", "H₂O₂", 34),
        ("എത്തanol", "C₂H₅OH", 46), ("അസറ്റിക് അമ്ലം", "CH₃COOH", 60),
        ("carbon monoxide", "CO", 28), ("ozone", "O₃", 48),
        ("calcium hydroxide", "Ca(OH)₂", 74), ("sodium bicarbonate", "NaHCO₃", 84),
        ("KNO₃", "KNO₃", 101), ("CuSO₄", "CuSO₄", 160), ("FeSO₄", "FeSO₄", 152),
        ("Al₂O₃", "Al₂O₃", 102), ("NH₄Cl", "NH₄Cl", 53), ("CaCO₃", "CaCO₃", 100),
    ]
    for name, formula, mm in compounds_mm:
        for n in range(1, 25):
            mass = mm * n
            wrong = [str(mass + k) for k in (mm, n, 1, 2, 10) if mass + k != mass][:3]
            add_candidate(out, existing, rng,
                f"'{name}' ({formula}) {n} mol-ന്റെ പിണ്ഡം (g) എത്ര?",
                str(mass), wrong, "medium")
            add_candidate(out, existing, rng,
                f"'{formula}' molar mass {mm} g/mol: {mass} g-ൽ mol എത്ര?",
                str(n), [str(n + k) for k in (1, 2, -1) if n + k > 0 and n + k != n][:3], "hard")

    avogadro = 6
    for n in range(1, 15):
        atoms = n * avogadro
        add_candidate(out, existing, rng,
            f"Avogadro (≈6×10²³): {n} mol-ൽ atom count (×10²³ units) എത്ര?",
            str(n * 6), [str(n * 6 + k) for k in (1, 2, n) if n * 6 + k != n * 6][:3], "hard")
'''
    chem = chem.replace("    return out\n", block + "\n    return out\n")
    chem_path.write_text(chem, encoding="utf-8")
    print("Chemistry mole expansion done")

# --- Geography: state areas (2011 census, sq km) ---
geo_path = BASE / "geography_facts.py"
geo = geo_path.read_text(encoding="utf-8")
if "INDIAN_STATE_AREA" not in geo:
    data = '''
INDIAN_STATE_AREA: list[tuple[str, str]] = [
    ("ആന്ധ്രപ്രദേശ്", "1,62,975"), ("അരുണാചൽ പ്രദേശ്", "83,743"), ("അസം", "78,438"),
    ("ബിഹാർ", "94,163"), ("ഛത്തീസ്ഗഢ്", "1,35,192"), ("ഗോവ", "3,702"), ("ഗുജറാത്ത്", "1,96,024"),
    ("ഹരിയാണ", "44,212"), ("ഹിമാചൽ പ്രദേശ്", "55,673"), ("ഝാർഖണ്ഡ്", "79,714"),
    ("കർണാടക", "1,91,791"), ("കേരളം", "38,863"), ("മധ്യപ്രദേശ്", "3,08,245"),
    ("മഹാരാഷ്ട്ര", "3,07,713"),     ("മണിപ്പൂർ", "22,327"), ("മേഘാലയ", "22,429"),
    ("\u0d2e\u0d3f\u0d34\u0d4b\u0d30\u0d02", "21,081"),
    ("\u0d28\u0d3e\u0d17\u0d32\u0d3e\u0d02\u0d21\u0d4d", "16,579"), ("ഒഡിഷ", "1,55,707"),
    ("പഞ്ചാബ്", "50,362"), ("രാജസ്ഥാൻ", "3,42,239"), ("സിക്കിം", "7,096"),
    ("തമിഴ്നാട്", "1,30,058"), ("തെലങ്കാന", "1,12,077"), ("ത്രിപുര", "10,486"),
    ("ഉത്തരാഖണ്ഡ്", "53,483"), ("ഉത്തരപ്രദേശ്", "2,40,928"),     ("പശ്ചിമബംഗാൾ", "88,752"),
    ("\u0d1c\u0d3e\u0d2e\u0d4d\u0d2e\u0d42 \u0d15\u0d36\u0d4d\u0d36\u0d40\u0d30\u0d4d", "1,01,387"),
    ("\u0d32\u0d26\u0d3e\u0d16\u0d4d", "59,146"), ("\u0d26\u0d3f\u0d32\u0d4d\u0d32\u0d3f", "1,484"),
]
'''
    idx = geo.index("def _pick3")
    geo = geo[:idx] + data + geo[idx:]
    gen = '''
    areas = [a for _, a in INDIAN_STATE_AREA]
    for state, area in INDIAN_STATE_AREA:
        if any(c.isascii() and c.isalpha() for c in state):
            continue
        states = [s for s, _ in INDIAN_STATE_AREA if not any(c.isascii() and c.isalpha() for c in s)]
        add(f"'{state}'-ന്റെ വിസ്തീർണ്ണം (sq km)?", area, [a for a in areas if a != area], "hard")
        add(f"വിസ്തീർണ്ണം {area} sq km olan ഇന്ത്യൻ സംസ്ഥാനം?", state, [s for s in states if s != state], "hard")
'''
    gen = gen.replace("olan", " olan")  # fix typo
    gen = '''
    areas = [a for _, a in INDIAN_STATE_AREA]
    for state, area in INDIAN_STATE_AREA:
        if any(c.isascii() and c.isalpha() for c in state):
            continue
        states = [s for s, _ in INDIAN_STATE_AREA if not any(c.isascii() and c.isalpha() for c in s)]
        add(f"'{state}'-ന്റെ വിസ്തീർണ്ണം (sq km)?", area, [a for a in areas if a != area], "hard")
        add(f"വിസ്തീർണ്ണം {area} sq km ആയ ഇന്ത്യൻ സംസ്ഥാനം?", state, [s for s in states if s != state], "hard")
'''
    geo = geo.replace("    return out\n", gen + "\n    return out\n")
    geo_path.write_text(geo, encoding="utf-8")
    print("Geography area expansion done")

# --- World history: programmatic century questions ---
wh_path = BASE / "world_history_facts.py"
wh = wh_path.read_text(encoding="utf-8")
if "century" not in wh:
    block = '''
    events = [
        ("1776", "18"), ("1789", "18"), ("1815", "19"), ("1914", "20"), ("1939", "20"),
        ("1945", "20"), ("1969", "20"), ("1989", "20"), ("2001", "21"), ("1492", "15"),
        ("1066", "11"), ("1215", "13"), ("1453", "15"), ("1649", "17"), ("1688", "17"),
        ("1848", "19"), ("1905", "20"), ("1917", "20"), ("1941", "20"), ("1957", "20"),
        ("1961", "20"), ("1975", "20"), ("1986", "20"), ("1991", "20"),
    ]
    centuries = list({c for _, c in events})
    for year, century in events:
        _add(out, existing, rng, f"വർഷം {year} ഏത് നൂറ്റാണ്ടിലാണ്?", century + " നൂറ്റാണ്ട്",
             [c + " നൂറ്റാണ്ട്" for c in centuries if c != century], "medium")
        _add(out, existing, rng, f"{century} നൂറ്റാണ്ടിലെ പ്രധാന വർഷം?", year,
             [y for y, _ in events if y != year], "hard")
'''
    wh = wh.replace("    return out\n", block + "\n    return out\n")
    wh_path.write_text(wh, encoding="utf-8")
    print("World history century expansion done")

import importlib, random
for mod in ["chemistry_facts", "geography_facts", "world_history_facts"]:
    m = importlib.import_module(mod)
    importlib.reload(m)
    print(mod, len(m.generate_candidates(set(), random.Random(42))))
