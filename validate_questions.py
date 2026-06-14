#!/usr/bin/env python3
"""Validate all quiz JSON banks: structure, Malayalam rules, filler, known fact traps."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

from apply_malayalam_rules import validate_file as malayalam_issues
from option_type_utils import option_type_mismatch

BASE = Path(__file__).parent
SKIP = {"english_language.json", "current_affairs_manifest.json"}

FILLER_PATTERNS = [
    re.compile(r"^വർഷം .+ ഏത് ദശാബ്ദത്തിൽ\?$"),
    re.compile(r"^വർഷം .+ ഏത് നൂറ്റാണ്ടിലാണ്\?$"),
    re.compile(r"ഏത് ചോദ്യത്തിന്റെ ഉത്തരമാണ്"),
    re.compile(r"ഉത്തരമുള്ള ചോദ്യം"),
    re.compile(r"പ്രദേശം-\d+"),
    re.compile(r"വസ്തുത-\d+"),
    re.compile(r"വസ്തു-\d+"),
    re.compile(r"അവാർഡ്-\d+"),
    re.compile(r"പുരസ്കാരം-\d+"),
    re.compile(r"സൂചിപ്പിക്കുന്ന പ്രവർത്തി"),
    re.compile(r"നടത്തുന്ന സേവനം"),
    re.compile(r"നൽകുന്നത്/ബന്ധപ്പെട്ടത്"),
    re.compile(r"^ആകാശ വസ്തു '.+' ഏത് (തരത്തിൽ പെടുന്നു|നക്ഷത്രസമൂഹം/പ്രദേശത്താണ്)"),
    re.compile(r"ക്ഷുദ്രഗ്രഹം [^\s']+-\d+"),
    re.compile(r"ഗാലക്സി NGC-\d+"),
]

# Filmfare-only wins must NOT appear as National Film Award Best Actor answers.
NATIONAL_FILM_STEM = re.compile(r"നാഷണൽ ഫിലിം അവാർഡ്.*മികച്ച നടന", re.I)
NATIONAL_FILM_FORBIDDEN = re.compile(
    r"രണ്വീർ സിംഗ്|^83$|ചക്ദേ|Chak De|ലഗാൻ|Lagaan|അഗ്നിപഥ്|Agneepath|"
    r"വാസ്തവ്|Vaastav|സർദാർ Udham|Sardar Udham|ഒരുപ്പാട് ഓരോ പാതയില",
    re.I,
)

# Separate award families — stem must name the correct award body.
AWARD_STEM_PAIRS = [
    (re.compile(r"നാഷണൽ ഫിലിം അവാർഡ്"), re.compile(r"ഫിലിംഫെയർ|Filmfare")),
    (re.compile(r"ഫിലിംഫെയർ"), re.compile(r"നാഷണൽ ഫിലിം")),
    (re.compile(r"ഭാരതരത്ന"), re.compile(r"പത്മശ്രീ|പത്മഭൂഷൺ")),
]


def load_questions(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("questions", [])


def structural_issues(q: dict, qid: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    stem = q.get("question", "").strip()
    opts = q.get("options", [])
    ans = q.get("answer", "")
    if not stem:
        out.append((qid, "empty_question"))
    if len(opts) != 4:
        out.append((qid, f"option_count_{len(opts)}"))
    if len(set(opts)) != len(opts):
        out.append((qid, "duplicate_options"))
    if ans not in opts:
        out.append((qid, f"answer_not_in_options: {ans!r}"))
    if q.get("difficulty") not in {"easy", "medium", "hard"}:
        out.append((qid, "invalid_difficulty"))
    return out


def filler_issues(q: dict, qid: str) -> list[tuple[str, str]]:
    text = q.get("question", "") + " " + " ".join(q.get("options", [])) + " " + q.get("answer", "")
    out: list[tuple[str, str]] = []
    for pat in FILLER_PATTERNS:
        if pat.search(text):
            out.append((qid, f"filler:{pat.pattern[:40]}"))
    stem = q.get("question", "").strip()
    ans = q.get("answer", "")
    if stem and ans:
        from giveaway_utils import is_answer_in_stem_giveaway, is_banned_giveaway_stem

        if is_answer_in_stem_giveaway(stem, ans):
            out.append((qid, "giveaway:answer_quoted_in_stem"))
        elif is_banned_giveaway_stem(stem):
            out.append((qid, "giveaway:banned_stem_template"))
    return out


def option_mismatch_issues(q: dict, qid: str) -> list[tuple[str, str]]:
    stem = q.get("question", "")
    opts = q.get("options", [])
    ans = q.get("answer", "")
    code = option_type_mismatch(stem, opts, ans)
    if code:
        return [(qid, f"option_type_mismatch:{code}")]
    return []


def fact_trap_issues(q: dict, qid: str) -> list[tuple[str, str]]:
    stem = q.get("question", "")
    ans = q.get("answer", "")
    out: list[tuple[str, str]] = []
    if NATIONAL_FILM_STEM.search(stem) and NATIONAL_FILM_FORBIDDEN.search(ans):
        out.append((qid, f"award_mixup:national_film_actor:{ans}"))
    for stem_pat, forbidden in AWARD_STEM_PAIRS:
        if stem_pat.search(stem) and forbidden.search(ans):
            out.append((qid, f"award_mixup:wrong_body:{ans}"))
    return out


def english_language_issues(q: dict, qid: str, filename: str) -> list[tuple[str, str]]:
    if filename != "english_language.json":
        return []
    out: list[tuple[str, str]] = []
    stem = q.get("question", "")
    if re.search(r"[\u0D00-\u0D7F]", stem):
        out.append((qid, "malayalam_in_english_bank"))
    return out


def file_consecutive_template_issues(questions: list[dict]) -> list[tuple[str, str, str]]:
    from refill_common import max_consecutive_template_run, stem_template

    out: list[tuple[str, str, str]] = []
    run, key = max_consecutive_template_run(questions)
    if run >= 3 and key:
        # flag each question in the longest run starting from first occurrence
        if not questions:
            return out
        best_start = 0
        best_len = 1
        cur_key = stem_template(questions[0].get("question", ""))
        cur_start = 0
        cur_len = 1
        for i, q in enumerate(questions[1:], start=1):
            k = stem_template(q.get("question", ""))
            if k == cur_key:
                cur_len += 1
            else:
                if cur_len > best_len:
                    best_len = cur_len
                    best_start = cur_start
                cur_key = k
                cur_start = i
                cur_len = 1
        if cur_len > best_len:
            best_len = cur_len
            best_start = cur_start
        if best_len >= 3:
            for q in questions[best_start : best_start + best_len]:
                out.append((
                    q.get("id", "?"),
                    "consecutive_template_run",
                    f"{best_len}x:{key[:40]}",
                ))
    return out


def validate_json_file(path: Path, global_stems: Counter[str]) -> dict:
    issues: list[tuple[str, str, str]] = []
    questions = load_questions(path)
    local_stems: Counter[str] = Counter()

    for q in questions:
        qid = q.get("id", "?")
        stem = q.get("question", "").strip()
        local_stems[stem] += 1
        if stem:
            global_stems[stem] += 1

        for code, detail in (
            structural_issues(q, qid)
            + filler_issues(q, qid)
            + option_mismatch_issues(q, qid)
            + fact_trap_issues(q, qid)
            + english_language_issues(q, qid, path.name)
        ):
            issues.append((qid, code, detail))

        if stem and local_stems[stem] > 1:
            issues.append((qid, "duplicate_stem_local", stem[:80]))

    for qid, code, detail in malayalam_issues(path.name):
        issues.append((qid, f"malayalam:{code}", detail[:120]))

    for qid, code, detail in file_consecutive_template_issues(questions):
        issues.append((qid, code, detail))

    return {
        "file": path.name,
        "count": len(questions),
        "issues": issues,
    }


def main(argv: list[str]) -> int:
    paths = sorted(BASE.glob("*.json"))
    if len(argv) > 1:
        names = {Path(a).name for a in argv[1:]}
        paths = [p for p in paths if p.name in names]

    global_stems: Counter[str] = Counter()
    reports = [validate_json_file(p, global_stems) for p in paths if p.name not in SKIP]

    global_dupes = {s for s, c in global_stems.items() if c > 1 and s}
    total_issues = 0
    print("Question bank validation\n" + "=" * 40)
    for rep in reports:
        # add global duplicate flags
        extra = []
        for q in load_questions(BASE / rep["file"]):
            stem = q.get("question", "").strip()
            if stem in global_dupes:
                extra.append((q.get("id", "?"), "duplicate_stem_global", stem[:80]))
        rep["issues"].extend(extra)

        n = len(rep["issues"])
        total_issues += n
        status = "OK" if n == 0 else f"{n} issue(s)"
        print(f"  {rep['file']}: {rep['count']} questions — {status}")
        if n and (len(argv) > 1 or n <= 20):
            for qid, code, detail in rep["issues"][:30]:
                print(f"    [{qid}] {code}: {detail}")
            if n > 30:
                print(f"    ... and {n - 30} more")

    print("=" * 40)
    print(f"Total issues: {total_issues}")
    if total_issues:
        print("\nRun with file args for detail: python3 validate_questions.py awards.json")
        print("Fix fact traps before merge; never guess award winners from templates.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
