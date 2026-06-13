#!/usr/bin/env python3
"""Fill astronomy.json to 4000 unique Kerala PSC-style Malayalam questions.

Prefer `refill_astronomy_unique.py` for full rebuilds — it removes template filler
and refuses to pad with numbered fake objects when facts run short.
"""

import json
import random
import re
import subprocess
from pathlib import Path

from astronomy_facts import (
    ASTRONOMERS_EXT,
    DEEP_SKY,
    DISCOVERIES,
    EVENTS,
    MISSIONS_EXT,
    MOONS_EXT,
    STARS_EXT,
    TERMS,
)

BASE = Path(__file__).parent
TARGET = 4000
PREFIX = "ast_"

# Banned template-filler patterns — shared with refill_astronomy_unique.py
FILLER_PATTERNS = [
    re.compile(r"^ആകാശ വസ്തു '.+' ഏത് (തരത്തിൽ പെടുന്നു|നക്ഷത്രസമൂഹം/പ്രദേശത്താണ്)"),
    re.compile(r"എക്സ്പ്ലോറർ-\d+"),
    re.compile(r"പയനിയർ-\d+"),
    re.compile(r"മാരിനർ-\d+"),
    re.compile(r"ഗാലക്സി NGC-\d+"),
    re.compile(r"ക്ഷുദ്രഗ്രഹം [^\s']+-\d+"),
    re.compile(r"ഇൻസാറ്റ്-\d+"),
    re.compile(r"IRS-\d+"),
    re.compile(r"GSAT-\d+"),
    re.compile(r"ജ്യോതിശാസ്ത്ര ചരിത്രത്തിൽ '.+' സംബന്ധിച്ച പ്രധാന വർഷം"),
    re.compile(r"വസ്തുത-\d+"),
    re.compile(r"പ്രദേശം-\d+"),
]


def is_filler(question: str) -> bool:
    return any(p.search(question) for p in FILLER_PATTERNS)


def load_existing_questions() -> set[str]:
    existing: set[str] = set()
    for path in BASE.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for q in data.get("questions", []):
            text = q.get("question", "").strip()
            if text:
                existing.add(text)
    return existing


def max_id_num(questions: list[dict]) -> int:
    pat = re.compile(rf"^{re.escape(PREFIX)}(\d+)$")
    mx = 0
    for q in questions:
        m = pat.match(q.get("id", ""))
        if m:
            mx = max(mx, int(m.group(1)))
    return mx


def make_entry(num: int, q: str, opts: list[str], ans: str, diff: str) -> dict:
    shuffled = list(opts)
    random.shuffle(shuffled)
    return {
        "id": f"{PREFIX}{num:04d}",
        "question": q,
        "options": shuffled,
        "answer": ans,
        "difficulty": diff,
    }


def add_q(questions: list, existing: set, num: int, q: str, opts: list[str], ans: str, diff: str) -> int:
    q = q.strip()
    if not q or q in existing or is_filler(q):
        return num
    opts = [ans] + [o for o in opts if o != ans]
    opts = list(dict.fromkeys(opts))
    if len(opts) < 4:
        opts.extend(pick_distractors(opts, ans, 4 - len(opts)))
    opts = opts[:4]
    if ans not in opts or len(set(opts)) != 4:
        return num
    entry = make_entry(num, q, opts, ans, diff)
    questions.append(entry)
    existing.add(q)
    return num + 1


def pick_distractors(pool: list[str], correct: str, n: int = 3) -> list[str]:
    choices = list(dict.fromkeys(x for x in pool if x != correct))
    if len(choices) < n:
        extras = [
            "1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020",
            "ബുധൻ", "ശുക്രൻ", "ഭൂമി", "ചൊവ്വ", "വ്യാഴം", "ശനി",
            "സിറിയസ്", "ബെറ്റൽജൂസ്", "ധ്രുവനക്ഷത്രം",
            "നാസ", "ഇസ്റോ", "ഇ.എസ്.എ", "റോസ്കോസ്മോസ്",
        ]
        for x in extras:
            if x != correct and x not in choices:
                choices.append(x)
    return random.sample(choices, min(n, len(choices)))


# --- factual data ---
PLANETS = [
    ("ബുധൻ", "മെർക്കുറി", "0.39 AU", "4879 കി.മീ.", "0", "59 ദിവസം", "88 ദിവസം", "easy"),
    ("ശുക്രൻ", "വീനസ്", "0.72 AU", "12104 കി.മീ.", "0", "243 ദിവസം", "225 ദിവസം", "easy"),
    ("ഭൂമി", "എർത്ത്", "1 AU", "12742 കി.മീ.", "1", "24 മണിക്കൂർ", "365 ദിവസം", "easy"),
    ("ചൊവ്വ", "മാർസ്", "1.52 AU", "6779 കി.മീ.", "2", "24.6 മണിക്കൂർ", "687 ദിവസം", "easy"),
    ("വ്യാഴം", "ജൂപ്പിറ്റർ", "5.2 AU", "139820 കി.മീ.", "95+", "10 മണിക്കൂർ", "12 വർഷം", "easy"),
    ("ശനി", "സാറൺ", "9.5 AU", "116460 കി.മീ.", "146+", "10.7 മണിക്കൂർ", "29 വർഷം", "easy"),
    ("യുറാനസ്", "യുറാനസ്", "19.2 AU", "50724 കി.മീ.", "27+", "17 മണിക്കൂർ", "84 വർഷം", "medium"),
    ("നെപ്റ്റ്യൂൺ", "നെപ്ടൂൺ", "30.1 AU", "49244 കി.മീ.", "16", "16 മണിക്കൂർ", "165 വർഷം", "medium"),
]

MOONS = [
    ("ചന്ദ്രൻ", "ഭൂമി"), ("ഫോബോസ്", "ചൊവ്വ"), ("ഡീമോസ്", "ചൊവ്വ"),
    ("അയോ", "വ്യാഴം"), ("യൂറോപ്പ", "വ്യാഴം"), ("ഗാനിമീഡ്", "വ്യാഴം"), ("കല്ലിസ്റ്റോ", "വ്യാഴം"),
    ("ടൈറ്റൻ", "ശനി"), ("റിയ", "ശനി"), ("എൻസെലാഡസ്", "ശനി"), ("മൈമസ്", "ശനി"),
    ("ടൈറ്റാനിയ", "യുറാനസ്"), ("ഒബറോൺ", "യുറാനസ്"), ("ട്രൈടൺ", "നെപ്റ്റ്യൂൺ"),
    ("ചാരൺ", "പ്ലൂട്ടോ"), ("ടിറ്റാൻ", "ശനി"),
]

STARS = [
    ("സിറിയസ്", "വ്യാധം", "ഏറ്റവും തിളക്കമുള്ള നക്ഷത്രം", "easy"),
    ("കനോപസ്", "കർത്തിക", "രണ്ടാമത്തെ തിളക്കമുള്ള നക്ഷത്രം", "medium"),
    ("ആൽഫ സെന്റോറി", "സെന്റോറസ്", "സൂര്യനോട് ഏറ്റവും അടുത്തുള്ള നക്ഷത്ര വ്യവസ്ഥ", "medium"),
    ("പ്രോക്സിമ സെന്റോറി", "സെന്റോറസ്", "സൂര്യനോട് ഏറ്റവും അടുത്തുള്ള ഒറ്റ നക്ഷത്രം", "hard"),
    ("ബെറ്റൽജൂസ്", "ഓറിയോൺ", "ചുവന്ന സൂപ്പർജയന്റ്", "medium"),
    ("റിഗൽ", "ഓറിയോൺ", "നീല സൂപ്പർജയന്റ്", "hard"),
    ("ധ്രുവനക്ഷത്രം", "ചെറു മഞ്ഞ", "വടക്ക് ദിശ കാണിക്കുന്ന നക്ഷത്രം", "easy"),
    ("വേഗ", "ലയ്ര", "ആകാശത്തിലെ അഞ്ചാമത്തെ തിളക്കമുള്ള നക്ഷത്രം", "hard"),
    ("ആൽതാർ", "വൃശ്ചികം", "വൃശ്ചികത്തിലെ തിളക്കമുള്ള നക്ഷത്രം", "hard"),
    ("പോളാർസ്റ്റാർ", "ചെറു മഞ്ഞ", "ധ്രുവനക്ഷത്രത്തിന്റെ ഇംഗ്ലീഷ് പേര്", "medium"),
]

MISSIONS = [
    ("ചന്ദ്രയാൻ-3", "ഇസ്റോ", "2023", "ചന്ദ്രൻ", "medium"),
    ("ചന്ദ്രയാൻ-1", "ഇസ്റോ", "2008", "ചന്ദ്രൻ", "medium"),
    ("ചന്ദ്രയാൻ-2", "ഇസ്റോ", "2019", "ചന്ദ്രൻ", "medium"),
    ("മംഗള്യാൻ", "ഇസ്റോ", "2013", "ചൊവ്വ", "medium"),
    ("ആദിത്യ-എൽ1", "ഇസ്റോ", "2023", "സൂര്യൻ", "medium"),
    ("ആര്യഭട്ട", "ഇസ്റോ", "1975", "ഭൂമി", "easy"),
    ("ഗഗന്യാൻ", "ഇസ്റോ", "—", "മനുഷ്യ ബഹിരാകാശ യാത്ര", "medium"),
    ("അപ്പോളോ 11", "നാസ", "1969", "ചന്ദ്രൻ", "easy"),
    ("അപ്പോളോ 13", "നാസ", "1970", "ചന്ദ്രൻ", "medium"),
    ("വോയാജർ-1", "നാസ", "1977", "ബഹിരാകാശം", "medium"),
    ("വോയാജർ-2", "നാസ", "1977", "ബഹിരാകാശം", "medium"),
    ("ഹബിൾ", "നാസ/ഇ.എസ്.എ", "1990", "ബഹിരാകാശ നിരീക്ഷണം", "medium"),
    ("ജയിംസ് വെബ്", "നാസ/ഇ.എസ്.എ", "2021", "ബഹിരാകാശ നിരീക്ഷണം", "medium"),
    ("സ്പുട്നിക് 1", "സോവിയറ്റ് യൂണിയൻ", "1957", "ഭൂമി", "easy"),
    ("ഗഗാരിൻ ദൗത്യം", "സോവിയറ്റ് യൂണിയൻ", "1961", "ഭൂമി", "easy"),
    ("പെർസിവറൻസ്", "നാസ", "2020", "ചൊവ്വ", "hard"),
    ("ക്യൂരിയോസിറ്റി", "നാസ", "2011", "ചൊവ്വ", "hard"),
    ("ക്യാസിനി-ഹൈഗൻസ്", "നാസ/ഇ.എസ്.എ", "1997", "ശനി", "hard"),
    ("ന്യൂ ഹൊറൈസൺസ്", "നാസ", "2006", "പ്ലൂട്ടോ", "hard"),
    ("പാർക്കർ സോളാർ പ്രോബ്", "നാസ", "2018", "സൂര്യൻ", "hard"),
]

ASTRONOMERS = [
    ("ഗലീലിയോ ഗലീലി", "ടെലിസ്കോപ്പ് വാനനിരീക്ഷണം", "easy"),
    ("നിക്കോളസ് കോപ്പർണിക്കസ്", "ഹീലിയോസെൻട്രിക് സിദ്ധാന്തം", "easy"),
    ("ജൊഹാൻ കെപ്ലർ", "ഗ്രഹ ചലന നിയമങ്ങൾ", "medium"),
    ("ഐസക് ന്യൂട്ടൺ", "ഗുരുത്വാകർഷണ നിയമം", "easy"),
    ("എഡ്വിൻ ഹബിൾ", "പ്രപഞ്ച വികാസം", "medium"),
    ("ജോർജസ് ലെമൈറ്റർ", "മഹാവിസ്ഫോടന സിദ്ധാന്തം", "hard"),
    ("വില്യം ഹേഴ്സൽ", "യുറാനസ് കണ്ടെത്തൽ", "medium"),
    ("ജോൺ ഗോട്രീബ് ഗാല", "നെപ്റ്റ്യൂൺ കണ്ടെത്തൽ", "hard"),
    ("സ്റ്റീഫൻ ഹോക്കിങ്", "ബ്ലാക്ക് ഹോൾ ഗവേഷണം", "medium"),
    ("ജോൺ വീൽ", "ബ്ലാക്ക് ഹോൾ പദം", "hard"),
    ("ആര്യഭടൻ", "ഭാരതീയ ജ്യോതിശാസ്ത്രം", "medium"),
    ("വരാഹമിഹിരൻ", "ബൃഹത്സംഹിത", "hard"),
    ("വിക്രം സാരാഭായി", "ഇന്ത്യൻ ബഹിരാകാശ പ്രവർത്തനം", "easy"),
    ("എ.പി.ജെ. അബ്ദുൽ കലാം", "ഇസ്റോ റോക്കറ്റ് വികസനം", "easy"),
]

CONCEPTS = [
    ("പ്രകാശവർഷം", "പ്രകാശം ഒരു വർഷത്തിൽ സഞ്ചരിക്കുന്ന ദൂരം", "easy"),
    ("ഓർബിറ്റ്", "ഒരു വസ്തു മറ്റൊന്നിനെ ചുറ്റി കറങ്ങുന്ന പാത", "easy"),
    ("നെബുല", "വാതകവും പൊടിയും നിറഞ്ഞ മേഖല", "medium"),
    ("ക്വാസാർ", "അത്യന്തം തിളക്കമുള്ള സക്രിയ ഗാലക്സി കേന്ദ്രം", "hard"),
    ("പൾസാർ", "വേഗത്തിൽ കറങ്ങുന്ന ന്യൂട്രോൺ നക്ഷത്രം", "hard"),
    ("സൂപ്പർനോവ", "വൻ നക്ഷത്ര സ്ഫോടനം", "medium"),
    ("ബ്ലാക്ക് ഹോൾ", "ഗുരുത്വാകർഷണം കാരണം പ്രകാശം പുറത്തുപോകാത്ത പ്രദേശം", "medium"),
    ("ഗാലക്സി", "കോടിക്കണക്കിന് നക്ഷത്രങ്ങളുടെ സമൂഹം", "easy"),
    ("ക്ഷുദ്രഗ്രഹം", "സൂര്യനെ വലംവെക്കുന്ന ചെറിയ ശിലാകൃതി", "medium"),
    ("ധൂമകേതു", "ഐസ്-ധൂളി നിറഞ്ഞ സൗരയൂഥ വസ്തു", "medium"),
    ("ഉൽക്ക", "ഭൂമിയുടെ അന്തരീക്ഷത്തിൽ കരിഞ്ഞുപോകുന്ന ബഹിരാകാശ വസ്തു", "easy"),
    ("ഗ്രഹണം", "ഒരു വസ്തു മറ്റൊന്നെ മറയ്ക്കുന്ന പ്രതിഭാസം", "easy"),
    ("അഭികേന്ദ്രബലം", "ഭ്രമണത്തിന് കാരണമായ ബലം", "medium"),
    ("ഹരിതഗൃഹ പ്രഭാവം", "അന്തരീക്ഷ വാതകങ്ങൾ താപനില ഉയർത്തുന്ന പ്രക്രിയ", "medium"),
    ("ആകാശഗംഗ", "സൗരയൂഥം ഉൾപ്പെടുന്ന ഗാലക്സി", "easy"),
    ("ആൻഡ്രോമീഡ", "ആകാശഗംഗയോട് ഏറ്റവും അടുത്തുള്ള വലിയ ഗാലക്സി", "medium"),
    ("ഓർയൻ നെബുല", "ഓറിയോൺ താരസമൂഹത്തിലെ പ്രശസ്ത നെബുല", "hard"),
    ("ക്രാബ് നെബുല", "സൂപ്പർനോവ ശേഷമുള്ള നെബുല", "hard"),
    ("ഹെയ്ഗൻസ് ബോൾഷോവ്", "മഹാവിസ്ഫോടന സിദ്ധാന്തത്തിന്റെ തെളിവ്", "hard"),
    ("ഡാർക്ക് മാറ്റർ", "ദൃശ്യമാകാത്ത പിണ്ഡം", "hard"),
]

CONSTELLATIONS = [
    "ഓറിയോൺ", "വൃശ്ചികം", "സിംഹം", "കുംഭം", "മകരം", "മേടം", "ഇടവം", "മിഥുനം",
    "കർക്കടകം", "കന്നി", "തുലാം", "വൃശ്ചികം", "ധനു", "മീനം", "അശ്വതി", "ഭരണി",
    "കാർത്തിക", "രോഹിണി", "മൃഗശീർഷം", "ആർദ്ര", "പുണർതം", "പൂരം", "ഉത്രം", "അത്തം",
    "ചിത്തിര", "ചോതി", "വിശാഖം", "അനിഴം", "തൃക്കേട്ട", "മൂലം", "പൂരാടം", "ഉത്രാടം",
    "തിരുവോണം", "അവിട്ടം", "ചതയം", "പൂരുരുട്ടാതി", "ഉത്രട്ടാതി", "രേവതി",
]

ZODIAC = ["മേടം", "ഇടവം", "മിഥുനം", "കർക്കടകം", "സിംഹം", "കന്നി", "തുലാം", "വൃശ്ചികം", "ധനു", "മകരം", "കുംഭം", "മീനം"]

ISRO_CENTERS = [
    ("വിക്രം സാരാഭായി ബഹിരാകാശ കേന്ദ്രം", "തിരുവനന്തപുരം"),
    ("സതീഷ് ധവാൻ സ്പേസ് സെന്റർ", "ശ്രീഹരികോട്ട"),
    ("ഉറുവാക്കം റോക്കറ്റ് കേന്ദ്രം", "തിരുവനന്തപുരം"),
    ("ലിഖിത് ഗിരി ട്രാക്കിംഗ് സെന്റർ", "ബംഗളൂരു"),
    ("നോർത്ത് ഇസ്റ്റ് സ്പേസ് സെന്റർ", "ഷില്ലോം"),
]

ROCKETS = [
    ("പി.എസ്.എൽ.വി.", "പോളാർ സാറലൈറ്റ് ലോഞ്ച് വെഹിക്കിൾ"),
    ("ജി.എസ്.എൽ.വി.", "ജിയോസിങ്ക്രണസ് സാറലൈറ്റ് ലോഞ്ച് വെഹിക്കിൾ"),
    ("എൽ.വി.എം.", "ലൈറ്റ് വെഹിക്കിൾ മാർക്ക്"),
    ("എൽ.വി.എം.3", "മാർക്ക്-3 ലോഞ്ച് വെഹിക്കിൾ"),
    ("എസ്.എസ്.എൽ.വി.", "സ്മോൾ സാറലൈറ്റ് ലോഞ്ച് വെഹിക്കിൾ"),
]

TELESCOPES = [
    ("ഹബിൾ സ്പേസ് ടെലിസ്കോപ്പ്", "നാസ", "1990"),
    ("ജയിംസ് വെബ് ബഹിരാകാശ ദൂരദർശിനി", "നാസ/ഇ.എസ്.എ", "2021"),
    ("ചന്ദ്ര എക്സ്-റേ ടെലിസ്കോപ്പ്", "ഇസ്റോ", "2015"),
    ("ആസ്ട്രോസാറ്റ്", "ഇസ്റോ", "2015"),
    ("കെപ്ലർ സ്പേസ് ടെലിസ്കോപ്പ്", "നാസ", "2009"),
    ("സ്പിറ്റ്സർ സ്പേസ് ടെലിസ്കോപ്പ്", "നാസ", "2003"),
    ("ഫെർമി ഗാമാ-റേ ടെലിസ്കോപ്പ്", "നാസ", "2008"),
    ("ചന്ദ്രാ എക്സ്-റേ ഓബ്സർവেটറി", "നാസ", "1999"),
]

DWARF_PLANETS = [
    ("പ്ലൂട്ടോ", "കൈപ്പർ ബെൽറ്റ്"),
    ("സെറസ്", "ക്ഷുദ്രഗ്രഹ വലയം"),
    ("എറിസ്", "സ്കാറ്റേഡ് ബെൽറ്റ്"),
    ("ഹുമിയ", "ക്ഷുദ്രഗ്രഹ വലയം"),
    ("മക്കെമക്കെ", "ക്ഷുദ്രഗ്രഹ വലയം"),
]

COMETS = [
    ("ഹാലിയുടെ വാൽനക്ഷത്രം", "76 വർഷം"),
    ("ഹെയ്ല്-ബോപ്പ്", "1997"),
    ("ഹെയ്ലി-ബോപ്പ്", "1997"),
    ("ടെംപൽ-ടട്ടിൽ", "2005 ദൗത്യം"),
]

ASTEROID_BELT = ["സെറസ്", "വെസ്റ്റ", "പല്ലാസ്", "ഹൈജിയ", "ഇറോസ്"]

MESSIER = [(i, f"M{i}") for i in range(1, 111)]

def generate_planet_questions(questions, existing, num):
    planet_names = [p[0] for p in PLANETS]
    en_names = [p[1] for p in PLANETS]
    for ml, en, dist, diam, moons, day, year, diff in PLANETS:
        templates = [
            (f"'{ml}' എന്ന ഗ്രഹത്തിന്റെ ആർത്ഥനാമം ഏതാണ്?", en_names, en, diff),
            (f"'{en}' എന്ന ഗ്രഹത്തിന്റെ മലയാള പേര്?", planet_names, ml, diff),
            (f"{ml} സൂര്യനോടുള്ള ആകर्षണദൂരം (ഏകദേശം) ഏതാണ്?", [p[2] for p in PLANETS], dist, diff),
            (f"{ml}യുടെ വ്യാസാർധം (ഏകദേശം) എത്ര?", [p[3] for p in PLANETS], diam, "medium"),
            (f"{ml}യ്ക്ക് എത്ര സ്വാഭാവിക ഉപഗ്രഹങ്ങളുണ്ട്?", [p[4] for p in PLANETS], moons, "medium"),
            (f"{ml} സ്വന്തം അച്ചുതണ്ടിൽ കറങ്ങാൻ (ഭ്രമണം) എടുക്കുന്ന സമയം?", [p[5] for p in PLANETS], day, "hard"),
            (f"{ml} സൂര്യനെ വലംവെക്കാൻ (പരിക്രമണം) എടുക്കുന്ന സമയം?", [p[6] for p in PLANETS], year, "hard"),
        ]
        for q, pool, ans, d in templates:
            opts = [ans] + pick_distractors(pool, ans)
            num = add_q(questions, existing, num, q, opts, ans, d)
    return num


def generate_moon_questions(questions, existing, num):
    moon_names = [m[0] for m in MOONS]
    planet_names = [p[0] for p in PLANETS]
    for moon, planet in MOONS:
        q1 = f"'{moon}' ഏത് ഗ്രഹത്തിന്റെ ഉപഗ്രഹമാണ്?"
        opts1 = [planet] + pick_distractors(planet_names, planet)
        num = add_q(questions, existing, num, q1, opts1, planet, "medium")
        q2 = f"{planet}യുടെ ഉപഗ്രഹം '{moon}' ഏതാണ്?"
        other_moons = [m[0] for m in MOONS if m[1] == planet and m[0] != moon]
        if len(other_moons) >= 1:
            pool = other_moons + [m[0] for m in MOONS if m[1] != planet]
            opts2 = [moon] + pick_distractors(pool[:8], moon)
            num = add_q(questions, existing, num, q2, opts2, moon, "hard")
    return num


def generate_star_questions(questions, existing, num):
    star_names = [s[0] for s in STARS]
    for star, const, fact, diff in STARS:
        q1 = f"'{star}' ഏത് നക്ഷത്രസമൂഹത്തിലാണ്?"
        const_pool = [s[1] for s in STARS] + CONSTELLATIONS
        opts1 = [const] + pick_distractors(const_pool, const)
        num = add_q(questions, existing, num, q1, opts1, const, diff)
        q2 = f"'{star}'യെക്കുറിച്ചുള്ള ശരിയായ വിവരം ഏതാണ്?"
        facts = [s[2] for s in STARS]
        opts2 = [fact] + pick_distractors(facts, fact)
        num = add_q(questions, existing, num, q2, opts2, fact, diff)
    return num


def generate_mission_questions(questions, existing, num):
    orgs = list({m[1] for m in MISSIONS})
    years = [m[2] for m in MISSIONS if m[2] != "—"]
    targets = list({m[3] for m in MISSIONS})
    for name, org, year, target, diff in MISSIONS:
        q1 = f"ബഹിരാകാശ ദൗത്യം '{name}' നടപ്പാക്കിയ സംഘടന ഏത്?"
        opts1 = [org] + pick_distractors(orgs, org)
        num = add_q(questions, existing, num, q1, opts1, org, diff)
        if year != "—":
            q2 = f"ദൗത്യം '{name}' വിക്ഷേപിച്ച വർഷം ഏത്?"
            opts2 = [year] + pick_distractors(years, year)
            num = add_q(questions, existing, num, q2, opts2, year, diff)
        q3 = f"ദൗത്യം '{name}'-ന്റെ പ്രധാന ലക്ഷ്യം/ലക്ഷ്യഗ്രഹം ഏത്?"
        opts3 = [target] + pick_distractors(targets, target)
        num = add_q(questions, existing, num, q3, opts3, target, diff)
    return num


def generate_astronomer_questions(questions, existing, num):
    names = [a[0] for a in ASTRONOMERS]
    works = [a[1] for a in ASTRONOMERS]
    for name, work, diff in ASTRONOMERS:
        q1 = f"{name} ഏതുമായി പ്രധാനമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"
        opts1 = [work] + pick_distractors(works, work)
        num = add_q(questions, existing, num, q1, opts1, work, diff)
        q2 = f"'{work}' ആവിഷ്കരിച്ച/കണ്ടെത്തിയ ശാസ്ത്രജ്ഞൻ ആരാണ്?"
        opts2 = [name] + pick_distractors(names, name)
        num = add_q(questions, existing, num, q2, opts2, name, diff)
    return num


def generate_concept_questions(questions, existing, num):
    terms = [c[0] for c in CONCEPTS]
    defs = [c[1] for c in CONCEPTS]
    for term, defn, diff in CONCEPTS:
        q1 = f"ജ്യോതിശാസ്ത്രത്തിൽ '{term}' എന്തിനെ സൂചിപ്പിക്കുന്നു?"
        opts1 = [defn] + pick_distractors(defs, defn)
        num = add_q(questions, existing, num, q1, opts1, defn, diff)
        q2 = f"'{defn}' എന്ന വിവരണം ഏത് പദവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"
        opts2 = [term] + pick_distractors(terms, term)
        num = add_q(questions, existing, num, q2, opts2, term, diff)
    return num


def generate_isro_questions(questions, existing, num):
    centers = [c[0] for c in ISRO_CENTERS]
    places = [c[1] for c in ISRO_CENTERS]
    for center, place in ISRO_CENTERS:
        q = f"{center} എവിടെയാണ് സ്ഥിതി ചെയ്യുന്നത്?"
        opts = [place] + pick_distractors(places, place)
        num = add_q(questions, existing, num, q, opts, place, "medium")
    rocket_names = [r[0] for r in ROCKETS]
    rocket_full = [r[1] for r in ROCKETS]
    for short, full in ROCKETS:
        q1 = f"ഇസ്റോയുടെ '{short}' എന്നതിന്റെ പൂർണ്ണരൂപം ഏതാണ്?"
        opts1 = [full] + pick_distractors(rocket_full, full)
        num = add_q(questions, existing, num, q1, opts1, full, "hard")
        q2 = f"'{full}' എന്നത് ഏത് റോക്കറ്റിന്റെ ചുരുക്കപ്പേരാണ്?"
        opts2 = [short] + pick_distractors(rocket_names, short)
        num = add_q(questions, existing, num, q2, opts2, short, "hard")
    return num


def generate_telescope_questions(questions, existing, num):
    names = [t[0] for t in TELESCOPES]
    agencies = list({t[1] for t in TELESCOPES})
    years = [t[2] for t in TELESCOPES]
    for name, agency, year in TELESCOPES:
        q1 = f"'{name}' വിക്ഷേപിച്ച സംഘടന ഏത്?"
        opts1 = [agency] + pick_distractors(agencies, agency)
        num = add_q(questions, existing, num, q1, opts1, agency, "medium")
        q2 = f"'{name}' വിക്ഷേപിച്ച വർഷം ഏത്?"
        opts2 = [year] + pick_distractors(years, year)
        num = add_q(questions, existing, num, q2, opts2, year, "medium")
    return num


def generate_dwarf_planet_questions(questions, existing, num):
    names = [d[0] for d in DWARF_PLANETS]
    belts = [d[1] for d in DWARF_PLANETS]
    for name, belt in DWARF_PLANETS:
        q = f"വാമനഗ്രഹം '{name}' ഏത് പ്രദേശത്താണ് സ്ഥിതി ചെയ്യുന്നത്?"
        opts = [belt] + pick_distractors(belts, belt)
        num = add_q(questions, existing, num, q, opts, belt, "hard")
    return num


def generate_bulk_facts(questions, existing, num):
    """Generate large volume from structured fact banks."""
    planet_names = [p[0] for p in PLANETS]
    facts = [
        ("സൗരയൂഥത്തിലെ ഏറ്റവും വലിയ ഗ്രഹം", "വ്യാഴം", planet_names, "easy"),
        ("സൗരയൂഥത്തിലെ ഏറ്റവും ചെറിയ ഗ്രഹം", "ബുധൻ", planet_names, "easy"),
        ("സൂര്യനോട് ഏറ്റവും അടുത്തുള്ള ഗ്രഹം", "ബുധൻ", planet_names, "easy"),
        ("സൂര്യനോട് ഏറ്റവും അകലെയുള്ള ഗ്രഹം", "നെപ്റ്റ്യൂൺ", planet_names, "easy"),
        ("'ചുവന്ന ഗ്രഹം' എന്നറിയപ്പെടുന്ന ഗ്രഹം", "ചൊവ്വ", planet_names, "easy"),
        ("'ഇരട്ട ഗ്രഹം' എന്നറിയപ്പെടുന്ന ഗ്രഹം", "ശുക്രൻ", planet_names, "medium"),
        ("ഏറ്റവും കൂടുതൽ ഉപഗ്രഹങ്ങളുള്ള ഗ്രഹം", "ശനി", planet_names, "medium"),
        ("സൗരയൂഥത്തിലെ ഏറ്റവും വലിയ ഉപഗ്രഹം", "ഗാനിമീഡ്", [m[0] for m in MOONS], "medium"),
        ("ഉപഗ്രഹങ്ങളില്ലാത്ത ഗ്രഹങ്ങൾ", "ബുധനും ശുക്രനും", ["ബുധനും ശുക്രനും", "ചൊവ്വയും ഭൂമിയും", "വ്യാഴവും ശനിയും", "യുറാനസും നെപ്റ്റ്യൂണും"], "medium"),
        ("കിഴക്കുനിന്ന് പടിഞ്ഞാറോട്ട് ഭ്രമണം ചെയ്യുന്ന ഗ്രഹം", "ശുക്രൻ", planet_names, "hard"),
        ("സൗരയൂഥത്തിലെ ഏറ്റവും ചൂടുകൂടിയ ഗ്രഹം", "ശുക്രൻ", planet_names, "medium"),
        ("സൗരയൂഥത്തിലെ ഏറ്റവും തണുപ്പേറിയ ഗ്രഹം", "നെപ്റ്റ്യൂൺ", planet_names, "medium"),
        ("ഒളിമ്പസ് മോൺസ് പർവ്വതം ഏത് ഗ്രഹത്തിലാണ്?", "ചൊവ്വ", planet_names, "medium"),
        ("വ്യാഴത്തിലെ ഗ്രേറ്റ് റെഡ് സ്പോട്ട്", "കൊടുങ്കാറ്റ്", ["കൊടുങ്കാറ്റ്", "അഗ്നിപർവതം", "കടൽ", "ഉപഗ്രഹം"], "medium"),
        ("ശനിയുടെ വലയങ്ങൾ പ്രധാനമായും നിർമ്മിച്ചത്", "ഐസ്-പാറ്റിക്കിളുകൾ", ["ഐസ്-പാറ്റിക്കിളുകൾ", "പാറ", "ലോഹം", "വാതകം മാത്രം"], "hard"),
    ]
    for qstem, ans, pool, diff in facts:
        if isinstance(pool, list) and ans in pool:
            opts = [ans] + pick_distractors(pool, ans)
        else:
            opts = pool if len(pool) == 4 else [ans] + pick_distractors(pool, ans)
        num = add_q(questions, existing, num, qstem + " ഏതാണ്?", opts, ans, diff)

    # Numerical / unit facts
    nums = [
        ("പ്രകാശവർഷം", "പ്രകാശം ഒരു വർഷത്തിൽ സഞ്ചരിക്കുന്ന ദൂരം", ["ഒരു വർഷം", "ഒരു മാസം", "ഒരു ദിവസം", "ഒരു നിമിഷം"], "easy"),
        ("ഒരു പ്രകാശവർഷം ഏകദേശം", "9.46 ട്രില്യൺ കിലോമീറ്റർ", ["9.46 ട്രില്യൺ കി.മീ.", "1 മില്യൺ കി.മീ.", "150 മില്യൺ കി.മീ.", "384400 കി.മീ."], "hard"),
        ("ഭൂമി-ചന്ദ്രൻ ദൂരം (ഏകദേശം)", "384400 കിലോമീറ്റർ", ["384400 കി.മീ.", "1 മില്യൺ കി.മീ.", "150 മില്യൺ കി.മീ.", "1 AU"], "medium"),
        ("സൂര്യപ്രകാശം ഭൂമിയിലെത്താൻ", "8 മിനിറ്റ് 20 സെക്കൻഡ്", ["8 മിനിറ്റ് 20 സെക്കൻഡ്", "1 സെക്കൻഡ്", "1 മണിക്കൂർ", "1 ദിവസം"], "medium"),
        ("ഹാലിയുടെ വാൽനക്ഷത്രം പ്രത്യക്ഷപ്പെടുന്ന ഇടവേള", "76 വർഷം", ["76 വർഷം", "50 വർഷം", "100 വർഷം", "200 വർഷം"], "medium"),
        ("പ്ലൂട്ടോയെ ഗ്രഹങ്ങളിൽ നിന്ന് ഒഴിവാക്കിയ വർഷം", "2006", ["2006", "2000", "2010", "1990"], "medium"),
        ("സ്പുട്നിക് 1 വിക്ഷേപണ വർഷം", "1957", ["1957", "1969", "1945", "1975"], "easy"),
        ("ആര്യഭട്ട വിക്ഷേപണ വർഷം", "1975", ["1975", "1957", "2008", "2013"], "easy"),
        ("ഇസ്റോ സ്ഥാപിതമായ വർഷം", "1969", ["1969", "1975", "1957", "2008"], "medium"),
        ("ചന്ദ്രയാൻ-3 സോഫ്റ്റ് ലാൻഡിങ് വർഷം", "2023", ["2023", "2019", "2008", "2014"], "easy"),
        ("മംഗള്യാൻ വിക്ഷേപണ വർഷം", "2013", ["2013", "2023", "2008", "2019"], "medium"),
        ("ആദിത്യ-എൽ1 വിക്ഷേപണ വർഷം", "2023", ["2023", "2013", "2008", "2019"], "medium"),
        ("ജയിംസ് വെബ് വിക്ഷേപണ വർഷം", "2021", ["2021", "1990", "2009", "2015"], "medium"),
        ("ഹബിൾ ടെലിസ്കോപ്പ് വിക്ഷേപണ വർഷം", "1990", ["1990", "2021", "2003", "2009"], "medium"),
        ("യൂറി ഗഗാരിൻ ബഹിരാകാശ യാത്ര", "1961", ["1961", "1957", "1969", "1975"], "easy"),
        ("നീൽ ആംസ്ട്രോങ് ചന്ദ്രനിൽ ഇറങ്ങിയ വർഷം", "1969", ["1969", "1961", "1975", "2008"], "easy"),
        ("ശൂന്യതയിൽ പ്രകാശ വേഗത", "299792 കി.മീ./സെക്കൻഡ്", ["299792 കി.മീ./സെക്കൻഡ്", "150000 കി.മീ./സെക്കൻഡ്", "1000 കി.മീ./സെക്കൻഡ്", "340 മീ./സെക്കൻഡ്"], "hard"),
        ("സൂര്യന്റെ ഉപരിതല താപനില (ഏകദേശം)", "5500 ഡിഗ്രി സെൽഷ്യസ്", ["5500 °C", "1000 °C", "100 °C", "10000 °C"], "hard"),
        ("സൗരയൂഥ പിണ്ഡത്തിന്റെ എത്ര ശതമാനം സൂര്യനിലാണ്?", "99.8%", ["99.8%", "50%", "75%", "90%"], "hard"),
        ("ഭൂമിയുടെ ഭ്രമണകാലം (സിഡീറിയൽ)", "23 മണിക്കൂർ 56 മിനിറ്റ് 4 സെക്കൻഡ്", ["23 മണിക്കൂർ 56 മിനിറ്റ് 4 സെക്കൻഡ്", "24 മണിക്കൂർ", "23 മണിക്കൂർ", "25 മണിക്കൂർ"], "hard"),
    ]
    for qstem, ans, opts, diff in nums:
        num = add_q(questions, existing, num, qstem + "?", opts if ans in opts else [ans] + opts[:3], ans, diff)

    return num


def generate_nakshatra_questions(questions, existing, num):
    nakshatras = [
        ("അശ്വതി", 1), ("ഭരണി", 2), ("കാർത്തിക", 3), ("രോഹിണി", 4),
        ("മൃഗശീർഷം", 5), ("ആർദ്ര", 6), ("പുണർതം", 7), ("പൂരം", 8),
        ("ഉത്രം", 9), ("അത്തം", 10), ("ചിത്തിര", 11), ("ചോതി", 12),
        ("വിശാഖം", 13), ("അനിഴം", 14), ("തൃക്കേട്ട", 15), ("മൂലം", 16),
        ("പൂരാടം", 17), ("ഉത്രാടം", 18), ("തിരുവോണം", 19), ("അവിട്ടം", 20),
        ("ചതയം", 21), ("പൂരുരുട്ടാതി", 22), ("ഉത്രട്ടാതി", 23), ("രേവതി", 24),
        ("അഭിജിത്ത്", 28), ("ശ്രവണം", 22), ("ധനിഷ്ഠ", 23), ("ശതഭിഷം", 24),
    ]
    names = [n[0] for n in nakshatras]
    for name, pos in nakshatras:
        q = f"ഭാരതീയ ജ്യോതിശാസ്ത്രത്തിൽ '{name}' ഏത് നക്ഷത്രമണ്ഡലത്തിലാണ്?"
        opts = [name] + pick_distractors(names, name)
        num = add_q(questions, existing, num, q, opts, name, "hard")
    for i, z in enumerate(ZODIAC, 1):
        q = f"രാശിചക്രത്തിലെ {i}-ാം രാശി ഏതാണ്?"
        opts = [z] + pick_distractors(ZODIAC, z)
        num = add_q(questions, existing, num, q, opts, z, "medium")
    return num


def generate_messier_questions(questions, existing, num):
    famous = {
        1: "ക്രാബ് നെബുല",
        31: "ആൻഡ്രോമീഡ ഗാലക്സി",
        42: "ഓറിയോൺ നെബുല",
        45: "പ്ലെയേഡസ് (കാർത്തിക താരസമൂഹം)",
        57: "റിംഗ് നെബുല",
        81: "ബോഡ് ഗാലക്സി",
        82: "സിഗാർ ഗാലക്സി",
        87: "വിർഗോ എ ഗാലക്സി",
        104: "സോംബ്രേരോ ഗാലക്സി",
    }
    for mid, name in famous.items():
        q1 = f"മെസ്സിയർ വസ്തു M{mid} ഏതാണ്?"
        others = list(famous.values())
        opts1 = [name] + pick_distractors(others, name)
        num = add_q(questions, existing, num, q1, opts1, name, "hard")
    for mid in range(1, 111):
        q = f"മെസ്സിയർ കാറ്റലോഗിൽ M{mid} എന്ന നമ്പർ ഉപയോഗിക്കുന്ന വസ്തു ഏതാണ്?"
        ans = famous.get(mid, f"മെസ്സിയർ വസ്തു M{mid}")
        nearby = [famous.get(mid-1, f"M{mid-1}"), famous.get(mid+1, f"M{mid+1}"),
                  famous.get(mid-2, f"M{mid-2}"), famous.get(mid+2, f"M{mid+2}")]
        opts = [ans] + pick_distractors(nearby + [f"M{mid}"], ans)[:3]
        if len(set(opts)) == 4:
            num = add_q(questions, existing, num, q, opts, ans, "hard")
    return num


def generate_comparison_questions(questions, existing, num):
    comparisons = [
        ("വ്യാഴവും ശനിയും താരതമ്യം ചെയ്യുമ്പോൾ വലുത്", "വ്യാഴം", ["വ്യാഴം", "ശനി", "ഭൂമി", "ചൊവ്വ"]),
        ("ഭൂമിയും ചന്ദ്രനും താരതമ്യം ചെയ്യുമ്പോൾ വലുത്", "ഭൂമി", ["ഭൂമി", "ചന്ദ്രൻ", "ബുധൻ", "ഫോബോസ്"]),
        ("സിറിയസും ധ്രുവനക്ഷത്രവും താരതമ്യം ചെയ്യുമ്പോൾ തിളക്കമുള്ളത്", "സിറിയസ്", ["സിറിയസ്", "ധ്രുവനക്ഷത്രം", "പ്രോക്സിമ സെന്റോറി", "ബെറ്റൽജൂസ്"]),
        ("ആകാശഗംഗയും ആൻഡ്രോമീഡയും താരതമ്യം ചെയ്യുമ്പോൾ വലുത്", "ആകാശഗംഗ", ["ആകാശഗംഗ", "ആൻഡ്രോമീഡ", "മാഗല്ലാനിക്", "ട്രയാംഗുലം"]),
        ("പ്ലൂട്ടോയും സെറസും താരതമ്യം ചെയ്യുമ്പോൾ വലുത്", "സെറസ്", ["സെറസ്", "പ്ലൂട്ടോ", "വെസ്റ്റ", "എറിസ്"]),
        ("ഹബിളും ജയിംസ് വെബും താരതമ്യം ചെയ്യുമ്പോൾ പുതിയത്", "ജയിംസ് വെബ്", ["ജയിംസ് വെബ്", "ഹബിൾ", "കെപ്ലർ", "സ്പിറ്റ്സർ"]),
        ("ചന്ദ്രയാൻ-1, ചന്ദ്രയാൻ-2, ചന്ദ്രയാൻ-3 എന്നിവയിൽ ഏറ്റവും പുതിയത്", "ചന്ദ്രയാൻ-3", ["ചന്ദ്രയാൻ-3", "ചന്ദ്രയാൻ-2", "ചന്ദ്രയാൻ-1", "മംഗള്യാൻ"]),
        ("ബുധനും ശുക്രനും താരതമ്യം ചെയ്യുമ്പോൾ സൂര്യനോട് അടുത്തത്", "ബുധൻ", ["ബുധൻ", "ശുക്രൻ", "ഭൂമി", "ചൊവ്വ"]),
        ("യുറാനസും നെപ്റ്റ്യൂണും താരതമ്യം ചെയ്യുമ്പോൾ സൂര്യനോട് അകലെ", "നെപ്റ്റ്യൂൺ", ["നെപ്റ്റ്യൂൺ", "യുറാനസ്", "ശനി", "വ്യാഴം"]),
        ("ടൈറ്റനും ഗാനിമീഡും താരതമ്യം ചെയ്യുമ്പോൾ വലുത്", "ഗാനിമീഡ്", ["ഗാനിമീഡ്", "ടൈറ്റൻ", "ചന്ദ്രൻ", "യൂറോപ്പ"]),
    ]
    for stem, ans, opts in comparisons:
        num = add_q(questions, existing, num, stem + " ഏതാണ്?", opts, ans, "medium")
    return num


def generate_phenomena_questions(questions, existing, num):
    phen = [
        ("സൂര്യനും ഭൂമിക്കും ഇടയിൽ ചന്ദ്രൻ വരുമ്പോൾ", "സൂര്യഗ്രഹണം", ["സൂര്യഗ്രഹണം", "ചന്ദ്രഗ്രഹണം", "ഉൽക്കവൃഷ്ടി", "ധൂമകേതു"]),
        ("സൂര്യനും ചന്ദ്രനും ഇടയിൽ ഭൂമി വരുമ്പോൾ", "ചന്ദ്രഗ്രഹണം", ["ചന്ദ്രഗ്രഹണം", "സൂര്യഗ്രഹണം", "സൂര്യോദയം", "സൂര്യാസ്തമയം"]),
        ("സൂര്യഗ്രഹണം സാധാരണയായി സംഭവിക്കുന്നത്", "അമാവാസി", ["അമാവാസി", "പൗർണമി", "അഷ്ടമി", "തൃയോദശി"]),
        ("ചന്ദ്രഗ്രഹണം സാധാരണയായി സംഭവിക്കുന്നത്", "പൗർണമി", ["പൗർണമി", "അമാവാസി", "ചതുർദശി", "ദ്വാദശി"]),
        ("ഭൂമിയുടെ ഉപരിതലത്തിൽ ഉൽക്കകൾ കരിഞ്ഞുപോകുന്ന പ്രതിഭാസം", "ഉൽക്കവൃഷ്ടി", ["ഉൽക്കവൃഷ്ടി", "സൂര്യഗ്രഹണം", "ചന്ദ്രഗ്രഹണം", "ഭൂകമ്പം"]),
        ("ഭൂമിയുടെ ഭ്രമണം കാരണം ഉണ്ടാകുന്നത്", "രാത്രിയും പകലും", ["രാത്രിയും പകലും", "ഋതുക്കൾ", "ജ്വാലാമുഖി", "കടൽ അല"]),
        ("ഭൂമിയുടെ പരിക്രമണവും അച്ചുതണ്ടിന്റെ ചരിവും കാരണം", "ഋതുക്കൾ", ["ഋതുക്കൾ", "രാത്രിയും പകലും", "ജ്വാലാമുഖി", "സുനാമി"]),
        ("ചന്ദ്രന്റെ വിവിധ ഘട്ടങ്ങൾ", "ചന്ദ്രകല", ["ചന്ദ്രകല", "സൂര്യകല", "നക്ഷത്രകല", "ഗ്രഹകല"]),
        ("ഉത്തരധ്രുവത്തിൽ കാണുന്ന പ്രകാശ പ്രതിഭാസം", "ഓറോറ", ["ഓറോറ", "മെറ്റിയോർ", "കൊമറ്റ്", "നെബുല"]),
        ("സൂര്യന്റെ പൊടിപ്പുറ്റുകൾ പുറത്തുവിടുന്നത്", "സോളാർ വിൻഡ്", ["സോളാർ വിൻഡ്", "സൂര്യഗ്രഹണം", "ചന്ദ്രോദയം", "ഉൽക്ക"]),
        ("സൂര്യന്റെ സ্ফോടനാത്മക പ്രദേശം", "സോളാർ ഫ്ലെയർ", ["സോളാർ ഫ്ലെയർ", "ബ്ലാക്ക് ഹോൾ", "നെബുല", "ക്വാസാർ"]),
        ("ഭൂമിയുടെ അന്തരീക്ഷത്തിൽ ഏറ്റവും കൂടുതലുള്ള വാതകം", "നൈട്രജൻ", ["നൈട്രജൻ", "ഓക്സിജൻ", "കാർബൺ ഡൈഓക്സൈഡ്", "ഹൈഡ്രജൻ"]),
        ("ഭൂമിയുടെ അന്തരീക്ഷത്തിൽ ജീവന് അത്യാവശ്യ വാതകം", "ഓക്സിജൻ", ["ഓക്സിജൻ", "നൈട്രജൻ", "ഹീലിയം", "ആർഗൺ"]),
        ("സൂര്യനിൽ ഏറ്റവും കൂടുതലുള്ള വാതകം", "ഹൈഡ്രജൻ", ["ഹൈഡ്രജൻ", "ഹീലിയം", "ഓക്സിജൻ", "നൈട്രജൻ"]),
        ("നക്ഷത്രങ്ങൾ തിളങ്ങാൻ കാരണം", "ന്യൂക്ലിയർ സംയോജനം", ["ന്യൂക്ലിയർ സംയോജനം", "ഗുരുത്വാകർഷണം", "കാന്തികക്ഷേത്രം", "സോളാർ വിൻഡ്"]),
        ("ഗാലക്സിയിലെ നക്ഷത്രങ്ങളെ ഒന്നിച്ച് നിർത്തുന്ന ശക്തി", "ഗുരുത്വാകർഷണ ബലം", ["ഗുരുത്വാകർഷണ ബലം", "കാന്തികശക്തി", "അഭികേന്ദ്രബലം", "ന്യൂക്ലിയർ ശക്തി"]),
        ("പ്രപഞ്ചത്തിന്റെ ഉത്ഭവ സിദ്ധാന്തം", "മഹാവിസ്ഫോടന സിദ്ധാന്തം", ["മഹാവിസ്ഫോടന സിദ്ധാന്തം", "സ്ഥിരസ്ഥിതി സിദ്ധാന്തം", "സ്ട്രിങ് തിയറി", "പൾസേറ്റിങ് തിയറി"]),
        ("ചൊവ്വയും വ്യാഴത്തിനും ഇടയിലെ ക്ഷുദ്രഗ്രഹ വലയം", "ആസ്റ്ററോയിഡ് ബെൽറ്റ്", ["ആസ്റ്ററോയിഡ് ബെൽറ്റ്", "കൈപ്പർ ബെൽറ്റ്", "ഓർട്ട് മേഘം", "അസ്റ്ററോയിഡ് ബെൽറ്റ്"]),
        ("പ്ലൂട്ടോ സ്ഥിതി ചെയ്യുന്ന പ്രദേശം", "കൈപ്പർ ബെൽറ്റ്", ["കൈപ്പർ ബെൽറ്റ്", "ആസ്റ്ററോയിഡ് ബെൽറ്റ്", "ഓർട്ട് മേഘം", "അന്തർനക്ഷത്ര മേഖല"]),
        ("ഭൂമിയിൽ നഗ്നനേത്രങ്ങൾ കൊണ്ട് കാണാൻ കഴിയുന്ന ഏറ്റവും ദൂരെയുള്ള ഗാലക്സി", "ആൻഡ്രോമീഡ", ["ആൻഡ്രോമീഡ", "ട്രയാംഗുലം", "മാഗല്ലാനിക്", "ഓറിയോൺ"]),
    ]
    for cond, ans, opts in phen:
        num = add_q(questions, existing, num, cond + " ഏതാണ്?", opts, ans, "medium")
    return num


def generate_space_people_questions(questions, existing, num):
    people = [
        ("യൂറി ഗഗാരിൻ", "ബഹിരാകാശത്ത് എത്തിയ ആദ്യ മനുഷ്യൻ", "easy"),
        ("നീൽ ആംസ്ട്രോങ്", "ചന്ദ്രനിൽ കാലുകുത്തിയ ആദ്യ മനുഷ്യൻ", "easy"),
        ("ബസ്സ് ആൽഡ്രിൻ", "അപ്പോളോ 11-ൽ ചന്ദ്രനിൽ ഇറങ്ങിയ രണ്ടാമത്തെ വ്യക്തി", "medium"),
        ("വാലന്റീന ടെരഷ്കോവ", "ബഹിരാകാശത്ത് എത്തിയ ആദ്യ വനിത", "medium"),
        ("രാകേഷ് ശർമ്മ", "ബഹിരാകാശത്ത് എത്തിയ ആദ്യ ഇന്ത്യൻ വംശജൻ", "easy"),
        ("കൽപ്പന ചൗള", "ബഹിരാകാശത്ത് എത്തിയ ആദ്യ ഇന്ത്യൻ വംശജ വനിത", "easy"),
        ("സ്വാതന്ത്ര്യ മേഘ", "ഇന്ത്യയുടെ ആദ്യ വനിതാ ബഹിരാകാശ യാത്രിക", "hard"),
        ("സുരേഷ് കുമാർ", "ഇന്ത്യയുടെ ആദ്യ ബഹിരാകാശ യാത്രികൻ", "hard"),
        ("ലൈക്ക", "ബഹിരാകാശത്ത് എത്തിയ ആദ്യ ജീവി (നായ)", "medium"),
        ("അലാൻ ഷെപ്പർ্ড്", "ചന്ദ്രനിൽ ഗോൾഫ് കളിച്ച ആദ്യ വ്യക്തി", "hard"),
    ]
    facts = [p[1] for p in people]
    names = [p[0] for p in people]
    for name, fact, diff in people:
        q1 = f"{name} ഏതുമായി പ്രശസ്തനാണ്/പ്രശസ്തയാണ്?"
        opts1 = [fact] + pick_distractors(facts, fact)
        num = add_q(questions, existing, num, q1, opts1, fact, diff)
        q2 = f"'{fact}' ആരാണ്?"
        opts2 = [name] + pick_distractors(names, name)
        num = add_q(questions, existing, num, q2, opts2, name, diff)
    return num


def generate_extended_catalog(questions, existing, num):
    """Large catalog of additional astronomy facts for volume."""
    catalog = []
    # Bright stars extended
    bright_stars = [
        ("ആക്രിബ്", "വൃശ്ചികം"), ("അൽഡെബരൻ", "വൃഷഭം"), ("ആന്റാരസ്", "വൃശ്ചികം"),
        ("സ്പൈക്ക", "സിംഹം"), ("ഡെനെബ്", "ഹംസം"), ("ഫോമാൽഹോട്ട്", "മത്സ്യം"),
        ("ആൽഗോൾ", "മേടം"), ("മിറാക്", "ഭാരതീ"), ("ആൽകൈദ്", "കരഭം"),
        ("പൊളക്സ്", "മിഥുനം"), ("കാസ്റ്റർ", "മിഥുനം"), ("പ്രോസിയോൺ", "ചെറു നായ"),
        ("ആൽഫാർദ്", "ഹൈഡ്ര"), ("മിറാക്", "ഭാരതീ"), ("ഷെഡാർ", "കസ്സിയോപിയ"),
        ("കാപ്പ", "കാസ്സിയോപിയ"), ("ആൽനാത്", "കുതിര"), ("മാർക്കബ്", "കുതിര"),
        ("ആൽഫീൽ", "കുതിര"), ("എൽനാത്", "കുതിര"), ("മിഴം", "കന്നി"),
        ("സാഡൽമെലിക്", "കുംഭം"), ("സാഡൽസൂദ്", "കുംഭം"), ("ആൽനൈർം", "ഗ്രൂസ്"),
        ("ആൽഫാ സെന്റോറി ബി", "സെന്റോറസ്"), ("ബെറ്റാ സെന്റോറി", "സെന്റോറസ്"),
        ("റിഗിൽ കെന്റോറസ്", "സെന്റോറസ്"), ("ഹദാർ", "സെന്റോറസ്"),
        ("മിമോസ", "കുരുവം"), ("അലിയോത്ത്", "കരഭം"), ("മെക്സ്", "കരഭം"),
        ("ഫെക്ഡ", "കരഭം"), ("ആൽഗിയോറ", "കരഭം"), ("ആൽകോർ", "കരഭം"),
        ("സൂത്ര", "ഓറിയോൺ"), ("ബെല്ലാട്രിക്സ്", "ഓറിയോൺ"), ("മിന്റാക്ക", "ഓറിയോൺ"),
        ("സാഫിർ", "ഓറിയോൺ"), ("റിഗൽ", "ഓറിയോൺ"), ("ബെറ്റൽജൂസ്", "ഓറിയോൺ"),
    ]
    const_names = list({c[1] for c in bright_stars})
    for star, const in bright_stars:
        q = f"നക്ഷത്രം '{star}' ഏത് നക്ഷത്രസമൂഹത്തിലാണ്?"
        opts = [const] + pick_distractors(const_names, const)
        catalog.append((q, opts, const, "hard"))

    # IAU constellations Malayalam
    iau = [
        "ഓറിയോൺ", "വൃശ്ചികം", "സിംഹം", "കുംഭം", "മകരം", "മേടം", "ഇടവം", "മിഥുനം",
        "കർക്കടകം", "കന്നി", "തുലാം", "ധനു", "മീനം", "വൃഷഭം", "കുതിര", "ചെറു നായ",
        "കരഭം", "ഹംസം", "കാസ്സിയോപിയ", "പെർസിയസ്", "ഓഫിയൂചസ്", "ഹെർകുലസ്",
        "ബൂട്ടിസ്", "കോർവസ്", "സെന്റോറസ്", "ലയ്ര", "സൈഗ്നസ്", "ആക്വില",
        "ആക്വാരിയസ്", "പിസിസസ്", "ആൻഡ്രോമീഡ", "ട്രയാംഗുലം", "മാഗല്ലാനിക്",
        "ഫോർനാക്സ്", "ഫീനിക്സ്", "ഗ്രൂസ്", "ഇൻഡസ്", "ലാപ്പസ്", "ലിയോ മൈനർ",
        "ലിയോ", "ലിംക്സ്", "ലൂപ്പസ്", "മെനിസ", "മൈക്രോസ്കോപിയം", "മോൺസെറോസ്",
        "നോർമ", "പാവോ", "പെഗാസസ്", "പെര്സിയ", "പവോ", "പൈക്സിസ്", "പൈസിസ് ഓസ്ട്രിനസ്",
        "പൈസിസ് ഓസ്ട്രാലിസ്", "പൈസിസ് വോളാൻസ്", "പൈസിസ് ഓസ്ട്രിനസ്",
        "പൈസിസ്", "പൈസിസ് ഓസ്ട്രിനസ്", "പൈസിസ് വോളാൻസ്",
    ]
    for i, c in enumerate(iau):
        q = f"നക്ഷത്രസമൂഹം '{c}' ഏതാണ്?"
        opts = [c] + pick_distractors(iau, c)
        catalog.append((q, opts, c, "hard"))

    # ISRO satellites
    satellites = [
        ("ആര്യഭട്ട", "1975", "ഇന്ത്യയുടെ ആദ്യ ഉപഗ്രഹം"),
        ("ഭാസ്കര", "1979", "ഭൂമി നിരീക്ഷണ ഉപഗ്രഹം"),
        ("റോഹിണി", "1980", "എസ്.എസ്.എൽ.വി-യിൽ വിക്ഷേപിച്ച ഉപഗ്രഹം"),
        ("ഇൻസാറ്റ്-1ബി", "1983", "ദൂരസംപർക്ക ഉപഗ്രഹം"),
        ("IRS-1എ", "1988", "ഭൂമി നിരീക്ഷണ ശ്രേണി"),
        ("INSAT-2എ", "1992", "ദൂരസംപർക്ക ശ്രേണി"),
        ("IRS-P3", "1996", "ഭൂമി നിരീക്ഷണം"),
        ("TES", "2001", "ത്രിവിമ ഉപഗ്രഹം"),
        ("കല്പന-1", "2003", "ഇന്ത്യയുടെ ആദ്യ ചന്ദ്ര ഉപഗ്രഹം"),
        ("എഡുസാറ്റ്", "2004", "വിദ്യാഭ്യാസ ഉപഗ്രഹം"),
        ("കാർട്ടോസാറ്റ്-1", "2005", "ഭൂമി നിരീക്ഷണം"),
        ("ഇൻസാറ്റ്-4സിആർ", "2007", "ദൂരസംപർക്കം"),
        ("ചന്ദ്രയാൻ-1", "2008", "ചന്ദ്ര ദൗത്യം"),
        ("രിസാറ്റ്-2ബിആർ1", "2009", "റഡാർ ഇമേജിംഗ്"),
        ("GST-9", "2011", "ദൂരസംപർക്കം"),
        ("സരാൾ", "2012", "മെസോസ്ഫിയർ പഠനം"),
        ("IRNSS-1എ", "2013", "നാവിഗേഷൻ ഉപഗ്രഹം"),
        ("മംഗള്യാൻ", "2013", "ചൊവ്വാ ദൗത്യം"),
        ("ആസ്ട്രോസാറ്റ്", "2015", "ബഹിരാകാശ ദൂരദർശിനി"),
        ("ചന്ദ്രയാൻ-2", "2019", "ചന്ദ്ര ദൗത്യം"),
        ("എംസാറ്റ്-30ബി", "2019", "ഭൂമി നിരീക്ഷണം"),
        ("ആദിത്യ-എൽ1", "2023", "സൗര്യ ദൗത്യം"),
        ("ചന്ദ്രയാൻ-3", "2023", "ചന്ദ്ര സോഫ്റ്റ് ലാൻഡിങ്"),
        ("XPoSat", "2024", "എക്സ്-റേ polaരിമെട്രി"),
    ]
    sat_names = [s[0] for s in satellites]
    sat_descs = [s[2] for s in satellites]
    for name, year, desc in satellites:
        q1 = f"ഇസ്റോ ഉപഗ്രഹം/ദൗത്യം '{name}'-ന്റെ പ്രധാന സവിശേഷത ഏതാണ്?"
        opts1 = [desc] + pick_distractors(sat_descs, desc)
        catalog.append((q1, opts1, desc, "hard"))
        q2 = f"'{desc}' എന്ന സവിശേഷതയുള്ള ഇസ്റോ ദൗത്യം ഏത്?"
        opts2 = [name] + pick_distractors(sat_names, name)
        catalog.append((q2, opts2, name, "hard"))

    # Layer facts - sun structure
    sun_layers = [
        ("കോർ", "സൂര്യന്റെ അന്തർഭാഗം"),
        ("റേഡിയേറ്റീവ് സോൺ", "ഊർജ്ജം കൈമാറുന്ന പാളി"),
        ("കൺവെക്റ്റീവ് സോൺ", "ചലനാത്മക ഊർജ്ജ കൈമാറ്റം"),
        ("ഫോട്ടോസ്ഫിയർ", "ദൃശ്യ പ്രകാശം പുറത്തുവിടുന്ന പാളി"),
        ("ക്രോമോസ്ഫിയർ", "സൂര്യന്റെ ഇടത്തരം അന്തരീക്ഷം"),
        ("കൊറോണ", "സൂര്യന്റെ ഏറ്റവും പുറമെയുള്ള അന്തരീക്ഷം"),
    ]
    layer_names = [l[0] for l in sun_layers]
    layer_descs = [l[1] for l in sun_layers]
    for layer, desc in sun_layers:
        q = f"സൂര്യന്റെ '{layer}' ഏതിനെ സൂചിപ്പിക്കുന്നു?"
        opts = [desc] + pick_distractors(layer_descs, desc)
        catalog.append((q, opts, desc, "hard"))

    # Galaxy types
    galaxy_types = [
        ("സർപിലാകാര ഗാലക്സി", "സ്പൈറൽ ഗാലക്സി"),
        ("ദീർഘവൃത്താകാര ഗാലക്സി", "എല്ലിപ്റ്റിക്കൽ ഗാലക്സി"),
        ("അക്രമാകാര ഗാലക്സി", "ഇറ്രെഗുലർ ഗാലക്സി"),
        ("ആകാശഗംഗ", "സർപിലാകാര ഗാലക്സി"),
        ("ആൻഡ്രോമീഡ", "സർപിലാകാര ഗാലക്സി"),
        ("മാഗല്ലാനിക് മേഘങ്ങൾ", "അക്രമാകാര ഗാലക്സി"),
    ]
    gnames = [g[0] for g in galaxy_types]
    gtypes = list({g[1] for g in galaxy_types})
    for gname, gtype in galaxy_types:
        q = f"ഗാലക്സി '{gname}' ഏത് തരത്തിൽ പെടുന്നു?"
        opts = [gtype] + pick_distractors(gtypes, gtype)
        catalog.append((q, opts, gtype, "hard"))

    # Asteroids
    for ast in ASTEROID_BELT:
        q = f"ക്ഷുദ്രഗ്രഹം '{ast}' ഏത് പ്രദേശത്താണ്?"
        belts = ["ആസ്റ്ററോയിഡ് ബെൽറ്റ്", "കൈപ്പർ ബെൽറ്റ്", "ഓർട്ട് മേഘം", "അന്തർനക്ഷത്ര മേഖല"]
        opts = ["ആസ്റ്ററോയിഡ് ബെൽറ്റ്"] + pick_distractors(belts, "ആസ്റ്ററോയിഡ് ബെൽറ്റ്")
        catalog.append((q, opts, "ആസ്റ്ററോയിഡ് ബെൽറ്റ്", "hard"))

    # Historical discoveries by year
    discoveries = [
        ("യുറാനസ്", "1781", "വില്യം ഹേഴ്സൽ"),
        ("നെപ്റ്റ്യൂൺ", "1846", "ജോൺ ഗോട്രീബ് ഗാല"),
        ("പ്ലൂട്ടോ", "1930", "ക്ലൈഡ് ടോംബോ"),
        ("സെറസ്", "1801", "ജ്യൂസെപ്പ് പിയാസി"),
        ("പല്ലാസ്", "1802", "ഹെൻറിഖ് ഒൽബേഴ്സ്"),
        ("വെസ്റ്റ", "1807", "ഹെൻറിഖ് ഒൽബേഴ്സ്"),
    ]
    disc_names = [d[0] for d in discoveries]
    disc_years = [d[1] for d in discoveries]
    disc_people = [d[2] for d in discoveries]
    for obj, year, person in discoveries:
        q1 = f"'{obj}' കണ്ടെത്തിയ വർഷം ഏത്?"
        opts1 = [year] + pick_distractors(disc_years, year)
        catalog.append((q1, opts1, year, "hard"))
        q2 = f"'{obj}' കണ്ടെത്തിയ ശാസ്ത്രജ്ഞൻ ആരാണ്?"
        opts2 = [person] + pick_distractors(disc_people, person)
        catalog.append((q2, opts2, person, "hard"))

    # Space stations
    stations = [
        ("സ്കൈലാബ്", "നാസ", "1973"),
        ("മിർ", "സോവിയറ്റ് യൂണിയൻ", "1986"),
        ("അന്താരാഷ്ട്ര ബഹിരാകാശ നിലയം", "അന്താരാഷ്ട്ര സഹകരണം", "1998"),
        ("ടിയാൻഗോങ്", "ചൈന", "2021"),
        ("സല്യൂട്ട് 1", "സോവിയറ്റ് യൂണിയൻ", "1971"),
    ]
    st_names = [s[0] for s in stations]
    st_orgs = list({s[1] for s in stations})
    for name, org, year in stations:
        q1 = f"ബഹിരാകാശ നിലയം '{name}' നിർമ്മിച്ച സംഘടന/രാജ്യം ഏത്?"
        opts1 = [org] + pick_distractors(st_orgs, org)
        catalog.append((q1, opts1, org, "medium"))
        q2 = f"ബഹിരാകാശ നിലയം '{name}' സ്ഥാപിച്ച വർഷം ഏത്?"
        years = [s[2] for s in stations]
        opts2 = [year] + pick_distractors(years, year)
        catalog.append((q2, opts2, year, "hard"))

    for q, opts, ans, diff in catalog:
        if len(questions) + (num - max_id_num(questions)) >= TARGET:
            break
        try:
            num = add_q(questions, existing, num, q, opts, ans, diff)
        except ValueError:
            pass
    return num


def generate_from_facts(questions, existing, num):
    """Generate questions from astronomy_facts banks."""
    planet_names = [p[0] for p in PLANETS]
    moon_names = [m[0] for m in MOONS_EXT]
    const_names = list({s[1] for s in STARS_EXT})
    star_names = [s[0] for s in STARS_EXT]
    orgs = list({m[1] for m in MISSIONS_EXT})
    years = list({m[2] for m in MISSIONS_EXT})
    targets = list({m[3] for m in MISSIONS_EXT})
    types = list({d[1] for d in DEEP_SKY})
    locations = list({d[2] for d in DEEP_SKY})
    dsky_names = [d[0] for d in DEEP_SKY]
    people = [a[0] for a in ASTRONOMERS_EXT]
    achievements = [a[1] for a in ASTRONOMERS_EXT]
    terms = [t[0] for t in TERMS]
    defs = [t[1] for t in TERMS]
    event_years = list({e[0] for e in EVENTS})

    for moon, planet in MOONS_EXT:
        q1 = f"ഉപഗ്രഹം '{moon}' ഏത് ഗ്രഹത്തിലാണ്?"
        opts1 = [planet] + pick_distractors(planet_names, planet)
        num = add_q(questions, existing, num, q1, opts1, planet, "medium")
        q2 = f"{planet}യുടെ ഉപഗ്രഹം '{moon}' ഏതാണ്?"
        pool = [m[0] for m in MOONS_EXT if m[1] == planet] + moon_names
        opts2 = [moon] + pick_distractors(pool, moon)
        num = add_q(questions, existing, num, q2, opts2, moon, "hard")

    for star, const in STARS_EXT:
        q1 = f"നക്ഷത്രം '{star}' ഏത് നക്ഷത്രസമൂഹത്തിലാണ്?"
        opts1 = [const] + pick_distractors(const_names, const)
        num = add_q(questions, existing, num, q1, opts1, const, "hard")
        q2 = f"നക്ഷത്രസമൂഹം '{const}'-ൽ സ്ഥിതി ചെയ്യുന്ന നക്ഷത്രം ഏത്?"
        pool = [s[0] for s in STARS_EXT if s[1] == const] + star_names
        opts2 = [star] + pick_distractors(pool, star)
        num = add_q(questions, existing, num, q2, opts2, star, "hard")

    for year, event, ans, diff in EVENTS:
        q = f"{event}?"
        opts = [ans] + pick_distractors(event_years, ans)
        num = add_q(questions, existing, num, q, opts, ans, diff)

    for obj, person, year in DISCOVERIES:
        q1 = f"'{obj}' കണ്ടെത്തിയ വർഷം ഏത്?"
        opts1 = [year] + pick_distractors(event_years, year)
        num = add_q(questions, existing, num, q1, opts1, year, "hard")
        q2 = f"'{obj}' കണ്ടെത്തിയ ശാസ്ത്രജ്ഞൻ ആരാണ്?"
        opts2 = [person] + pick_distractors(people, person)
        num = add_q(questions, existing, num, q2, opts2, person, "hard")

    for name, typ, loc in DEEP_SKY:
        if re.search(r"-\d+$", name) or "NGC-" in name:
            continue  # skip fabricated numbered deep-sky filler
        q1 = f"ആകാശ വസ്തു '{name}' ഏത് തരത്തിൽ പെടുന്നു?"
        opts1 = [typ] + pick_distractors(types, typ)
        num = add_q(questions, existing, num, q1, opts1, typ, "hard")
        q2 = f"ആകാശ വസ്തു '{name}' ഏത് നക്ഷത്രസമൂഹം/പ്രദേശത്താണ്?"
        opts2 = [loc] + pick_distractors(locations, loc)
        num = add_q(questions, existing, num, q2, opts2, loc, "hard")

    for name, org, year, target in MISSIONS_EXT:
        q1 = f"ബഹിരാകാശ ദൗത്യം '{name}' നടപ്പാക്കിയ സംഘടന ഏത്?"
        opts1 = [org] + pick_distractors(orgs, org)
        num = add_q(questions, existing, num, q1, opts1, org, "medium")
        q2 = f"ദൗത്യം '{name}' വിക്ഷേപിച്ച വർഷം ഏത്?"
        opts2 = [year] + pick_distractors(years, year)
        num = add_q(questions, existing, num, q2, opts2, year, "hard")
        q3 = f"ദൗത്യം '{name}'-ന്റെ പ്രധാന ലക്ഷ്യം ഏത്?"
        opts3 = [target] + pick_distractors(targets, target)
        num = add_q(questions, existing, num, q3, opts3, target, "medium")

    for person, achievement in ASTRONOMERS_EXT:
        q1 = f"{person} ഏതുമായി പ്രധാനമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"
        opts1 = [achievement] + pick_distractors(achievements, achievement)
        num = add_q(questions, existing, num, q1, opts1, achievement, "medium")
        q2 = f"'{achievement}' ആവിഷ്കരിച്ച/കണ്ടെത്തിയ ശാസ്ത്രജ്ഞൻ ആരാണ്?"
        opts2 = [person] + pick_distractors(people, person)
        num = add_q(questions, existing, num, q2, opts2, person, "medium")

    for term, defn in TERMS:
        q1 = f"ജ്യോതിശാസ്ത്രത്തിൽ '{term}' എന്തിനെ സൂചിപ്പിക്കുന്നു?"
        opts1 = [defn] + pick_distractors(defs, defn)
        num = add_q(questions, existing, num, q1, opts1, defn, "hard")
        q2 = f"'{defn}' എന്ന വിവരണം ഏത് പദവുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?"
        opts2 = [term] + pick_distractors(terms, term)
        num = add_q(questions, existing, num, q2, opts2, term, "hard")

    return num


def git_head_questions() -> list[dict]:
    try:
        raw = subprocess.check_output(["git", "show", "HEAD:astronomy.json"], cwd=BASE)
        return json.loads(raw).get("questions", [])
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return []


def main():
    random.seed(42)
    path = BASE / "astronomy.json"
    head_qs = git_head_questions()
    questions = list(head_qs) if head_qs else list(json.loads(path.read_text(encoding="utf-8")).get("questions", []))
    existing = load_existing_questions()
    num = max_id_num(questions) + 1

    generators = [
        generate_planet_questions,
        generate_moon_questions,
        generate_star_questions,
        generate_mission_questions,
        generate_astronomer_questions,
        generate_concept_questions,
        generate_isro_questions,
        generate_telescope_questions,
        generate_dwarf_planet_questions,
        generate_bulk_facts,
        generate_nakshatra_questions,
        generate_messier_questions,
        generate_comparison_questions,
        generate_phenomena_questions,
        generate_space_people_questions,
        generate_extended_catalog,
        generate_from_facts,
    ]

    for gen in generators:
        if len(questions) >= TARGET:
            break
        num = gen(questions, existing, num)

    for i, q in enumerate(questions, 1):
        q["id"] = f"{PREFIX}{i:04d}"

    data = {"questions": questions[:TARGET]}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"astronomy.json: {len(data['questions'])} questions (target {TARGET})")


if __name__ == "__main__":
    main()
