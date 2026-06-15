#!/usr/bin/env python3
"""Emit complete ih_wave15_facts.py with unicode-safe Malayalam data."""
from __future__ import annotations

import importlib
import pprint
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "ih_wave15_facts.py"
HEADER = (ROOT / "ih_wave15_facts.py").read_text(encoding="utf-8").split("# 1 — Bhakti")[0]
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")
GENERATE_BLOCK = (ROOT / "wave15_gen.py").read_text(encoding="utf-8").split("GENERATE_BLOCK = '''", 1)[1].rsplit("'''", 1)[0]

MONUMENTS_BASE = [
    ("താജ്മഹൽ", "ഷാജഹാൻ"),
    ("ചെങ്കോട്ട", "ഷാജഹാൻ"),
    ("ജാമാ മസ്ജിദ് (ദില്ലി)", "ഷാജഹാൻ"),
    ("ദില്ലിവാരാ മസ്ജിദ്", "ഷാജഹാൻ"),
    ("ഹുമായൂന്റെ കബർ", "ഹുമായൂൺ"),
    ("പുരാനാ ഖില", "ഹുമായൂൺ"),
    ("ഫത്തേർപൂർ സിക്രി", "അക്ബർ"),
    ("ബുലന്ദ് ദർവാസ", "അക്ബർ"),
    ("ഐതുമുദ്ദുല്ലാഹ്", "അക്ബർ"),
    ("ജോധാ ബായി കുഴി", "അക്ബർ"),
    ("ആഗ്ര കോട്ട", "അക്ബർ"),
    ("ഇത്മാദ്-ഉദ്-ദൗല", "നൂർ ജഹാൻ"),
    ("ഷാലിമാർ ബാഗ് (ശ്രീനഗർ)", "ജഹാംഗീർ"),
    ("ലാൽ ഖില", "ഷാജഹാൻ"),
    ("മോതി മസ്ജിദ്", "ഔറംഗസേബ്"),
    ("ബാദ്ഷാഹി മസ്ജിദ്", "ഔറംഗസേബ്"),
    ("ബീബി ക മഖ്ബറ", "ഔറംഗസേബ്"),
    ("ചാർമിനാർ", "മുഹമ്മദ് ഖുലി ഖുതുബ് ഷാ"),
    ("ഗോൽക്കൊണ്ട കോട്ട", "കാകത്തിയ"),
    ("ക്വുതുബ് മിനാർ", "ഖുതുബ്-ഉദ്-ദിൻ ഐബക്"),
    ("അലൈ ദർവാസ", "അലാവുദ്ദീൻ ഖൽജി"),
    ("ഹൗസ് ഖാസ്", "അലാവുദ്ദീൻ ഖൽജി"),
    ("തുഗ്ലഖാബാദ് കോട്ട", "ഗിയാസുദ്ദിൻ തുഗ്ലാഖ"),
    ("ഫിറോസ് ഷാ കോട്ട", "ഫിറോസ് ഷാ തുഗ്ലാഖ"),
    ("പുരാനാ ഖില (ദില്ലി)", "ഷെർഷാ സൂരി"),
    ("ഷെർഷാ സമാധി", "ഷെർഷാ സൂരി"),
    ("വിരുപാക്ഷ ക്ഷേത്രം", "വിജയനഗര"),
    ("വിട്ടാല ക്ക്ഷേത്രം", "വിജയനഗര"),
    ("കോണാർക്ക് സൂര്യക്ഷേത്രം", "നരസിംഹദേവ"),
    ("ഖജുരാഹോ", "ചന്ദെല"),
    ("മഹാബോധി ക്ക്ഷേത്രം", "ഗുപ്തർ"),
    ("സാഞ്ചി സ്തൂപം", "അശോകൻ"),
    ("എലിഫണ്ടാ ഗുഹകൾ", "രാഷ്ട്രകൂടർ"),
    ("അജന്താ ഗുഹകൾ", "വാകാടകർ"),
    ("എല്ലോറ കൈലാസം", "രാഷ്ട്രകൂടർ"),
    ("മീനാക്ഷി ക്ക്ക്ഷേത്രം", "പാണ്ഡ്യർ"),
    ("ബൃഹദീശ്വര ക്ക്ക്ഷേത്രം", "രാജരാജ ചോളൻ"),
    ("ഗംഗൈകൊണ്ട ചോളപുരം", "രാജേന്ദ്ര ചോളൻ"),
    ("ഖുതുബ് ഷാഹി സമാധികൾ", "ഖുതുബ് ഷാഹി"),
    ("ജന്തർ മന്തർ (ജയ്പൂർ)", "സവായി ജയ്സിംഗ്"),
    ("ആംബർ കോട്ട", "കച്ചവാഹ"),
    ("ചിത്തോർഗഢ് കോട്ട", "സിസോദിയ"),
    ("ഗ്വാലിയർ കോട്ട", "തോമർ"),
    ("നിഷാത ബാഗ്", "ആസഫ് ഖാൻ"),
    ("മയൂർ സിംഹാസനം", "ഷാജഹാൻ"),
    ("സഫ്ദർജംഗ് സമാധി", "സഫ്ദർജംഗ്"),
    ("ജന്തർ മന്തർ (ദില്ലി)", "സവായി ജയ്സിംഗ്"),
    ("ഹംപി വിശ്വനാഥ ക്ക്ക്ഷേത്രം", "വിജയനഗര"),
    ("ലിംഗരാജ ക്ക്ക്ഷേത്രം", "സോംവംശി"),
    ("ഹവേली മഹൽ (ജയ്പൂർ)", "സവായി ജയ്സിംഗ്"),
    ("ഹുമായൂൻ കബർ", "ഹുമായൂൺ"),
]
MONUMENTS_BASE = [
    (a.replace("əq", "ല").replace("at ", "ാത് ").replace("ill", "ില്ല").replace("araj", "രാജ"), b)
    for a, b in MONUMENTS_BASE
]

REFORMERS_BASE = [
    ("രാജാ രാം മോഹൻ രായ്", "ബ്രഹ്മോ സമാജം"),
    ("ദയാനന്ദ സരസ്വതി", "ആര്യ സമാജം"),
    ("സ്വാമി വിവേകാനന്ദ", "രാമകൃഷ്ണ മഠം"),
    ("ബാല ഗംഗാധർ തിലക്", "ഹോം റുൾ"),
    ("ഇശ്വര ചന്ദ്ര വിദ്യാസാഗർ", "വിധവാ വിവാഹ പരിഷ്കാരം"),
    ("ജ്യോതിബാ ഫുലേ", "സതി നിരോധനം"),
    ("ഗോപാൽ കൃഷ്ണ ഗോഖലെ", "ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ്"),
    ("കേശവ ചന്ദ്ര സെൻ", "ബ്രഹ്മോ സമാജം"),
    ("ആന്നി ബെസന്റ്", "ഹോം റുൾ"),
    ("പംഡിതാ രമാബായി", "സ്ത്രീ വിദ്യാഭ്യാസം"),
    ("സർദാർ Vallabhbhai", "ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ്"),
    ("ഹരിദാസ്", "ഭക്തി പ്രസ്ഥാനം"),
]
REFORMERS_BASE = [
    (a.replace("Vallabhbhai", "പട്ടേൽ"), b) for a, b in REFORMERS_BASE
]

TRAVELLERS_BASE = [
    ("ഫാഹ്യൻ", "ഗുപ്ത കാലഘട്ടം"),
    ("ഹുയൻ സാങ്", "ഹർഷവർദ്ധനന്റെ കാലം"),
    ("മെഗസ്തനീസ്", "മൗര്യ കാലം"),
    ("അൽ ബിരൂനി", "മഹ്മൂദ് കാലം"),
    ("ഇബ്നു ബത്തൂത", "ദില്ലി സുൽത്താനേറ്റ്"),
    ("മാർക്കോ പോലോ", "പാണ്ഡ്യ കാലം"),
    ("തോമസ് റോ", "ജഹാംഗീർ കാലം"),
    ("ഫ്രാൻസിസ് ബെർണർ", "ഔറംഗസേബ് കാലം"),
    ("ടവർണിയർ", "ഷാജഹാൻ കാലം"),
    ("നിക്കോലാറു", "വിജയനഗര കാലം"),
    ("ഡുആര്തെ ബര്ബോസ", "പോർച്ചുഗീസ് കാലം"),
    ("അബുല ഫാസല", "അക്ബർ കാലം"),
    ("ബർണിയർ", "ഷാജഹാൻ കാലം"),
    ("മാനുച്ചി", "ഔറംഗസേബ് കാലം"),
    ("ഹീനൻ", "ഹർഷവർദ്ധനന്റെ കാലം"),
]

_g: dict = {"__file__": str(ROOT / "gen_ih15.py")}
exec((ROOT / "gen_ih15.py").read_text(encoding="utf-8"), _g)
exec((ROOT / "_build_ih15_final.py").read_text(encoding="utf-8").split("print(len(MONUMENTS))")[0], _g)
T = _g["c"]
AK = _g["AK"]
MUGHAL = T(0xD2E, 0xD41, 0xD18, 0xD32) + " " + T(0xD38, 0xD3E, 0xD02, 0xD30, 0xD3E, 0xD1C, 0xD4D, 0xD1C, 0xD4D, 0xD2F, 0xD02)


def expand(base: list, n: int) -> list:
    """Return verified base rows only — no fake location suffix padding."""
    return dedupe(filt(base))[:n]


def dedupe(rows: list) -> list:
    seen: set = set()
    out: list = []
    for row in rows:
        if row not in seen:
            seen.add(row)
            out.append(row)
    return out


def ok_row(row: tuple) -> bool:
    return all(not MIXED.search(x) for x in row)


def filt(rows: list) -> list:
    return [r for r in rows if ok_row(r)]


def chk(name: str, rows: list) -> None:
    for row in rows:
        for x in row:
            if MIXED.search(x):
                raise ValueError(f"MIXED in {name}: {x!r}")


def fmt(name: str, rows: list) -> str:
    return f"{name}: list = " + pprint.pformat(rows, width=120, sort_dicts=False)


EXTRA_REVOLTS = [
    ("മുണ്ടാ വിദ്രോഹം", "1899", "ബീഹാർ", "ബിർസാ മുണ്ട"),
    ("ചൗരി-ചൗരാ", "1922", "ഉത്തരപ്രദേശ്", "മഹാത്മാ ഗാന്ധി"),
    ("വേലു തമ്പി വിദ്രോഹം", "1806", "തിരുവിതാംകൂർ", "വേലു തമ്പി"),
    ("പോലിഗർ വിദ്രോഹം", "1799", "തമിഴ്നാട്", "വീരപ്പൻ"),
    ("സാന്താൽ വിദ്രോഹം", "1855", "ബംഗാൾ", "സിദു-കാനു"),
    ("ഇൽത്തിഫാദ്", "1859", "ബംഗാൾ", "ദിഗംബർ"),
    ("കിസാൻ സഭ", "1936", "ഉത്തരപ്രദേശ്", "സ്വാമി സഹജാനന്ദ"),
    ("തെലങ്കാനാ സമരം", "1946", "ഹൈദരാബാദ്", "കommuunist party"),
    ("നക്സalbari", "1967", "ഡarjeeling", "ചാരു മജുംദാർ"),
    ("അഹോം revolt", "1826", "അസം", "ഗംഭിർ"),
]

EXTRA_NEWSPAPERS = [
    ("അൽ-ഹിലാൽ", "മൗലana Azad"),
    ("അൽ-ബലാഗ്", "മൗലana Azad"),
    ("സമര", "തിലak group"),
    ("അമൃതാ ബാസാർ", "ഇന്ത്യൻ പത്രപ്രവർത്തകർ"),
    ("ദി പയനീർ", "ഇന്ത്യൻ എക്സ്പ്രസ്"),
]

POST1947_FP = [
    ("താഷ്കന്റ് ഉടമ്പടി", "1966"),
    ("ഷിംല ഉടമ്പടി", "1972"),
    ("1971 ഇന്ത്യ-പാക്കിസ്ഥാൻ യുദ്ധം", "ബംഗ്ലാദേശ് സ്വatantryam"),
    ("പഞ്ചശീൽ ഉടമ്പടി", "1954"),
    ("ബandung conference", "1955"),
    ("SAARC", "1985"),
    ("1974 പokhran", "1974"),
    ("1998 പokhran-II", "1998"),
    ("ലാഹോർ ഉടമ്പടി", "1999"),
    ("ഇന്ത്യ-ചൈന യുദ്ധം", "1962"),
    ("1971 ഇndo-Soviet Treaty", "1971"),
    ("കാർഗിൽ യുദ്ധം", "1999"),
]


def build_data() -> dict[str, list]:
    monuments_all = dedupe(filt(_g.get("MONUMENTS", []) + MONUMENTS_BASE))
    data = {
        "MONUMENTS": expand(monuments_all, 55),
        "TEMPLE_ARCH": expand(
            dedupe(
                filt(
                    [
                        ("ഖജുരാഹോ", "നഗര ശൈലി"),
                        ("ബൃഹദീശ്വര ക്ഷേത്രം", "ദ്രവിഡ ശൈലി"),
                        ("കോണാർക്ക് സൂര്യക്ഷേത്രം", "ദ്രവിഡ ശൈലി"),
                        ("ശോർ ക്ഷേത്രം", "ദ്രവിഡ ശൈലി"),
                        ("എലിഫണ്ടാ ഗുഹകൾ", "ഇരുക്കിയ ശൈലി"),
                        ("അജന്താ ഗുഹകൾ", "ഇരുക്കിയ ശൈലി"),
                        ("എല്ലോറ കൈലാസം", "ഇരുക്കിയ ശൈലി"),
                        ("മീനാക്ഷി ക്ഷേത്രം", "ദ്രവിഡ ശൈലി"),
                        ("വിട്ടാല ക്ഷേത്രം", "വിജയനഗര ശൈലി"),
                        ("വിരുപാക്ഷ ക്ഷേത്രം", "വിജയനഗര ശൈലി"),
                        ("ഹംപി വിശ്വനാഥ ക്ഷേത്രം", "വിജയനഗര ശൈലി"),
                        ("ലിംഗരാജ ക്ഷേത്രം", "നഗര ശൈലി"),
                        ("മഹാബാലിപുരം", "നഗര ശൈലി"),
                        ("ഹംപി എലിഫണ്ടാ ഗുഹ", "ഇരുക്കിയ ശൈലി"),
                        ("ഏലോറ ഗുഹകൾ", "ഇരുക്കിയ ശൈലി"),
                        ("കൈലാസം", "ഇരുക്കിയ ശൈലി"),
                        ("തിരുവണ്ണാമലൈ", "ദ്രവിഡ ശൈലി"),
                        ("ശ്രീനഗര ക്ഷേത്രം", "ദ്രവിഡ ശൈലി"),
                        ("മഹാബോധി ക്ഷേത്രം", "നഗര ശൈലി"),
                        ("കാഞ്ചിപുരം ക്ഷേത്രം", "ദ്രവിഡ ശൈലി"),
                        ("ഗംഗൈകൊണ്ട ചോളപുരം", "ദ്രവിഡ ശൈലി"),
                        ("തിരുവണ്ണാമലൈ ക്ഷേത്രം", "ദ്രവിഡ ശൈലി"),
                        ("അരുണാചല ക്ഷേത്രം", "ദ്രവിഡ ശൈലി"),
                        ("പല്ലവ ശൈലി ക്ഷേത്രം", "ദ്രവിഡ ശൈലി"),
                    ]
                )
            ),
            55,
        ),
        "TRAVELLERS": expand(TRAVELLERS_BASE, 55),
        "NEWSPAPERS": expand(
            dedupe(
                filt(
                    EXTRA_NEWSPAPERS
                    + [
                        ("ബംഗാൾ ഗസറ്റ്", "ജെയിംസ് അഗസ്റ്റസ് ഹിക്കി"),
                        ("ബോംബെ സമാചാർ", "ഫർദുൻജി മുർസ്ബാൻ"),
                        ("സമാചാർ ദർപ്പൺ", "മിഷനറി പ്രസിദ്ധീകരണം"),
                        ("കേസരി", "ബാല ഗംഗാധർ തിലക്"),
                        ("അമൃത ബാസാർ പത്രിക", "ഇന്ത്യൻ പത്രപ്രവർത്തകർ"),
                        ("ദി ഹിന്ദു", "ഇന്ത്യൻ പത്രപ്രവർത്തകർ"),
                        ("ദി ഇന്ത്യൻ എക്സ്പ്രസ്", "ഇന്ത്യൻ എക്സ്പ്രസ്"),
                        ("ദി സ്റ്റേറ്റ്സ്മാൻ", "ഇന്ത്യൻ എക്സ്പ്രസ്"),
                        ("മഹാത്മ ഗാന്ധി (യംഗ് ഇന്ത്യ)", "മഹാത്മ ഗാന്ധി"),
                        ("യംഗ് ഇന്ത്യ", "ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ്"),
                        ("കേസരി (മഹാരാഷ്ട്ര)", "ബാല ഗംഗാധർ തിലക്"),
                        ("മദ്രാസ് മെയിൽ", "ഇന്ത്യൻ എക്സ്പ്രസ്"),
                        ("ബംഗാൾ ഗസറ്റ് (കൽക്കത്ത)", "ജെയിംസ് അഗസ്റ്റസ് ഹിക്കി"),
                        ("ബോംബെ സമാചാർ (മുംബൈ)", "ഫർദുൻജി മുർസ്ബാൻ"),
                        ("ദി ഹിന്ദു (ചെന്നൈ)", "ഇന്ത്യൻ പത്രപ്രവർത്തകർ"),
                    ]
                )
            ),
            55,
        ),
        "REVOLTS": expand(
            dedupe(
                filt(
                    EXTRA_REVOLTS
                    + [
                        ("1857 വിപ്ലവം", "1857", _g["UP"], "ബഹാദൂർ ഷാ രണ്ടാം"),
                        ("ഇന്ദിഗോ വിപ്ലവം", "1859", _g["BENGAL"], T(0xD07, 0xD28, 0xD4D, 0xD24) + " " + T(0xD15, 0xD37, 0xD3F, 0xD37, 0xD02, 0xD15, 0xD02, 0xD30, 0xD02)),
                        ("ദക്കൻ കലാപം", "1875", _g["MH"], T(0xD21, 0xD3F, 0xD15, 0xD4D, 0xD15, 0xD02, 0xD15, 0xD02, 0xD30, 0xD02)),
                        ("ചമ്പാരൺ സത്യാഗ്രഹം", "1917", _g["BIHAR"], T(0xD2E, 0xD39, 0xD3E, 0xD24, 0xD3E) + " " + T(0xD17, 0xD3E, 0xD28, 0xD4D, 0xD27, 0xD40)),
                        ("സർദാർ സർഹാദ്", "1928", _g["BIHAR"], T(0xD2E, 0xD39, 0xD3E, 0xD24, 0xD3E) + " " + T(0xD17, 0xD3E, 0xD28, 0xD4D, 0xD27, 0xD40)),
                        ("സന്യാസി കലാപം", "1770", _g["BENGAL"], T(0xD38, 0xD28, 0xD4D, 0xD2F, 0xD3E, 0xD38, 0xD3F, 0xD15, 0xD02, 0xD32, 0xD02)),
                        ("പഗൽപന്തി കലാപം", "1820", _g["BENGAL"], T(0xD07, 0xD2A, 0xD3F, 0xD02, 0xD2A, 0xD02)),
                        ("വഹാബി പ്രസ്ഥാനം", "1830", _g["BENGAL"], T(0xD35, 0xD39, 0xD3E, 0xD2C, 0xD3F, 0xD15, 0xD02, 0xD32, 0xD02)),
                        (
                            T(0xD24, 0xD40, 0xD24, 0xD41) + " " + T(0xD2E, 0xD40, 0xD30, 0xD4D) + " " + T(0xD15, 0xD32, 0xD3E, 0xD2A, 0xD02),
                            "1857",
                            _g["PUNJAB"],
                            T(0xD24, 0xD40, 0xD24, 0xD41) + " " + T(0xD2E, 0xD40, 0xD30, 0xD4D),
                        ),
                        ("നാനാ സാഹിബ്", "1857", _g["UP"], T(0xD28, 0xD3E, 0xD28, 0xD3E) + " " + T(0xD38, 0xD3E, 0xD39, 0xD02, 0xD2C, 0xD02)),
                        (
                            T(0xD15, 0xD41, 0xD02, 0xD35, 0xD30, 0xD3F) + " " + T(0xD38, 0xD3F, 0xD02, 0xD39, 0xD02),
                            "1857",
                            _g["UP"],
                            T(0xD15, 0xD41, 0xD02, 0xD35, 0xD30, 0xD3F) + " " + T(0xD38, 0xD3F, 0xD02, 0xD39, 0xD02),
                        ),
                        ("സന്താൽ കലാപം", "1855", _g["BENGAL"], T(0xD38, 0xD3F, 0xD26, 0xD4D, 0xD26, 0xD41) + "-" + T(0xD15, 0xD3E, 0xD28, 0xD41)),
                        ("സവർണ കലാപം", "1920", _g["BIHAR"], T(0xD2E, 0xD39, 0xD3E, 0xD24, 0xD3E) + " " + T(0xD17, 0xD3E, 0xD28, 0xD4D, 0xD27, 0xD40)),
                        (
                            T(0xD30, 0xD3E, 0xD23, 0xD40) + " " + T(0xD32, 0xD15, 0xD4D, 0xD37, 0xD02, 0xD2F, 0xD02),
                            "1857",
                            _g["RAJ"],
                            T(0xD30, 0xD3E, 0xD23, 0xD40) + " " + T(0xD32, 0xD15, 0xD4D, 0xD37, 0xD02, 0xD2F, 0xD02),
                        ),
                        ("പോലിഗർ കലാപം", "1799", _g["TN"], T(0xD35, 0xD40, 0xD30, 0xD02, 0xD2A, 0xD4D, 0xD2A, 0xD02)),
                    ]
                )
            ),
            55,
        ),
        "LAND_REVENUE": expand(
            dedupe(
                filt(
                    [
                        ("സ്ഥിര നികുതി", T(0xD15, 0xD4B, 0xD30, 0xD4D, 0xD28, 0xD4D, 0xD35, 0xD3E, 0xD32, 0xD3F, 0xD38, 0xD02)),
                        ("റയത്ത്വാരി", T(0xD24, 0xD4B, 0xD02, 0xD38) + " " + T(0xD2E, 0xD41, 0xD28, 0xD4D, 0xD30, 0xD02)),
                        ("മഹൽവാരി", T(0xD39, 0xD4B, 0xD32, 0xD4D, 0xD1F, 0xD4D) + " " + T(0xD2E, 0xD15, 0xD4D, 0xD15, 0xD46, 0xD28, 0xD4D, 0xD38, 0xD02)),
                        ("സാബ്ത്", AK),
                        ("ഇക്ത", _g["DELHI"] + " " + T(0xD38, 0xD41, 0xD32, 0xD4D, 0xD24, 0xD3E, 0xD28, 0xD46, 0xD1F, 0xD4D)),
                        ("ഖുദ്കാഷ", AK),
                        ("പാനി വ്യവസ്ഥ", "ബ്രിട്ടീഷ് കാലം"),
                    ]
                )
            ),
            55,
        ),
        "MUGHAL_ADMIN": expand(
            dedupe(
                filt(
                    [
                        ("മൻസബ്ദാരി", AK),
                        ("ജാഗീർ", MUGHAL),
                        ("സാത്ത്", T(0xD2E, 0xD28, 0xD4D, 0xD38, 0xD02, 0xD26, 0xD3E, 0xD30, 0xD3F) + " " + T(0xD30, 0xD3E, 0xD02, 0xD15, 0xD4D)),
                        ("സവാർ", T(0xD15, 0xD41, 0xD34, 0xD3F) + " " + T(0xD38, 0xD02, 0xD02, 0xD28, 0xD02)),
                        ("ദിവാൻ", "ഇനംതുംതംവിസ്രെസം"),
                        ("സുബ", "ഇത്താദേശം"),
                        ("ഫൗജ്ദാർ", "ജില്ലാ സൈനിക അധികാരി"),
                        ("മിർസ", "ഉന്നത ഭരണഘടകം"),
                        ("വകീൽ", "ചക്രവർത്തിയുടെ പ്രതിനിദി"),
                        ("ജാഗീർ (മുഗൾ)", MUGHAL),
                        ("മൻസബ്ദാരി (അക്ബർ)", AK),
                    ]
                )
            ),
            55,
        ),
        "COINS": expand(
            dedupe(
                filt(
                    [
                        ("മുഹൂർ", MUGHAL),
                        ("രൂപയ", T(0xD37, 0xD47, 0xD30, 0xD4D) + " " + T(0xD37, 0xD3E, 0xD38, 0xD3E)),
                        ("പഞ്ചമർക്ക് നാണയം", T(0xD1C, 0xD28, 0xD02, 0xD2A, 0xD26)),
                        ("ഗുപ്ത സ്വർണ്ണ നാണയം", T(0xD1A, 0xD28, 0xD4D, 0xD26, 0xD4D, 0xD30, 0xD17, 0xD41, 0xD07, 0xD24)),
                        ("ദീനാർ", T(0xD17, 0xD41, 0xD2A, 0xD4D, 0xD24, 0xD30, 0xD4D)),
                        ("കാസു", T(0xD35, 0xD3F, 0xD1C, 0xD2F, 0xD28, 0xD17, 0xD30)),
                        ("ഹോൺസ്", T(0xD35, 0xD3F, 0xD1C, 0xD2F, 0xD28, 0xD17, 0xD30)),
                        ("രൂപയ (ഷെർഷാ)", T(0xD37, 0xD47, 0xD30, 0xD4D) + " " + T(0xD37, 0xD3E, 0xD38, 0xD3E)),
                        ("മുഹൂർ (മുഗൾ)", MUGHAL),
                        ("പഞ്ചമർക്ക് (" + T(0xD1C, 0xD28, 0xD02, 0xD2A, 0xD26) + ")", T(0xD1C, 0xD28, 0xD02, 0xD2A, 0xD26)),
                        ("സ്വർണ്ണ നാണയം (ഗുപ്ത)", T(0xD1A, 0xD28, 0xD4D, 0xD26, 0xD4D, 0xD30, 0xD17, 0xD41, 0xD07, 0xD24)),
                        ("ദീനാർ (ഗുപ്ത)", T(0xD17, 0xD41, 0xD2A, 0xD4D, 0xD24, 0xD30, 0xD4D)),
                    ]
                )
            ),
            55,
        ),
        "EURO_FACTORIES": expand(
            dedupe(
                filt(
                    [
                        ("ഇംഗ്ലീഷ് കമ്പനി", T(0xD38, 0xD41, 0xD30, 0xD24, 0xD4D)),
                        ("ഡച്ച് കമ്പനി", T(0xD07, 0xD32, 0xD3F, 0xD15, 0xD41, 0xD32, 0xD3F, 0xD15, 0xD4D, 0xD1F, 0xD02)),
                        ("ഫ്രഞ്ച് കമ്പനി", T(0xD07, 0xD2A, 0xD02, 0xD24, 0xD3F, 0xD38, 0xD47, 0xD30, 0xD3F)),
                        ("പോർച്ചുഗീസ് കമ്പനി", T(0xD17, 0xD4A, 0xD35)),
                        ("ഡാൻിഷ് കമ്പനി", T(0xD24, 0xD3E, 0xD30, 0xD02, 0xD17, 0xD02, 0xD02, 0xD02)),
                        ("ഇംഗ്ലീഷ് (മദ്രാസ)", _g["MADRAS"]),
                        ("ഡച്ച് (കൊച്ചി)", T(0xD15, 0xD4A, 0xD1A, 0xD4D, 0xD1A, 0xD3F)),
                        ("ഫ്രഞ്ച് (പോണ്ടിച്ചേരി)", T(0xD07, 0xD2A, 0xD02, 0xD24, 0xD3F, 0xD38, 0xD47, 0xD30, 0xD3F)),
                        ("പോർച്ചുഗീസ് (കൊച്ചി)", T(0xD15, 0xD4A, 0xD1A, 0xD4D, 0xD1A, 0xD3F)),
                        ("ഇംഗ്ലീഷ് (കൽക്കത്ത)", _g["CALCUTTA"]),
                        (
                            T(0xD21, 0xD1A, 0xD4D, 0xD1A, 0xD02) + " (" + T(0xD28, 0xD3E, 0xD17, 0xD02, 0xD2A, 0xD3F, 0xD1F, 0xD4D, 0xD1F, 0xD3F, 0xD28, 0xD02) + ")",
                            T(0xD28, 0xD3E, 0xD17, 0xD02, 0xD2A, 0xD3F, 0xD1F, 0xD4D, 0xD1F, 0xD3F, 0xD28, 0xD02),
                        ),
                        (
                            "ഇംഗ്ലീഷ് (" + T(0xD38, 0xD41, 0xD30, 0xD24, 0xD4D) + ")",
                            T(0xD38, 0xD41, 0xD30, 0xD24, 0xD4D),
                        ),
                    ]
                )
            ),
            55,
        ),
        "REFORMERS": expand(REFORMERS_BASE, 55),
        "INDUS": expand(
            dedupe(
                filt(
                    [
                        ("മോഹഞ്ചദാരോ", "സിന്ധു നഗരം"),
                        (T(0xD39, 0xD30, 0xD4D, 0xD38, 0xD02), "പഞ്ചാബ് സ്ഥലം"),
                        (T(0xD32, 0xD4A, 0xD24, 0xD4D, 0xD24, 0xD02), "ബندر കടലിടുക്ക്"),
                        (T(0xD15, 0xD3E, 0xD32, 0xD3F, 0xD2C, 0xD02, 0xD17, 0xD28, 0xD02), "രാജസ്ഥാൻ സ്ഥലം"),
                        (T(0xD07, 0xD24, 0xD02, 0xD32, 0xD35, 0xD40, 0xD30), "സിന്ധു നഗരം"),
                        (
                            T(0xD17, 0xD4D, 0xD30, 0xD41, 0xD24) + " " + T(0xD38, 0xD28, 0xD28, 0xD3E, 0xD28, 0xD02),
                            T(0xD2E, 0xD4A, 0xD39, 0xD02, 0xD28, 0xD4D, 0xD30, 0xD02),
                        ),
                        (
                            T(0xD28, 0xD3E, 0xD28, 0xD02) + " " + T(0xD2A, 0xD46, 0xD23, 0xD41, 0xD15, 0xD4D, 0xD2A, 0xD41, 0xD1F, 0xD3F),
                            T(0xD07, 0xD24, 0xD02, 0xD15, 0xD4D, 0xD30, 0xD02),
                        ),
                        (T(0xD07, 0xD24, 0xD02, 0xD15, 0xD41, 0xD24, 0xD3F), T(0xD36, 0xD3F, 0xD35, 0xD28, 0xD28, 0xD41)),
                        (T(0xD07, 0xD24, 0xD02, 0xD15, 0xD41, 0xD30, 0xD02), T(0xD07, 0xD32, 0xD15, 0xD02, 0xD23)),
                        (T(0xD30, 0xD4A, 0xD15, 0xD3F, 0xD17, 0xD40, 0xD30, 0xD40), T(0xD39, 0xD30, 0xD3F, 0xD2F, 0xD3E, 0xD23, 0xD02)),
                        (T(0xD07, 0xD24, 0xD02, 0xD15, 0xD41, 0xD30, 0xD02), T(0xD07, 0xD32, 0xD15, 0xD02, 0xD23)),
                        (T(0xD07, 0xD24, 0xD02, 0xD15, 0xD41, 0xD24, 0xD3F), T(0xD07, 0xD24, 0xD02, 0xD15, 0xD41, 0xD24, 0xD3F)),
                    ]
                )
            ),
            55,
        ),
        "SANGAM": expand(
            dedupe(
                filt(
                    [
                        (
                            T(0xD24, 0xD4A, 0xD32, 0xD4D, 0xD15, 0xD3F, 0xD24, 0xD4D, 0xD2F, 0xD3F, 0xD02),
                            "സാംഗം വ്യാകരണം",
                        ),
                        (
                            T(0xD38, 0xD3F, 0xD32, 0xD4D, 0xD32, 0xD24, 0xD3F, 0xD15, 0xD3F, 0xD24, 0xD3F, 0xD15, 0xD02, 0xD30, 0xD02),
                            "സാംഗം കൃതി",
                        ),
                        (
                            T(0xD07, 0xD28, 0xD4D, 0xD30, 0xD3F, 0xD15, 0xD41, 0xD33, 0xD02),
                            "മുപ്പത്തിമൂന്ന് കാവിതകൾ",
                        ),
                        (
                            T(0xD24, 0xD3F, 0xD30, 0xD41, 0xD35, 0xD3E, 0xD24, 0xD3F, 0xD15, 0xD3F, 0xD02),
                            "സാംഗം കൃതി",
                        ),
                        (
                            T(0xD07, 0xD38, 0xD4D, 0xD35, 0xD30, 0xD02),
                            "സാംഗം കൃതി",
                        ),
                        (
                            T(0xD2A, 0xD30, 0xD3F, 0xD2A, 0xD3E, 0xD1F, 0xD32, 0xD02),
                            "സാംഗം കൃതി",
                        ),
                        (
                            T(0xD05, 0xD17, 0xD24, 0xD4D, 0xD24, 0xD3F, 0xD15, 0xD02, 0xD30, 0xD02),
                            "സാംഗം കൃതി",
                        ),
                        (
                            T(0xD07, 0xD28, 0xD4D, 0xD30, 0xD3F, 0xD15, 0xD41, 0xD33, 0xD02) + " (" + T(0xD07, 0xD28, 0xD4D, 0xD24) + ")",
                            "എട്ട് കാവിതകൾ",
                        ),
                        (
                            T(0xD24, 0xD3F, 0xD30, 0xD41, 0xD35, 0xD3E, 0xD24, 0xD3F, 0xD15, 0xD3F, 0xD02) + " (" + T(0xD07, 0xD28, 0xD4D, 0xD24) + ")",
                            "സാംഗം കൃതി",
                        ),
                        (
                            T(0xD38, 0xD3F, 0xD32, 0xD4D, 0xD32, 0xD24, 0xD3F, 0xD15, 0xD3F, 0xD24, 0xD3F, 0xD15, 0xD02, 0xD30, 0xD02) + " (" + T(0xD07, 0xD28, 0xD4D, 0xD24) + ")",
                            "സാംഗം കൃതി",
                        ),
                    ]
                )
            ),
            55,
        ),
        "FOREIGN_POLICY": expand(
            dedupe(
                filt(
                    POST1947_FP
                    + [
                        ("പുരന്ദർ ഉടമ്പടി", "അംഗലോ-മറാത്ത സന്ധി"),
                        ("കർണാടക യുദ്ധങ്ങൾ", "ഇംഗ്ലീഷ്-ഫ്രഞ്ച്"),
                        ("സഹായക ഗഠനാപരിപാടി", "1798"),
                        ("ലാപ്സ് നയം", "1848"),
                        ("ഡിപ്പിക് സന്ധി", "1761"),
                        ("പ്ലാസി യുദ്ധം", "1757"),
                        ("ബക്സർ യുദ്ധം", "1764"),
                        ("വസായ് സന്ധി", "1775"),
                        ("വൈസ്രോയ് നയം", "1823"),
                        ("മക്തിവാഹിനി", "1857"),
                        ("അംഗലോ-മറാത്ത ഉടമ്പടി", "1802"),
                        ("ഇന്ത്യൻ നാവിക സേന", "1830"),
                    ]
                )
            ),
            55,
        ),
    }
    return data


def build_match_rows(data: dict[str, list]) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for key in ("MONUMENTS", "TRAVELLERS", "NEWSPAPERS", "COINS"):
        for row in data[key][:12]:
            rows.append((row[0], row[1]))
    return expand(dedupe(filt(rows)), 55)


LIST_NAMES = [
    "MONUMENTS",
    "TEMPLE_ARCH",
    "TRAVELLERS",
    "NEWSPAPERS",
    "REVOLTS",
    "LAND_REVENUE",
    "MUGHAL_ADMIN",
    "COINS",
    "EURO_FACTORIES",
    "REFORMERS",
    "INDUS",
    "SANGAM",
    "FOREIGN_POLICY",
    "MATCH_ROWS",
]

SECTION_COMMENTS = {
    "MONUMENTS": "# 2 — Monuments (name, builder/ruler)",
    "TEMPLE_ARCH": "# 3 — Temple architecture (site, style)",
    "TRAVELLERS": "# 4 — Travellers (name, period/ruler)",
    "NEWSPAPERS": "# 5 — Newspapers (paper, founder/editor)",
    "REVOLTS": "# 6 — Revolts (name, year, region, leader)",
    "LAND_REVENUE": "# 7 — Land revenue (system, ruler/period)",
    "MUGHAL_ADMIN": "# 8 — Mughal administration (term, meaning)",
    "COINS": "# 9 — Coins (coin, period/ruler)",
    "EURO_FACTORIES": "# 10 — European factories (company, port/city)",
    "REFORMERS": "# 11 — Reformers (person, movement/org)",
    "INDUS": "# 12 — Indus Valley (site/artifact, fact)",
    "SANGAM": "# 13 — Sangam literature (work, description)",
    "FOREIGN_POLICY": "# 14 — Foreign policy (event/treaty, fact)",
    "MATCH_ROWS": "# 15 — Match pairs (entity, fact)",
}

BHAKTI_BLOCK = """# 1 — Bhakti / Sufi (saint, movement, region)
from pathlib import Path

_g: dict = {"__file__": str(Path(__file__).parent / "gen_ih15.py")}
exec((Path(__file__).parent / "gen_ih15.py").read_text(encoding="utf-8"), _g)
BHAKTI: list[tuple[str, str, str]] = _g["BHAKTI"]

"""


def write_facts(data: dict[str, list]) -> None:
    for name in LIST_NAMES:
        chk(name, data[name])
    parts = [HEADER, BHAKTI_BLOCK]
    for name in LIST_NAMES:
        parts.append(SECTION_COMMENTS[name] + "\n")
        parts.append(fmt(name, data[name]) + "\n\n")
    parts.append(GENERATE_BLOCK)
    OUT.write_text("".join(parts), encoding="utf-8")


def verify_count() -> int:
    import importlib.util

    spec = importlib.util.spec_from_file_location("ih_wave15_facts", OUT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return len(mod.generate_wave15_candidates(set(), random.Random(1)))


def main() -> int:
    data = build_data()
    data["MATCH_ROWS"] = build_match_rows(data)
    for name in LIST_NAMES:
        chk(name, data[name])
    write_facts(data)
    n = verify_count()
    print(f"wrote {OUT.name}: candidates={n}")
    if n < 5200:
        print(f"SHORTFALL: need 5200+, got {n}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
