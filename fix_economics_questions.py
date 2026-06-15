#!/usr/bin/env python3
"""Fix bulk filler / definition-template corruption in economics.json."""

from __future__ import annotations

import json
import random
import re
from pathlib import Path

BASE = Path(__file__).parent
PATH = BASE / "economics.json"

# Keep manually rewritten questions untouched.
SKIP_IDS = {
    "eco_762",
    "eco_769",
    "eco_774",
    "eco_775",
    "eco_776",
    "eco_777",
    "eco_778",
    "eco_779",
    "eco_780",
    "eco_781",
    "eco_782",
    "eco_783",
    "eco_784",
}

WRAP_RE = re.compile(
    r"^സാമ്പത്തികമായി (.+?) എന്നതിനെ സൂചിപ്പിക്കുന്ന പ്രവർത്തി$"
)
PROC_RE = re.compile(
    r"^(?:നികുതി സംവിധാനത്തിൽ|വിപണിയിൽ|ബാങ്കിംഗിൽ|അന്താരാഷ്ട്ര വ്യാപാരത്തിൽ) "
    r"(.+?) നടപ്പിലാക്കുന്ന പ്രക്രിയ$"
)
BANKING_PREFIX_RE = re.compile(
    r"^ബാങ്കിംഗിൽ തിരിച്ചറിയലിനും ഇടപാടുകൾക്കായി ഉപയോഗിക്കുന്ന — (.+)$"
)
TERM_RE = re.compile(r"'([^']+)'")

BAD_DIST_SUBSTRINGS = (
    "കൃഷി ഉൽപ്പാദനം നിയന്ത്രിക്കുന്ന",
    "കമ്പനികളുടെ ഓഡിറ്റ്",
    "സർക്കാർ നികുതി ശേഖരിക്കുന്ന",
    "ഓഹരി വിപണിയിൽ കൃത്രിമ വിലക്കയറ്റം",
    "രാജ്യാന്തര വ്യാപാര നിയന്ത്രണം",
    "വിദേശ നാണ്യം കയറ്റുമതി",
    "തൊഴിലാളികളുടെ ശമ്പലം നിർണയിക്കുന്ന",
    "സർക്കാർ ബജറ്റ് തയ്യാറാക്കുന്ന",
    "വിപണിയിലെ ഓഹരി വില നിർണയിക്കുന്ന",
    "കമ്പനിയുടെ ഡിവിഡൻഡ് വിതരണം",
    "കമ്പനിയുടെ ലാഭം ഉപഭോക്താക്കൾക്ക് വിതരണം",
    "കയറ്റുമതി ലൈസൻസ് നൽകുന്ന",
    "സർക്കാർ നിശ്ചയിച്ച വിലയിൽ ഉൽപ്പാദനം",
    "സാധനങ്ങളുടെ ഉൽപ്പാദനം നിയന്ത്രിക്കുന്ന",
    "വിദേശ നാണ്യത്തിന്റെ മൂല്യനിർണയം",
    "ബാങ്ക് വായ്പകൾ തിരിച്ചടച്ച് പലിശ നേടുന്ന",
    "ആർബിഐയുടെ നാണ്യനയ നയം നിർവഹിക്കുന്ന",
    "രാജ്യാന്തര വ്യാപാര ലൈസൻസ് നൽകുന്ന",
    "നടത്തുന്ന സേവനം",
    "നിയന്ത്രിക്കുന്ന നിയമം",
    "നടപ്പിലാക്കുന്ന പ്രക്രിയ",
    "സൂചിപ്പിക്കുന്ന പ്രവർത്തി",
)

BANKING_DISTRACTORS = [
    "ചെക്ക് മതിയാക്കൽ",
    "വായ്പ അനുമതി നൽകൽ",
    "നിശ്ചിത നിക്ഷേപ പലിശ നിരക്ക് നിശ്ചയിക്കൽ",
    "അക്കൗണ്ട് സ്റ്റേറ്റ്മെന്റ് തയ്യാറാക്കൽ",
    "ATM കാർഡ് വിതരണം",
    "SWIFT കോഡ് നൽകൽ",
    "വായ്പ കുടിശ്ശിക പിന്തുടർച്ച",
    "പാസ്‌ബുക്ക് അപ്ഡേഷൻ",
    "നിലവിലെ അക്കൗണ്ട് നിയന്ത്രണം",
    "ഓവർഡ്രാഫ്റ്റ് അനുമതി",
    "നിശ്ചിത നിക്ഷേപം പുതുക്കൽ",
    "ചെക്ക് ബൗൺസ് ഫീ ഈടാക്കൽ",
    "നെറ്റ് ബാങ്കിംഗ് പാസ്‌വേഡ് പുനഃസജ്ജമാക്കൽ",
    "അക്കൗണ്ട് ട്രാൻസ്ഫർ പരിധി നിശ്ചയിക്കൽ",
    "ബാങ്ക് ഗാരന്റി നൽകൽ",
]

ECON_DISTRACTORS = [
    "വില കുറയൽ",
    "തൊഴിലില്ലായ്മ",
    "നാണ്യപ്പെരുപ്പം",
    "വിനിമയ നിരക്ക്",
    "ബജറ്റ് കമ്മി",
    "വളർച്ചാ നിരക്ക് കുറയൽ",
    "വിപണി മൂലധനം",
    "ഉൽപ്പാദന വർദ്ധനവ്",
    "വിലക്കയറ്റം",
    "നികുതി വർദ്ധനവ്",
    "കാർഷിക വികസനം",
    "വ്യാപാര കമ്മി",
    "നിക്ഷേപ വർദ്ധനവ്",
    "പണലഭ്യത കുറയൽ",
    "സാമ്പത്തിക അസമത്വം",
]

BAD_STEM_MARKERS = (
    "പ്രധാനമായി എന്തിനെ സൂചിപ്പിക്കുന്നു?",
    "പ്രധാന സാമ്പത്തിക സവിശേഷത ഏതാണ്?",
    "പ്രധാനമായി എന്തിനാണ്?",
    "പ്രധാന പ്രയോജനം എന്താണ്?",
)


def unwrap_text(text: str) -> str:
    text = text.strip()
    for pattern in (WRAP_RE, PROC_RE, BANKING_PREFIX_RE):
        m = pattern.match(text)
        if m:
            return m.group(1).strip()
    return text


def is_bad_distractor(text: str) -> bool:
    return any(s in text for s in BAD_DIST_SUBSTRINGS)


def extract_term(question: str) -> str | None:
    m = TERM_RE.search(question)
    return m.group(1).strip() if m else None


def rewrite_stem(question: str, answer: str) -> str:
    if not any(m in question for m in BAD_STEM_MARKERS):
        return question

    term = extract_term(question)
    if not term:
        for marker in BAD_STEM_MARKERS:
            if marker in question:
                term = question.split(marker)[0].strip().strip("'\"")
                break
    if not term:
        return question

    if "ബാങ്കിംഗ് സേവനങ്ങളിൽ" in question or (
        "ബാങ്കിംഗ്" in question and "സേവന" in question
    ):
        if "സന്ദേശം" in term or "അലേർട്ട്" in term or "ഓഫർ" in term:
            return f"ബാങ്കുകൾ '{term}' വഴി ഉപഭോക്താക്കൾക്ക് പ്രധാനമായും എന്ത് നൽകുന്നു?"
        if "രജിസ്ട്രേഷൻ" in term:
            return f"ബാങ്ക് സേവനങ്ങളിൽ '{term}' എന്തിനാണ് ആവശ്യം?"
        if any(x in term.lower() for x in ("പേയ്", "payment", "പേ")):
            return f"ബാങ്കിംഗിൽ '{term}' എന്തിനാണ് ഉപയോഗിക്കുന്നത്?"
        if any(
            x in term
            for x in ("അക്കൗണ്ട്", "കാർഡ്", "ലോൺ", "ഡെപ്പോസിറ്റ്", "നിക്ഷേപ")
        ):
            return f"ബാങ്ക് സേവനങ്ങളിൽ '{term}' എന്ത് സംബന്ധിച്ചതാണ്?"
        if any(x in term for x in ("എടിഎം", "പാസ്‌ബുക്ക്", "ലോക്കർ", "ചെക്ക്")):
            return f"ബാങ്കിംഗിൽ '{term}' എന്തിനാണ്?"
        return f"ബാങ്ക് സേവനങ്ങളിൽ '{term}'-ന്റെ പ്രധാന ഉപയോഗം എന്ത്?"

    if "സാമ്പത്തിക ശാസ്ത്രത്തിൽ" in question or "സാമ്പത്തിക സവിശേഷത" in question:
        return f"സാമ്പത്തിക ശാസ്ത്രത്തിൽ '{term}' എന്താണ്?"

    return f"'{term}' എന്താണ്?"


def polish_answer(answer: str) -> str:
    answer = unwrap_text(answer)
    replacements = {
        "സ്റ്റോക്ക് മാർക്കറ്റ്": "ഓഹരി വിപണി",
        "ഡിമാൻഡ് ആൻഡ് സപ്ലൈ": "ആവശ്യവും വിതരണവും",
        "ബാലൻസ് ഓഫ് ട്രേഡ്": "വ്യാപാര ബാലൻസ്",
        "ഡയറക്ട് ടാക്സ്": "നേരിട്ടുള്ള നികുതി",
        "പെട്രോളിയം ഉൽപ്പന്നങ്ങൾ": "പെട്രോളിയം ഉൽപ്പന്നങ്ങൾ",
        "നികുതി വർദ്ധനവ്": "നികുതി വർദ്ധന",
        "ജോലിയിൽ നിന്ന് കിട്ടുന്നത്": "ജോലിയിലൂടെയോ മറ്റ് ഉത്ഭവങ്ങളിലൂടെയോ ലഭിക്കുന്ന വരുമാനം",
        "ഭാവിയിലേക്കായി പണം വെക്കൽ": "ഭാവിയിലെ ആവശ്യങ്ങൾക്കായി പണം സംരക്ഷിക്കൽ",
        "പണം മുൻകൂട്ടി പ്ലാൻ ചെയ്യൽ": "ഭാവിയിലെ ആവശ്യങ്ങൾക്കായി പണം ആസൂത്രണം ചെയ്യൽ",
        "ഉടമസ്ഥതയിലുള്ള വസ്തുക്കൾ": "ഉടമസ്ഥതയിലുള്ള സ്വത്ത്/സാധനങ്ങൾ",
        "പണം കൈമാറാൻ": "പണം കൈമാറ്റം ചെയ്യൽ",
    }
    return replacements.get(answer, answer)


def pick_distractors(
    answer: str, question: str, count: int, rng: random.Random
) -> list[str]:
    pool = (
        BANKING_DISTRACTORS
        if "ബാങ്ക്" in question or "ബാങ്കിംഗ്" in question
        else ECON_DISTRACTORS
    )
    candidates = [c for c in pool if c != answer]
    rng.shuffle(candidates)
    return candidates[:count]


def fix_options(
    options: list[str], answer: str, question: str, qid: str, rng: random.Random
) -> list[str]:
    cleaned = [polish_answer(unwrap_text(o)) for o in options]
    answer = polish_answer(unwrap_text(answer))

    # Replace bad distractors
    result = []
    needed = 0
    for opt in cleaned:
        if opt == answer:
            result.append(opt)
        elif is_bad_distractor(opt):
            needed += 1
        else:
            result.append(opt)

    if needed:
        extras = pick_distractors(answer, question, needed + 4, rng)
        ei = 0
        final = []
        used = {answer}
        for opt in cleaned:
            if opt == answer:
                final.append(answer)
            elif is_bad_distractor(opt):
                while ei < len(extras) and extras[ei] in used:
                    ei += 1
                repl = extras[ei] if ei < len(extras) else f"ബാങ്ക് സേവനം {qid}-b"
                ei += 1
                while repl in used:
                    repl = repl + " "
                final.append(repl)
                used.add(repl)
            else:
                if opt in used:
                    while ei < len(extras) and extras[ei] in used:
                        ei += 1
                    repl = extras[ei] if ei < len(extras) else opt + " "
                    ei += 1
                    opt = repl
                final.append(opt)
                used.add(opt)
        result = final
    else:
        result = cleaned

    # Ensure answer present
    if answer not in result:
        if result:
            result[0] = answer
        else:
            result = [answer]

    # Ensure 4 unique options
    used = set()
    unique = []
    for opt in result:
        if opt not in used:
            unique.append(opt)
            used.add(opt)
    extras = pick_distractors(answer, question, 8, rng)
    ei = 0
    while len(unique) < 4:
        while ei < len(extras) and extras[ei] in used:
            ei += 1
        filler = extras[ei] if ei < len(extras) else f"മറ്റ് സേവനം {len(unique)}"
        ei += 1
        if filler not in used:
            unique.append(filler)
            used.add(filler)
    return unique[:4]


def needs_fix(q: dict) -> bool:
    if q.get("id") in SKIP_IDS:
        return False
    texts = [q.get("question", ""), q.get("answer", ""), *q.get("options", [])]
    if any(WRAP_RE.match(t.strip()) for t in texts if t):
        return True
    if any(PROC_RE.match(t.strip()) or BANKING_PREFIX_RE.match(t.strip()) for t in texts if t):
        return True
    if any(m in q.get("question", "") for m in BAD_STEM_MARKERS):
        return True
    if any(is_bad_distractor(o) for o in q.get("options", [])):
        return True
    return False


def fix_question(q: dict, rng: random.Random) -> tuple[dict, bool]:
    if not needs_fix(q):
        return q, False

    new_q = dict(q)
    answer = polish_answer(unwrap_text(new_q.get("answer", "")))
    question = new_q.get("question", "")
    if any(m in question for m in BAD_STEM_MARKERS):
        question = rewrite_stem(question, answer)
    new_q["question"] = question
    new_q["options"] = fix_options(new_q.get("options", []), answer, question, new_q["id"], rng)
    if answer not in new_q["options"]:
        new_q["options"][-1] = answer
    new_q["answer"] = answer
    return new_q, True


def main() -> None:
    rng = random.Random(42)
    data = json.loads(PATH.read_text(encoding="utf-8"))
    fixed = 0
    out = []
    for q in data["questions"]:
        nq, changed = fix_question(q, rng)
        if changed:
            fixed += 1
        out.append(nq)
    data["questions"] = out
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Fixed {fixed} / {len(out)} questions")


if __name__ == "__main__":
    main()
