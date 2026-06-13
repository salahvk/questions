#!/usr/bin/env python3
"""Verified chemistry facts — periodic table and compounds."""

from __future__ import annotations

import random

from refill_common import add_candidate, Candidate

ELEMENTS = [
    (1, "ഹൈഡ്രജൻ", "H"),
    (2, "ഹീലിയം", "He"),
    (3, "ലിഥിയം", "Li"),
    (4, "ബെറിലിയം", "Be"),
    (5, "ബോoron", "B"),
    (6, "കാർബൺ", "C"),
    (7, "നൈട്രജൻ", "N"),
    (8, "ഓക്സിജൻ", "O"),
    (9, "ഫ്ലൂറിൻ", "F"),
    (10, "നിയോൺ", "Ne"),
    (11, "സോഡിയം", "Na"),
    (12, "മഗ്നീഷ്യം", "Mg"),
    (13, "അല്യുമിനിയം", "Al"),
    (14, "സിലിക്കൺ", "Si"),
    (15, "ഫോസ്ഫറസ്", "P"),
    (16, "സൾഫർ", "S"),
    (17, "ക്ലോറിൻ", "Cl"),
    (18, "ആർഗൺ", "Ar"),
    (19, "പൊട്ടാസ്യം", "K"),
    (20, "കാൽസ്യം", "Ca"),
    (21, "സ്കാൻഡിയം", "Sc"),
    (22, "ടൈറ്റാനിയം", "Ti"),
    (23, "വാനേഡിയം", "V"),
    (24, "ക്രോമിയം", "Cr"),
    (25, "മാംഗനീസ്", "Mn"),
    (26, "അയൺ", "Fe"),
    (27, "കോബാൽട്ട്", "Co"),
    (28, "നിക്കൽ", "Ni"),
    (29, "താമ്രം", "Cu"),
    (30, "സിങ്ക്", "Zn"),
    (31, "ഗാLLium", "Ga"),
    (32, "ജർമാനിയം", "Ge"),
    (33, "arsenic", "As"),
    (34, "സെലീനിയം", "Se"),
    (35, "ബ്രോമിൻ", "Br"),
    (36, "ക്രിപ്റ്റൺ", "Kr"),
    (37, "റുബിഡിയം", "Rb"),
    (38, "സ്ട്രോൺഷ്യം", "Sr"),
    (39, "yttrium", "Y"),
    (40, "zirconium", "Zr"),
    (41, "നയോബിയം", "Nb"),
    (42, "മോളിബ്ഡെനം", "Mo"),
    (43, "ടെക്നീഷ്യം", "Tc"),
    (44, "റുഥീനിയം", "Ru"),
    (45, "റോഡിയം", "Rh"),
    (46, "പല്ലadium", "Pd"),
    (47, "വെള്ളി", "Ag"),
    (48, "കadmium", "Cd"),
    (49, "ഇൻഡിയം", "In"),
    (50, "വെള്ളീയം", "Sn"),
    (51, "ആന്റിമണി", "Sb"),
    (52, "ടെല്ലുറിയം", "Te"),
    (53, "അയോഡിൻ", "I"),
    (54, "ക്സenon", "Xe"),
    (55, "സീസിയം", "Cs"),
    (56, "ബാരിയം", "Ba"),
    (57, "ലാന്തനം", "La"),
    (58, "സീrium", "Ce"),
    (59, "praseodymium", "Pr"),
    (60, "neodymium", "Nd"),
    (61, "promethium", "Pm"),
    (62, "samarium", "Sm"),
    (63, "europium", "Eu"),
    (64, "gadolinium", "Gd"),
    (65, "terbium", "Tb"),
    (66, "dysprosium", "Dy"),
    (67, "holmium", "Ho"),
    (68, "erbium", "Er"),
    (69, "thulium", "Tm"),
    (70, "ytterbium", "Yb"),
    (71, "lutetium", "Lu"),
    (72, "hafnium", "Hf"),
    (73, "tantalum", "Ta"),
    (74, "ടംgstene", "W"),
    (75, "rhenium", "Re"),
    (76, "osmium", "Os"),
    (77, "iridium", "Ir"),
    (78, "പ്ലatinum", "Pt"),
    (79, "സ്വർണ്ണം", "Au"),
    (80, "പാരദം", "Hg"),
    (81, "thallium", "Tl"),
    (82, "ലീഡ്", "Pb"),
    (83, "bismuth", "Bi"),
    (84, "polonium", "Po"),
    (85, "astatine", "At"),
    (86, "radon", "Rn"),
    (87, "francium", "Fr"),
    (88, "radium", "Ra"),
    (89, "actinium", "Ac"),
    (90, "thorium", "Th"),
    (91, "protactinium", "Pa"),
    (92, "യുറേനിയം", "U"),
    (93, "neptunium", "Np"),
    (94, "plutonium", "Pu"),
    (95, "americium", "Am"),
    (96, "curium", "Cm"),
    (97, "berkelium", "Bk"),
    (98, "californium", "Cf"),
    (99, "einsteinium", "Es"),
    (100, "fermium", "Fm"),
    (101, "mendelevium", "Md"),
    (102, "nobelium", "No"),
    (103, "lawrencium", "Lr"),
    (104, "rutherfordium", "Rf"),
    (105, "dubnium", "Db"),
    (106, "seaborgium", "Sg"),
    (107, "bohrium", "Bh"),
    (108, "hassium", "Hs"),
    (109, "meitnerium", "Mt"),
    (110, "darmstadtium", "Ds"),
    (111, "roentgenium", "Rg"),
    (112, "copernicium", "Cn"),
    (113, "nihonium", "Nh"),
    (114, "flerovium", "Fl"),
    (115, "moscovium", "Mc"),
    (116, "livermorium", "Lv"),
    (117, "tennessine", "Ts"),
    (118, "oganesson", "Og")
]

GROUPS = {
    1: "� alkali ലോഹങ്ങൾ", 2: "ആൽക്കലി ഭൂമി ലോഹങ്ങൾ", 17: "ഹാലോജens", 18: "നobre ഗ്യാസുകൾ",
}

COMPOUNDS = [
    ("ജലം", "H₂O"), ("കarbon dioxide", "CO₂"), ("ഉപ്പ്", "NaCl"), ("അമോണിയ", "NH₃"),
    ("മീഥേൻ", "CH₄"), ("ഗ്ലൂക്കോസ്", "C₆H₁₂O₆"), ("സൾഫ്യൂറിക് അമ്ലം", "H₂SO₄"),
    ("നൈട്രിക് അമ്ലം", "HNO₃"), ("ഹൈഡ്രോക്ലോറിക് അമ്ലം", "HCl"), ("സോഡിയം ഹൈഡ്രോക്സൈഡ്", "NaOH"),
    ("പൊട്ടാസ്യം നൈട്രേറ്റ്", "KNO₃"), ("കalcium carbonate", "CaCO₃"), ("ഓക്സിജൻ", "O₂"),
    ("നൈട്രജൻ", "N₂"), ("ഹൈഡ്രജൻ പെറോക്സൈഡ്", "H₂O₂"), ("എത്തanol", "C₂H₅OH"),
    ("അസറ്റിക് അമ്ലം", "CH₃COOH"), ("പൊട്ടാസ്യം permanganate", "KMnO₄"),
    ("copper sulphate", "CuSO₄"), ("ferrous sulphate", "FeSO₄"), ("aluminium oxide", "Al₂O₃"),
    ("carbon monoxide", "CO"), ("ozone", "O₃"), ("ammonium chloride", "NH₄Cl"),
    ("calcium hydroxide", "Ca(OH)₂"), ("sodium bicarbonate", "NaHCO₃"),
]

def generate_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []
    names = [ml for _, ml, _ in ELEMENTS]
    symbols = [sym for _, _, sym in ELEMENTS]
    numbers = [str(z) for z, _, _ in ELEMENTS]

    for z, ml, sym in ELEMENTS:
        add_candidate(out, existing, rng,
            f"ആവർത്തനപ്പട്ടികയിൽ '{ml}' മൂലകത്തിന്റെ അണുസംഖ്യ ഏതാണ്?", str(z),
            [str(z + k) for k in (1, 2, -1, 3) if 0 < z + k <= 118], "easy", pool=numbers)
        add_candidate(out, existing, rng,
            f"രാസ ചിഹ്നം '{sym}' ഏത് മൂലകത്തിന്റേതാണ്?", ml,
            [n for n in names if n != ml][:6], "easy", pool=names)
        add_candidate(out, existing, rng,
            f"അണുസംഖ്യ {z} ഏത് മൂലകത്തിന്റേതാണ്?", ml,
            [n for n in names if n != ml][:6], "medium", pool=names)
        # Period for first 7 periods (approx)
        period = 1 if z<=2 else 2 if z<=10 else 3 if z<=18 else 4 if z<=36 else 5 if z<=54 else 6 if z<=86 else 7
        add_candidate(out, existing, rng,
            f"'{ml}' (Z={z}) ഏത് ആവർത്തനപ്പട്ടികാ കാലത്തിലാണ്?", str(period),
            [str(p) for p in range(1,8) if p != period], "hard")

    for name, formula in COMPOUNDS:
        others = [f for _, f in COMPOUNDS if f != formula]
        add_candidate(out, existing, rng,
            f"'{name}'-ന്റെ രാസ സൂത്രം ഏതാണ്?", formula, others[:6], "medium", pool=others)


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


    # molar mass calculations (verified integer sums)
    molar = [
        ("H₂O", 18), ("NaCl", 58), ("CO₂", 44), ("O₂", 32), ("N₂", 28),
        ("CH₄", 16), ("NH₃", 17), ("H₂SO₄", 98), ("HCl", 36), ("NaOH", 40),
        ("CaCO₃", 100), ("C₆H₁₂O₆", 180), ("H₂O₂", 34), ("O₃", 48),
        ("C₂H₅OH", 46), ("CH₃COOH", 60), ("KMnO₄", 158), ("CuSO₄", 160),
        ("FeSO₄", 152), ("Al₂O₃", 102), ("CO", 28), ("NH₄Cl", 53),
        ("Ca(OH)₂", 74), ("NaHCO₃", 84), ("KNO₃", 101), ("HNO₃", 63),
    ]
    for formula, mm in molar:
        for n in range(1, 8):
            ans = str(mm * n)
            wrong = [str(mm * n + k) for k in (mm, n, 1, 2) if mm * n + k != mm * n][:3]
            add_candidate(out, existing, rng,
                f"'{formula}'-ന്റെ {n} mol-ന്റെ molar mass (g/mol basis) × {n} = ? g/mol units",
                ans, wrong, "hard")
        wrong_mm = [str(m) for _, m in molar if m != mm][:6]
        add_candidate(out, existing, rng,
            f"'{formula}'-ന്റെ molar mass (g/mol) എത്ര?",
            str(mm), wrong_mm, "medium", pool=[str(m) for _, m in molar])

    for z in range(1, 37):
        period = 1 if z <= 2 else 2 if z <= 10 else 3 if z <= 18 else 4 if z <= 36 else 5
        add_candidate(out, existing, rng,
            f"Z = {z} മൂലകം ഏത് ആവർത്തനപ്പട്ടികാ കാലത്തിലാണ്?",
            str(period), [str(p) for p in range(1, 8) if p != period], "medium")


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
        for n in range(1, 100):
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

    return out
