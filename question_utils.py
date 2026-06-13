#!/usr/bin/env python3
"""Shared utilities for generating unique MCQ questions."""
import json
import os
import random
import re

random.seed(42)

_QUESTION_PREFIXES = [
    "റിവിഷൻ ചോദ്യം: ",
    "ഒറ്റവരി GK: ",
    "ചുരുക്കചോദ്യം: ",
    "പൊതുവിജ്ഞാനം: ",
    "പരീക്ഷാ മോഡൽ ചോദ്യം: ",
    "സിവിൽ സർവീസ് സ്റ്റൈൽ ചോദ്യം: ",
    "മലയാളം ക്വിസ്: ",
    "ഫാക്ട് ചെക്ക്: ",
    "താഴെക്കാണുന്ന ചോദ്യത്തിന് ഉത്തരം: ",
    "ശരിയായ ഉത്തരം തിരഞ്ഞെടുക്കുക: ",
    "താഴെക്കൊടുത്ത ചോദ്യത്തിന് ഉചിതമായ ഉത്തരമേത്? ",
    "വസ്തുത അധിഷ്ഠിത ചോദ്യം: ",
    "MCQ രൂപത്തിൽ: ",
    "ശാസ്ത്രീയ അറിവ് പരിശോധന: ",
    "GK ചോദ്യം: ",
    "പരീക്ഷാ ചോദ്യം: ",
    "ഒരു മാർക്ക് ചോദ്യം: ",
    "പൊതുവിജ്ഞാന പരിശോധന: ",
    "വസ്തുത അറിയുക: ",
    "ശരിയായ ഓപ്ഷൻ തിരഞ്ഞെടുക്കുക: ",
    "താഴെ പറയുന്ന ചോദ്യത്തിന് ഉത്തരം കണ്ടെത്തുക: ",
    "കാലാവസ്ഥ വിജ്ഞാനം: ",
    "പ്രകൃതി ശാസ്ത്ര ചോദ്യം: ",
    "ശരിയായ പരിഹാരം: ",
]

_QUESTION_SUFFIX_PATTERNS = [
    r" ശരിയായ ഉത്തരം തിരഞ്ഞെടുക്കുക\.$",
    r" \(വികൽപങ്ങളിൽ നിന്ന് തിരഞ്ഞെടുക്കുക\)$",
    r" — ശരിയായത് ഏത്\?$",
    r" എന്ന ചോദ്യത്തിന് ശരിയായ ഉത്തരം ഏത്\?$",
    r" \(സരിയായ ഉത്തരമോ\?\)$",
    r" \[അഭ്യാസ രൂപം \d+\]$",
    r" \(രൂപം \d+\)$",
    r" \(വേരിയന്റ് \d+\)$",
]

_KERALA_QUESTION_PATTERNS = [
    (r"^കേരളത്തെക്കുറിച്ചുള്ള പൊതുവിജ്ഞാനത്തിൽ (.+) ആയി അറിയപ്പെടുന്നത് എന്ത്\?$", r"\1 ഏത്?"),
    (r"^കേരള നവോത്ഥാന പഠനത്തിൽ (.+) ആയി രേഖപ്പെടുന്നത് എന്ത്\?$", r"\1 ആരാണ്/എതാണ്?"),
    (r"^കേരളചരിത്ര പഠനത്തിൽ (.+) ആയി അറിയപ്പെടുന്നത് ഏത്\?$", r"\1 ഏത്?"),
    (r"^കേരള രാഷ്ട്രീയ പൊതുവിജ്ഞാനത്തിൽ (.+) ആയി അറിയപ്പെടുന്നത് ഏത്\?$", r"\1 ഏത്?"),
    (r"^കേരളത്തിലെ പ്രധാന സ്ഥാപനങ്ങളെക്കുറിച്ചുള്ള പഠനത്തിൽ (.+) ആയി അറിയപ്പെടുന്നത് ഏത്\?$", r"\1 ഏത്?"),
    (r"^ജില്ലാ വിവരങ്ങളിൽ (.+) ആയി രേഖപ്പെടുത്തുന്നത് എന്ത്\?$", r"\1 ഏത്?"),
    (r"^സംസ്ഥാന രാഷ്ട്രീയ പഠനത്തിൽ (.+) എന്ന് പറയുമ്പോൾ ഉത്തരം എന്ത്\?$", r"\1 ഏത്?"),
    (r"^സ്ഥാപന വിവരങ്ങളിൽ (.+) എന്ന് രേഖപ്പെടുത്തുന്നത് എന്ത്\?$", r"\1 ഏത്?"),
    (r"^ചരിത്രകുറിപ്പിൽ (.+) എന്ന് കാണുമ്പോൾ ഉത്തരം എന്ത്\?$", r"\1 ആരാണ്/എതാണ്?"),
    (r"^(.+) എന്ന ചോദ്യത്തിന് ശരിയായ ഉത്തരം (?:എന്ത്|ഏത്)\?$", r"\1 ഏത്?"),
    (r"^(.+) എന്നത് താഴെ പറയുന്നവയിൽ ഏതാണ്\?$", r"\1 ഏത്?"),
    (r"^(.+) എന്ന വിജ്ഞാനബിന്ദുവിന് യോജിച്ച ഉത്തരമ(?:ാരാണ്/എതാണ്|ം ഏത്)\?$", r"\1 ഏത്?"),
    (r"^(.+) എന്ന് പറയുമ്പോൾ ഏത് പേര് വരും\?$", r"\1 ഏത്?"),
    (r"^(.+) എന്ന നിലയിൽ ശരിയായ തിരഞ്ഞെടുപ്പ് ഏത്\?$", r"\1 ഏത്?"),
    (r"^(.+) എന്നതിൽ യോജിച്ച തിരഞ്ഞെടുപ്പ് ഏത്\?$", r"\1 ആരാണ്/എതാണ്?"),
    (r"^(.+) സംബന്ധിച്ച ശരിയായ (?:ഓപ്ഷൻ|തിരഞ്ഞെടുപ്പ്) ഏത്\?$", r"\1 ഏത്?"),
    (r"^(.+) സംബന്ധിച്ച യോജിച്ച (?:ഉത്തരം തിരഞ്ഞെടുക്കുക|തിരഞ്ഞെടുപ്പ് ഏത്)\.?$", r"\1 ഏത്?"),
    (r"^(.+) തിരിച്ചറിയുക\.$", r"\1 ഏത്?"),
    (r"^(.+) കണ്ടെത്തുക\.$", r"\1 ഏത്?"),
    (r"^(.+) പറയുക\.$", r"\1 ഏത്?"),
]


def normalize_question(question: str) -> str:
    """Return plain question text without decorative prefixes or suffixes."""
    text = question.strip()
    changed = True
    while changed:
        changed = False
        for prefix in _QUESTION_PREFIXES:
            if text.startswith(prefix):
                text = text[len(prefix) :].strip()
                changed = True

    for pattern, replacement in _KERALA_QUESTION_PATTERNS:
        match = re.match(pattern, text)
        if match:
            text = re.sub(pattern, replacement, text).strip()
            break

    for pattern in _QUESTION_SUFFIX_PATTERNS:
        updated = re.sub(pattern + "$", "", text).strip()
        if updated != text:
            text = updated

    return text


_ELEMENT_SYM = re.compile(r"^തനിമ '([^']+)'യുടെ രാസ ചിഹ്നം ഏതാണ്\?$")
_ELEMENT_REV = re.compile(r"^രാസ ചിഹ്നം '([^']+)' ഏത് തനിമയെ സൂചിപ്പിക്കുന്നു\?$")
_ELEMENT_NUM = re.compile(r"^തനിമ '([^']+)'യുടെ അണുസംഖ്യ എത്ര\?$")
_COMPOUND_FORMULA = re.compile(r"^'([^']+)'യുടെ രാസ സൂത്രം ഏതാണ്\?$")
_FORMULA_COMPOUND = re.compile(r"^രാസ സൂത്രം '([^']+)' ഏത് പദാർത്ഥമാണ്\?$")


def _is_element_triplet(questions, index):
    if index + 2 >= len(questions):
        return False
    texts = [questions[index + offset]["question"].strip() for offset in range(3)]
    return (
        _ELEMENT_SYM.match(texts[0])
        and _ELEMENT_REV.match(texts[1])
        and _ELEMENT_NUM.match(texts[2])
    )


def _is_compound_pair(questions, index):
    if index + 1 >= len(questions):
        return False
    texts = [questions[index + offset]["question"].strip() for offset in range(2)]
    return _COMPOUND_FORMULA.match(texts[0]) and _FORMULA_COMPOUND.match(texts[1])


def space_inverse_question_pairs(questions):
    """Separate rephrased inverse pairs (symbol/name, formula/compound)."""
    spaced = []
    index = 0
    while index < len(questions):
        if _is_element_triplet(questions, index):
            sym_questions, rev_questions, num_questions = [], [], []
            while index < len(questions) and _is_element_triplet(questions, index):
                sym_questions.append(questions[index])
                rev_questions.append(questions[index + 1])
                num_questions.append(questions[index + 2])
                index += 3
            block = []
            for sym_q, num_q in zip(sym_questions, num_questions):
                block.append(sym_q)
                block.append(num_q)
            block.extend(rev_questions)
            spaced.extend(block)
            continue

        if _is_compound_pair(questions, index):
            forward, reverse = [], []
            while index < len(questions) and _is_compound_pair(questions, index):
                forward.append(questions[index])
                reverse.append(questions[index + 1])
                index += 2
            spaced.extend(forward)
            spaced.extend(reverse)
            continue

        spaced.append(questions[index])
        index += 1
    return spaced


def reindex_questions(questions, prefix):
    for index, item in enumerate(questions, start=1):
        item["id"] = f"{prefix}_{index:03d}"
    return questions


def clean_question_bank(data: dict) -> tuple[dict, int, int]:
    """Strip decorative wrappers and remove duplicate questions."""
    questions = data.get("questions", [])
    if not questions:
        return data, 0, 0

    prefix_match = re.match(r"^([a-z]+)_\d+$", questions[0].get("id", ""))
    id_prefix = prefix_match.group(1) if prefix_match else "q"

    cleaned = []
    seen = set()
    stripped = 0
    removed = 0

    for item in questions:
        original = item.get("question", "").strip()
        normalized = normalize_question(original)
        if normalized != original:
            stripped += 1

        key = (normalized, item.get("answer", "").strip())
        if key in seen:
            removed += 1
            continue

        seen.add(key)
        cleaned.append({**item, "question": normalized})

    for index, item in enumerate(cleaned, start=1):
        item["id"] = f"{id_prefix}_{index:03d}"

    return {"questions": cleaned}, stripped, removed

SKIP_FILES = {
    "current_affairs_manifest.json",
}


def load_existing():
    seen = set()
    files = {}
    for fname in os.listdir("."):
        if not fname.endswith(".json") or fname in SKIP_FILES:
            continue
        if fname.startswith("current_affairs_2026_"):
            continue
        with open(fname, encoding="utf-8") as f:
            data = json.load(f)
        if "questions" not in data:
            continue
        files[fname] = data
        for q in data["questions"]:
            seen.add(q["question"].strip())
    return seen, files


def max_id(questions, prefix):
    nums = []
    for q in questions:
        m = re.search(rf"{re.escape(prefix)}_(\d+)$", q["id"])
        if m:
            nums.append(int(m.group(1)))
    return max(nums) if nums else 0


def make_mcq(question, answer, distractors, difficulty="medium"):
    pool = list({x for x in distractors if x != answer})
    random.shuffle(pool)
    options = [answer] + pool[:3]
    while len(options) < 4:
        options.append(f"ഓപ്ഷൻ {len(options)}")
    random.shuffle(options)
    return {
        "question": question,
        "options": options,
        "answer": answer,
        "difficulty": difficulty,
    }


def add_unique(seen, questions, prefix, counter, mcq):
    text = mcq["question"].strip()
    if text in seen:
        return counter, False
    seen.add(text)
    counter += 1
    questions.append({"id": f"{prefix}_{counter:03d}", **mcq})
    return counter, True


def gen_from_facts(seen, prefix, facts, template=None, start_counter=0, limit=None):
    qs = []
    counter = start_counter
    for item in facts:
        if limit is not None and len(qs) >= limit:
            break
        if len(item) == 3:
            key, answer, wrong = item
            diff = "medium"
        elif len(item) == 4:
            key, answer, wrong, diff = item
        else:
            qtext, answer, wrong, diff = item
            mcq = make_mcq(qtext, answer, wrong, diff)
            counter, _ = add_unique(seen, qs, prefix, counter, mcq)
            continue
        qtext = template.format(key) if template else key
        mcq = make_mcq(qtext, answer, wrong, diff)
        counter, _ = add_unique(seen, qs, prefix, counter, mcq)
    return qs, counter


def fill_file(fname, prefix, seen, generators, target=500):
    """Keep existing questions, append generated ones up to target."""
    _, files = load_existing()
    existing = files.get(fname, {}).get("questions", [])
    questions = list(existing)
    for q in existing:
        seen.add(q["question"].strip())
    counter = max_id(questions, prefix)

    for gen in generators:
        if len(questions) >= target:
            break
        need = target - len(questions)
        new_qs, counter = gen(seen, prefix, counter, need)
        questions.extend(new_qs)

    out = {"questions": questions[:target]}
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return len(out["questions"])
