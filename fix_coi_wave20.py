#!/usr/bin/env python3
"""Post-process coi_wave20_facts.py: Latin filter in _add + clean data rows."""

from __future__ import annotations

import random
import re
from pathlib import Path

ROOT = Path(__file__).parent
TARGET = ROOT / "coi_wave20_facts.py"

MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")
_LATIN4 = re.compile(r"[a-zA-Z]{4,}")
ALLOWED = re.compile(r"\b(GST|UPSC|CAG|NJAC|NCSC|NCST|NCBC|EWS)\b")
PH = re.compile(r"^അനുച്ഛേദം .+ വ്യവസ്ഥ$")

NEW_ADD = '''def _strip_allowed_latin(text: str) -> str:
    return _ALLOWED_LATIN.sub("", text)


def _has_stray_latin(text: str) -> bool:
    return bool(_LATIN4.search(_strip_allowed_latin(text)))


def _add(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    q: str,
    ans: str,
    wrong: list[str],
    diff: str = "medium",
    pool: list[str] | None = None,
) -> None:
    blob = q + ans + "".join(wrong)
    if MIXED.search(blob):
        return
    if _has_stray_latin(blob):
        return
    add_candidate(out, existing, rng, q, ans, wrong, diff, pool)
'''

INSERT_AFTER_MIXED = '''_ALLOWED_LATIN = re.compile(
    r"\\b(GST|UPSC|CAG|NJAC|NCSC|NCST|NCBC|EWS)\\b"
)
_LATIN4 = re.compile(r"[a-zA-Z]{4,}")
'''


def ml_num(n: int) -> str:
    m = {
        1: "ഒന്ന്", 2: "രണ്ട്", 3: "മൂന്ന്", 4: "നാല്", 5: "അഞ്ച്", 6: "ആറ്", 7: "ഏഴ്",
        8: "എട്ട്", 9: "ഒമ്പത്", 10: "പത്ത്", 11: "പതിനൊന്ന്", 12: "പന്ത്രിഞ്ച്",
        13: "പതിമൂന്ന്", 14: "പതിനാല്", 15: "പതിനഞ്ച്", 16: "പതിനാറ്", 17: "പതിനേഴ്",
        18: "പതിനെട്ട്", 19: "പത്തൊമ്പത്", 31: "മുപ്പത്തൊന്ന്",
    }
    if n in m:
        return m[n]
    tens, ones = divmod(n, 10)
    t = {2: "ഇരുപത്", 3: "മുപ്പത്"}.get(tens, str(tens))
    return t if ones == 0 else t + m[ones]


def fix_text(s: str) -> str:
    rep = {
        "മിസoram": "മിസോറം", "നാഗaland": "നാഗാലാൻഡ്", "ഛത്തീസ്ഗarh": "ഛത്തീസ്ഗഡ്",
        "ജammu കശ്മീർ": "ജമ്മു-കശ്മീർ", "ലadakh": "ലഡാക്", "ചണ്ഡigarh": "ചണ്ഡീഗഡ്",
        "ദādra നഗർ ഹവേലി": "ദാദ്ര നഗർ ഹവേലി", "ലക്ഷദweep": "ലക്ഷദ്വീപ്",
        "കൺട്രോളർ ആൻഡ് ഓഡിറ്റർ ജനറൽ": "നിയന്ത്രണ-ഓഡിറ്റ് ജനറൽ",
        "അറ്റോർണി ജനറൽ": "മുഖ്യ നിയമോപദേശകൻ",
        "pension ലഭ്യമാക്കൽ": "വിരമണാനന്തര ആനukopalyam",
        "സത്യപ്രതിജ്ഞയും രഹസ്യസംrakshan": "സത്യപ്രതിജ്ഞാ രൂപവും രഹസ്യം പാലിക്കൽ",
        "സanskrit": "സംസ്കൃതം", "ബengali": "ബംഗാളി", "ഗujarati": "ഗുജറാത്തി",
        "മarathi": "മറാത്തി", "തelugu": "തെലുങ്ക്", "കannada": "കന്നഡ",
        "ഒriya": "ഒഡിയ", "പunjabi": "പഞ്ചാബി", "അssamese": "അസമീസ്",
        "മanipuri": "മണിപ്പുരി", "നepali": "നേപ്പാളി", "ബodo": "ബോഡോ",
        "ഡogri": "ഡോഗ്രി", "മaithili": "മൈഥിലി", "സantali": "സantalി", "സindhi": "സindi",
        "Inter-State Council": "അന്തരസംസ്ഥാന കൗൺസിൽ",
        "Consolidated Fund": "ഏകീകൃത നിധി",
        "Contingency Fund": "അനിശ്ചിത നിധി",
        "Finance Commission": "ധനകമ്മിഷൻ",
        "Election Commission": "തിരഞ്ഞെടുപ്പ് കമ്മീഷൻ",
        "President Rule": "രാഷ്ട്രപതി ഭരണം",
        "National Emergency": "ദേശീയ അടിയന്തരാവസ്ഥ",
        "Financial Emergency": "ധനകാര്യ അടിയന്തരാവസ്ഥ",
        "official language Hindi": "കേന്ദ്ര ഔദ്യോഗിക ഭാഷ ഹിന്ദി",
        "state official language": "സംസ്ഥാന ഔദ്യോഗിക ഭാഷ",
        "language of Supreme Court": "സുപ്രീംകോടതിയുടെ ഭാഷ",
        "Hindi development directive": "ഹിന്ദി വികസന നിർദ്ദേശം",
        "8th schedule language": "എട്ടാം ഷെഡ്യൂളിലെ ഭാഷ",
        "official language union": "കേന്ദ്ര ഔദ്യോഗിക ഭാഷ",
        "continues for 15 years": "15 വർഷം തുടരുന്നു",
        "Zonal Councils": "മേഖലാ കൗൺസിലുകൾ",
        "5 zonal councils": "അഞ്ച് മേഖലാ കൗൺസിലുകൾ",
        "no-confidence motion": "അവിശ്വാസ പ്രമേയം",
        "joint session": "സംയുക്ത അധിവേശം",
        "parliament privileges": "പാർലമെന്റ്特権",
        "motion of thanks": "നന്ദി പ്രമേയം",
        "casting vote": "നിർണായക വോട്ട്",
        "speaker casting vote": "സ്പീക്കറുടെ നിർണായക വോട്ട്",
        "money bill definition": "ധനബിൽ നിർവചനം",
        "annual financial statement": "വാർഷിക ധനകാര്യ പ്രസ്താവന",
        "administrative tribunals": "ഭരണ ധികാരണങ്ങൾ",
        "other tribunals": "മറ്റ് ധികാരണങ്ങൾ",
        "Part XIV-A added": "ഭാഗം XIV-A ചേർത്തു",
        "cooperative societies constitutional status": "സഹകരണ സമിതികൾക്ക് ഭരണഘടനാ നില",
        "Canada": "കാനഡ", "Australia": "ഓസ്ട്രേലിയ", "Japan": "ജപ്പാൻ",
        "UK": "ഇംഗ്ലണ്ട്", "USA": "അമേരിക്ക", "Ireland": "അയർലൻഡ്",
        "Germany": "ജർമ്മനി", "USSR": "സോവിയറ്റ് യൂണിയൻ", "South Africa": "ദക്ഷിണാഫ്രിക്ക",
        "secularism": "മതേതരത്വം", "federalism": "സംഘടിതാധിപത്യം",
        "democracy": "ജനാധിപത്യം", "rule of law": "നിയമത്തിന്റെ ആധിപത്യം",
        "judicial review": "നീതിപരിശോധന",
        "separation of powers": "അധികാര വേർതിരിവ്",
        "free and fair elections": "സ്വതന്ത്രവും നീതിയുള്ളതുമായ തിരഞ്ഞെടുപ്പുകൾ",
        "welfare state": "ക്ഷേമ രാഷ്ട്രം",
        "limited amending power": "പരിമിത ഭേദഗതി അധികാരം",
        "quasi-federal structure": "അർദ്ധ-സംഘടിത ഘടന",
        "single citizenship": "ഏക പൗരത്വം",
        "parliamentary system from UK": "ഇംഗ്ലണ്ടിൽ നിന്നുള്ള പാർലമെന്റ് സംവിധാനം",
        "fundamental rights from USA": "അമേരിക്കയിൽ നിന്നുള്ള മൗലികാവകാശങ്ങൾ",
        "DPSP from Ireland": "അയർലൻഡിൽ നിന്നുള്ള നിർദ്ദേശക തത്വങ്ങൾ",
        "emergency provisions from Germany": "ജർമ്മനിയിൽ നിന്നുള്ള അടിയന്തരാവസ്ഥാ വ്യവസ്ഥകൾ",
        "fundamental duties from USSR": "സോവിയറ്റ് യൂണിയനിൽ നിന്നുള്ള മൗലിക കടമകൾ",
        "amendment procedure from South Africa": "ദക്ഷിണാഫ്രിക്കയിൽ നിന്നുള്ള ഭേദഗതി നടപടിക്രമം",
        "federation with strong centre from Canada": "കാനഡയിൽ നിന്നുള്ള ശക്തമായ കേന്ദ്രമുള്ള സംഘടിതാധിപത്യം",
        "concurrent list from Australia": "ഓസ്ട്രേലിയയിൽ നിന്നുള്ള സമാന്തര പട്ടിക",
        "procedure established by law from Japan": "ജപ്പാനിൽ നിന്നുള്ള നിയമപ്രകാരമുള്ള നടപടിക്രമം",
        "simple majority": "സാധാരണ ഭൂരിപക്ഷം",
        "special majority": "പ്രത്യേക ഭൂരിപക്ഷം",
        "ratification": "സംസ്ഥാന_ratification",
        "state ratification": "സംസ്ഥാന_ratification",
        "anti-defection": "വിരോധ പക്ഷത്തേക്ക് കടന്നുപോകൽ നിയന്ത്രണം",
        "mini constitution": "മini ഭരണഘടന",
        "zamindari abolition acts protected": "ജമീന്ദാരി നിരോധന നിയമങ്ങൾ സംരക്ഷണം",
        "284+ acts listed": "284-ലധികം നിയമങ്ങൾ",
        "future laws cannot be validated": "ഭാവി നിയമങ്ങൾ സാധൂകരിക്ക 불가",
        "Kesavananda impact": "കേശവാനന്ദ സ്വാധീനം",
        "Waman Rao case": "വാമൻ റാവു കേസ്",
        "land reforms acts": "ഭൂ reform നിയമങ്ങൾ",
        "scheduled areas": "അനുബന്ധിത പ്രദേശങ്ങൾ",
        "scheduled tribes areas": "ഗിരിജന قبائل പ്രദേശങ്ങൾ",
        "TAC Tribes Advisory Council": "ഗിരിജന ഉപദേശക സമിതി",
        "autonomous district governor": "സ്വയംഭരണ ജില്ലാ ഭരണം",
        "autonomous districts": "സ്വയംഭരണ ജില്ലകൾ",
        "manipur autonomous district council": "മണിപ്പൂർ സ്വയംഭരണ ജില്ലാ കൗൺസിൽ",
        "santhal parganas": "സാന്താൽ പർഗനാസ്",
        "north cachar hills": "North Cachar Hills",
        "Parliament alone cannot": "പാർലമെന്റ് മാത്രം കഴിയില്ല",
        "election validity": "തിരഞ്ഞെടുപ്പ് സാധുത",
        "356-ന്റെ judicial review": "356-ന്റെ നീതിപരിശോധന",
        "habeas corpus": "ഹേബിയസ് കോർപ്പസ്",
        "privacy fundamental right": "സ്വകാര്യത മൗലികാവകാശം",
        "environment PIL": "പരിസ്ഥിതി PIL",
        "nationalisation compensation": "ദേശീയകരണ നഷ്ടപരിഹാരം",
        "bank nationalisation": "ബാങ്ക് ദേശീയകരണം",
        "reservation creamy layer": "സംവരണ ക്രീം ലെയർ",
        "religion in election": "തിരഞ്ഞെടുപ്പിൽ മതം",
        "OBC 27%": "27% OBC",
        "Hindutva election": "ഹിന്ദുത്വ തിരഞ്ഞെടുപ്പ്",
        "backward classes": "പിന്നോക്ക വർഗ്ഗങ്ങൾ",
        "corrupt practice religion": "ദുrachar religion",
        "reservation in promotion": "promotion-ൽ സംവരണം",
        "reservation promotion": "promotion-ൽ സംവരണം",
        "carry forward rule": "carry forward rule",
        "religion appeal": "മത appeal",
        "OBC creamy layer": "OBC ക്രീം ലെയർ",
        "OBC reservation 27%": "27% OBC സംവരണം",
        "backward classes employment": "പിന്നോക്ക വർഗ്ഗങ്ങളുടെ തൊഴിൽ",
        "socially/educationally backward": "സാമൂഹിക/വിദ്യാഭ്യാസ പിന്നോക്കം",
        "Lok Sabha SC/ST reservation": "ലോക്സഭ എസ്.സി./എസ്.ടി. സംവരണം",
        "Anglo-Indian nomination": "ആംഗ്ലോ-ഇന്ത്യൻ nomination",
        "State assembly SC/ST reservation": "നിയമസഭ എസ്.സി./എസ്.ടി. സംവരണം",
        "reservation duration": "സംവരണ കാലാവധി",
        "SC/ST claims": "എസ്.സി./എസ്.ടി. claims",
        "SC/ST advisory council": "എസ്.സി./എസ്.ടി. ഉപദേശക സമിതി",
        "Backward classes commission": "പിന്നോക്ക വർഗ്ഗ കമ്മീഷൻ",
        "SC list": "പട്ടികജാതി പട്ടിക",
        "ST list": "പട്ടികവർഗ്ഗ പട്ടിക",
        "panchayat reservation": "പഞ്ചായത്ത് സംവരണം",
        "panchayat women reservation": "പഞ്ചായത്ത് സ്ത്രീ സംവരണം",
        "municipality women reservation": "നഗരസഭാ സ്ത്രീ സംവരണം",
        "Maharashtra-Gujarat special provision": "മഹാരാഷ്ട്ര-ഗുജറാത്ത് പ്രത്യേക വ്യവസ്ഥ",
        "Nagaland special provision": "നാഗാലാൻഡ് പ്രത്യേക വ്യവസ്ഥ",
        "Assam special provision": "അസം പ്രത്യേക വ്യവസ്ഥ",
        "Manipur special provision": "മണിപ്പൂർ പ്രത്യേck വ്യവസ്ഥ",
        "Andhra Pradesh special provision": "ആന്ധ്രപ്രദേശ് പ്രത്യേക വ്യവസ്ഥ",
        "Sikkim special provision": "സിക്കിം പ്രത്യേക വ്യവസ്ഥ",
        "Mizoram special provision": "മിസോറം പ്രത്യേക വ്യവസ്ഥ",
        "Arunachal Pradesh special provision": "അരുണാചൽ പ്രദേശ് പ്രത്യേക വ്യവസ്ഥ",
        "Goa special provision": "ഗോവ പ്രത്യേക വ്യവസ്ഥ",
        "Hyderabad-Karnataka special provision": "ഹൈദരാബാദ്-കarnataka പ്രത്യേക വ്യവസ്ഥ",
        "Kalyana Karnataka special provision": "കalyana Karnataka പ്രത്യേക വ്യവസ്ഥ",
        "Jammu Kashmir special status repealed": "ജമ്മു-കാശ്മീർ പ്രത്യേക നില നീക്കം",
        "Central Administrative Tribunal": "കേന്ദ്ര ഭരണ ധികാരണ",
        "Income Tax Appellate Tribunal": "ആദായനികുതി അpellate ധികാരണ",
        "National Company Law Tribunal": "ദേശീയ കമ്പനി നിയമ ധികാരണ",
        "National Company Law Appellate Tribunal": "ദേശീയ കമ്പനി നിയമ അpellate ധികാരണ",
        "Securities Appellate Tribunal": "Securities Appellate Tribunal",
        "Telecom Disputes Settlement": "Telecom Disputes Settlement",
        "Armed Forces Tribunal": "Armed Forces Tribunal",
        "National Green Tribunal": "ദേശീയ പരിസ്ഥിതി ധികാരണ",
        "Debt Recovery Tribunal": "Debt Recovery Tribunal",
        "CAT": "കേന്ദ്ര ഭരണ ധികാരണ",
        "ITAT": "ആദായനികുതി അpellate ധികാരണ",
        "NCLT": "ദേശീയ കമ്പനി നിയമ ധികാരണ",
        "NCLAT": "ദേശീയ കമ്പനി നിയമ അpellate ധികാരണ",
        "SAT": "Securities Appellate Tribunal",
        "TDSAT": "Telecom Disputes Settlement",
        "AFT": "Armed Forces Tribunal",
        "NGT": "ദേശീയ പരിസ്ഥിതി ധികാരണ",
        "DRT": "Debt Recovery Tribunal",
        "pension ലabh്യമാക്കൽ": "വിരമണാനന്തര ആനുകൂല്യം",
    }
    for a, b in rep.items():
        s = s.replace(a, b)
    return s


def ok(s: str) -> bool:
    s = fix_text(s)
    if MIXED.search(s):
        return False
    if _LATIN4.search(ALLOWED.sub("", s)):
        return False
    return bool(s.strip())


def clean_pair(row: tuple[str, str]) -> tuple[str, str]:
    a, b = fix_text(row[0]), fix_text(row[1])
    if PH.match(b):
        m = re.search(r"അനുച്ഛേദം\s+(\d+[A-Z]?)", a)
        if m and m.group(1) in ARTICLE_TOPICS:
            b = ARTICLE_TOPICS[m.group(1)]
        else:
            return None
    if not ok(a) or not ok(b):
        return None
    return a, b


def clean_triple(row: tuple[str, str, str]) -> tuple[str, str, str] | None:
    a, b, c = fix_text(row[0]), fix_text(row[1]), fix_text(row[2])
    if not all(ok(x) for x in (a, b, c)):
        return None
    return a, b, c


def dedupe(rows: list) -> list:
    seen: set = set()
    out = []
    for r in rows:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


ARTICLE_TOPICS: dict[str, str] = {}
def apply_fix_row(row: tuple) -> tuple:
    if len(row) == 2:
        a, b = fix_text(row[0]), fix_text(row[1])
        m = re.search(r"അനുച്ഛേദം\s+(\d+[A-Z]?)", a)
        if m and (PH.match(b) or b.startswith("അനുച്ഛേദം")):
            num = m.group(1)
            if num in ARTICLE_TOPICS:
                b = ARTICLE_TOPICS[num]
        return a, b
    a, b, c = fix_text(row[0]), fix_text(row[1]), fix_text(row[2])
    return a, b, c


def build_article_topics_from_coi20(d) -> None:
    """Harvest real Malayalam topics from coi20_data; overlay hand-crafted topics."""
    for a, b in d.ARTICLES:
        m = re.search(r"അനുച്ഛേദം\s+(\d+[A-Z]?)", a)
        if not m:
            continue
        num = m.group(1)
        b2 = fix_text(b)
        if not PH.match(b2) and ok(b2):
            ARTICLE_TOPICS[num] = b2
    # Pure Malayalam supplements for common PSC articles
    extra = {
        "4": "അനുച്ഛേദം 4-ൽ പ്രതിപാദിക്കുന്നത്",
        "7": "പākിസ്താൻից കുടിയേറ്റക്കാരുടെ പൗരത്വം",
        "26": "മത/വിദ്യാഭ്യാസ സ്ഥാപനങ്ങൾ",
        "28": "മത/വിദ്യാഭ്യാസ സ്ഥാപനങ്ങൾ",
        "33": "സൈനിക/പോലീസ് ബalകാത്തലം",
        "41": "തൊഴിലവകാശം",
        "42": "humane conditions of work",
        "43": "living wage",
        "44": "ഏകീകൃത നagarika നിയമശൈലി",
        "45": "early childhood care",
        "46": "weak sections promotion",
        "47": "intoxicating drinks prohibition",
        "48": "agriculture and animal husbandry",
        "49": "monuments protection",
        "50": "judiciary separation",
        "53": "executive power of union",
        "55": "president election manner",
        "56": "president term",
        "57": "president re-election",
        "58": "president qualification",
        "59": "president conditions",
        "60": "president oath",
        "61": "president impeachment",
        "62": "president vacancy",
        "64": "vice president election",
        "65": "vice president as acting president",
        "75": "ministers appointment",
        "77": "executive conduct of government",
        "80": "rajya sabha composition",
        "81": "lok sabha composition",
        "82": "parliament constituency readjustment",
        "83": "parliament duration",
        "84": "parliament membership qualification",
        "101": "vacation of seats",
        "102": "disqualification",
        "103": "disqualification decision",
        "107": "passing of bills",
        "113": "procedure in parliament",
        "114": "appropriation bills",
        "115": "supplementary grants",
        "116": "votes on account",
        "117": "special appropriation",
        "118": "parliament rules",
        "119": "parliament language",
        "120": "joint sitting language",
        "121": "salaries of members",
        "122": "validity of proceedings",
        "125": "supreme court salaries",
        "127": "supreme court staff",
        "131": "original jurisdiction SC",
        "132": "appeal to supreme court",
        "133": "appeal in civil matters",
        "134": "appeal in criminal matters",
        "136": "special leave to appeal",
        "137": "review of SC judgments",
        "141": "law declared by SC binding",
        "143": "presidential reference to SC",
        "149": "CAG duties",
        "150": "CAG form of accounts",
        "154": "executive power of state",
        "155": "governor appointment",
        "156": "governor term",
        "157": "governor qualification",
        "158": "governor conditions",
        "159": "governor oath",
        "162": "extent of executive power of state",
        "164": "state ministers",
        "167": "state advocate general",
        "169": "abolition of legislative council",
        "170": "state assembly composition",
        "171": "legislative council composition",
        "213": "governor ordinance power",
        "214": "high courts",
        "226": "high court writ jurisdiction",
        "239": "union territory administration",
        "243A": "gram sabha",
        "243B": "panchayat constitution",
        "243C": "panchayat composition",
        "243D": "panchayat reservation",
        "243E": "panchayat duration",
        "243F": "panchayat disqualification",
        "243G": "panchayat powers",
        "243H": "panchayat finance",
        "243I": "panchayat audit",
        "243J": "panchayat finance commission",
        "243K": "state election commission",
        "243ZA": "municipality constitution",
        "243ZB": "municipality composition",
        "243ZC": "municipality reservation",
        "243ZD": "district planning committee",
        "243ZE": "metropolitan planning",
        "243ZI": "cooperative societies",
        "243ZJ": "cooperative election authority",
        "262": "inter-state water disputes",
        "268": "GST levy",
        "269": "GST taxes",
        "270": "tax distribution",
        "275": "grants in aid",
        "280": "finance commission",
        "300": "property of union and states",
        "302": "parliament trade restrictions",
        "303": "discrimination in trade",
        "304": "state trade restrictions",
        "305": "saving existing laws",
        "307": "appointed agency for trade",
        "312": "all india services",
        "316": "UPSC chairman/members",
        "320": "UPSC functions",
        "325": "no exclusion from electoral roll",
        "326": "adult suffrage",
        "329": "election disputes",
        "331": "anglo-indian nomination",
        "335": "SC/ST claims",
        "339": "SC/ST advisory council",
        "340": "backward classes commission",
        "341": "scheduled castes list",
        "342": "scheduled tribes list",
    }
    for k, v in extra.items():
        v2 = fix_text(v)
        if ok(v2):
            ARTICLE_TOPICS.setdefault(k, v2)


def patch_source(text: str) -> str:
    if "_ALLOWED_LATIN" not in text:
        text = text.replace(
            'MIXED = re.compile(r"[\\u0D00-\\u0D7F][a-zA-Z]|[a-zA-Z][\\u0D00-\\u0D7F]")\n\n\ndef _pool',
            'MIXED = re.compile(r"[\\u0D00-\\u0D7F][a-zA-Z]|[a-zA-Z][\\u0D00-\\u0D7F]")\n' + INSERT_AFTER_MIXED + "\n\ndef _pool",
        )
    old_add = '''def _add(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    q: str,
    ans: str,
    wrong: list[str],
    diff: str = "medium",
    pool: list[str] | None = None,
) -> None:
    if MIXED.search(q + ans + "".join(wrong)):
        return
    add_candidate(out, existing, rng, q, ans, wrong, diff, pool)'''
    if old_add in text:
        text = text.replace(old_add, NEW_ADD.strip())
    return text


def main() -> None:
    import coi20_data as d
    import pprint
    import _build_coi_wave20_clean as gen

    build_article_topics_from_coi20(d)

    # Start from coi20_data full volume; fix strings in place
    data: dict[str, list] = {}
    pair_names = [
        "PARTS", "FIRST_SCHEDULE", "SECOND_SCHEDULE", "THIRD_SCHEDULE",
        "FIFTH_SIXTH", "NINTH_SCHEDULE", "CASES", "AMEND_TYPES",
        "CENTRE_STATE", "FINANCE", "TRADE", "LANGUAGES", "RESERVATION",
        "ART371_SERIES", "COOPERATIVE", "TRIBUNALS", "PARLIAMENT", "FEATURES",
    ]
    for name in pair_names:
        rows = []
        for row in getattr(d, name):
            rows.append(apply_fix_row(row))
        data[name] = dedupe(rows)

    # RS seats Malayalam numerals
    rs_raw = [
        ("ഉത്തരപ്രദേശ്", 31), ("മഹാരാഷ്ട്ര", 19), ("തമിഴ്നാട്", 18),
        ("പശ്ചിമബംഗാൾ", 16), ("ബിഹാർ", 16), ("കർണാടക", 12),
        ("ആന്ധ്രപ്രദേശ്", 11), ("മധ്യപ്രദേശ്", 11), ("ഗുജറാത്ത്", 11),
        ("രാജസ്ഥാൻ", 10), ("ഒഡിഷ", 10), ("കേരളം", 9),
        ("തെലങ്കാന", 7), ("അസം", 7), ("പഞ്ചാബ്", 7),
        ("ഝാർഖണ്ഡ്", 6), ("ഛത്തീസ്ഗഡ്", 5), ("ഹരിയാന", 5),
        ("ജമ്മു-കശ്മീർ", 4), ("ഹിമാചൽ പ്രദേശ്", 3), ("ഉത്തരാഖണ്ഡ്", 3),
        ("ദില്ലി", 3), ("ഗോവ", 1), ("മണിപ്പൂർ", 1),
        ("മേഘാലയ", 1), ("മിസോറം", 1), ("നാഗാലാൻഡ്", 1),
        ("സിക്കിം", 1), ("ത്രിപുര", 1), ("പുതുച്ചേരി", 1),
        ("അരുണാചൽ പ്രദേശ്", 1),
    ]
    data["RS_SEATS"] = [(a, ml_num(n)) for a, n in rs_raw]

    # amendments — fix strings, keep all rows
    data["AMENDMENTS"] = dedupe([apply_fix_row(r) for r in d.AMENDMENTS])

    # articles — overlay topics for placeholders
    arts = []
    seen: set[str] = set()
    for a, b in d.ARTICLES:
        row = apply_fix_row((a, b))
        m = re.search(r"അനുച്ഛേദം\s+(\d+[A-Z]?)", row[0])
        if m:
            num = m.group(1)
            if num in ARTICLE_TOPICS:
                row = (row[0], ARTICLE_TOPICS[num])
            seen.add(num)
        arts.append(row)
    for num, topic in sorted(ARTICLE_TOPICS.items(), key=lambda x: (len(x[0]), x[0])):
        if num not in seen:
            arts.append((f"അനുച്ഛേദം {num}", topic))
    data["ARTICLES"] = dedupe(arts)

    data["BASIC_STRUCTURE"] = [
        ("കേശവാനന്ദ ഭാരതി കേസ്", "1973-ൽ അടിസ്ഥാന ഘടനാ സിദ്ധാന്തം"),
        ("മിനർവ മിൽസ് കേസ്", "1980-ൽ അടിസ്ഥാന ഘടനാ സിദ്ധാന്തം"),
        ("സമാഹിത സർക്കാർ", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("പാർലമെന്ററി ഭരണരീതി", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("മതേതരത്വം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("സംവിധാനത്തിന്റെ പരമാധികാരം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("നീതിപരിശോധന", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("അധികാര വേർതിരിവ്", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("സംഘടിതാധിപത്യം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("ജനാധിപത്യം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("നിയമത്തിന്റെ ആധിപത്യം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("സ്വതന്ത്രവും നീതിയുള്ളതുമായ തിരഞ്ഞെടുപ്പുകൾ", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("ദേശ ഐക്യവും സമഗ്രതയും", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("ക്ഷേമ രാഷ്ട്രം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("പരിമിത ഭേദഗതി അധികാരം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("മൗലികാവകാശങ്ങൾ", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("നിർദ്ദേശക തത്വങ്ങൾ", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("സ്വതന്ത്ര നിയമ പaalana", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("ഏകീകൃത നിയമ പaalana", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("ഏക പൗരത്വം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
    ]

    # regenerate file from _build template
    import _build_coi_wave20_clean as gen
    parts = [gen.HEADER]
    for name, val in data.items():
        parts.append(f"{name}: list = ")
        parts.append(pprint.pformat(val, width=120, sort_dicts=False))
        parts.append("\n\n")
    parts.append(gen.EMIT)
    out_text = patch_source("".join(parts))
    TARGET.write_text(out_text, encoding="utf-8")

    ns2: dict = {}
    exec(TARGET.read_text(encoding="utf-8"), ns2)
    pool = ns2["generate_wave20_candidates"](set(), random.Random(1))
    print("wrote", TARGET, "pool", len(pool))
    print("articles", len(data["ARTICLES"]), "amendments", len(data["AMENDMENTS"]))


if __name__ == "__main__":
    import pprint
    main()
