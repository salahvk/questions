#!/usr/bin/env python3
"""Fix geography.json questions where the answer appears quoted in the stem."""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
from pathlib import Path

from geography_facts import (
    CAPITALS,
    COUNTRY_CONTINENT,
    INDIAN_DAMS,
    INDIAN_NATIONAL_PARKS,
    INDIAN_RIVER_LENGTH,
    INDIAN_STATE_AREA,
    INDIAN_STATE_CAPITALS,
    INDIAN_STATE_POPULATION,
    KERALA_DISTRICTS,
    MOUNTAIN_PEAKS,
)
from giveaway_utils import is_answer_in_stem_giveaway, rewrite_giveaway_question
from refill_common import load_global_stems, pick3

BASE = Path(__file__).parent
FILE = "geography.json"

KERALA_DISTRICT_ALT: dict[str, tuple[str, str, list[str], str]] = {
    "തിരുവനന്തപുരം": (
        "പത്മനാഭസ്വാമി ക്ഷേത്രം ഏത് കേരള ജില്ലയിലാണ്?",
        "തിരുവനന്തപുരം",
        ["കൊല്ലം", "കോട്ടയം", "തൃശ്ശൂർ"],
        "easy",
    ),
    "കൊല്ലം": (
        "കേരളത്തിലെ പ്രശസ്തമായ കശുവണ്ടി തുറമുഖ നഗരം ഏത് ജില്ലയിലാണ്?",
        "കൊല്ലം",
        ["എറണാകുളം", "തിരുവനന്തപുരം", "ആലപ്പുഴ"],
        "medium",
    ),
    "പത്തനംതിട്ട": (
        "സബരിമല ശാസ്താവ് ക്ഷേത്രം ഏത് കേരള ജില്ലയിലാണ്?",
        "പത്തനംതിട്ട",
        ["ഇടുക്കി", "കോട്ടയം", "കൊല്ലം"],
        "easy",
    ),
    "ആലപ്പുഴ": (
        "കേരളത്തിലെ 'കായലുകളുടെ നാട്' എന്നറിയപ്പെടുന്ന ജില്ല ഏത്?",
        "ആലപ്പുഴ",
        ["കൊല്ലം", "എറണാകുളം", "കോട്ടയം"],
        "easy",
    ),
    "കോട്ടയം": (
        "വെമ്പനാട് കായലിന്റെ ഭാഗം ഉൾപ്പെടുന്ന പ്രശസ്ത ജില്ല ഏത്?",
        "കോട്ടയം",
        ["ആലപ്പുഴ", "ഇടുക്കി", "എറണാകുളം"],
        "medium",
    ),
    "തൃശ്ശൂർ": (
        "തൃശ്ശൂർ പൂരം ഏത് ജില്ലയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
        "തൃശ്ശൂർ",
        ["പാലക്കാട്", "എറണാകുളം", "മലപ്പുറം"],
        "easy",
    ),
    "പാലക്കാട്": (
        "പാലക്കാട് കോട്ട ഏത് കേരള ജില്ലയിലാണ്?",
        "പാലക്കാട്",
        ["തൃശ്ശൂർ", "മലപ്പുറം", "വയനാട്"],
        "easy",
    ),
    "മലപ്പുറം": (
        "കേരളത്തിലെ ഏറ്റവും കൂടുതൽ ജനസംഖ്യയുള്ള ജില്ല ഏത്?",
        "മലപ്പുറം",
        ["എറണാകുളം", "തിരുവനന്തപുരം", "കോഴിക്കോട്"],
        "medium",
    ),
    "കോഴിക്കോട്": (
        "കപ്പാട് (നൃത്തരൂപം) ഏത് ജില്ലയുമായി പ്രധാനമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
        "കോഴിക്കോട്",
        ["മലപ്പുറം", "വയനാട്", "കണ്ണൂർ"],
        "medium",
    ),
    "കണ്ണൂർ": (
        "സ്തംഭേശ്വര ക്ഷേത്രം (സ്തംഭം) ഏത് ജില്ലയിലാണ്?",
        "കണ്ണൂർ",
        ["കാസർഗോഡ്", "വയനാട്", "കോഴിക്കോട്"],
        "hard",
    ),
    "കാസർഗോഡ്": (
        "ബേക്കൽ കോട്ട ഏത് കേരള ജില്ലയിലാണ്?",
        "കാസർഗോഡ്",
        ["കണ്ണൂർ", "വയനാട്", "മലപ്പുറം"],
        "easy",
    ),
}

STATES = [s for s, _ in INDIAN_STATE_CAPITALS]
CAPITALS_LIST = [c for _, c in CAPITALS]
CONTINENTS = list({c for _, c in COUNTRY_CONTINENT})

YESNO_REWRITES = [
    (
        re.compile(
            r"^'([^']+)' സംസ്ഥാന(?:ത്ത്|ത്തിന്റെ) (?:പ്രധാന )?"
            r"കാർഷിക (?:വിള|ഉൽപ്പന്നം) '([^']+)' — ശരിയ(?:ാണോ|ോ)\?$"
        ),
        lambda s, e: (f"'{e}' പ്രധാനമായി ഏത് സംസ്ഥാനത്തിൽ കൃഷി ചെയ്യുന്നു?", s),
    ),
    (
        re.compile(r"^'([^']+)' നദിയ(?:ude|യുടെ) തീര(?:ത്ത്|ത്തുള്ള) (?:പ്രധാന )?നഗരം '([^']+)' — ശരിയ(?:ാണോ|ോ)\?$"),
        lambda s, e: (f"'{e}' നഗരം ഏത് നദിയുടെ തീരത്താണ്?", s),
    ),
    (
        re.compile(r"^'([^']+)' നദിയ(?:ude|യുടെ) തീര(?:ത്ത്|ത്ത്) '([^']+)' — ശരിയ(?:ാണോ|ോ)\?$"),
        lambda s, e: (f"'{e}' നഗരം ഏത് നദിയുടെ തീരത്താണ്?", s),
    ),
    (
        re.compile(
            r"^'([^']+)' സംസ്ഥാന(?:ത്തിലെ|ത്തിലെ) (?:പ്രശസ്തമായ )?"
            r"(?:ഖനി/വ്യവസായ കേന്ദ്രം|ഹിൽ സ്റ്റേഷൻ|ജലപാതം|വന്യജീവി സങ്കേതം|"
            r"തടാകം|ആണവ/വൈദ്യുത കേന്ദ്രം|കയറ്റം|കാലാവസ്ഥാ പ്രദേശം|"
            r"ജൈവവൈവിധ്യ സംരക്ഷിത പ്രദേശം|യുനെസ്കോ ലോക പൈതൃക കേന്ദ്രം) "
            r"'([^']+)' — ശരിയ(?:ാണോ|ോ)\?$"
        ),
        lambda s, e: (f"'{e}' ഏത് സംസ്ഥാനത്താണ്?", s),
    ),
    (
        re.compile(r"^'([^']+)' നദിയ(?:ude|യുടെ) പോഷക നദി '([^']+)' — ശരിയ(?:ാണോ|ോ)\?$"),
        lambda s, e: (f"'{e}' ഏത് പ്രധാന നദിയുടെ പോഷക നദിയാണ്?", s),
    ),
]


def _rewrite_yesno(stem: str, answer: str) -> tuple[str, str] | None:
    for pat, fn in YESNO_REWRITES:
        m = pat.match(stem.strip())
        if m and m.group(2).strip() == answer.strip():
            return fn(m.group(1).strip(), m.group(2).strip())
    return None


def _rebuild_options(question: str, answer: str, rng: random.Random) -> list[str]:
    ans = answer.strip()

    if "ദേശീയോദ്യാനം ഏത് സംസ്ഥാന" in question:
        pool = list(dict.fromkeys(s for _, s in INDIAN_NATIONAL_PARKS))
        return pick3(pool, ans, rng)

    if "അണക്കെട്ട് ഏത് നദിയിൽ" in question:
        rivers = list(dict.fromkeys(r for _, r, _ in INDIAN_DAMS))
        return pick3(rivers, ans, rng)

    if "ശിഖരം ഏത് പർവതനിര" in question:
        ranges = list(dict.fromkeys(r for _, r, _ in MOUNTAIN_PEAKS))
        return pick3(ranges, ans, rng)

    if "ശിഖരം ഏതാണ്" in question or "ശിഖരം" in question:
        peaks = list(dict.fromkeys(p for p, _, _ in MOUNTAIN_PEAKS))
        return pick3(peaks, ans, rng)

    if "അണക്കെട്ട് ഏതാണ്" in question:
        dams = list(dict.fromkeys(d for d, _, _ in INDIAN_DAMS))
        return pick3(dams, ans, rng)

    if "രാജ്യത്തിന്റെ തലസ്ഥാനം" in question:
        return pick3(CAPITALS_LIST, ans, rng)

    if "ഭൂഖണ്ഡത്തിലാണ്" in question:
        return pick3(CONTINENTS, ans, rng)

    if "ദൈർഘ്യം" in question and "നദി ഏത്" in question:
        rivers = [r for r, _ in INDIAN_RIVER_LENGTH]
        return pick3(rivers, ans, rng)

    if "വിസ്തീർണ്ണം" in question and "സംസ്ഥാനം ഏത്" in question:
        states = [s for s, _ in INDIAN_STATE_AREA]
        return pick3(states, ans, rng)

    if "ജനസംഖ്യ" in question and "സംസ്ഥാനം ഏത്" in question:
        states = [s for s, _ in INDIAN_STATE_POPULATION]
        return pick3(states, ans, rng)

    if "കൃഷി ചെയ്യുന്നു" in question or "ഏത് സംസ്ഥാനത്താണ്?" in question:
        return pick3(STATES, ans, rng)

    if "നദിയുടെ തീരത്താണ്" in question:
        rivers = list(dict.fromkeys(r for _, r, _ in INDIAN_DAMS))
        return pick3(rivers, ans, rng)

    if "പോഷക നദിയാണ്" in question:
        rivers = list(dict.fromkeys(r for r, _ in INDIAN_RIVER_LENGTH))
        return pick3(rivers, ans, rng)

    if "ജില്ല" in question:
        dists = [d for d, _ in KERALA_DISTRICTS]
        return pick3(dists, ans, rng)

    return pick3(STATES + CAPITALS_LIST[:20], ans, rng)


def _alt_district_question(district: str) -> tuple[str, str, list[str]] | None:
    alt = KERALA_DISTRICT_ALT.get(district)
    if alt:
        q, ans, wrong, _ = alt
        return q, ans, wrong
    for dist, hq in KERALA_DISTRICTS:
        if dist == district and hq != district:
            dists = [d for d, _ in KERALA_DISTRICTS if d != dist]
            return f"'{hq}' ഏത് കേരള ജില്ലയുടെ ആസ്ഥാനമാണ്?", dist, dists[:3]
    return None


def _try_rewrite(stem: str, answer: str) -> tuple[str, str] | None:
    r = rewrite_giveaway_question(stem, answer)
    if r:
        return r
    return _rewrite_yesno(stem, answer)


def fix_questions(questions: list[dict], rng: random.Random) -> tuple[int, int, int]:
    stems_in_file = {q["question"].strip() for q in questions}
    fixed = removed = 0

    i = 0
    while i < len(questions):
        q = questions[i]
        stem = q["question"].strip()
        ans = q["answer"].strip()
        if not is_answer_in_stem_giveaway(stem, ans):
            i += 1
            continue

        rewritten = _try_rewrite(stem, ans)
        if rewritten is None and "ജില്ല" in stem:
            m = re.search(r"'([^']+)'", stem)
            if m and m.group(1).strip() == ans:
                alt = _alt_district_question(ans)
                if alt:
                    rewritten = (alt[0], alt[1])

        if rewritten:
            new_q, new_ans = rewritten
            if new_q in stems_in_file and new_q != stem:
                # Good version already in file — drop duplicate bad row
                questions.pop(i)
                stems_in_file.discard(stem)
                removed += 1
                continue
            q["question"] = new_q
            q["answer"] = new_ans
            q["options"] = _rebuild_options(new_q, new_ans, rng)
            stems_in_file.discard(stem)
            stems_in_file.add(new_q)
            fixed += 1
            i += 1
            continue

        # Unhandled giveaway — remove rather than keep broken item
        questions.pop(i)
        stems_in_file.discard(stem)
        removed += 1

    return fixed, removed, len(questions)


def dedupe_options(questions: list[dict], rng: random.Random) -> int:
    n = 0
    for q in questions:
        opts = q.get("options", [])
        ans = q.get("answer", "")
        if len(set(opts)) == 4 and ans in opts:
            continue
        q["options"] = _rebuild_options(q["question"], ans, rng)
        n += 1
    return n


def main() -> int:
    path = BASE / FILE
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data["questions"]
    rng = random.Random(42)

    before = len(questions)
    fixed, removed, after = fix_questions(questions, rng)
    opts_fixed = dedupe_options(questions, rng)
    data["questions"] = questions
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"{FILE}: {before} → {after} questions")
    print(f"  Rewrote {fixed}, removed {removed} giveaway rows")
    print(f"  Rebuilt options on {opts_fixed} rows")

    subprocess.run([sys.executable, "apply_malayalam_rules.py", FILE], cwd=BASE, check=False)
    r = subprocess.run([sys.executable, "validate_questions.py", FILE], cwd=BASE)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
