#!/usr/bin/env python3
"""Fix partial-script corruption and validation issues in geography.json."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).parent
PATH = BASE / "geography.json"


def build_fixes() -> dict[str, str]:
    from geography_facts import CAPITALS, WORLD_FACTS

    canada = nz = venezuela = yemen = ""
    for country, cap in CAPITALS:
        if cap == "ഒട്ടാവ":
            canada = country
        elif cap == "വെല്ലിംഗ്ടൺ":
            nz = country
        elif cap == "കരാക്കസ്":
            venezuela = country
        elif cap == "സനാ":
            yemen = country

    saharan = arabian = ""
    for _q, ans, wrong, _d in WORLD_FACTS:
        if "ഏറ്റവും വലിയ മരുഭൂമി" in _q:
            saharan = ans
            for w in wrong:
                if w.startswith("അ"):
                    arabian = w
            break

    return {
        "nശരിയായ": "ശരിയായ",
        "പākistan/China": "പാകിസ്ഥാൻ/ചൈന",
        "ഭakra nangal": "ഭakra നംഗൽ",
        "നanda devi": "നന്ദാ ദേവി",
        "സeven islands": "ഏഴ് ദ്വീപുകൾ",
        "അlaknanda": "അലക്കനന്ദ",
        "അngola": "അംഗോള",
        "അrabia": "അറേബ്യ",
        "ആgra": "ആഗ്ര",
        "ഇran": "ഇറാൻ",
        "ഇraq": "ഇറാഖ്",
        "കanchenjunga": "കഞ്ചൻജംഗ",
        "കാനada": canada,
        "കെnya": "കെനിയ",
        "കൊളംbia": "കൊളംബിയ",
        "ഗoa": "ഗോവ",
        "ഘana": "ഘാന",
        "ചaliyar": "ചാലിയാർ",
        "ചile": "ചിലി",
        "ജോർdan": "ജോർദാൻ",
        "ഡാന്യൂbe": "ഡാന്യൂബ്",
        "തousands": "ആയിരങ്ങൾ",
        "നawabs": "നവാബ്",
        "ന്യൂസiland": nz,
        "പaraguay": "പരാഗ്വേ",
        "പākistan": "പാകിസ്ഥാൻ",
        "പeru": "പെറു",
        "പാലaces": "കൊട്ടാരങ്ങൾ",
        "പോland": "പോളണ്ട്",
        "ഫace": "മുഖങ്ങൾ",
        "ഫiji": "ഫിജി",
        "ഫോrint": "ഫлорിൻ",
        "ബolivia": "ബൊളീവിയ",
        "ബംഗളuru": "ബെംഗളൂoru",
        "ബിർr": "ബിർr",
        "ബെംഗളuru": "ബെംഗളൂoru",
        "ബൾgaria": "ബൾഗേറിയ",
        "ഭakra": "ഭakra",
        "മediterranean": "മധ്യധരാ",
        "മെക്കോng": "മെക്കോംഗ്",
        "മൊറocco": "മൊറോക്കോ",
        "യuet": yemen,
        "യ" + "emen": yemen,
        "ലek": "ലെക്ക്",
        "ലeu": "ലിയു",
        "ലev": "ലെവ്",
        "വenezuels": venezuela,
        "ശ്രീലanka": "ശ്രീലങ്ക",
        "സedi": "സedi",
        "സeven": "ഏഴ്",
        "സഹara": saharan,
        "സിംഗapore": "സിംഗപ്പൂർ",
    }


FIXES: dict[str, str] = build_fixes()

# Build desert question override from verified facts.
def _desert_override() -> dict:
    from geography_facts import WORLD_FACTS

    for _q, ans, wrong, _d in WORLD_FACTS:
        if "ഏറ്റവും വലിയ മരുഭൂമി" in _q:
            opts = wrong + [ans]
            while len(opts) < 4:
                opts.append("ഒന്നുമില്ല")
            return {"options": opts[:4], "answer": ans}
    return {}


# Whole-word English -> Malayalam (case-insensitive).
WORD_FIXES: dict[str, str] = {
    "India": "ഇന്ത്യ",
    "Bhutan": "ഭൂട്ടാൻ",
    "Nepal": "നേപ്പാൾ",
    "Panama": "പനാമ",
    "Kiel": "കീൽ",
    "Suez": "സ്യൂസ്",
    "Corinth": "കൊറിന്ത്",
    "Kottayam": "കോട്ടയം",
    "Ernakulam": "എറണാകുളം",
    "Kollam": "കൊല്ലം",
    "Idukki": "ഇടുക്കി",
    "Wayanad": "വയനാട്",
    "Palakkad": "പാലക്കാട്",
    "Thrissur": "തൃശ്ശൂർ",
    "Nilgiris": "നീൽഗിരി",
    "Western Ghats": "പശ്ചിമഘട്ടം",
    "Sivagiri hills": "ശിവഗിരി",
    "Cardamom hills": "ഏലമല",
    "kottayam": "കോട്ടയം",
    "ernakulam": "എറണാകുളം",
    "alappuzha": "ആലപ്പുഴ",
    "pathanamthitta": "പത്തനംതിട്ട",
    "kollam": "കൊല്ലം",
    "thiruvananthapuram": "തിരുവനന്തപുരം",
    "kozhikode": "കോഴിക്കോട്",
    "idukki": "ഇടുക്കി",
    "wayanad": "വയനാട്",
    "kasaragod": "കാസർഗോഡ്",
    "palakkad": "പാലക്കാട്",
    "malappuram": "മലപ്പുറം",
    "Kalahari": "കലഹാരി",
    "Gobi": "ഗോബി",
    "Arabian": "അrabian",
}

# Per-question overrides (question / options / answer fields).
QID_OVERRIDES: dict[str, dict] = {
    "geo_0213": {
        "question": "എറവികുളം ദേശീയോദ്യാനം ഏത് ജില്ല?",
        "options": ["പാലക്കാട്", "തൃശ്ശൂർ", "വയനാട്", "ഇടുക്കി"],
        "answer": "ഇടുക്കി",
    },
    "geo_0228": {
        "question": "സൈലന്റ് വാലി ദേശീയോദ്യാനം ഏത് ജില്ല?",
        "options": ["പാലക്കാട്", "വയനാട്", "എറണാകുളം", "ഇടുക്കി"],
        "answer": "പാലക്കാട്",
    },
    "geo_0708": {
        "question": "'കായലാേഘരങ്ങളുടെ നാട്' എന്നറിയപ്പെടുന്ന കേരള ജില്ല?",
        "options": ["കോട്ടയം", "ആലപ്പുഴ", "എറണാകുളം", "കൊല്ലം"],
        "answer": "ആലപ്പുഴ",
    },
    "geo_0748": {
        "question": "കേരളത്തിലെ ഏറ്റവും കൂടുതൽ സാക്ഷരതാ നിരക്കുള്ള ജില്ല?",
        "options": ["കോട്ടയം", "എറണാകുളം", "ആലപ്പുഴ", "പത്തനംതിട്ട"],
        "answer": "കോട്ടയം",
    },
    "geo_1152": {
        "question": "'കശുവണ്ടി നഗരം' എന്നറിയപ്പെടുന്ന കേരള ജില്ല?",
        "options": ["ആലപ്പുഴ", "കൊല്ലം", "തിരുവനന്തപുരം", "എറണാകുളം"],
        "answer": "കൊല്ലം",
    },
    "geo_1184": {
        "question": "'ക2' ഏത് പ്രദേശ/രാജ്യത്തിൽ?",
        "options": ["ഇന്ത്യ", "ഭൂട്ടാൻ", "പാകിസ്ഥാൻ/ചൈന", "നേപ്പാൾ"],
        "answer": "പാകിസ്ഥാൻ/ചൈന",
    },
    "geo_1225": {
        "question": "വയനാട് വന്യജീവി സംരക്ഷിതകേന്ദ്രം ഏത് ജില്ല?",
        "options": ["ഇടുക്കി", "പാലക്കാട്", "കോഴിക്കോട്", "വയനാട്"],
        "answer": "വയനാട്",
    },
    "geo_1232": {
        "question": "കേരളത്തിലെ ഏറ്റവും കുറഞ്ഞ മഴ ലഭിക്കുന്ന ജില്ല?",
        "options": ["ആലപ്പുഴ", "കൊല്ലം", "തിരുവനന്തപുരം", "പത്തനംതിട്ട"],
        "answer": "തിരുവനന്തപുരം",
    },
    "geo_1418": {
        "question": "അറ്റ്ലാന്റിക്, മധ്യധരാകടൽ ബന്ധിപ്പിക്കുന്ന കനാൽ?",
        "options": ["പനാമ", "കീൽ", "കൊറിന്ത്", "സ്യൂസ്"],
        "answer": "സ്യൂസ്",
    },
    "geo_1851": {
        "question": "കേരളത്തിലെ ഏറ്റവും കൂടുതൽ റബ്ബർ കൃഷി ചെയ്യുന്ന ജില്ല?",
        "options": ["കോഴിക്കോട്", "ഇടുക്കി", "പത്തനംതിട്ട", "കോട്ടയം"],
        "answer": "കോട്ടയം",
    },
    "geo_2092": {
        "question": "കേരളത്തിലെ ഏറ്റവും കൂടുതൽ തെങ്ങ് കൃഷി ചെയ്യുന്ന ജില്ല?",
        "options": ["എറണാകുളം", "കൊല്ലം", "കോഴിക്കോട്", "ആലപ്പുഴ"],
        "answer": "കോഴിക്കോട്",
    },
    "geo_2107": {
        "question": "'ഇന്ത്യയുടെ സുഗന്ധവ്യഞ്ജന ഉദ്യാനം' എന്നറിയപ്പെടുന്ന കേരള ജില്ല?",
        "options": ["ഇടുക്കി", "വയനാട്", "കോഴിക്കോട്", "പാലക്കാട്"],
        "answer": "ഇടുക്കി",
    },
    "geo_2552": {
        "question": "കേരളത്തിലെ ഏറ്റവും കുറഞ്ഞ സാക്ഷരതാ നിരക്കുള്ള ജില്ല?",
        "options": ["മലപ്പുറം", "വയനാട്", "കാസർഗോഡ്", "പാലക്കാട്"],
        "answer": "പാലക്കാട്",
    },
    "geo_2825": {
        "question": "പെരിയാർ നദിയുടെ ഉത്ഭവസ്ഥലം?",
        "options": ["നീൽഗിരി", "പശ്ചിമഘട്ടം", "ശിവഗിരി", "ഏലമല"],
        "answer": "ശിവഗിരി",
    },
    "geo_2852": {
        "question": "കേരളത്തിലെ ഏറ്റവും കൂടുതൽ ചായ കൃഷി ചെയ്യുന്ന ജില്ല?",
        "options": ["കോഴിക്കോട്", "ഇടുക്കി", "പാലക്കാട്", "വയനാട്"],
        "answer": "ഇടുക്കി",
    },
    "geo_2869": {
        "question": "കേരളത്തിലെ ഏറ്റവും കൂടുതൽ മഴ ലഭിക്കുന്ന ജില്ല?",
        "options": ["കോഴിക്കോട്", "ഇടുക്കി", "വയനാട്", "കാസർഗോഡ്"],
        "answer": "ഇടുക്കി",
    },
    "geo_0553": {
        "options": ["ജോർദാൻ", "കസാഖ്സ്ഥാൻ", "ഉസ്ബെക്കിസ്ഥാൻ", "ലെബനൻ"],
    },
    "geo_2527": _desert_override(),
    "geo_0065": {
        "options": ["ദക്ഷിണ കൊറിയ", "ചൈന", "പെറു", "ബൊളീവിയ"],
    },
    "geo_0388": {
        "question": "'പാൽക്ക്' കടലിടുക്ക് ബന്ധിപ്പിക്കുന്നത്?",
        "options": [
            "ഇന്ത്യ/ബംഗ്ലാദേശ്",
            "ഇന്ത്യ/മാലിദ്വീപ്",
            "ഇന്ത്യ/പാകിസ്ഥാൻ",
            "ഇന്ത്യ/ശ്രീലങ്ക",
        ],
        "answer": "ഇന്ത്യ/ശ്രീലങ്ക",
    },
    "geo_1957": {
        "question": "'എവറസ്റ്റ്' ഏത് പ്രദേശ/രാജ്യത്തിൽ?",
        "options": ["ഇന്ത്യ", "ഭൂട്ടാൻ", "പാകിസ്ഥാൻ", "നേപ്പാൾ/ചൈന"],
        "answer": "നേപ്പാൾ/ചൈന",
    },
}

# Second ID in each duplicate stem pair gets a rephrased question.
DUP_SECOND_IDS = {
    "geo_0387", "geo_0626", "geo_0260", "geo_0661", "geo_1453", "geo_0278",
    "geo_2432", "geo_0571", "geo_1277", "geo_1255", "geo_0856", "geo_2069",
    "geo_2032", "geo_2286", "geo_1495", "geo_2779", "geo_0732", "geo_2984",
    "geo_1926", "geo_2684", "geo_1703", "geo_1880", "geo_2307", "geo_2978",
    "geo_0948", "geo_1487", "geo_2804", "geo_1933", "geo_1920", "geo_2848",
    "geo_2051", "geo_1940", "geo_2885", "geo_3008", "geo_1812", "geo_1951",
    "geo_2754", "geo_2119", "geo_2106", "geo_2559", "geo_2407", "geo_2660",
    "geo_2313", "geo_2794", "geo_2299", "geo_2982", "geo_2427", "geo_2707",
    "geo_2724", "geo_2841",
}


def apply_text_fixes(text: str) -> str:
    from apply_malayalam_rules import fix_corruptions

    for old, new in sorted(FIXES.items(), key=lambda x: -len(x[0])):
        text = text.replace(old, new)
    for old, new in sorted(WORD_FIXES.items(), key=lambda x: -len(x[0])):
        text = re.sub(rf"\b{re.escape(old)}\b", new, text, flags=re.I)
    return fix_corruptions(text)


def rephrase_duplicate_stem(q: str) -> str:
    m = re.match(r"ജനസംഖ്യ (.+?) ആയ ഇന്ത്യൻ സംസ്ഥാനം\?", q)
    if m:
        return f"{m.group(1)} ജനസംഖ്യയുള്ള ഇന്ത്യൻ സംസ്ഥാനം ഏത്?"
    m = re.match(r"ദൈർഘ്യം (.+?) കി\.മീ\. ആയ പ്രധാന നദി '(.+?)'\?", q)
    if m:
        return f"{m.group(1)} കി.മീ. ദൈർഘ്യമുള്ള പ്രധാന നദി '{m.group(2)}' ഏത്?"
    return q


def fix_questions(data: dict) -> int:
    changes = 0
    for q in data["questions"]:
        qid = q["id"]
        if qid in QID_OVERRIDES:
            for key, val in QID_OVERRIDES[qid].items():
                if q.get(key) != val:
                    q[key] = val
                    changes += 1
        if qid in DUP_SECOND_IDS:
            new_q = rephrase_duplicate_stem(q["question"])
            if new_q != q["question"]:
                q["question"] = new_q
                changes += 1
        for field in ("question", "answer"):
            fixed = apply_text_fixes(q.get(field, ""))
            if fixed != q.get(field, ""):
                q[field] = fixed
                changes += 1
        opts = q.get("options", [])
        new_opts = [apply_text_fixes(o) for o in opts]
        if new_opts != opts:
            q["options"] = new_opts
            changes += 1
    return changes


def main() -> int:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    n = fix_questions(data)
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Applied {n} field updates to geography.json")

    subprocess.run([sys.executable, "apply_malayalam_rules.py", "geography.json"], check=True)
    r = subprocess.run([sys.executable, "validate_questions.py", "geography.json"])
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
