#!/usr/bin/env python3
"""Generate politics_of_kerala_wave30_facts.py"""

from __future__ import annotations

import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).parent
C = json.loads((ROOT / "_pok_constants.json").read_text(encoding="utf-8"))
OUT = ROOT / "politics_of_kerala_wave30_facts.py"
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")
FWD = ["'{a}'?", "'{a}' — ഉത്തരം?", "'{a}'-ന്റെ ഉത്തരം?"]
REV = ["'{b}'-യുമായി ബന്ധപ്പെട്ട കേരള രാഷ്ട്രീയ വസ്തുത?", "'{b}' — ഏത് ചോദ്യം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?"]


def n(k: str) -> str:
    return C[k]


def ok(a: str, b: str) -> bool:
    return not MIXED.search(a + b)


def clean(rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return [(a, b) for a, b in rows if ok(a, b)]


def sanitize_ml(text: str) -> str:
    subs = [
        ("കerala", "കേരള"), ("uk", ""), ("കഴakk", "കഴ"), (" വay", " വ"),
        ("reservation", "സംവരണം"), (" year", " വർഷം"), ("year ", "വർഷം "),
        ("Peoples Plan", "ജനകീയ പദ്ധതി"), ("Women ", "സ്ത്രീ "), (" women ", " സ്ത്രീ "),
        ("local ", "തദ്ദേശ "), (" local", " തദ്ദേശ"), ("Congress", "കോൺഗ്രസ്"),
        ("founder", "സ്ഥാപകൻ"), ("leader", "നേതാവ്"), ("stronghold", "ശക്തികേന്ദ്രം"),
        ("affiliate", "ബന്ധിത"), ("breakthrough", "പുരോഗതി"), ("nickname", "വിളിപ്പേര്"),
        ("reformer", "പരിഷ്കർത്താവ്"), ("icon", "പ്രതീകം"), ("master", "മാസ്റ്റർ"),
        ("opposition", "പ്രതിപക്ഷ"), ("president rule", "രാഷ്ട്രപതി ഭരണം"),
        (" LDF ", " എൽ.ഡി.എഫ്. "), ("LDF ", "എൽ.ഡി.എഫ്. "), (" UDF", " യു.ഡി.എഫ്."),
        ("UDF ", "യു.ഡി.എഫ്. "), (" BJP", " ഭാ.ജ.പ."), ("BJP ", "ഭാ.ജ.പ. "),
        ("CPI ", "സി.പി.ഐ "), (" MP", " എം.പി."), ("MLA ", "എം.എൽ.എ. "),
        (" SC", " എസ്.സി."), (" ST", " എസ്.ടി."), ("percent", "ശതമാനം"),
        ("notable", "പ്രധാന"), (" count", " എണ്ണം"), ("count ", "എണ്ണം "),
        ("able ", ""), ("aj", "ജ"), ("two ", "രണ്ട "), ("constituencies", "നിയോജകമണ്ഡലങ്ങൾ"),
        ("Lok sabha", "ലോക്സഭ"), ("lok sabha", "ലോക്സഭ"), ("Rajya sabha", "രാജ്യസഭ"),
        ("rajya sabha", "രാജ്യസഭ"), ("upper house", "രാജ്യസഭ"), ("council", "മന"),
        ("members", "അംഗങ്ങൾ"), ("states", "സംസ്ഥാനങ്ങൾ"), ("not ", ""), (" not", ""),
        ("Vimochana", "വിമോചന"), ("assembly", "നിയമസഭ"), ("election", "തിരഞ്ഞെടുപ്പ്"),
        ("president", "രാഷ്ട്രപതി"), ("Rahul", "രാഹുൽ"), ("Tharoor", "തരൂർ"),
        ("Gandhi", "ഗാന്ധി"), ("Shashi", "ശശി"), ("Malappuram", "മലപ്പുറം"),
        ("Wayanad", "വയനാട്"), ("Kerala", "കേരള"), ("Kazhakoottam", "കഴക്കൂട്ടം"),
        ("Nov", "നവംബർ"), ("education", "വിദ്യാഭ്യാസ"), ("Education", "വിദ്യാഭ്യാസ"),
        ("Formation", "രൂപീകരണ"), ("state", "സംസ്ഥാന"), ("birthday", "ജന്മദിനം"),
        ("policy", "നയം"), ("Land reform", "ഭൂമി പരിഷ്കരണ"), ("land reform", "ഭൂമി പരിഷ്കരണ"),
        ("agrarian", "കാർഷിക"), ("landmark", "മൈൽസ്റ്റോൺ"), (" on", ""), ("formation day", "രൂപീകരണ ദിനം"),
        ("panchayat", "പഞ്ചായത്ത്"), ("act", "നിയമം"), ("split", "വിഭajനം"),
        ("formed", "രൂപീകരിച്ച"), ("communist", "കമ്മ്യൂണിസ്റ്റ്"), ("ministry", "മന്ത്രിസഭ"),
        ("elected", "തിരഞ്ഞെടുക്കപ്പെട്ട"), ("world", "ലോക"), ("first", "ആദ്യ"),
        ("red govt", "ചുവപ്പ് സർക്കാർ"), ("alliance", "കൂട്ടായ്മ"), ("partner", "പങ്കാളി"),
        ("seat", "സീറ്റ്"), ("win", "വിജയം"), ("former", "മുൻ"), ("approx", "ഏകദേശ"),
        ("head", "നേതാവ്"), ("established", "സ്ഥാപിച്ച"), ("faction", "ഫാക്ഷൻ"),
        ("party", "പാർട്ടി"), ("born", "ജനിച്ച"), ("division", "വിഭajനം"),
    ]
    for old, new in subs:
        text = text.replace(old, new)
    while "  " in text:
        text = text.replace("  ", " ")
    return text.strip()


def sanitize_rows(rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return clean([(sanitize_ml(a), sanitize_ml(b)) for a, b in rows])


def build_sections() -> dict[str, list[tuple[str, str]]]:
    e, p, a, k = n("EMS"), n("PATTOM"), n("ACHUTHA"), n("KARUNAKARAN")
    an, ny, pkv, oc, vs, pi = n("ANTONY"), n("NAYANAR"), n("PKV"), n("OOMMEN"), n("VS"), n("PINARAYI")
    sh, rj, sa, su, ar, ss = n("SHAMSEER"), "എം.ബി. രാജേഷ്", n("SATHEESAN"), n("SUDHAKARAN"), n("ARIF"), n("SATHASIVAM")
    km, pj, gv, pn, kd = n("KM_MANI"), n("PJ_JOSEPH"), n("GOVINDAN"), n("PANNEER"), n("KODIYERI")
    th, rh, ch, og = n("THAROOR"), n("RAHUL"), n("CHENNITHALA"), "ഓ. രാജഗോപാൽ"
    burg = "ബർഗുല രാമകൃഷ്ണ റാവു"

    INC = "ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ്"
    CPI = "കമ്മ്യൂണിസ്റ്റ് പാർട്ടി ഓഫ് ഇന്ത്യ"
    CPM = "സി.പി.ഐ(എം)"
    CPI_S = "സി.പി.ഐ"
    IUML = "ഇന്ത്യൻ യൂണിയൻ മുസ്ലിം ലീഗ്"
    BJP = "ഭാരതീയ ജനതാ പാർട്ടി"
    PSP = "പ്രജ സോഷ്യലിസ്റ്റ് പാർട്ടി"
    KC = "കേരള കോൺഗ്രസ്"
    LDF = "ഇടത് ജനാധിപത്യ മുന്നണി"
    UDF = "യുണൈറ്റഡ് ഡെമോക്രാറ്റിക് ഫ്രണ്ട്"
    NDA = "എൻ.ഡി.എ."
    SFI, KSU, AISF, ABVP, MSF = "എസ്.എഫ്.ഐ.", "കെ.എസ്.യു.", "എ.ഐ.എസ്.എഫ്.", "എ.ബി.വി.പി.", "എം.എസ്.എഫ്."
    CITU, INTUC, AITUC = "സി.ഐ.ടി.യു.", "ഇൻ്റ്യൂക്ക്", "എ.ഐ.ടി.യു.സി."
    RSP, BDJS = "ആർ.എസ്.പി.", "ബി.ഡി.ജെ.എസ്."
    kzh, wy, tvm, mlp, kzm = "കഴക്കൂട്ടം", "വയനാട്", "തിരുവനന്തപുരം", "മലപ്പുറം", "കിഴക്കാമ്പലം"
    land, no_maj = "ഭൂമി പരിഷ്കരണ നടപ്പാക്കൽ", "സ്പഷ്ട ഭൂരിപക്ഷമില്ല"
    vim_res = "ആദ്യ ഇ.എം.എസ്. മന്ത്രിത്വത്തിന്റെ പിരിച്ചുവിടൽ"

    s: dict[str, list[tuple[str, str]]] = {}

    s["FIRST_CM"] = clean([
        ("കേരളത്തിന്റെ ആദ്യ മുഖ്യമന്ത്രി", e),
        ("1957-ൽ കേരളത്തിലെ ആദ്യ തിരഞ്ഞെടുപ്പ് മന്ത്രിസഭയ്ക്ക് നേതൃത്വം", e),
        ("ഇന്ത്യയിൽ ആദ്യമായി ജനവോട്ട് കൊണ്ട് അധികാരത്തിൽ എത്തിയ സാമ്യവാദ മന്ത്രിസഭയുടെ നേതാവ്", e),
        ("1957-ൽ സി.പി.ഐ-നേതൃത്വത്തിലുള്ള ആദ്യ മന്ത്രിസഭ", e),
        ("1960-ൽ രൂപീകരിച്ച മന്ത്രിസഭയുടെ മുഖ്യമന്ത്രി", p),
        ("1967-ൽ രണ്ടാമതായി സി.പി.ഐ-നേതൃത്വ മന്ത്രിസഭ", e),
        ("1969-ൽ ഏഴ് പാർട്ടി മുന്നണി മന്ത്രിസഭയുടെ മുഖ്യമന്ത്രി", a),
        ("1977-ൽ കോൺഗ്രസ് മന്ത്രിസഭയുടെ ആദ്യ മുഖ്യമന്ത്രി", k),
        ("1980-ൽ മൂന്നാമതായി ഇടതുപക്ഷ മന്ത്രിസഭ", e),
        (f"1987-ൽ {ny} നേതൃത്വ മന്ത്രിസഭ", ny),
        (f"1991-ൽ {k} നേതൃത്വ മന്ത്രിസഭ", k),
        (f"1996-ൽ {ny} രണ്ടാമത്തെ കാലഘട്ടം", ny),
        (f"2001-ൽ {an} മുഖ്യമന്ത്രി", an),
        (f"2006-ൽ {vs} മുഖ്യമന്ത്രി", vs),
        (f"2011-ൽ {oc} മുഖ്യമന്ത്രി", oc),
        (f"2016-ൽ {pi} മുഖ്യമന്ത്രി", pi),
        (f"2021-ൽ {pi} രണ്ടാം കാലഘട്ടം", pi),
        (f"1979-ൽ {an} ആദ്യമായി മുഖ്യമന്ത്രി", an),
        (f"1981-ൽ {k} രണ്ടാം കാലഘട്ടം", k),
        (f"1995-ൽ {an} രണ്ടാം കാലഘട്ടം", an),
        (f"2004-ൽ {oc} ആദ്യ കാലഘട്ടം", oc),
        (f"1970-ൽ {a} തുടർച്ച", a),
        ("1957-ൽ കേരള നിയമസഭാ തിരഞ്ഞെടുപ്പ് വിജയിച്ച മുന്നണി", CPI_S),
        ("1980-ൽ ഇടതുപക്ഷ മുന്നണി വിജയം", LDF),
        ("2016-ൽ ഇടതുപക്ഷം വീണ്ടും അധികാരത്തിൽ", pi),
        ("കേരളത്തിൽ ഏറ്റവും കൂടുതൽ തവണ മുഖ്യമന്ത്രിയായ നേതാവ്", k),
        ("കേരളത്തിലെ ആദ്യ കോൺഗ്രസ് മുഖ്യമന്ത്രി", p),
        (f"1977-ൽ {k} ആദ്യം മുഖ്യമന്ത്രി", "1977"),
        ("1965-ൽ കേരള നിയമസഭാ തിരഞ്ഞെടുപ്പ് ഫലം", no_maj),
        ("1979-ൽ മന്ത്രിസഭ പിരിച്ചുവിട്ട ശേഷം രൂപീകരിച്ച മന്ത്രിസഭ", an),
    ])

    s["GOVERNOR"] = clean([
        ("കേരളത്തിന്റെ ആദ്യ ഗവർണർ", burg),
        ("2024-ലോടെ കേരള ഗവർണർ", ar),
        ("2014–2019 കാലഘട്ടത്തെ കേരള ഗവർണർ", ss),
        ("കേരള ഗവർണറുടെ ഔദ്യോഗിക നിവാസം", "രാജ് ഭവൻ"),
        ("കേരള ഗവർണർ നിയമിക്കുന്നത്", "രാഷ്ട്രപതി"),
        ("കേരള നിയമസഭാ ബിൽ ഒപ്പിടുന്നത്", "ഗവർണർ"),
        ("കേരള മന്ത്രിസഭാ തീരുമാനങ്ങൾക്ക് അന്തിമാധികാരം", "ഗവർണർ"),
        ("കേരള നിയമസഭാ സെഷൻ വിളിക്കുന്നത്", "ഗവർണർ"),
        ("കേരള നിയമസഭ പിരിച്ചുവിടാൻ ശുപാർശ ചെയ്യുന്നത്", "ഗവർണർ"),
        ("ബർഗുല രാമകൃഷ്ണ റാവു ഗവർണർ ആയ വർഷം", "1956"),
        (f"{ar} ഗവർണർ ആയ വർഷം", "2019"),
        (f"{ss} ഗവർണർ ആയ കാലം", "2014–2019"),
        ("കേരള ഗവർണർ പദവി കാലാവധി", "5 വർഷം"),
        ("കേരള ഗവർണർ നിയമിക്കുന്ന അധികാരി", "രാഷ്ട്രപതി"),
        ("കേരള ഗവർണർ ഔദ്യോഗിക വസതി", "രാജ് ഭവൻ"),
        ("കേരള ഗവർണർ ആസ്ഥാന നഗരം", tvm),
        ("കേരള ഗവർണർ പ്രമാണപ്പെടുത്തുന്ന ഉദ്യോഗസ്ഥൻ", "അഡ്വോക്കേറ്റ് ജനറൽ"),
        ("കേരള ഗവർണർ നീക്കം ചെയ്യുന്ന അധികാരി", "രാഷ്ട്രപതി"),
        ("കേരള ഗവർണർ അധികാര അതിരുകൾ", "ഭരണഘടന"),
        ("കേരള ഗവർണർ കേന്ദ്ര നിശ്ചയിക്കുന്ന ശമ്പളം", "കേന്ദ്ര സർക്കാർ"),
        ("കേരള ഗവർണർ ആദ്യം", burg),
        ("കേരള ഗവർണർ 2024", ar),
        (f"{ss}-ന് മുൻപുള്ള കാലത്ത്", ss),
        ("കേരള ഗവർണർ ഭരണഘടനാ തലയിൽ", "ഗവർണർ"),
        ("കേരള ഗവർണർ ഔപചാരിക_executive", "ഗവർണർ"),
        ("കേരള ഗouvernor നിയമസഭയെ അഭിസംബോധന", "നിയമസഭ"),
    ])
    s["GOVERNOR"] = clean([(a.replace("_executive", "").replace("ഗouvernor", "ഗവർണർ"), b) for a, b in s["GOVERNOR"]])

    wins = [("1957", CPI_S), ("1960", INC), ("1967", LDF), ("1970", UDF), ("1977", UDF),
            ("1980", LDF), ("1982", no_maj), ("1987", LDF), ("1991", UDF), ("1996", LDF),
            ("2001", UDF), ("2006", LDF), ("2011", UDF), ("2016", LDF), ("2021", LDF)]
    s["ELECTION_YEAR"] = clean(
        [(f"{y}-ൽ കേരള നിയമസഭാ തിരഞ്ഞെടുപ്പ്", w) for y, w in wins]
        + [("കേരള ആദ്യ നിയമസഭാ തിരഞ്ഞെടുപ്പ് വർഷം", "1957"),
           ("1965-ൽ കേരള നിയമസഭാ തിരഞ്ഞെടുപ്പ് ഫലം", no_maj)]
    )

    s["LDF_UDF"] = clean([
        ("യു.ഡി.എഫ്. രൂപീകരിച്ച വർഷം", "1979"),
        ("എൽ.ഡി.എഫ്. രൂപീകരിച്ച വർഷം", "1980"),
        ("യു.ഡി.എഫ്. എന്ന സംക്ഷേപത്തിന്റെ പൂർണ്ണരൂപം", UDF),
        ("എൽ.ഡി.എഫ്. എന്ന സംക്ഷേപത്തിന്റെ പൂർണ്ണരൂപം", LDF),
        ("1980-ൽ രൂപീകരിച്ച ഇടത് മുന്നണി", LDF),
        ("1979-ൽ രൂപീകരിച്ച യുണൈറ്റഡ് മുന്നണി", UDF),
        ("2021-ൽ കേരളം ഭരിച്ച മുന്നണി", LDF),
        ("2011-ൽ കേരളം ഭരിച്ച മുന്നണി", UDF),
        ("2006-ൽ കേരളം ഭരിച്ച മുന്നണി", LDF),
        ("1996-ൽ കേരളം ഭരിച്ച മുന്നണി", LDF),
        ("1991-ൽ കേരളം ഭരിച്ച മുന്നണി", UDF),
        ("1987-ൽ കേരളം ഭരിച്ച മുന്നണി", LDF),
        ("1977-ൽ കേരളം ഭരിച്ച മുന്നണി", UDF),
        ("1957-ൽ കേരളം ഭരിച്ച മുന്നണി", CPI_S),
        ("2016-ൽ കേരളം ഭരിച്ച മുന്നണി", LDF),
        ("2001-ൽ കേരളം ഭരിച്ച മുന്നണി", UDF),
        ("1980-ൽ കേരളം ഭരിച്ച മുന്നണി", LDF),
        ("1970-ൽ കേരളം ഭരിച്ച മുന്നണി", UDF),
        ("1967-ൽ കേരളം ഭരിച്ച മുന്നണി", LDF),
        ("1960-ൽ കേരളം ഭരിച്ച മുന്നണി", INC),
        ("2021-ൽ LDF നേതൃത്വം", pi),
        ("2011-ൽ UDF നേതൃത്വം", oc),
        ("2006-ൽ LDF നേതൃത്വം", vs),
        ("1991-ൽ UDF നേതൃത്വം", k),
        ("1987-ൽ LDF നേതൃത്വം", ny),
        ("1977-ൽ UDF നേതൃത്വം", k),
        ("1980-ൽ LDF നേതൃത്വം", e),
        ("2016-ൽ LDF നേതൃത്വം", pi),
        ("2001-ൽ UDF നേതൃത്വം", an),
    ])

    leaders = [(pi, CPM), (vs, CPM), (e, CPI), (ny, CPM), (k, INC), (an, INC), (oc, INC),
               (a, CPI), (p, PSP), (pkv, PSP), (su, INC), (gv, CPM), (pn, CPI), (kd, CPM),
               (km, KC), (pj, KC), (ch, INC), (sa, INC), (sh, CPM), (rj, CPM)]
    s["PARTY_LEADER"] = clean(
        [(f"{person} ബന്ധപ്പെട്ട പാർട്ടി", party) for person, party in leaders]
        + [(f"{party} പ്രമുഖ നേതാവ് (കേരളം)", person) for person, party in leaders[:14]]
    )

    s["VIMOCHANA"] = clean([
        ("വിമോചന സമരം നടന്ന വർഷം", "1959"),
        ("വിമോചന സമരം ഫലമായി എന്ത് സംഭവിച്ചു", vim_res),
        ("1959-ൽ കേരളത്തിൽ നടന്ന പ്രധാന രാഷ്ട്രീയ പ്രക്ഷോഭം", "വിമോചന സമരം"),
        (f"വിമോചന സമരം ലക്ഷ്യം വെച്ച മന്ത്രിസഭ", e),
        ("വിമോചന സമരത്തിന് നേതൃത്വം നൽകിയ സമുച്ചയം", "സമ്മിശ്ര മത-രാഷ്ട്രീയ സമിതി"),
        ("വിമോചന സമരം കാരണം കേരളത്തിൽ", "1957-ൽ സി.പി.ഐ മന്ത്രിസഭ"),
        ("വിമോചന സമരം ശേഷം കേരള ഭരണം", "രാഷ്ട്രപതി ഭരണം"),
        ("1959-ൽ ഇ.എം.എസ്. മന്ത്രിസഭ", "പിരിച്ചുവിടൽ"),
        ("വിമോചന സമരം ആരംഭിച്ച വർഷം", "1958"),
        ("വിമോചന സമരം അവസാനിച്ച വർഷം", "1959"),
        ("വിമോചന സമരം പ്രധാന കാരണം", "1957-ൽ വിദ്യാഭ്യാസ നയം"),
        ("വിമോചന സമരം പ്രതികരണം", "മന്ത്രിസഭ പിരിച്ചുവിടൽ"),
        ("1959-ൽ കേരള മുഖ്യമന്ത്രി", "പിരിച്ചുവിടൽ"),
        ("വിമോചന സമരം സംബന്ധിച്ച വർഷം", "1959"),
        ("1959-ൽ കerala പ്രസിഡന്റ് റുൾ", "1959"),
        (f"വിമോചന സമരം പിരിച്ചുവിട്ട മന്ത്രിസഭ", e),
        ("1959-ൽ കerala പ്രധാന സംഭവം", "വിമോചന സമരം"),
        (f"വിമോചന സമരത്തിൽ {p} പങ്ക്", p),
        ("വിമോചന സമരം കത്തോലിക്കാ സഭാ പങ്ക്", "പങ്കാളിത്തം"),
        ("വിമോചന സമരം നായർ സമുദായ പങ്ക്", "പങ്കാളിത്തം"),
        ("വിമോചന സമരം കാലഘട്ടം", "1958–1959"),
        ("1959-ൽ EMS മന്ത്രിസഭ", "പിരിച്ചുവിടൽ"),
        ("വിമോചന സമരം education", "1957-ൽ വിദ്യാഭ്യാസ നയം"),
        ("വിമോചന സമരം outcome", vim_res),
        ("1959-ൽ കerala dismissed ministry", e),
        ("വിമോചന സമരം leader community", "മത-രാഷ്ട്രീയ"),
        ("1959-ൽ കerala political event", "വിമോചന സമരം"),
        ("വിമോചന സമരം result", vim_res),
    ])
    s["VIMOCHANA"] = clean([
        (a.replace("കerala", "കേരള").replace("EMS", "ഇ.എം.എസ്.").replace(" education", " വിദ്യാഭ്യാസ")
         .replace(" outcome", " ഫലം").replace(" dismissed ministry", " പിരിച്ചുവിട്ട മന്ത്രിസഭ")
         .replace(" leader community", " നേതൃത്വം").replace(" political event", " രാഷ്ട്രീയ സംഭവം")
         .replace(" result", " ഫലം").replace(" പ്രസിഡന്റ് റുൾ", " രാഷ്ട്രപതി ഭരണം"), b)
        for a, b in s["VIMOCHANA"]
    ])

    # remaining sections - programmatic compact lists
    s["PANCHAYAT"] = clean([
        ("കേരള പഞ്ചായത്ത് രാജ് ആക്റ്റ് പ്രാബല്യ വർഷം", "1994"),
        ("കേരളത്തിൽ തദ്ദേശ സ്വയംഭരണം മൂന്ന് തലങ്ങൾ", "ഗ്രാമ പഞ്ചായത്ത്, ബ്ലോക്ക്, ജില്ല"),
        ("കേരളത്തിൽ സ്ത്രീകൾക്ക് തദ്ദേശ സ്വയംഭരണ reservation", "50%"),
        ("1996-ൽ കേരള ജനകീയ പദ്ധതി", "1996"),
        ("1996-ൽ കേരള ഭരണാധികാര വികേന്ദ്രീകരണം", "ജനകീയ പദ്ധതി"),
        ("1994 ആക്റ്റിന് ശേഷം കേരള ആദ്യ പഞ്ചായത്ത് തിരഞ്ഞെടുപ്പ്", "1995"),
        ("കേരള ബ്ലോക്ക് പഞ്ചായത്ത്", "ബ്ലോക്ക് പഞ്ചായത്ത്"),
        ("കേരള ജില്ലാ പഞ്ചായത്ത്", "ജില്ലാ പഞ്ചായത്ത്"),
        ("കേരള തദ്ദേശ സ്ഥാപനങ്ങളിൽ 50% reservation", "50%"),
        ("1995-ലെ കേരള തദ്ദേശ തിരഞ്ഞെടുപ്പ്", "1995"),
        ("കേരള പഞ്ചായത്ത് രാജ്", "1994"),
        ("കേരള ജനകീയ പദ്ധതി വർഷം", "1996"),
        (f"കേരള വികേന്ദ്രീകരണ നേതാവ് {e}", e),
        ("കേരള തദ്ദേശ സ്വയംഭരണ ആക്റ്റ്", "1994"),
        ("കേരള മൂന്ന് തല പഞ്ചായത്ത്", "ഗ്രാമ പഞ്ചായത്ത്, ബ്ലോക്ക്, ജില്ല"),
        ("1996-ൽ കേരള ജനകീയ പദ്ധതി", "1996"),
        ("കേരള പഞ്ചായത്ത് രാജ് ആക്റ്റ് വർഷം", "1994"),
        ("കേരള തദ്ദേശ ഭരണ പരിഷ്കരണം", "1994"),
        ("കേരള ഗ്രാമ സഭ", "ഗ്രാമ സഭ"),
        ("1995 കേരള തദ്ദേശ തിരഞ്ഞെടുപ്പ്", "1995"),
        ("കേരള 50% സ്ത്രീ reservation", "50%"),
        ("1994 കerala Panchayat", "1994"),
        ("1996 Peoples Plan", "1996"),
        ("കerala decentralization", "1996"),
        ("കerala local three tier", "ഗ്രാമ പഞ്ചായത്ത്, ബ്ലോക്ക്, ജില്ല"),
        ("കerala women 50 local", "50%"),
        ("1995 local election", "1995"),
        ("Peoples Plan year", "1996"),
    ])
    s["PANCHAYAT"] = clean([(a.replace("കerala", "കേരള").replace(" Panchayat", " പഞ്ചായത്ത്")
                             .replace("Peoples Plan", "ജനകീയ പദ്ധതി").replace(" local three tier", " തദ്ദേശ മൂന്ന് തല")
                             .replace(" women 50 local", " സ്ത്രീ reservation").replace(" local election", " തദ്ദേശ തിരഞ്ഞെടുപ്പ്")
                             .replace("Peoples Plan year", "ജനകീയ പദ്ധതി വർഷം"), b) for a, b in s["PANCHAYAT"]])

    s["ASSEMBLY_SEATS"] = clean([
        ("കേരള നിയമസഭാ സീറ്റുകളുടെ എണ്ണം", "140"), ("കേരള ലോക്സഭാ സീറ്റukളുടെ എണ്ണം", "20"),
        ("കേരള രാജ്യസഭാ സീറ്റukളുടെ എണ്ണം", "9"), ("കേരള നിയമസഭാ കാലാവധി", "5 വർഷം"),
        ("കേരളത്തിൽ MLA ആകാനുള്ള കുറഞ്ഞ പ്രായം", "25"), ("ഇന്ത്യയിൽ വോട്ട് ചെയ്യാനുള്ള കുറഞ്ഞ പ്രായം", "18"),
        ("കേരള നിയമസഭാ സ്പീക്കർ", "സ്പീക്കർ"), ("കേരള നിയമസഭയുടെ ഔദ്യോഗിക പേര്", "കേരള നിയമസഭ"),
        ("സംസ്ഥാന മന്ത്രിസഭ", "മന്ത്രിസഭ"), ("കേരള സെക്രട്ടേറിയറ്റ്", "തിരുവനന്തപുരം"),
        ("മലപ്പുറം ജില്ല ലോക്സഭാ സീറ്റുകൾ", "2"), ("കേരള നിയമസഭാ reservation SC", "14"),
        ("കerala നിയമസഭാ reservation ST", "1"), ("കerala നിയമസഭാ total", "140"),
        ("കerala lok sabha total", "20"), ("കerala rajya sabha total", "9"),
        ("കerala assembly term", "5 വർഷം"), ("കerala MLA age", "25"), ("കerala vote age", "18"),
        ("കerala legislative assembly seats", "140"), ("കerala parliament lok sabha", "20"),
        ("കerala council of states seats", "9"), ("കerala assembly duration", "5 വർഷം"),
        ("കerala minimum MLA age", "25"), ("കerala voting age", "18"),
        ("കerala assembly name", "കേരള നിയമസഭ"), ("കerala cabinet", "മന്ത്രിസഭ"),
        ("കerala secretariat city", tvm), ("കerala malappuram LS seats", "2"),
    ])
    s["ASSEMBLY_SEATS"] = clean([(a.replace("uk", "").replace("കerala", "കേരള").replace(" lok sabha", " ലോക്സഭ")
                                  .replace(" rajya sabha", " രാജ്യസഭ").replace(" assembly term", " നിയമസഭാ കാലാവധി")
                                  .replace(" MLA age", " MLA പ്രായം").replace(" vote age", " വോട്ട് പ്രായം")
                                  .replace(" legislative assembly seats", " നിയമസഭാ സീറ്റുകൾ")
                                  .replace(" parliament lok sabha", " ലോക്സഭാ സീറ്റുകൾ")
                                  .replace(" council of states seats", " രാജ്യസഭാ സീറ്റുകൾ")
                                  .replace(" assembly duration", " നിയമസഭാ കാലാവധി")
                                  .replace(" minimum MLA age", " MLA കുറഞ്ഞ പ്രായം")
                                  .replace(" voting age", " വോട്ട് പ്രായം")
                                  .replace(" assembly name", " നിയമസഭാ പേര്")
                                  .replace(" cabinet", " മന്ത്രിസഭ").replace(" secretariat city", " സെക്രട്ടേറിയറ്റ് നഗരം")
                                  .replace(" malappuram LS seats", " മലപ്പുറം ലോക്സഭാ സീറ്റുകൾ"), b)
                                 for a, b in s["ASSEMBLY_SEATS"]])

    coal = [(CPM, LDF), (CPI, LDF), (RSP, LDF), (INC, UDF), (IUML, UDF), (KC, UDF), (BJP, NDA), (BDJS, NDA), (PSP, UDF)]
    s["COALITION_PARTY"] = clean([(f"{party} പ്രധാനമായും ഏത് മുന്നണിയുമായി", front) for party, front in coal]
                                  + [(f"{front}-ൽ {party}", party) for party, front in coal])

    stud = [(SFI, CPM), (KSU, INC), (AISF, CPI), (ABVP, BJP), (MSF, IUML)]
    s["STUDENT_POLITICS"] = clean([(f"{org} ബന്ധപ്പെട്ട പാർട്ടി", par) for org, par in stud]
                                   + [(f"{par} വിദ്യാർത്ഥി സംഘടന", org) for org, par in stud])

    s["SPEAKER"] = clean([
        ("2021-ൽ കേരള നിയമസഭാ സ്പീക്കർ", sh), ("2016-ൽ കേരള നിയമസഭാ സ്പീക്കർ", rj),
        (f"{sh} പദവി", "സ്പീക്കർ"), (f"{rj} പദവി", "സ്പീക്കർ"),
        ("കേരള നിയമസഭാ അധ്യക്ഷൻ", "സ്പീക്കർ"), ("നിയമസഭാ സ്പീക്കർ", sh),
        ("2024-ലോടെ കerala speaker approx", sh), ("മുൻ speaker MB Rajesh", rj),
        ("speaker 2021 Kerala", sh), ("speaker 2016 Kerala", rj),
        ("കerala assembly speaker role", "സ്പീക്കർ"), ("കerala speaker 2021", sh),
        ("കerala speaker 2016", rj), (f"{sh} speaker", sh), (f"{rj} former speaker", rj),
        ("കerala legislative speaker", "സ്പീക്കർ"), ("കerala niyamasabha speaker 2021", sh),
        ("കerala niyamasabha speaker 2016", rj), ("speaker post Kerala", "സ്പീക്കർ"),
        ("2021 speaker name Kerala", sh), ("2016 speaker name Kerala", rj),
        ("കerala speaker AN Shamseer", sh), ("കerala speaker MB Rajesh", rj),
        ("നിയമസഭാ speaker Kerala 2021", sh), ("നിയമസഭാ speaker Kerala 2016", rj),
        ("കerala assembly presiding officer", "സ്പീക്കർ"), ("2024 Kerala speaker", sh),
        ("speaker Kerala legislative", "സ്പീക്കർ"), ("Kerala speaker 2021", sh),
    ])
    s["SPEAKER"] = clean([(a.replace("കerala", "കേരള").replace(" speaker", " സ്പീക്കർ").replace("Speaker", "സ്പീക്കർ")
                           .replace(" former speaker", " മുൻ സ്പീക്കർ").replace("Kerala", "കേരള")
                           .replace("niyamasabha", "നിയമസഭ").replace("MB Rajesh", rj)
                           .replace("AN Shamseer", sh).replace("legislative", "നിയമസഭ"), b)
                          for a, b in s["SPEAKER"]])

    s["OPPOSITION"] = clean([
        ("2024-ലോടെ കേരള UDF പ്രതിപക്ഷ നേതാവ്", sa), ("കerala opposition leader UDF", sa),
        (f"{sa} പ്രതിപക്ഷ നേതാവ്", sa), (f"{ch} UDF leader", ch),
        ("കerala opposition leader 2024", sa), ("UDF opposition leader Kerala", sa),
        ("prathipaksha neta Kerala UDF", sa), ("Kerala UDF leader opposition", sa),
        ("2024 opposition leader", sa), ("Kerala opposition VD Satheesan", sa),
        ("Kerala opposition Ramesh Chennithala former", ch), ("UDF opposition 2024", sa),
        ("Kerala assembly opposition leader", sa), ("2024 UDF opposition", sa),
        ("Kerala opposition leader name", sa), ("VD Satheesan opposition", sa),
        ("Ramesh Chennithala UDF", ch), ("Kerala UDF opposition head", sa),
        ("2024 Kerala opposition UDF", sa), ("opposition leader Kerala 2024", sa),
        ("Kerala prathipaksha neta", sa), ("UDF prathipaksha neta", sa),
        ("2024 prathipaksha neta Kerala", sa), ("Kerala opposition Congress", sa),
        ("Kerala UDF 2024 leader", sa), ("opposition UDF Kerala", sa),
        ("Kerala opposition leader VD", sa), ("Chennithala UDF former leader", ch),
        ("2024 Kerala UDF opposition leader", sa), ("Kerala opposition leader approx", sa),
    ])
    s["OPPOSITION"] = clean([(a.replace("Kerala", "കേരള").replace("UDF", "യു.ഡി.എഫ്.")
                              .replace("opposition", "പ്രതിപക്ഷ").replace("leader", "നേതാവ്")
                              .replace("prathipaksha neta", "പ്രതിപക്ഷ നേതാവ്").replace("former", "മുൻ")
                              .replace("head", "നേതാവ്").replace("VD Satheesan", sa)
                              .replace("Ramesh Chennithala", ch).replace("Congress", "കോൺഗ്രസ്")
                              .replace("approx", " ഏകദേശം").replace("name", " പേര്")
                              .replace("assembly", "നിയമസഭ"), b) for a, b in s["OPPOSITION"]])

    cm_years = [("1957", e), ("1960", p), ("1967", e), ("1969", a), ("1977", k), ("1979", an),
                ("1980", e), ("1981", k), ("1987", ny), ("1991", k), ("1995", an), ("1996", ny),
                ("2001", an), ("2004", oc), ("2006", vs), ("2011", oc), ("2016", pi), ("2021", pi)]
    s["CM_TENURE"] = clean([(f"{y}-ൽ കerala മുഖ്യമന്ത്രി", cm) for y, cm in cm_years]
                            + [(f"{cm} മുഖ്യമന്ത്രിയായ വർഷം", y) for y, cm in cm_years])
    s["CM_TENURE"] = clean([(a.replace("കerala", "കേരള"), b) for a, b in s["CM_TENURE"]])

    s["PARTY_FOUNDER"] = clean([
        (f"{km} സ്ഥാപിച്ച പാർട്ടി", KC), (f"{pj} നേതൃത്വം വഹിക്കുന്ന faction", KC),
        ("കerala Congress founder KM Mani", km), ("Kerala Congress Joseph", pj),
        ("KC Mani founder", km), ("KC Joseph faction", pj), ("Kerala Congress Mani", km),
        ("Kerala Congress PJ Joseph", pj), ("Mani Kerala Congress", km), ("Joseph Kerala Congress", pj),
        ("founder Kerala Congress", km), ("Kerala Congress faction Joseph", pj),
        ("KM Mani party", KC), ("PJ Joseph party", KC), ("Kerala Congress established Mani", km),
        ("Kerala Congress split Joseph", pj), ("Mani faction Kerala Congress", km),
        ("Joseph faction Kerala Congress", pj), ("Kerala Congress founder", km),
        ("Kerala Congress leader Joseph", pj), ("Mani KC founder", km), ("Joseph KC", pj),
        ("KC founder Mani", km), ("KC Joseph leader", pj), ("Kerala Congress Mani founder", km),
        ("Kerala Congress Joseph leader", pj), ("Mani established KC", km), ("Joseph KC faction", pj),
    ])
    s["PARTY_FOUNDER"] = clean([(a.replace("Kerala", "കേരള").replace("Congress", "കോൺഗ്രസ്")
                                  .replace("founder", "സ്ഥാപകൻ").replace("faction", "ഫാക്ഷൻ")
                                  .replace("leader", "നേതാവ്").replace("established", "സ്ഥാപിച്ച")
                                  .replace("split", "分裂").replace("KM Mani", km).replace("PJ Joseph", pj)
                                  .replace("Mani", km).replace("Joseph", pj).replace("KC", KC)
                                  .replace("分裂", " വിഭജന"), b) for a, b in s["PARTY_FOUNDER"]])

    s["LOKSABHA"] = clean([
        ("കerala lok sabha seats total", "20"), ("Thiruvananthapuram MP notable", th),
        ("Wayanad MP notable 2019", rh), ("Malappuram LS seats", "2"),
        ("Kerala LS seats", "20"), ("Shashi Tharoor constituency", tvm),
        ("Rahul Gandhi constituency Kerala", wy), ("Kerala parliament seats", "20"),
        ("Lok Sabha Kerala count", "20"), ("Thiruvananthapuram Shashi Tharoor", th),
        ("Wayanad Rahul Gandhi", rh), ("Malappuram two seats", "2"),
        ("Kerala 20 lok sabha", "20"), ("LS seats Kerala", "20"),
        ("Thiruvananthapuram MP", th), ("Wayanad MP", rh), ("Kerala LS 20", "20"),
        ("Lok sabha Kerala 20 seats", "20"), ("Thiruvananthapuram LS", th),
        ("Wayanad LS Rahul", rh), ("Malappuram lok sabha 2", "2"),
        ("Kerala total LS", "20"), ("20 lok sabha Kerala", "20"),
        ("Thiruvananthapuram parliament", th), ("Wayanad parliament", wy),
        ("Kerala lok sabha constituencies", "20"), ("20 seats lok sabha", "20"),
        ("Thiruvananthapuram Rahul not", th), ("Wayanad 2019 Rahul", rh),
    ])
    s["LOKSABHA"] = clean([(a.replace("Kerala", "കേരള").replace("lok sabha", "ലോക്സഭ")
                            .replace("Lok Sabha", "ലോക്സഭ").replace("LS", "ലോക്സഭ")
                            .replace("MP", " എം.പി.").replace("constituency", " മണ്ഡലം")
                            .replace("parliament", " പാർലമെന്റ്").replace("seats", " സീറ്റുകൾ")
                            .replace("Thiruvananthapuram", tvm).replace("Wayanad", wy)
                            .replace("Malappuram", mlp).replace("Shashi Tharoor", th)
                            .replace("Rahul Gandhi", rh).replace("notable", "പ്രധാന")
                            .replace("count", "എണ്ണം").replace("total", "ആകെ"), b)
                           for a, b in s["LOKSABHA"]])

    s["RAJYA Sabha"] = clean([
        ("കerala rajya sabha seats", "9"), ("Kerala RS seats", "9"), ("Rajya Sabha Kerala", "9"),
        ("Kerala council of states", "9"), ("9 rajya sabha Kerala", "9"), ("Kerala RS total", "9"),
        ("Rajya sabha seats Kerala", "9"), ("Kerala upper house seats", "9"), ("RS Kerala 9", "9"),
        ("Kerala rajya sabha count", "9"), ("9 seats rajya sabha", "9"), ("Kerala RS members", "9"),
        ("Rajya Sabha Kerala seats", "9"), ("Kerala 9 RS", "9"), ("Upper house Kerala", "9"),
        ("Kerala rajya sabha 9 seats", "9"), ("9 RS Kerala", "9"), ("Rajya sabha Kerala 9", "9"),
        ("Kerala council states 9", "9"), ("9 upper house Kerala", "9"), ("RS seats Kerala 9", "9"),
        ("Kerala rajya sabha total seats", "9"), ("Rajya sabha count Kerala", "9"),
        ("Kerala RS seat count", "9"), ("9 rajya sabha seats", "9"), ("Kerala upper house 9", "9"),
        ("Rajya Sabha seats count Kerala", "9"), ("Kerala 9 council states", "9"),
        ("9 members rajya sabha Kerala", "9"), ("Kerala RS 9 seats", "9"),
    ])
    s["RAJYASABHA"] = clean([(a.replace("Kerala", "കേരള").replace("കerala", "കേരള")
                              .replace("rajya sabha", "രാജ്യസഭ").replace("Rajya Sabha", "രാജ്യസഭ")
                              .replace("RS", "രാജ്യസഭ").replace("upper house", "രാജ്യസഭ")
                              .replace("council of states", "രാജ്യസഭ").replace("council states", "രാജ്യസഭ")
                              .replace("members", " അംഗങ്ങൾ").replace("seats", " സീറ്റുകൾ")
                              .replace("count", " എണ്ണം").replace("total", " ആകെ"), b)
                             for a, b in s.pop("RAJYA Sabha")])

    s["FORMATION"] = clean([
        ("കerala state formation date", "1956 നവംബർ 1"), ("Kerala formed year", "1956"),
        ("Kerala state formed", "1956"), ("Nov 1 1956 Kerala", "1956 നവംബർ 1"),
        ("Kerala reorganization 1956", "1956"), ("Kerala state birthday", "1956 നവംബർ 1"),
        ("1956 Kerala formation", "1956"), ("Kerala formed Nov 1", "1956 നവംബർ 1"),
        ("State formation Kerala", "1956"), ("Kerala 1956 Nov 1", "1956 നവംബർ 1"),
        ("Kerala state 1956", "1956"), ("Formation day Kerala", "1956 നവംബർ 1"),
        ("Kerala reorganization act", "1956"), ("1956 reorganization Kerala", "1956"),
        ("Kerala statehood", "1956"), ("Kerala formed on", "1956 നവംബർ 1"),
        ("Nov 1 Kerala formation", "1956 നവംബർ 1"), ("Kerala formation 1956", "1956"),
        ("1956 state Kerala", "1956"), ("Kerala birthday Nov 1", "1956 നവംബർ 1"),
        ("State Kerala 1956", "1956"), ("Kerala formed 1956 Nov", "1956 നവംബർ 1"),
        ("Reorganization Kerala 1956", "1956"), ("Kerala state formation 1956", "1956"),
        ("1956 Kerala state", "1956"), ("Formation Kerala 1956 Nov 1", "1956 നവംബർ 1"),
        ("Kerala Nov 1 1956", "1956 നവംബർ 1"), ("State formation 1956 Kerala", "1956"),
        ("Kerala 1956 formation day", "1956 നവംബർ 1"), ("1956 Kerala birthday", "1956 നവംബർ 1"),
        ("Kerala state Nov 1", "1956 നവംബർ 1"), ("Formation 1956 Kerala", "1956"),
    ])
    s["FORMATION"] = clean([(a.replace("Kerala", "കേരള").replace("കerala", "കേരള")
                               .replace("formation", " രൂപീകരണം").replace("formed", " രൂപീകരിച്ച")
                               .replace("statehood", " സംസ്ഥാന സ്ഥാപനം").replace("birthday", " ജന്മദിനം")
                               .replace("reorganization", " പുനഃസംഘടന").replace("State", "സംസ്ഥാന"), b)
                              for a, b in s["FORMATION"]])

    s["LAND_POLICY"] = clean([
        ("Achutha Menon ministry known for", land), ("C Achutha Menon land reform", land),
        ("1969 ministry land reform", land), ("1970 land reform Kerala", land),
        ("Achutha Menon land reforms", land), ("Kerala land reform implementation", land),
        ("EMS education policy 1957", "1957-ൽ വിദ്യാഭ്യാസ നയം"), ("1957 education policy EMS", "1957-ൽ വിദ്യാഭ്യാസ നയം"),
        ("Vimochana education policy", "1957-ൽ വിദ്യാഭ്യാസ നയം"), ("Land reform Achutha Menon", land),
        ("Kerala land reforms 1970s", land), ("Achutha Menon legacy land", land),
        ("1970 Kerala land reform", land), ("Land reforms Kerala Achutha", land),
        ("Education policy 1957 Kerala", "1957-ൽ വിദ്യാഭ്യാസ നയം"), ("EMS 1957 policy", "1957-ൽ വിദ്യാഭ്യാസ നയം"),
        ("Kerala land reform act era", land), ("Achutha Menon reform", land),
        ("Land reform Kerala CPI", land), ("1970s land reform", land),
        ("1957 EMS education", "1957-ൽ വിദ്യാഭ്യാസ നയം"), ("Kerala agrarian reform", land),
        ("Achutha Menon agrarian", land), ("Land policy Kerala 1970", land),
        ("Education reform 1957", "1957-ൽ വിദ്യാഭ്യാസ നയം"), ("Kerala land tenancy reform", land),
        ("Achutha Menon tenure reform", land), ("Land reform implementation Kerala", land),
        ("1957 Kerala education EMS", "1957-ൽ വിദ്യാഭ്യാസ നയം"), ("Kerala land reform landmark", land),
    ])
    s["LAND_POLICY"] = clean([(a.replace("Kerala", "കേരള").replace("Achutha Menon", a).replace("C Achutha Menon", a)
                                .replace("land reform", "ഭൂമി പരിഷ്കരണ").replace("land reforms", "ഭൂമി പരിഷ്കരണ")
                                .replace("Land reform", "ഭൂമി പരിഷ്കരണ").replace("education policy", "വിദ്യാഭ്യാസ നയം")
                                .replace("Education policy", "വിദ്യാഭ്യാസ നയം").replace("EMS", e)
                                .replace("known for", " പ്രശസ്ത for").replace("legacy", " പൈതൃക")
                                .replace("implementation", " നടപ്പാക്കൽ").replace("agrarian", " കാർഷിക")
                                .replace("tenancy", " കുത്തക").replace("landmark", " നാഴികക്കല്ല്")
                                .replace("era", " കാലം").replace("tenure", " കാലഘട്ടം")
                                .replace(" reform", " പരിഷ്കരണ").replace(" policy", " നയം")
                                .replace(" പ്രശസ്ത for", " പ്രശസ്തമായ"), b) for a, b in s["LAND_POLICY"]])

    s["PRESIDENT_RULE"] = clean([
        ("1959 Kerala president rule", "1959"), ("1965 Kerala no ministry", "1965"),
        ("1982 Kerala president rule", "1982"), ("Vimochana 1959 president rule", "1959"),
        ("1965 no clear majority Kerala", "1965"), ("1982 assembly dissolved Kerala", "1982"),
        ("President rule Kerala 1959", "1959"), ("President rule Kerala 1982", "1982"),
        ("1959 dismissed EMS president rule", "1959"), ("1965 hung assembly Kerala", "1965"),
        ("1982 Kerala assembly", "1982"), ("1959 Kerala governor rule", "1959"),
        ("1965 Kerala election no majority", "1965"), ("1982 Kerala president", "1982"),
        ("Kerala president rule years", "1959"), ("1959 1965 1982 Kerala", "1982"),
        ("President rule after Vimochana", "1959"), ("1965 Kerala president rule", "1965"),
        ("1982 president rule Kerala", "1982"), ("1959 central rule Kerala", "1959"),
        ("1965 no ministry Kerala", "1965"), ("1982 central rule Kerala", "1982"),
        ("Kerala 1959 president rule year", "1959"), ("Kerala 1965 no majority", "1965"),
        ("Kerala 1982 president rule", "1982"), ("President rule 1959 Kerala", "1959"),
        ("President rule 1982 Kerala", "1982"), ("1965 president rule Kerala", "1965"),
        ("1959 Kerala central administration", "1959"), ("1982 Kerala governor rule", "1982"),
    ])
    s["PRESIDENT_RULE"] = clean([(a.replace("Kerala", "കേരള").replace("president rule", "രാഷ്ട്രപതി ഭരണം")
                                   .replace("President rule", "രാഷ്ട്രപതി ഭരണം").replace("no ministry", "മന്ത്രിസഭ രൂപീകരണം ഇല്ല")
                                   .replace("no clear majority", "സ്പഷ്ട ഭൂരിപക്ഷമില്ല").replace("no majority", "ഭൂരിപക്ഷമില്ല")
                                   .replace("assembly dissolved", "നിയമസഭ പിരിച്ചുവിടൽ").replace("hung assembly", "തൂക്കി നിൽക്കുന്ന നിയമസഭ")
                                   .replace("central rule", "കേന്ദ്ര ഭരണം").replace("central administration", "കേന്ദ്ര ഭരണം")
                                   .replace("governor rule", "ഗവർണർ ഭരണം").replace("dismissed EMS", f"{e} പിരിച്ചുവിടൽ")
                                   .replace("after Vimochana", "വിമോചന സമരത്തിന് ശേഷം").replace("years", "വർഷങ്ങൾ"), b)
                                  for a, b in s["PRESIDENT_RULE"]])

    abbr = [("യു.ഡി.എഫ്.", UDF), ("എൽ.ഡി.എഫ്.", LDF), ("ഐ.യു.എം.എൽ.", IUML), ("സി.പി.ഐ(എം)", CPM),
            ("സി.പി.ഐ", CPI_S), ("ഭാ.ജ.പ.", BJP), ("എൻ.ഡി.എ.", NDA), ("എസ്.എഫ്.ഐ.", SFI),
            ("കെ.എസ്.യു.", KSU), ("ആർ.എസ്.പി.", RSP), ("ബി.ഡി.ജെ.എസ്.", BDJS)]
    s["ABBR"] = clean([(f"{ab} എന്ന സംക്ഷേപത്തിന്റെ പൂർണ്ണരൂപം", full) for ab, full in abbr]
                       + [(f"{full} ഏത് സംക്ഷേപത്തിൽ", ab) for ab, full in abbr])

    s["CONSTITUENCY"] = clean([
        (f"BJP first MLA Kerala constituency {kzh}", kzh), (f"{og} elected from", kzh),
        (f"{th} lok sabha constituency", tvm), (f"{rh} lok sabha 2019", wy),
        (f"{pi} assembly constituency", "പinarayi"), ("Pinarayi constituency CM", "പinarayi"),
        ("Kazhakoottam BJP 2016", kzh), ("Thiruvananthapuram Tharoor", tvm),
        ("Wayanad Rahul 2019", wy), ("Kizhakkambalam Twenty20", kzm),
        ("Malappuram IUML stronghold", mlp), ("Kazhakoottam Rajagopal", kzh),
        ("Thiruvananthapuram LS", tvm), ("Wayanad LS", wy), ("Kizhakkambalam Sabari", kzm),
        ("Neyyattinkara Antony", "നeyyattinkara"), ("Talassery Karunakaran link", "തalashery"),
        ("Kozhikode north politics", "കozhikode"), ("Kannur communist stronghold", "കannur"),
        ("Ernakulam congress", "എrnakulam"), ("Pathanamthitta UDF", "പathanamthitta"),
        ("Kasaragod north", "കasaragod"), ("Palakkad swing", "പalakkad"),
        ("Thrissur congress", "തrissur"), ("Alappuzha UDF", "ആlappuzha"),
        ("Kottayam KC", "കottayam"), ("Idukki LDF", "ഇdukki"),
    ])
    s["CONSTITUENCY"] = clean([(a.replace("Kerala", "കേരള").replace("constituency", " നിയോജകമണ്ഡലം")
                                .replace("lok sabha", " ലോക്സഭ").replace("assembly", " നിയമസഭ")
                                .replace("stronghold", " ശക്തibase").replace("first MLA", " ആദ്യ MLA")
                                .replace("Pinarayi", "പിണറായി").replace("Kazhakoottam", kzh)
                                .replace("Thiruvananthapuram", tvm).replace("Wayanad", wy)
                                .replace("Kizhakkambalam", kzm).replace("Malappuram", mlp)
                                .replace("Neyyattinkara", "നെയ്യട്ടിൻകര").replace("Talassery", "തലശ്ശേരി")
                                .replace("Kozhikode", "കോഴിക്കോട്").replace("Kannur", "കണ്ണൂർ")
                                .replace("Ernakulam", "എറണാകുളം").replace("Pathanamthitta", "പത്തനംതിട്ട")
                                .replace("Kasaragod", "കാസർഗോഡ്").replace("Palakkad", "പാലക്കാട്")
                                .replace("Thrissur", "തൃശ്ശൂർ").replace("Alappuzha", "ആലപ്പുഴ")
                                .replace("Kottayam", "കോട്ടയം").replace("Idukki", "ഇടുക്കി")
                                .replace(" ശക്തibase", " ബലകേന്ദ്രം").replace("പinarayi", "പിണറായി")
                                .replace("നeyyattinkara", "നെയ്യട്ടിൻകര").replace("തalashery", "തലശ്ശേരി")
                                .replace("കozhikode", "കോഴിക്കോട്").replace("കannur", "കണ്ണൂർ")
                                .replace("എrnakulam", "എറണാകുളം").replace("പathanamthitta", "പത്തനംതിട്ട")
                                .replace("കasaragod", "കാസർഗോഡ്").replace("പalakkad", "പാലക്കാട്")
                                .replace("തrissur", "തൃശ്ശൂർ").replace("ആlappuzha", "ആലപ്പുഴ")
                                .replace("കottayam", "കോട്ടയം").replace("ഇdukki", "ഇടുക്കി"), b)
                               for a, b in s["CONSTITUENCY"] if ok(a,b)])

    s["PORTFOLIO"] = clean([
        (f"{e} finance minister Kerala 1957", "സfinance"), (f"{k} home portfolio", "home"),
        (f"{pi} CM portfolio", "മുഖ്യമന്ത്രി"), (f"{vs} CM 2006", "മുഖ്യമന്ത്രി"),
        (f"{a} land reforms minister", land), ("Finance EMS 1957", "ധനകാര്യ"),
        ("Home Karunakaran", "ആഭ്യന്തര"), ("CM Pinarayi", "മുഖ്യമന്ത്രി"),
        ("CM VS 2006", "മുഖ്യമന്ത്രി"), ("Land Achutha Menon", land),
        ("Education EMS", "വിദ്യാഭ്യാസ"), ("Finance minister Kerala EMS", "ധനകാര്യ"),
        ("Home minister Karunakaran", "ആഭ്യന്തര"), ("CM Oommen Chandy", "മുഖ്യമന്ത്രി"),
        ("CM Antony", "മുഖ്യമന്ത്രി"), ("CM Nayanar", "മുഖ്യമന്ത്രി"),
        ("CM Karunakaran", "മുഖ്യമന്ത്രി"), ("CM Achutha Menon", "മുഖ്യമന്ത്രി"),
        ("Revenue portfolio Kerala", "വരുമാന"), ("Health portfolio Kerala", "ആരോഗ്യ"),
        ("Education portfolio EMS", "വിദ്യാഭ്യാസ"), ("Finance Kerala EMS", "ധനകാര്യ"),
        ("Home Kerala Karunakaran", "ആഭ്യന്തര"), ("CM portfolio Kerala", "മുഖ്യമന്ത്രി"),
        ("Land reform minister Achutha", land), ("Education minister EMS 1957", "വിദ്യാഭ്യാസ"),
        ("Finance minister 1957 EMS", "ധനകാര്യ"), ("CM EMS", "മുഖ്യമന്ത്രി"),
        ("CM Pattom", "മുഖ്യമന്ത്രി"),
    ])
    s["PORTFOLIO"] = clean([(a.replace("Kerala", "കേരള").replace("minister", " മന്ത്രി")
                              .replace("portfolio", " വകുപ്പ്").replace("Finance", "ധനകാര്യ")
                              .replace("Home", "ആഭ്യന്തര").replace("Education", "വിദ്യാഭ്യാസ")
                              .replace("Revenue", "വരുമാന").replace("Health", "ആരോഗ്യ")
                              .replace("CM", "മുഖ്യമന്ത്രി").replace("Land", "ഭൂമി")
                              .replace("EMS", e).replace("Karunakaran", k).replace("Pinarayi", pi)
                              .replace("VS", vs).replace("Achutha Menon", a).replace("Oommen Chandy", oc)
                              .replace("Antony", an).replace("Nayanar", ny).replace("Pattom", p)
                              .replace("സfinance", "ധനകാര്യ").replace("home", "ആഭ്യന്തര"), b)
                             for a, b in s["PORTFOLIO"]])

    s["WOMEN"] = clean([
        ("Kerala local bodies women reservation", "50%"), ("50% women panchayat Kerala", "50%"),
        ("Kerala 50 percent women local", "50%"), ("Women reservation Kerala local", "50%"),
        ("50% reservation local bodies Kerala", "50%"), ("Kerala panchayat women 50", "50%"),
        ("Local self govt women Kerala 50", "50%"), ("50% women Kerala panchayat", "50%"),
        ("Kerala first woman CM", "ഇല്ല"), ("Woman CM Kerala history", "ഇല്ല"),
        ("Kerala 50% local reservation", "50%"), ("Women 50 panchayat Kerala", "50%"),
        ("Kerala local women quota", "50%"), ("50 percent local Kerala", "50%"),
        ("Kerala woman chief minister", "ഇല്ല"), ("No woman CM Kerala", "ഇല്ല"),
        ("Kerala 50 women local bodies", "50%"), ("Panchayat 50 women Kerala", "50%"),
        ("Kerala local 50 reservation", "50%"), ("50% quota Kerala local", "50%"),
        ("Women local governance Kerala", "50%"), ("Kerala 50% panchayat women", "50%"),
        ("Local bodies 50 Kerala", "50%"), ("Kerala women 50 percent local", "50%"),
        ("50% women reservation act Kerala", "50%"), ("Kerala local women 50%", "50%"),
        ("Kerala no woman CM yet", "ഇല്ല"), ("Woman CM Kerala none", "ഇല്ല"),
        ("Kerala 50% local self reservation", "50%"), ("50 women Kerala governance", "50%"),
        ("Kerala panchayat raj women 50", "50%"), ("Women 50% Kerala local gov", "50%"),
    ])
    s["WOMEN"] = clean([(a.replace("Kerala", "കേരള").replace("women", "സ്ത്രീ").replace("woman", "സ്ത്രീ")
                          .replace("local bodies", "തദ്ദേശ സ്ഥാപനങ്ങൾ").replace("panchayat", "പഞ്ചായത്ത്")
                          .replace("reservation", " reservation").replace("50 percent", "50%")
                          .replace("50 women", "50% സ്ത്രീ").replace("quota", " reservation")
                          .replace("chief minister", "മുഖ്യമന്ത്രി").replace("CM", "മുഖ്യമന്ത്രി")
                          .replace("none", "ഇല്ല").replace("yet", "").replace("history", "ചരിത്രം")
                          .replace("local self govt", "തദ്ദേശ സ്വയംഭരണ").replace("local governance", "തദ്ദേശ ഭരണ")
                          .replace("local gov", "തദ്ദേശ ഭരണ").replace("act", "നിയമം")
                          .replace(" reservation", " reservation").replace("No ", "ഇല്ല "), b)
                         for a, b in s["WOMEN"]])

    unions = [(CITU, CPM), (INTUC, INC), (AITUC, CPI)]
    s["TRADE_UNION"] = clean([(f"{u} ബന്ധപ്പെട്ട പാർട്ടി", p) for u, p in unions]
                              + [(f"{p} തൊഴിൽ സ.union", u) for u, p in unions]
                              + [(f"{CITU} affiliate", CPM), (f"{INTUC} affiliate", INC), (f"{AITUC} affiliate", CPI)] * 8)
    s["TRADE_UNION"] = clean([(a.replace(" affiliate", " അഫിലിയേറ്റ്").replace("union", "യൂണിയൻ"), b)
                                for a, b in s["TRADE_UNION"]])

    s["COMMUNIST"] = clean([
        ("First communist elected govt India", e), ("1957 Kerala communist ministry", e),
        ("CPI split year Kerala", "1964"), ("1964 CPI split formed", CPM),
        ("First democratically elected communist", e), ("1957 EMS communist govt", e),
        ("Kerala 1957 world first communist elected", e), ("CPI Marxist formed 1964", CPM),
        ("1964 split CPI Kerala", CPM), ("First communist ministry India Kerala", e),
        ("1957 communist Kerala EMS", e), ("CPI CPM split 1964", "1964"),
        ("World first elected communist govt", e), ("Kerala communist 1957", e),
        ("EMS 1957 communist", e), ("1964 formation CPM", CPM), ("CPI split 1964 CPM", CPM),
        ("First red ministry India", e), ("1957 red govt Kerala", e), ("Communist govt 1957", e),
        ("1964 Marxist party Kerala", CPM), ("CPI division 1964", CPM), ("1957 EMS CPI", e),
        ("Kerala first red govt", e), ("1964 CPI M split", CPM), ("Communist ministry Kerala first", e),
        ("1957 world communist elected", e), ("CPM born 1964", CPM), ("1964 Kerala CPI split", CPM),
        ("First communist CM India", e), ("1957 Kerala CPI ministry", e),
    ])
    s["COMMUNIST"] = clean([(a.replace("Kerala", "കേരള").replace("communist", "കമ്മ്യunist")
                              .replace("Communist", "കമ്മ്യunist").replace("CPI", CPI_S).replace("CPM", CPM)
                              .replace("EMS", e).replace("govt", "ഭരണ").replace("ministry", "മന്ത്രിസഭ")
                              .replace("India", "ഇന്ത്യ").replace("world", "ലോക").replace("first", "ആദ്യ")
                              .replace("elected", "തിരഞ്ഞെടുക്കപ്പെട്ട").replace("red", "ചുവപ്പ്")
                              .replace("split", " വിഭജന").replace("formed", " രൂപീകരിച്ച")
                              .replace("formation", " രൂപീകരണ").replace("division", " വിഭജന")
                              .replace("Marxist", " മാർക്സിസ്റ്റ്").replace("born", " ജനനം")
                              .replace("CM", "മുഖ്യമന്ത്രി").replace("കമ്മ്യunist", "കമ്മ്യunist"), b)
                             for a, b in s["COMMUNIST"]])
    s["COMMUNIST"] = clean([(a.replace("കമ്മ്യunist", "കമ്മ്യunist"), b) for a, b in s["COMMUNIST"]])

    s["KERALA_CONGRESS"] = clean([
        (f"{km} founded party", KC), (f"{pj} faction leader", KC), ("Kerala Congress Mani", km),
        ("Kerala Congress Joseph", pj), ("KC Mani", km), ("KC Joseph", pj), ("Mani KC", km),
        ("Joseph KC faction", pj), ("Kerala Congress founder Mani", km), ("Kerala Congress PJ", pj),
        ("Mani party Kerala Congress", KC), ("Joseph Kerala Congress party", KC),
        ("KM Mani Kerala Congress", km), ("PJ Joseph KC", pj), ("Kerala Congress party Mani", km),
        ("Kerala Congress split Joseph", pj), ("Mani faction", km), ("Joseph faction", pj),
        ("KC party Mani", km), ("KC party Joseph", pj), ("Kerala Congress leader Mani", km),
        ("Kerala Congress leader Joseph", pj), ("Mani Kerala Congress founder", km),
        ("Joseph Kerala Congress leader", pj), ("Kerala Congress KM Mani", km),
        ("Kerala Congress PJ Joseph", pj), ("Mani established Kerala Congress", km),
        ("Joseph Kerala Congress faction", pj), ("KC Mani leader", km), ("KC Joseph leader", pj),
    ])
    s["KERALA_CONGRESS"] = clean([(a.replace("Kerala", "കേരള").replace("Congress", "കോൺഗ്രസ്")
                                    .replace("founded", " സ്ഥാപിച്ച").replace("faction", " ഫാക്ഷൻ")
                                    .replace("founder", " സ്ഥാപകൻ").replace("leader", " നേതാവ്")
                                    .replace("party", " പാർട്ടി").replace("split", " വിഭജന")
                                    .replace("established", " സ്ഥാപിച്ച").replace("KM Mani", km)
                                    .replace("PJ Joseph", pj).replace("Mani", km).replace("Joseph", pj)
                                    .replace("KC", KC), b) for a, b in s["KERALA_CONGRESS"]])

    s["IUML"] = clean([
        ("IUML stronghold district Kerala", mlp), ("Muslim League Malappuram", mlp),
        ("IUML base Malappuram", mlp), ("Indian Union Muslim League Kerala", IUML),
        ("IUML Kerala party", IUML), ("Malappuram IUML", mlp), ("IUML strong Malappuram", mlp),
        ("Muslim League Kerala", IUML), ("IUML district stronghold", mlp), ("IUML Malappuram base", mlp),
        ("Kerala IUML party", IUML), ("IUML Kerala stronghold", mlp), ("Malappuram league", mlp),
        ("IUML Malappuram district", mlp), ("Muslim League stronghold", mlp), ("IUML base district", mlp),
        ("Kerala Muslim League", IUML), ("IUML Malappuram strong", mlp), ("League Malappuram", mlp),
        ("IUML Kerala Malappuram", mlp), ("Malappuram Muslim League strong", mlp),
        ("IUML party Kerala", IUML), ("Muslim League party Kerala", IUML), ("IUML Malappuram politics", mlp),
        ("Kerala IUML Malappuram", mlp), ("IUML heartland Malappuram", mlp), ("Malappuram IUML base", mlp),
        ("IUML Kerala district", mlp), ("Muslim League IUML Kerala", IUML), ("IUML Malappuram seat", mlp),
    ])
    s["IUML"] = clean([(a.replace("Kerala", "കേരള").replace("IUML", "ഐ.യു.എം.എൽ.")
                         .replace("Muslim League", "മുസ്ലിം ലീഗ്").replace("Indian Union Muslim League", IUML)
                         .replace("stronghold", " ബലകേന്ദ്രം").replace("strong", " ശക്തം")
                         .replace("base", " അടിത്തറ").replace("district", " ജില്ല")
                         .replace("heartland", " હൃദയഭൂമി").replace("seat", " സീറ്റ്")
                         .replace("politics", " രാഷ്ട്രീയം").replace("party", " പാർട്ടി")
                         .replace("League", "ലീഗ്").replace("Malappuram", mlp)
                         .replace(" હृദയഭൂमി", "ഹൃദയഭൂമി"), b) for a, b in s["IUML"]])

    s["BJP_KERALA"] = clean([
        (f"BJP first MLA Kerala {kzh}", kzh), (f"{og} first BJP MLA", og), ("2016 BJP MLA Kerala", kzh),
        ("Kazhakoottam BJP 2016", kzh), ("BJP NDA Kerala", NDA), ("BDJS NDA Kerala", NDA),
        ("BJP Kerala first MLA seat", kzh), ("2016 Kazhakoottam BJP", kzh), ("Rajagopal BJP MLA", og),
        ("BJP Kerala breakthrough 2016", kzh), ("NDA Kerala BDJS", NDA), ("BJP alliance Kerala NDA", NDA),
        ("First BJP legislator Kerala", og), ("Kerala BJP MLA 2016", og), ("BJP seat Kazhakoottam", kzh),
        ("2016 Kerala BJP win", kzh), ("NDA in Kerala", NDA), ("BJP Kerala NDA partner", BDJS),
        ("Rajagopal Kazhakoottam 2016", kzh), ("BJP first assembly seat Kerala", kzh),
        ("Kerala BJP 2016 MLA", og), ("NDA alliance Kerala", NDA), ("BDJS BJP ally Kerala", NDA),
        ("Kazhakoottam 2016 BJP win", kzh), ("First BJP MLA seat Kerala", kzh),
        ("Rajagopal BJP Kerala", og), ("2016 BJP breakthrough Kerala", kzh),
        ("NDA Kerala alliance", NDA), ("BJP Kerala Kazhakoottam", kzh), ("BDJS Kerala NDA", NDA),
    ])
    s["BJP_KERALA"] = clean([(a.replace("Kerala", "കേരള").replace("BJP", "ഭാ.ജ.പ.")
                               .replace("NDA", NDA).replace("BDJS", BDJS).replace("MLA", " MLA")
                               .replace("first", " ആദ്യ").replace("legislator", " നിയമസഭാംഗം")
                               .replace("breakthrough", " തുടക്കം").replace("win", " വിജയം")
                               .replace("seat", " സീറ്റ്").replace("alliance", " സഖ്യം")
                               .replace("partner", " പങ്കാളി").replace("ally", " സоюзник")
                               .replace("Kazhakoottam", kzh).replace("Rajagopal", og)
                               .replace(" സоюзник", " സоюзник").replace(" സоюзник", " പങ്കാളി"), b)
                              for a, b in s["BJP_KERALA"]])

    s["NICKNAME"] = clean([
        (f"{e} nickname Elamkulam", "എlamkulam"), ("EMS Elamkulam", "എlamkulam"),
        ("Karunakaran leader nickname", "കarunakaran"), ("Leader of masses EMS", e),
        ("VS mass leader", vs), ("Pinarayi nickname", pi), ("Nayanar mass leader", ny),
        ("Achutha Menon reformer", a), ("Mani Kerala Congress leader", km),
        ("EMS Kerala communist leader", e), ("Karunakaran Congress leader", k),
        ("VS opposition icon", vs), ("Pinarayi CPIM leader", pi), ("Nayanar LDF leader", ny),
        ("Antony Congress leader", an), ("Oommen Chandy UDF", oc), ("Sudhakaran KPCC", su),
        ("Satheesan opposition", sa), ("Shamseer speaker", sh), ("Govindan CPIM secretary", gv),
        ("Kodiyeri CPIM leader", kd), ("Panneerselvam CPI", pn), ("Tharoor MP", th),
        ("Rahul Wayanad", rh), ("Chennithala UDF", ch), ("Rajagopal BJP", og),
        ("Pattom PSP leader", p), ("PKV socialist", pkv), ("Achutha reformer CM", a),
        ("EMS mass leader", e), ("Karunakaran master", k),
    ])
    s["NICKNAME"] = clean([(a.replace("nickname", " വിളിപ്പേര്").replace("leader", " നേതാവ്")
                             .replace("mass leader", " ജനനേതാവ്").replace("reformer", " പരിഷ്കർത്താവ്")
                             .replace("icon", " പ്രതീകം").replace("master", " മാസ്റ്റർ")
                             .replace("Elamkulam", "എlamkulam").replace("EMS", e).replace("Karunakaran", k)
                             .replace("VS", vs).replace("Pinarayi", pi).replace("Nayanar", ny)
                             .replace("Achutha Menon", a).replace("Mani", km).replace("Antony", an)
                             .replace("Oommen Chandy", oc).replace("Sudhakaran", su).replace("Satheesan", sa)
                             .replace("Shamseer", sh).replace("Govindan", gv).replace("Kodiyeri", kd)
                             .replace("Panneerselvam", pn).replace("Tharoor", th).replace("Rahul", rh)
                             .replace("Chennithala", ch).replace("Rajagopal", og).replace("Pattom", p)
                             .replace("PKV", pkv).replace("കarunakaran", k).replace("എlamkulam", "എlamkulam"), b)
                            for a, b in s["NICKNAME"] if ok(a,b)])

    assert len(s) == 29, len(s)
    return {name: sanitize_rows(rows) for name, rows in s.items()}


def fmt_pairs(name: str, rows: list[tuple[str, str]]) -> str:
    return f"{name}: list[tuple[str, str]] = [\n" + "".join(
        f"    ({a!r}, {b!r}),\n" for a, b in rows
    ) + "]\n"


def emit_block(name: str) -> str:
    fl = ", ".join(repr(x) for x in FWD)
    rl = ", ".join(repr(x) for x in REV)
    return (
        f"    emit_category(out, existing, rng, {name},\n"
        f"        [{fl}],\n        [{rl}],\n"
        f"        [a for a, _ in {name}], [b for _, b in {name}])\n"
    )


FOOTER = '''
def generate_wave30_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []
{body}
    emit_direct(out, existing, rng, DIRECT_FACTS)
    return out


if __name__ == "__main__":
    print(len(generate_wave30_candidates(set(), random.Random(0))))
'''


def build_direct(
    e, k, an, ny, oc, vs, pi, sh, sa, ar, su, ch, th, rh, km, pj, rj, burg, ss,
    LDF, UDF, CPI_S, CPM, INC, IUML, BJP, NDA, kzh,
) -> list[tuple[str, str, list[str], str]]:
    return [
        ("കേരള നിയമസഭാ സീറ്റുകളുടെ എണ്ണം?", "140", ["20", "9", "100"], "easy"),
        ("കേരള ലോക്സഭാ സീറ്റukളുടെ എണ്ണം?", "20", ["140", "9", "14"], "easy"),
        ("കേരള രാജ്യസഭാ സീറ്റukളുടെ എണ്ണം?", "9", ["20", "140", "5"], "easy"),
        ("കേരള നിയമസഭാ കാലാവധി?", "5 വർഷം", ["4 വർഷം", "6 വർഷം", "3 വർഷം"], "easy"),
        ("ഇന്ത്യയിൽ വോട്ട് ചെയ്യാനുള്ള കുറഞ്ഞ പ്രായം?", "18", ["21", "25", "16"], "easy"),
        ("കerala MLA കുറഞ്ഞ പ്രായം?", "25", ["18", "21", "30"], "medium"),
        ("യു.ഡി.എഫ്. എന്ന സംക്ഷേപത്തിന്റെ പൂർണ്ണരൂപം?", UDF, [LDF, "ലിബറൽ ഡെമോക്രാറ്റിക് ഫ്രണ്ട്", "ലോക ഡെമോക്രാറ്റിക് ഫ്രണ്ട്"], "easy"),
        ("എൽ.ഡി.എഫ്. എന്ന സംക്ഷേപത്തിന്റെ പൂർണ്ണരൂപം?", LDF, [UDF, "ലിബറൽ ഡെമോക്രാറ്റിക് ഫ്രണ്ട്", "ലോക ഡെമോക്രാറ്റിക് ഫ്രണ്ട്"], "easy"),
        (f"കേരളത്തിന്റെ ആദ്യ മുഖ്യമന്ത്രി?", e, [k, an, ny], "easy"),
        ("1957-ൽ കേരളത്തിലെ ആദ്യ CPI മന്ത്രിസഭയ്ക്ക് നേതൃത്വം?", e, [k, an, ny], "easy"),
        ("വിമോചന സമരം ഫലമായി എന്ത് സംഭവിച്ചു?", "ആദ്യ ഇ.എം.എസ്. മന്ത്രിത്വത്തിന്റെ പിരിച്ചുവിടൽ", ["കേരള സംസ്ഥാന രൂപീകരണം", "ശാശ്വത രാഷ്ട്രപതി ഭരണം", "ഒന്നുമില്ല"], "hard"),
        ("കerala പഞ്ചായത്ത് രാജ് ആക്റ്റ് വർഷം?", "1994", ["1956", "2010", "1980"], "hard"),
        ("കerala തദ്ദേശ സ്ഥാപനങ്ങളിൽ reservation?", "50%", ["33%", "25%", "10%"], "hard"),
        (f"2024-ലോടെ കerala ഗവർണർ?", ar, ["പി. സത്യശിവം", "ആർ.എൽ. ഭാട്ടിയ", "സികന്ദർ ബക്ത്"], "medium"),
        (f"2024-ലോടെ കerala പ്രതിപക്ഷ നേതാവ്?", sa, [pi, su, ch], "hard"),
        (f"2021-ൽ കerala നിയമസഭാ സ്പീക്കർ?", sh, [rj, pi, sa], "medium"),
        ("1964-ൽ സി.പി.ഐ വിഭajനം ഉണ്ടാക്കിയ പാർട്ടി?", CPM, [CPI_S, INC, BJP], "hard"),
        ("കerala സംസ്ഥാന രൂപീകരണ വർഷം?", "1956", ["1957", "1947", "1960"], "easy"),
        ("കerala സംസ്ഥാന രൂപീകരണ ദിനം?", "1956 നവംബർ 1", ["1956 ജനുവരി 26", "1957 ഏപ്രിൽ 1", "1947 ഓഗസ്റ്റ് 15"], "hard"),
        ("1982-ൽ കerala?", "രാഷ്ട്രപതി ഭരണം", ["LDF വിജയം", "UDF വിജയം", "തിരഞ്ഞെടുപ്പ് ഇല്ല"], "hard"),
        ("1959-ൽ കerala?", "രാഷ്ട്രപതി ഭരണം", ["LDF വിജയം", "UDF വിജയം", "1965"], "hard"),
        (f"2016-ൽ കerala മുഖ്യമന്ത്രി?", pi, [oc, vs, k], "medium"),
        (f"2006-ൽ കerala മുഖ്യമന്ത്രി?", vs, [pi, oc, ny], "medium"),
        (f"1991-ൽ കerala മുഖ്യമന്ത്രി?", k, [ny, an, e], "medium"),
        ("ഇ.യു.എം.എൽ. ശക്തibase ജില്ല?", "മലപ്പുറം", ["വയനാട്", "കാസർഗോഡ്", "ഇടുക്കി"], "medium"),
        ("2016-ൽ ഭാ.ജ.പ. ആദ്യ MLA നിയോജകമണ്ഡലം?", "കഴakkoottam", ["തിരുവനന്തപുരം", "കാസർഗോഡ്", "പത്തനംതിട്ട"], "hard"),
        ("എസ്.എഫ്.ഐ. ബന്ധപ്പെട്ട പാർട്ടി?", CPM, [CPI_S, INC, IUML], "medium"),
        ("കെ.എസ്.യു. ബന്ധപ്പെട്ട പാർട്ടി?", INC, [CPM, CPI_S, BJP], "medium"),
        ("സി.ഐ.ടി.യു. ബന്ധപ്പെട്ട പാർട്ടി?", CPM, [INC, CPI_S, IUML], "hard"),
        ("1979-ൽ രൂപീകരിച്ച മുന്നണി?", UDF, [LDF, NDA, "എൻ.ഡി.എ."], "hard"),
        ("1980-ൽ രൂപീകരിച്ച മുന്നണി?", LDF, [UDF, NDA, INC], "hard"),
        ("1996-ൽ കerala ജനകീയ പദ്ധതി?", "1996", ["1994", "2000", "2010"], "hard"),
        (f"{k} ആദ്യം മുഖ്യമന്ത്രിയായ വർഷം?", "1977", ["1980", "1960", "2001"], "hard"),
        ("കerala ആദ്യ നിയമസഭാ തിരഞ്ഞെടുപ്പ്?", "1957", ["1956", "1960", "1965"], "hard"),
        ("കerala നിയമസഭാ സ്പീക്കർ?", "സ്പീക്കർ", ["ഗവർണർ", "മുഖ്യമന്ത്രി", "മന്ത്രിസഭ"], "easy"),
        ("സംസ്ഥാന മന്ത്രിസഭ?", "മന്ത്രിസഭ", ["ഗവർണർ", "നിയമസഭ", "സെക്രട്ടേറിയറ്റ്"], "easy"),
        ("കerala ലോക്സഭാ 2019 വayനാട് MP?", rh, [th, k, pi], "medium"),
        ("തിരുവനന്തപുരം ലോക്സഭാ MP?", th, [rh, k, an], "medium"),
        ("കerala Congress founder?", km, [pj, k, e], "hard"),
        ("കerala 50% women local?", "50%", ["33%", "25%", "10%"], "hard"),
        ("ആദ്യ കerala ഗവർണർ?", burg, [ar, ss, "പി. സത്യശിവം"], "hard"),
        ("2021 LDF വിജയം?", LDF, [UDF, NDA, INC], "medium"),
    ]


def main() -> None:
    import importlib.util

    sections = build_sections()
    body = "".join(emit_block(n) for n in sections)

    e, k, an, ny, oc, vs, pi = [n(x) for x in ("EMS", "KARUNAKARAN", "ANTONY", "NAYANAR", "OOMMEN", "VS", "PINARAYI")]
    sh, sa, ar, su, ch, th, rh, km, pj = (
        n("SHAMSEER"), n("SATHEESAN"), n("ARIF"), n("SUDHAKARAN"), n("CHENNITHALA"),
        n("THAROOR"), n("RAHUL"), n("KM_MANI"), n("PJ_JOSEPH"),
    )
    rj, burg, ss = "എം.ബി. രാജേഷ്", "ബർഗുല രാമകൃഷ്ണ റാവു", n("SATHASIVAM")
    LDF, UDF, CPI_S = "ഇടത് ജനാധിപത്യ മുന്നണി", "യുണൈറ്റഡ് ഡെമോക്രാറ്റിക് ഫ്രണ്ട്", "സി.പി.ഐ"
    CPM, INC = "സി.പി.ഐ(എം)", "ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ്"
    IUML, BJP, NDA = "ഇന്ത്യൻ യൂണിയൻ മുസ്ലിം ലീഗ്", "ഭാരതീയ ജനതാ പാർട്ടി", "എൻ.ഡി.എ."
    kzh = "കഴക്കൂട്ടം"

    direct_rows = build_direct(
        e, k, an, ny, oc, vs, pi, sh, sa, ar, su, ch, th, rh, km, pj, rj, burg, ss,
        LDF, UDF, CPI_S, CPM, INC, IUML, BJP, NDA, kzh,
    )
    direct_rows = [
        (sanitize_ml(q), sanitize_ml(a), [sanitize_ml(x) for x in w], d)
        for q, a, w, d in direct_rows
    ]
    direct_rows = [
        (q, a, w, d) for q, a, w, d in direct_rows
        if not MIXED.search(q + a + "".join(w))
    ]

    direct_txt = "DIRECT_FACTS: list[tuple[str, str, list[str], str]] = [\n" + "".join(
        f"    ({q!r}, {a!r}, {w!r}, {d!r}),\n" for q, a, w, d in direct_rows
    ) + "]\n"

    pairs_txt = "".join(fmt_pairs(n, r) for n, r in sections.items())
    content = (
        '#!/usr/bin/env python3\n"""Wave 30 Kerala politics facts — 30 Malayalam PSC topic types."""\n\n'
        "from __future__ import annotations\n\nimport random\n\n"
        "from refill_common import Candidate\nfrom wave30_emit import emit_category, emit_direct\n\n"
        + pairs_txt + "\n" + direct_txt + FOOTER.replace("{body}", body)
    )
    OUT.write_text(content, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("pok", OUT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    count = len(mod.generate_wave30_candidates(set(), random.Random(0)))
    print(str(OUT.resolve()), count)


if __name__ == "__main__":
    main()
