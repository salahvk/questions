#!/usr/bin/env python3
"""Apply Malayalam quiz cursor rules to JSON question files."""

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

from malayalamize_questions import (
    PRESERVE,
    malayalamize_question,
    malayalamize_text,
)

BASE = Path(__file__).parent
SKIP_FILES = {"english_language.json", "current_affairs_manifest.json"}
MALAYALAM = re.compile(r"[\u0D00-\u0D7F]")

# Allowed Latin tokens inside otherwise-Malayalam question stems (acronyms, years)
STEM_ACRONYMS = re.compile(
    r"\b(?:UDF|LDF|NDA|BJP|CPI|CPM|RSP|IUML|BDJS|MLA|MP|LS|FIFA|GST|ISRO|WHO|IMF|"
    r"WTO|ICC|ODI|T20|NEP|UPI|ECI|PTA|G20|NASA|RTE|IGNOU|NCERT|AIIMS|DRDO|"
    r"PM-JAY|PM-KISAN|ICDS|NSAP|NRHM|ABDM|KFON|IMEC|HAL|BHEL|ONGC|NTPC|"
    r"IOCL|SIDBI|KVIC|NALCO|BEL|BEML|DPIIT|ILO|FAO|IAEA|UNICEF|UNHCR|GATT|"
    r"USA|UAE|AYUSH|LPG|SEZ|STPI|MSME|NATO|OPEC|ASEAN|SAARC|BRICS|ICRC|"
    r"NITI|NGT|PWD|PLI|IMD|WANI|IN-SPACe|UNFCCC|ECI)\b",
    re.I,
)

# English filler leaked into Malayalam option sets
BANNED_OPTION_ENGLISH = re.compile(
    r"\b(?:only|always|linked|historically|enacted|winner|notable|approx|"
    r"forever|formation|includes|reservation|coalition|strong in|term length|"
    r"seats count|president|secretary|Leader|allied|bench cities)\b",
    re.I,
)

# Parenthetical content that may stay (acronyms, org names, place hints in Malayalam)
KEEP_PAREN = re.compile(
    r"^(UNESCO|GDP|RTE|IGNOU|NCERT|AIIMS|ISRO|DRDO|GST|IMF|WHO|WTO|FIFA|ICC|"
    r"IPL|ODI|T20|NEP|UPI|ECI|IMD|NGT|PWD|PLI|NITI|ICRC|BRICS|ASEAN|SAARC|"
    r"NATO|OPEC|EU|HAL|BHEL|ONGC|NTPC|IOCL|SIDBI|KVIC|NALCO|BEL|BEML|"
    r"PM-JAY|PM-KISAN|ICDS|NSAP|NRHM|ABDM|WANI|IN-SPACe|NASA|UNFCCC|G20|"
    r"KFON|IMEC|BJP|UDF|LDF|NDA|CPI|CPM|RSP|IUML|BDJS|PTA|MSME|SEZ|STPI|"
    r"DPIIT|ILO|FAO|IAEA|UNICEF|UNHCR|GATT|USA|UAE|AYUSH|80G|LPG|"
    r"Knot|NaCl|H2O|CO2|O2|DNA|RNA|ATP|pH|UV|IR|OR|AND|PART|III|II|IV|I)$",
    re.I,
)

# English glued to Malayalam suffixes (World Cup-ന്റെ etc.)
HYPHEN_GLUED = [
    (re.compile(r"FIFA Club World Cup-ന്റെ", re.I), "FIFA ക്ലബ് ലോകകപ്പിന്റെ"),
    (re.compile(r"FIFA World Cup-ന്റെ", re.I), "FIFA ലോകകപ്പിന്റെ"),
    (re.compile(r"World Cup-ന്റെ", re.I), "ലോകകപ്പിന്റെ"),
    (re.compile(r"match-ന്റെ", re.I), "മത്സരത്തിന്റെ"),
    (re.compile(r"team-ൽ", re.I), "ടീമിൽ"),
]

PAREN_ENGLISH = re.compile(r"\s*\(([A-Za-z0-9][^)]*)\)")

# Corrupted text from partial English→Malayalam conversion
CORRUPTION_FIXES: list[tuple[str, str]] = [
    ("തുmanaged പാട്ടുകൾ", "ഭജന പാട്ടുകൾ"),
    ("തുmanaged തുള്ളൽ", "തുമ്പി തുള്ളൽ"),
    ("ദുശ്ശblockസനൻ", "ദുശ്ശാസനൻ"),
    ("മണ്ണrules", "മണ്ണ് കുഴിച്ചെടുക്കുന്ന"),
    ("തrenown പാണ്ടി", "ചെണ്ട പാണ്ടി"),
    ("തുrenown കുമ്മാട്ടി", "തിരുവോണ കുമ്മാട്ടി"),
    ("ബ beaux-arts", "ബിയോ-ആർട്സ്"),
    ("റേ മാഗ്default", "റേനേ മാഗ്രitte"),
    ("ഹാcomplജനുകൾ", "ഹാലോജനുകൾ"),
    ("അArrhenius", "ആര്രിണിയസ്"),
    ("പട്ടുനൂൽ നെcontinuous", "പട്ടുനൂൽ നെയ്ത"),
    ("വെളുപ്പ് / ഓഫ്-വൈറ്റ് (കസവ് ബോർഡറോട് കൂടിയത്)", "വെളുപ്പ് / കസവ് ബോർഡറോട് കൂടിയത്"),
    ("നാഗര വാസ്തുവിദ്യ (Nagara Architecture / ചന്ദേല ശൈലി)", "നാഗര വാസ്തുവിദ്യ (ചന്ദേല ശൈലി)"),
    ("'ദി പെർസിസ്റ്റൻസ് ഓഫ് മെമ്മറി' (The Persistence of Memory - ഉരുകുന്ന വാച്ചുകൾ)", "'The Persistence of Memory' (ഉരുകുന്ന വാച്ചുകൾ)"),
    ("heavy water (ഭാരജലം)", "ഭാരജലം"),
    ("'എത്തanol'", "'എthalcohol'"),
    ("'ഓzone'", "'ഓzone'"),
    ("റേനേ മാഗ്രitte", "റെനെ മാഗ്രitte"),
    ("ദുശ്ശusageനൻ", "ദുശ്ശാസനൻ"),
    ("കumbalMain", "കumbalam"),
    ("alaMain", "alam"),
    ("കumbalaMain", "കumbalam"),
    ("കരിcoal", "കരിക്കാൽ"),
    ("വിഷാnumൂർത്തി", "വിഷ്ണുമൂർത്തി"),
    ("കakkahistory", "കാക്കാരിശ്ശി"),
    ("എlakkahistory", "കുറുമ്പാർ നൃത്തം"),
    ("സുബSub", "സുബ്ബാഹുല്ലാഹ്"),
    ("കൈholding", "കൈപിടിച്ച"),
    ("Early morning", "പ്രഭാത"),
    ("മാregular", "മാർഗ"),
    ("ചott", "ചോറ്റ"),
    ("ളMain", "ളം"),
    (" (Fauvism - വന്യമായ നിറങ്ങളുടെ ഉപയോഗം)", ""),
    (" (Mount Rushmore - പ്രസിഡന്റുമാരുടെ മുഖങ്ങൾ)", " (പ്രസിഡന്റുമാരുടെ മുഖങ്ങൾ)"),
    (" (Fourth Wall - നാലാം മതിൽ)", " (നാലാം മതിൽ)"),
    (" (Messiah - ഹല്ലേലൂയ കോറസ് അടങ്ങിയത്)", " (ഹല്ലേലൂയ കോറസ് അടങ്ങിയത്)"),
    (" (Symphony No. 9 - ചിരന്തന ഗീതം)", " (ചിരന്തന ഗീതം)"),
    (" (The Beatles - ജോർജ്ജ് ഹാരിസൺ)", " (ജോർജ്ജ് ഹാരിസൺ)"),
    (" (David - വെങ്കല രൂപം)", " (വെങ്കല രൂപം)"),
    (" (Tarpa - ഒരു തരം വലിയ പുല്ലാങ്കുഴൽ വാദ്യം)", " (ഒരു തരം വലിയ പുല്ലാങ്കുഴൽ വാദ്യം)"),
    ("A Version 5.25", " പതിപ്പ് 5.25"),
    ("Version 5.25", "പതിപ്പ് 5.25"),
    ("ചാരvaka", "ചാർവാക"),
    ("നവരasa", "നവറസം"),
    ("ഡemocritus", "ഡമോക്രിതസ്"),
    ("സോക്രATES", "സോക്രatis"),
    ("പ്ലato", "പ്ലato"),
    ("അറിസ്റ്റോട്ടil", "അറിസ്റ്റോട്ടil"),
    ("ക്ഷാരമൃത്തിregular", "ക്ഷാരഭൂമി"),
    ("തോട്ടiculture", "കൃഷി"),
    ("ഹermann Gundert", "ഹermann ഗundert"),
    ("സാൽzburg", "സാzburg"),
    ("മandi", "മandi"),
    ("വIDI", "വidy"),
    ("എthalcohol", "എthalcohol"),
    ("എത്തanol", "എthalcohol"),
    ("ഓzone", "ഓzone"),
    ("മാഗ്രitte", "മാഗ്രitte"),
]

# Manual fixes for corrupted entries
MANUAL_FIXES: dict[str, dict] = {
    "art_491": {
        "options": [
            "Campbell's Soup Cans",
            "കോക്കകോള ബോട്ടിലുകൾ",
            "മെർലിൻ മൺറോ രൂപങ്ങൾ",
            "ബലൂൺ ഡോഗ്",
        ],
        "answer": "Campbell's Soup Cans",
    },
    "art_731": {
        "answer": "വലിയ കത്തി പോലുള്ള ആകൃതിയിലുള്ള ചുട്ടിപ്പാലകൾ",
    },
    "art_756": {
        "options": ["പുളിമരം", "തേക്ക്", "മുള", "പ്ലാവ്"],
        "answer": "പുളിമരം",
    },
    "cin_008": {
        "options": ["ശിവ കങ്ക", "ഛോട്ടാ ചേതൻ", "മൈ ഡിയർ കുട്ടിച്ചാത്തൻ", "ഹക്കുസ് ബക്കുസ്"],
    },
    "ca_2026_06_022": {
        "question": "2026 ജൂണിൽ FIFA ക്ലബ് ലോകകപ്പിന്റെ ആതിഥ്യ രാജ്യം ഏത്?",
    },
    "eco_161": {
        "answer": "50",
    },
    "eco_762": {
        "question": "ബാങ്കുകൾ വായ്പയ്ക്ക് ഈടാക്കുന്ന പലിശ നിരക്ക് സാധാരണയായി എന്ത് എന്ന് വിളിക്കുന്നു?",
        "options": [
            "വിപണി മൂലധനം",
            "വായ്പ പലിശ നിരക്ക്",
            "നികുതി നിരക്ക്",
            "വിനിമയ നിരക്ക്",
        ],
        "answer": "വായ്പ പലിശ നിരക്ക്",
    },
    "eco_769": {
        "question": "ബാങ്ക് ഇടപാടുകൾ ഫോണിലൂടെ നടത്താൻ ഉപയോഗിക്കുന്ന സൗകര്യം എന്താണ്?",
        "options": [
            "ചെക്ക് ബുക്ക്",
            "മൊബൈൽ ബാങ്കിംഗ് ആപ്പ്",
            "ഡിമാൻഡ് ഡ്രാഫ്റ്റ്",
            "പോസ്റ്റൽ ഓർഡർ",
        ],
        "answer": "മൊബൈൽ ബാങ്കിംഗ് ആപ്പ്",
    },
    "edu_582": {
        "question": "IIT Mandi ഏത് നഗരത്തിലാണ്?",
        "options": ["മandi", "റൂർക്കി", "ഗുവാഹാടി", "ഹൈദരാബാദ്"],
        "answer": "മandi",
    },
    "hok_283": {
        "options": ["ഹermann ഗundert", "കെ. കേളപ്പൻ", "ടി.കെ. മാധവൻ", "ചന്ദു മേനോൻ"],
        "answer": "ഹermann ഗundert",
    },
    "mi_096": {
        "options": ["കൃഷി", "ഗോതമ്പ്", "എണ്ണയിട വിത്തുകൾ", "മുട്ട"],
        "answer": "കൃഷി",
    },
    "phi_062": {
        "question": "സോക്രatis-ന്റെ ശിഷ്യൻ?",
        "options": ["Heraclitus", "അറിസ്റ്റോട്ടil", "പ്ലato", "ഡമോക്രിതസ്"],
        "answer": "പ്ലato",
    },
    "phi_063": {
        "question": "പ്ലato-യുടെ ശിഷ്യൻ?",
        "options": ["Socrates", "Kant", "സോക്രatis", "അറിസ്റ്റോട്ടil"],
        "answer": "അറിസ്റ്റോട്ടil",
    },
    "phi_064": {
        "question": "അറിസ്റ്റോട്ടil-ന്റെ ഗുരു?",
        "options": ["പ്ലato", "സോക്രatis", "Descartes", "Kant"],
        "answer": "പ്ലato",
    },
}


def strip_redundant_english_parens(text: str) -> str:
    """Remove (English gloss) when Malayalam already present; keep allowed acronyms."""
    if not text or not MALAYALAM.search(text):
        return text

    def repl(match: re.Match[str]) -> str:
        inner = match.group(1).strip()
        if MALAYALAM.search(inner):
            return f" ({inner})"
        if KEEP_PAREN.match(inner):
            return f" ({inner})"
        if PRESERVE.search(inner) and len(inner.split()) <= 3:
            return f" ({inner})"
        # Bilingual gloss: Malayalam (English) or English (Malayalam) — drop English half
        if re.search(r"[a-zA-Z]{2,}", inner):
            return ""
        return ""

    return PAREN_ENGLISH.sub(repl, text)


def fix_hyphen_glued(text: str) -> str:
    result = text
    for pattern, replacement in HYPHEN_GLUED:
        result = pattern.sub(replacement, result)
    return result


def fix_corruptions(text: str) -> str:
    for old, new in CORRUPTION_FIXES:
        if old in text:
            text = text.replace(old, new)
    return text


def clean_text(text: str) -> str:
    text = fix_corruptions(text)
    text = malayalamize_text(text)
    text = strip_redundant_english_parens(text)
    text = fix_hyphen_glued(text)
    text = re.sub(r"  +", " ", text).strip()
    return text


def closest_option(answer: str, options: list[str]) -> str | None:
    best, score = None, 0.0
    for opt in options:
        s = SequenceMatcher(None, answer.lower(), opt.lower()).ratio()
        if s > score:
            score, best = s, opt
    return best if score >= 0.55 else None


def apply_manual_fix(q: dict) -> bool:
    qid = q.get("id", "")
    fix = MANUAL_FIXES.get(qid)
    if not fix:
        return False
    changed = False
    for key, val in fix.items():
        if q.get(key) != val:
            q[key] = val
            changed = True
    return changed


def process_question(q: dict) -> tuple[dict, bool]:
    new_q = dict(q)
    changed = apply_manual_fix(new_q)

    for field in ("question", "answer"):
        old = new_q.get(field, "")
        new = clean_text(old)
        if new != old:
            new_q[field] = new
            changed = True

    new_opts = []
    for opt in new_q.get("options", []):
        new_opt = clean_text(opt)
        if new_opt != opt:
            changed = True
        new_opts.append(new_opt)
    new_q["options"] = new_opts

    mal_q, mal_changed = malayalamize_question(new_q)
    if mal_changed:
        new_q = mal_q
        changed = True

    ans = new_q.get("answer", "")
    opts = new_q.get("options", [])
    if ans not in opts:
        match = closest_option(ans, opts)
        if match:
            new_q["answer"] = match
            changed = True

    return new_q, changed


def dedupe_questions(questions: list[dict], filename: str) -> tuple[list[dict], int]:
    seen: set[str] = set()
    result: list[dict] = []
    removed = 0
    for q in questions:
        text = q.get("question", "").strip()
        if text and text in seen:
            removed += 1
            continue
        if text:
            seen.add(text)
        result.append(q)
    return result, removed


def process_file(filename: str) -> dict:
    path = BASE / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.get("questions", [])
    updated = 0
    fixed_questions: list[dict] = []

    for q in questions:
        new_q, changed = process_question(q)
        if changed:
            updated += 1
        fixed_questions.append(new_q)

    deduped, dup_removed = dedupe_questions(fixed_questions, filename)
    data["questions"] = deduped
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "filename": filename,
        "total": len(deduped),
        "updated": updated,
        "duplicates_removed": dup_removed,
    }


def strip_allowed_stem_english(text: str) -> str:
    """Remove allowed acronyms/years so we can detect stray English in Malayalam stems."""
    result = STEM_ACRONYMS.sub("", text)
    result = re.sub(r"\b(?:19|20)\d{2}\b", "", result)
    result = PAREN_ENGLISH.sub("", result)
    return result


def validate_file(filename: str) -> list[tuple]:
    path = BASE / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    issues = []
    for q in data.get("questions", []):
        qid = q.get("id", "?")
        question = q.get("question", "")
        opts = q.get("options", [])
        ans = q.get("answer", "")
        if len(opts) != 4:
            issues.append((qid, "options_count", len(opts)))
        if ans not in opts:
            issues.append((qid, "answer_mismatch", ans))

        if not MALAYALAM.search(question):
            issues.append((qid, "english_only_question", question[:100]))
        elif re.search(r"[a-zA-Z]{4,}", strip_allowed_stem_english(question)):
            issues.append((qid, "mixed_language_stem", question[:100]))

        has_malayalam_option = any(MALAYALAM.search(o) for o in opts)
        for opt in opts:
            if BANNED_OPTION_ENGLISH.search(opt):
                issues.append((qid, "english_option_leak", opt[:100]))
            elif (
                has_malayalam_option
                and not MALAYALAM.search(opt)
                and re.search(r"[a-zA-Z]{4,}", opt)
                and not re.fullmatch(r"[\d%./\s\-+()A-Za-z]+", opt)
            ):
                # Allow deliberate English acronym distractors (e.g. United Democratic Front)
                if not re.search(
                    r"\b(?:Front|Forum|Force|Defence|Development|Union|Liberal|Local|Left|Unified)\b",
                    opt,
                ):
                    issues.append((qid, "mixed_language_options", opt[:100]))

        for text in [question, *opts, ans]:
            cleaned = PRESERVE.sub("", text)
            if re.search(r"[a-zA-Z]{4,}", cleaned) and not re.search(
                r"^[\u0D00-\u0D7F\s\d\W]+$", text
            ):
                if MALAYALAM.search(text):
                    issues.append((qid, "english_leak", text[:100]))
    return issues


def main(files: list[str] | None = None) -> None:
    targets = files or sorted(
        p.name for p in BASE.glob("*.json") if p.name not in SKIP_FILES
    )
    print("Applying Malayalam cursor rules...\n")
    for fname in targets:
        if not (BASE / fname).exists():
            print(f"  SKIP (missing): {fname}")
            continue
        stats = process_file(fname)
        issues = validate_file(fname)
        print(
            f"  {fname}: {stats['total']} questions, "
            f"{stats['updated']} updated, "
            f"{stats['duplicates_removed']} dupes removed, "
            f"{len(issues)} remaining issues"
        )


if __name__ == "__main__":
    import sys

    file_list = sys.argv[1:] if len(sys.argv) > 1 else None
    main(file_list)
