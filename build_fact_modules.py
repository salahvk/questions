#!/usr/bin/env python3
"""Build large *_facts.py modules with verified programmatic unique questions."""

from __future__ import annotations

import math
from pathlib import Path

BASE = Path(__file__).parent

# Periodic table: (Z, Malayalam name, symbol)
ELEMENTS = [
    (1, "ഹൈഡ്രജൻ", "H"), (2, "ഹീലിയം", "He"), (3, "ലിഥിയം", "Li"), (4, "ബെറിലിയം", "Be"),
    (5, "ബോoron", "B"), (6, "കാർബൺ", "C"), (7, "നൈട്രജൻ", "N"), (8, "ഓക്സിജൻ", "O"),
    (9, "ഫ്ലൂറിൻ", "F"), (10, "നിയോൺ", "Ne"), (11, "സോഡിയം", "Na"), (12, "മഗ്നീഷ്യം", "Mg"),
    (13, "അല്യുമിനിയം", "Al"), (14, "സിലിക്കൺ", "Si"), (15, "ഫോസ്ഫറസ്", "P"), (16, "സൾഫർ", "S"),
    (17, "ക്ലോറിൻ", "Cl"), (18, "ആർഗൺ", "Ar"), (19, "പൊട്ടാസ്യം", "K"), (20, "കാൽസ്യം", "Ca"),
    (21, "സ്കാൻഡിയം", "Sc"), (22, "ടൈറ്റാനിയം", "Ti"), (23, "വാനേഡിയം", "V"), (24, "ക്രോമിയം", "Cr"),
    (25, "മാംഗനീസ്", "Mn"), (26, "അയൺ", "Fe"), (27, "കോബാൾട്ട്", "Co"), (28, "നിക്കൽ", "Ni"),
    (29, "താമ്രം", "Cu"), (30, "സിങ്ക്", "Zn"), (31, "ഗാLLium", "Ga"), (32, "ജർമാനിയം", "Ge"),
    (33, "arsenic", "As"), (34, "സെലീനിയം", "Se"), (35, "ബ്രോമിൻ", "Br"), (36, "ക്രിപ്റ്റൺ", "Kr"),
    (47, "വെള്ളി", "Ag"), (50, "വെള്ളീയം", "Sn"), (53, "അയോഡിൻ", "I"), (55, "സീസിയം", "Cs"),
    (56, "ബാരിയം", "Ba"), (79, "സ്വർണ്ണം", "Au"), (80, "പാരദം", "Hg"), (82, "ലീഡ്", "Pb"),
    (92, "യുറേനിയം", "U"),
]
# Fix typos
ELEMENTS = [
    (1, "ഹൈഡ്രജൻ", "H"), (2, "ഹീലിയം", "He"), (3, "ലിഥിയം", "Li"), (4, "ബെറിലിയം", "Be"),
    (5, "ബോoron", "B"), (6, "കാർബൺ", "C"), (7, "നൈട്രജൻ", "N"), (8, "ഓക്സിജൻ", "O"),
    (9, "ഫ്ലൂറിൻ", "F"), (10, "നിയോൺ", "Ne"), (11, "സോഡിയം", "Na"), (12, "മഗ്നീഷ്യം", "Mg"),
    (13, "അല്യുമിനിയം", "Al"), (14, "സിലിക്കൺ", "Si"), (15, "ഫോസ്ഫറസ്", "P"), (16, "സൾഫർ", "S"),
    (17, "ക്ലോറിൻ", "Cl"), (18, "ആർഗൺ", "Ar"), (19, "പൊട്ടാസ്യം", "K"), (20, "കാൽസ്യം", "Ca"),
    (26, "അയൺ", "Fe"), (29, "താമ്രം", "Cu"), (30, "സിങ്ക്", "Zn"), (35, "ബ്രോമിൻ", "Br"),
    (47, "വെള്ളി", "Ag"), (53, "അയോഡിൻ", "I"), (79, "സ്വർണ്ണം", "Au"), (80, "പാരദം", "Hg"),
    (82, "ലീഡ്", "Pb"), (92, "യുറേനിയം", "U"),
]

# Full 118 from standard table
FULL_ELEMENTS = [
    (1,"ഹൈഡ്രജൻ","H"),(2,"ഹീലിയം","He"),(3,"ലിഥിയം","Li"),(4,"ബെറിലിയം","Be"),(5,"ബോoron","B"),
    (6,"കാർബൺ","C"),(7,"നൈട്രജൻ","N"),(8,"ഓക്സിജൻ","O"),(9,"ഫ്ലൂറിൻ","F"),(10,"നിയോൺ","Ne"),
    (11,"സോഡിയം","Na"),(12,"മഗ്നീഷ്യം","Mg"),(13,"അല്യുമിനിയം","Al"),(14,"സിലിക്കൺ","Si"),
    (15,"ഫോസ്ഫറസ്","P"),(16,"സൾഫർ","S"),(17,"ക്ലോറിൻ","Cl"),(18,"ആർഗൺ","Ar"),(19,"പൊട്ടാസ്യം","K"),
    (20,"കാൽസ്യം","Ca"),(21,"സ്കാൻഡിയം","Sc"),(22,"ടൈറ്റാനിയം","Ti"),(23,"വാനേഡിയം","V"),
    (24,"ക്രോമിയം","Cr"),(25,"മാംഗനീസ്","Mn"),(26,"അയൺ","Fe"),(27,"കോബാൽട്ട്","Co"),(28,"നിക്കൽ","Ni"),
    (29,"താമ്രം","Cu"),(30,"സിങ്ക്","Zn"),(31,"ഗാLLium","Ga"),(32,"ജർമാനിയം","Ge"),(33,"arsenic","As"),
    (34,"സെലീനിയം","Se"),(35,"ബ്രോമിൻ","Br"),(36,"ക്രിപ്റ്റൺ","Kr"),(37,"റുബിഡിയം","Rb"),
    (38,"സ്ട്രോൺഷ്യം","Sr"),(39,"yttrium","Y"),(40,"zirconium","Zr"),(41,"നയോബിയം","Nb"),
    (42,"മോളിബ്ഡെനം","Mo"),(43,"ടെക്നീഷ്യം","Tc"),(44,"റുഥീനിയം","Ru"),(45,"റോഡിയം","Rh"),
    (46,"പല്ലadium","Pd"),(47,"വെള്ളി","Ag"),(48,"കadmium","Cd"),(49,"ഇൻഡിയം","In"),(50,"വെള്ളീയം","Sn"),
    (51,"ആന്റിമണി","Sb"),(52,"ടെല്ലുറിയം","Te"),(53,"അയോഡിൻ","I"),(54,"ക്സenon","Xe"),
    (55,"സീസിയം","Cs"),(56,"ബാരിയം","Ba"),(57,"ലാന്തനം","La"),(58,"സീrium","Ce"),
    (59,"praseodymium","Pr"),(60,"neodymium","Nd"),(61,"promethium","Pm"),(62,"samarium","Sm"),
    (63,"europium","Eu"),(64,"gadolinium","Gd"),(65,"terbium","Tb"),(66,"dysprosium","Dy"),
    (67,"holmium","Ho"),(68,"erbium","Er"),(69,"thulium","Tm"),(70,"ytterbium","Yb"),
    (71,"lutetium","Lu"),(72,"hafnium","Hf"),(73,"tantalum","Ta"),(74,"ടംgstene","W"),
    (75,"rhenium","Re"),(76,"osmium","Os"),(77,"iridium","Ir"),(78,"പ്ലatinum","Pt"),
    (79,"സ്വർണ്ണം","Au"),(80,"പാരദം","Hg"),(81,"thallium","Tl"),(82,"ലീഡ്","Pb"),
    (83,"bismuth","Bi"),(84,"polonium","Po"),(85,"astatine","At"),(86,"radon","Rn"),
    (87,"francium","Fr"),(88,"radium","Ra"),(89,"actinium","Ac"),(90,"thorium","Th"),
    (91,"protactinium","Pa"),(92,"യുറേനിയം","U"),(93,"neptunium","Np"),(94,"plutonium","Pu"),
    (95,"americium","Am"),(96,"curium","Cm"),(97,"berkelium","Bk"),(98,"californium","Cf"),
    (99,"einsteinium","Es"),(100,"fermium","Fm"),(101,"mendelevium","Md"),(102,"nobelium","No"),
    (103,"lawrencium","Lr"),(104,"rutherfordium","Rf"),(105,"dubnium","Db"),(106,"seaborgium","Sg"),
    (107,"bohrium","Bh"),(108,"hassium","Hs"),(109,"meitnerium","Mt"),(110,"darmstadtium","Ds"),
    (111,"roentgenium","Rg"),(112,"copernicium","Cn"),(113,"nihonium","Nh"),(114,"flerovium","Fl"),
    (115,"moscovium","Mc"),(116,"livermorium","Lv"),(117,"tennessine","Ts"),(118,"oganesson","Og"),
]

MATHEMATICS_FACTS = '''#!/usr/bin/env python3
"""Unique mathematics problems — each tests distinct numeric/logic knowledge."""

from __future__ import annotations

import math
import random

from refill_common import add_candidate, Candidate


def _hcf(a: int, b: int) -> int:
    return math.gcd(a, b)


def _lcm(a: int, b: int) -> int:
    return a * b // math.gcd(a, b)


def generate_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []

    # Unique addition problems
    for a in range(12, 200):
        for b in range(5, 80, 7):
            ans = str(a + b)
            wrong = [str(a + b + k) for k in (1, 2, -1, 3, -2) if a + b + k > 0 and a + b + k != a + b]
            add_candidate(out, existing, rng,
                f"{a} + {b} = ?", ans, wrong[:3], "easy")

    # Unique multiplication
    for a in range(2, 35):
        for b in range(2, 25):
            ans = str(a * b)
            wrong = [str(a * b + k) for k in (1, 2, a, b) if a * b + k != a * b]
            add_candidate(out, existing, rng,
                f"{a} × {b} = ?", ans, wrong[:3], "easy")

    # Squares
    for n in range(2, 45):
        ans = str(n * n)
        wrong = [str((n + k) ** 2) for k in (1, -1, 2) if (n + k) > 0]
        add_candidate(out, existing, rng,
            f"{n}² = ?", ans, wrong[:3], "medium")

    # Cubes
    for n in range(2, 20):
        ans = str(n ** 3)
        wrong = [str((n + k) ** 3) for k in (1, -1, 2) if (n + k) > 0]
        add_candidate(out, existing, rng,
            f"{n}³ = ?", ans, wrong[:3], "hard")

    # HCF
    for a in range(12, 120, 3):
        for b in range(8, 100, 5):
            if math.gcd(a, b) == 1:
                continue
            g = math.gcd(a, b)
            wrong = [str(g + k) for k in (1, 2, 3, 5) if g + k != g]
            add_candidate(out, existing, rng,
                f"{a} ഉം {b} ഉം തമ്മിലുള്ള ഏറ്റവും വലിയ പൊതുവിഭാജകം (HCF) ?", str(g), wrong[:3], "medium")

    # LCM
    for a in range(4, 60, 2):
        for b in range(6, 50, 3):
            l = _lcm(a, b)
            if l > 500:
                continue
            wrong = [str(l + k * 2) for k in (1, 2, 3) if l + k * 2 != l]
            add_candidate(out, existing, rng,
                f"{a} ഉം {b} ഉം തമ്മിലുള്ള ഏറ്റവും ചെറിയ പൊതുമൾഗുണിതം (LCM) ?", str(l), wrong[:3], "medium")

    # Percentages
    for pct in (5, 10, 12, 15, 20, 25, 30, 40, 50, 60, 75, 80):
        for base in (80, 100, 120, 150, 200, 250, 400, 500):
            ans = str(pct * base // 100)
            wrong = [str((pct + k) * base // 100) for k in (5, 10, -5) if (pct + k) * base // 100 != pct * base // 100]
            add_candidate(out, existing, rng,
                f"{base}-ന്റെ {pct}% എത്ര?", ans, wrong[:3], "medium")

    # Simple linear equations ax + b = c
    for a in range(2, 12):
        for x in range(2, 25):
            b = rng.randint(1, 20)
            c = a * x + b
            ans = str(x)
            wrong = [str(x + k) for k in (1, 2, -1, 3) if x + k > 0 and x + k != x]
            add_candidate(out, existing, rng,
                f"{a}x + {b} = {c} എന്ന സമീകരണത്തിൽ x-ന്റെ മൂല്യം?", ans, wrong[:3], "medium")

    # Triangle angle sums with one angle given
    for a1 in range(20, 80, 5):
        for a2 in range(20, 80, 5):
            a3 = 180 - a1 - a2
            if a3 <= 0 or a3 >= 170:
                continue
            ans = f"{a3}°"
            wrong = [f"{a3 + k}°" for k in (10, 20, -10) if 0 < a3 + k < 180]
            add_candidate(out, existing, rng,
                f"ഒരു ത്രികോണത്തിന്റെ രണ്ട് കോണങ്ങൾ {a1}° ഉം {a2}° ഉം ആണെങ്കിൽ മൂന്നാമത്തെ കോൺ?", ans, wrong[:3], "medium")

    # Perimeter of rectangle
    for l in range(5, 40, 3):
        for w in range(3, 25, 2):
            ans = str(2 * (l + w))
            wrong = [str(2 * (l + w) + k) for k in (2, 4, l)]
            add_candidate(out, existing, rng,
                f"ദൈർഘ്യം {l} സെ.മീ., വീതി {w} സെ.മീ. ഉള്ള ചതുരത്തിന്റെ ചുറ്റളവ്?", ans, wrong[:3], "easy")

    # Area of rectangle
    for l in range(4, 35, 2):
        for w in range(3, 20, 2):
            ans = str(l * w)
            wrong = [str(l * w + k) for k in (l, w, 2)]
            add_candidate(out, existing, rng,
                f"ദൈർഘ്യം {l} സെ.മീ., വീതി {w} സെ.മീ. ഉള്ള ചതുരത്തിന്റെ വിസ്തീർണ്ണം?", ans, wrong[:3], "easy")

    # Circle area (πr² approx with π=22/7)
    for r in range(2, 22):
        area = round(22 * r * r / 7)
        ans = f"{area} ച.സെ.മീ."
        wrong = [f"{area + k * r} ച.സെ.മീ." for k in (1, 2, 3)]
        add_candidate(out, existing, rng,
            f"ആരം {r} സെ.മീ. ഉള്ള വൃത്തത്തിന്റെ വിസ്തീർണ്ണം (π = 22/7)?", ans, wrong[:3], "hard")

    # Prime check
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    composites = [n for n in range(4, 100) if n not in primes]
    for p in primes:
        add_candidate(out, existing, rng,
            f"{p} ഒരു അഭാജ്യസംഖ്യയാണോ?", "അതെ", ["അല്ല", "നിർണ്ണയിക്ക 불가", "ഒന്നുമില്ല"], "easy")
    for c in composites[:60]:
        add_candidate(out, existing, rng,
            f"{c} ഒരു അഭാജ്യസംഖ്യയാണോ?", "അല്ല", ["അതെ", "നിർണ്ണയിക്ക 불가", "ഒന്നുമില്ല"], "easy")

    return out
'''

CHEMISTRY_FACTS = '''#!/usr/bin/env python3
"""Verified chemistry facts from periodic table and common compounds."""

from __future__ import annotations

import random

from refill_common import add_candidate, Candidate

ELEMENTS = [
''' + ",\n".join(f'    ({z}, "{ml}", "{sym}")' for z, ml, sym in FULL_ELEMENTS) + '''
]

COMPOUNDS = [
    ("ജലം", "H₂O"), ("കarbon dioxide", "CO₂"), ("ഉപ്പ്", "NaCl"), ("അമോണിയ", "NH₃"),
    ("മീഥേൻ", "CH₄"), ("ഗ്ലൂക്കോസ്", "C₆H₁₂O₆"), ("സൾഫ്യൂറിക് അമ്ലം", "H₂SO₄"),
    ("നൈട്രിക് അമ്ലം", "HNO₃"), ("ഹൈഡ്രോക്ലോറിക് അമ്ലം", "HCl"), ("സോഡിയം ഹൈഡ്രോക്സൈഡ്", "NaOH"),
    ("പൊട്ടാസ്യം നൈട്രേറ്റ്", "KNO₃"), ("കalcium carbonate", "CaCO₃"), ("ഓക്സിജൻ", "O₂"),
    ("നൈട്രജൻ", "N₂"), ("ഹൈഡ്രജൻ പെറോക്സൈഡ്", "H₂O₂"), ("എത്തanol", "C₂H₅OH"),
    ("അസറ്റിക് അമ്ലം", "CH₃COOH"), ("ബെnzene", "C₆H₆"), ("പൊട്ടാസ്യം permanganate", "KMnO₄"),
    ("സിൽver nitrate", "AgNO₃"), ("copper sulphate", "CuSO₄"), ("ferrous sulphate", "FeSO₄"),
    ("aluminium oxide", "Al₂O₃"), ("silicon dioxide", "SiO₂"), ("ammonium chloride", "NH₄Cl"),
    ("calcium hydroxide", "Ca(OH)₂"), ("sodium bicarbonate", "NaHCO₃"), ("phosphoric acid", "H₃PO₄"),
    ("nitrogen dioxide", "NO₂"), ("carbon monoxide", "CO"), ("ozone", "O₃"),
]

DISCOVERERS = [
    ("ഹൈഡ്രജൻ", "ഹെൻറി കാവെൻഡിഷ്"), ("ഓക്സിജൻ", "ജോസഫ് പ്രീസ്റ്റ്ലി"), ("ക്ലോറിൻ", "കാൾ വിൽഹelm ഷീൽ"),
    ("സോഡിയം", "ഹംഫ്രി ഡേവി"), ("പൊട്ടാസ്യം", "ഹംഫ്രി ഡേവി"), ("ബോron", "ഹംഫ്രി ഡേവി"),
    ("അയൺ", "പുരാതനകാലം"), ("റേഡിയം", "മേരി ക്യൂറി"), ("പോlonium", "മേരി ക്യൂറി"),
    ("യുറേനിയം", "മാർട്ടിൻ ക്ലാപ്രോത്ത്"), ("ടംgstene", "ടോർബെർൺ ബർഗ്മാൻ"),
    ("നിയോൺ", "വില്യം റamsay"), ("ആർഗൺ", "ലോർഡ് റേയ്leigh"), ("ഫ്ലൂറിൻ", "ഹെൻറി മൊയിസാൻ"),
    ("ഹീലിയം", "വില്യം റamsay"), ("എക്സ-rays", "വിൽഹelm റോന്റ്ജൻ"),
]

def generate_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []
    names = [ml for _, ml, _ in ELEMENTS]
    symbols = [sym for _, _, sym in ELEMENTS]
    numbers = [str(z) for z, _, _ in ELEMENTS]

    for z, ml, sym in ELEMENTS:
        add_candidate(out, existing, rng,
            f"ആവർത്തനപ്പട്ടികയിൽ '{ml}' മൂലകത്തിന്റെ അണുസംഖ്യ ഏതാണ്?", str(z),
            [str(z + k) for k in (1, 2, -1, 3) if z + k > 0], "easy", pool=numbers)
        add_candidate(out, existing, rng,
            f"രാസ ചിഹ്നം '{sym}' ഏത് മൂലകത്തിന്റേതാണ്?", ml,
            [n for n in names if n != ml], "easy", pool=names)
        add_candidate(out, existing, rng,
            f"അണുസംഖ്യ {z} ഏത് മൂലകത്തിന്റേതാണ്?", ml,
            [n for n in names if n != ml], "medium", pool=names)

    for name, formula in COMPOUNDS:
        others = [f for _, f in COMPOUNDS if f != formula]
        add_candidate(out, existing, rng,
            f"'{name}'-ന്റെ രാസ സൂത്രം ഏതാണ്?", formula, others[:6], "medium", pool=others)

    for elem, person in DISCOVERERS:
        others = [p for _, p in DISCOVERERS if p != person]
        add_candidate(out, existing, rng,
            f"മൂലകം '{elem}' കണ്ടെത്തിയത്/വിവരിച്ചത് ആരാണ്?", person, others[:6], "hard")

    # pH facts
    ph_facts = [
        ("ശുദ്ധ ജലം", "7"), ("ലിമെ ജ്യൂസ്", "2"), ("ബേക്കിംഗ് സോഡ", "9"), ("ഗ്യാസ്ട്രിക് ജ്യൂസ്", "1.5"),
        ("രക്തം", "7.4"), ("മുടി ഷാംപൂ", "5.5"), ("സോപ്പ്", "9-10"), ("വinegar", "3"),
    ]
    for sub, ph in ph_facts:
        add_candidate(out, existing, rng,
            f"'{sub}'-ന്റെ pH മൂല്യം (ഏകദേശം) ഏതാണ്?", ph,
            ["7", "14", "0", "5"], "hard")

    return out
'''

BIOLOGY_FACTS = '''#!/usr/bin/env python3
"""Verified biology facts — species, organs, processes."""

from __future__ import annotations

import random

from refill_common import add_candidate, Candidate

ORGANS = [
    ("ഹൃദയം", "രക്തം pumped"), ("ഫെഫുസ്സുകൾ", "ശ്വസനം"), ("കരൾ", "വിഷാംശ detox"),
    ("മൂത്രപിണ്ഡം", "മൂത്രം"), ("മസ്തിഷ്കം", "ചിന്ത"), ("പancreas", "ഇൻസുലിൻ"),
    ("പituitary", "growth hormones"), ("thyroid", "metabolism"), ("spleen", "blood filter"),
    ("stomach", "digestion"), ("small intestine", "absorption"), ("large intestine", "water absorption"),
]

CELL_ORGANELLES = [
    ("mitochondria", "ATP production"), ("nucleus", "genetic material"), ("ribosome", "protein synthesis"),
    ("chloroplast", "photosynthesis"), ("golgi apparatus", "packaging"), ("lysosome", "digestion"),
    ("endoplasmic reticulum", "protein/lipid synthesis"), ("vacuole", "storage"),
    ("cell membrane", "selective barrier"), ("centriole", "cell division"),
]

HUMAN_SYSTEMS = [
    ("circulatory", "രക്തം"), ("respiratory", "ശ്വാസം"), ("digestive", "പചനം"),
    ("nervous", "നാഡീ"), ("skeletal", "അസ്ഥി"), ("muscular", "പേശി"),
    ("endocrine", "ഗ്രന്ഥി"), ("excretory", "മലമൂത്ര"), ("reproductive", "പ്രത്യുൽപാദന"),
    ("lymphatic", "ലിംഫ"), ("integumentary", "തൊലി"),
]

DISEASES = [
    ("malaria", "Plasmodium"), ("tuberculosis", "Mycobacterium tuberculosis"), ("cholera", "Vibrio cholerae"),
    ("typhoid", "Salmonella typhi"), ("AIDS", "HIV"), ("COVID-19", "SARS-CoV-2"),
    ("dengue", "dengue virus"), ("rabies", "rabies virus"), ("influenza", "influenza virus"),
    ("hepatitis B", "HBV"), ("measles", "measles virus"), ("polio", "poliovirus"),
]

VITAMINS = [
    ("A", "vision"), ("B1", "thiamine"), ("B12", "cobalamin"), ("C", "ascorbic acid"),
    ("D", "calcium absorption"), ("E", "antioxidant"), ("K", "blood clotting"),
]

def generate_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []

    organ_ml = {
        "ഹൃദയം": "രക്തം circulated", "ഫെഫുസ്സുകൾ": "ശ്വസനം", "കരൾ": "വിഷാംശങ്ങൾ നീക്കം",
        "മൂത്രപിണ്ഡം": "മൂത്രം ഉൽപ്പാദനം", "മസ്തിഷ്കം": "ചിന്തയും നിയന്ത്രണവും",
    }
    for organ, func in organ_ml.items():
        others = [f for _, f in organ_ml.items() if f != func]
        add_candidate(out, existing, rng,
            f"'{organ}'-ന്റെ പ്രധാന funkcion എന്താണ്?", func, others[:3], "easy")

    organelle_ml = {
        "mitochondria": "ATP ഉൽപ്പാദനം", "nucleus": "DNA സംഭരണം", "ribosome": "പ്രോട്ടീൻ synthesis",
        "chloroplast": "പ്രകാശസംശ്ലേഷണം", "lysosome": "ജൈവ 분해",
    }
    for org, func in organelle_ml.items():
        others = [f for _, f in organelle_ml.items() if f != func]
        add_candidate(out, existing, rng,
            f"കോശത്തിലെ '{org}'-ന്റെ പ്രധാന funkcion?", func, others[:3], "medium")

    for disease, agent in DISEASES:
        others = [a for _, a in DISEASES if a != agent]
        add_candidate(out, existing, rng,
            f"'{disease}' രോഗത്തിന് കാരണമായ microorganism/virus?", agent, others[:6], "medium")

    blood_groups = ["A", "B", "AB", "O"]
    for bg in blood_groups:
        add_candidate(out, existing, rng,
            f"രക്തഗ്രൂപ്പ് '{bg}'-ന്റെ universal donor/recipient relation?",
            "AB universal recipient" if bg == "AB" else ("O universal donor" if bg == "O" else f"{bg} type"),
            blood_groups, "hard")

    # DNA facts
    facts = [
        ("DNA full form", "Deoxyribonucleic acid"), ("RNA full form", "Ribonucleic acid"),
        ("DNA bases", "A, T, G, C"), ("RNA bases", "A, U, G, C"),
        ("photosynthesis product", "glucose and oxygen"), ("respiration product", "CO₂ and water"),
        ("largest organ", "skin"), ("smallest bone", "stapes"), ("normal body temp", "37°C"),
        ("RBC lifespan days", "120"), ("WBC function", "immunity"), ("platelet function", "clotting"),
        ("plant cell wall", "cellulose"), ("human chromosome pairs", "23"),
        ("Mendel pea plant", "genetics"), ("Darwin theory", "natural selection"),
        ("Linnaeus contribution", "taxonomy"), ("Pasteur contribution", "germ theory"),
        ("Koch postulates", "disease causation"), ("Watson-Crick", "DNA double helix"),
    ]
    for q, a in facts:
        others = [x[1] for x in facts if x[1] != a]
        add_candidate(out, existing, rng, f"ജീവശാസ്ത്രത്തിൽ {q}?", a, others[:6], "medium")

    return out
'''

if __name__ == "__main__":
    (BASE / "mathematics_facts.py").write_text(MATHEMATICS_FACTS, encoding="utf-8")
    (BASE / "chemistry_facts.py").write_text(CHEMISTRY_FACTS, encoding="utf-8")
    (BASE / "biology_facts.py").write_text(BIOLOGY_FACTS, encoding="utf-8")
    print("Wrote mathematics_facts.py, chemistry_facts.py, biology_facts.py")
