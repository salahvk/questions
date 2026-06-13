#!/usr/bin/env python3
"""Wave 3: geography currencies, history templates, sports Olympics, economics math."""

from __future__ import annotations

import re
from pathlib import Path

BASE = Path(__file__).parent


def patch_file(path: Path, marker: str, block: str, before: str = "    return out\n") -> bool:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return False
    text = text.replace(before, block + before)
    path.write_text(text, encoding="utf-8")
    return True


# --- Geography: currencies + river lengths + population ---
geo_path = BASE / "geography_facts.py"
geo = geo_path.read_text(encoding="utf-8")

CURRENCY_BLOCK = '''
COUNTRY_CURRENCY: list[tuple[str, str]] = [
    ("ഇന്ത്യ", "രൂപ"), ("അമേരിക്ക", "ഡോളർ"), ("ബ്രിട്ടൻ", "പൗണ്ട്"), ("ജപ്പാൻ", "യെൻ"),
    ("ചൈന", "യുവാൻ"), ("യൂറോ സോൺ", "യൂറോ"), ("റഷ്യ", "റൂബിൾ"), ("ഓസ്ട്രേലിയ", "ഡോളർ"),
    ("കാനഡ", "ഡോളർ"), ("സ്വിറ്റ്സർലാൻഡ്", "ഫ്രാങ്ക്"), ("സൗദി അറേബ്യ", "റിയാൽ"),
    ("യുഎഇ", "ദിർഹാം"), ("ഖത്തർ", "റിയാൽ"), ("കുവൈത്ത്", "ദിനാർ"), ("ഓമാൻ", "റിയാൽ"),
    ("ബഹ്റൈൻ", "ദിനാർ"), ("പാകിസ്ഥാൻ", "റുപ്പി"), ("ബംഗ്ലാദേശ്", "ടാക്ക"), ("നേപ്പാൾ", "റുപ്പി"),
    ("ശ്രീലങ്ക", "റുപ്പി"), ("ഭൂട്ടാൻ", "ഗുൽട്രം"), ("മ്യാൻമാർ", "ക്യാറ്റ്"), ("തailand", "ബaat"),
    ("വിയറ്റ്നാം", "ഡോം"), ("മലേഷ്യ", "റിംഗിറ്റ്"), ("സിംഗപ്പൂർ", "ഡോളർ"), ("ഇന്തോനേഷ്യ", "റുപിയ"),
    ("ഫിലippines", "പെസോ"), ("ദക്ഷിണ കൊറിയ", "വോൺ"), ("ഉത്തര കൊറിയ", "വോൺ"), ("ഇറാൻ", "റിയാൽ"),
    ("ഇറാഖ്", "ദിനാർ"), ("ഇസ്രായൽ", "ഷെക്കൽ"), ("ജോർdan", "ദിനാർ"), ("ലെബanon", "പൗണ്ട്"),
    ("തുർക്കി", "ലിറ"), ("അഫ്ഗാനിസ്ഥാൻ", "അഫ്ഗാനി"), ("കസാഖ്സ്ഥാൻ", "ടെംഗ"), ("ഉസ്ബെക്കിസ്ഥാൻ", "സോം"),
    ("ജർമ്മനി", "യൂറോ"), ("ഫ്രാൻസ്", "യൂറോ"), ("ഇറ്റലി", "യൂറോ"), ("സ്പെയിൻ", "യൂറോ"),
    ("പോർച്ചുഗൽ", "യൂറോ"), ("നെതർലാൻഡ്", "യൂറോ"), ("ബെൽജിയം", "യൂറോ"), ("സ്വീഡൻ", "ക്രോണ"),
    ("നോർവേ", "ക്രോൺ"), ("ഡെൻമാർക്ക്", "ക്രോൺ"), ("ഫിൻലാൻഡ്", "യൂറോ"), ("പോളണ്ട്", "സ്ലോട്ടി"),
    ("ചെkkiya", "കൊറുന"), ("ഹംഗറി", "ഫോrint"), ("റൊമാനിയ", "ലeu"), ("ബൾgaria", "ലev"),
    ("ഗ്രീസ്", "യൂറോ"), ("അൽbania", "ലek"), ("ഐറ്ലൻഡ്", "യൂറോ"), ("ഐസ്‌ലാൻഡ്", "ക്രോന"),
    ("ബ്രസീൽ", "റിയാൽ"), ("അർജentina", "പെസോ"), ("ചിലി", "പെസോ"), ("കൊളംbia", "പെസോ"),
    ("പെru", "സോൾ"), ("മെക്സിക്കോ", "പെസോ"), ("ഗuatemala", "ക്വെറ്റ്സാൽ"), ("ഈജിപ്ത്", "പൗണ്ട്"),
    ("നൈജീരിയ", "നൈറ"), ("കെnya", "ഷില്ലിംഗ്"), ("ദക്ഷിണാഫ്രിക്ക", "റാൻഡ്"), ("മൊറocco", "ദിർഹാം"),
    ("അൾgeria", "ദിനാർ"), ("എthiopia", "ബിർr"), ("ഘana", "സedi"), ("ടanzania", "ഷillin"),
    ("ന്യൂസiland", "ഡോളർ"), ("ഫിജി", "ഡോളർ"),
]

INDIAN_RIVER_LENGTH: list[tuple[str, str]] = [
    ("ഗംഗ", "2,525 km"), ("യമുന", "1,376 km"), ("ബ്രഹ്മപുത്ര", "2,900 km"), ("ഗോദാവരി", "1,465 km"),
    ("കൃഷ്ണ", "1,400 km"), ("കാവേരി", "805 km"), ("നർമ്മദ", "1,312 km"), ("മഹാനദി", "858 km"),
    ("താപ്തി", "724 km"), ("ചംബൽ", "960 km"), ("ബേത്വ", "590 km"), ("സോൺ", "784 km"),
    ("കോസി", "729 km"), ("സത്ലജ്", "1,450 km"), ("ബിയാസ്", "470 km"), ("ചെന്നാബ്", "974 km"),
    ("അലക്കനന്ദ", "190 km"), ("ഭാഗീരഥി", "205 km"), ("പെരിയാർ", "244 km"), ("പമ്പ", "176 km"),
    ("ഭരതപ്പുഴ", "209 km"), ("നൈൽ", "6,650 km"), ("അമason", "6,400 km"), ("മിസിസippi", "3,730 km"),
    ("യാങ്റ്റ്സ്", "6,300 km"), ("ഡാന്യൂbe", "2,850 km"), ("റൈൻ", "1,230 km"), ("വോൾga", "3,530 km"),
    ("മെക്കോng", "4,350 km"), ("യൂഫ്രates", "2,800 km"), ("ടൈഗ്രിസ", "1,850 km"),
]

INDIAN_STATE_POPULATION: list[tuple[str, str]] = [
    ("ഉത്തരപ്രദേശ്", "19.98 കോടി"), ("മഹാരാഷ്ട്ര", "11.23 കോടി"), ("ബിഹാർ", "10.40 കോടി"),
    ("പശ്ചിമബംഗാൾ", "9.13 കോടി"), ("മധ്യപ്രദേശ്", "7.26 കോടി"), ("തമിഴ്നാട്", "7.21 കോടി"),
    ("രാജസ്ഥാൻ", "6.85 കോടി"), ("കർണാടക", "6.10 കോടി"), ("ഗുജറാത്ത്", "6.04 കോടി"),
    ("ആന്ധ്രപ്രദേശ്", "4.93 കോടി"), ("ഒഡിഷ", "4.19 കോടി"), ("തെലങ്കാന", "3.50 കോടി"),
    ("കേരളം", "3.34 കോടി"), ("ഝാർഖണ്ഡ്", "3.29 കോടി"), ("അസം", "3.12 കോടി"),
    ("പഞ്ചാബ്", "2.77 കോടി"), ("ഛത്തീസ്ഗഢ്", "2.55 കോടി"), ("ഹരിയാണ", "2.53 കോടി"),
    ("ദilli", "1.67 കോടി"), ("ജammu കശ്മീർ", "1.22 കോടി"), ("ഉത്തരാഖണ്ഡ്", "1.00 കോടി"),
    ("ഹിമാചൽ പ്രദേശ്", "68.6 ലക്ഷം"), ("ത്രിപുര", "36.7 ലക്ഷം"), ("മണിപ്പൂർ", "28.5 ലക്ഷം"),
    ("മേഘാലയ", "29.7 ലക്ഷം"), ("ഗോവ", "14.6 ലക്ഷം"), ("സിക്കിം", "6.1 ലക്ഷം"),
]
'''

if "COUNTRY_CURRENCY" not in geo:
    idx = geo.index("def _pick3")
    geo = geo[:idx] + CURRENCY_BLOCK + "\n" + geo[idx:]
    geo_path.write_text(geo, encoding="utf-8")
    print("Added COUNTRY_CURRENCY data to geography_facts.py")
    geo = geo_path.read_text(encoding="utf-8")

GEO_GEN = '''
    currencies = [c for _, c in COUNTRY_CURRENCY]
    countries_cur = [c for c, _ in COUNTRY_CURRENCY]
    for country, currency in COUNTRY_CURRENCY:
        if re.search(r"[A-Za-z]", country + currency):
            continue
        add(f"'{country}'-ന്റെ നാണയം/കറൻസി ഏതാണ്?", currency,
            [c for c in currencies if c != currency], "medium")
        add(f"'{currency}' ഏത് രാജ്യത്തിന്റെ നാണയമാണ്?", country,
            [c for c in countries_cur if c != country], "medium")

    lengths = [l for _, l in INDIAN_RIVER_LENGTH]
    rivers_l = [r for r, _ in INDIAN_RIVER_LENGTH]
    for river, length in INDIAN_RIVER_LENGTH:
        if re.search(r"[A-Za-z]", river):
            continue
        add(f"'{river}' നദിയുടെ ദൈർഘ്യം (ഏകദേശം)?", length,
            [l for l in lengths if l != length], "hard")
        add(f"ദൈർഘ്യം {length} olan പ്രധാന നദി '{river}'?", river,
            [r for r in rivers_l if r != river], "hard")

    pops = [p for _, p in INDIAN_STATE_POPULATION]
    states_p = [s for s, _ in INDIAN_STATE_POPULATION]
    for state, pop in INDIAN_STATE_POPULATION:
        if re.search(r"[A-Za-z]", state):
            continue
        add(f"'{state}' സംസ്ഥാനത്തിന്റെ ജനസംഖ്യ (2011 ഏകദേശം)?", pop,
            [p for p in pops if p != pop], "hard")
        add(f"ജനസംഖ്യ {pop} olan ഇന്ത്യൻ സംസ്ഥാനം?", state,
            [s for s in states_p if s != state], "hard")

    for country, capital in CAPITALS:
        add(f"'{capital}' തലസ്ഥാനമുള്ള '{country}'-ന്റെ തലസ്ഥാനം?", capital,
            [c for _, c in CAPITALS if c != capital][:3], "easy")
'''

if "COUNTRY_CURRENCY" in geo and "നാണയം/കറൻസി" not in geo:
    if "import re" not in geo:
        geo = geo.replace("from collections import defaultdict", "from collections import defaultdict\nimport re")
    patch_file(geo_path, "നാണയം/കറൻസി", GEO_GEN)
    print("Geography currency/river/population expansion")

# --- Indian history: extra templates ---
ih_path = BASE / "indian_history_facts.py"
ih = ih_path.read_text(encoding="utf-8")
IH_GEN = '''
    for act, year, wrong, diff in ACTS:
        pool = wrong + [year]
        _add(out, existing, rng, f"ബ്രിട്ടീഷ് ഭരണകാല '{act}' പ്രാബല്യ വർഷം?", year, pool, diff)
        _add(out, existing, rng, f"'{year}'-ൽ പ്രാബല്യത്തിൽ വന്ന ഇന്ത്യൻ നിയമം?", act,
             [a for a, _, _, _ in ACTS if a != act][:6], diff)

    for battle, year, wrong, diff in BATTLES:
        pool = wrong + [year]
        _add(out, existing, rng, f"ഇന്ത്യൻ/ലോക ചരിത്രത്തിൽ '{battle}' വർഷം?", year, pool, diff)

    for dyn, founder, wrong, diff in DYNASTIES:
        pool = wrong + [founder]
        _add(out, existing, rng, f"'{dyn}'-യുടെ സ്ഥാപകനായി അറിയപ്പെടുന്നവർ?", founder, pool, diff)

    for cap, capital, wrong, diff in DYNASTY_CAPITALS:
        pool = wrong + [capital]
        _add(out, existing, rng, f"'{cap}'-ന്റെ തലസ്ഥാനം?", capital, pool, diff)
        _add(out, existing, rng, f"'{capital}' ഏത് രാജവംശ/സാമ്രാജ്യത്തിന്റെ തലസ്ഥാനം?", cap,
             [c for c, _, _, _ in DYNASTY_CAPITALS], diff)
'''
if "ബ്രിട്ടീഷ് ഭരണകാല" not in ih:
    patch_file(ih_path, "ബ്രിട്ടീഷ് ഭരണകാല", IH_GEN)
    print("Indian history template expansion")

# --- World history: reverse templates on static facts ---
wh_path = BASE / "world_history_facts.py"
wh = wh_path.read_text(encoding="utf-8")
WH_GEN = '''
    stems = [q for q, _, _, _ in STATIC_FACTS]
    for q, ans, wrong, diff in STATIC_FACTS:
        _add(out, existing, rng, f"ലോക ചരിത്രത്തിൽ '{ans}' ഉത്തരമുള്ള ചോദ്യം?", q,
             [s for s in stems if s != q][:3], diff)
        if ans.isdigit() or re.match(r"^\\d{4}", ans):
            decades = [str(int(ans[:4]) // 10 * 10) + "s" if len(ans) >= 4 and ans[:4].isdigit() else ans]
            if decades[0] != ans:
                _add(out, existing, rng, f"വർഷം {ans} ഏത് ദശാബ്ദത്തിൽ?", decades[0] + " കാലം",
                     [str(int(d)+10)+"s കാലം" for d in range(1000,2030,10) if str(int(d)+10)+"s കാലം" != decades[0]+" കാലം"][:3], "hard")
'''
if "ലോക ചരിത്രത്തിൽ" not in wh:
    if "import re" not in wh:
        wh = wh.replace("import random", "import random\nimport re")
        wh_path.write_text(wh, encoding="utf-8")
    patch_file(wh_path, "ലോക ചരിത്രത്തിൽ", WH_GEN)
    print("World history reverse templates")

# --- Sports: Olympics + FIFA programmatic ---
sports_path = BASE / "sports_facts.py"
OLY_BLOCK = '''
OLYMPICS_HOSTS: list[tuple[str, str]] = [
    ("1896", "ഏതൻസ്"), ("1900", "പാരീസ്"), ("1908", "ലണ്ടൻ"), ("1924", "പാരീസ്"),
    ("1964", "ടോക്കിയോ"), ("1968", "മെക്സിക്കോ"), ("1972", "മ്യൂണിഖ്"), ("1980", "മോസ്കോ"),
    ("1984", "ലോസ് ആഞ്ചൽസ്"), ("1988", "സോൾ"), ("1992", "ബാർcelona"), ("1996", "അtlanta"),
    ("2000", "സിഡ്നി"), ("2004", "ഏതൻസ്"), ("2008", "ബെയ്‌ജിംഗ്"), ("2012", "ലndon"),
    ("2016", "റio"), ("2020", "ടokyo"), ("2024", "പാരീസ്"), ("2028", "ലos Angeles"),
    ("2032", "ബrisbane"),
]

FIFA_HOSTS: list[tuple[str, str]] = [
    ("1930", "ഉറuguay"), ("1934", "ഇറ്റലി"), ("1938", "ഫ്രാൻസ്"), ("1950", "ബ്രസീൽ"),
    ("1954", "സ്വിറ്റ്സർലാൻഡ്"), ("1958", "സ്വീഡൻ"), ("1962", "ചിലി"), ("1966", "ഇംഗ്ലണ്ട്"),
    ("1970", "മെക്സിക്കോ"), ("1974", "ജർമ്മനി"), ("1978", "അർജentina"), ("1982", "സ്പെയിൻ"),
    ("1986", "മെക്സിക്കോ"), ("1990", "ഇറ്റലി"), ("1994", "അമേരിക്ക"), ("1998", "ഫ്രാൻസ്"),
    ("2002", "ജപ്പാൻ"), ("2006", "ജർമ്മനി"), ("2010", "ദക്ഷിണാഫ്രിക്ക"),
    ("2014", "ബ്രസീൽ"), ("2018", "റഷ്യ"), ("2022", "ഖത്തർ"),
]
'''

sports = sports_path.read_text(encoding="utf-8")
if "OLYMPICS_HOSTS" not in sports:
    idx = sports.index("def generate_candidates")
    sports = sports[:idx] + OLY_BLOCK + "\n" + sports[idx:]
    sports_path.write_text(sports, encoding="utf-8")
    print("Added OLYMPICS_HOSTS to sports_facts.py")

sports = sports_path.read_text(encoding="utf-8")
if "ഒളിമ്പിക്സ് ആതിഥ്യ നഗരം" not in sports:
    SPORTS_GEN = '''
    years_o = [y for y, _ in OLYMPICS_HOSTS]
    cities_o = [c for _, c in OLYMPICS_HOSTS]
    for year, city in OLYMPICS_HOSTS:
        if not re.search(r"^[\\u0D00-\\u0D7F]", city):
            continue
        _add(out, existing, rng, f"{year} ഒളിമ്പിക്സ് ആതിഥ്യ നഗരം?", city,
             [c for c in cities_o if c != city and re.search(r"^[\\u0D00-\\u0D7F]", c)][:3], "medium")
        _add(out, existing, rng, f"'{city}' ഒളിമ്പിക്സ് ആതിഥ്യം വഹിച്ച വർഷം?", year,
             [y for y in years_o if y != year][:3], "medium")

    years_f = [y for y, _ in FIFA_HOSTS]
    hosts_f = [h for _, h in FIFA_HOSTS]
    for year, host in FIFA_HOSTS:
        if re.search(r"[A-Za-z]", host) and not re.search(r"^[\\u0D00-\\u0D7F]", host):
            continue
        _add(out, existing, rng, f"{year} FIFA ലോകകപ്പ് ആതിഥ്യ രാജ്യം?", host,
             [h for h in hosts_f if h != host][:3], "medium")
        _add(out, existing, rng, f"'{host}' FIFA ലോകകപ്പ് ആതിഥ്യം വഹിച്ച വർഷം?", year,
             [y for y in years_f if y != year][:3], "hard")
'''
    if "import re" not in sports:
        sports = sports.replace("import random", "import random\nimport re")
        sports_path.write_text(sports, encoding="utf-8")
    patch_file(sports_path, "ഒളിമ്പിക്സ് ആതിഥ്യ നഗരം", SPORTS_GEN)
    print("Sports Olympics/FIFA expansion")

# --- Economics: more percentage variants ---
eco_path = BASE / "economics_facts.py"
ECO_GEN = '''
    for pct in range(1, 100):
        for base in (50, 75, 125, 250, 500, 750, 1250, 2500, 5000, 10000):
            val = base * pct // 100
            ans = f"₹{val:,}".replace(",", ",")
            wrong = [f"₹{base * (pct + k) // 100:,}".replace(",", ",")
                     for k in (1, 2, 5, 10) if 0 < pct + k < 100 and base * (pct + k) // 100 != val][:3]
            _add(out, existing, rng, f"₹{base:,}-ന്റെ {pct}% എത്ര?".replace(",", ","), ans, wrong, "easy")

    for cost in range(100, 5000, 100):
        for margin in range(5, 50, 5):
            profit = cost * margin // 100
            sp = cost + profit
            wrong = [str(sp + k) for k in (cost, margin, 10) if sp + k != sp][:3]
            _add(out, existing, rng, f"വില ₹{cost}, ലാഭം {margin}% — വിൽപ്പന വില?", f"₹{sp}", wrong, "medium")
'''
if "വില ₹" not in eco_path.read_text(encoding="utf-8"):
    patch_file(eco_path, "വില ₹", ECO_GEN)
    print("Economics profit/percentage expansion")

# --- Chemistry: extend mole range ---
chem_path = BASE / "chemistry_facts.py"
chem = chem_path.read_text(encoding="utf-8")
if "for n in range(1, 50):" in chem:
    chem = chem.replace("for n in range(1, 50):", "for n in range(1, 80):")
    chem_path.write_text(chem, encoding="utf-8")
    print("Chemistry mole range extended to 79")

import importlib
import random
from refill_common import load_global_stems

checks = [
    ("geography.json", "geography_facts"),
    ("indian_history.json", "indian_history_facts"),
    ("world_history.json", "world_history_facts"),
    ("sports.json", "sports_facts"),
    ("economics.json", "economics_facts"),
    ("chemistry.json", "chemistry_facts"),
]
for fn, mod in checks:
    m = importlib.import_module(mod)
    importlib.reload(m)
    n = len(m.generate_candidates(load_global_stems(fn), random.Random(42)))
    print(f"{fn}: {n} candidates")
