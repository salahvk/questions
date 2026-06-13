#!/usr/bin/env python3
"""Shared refill utilities — enforces .cursor/rules/malayalam-questions.mdc guards."""

from __future__ import annotations

import json
import random
import re
from pathlib import Path

from validate_questions import FILLER_PATTERNS

BASE = Path(__file__).parent
SKIP_GLOBAL = {"english_language.json", "current_affairs_manifest.json"}

# Extra banned stems from cursor rules §3–§5
BANNED_STEM_PATTERNS = [
    re.compile(r"^വർഷം .+ ഏത് ദശാബ്ദത്തിൽ\?$"),
    re.compile(r"^വർഷം .+ ഏത് നൂറ്റാണ്ടിലാണ്\?$"),
    re.compile(r"ഏത് ചോദ്യത്തിന്റെ ഉത്തരമാണ്"),
    re.compile(r"ഉത്തരമുള്ള ചോദ്യം"),
    re.compile(r"^'[^']+' ബാങ്കിംഗ് സേവനങ്ങളിൽ പ്രധാനമായി എന്തിനാണ്"),
    re.compile(r"^ബാങ്കിംഗ് സേവനങ്ങളിൽ '[^']+'-യുടെ പ്രധാന പ്രയോജനം"),
    re.compile(r"^'[^']+' സാമ്പത്തിക ശാസ്ത്രത്തിൽ പ്രധാനമായി"),
    re.compile(r"^ആകാശ വസ്തു '.+' ഏത് (തരത്തിൽ പെടുന്നു|നക്ഷത്രസമൂഹം/പ്രദേശത്താണ്)"),
    re.compile(r"^ലോക ഭൂമിശാസ്ത്രത്തിൽ '\d+' എന്ന"),
    re.compile(r"^NCERT പുസ്തകം"),
    re.compile(r"വിഷയം-\d+"),
]

Candidate = tuple[str, list[str], str, str]

# Stem templates for consecutive-run detection (variable slot → fixed key)
STEM_TEMPLATE_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^.+ സംസ്ഥാനത്തിന്റെ സ്കൂൾ ബോർഡ്\?$"), "state_school_board"),
    (re.compile(r"^.+ യൂണിവേഴ്സിറ്റി ഏത് നഗര"), "univ_city"),
    (re.compile(r"^IIT .+ ഏത് നഗര"), "iit_city"),
    (re.compile(r"^ഐഐടി .+ ഏത് നഗര"), "iit_city"),
    (re.compile(r"^.+ പരീക്ഷ ഏതിനാണ്\?$"), "exam_purpose"),
    (re.compile(r"^.+ പദ്ധതി ഏതിനാണ്\?$"), "scheme_purpose"),
    (re.compile(r"^.+ ഏത് മേഖല"), "scheme_sector"),
    (re.compile(r"^NCERT പുസ്തകം"), "ncert_fake"),
    (re.compile(r"^diploid: n=\d+, m=\d+ — ആകെ ക്രോമോസോം എണ്ണം\?$"), "bio_diploid_formula"),
    (re.compile(r"^DNA \d+ bp, GC \d+% — GC bp എണ്ണം\?$"), "bio_dna_gc_formula"),
    (re.compile(r"വിഷയം-\d+"), "ncert_fake"),
]


def stem_template(stem: str) -> str:
    s = stem.strip()
    for pat, key in STEM_TEMPLATE_RULES:
        if pat.search(s):
            return key
    return s


def max_consecutive_template_run(questions: list[dict]) -> tuple[int, str | None]:
    if not questions:
        return 0, None
    best = 1
    best_key: str | None = stem_template(questions[0].get("question", ""))
    cur_key = best_key
    cur = 1
    for q in questions[1:]:
        key = stem_template(q.get("question", ""))
        if key == cur_key:
            cur += 1
            if cur > best:
                best = cur
                best_key = cur_key
        else:
            cur_key = key
            cur = 1
    return best, best_key


def spread_consecutive_templates(
    questions: list[dict],
    rng: random.Random,
    *,
    max_run: int = 2,
) -> list[dict]:
    """Reorder so no more than `max_run` questions share the same stem template in a row."""
    if len(questions) <= 1:
        return questions

    from collections import defaultdict

    buckets: dict[str, list[dict]] = defaultdict(list)
    for q in questions:
        buckets[stem_template(q.get("question", ""))].append(q)

    for bucket in buckets.values():
        rng.shuffle(bucket)

    keys = list(buckets.keys())
    rng.shuffle(keys)
    keys.sort(key=lambda k: -len(buckets[k]))

    out: list[dict] = []
    last_keys: list[str] = []

    def can_place(key: str) -> bool:
        if not last_keys:
            return True
        run = 0
        for k in reversed(last_keys):
            if k == key:
                run += 1
            else:
                break
        return run < max_run

    while sum(len(buckets[k]) for k in buckets) > 0:
        placed = False
        for key in keys:
            if not buckets[key]:
                continue
            if can_place(key):
                out.append(buckets[key].pop(0))
                last_keys.append(key)
                if len(last_keys) > max_run:
                    last_keys = last_keys[-max_run:]
                placed = True
                break
        if not placed:
            # fallback: take from largest remaining bucket
            key = max((k for k in keys if buckets[k]), key=lambda k: len(buckets[k]))
            out.append(buckets[key].pop(0))
            last_keys = [key]

    return out


def interleave_candidates(candidates: list[Candidate], rng: random.Random) -> list[Candidate]:
    """Round-robin interleave candidates by stem template before refill."""
    from collections import defaultdict

    buckets: dict[str, list[Candidate]] = defaultdict(list)
    for c in candidates:
        buckets[stem_template(c[0])].append(c)
    for bucket in buckets.values():
        rng.shuffle(bucket)

    keys = list(buckets.keys())
    rng.shuffle(keys)
    keys.sort(key=lambda k: -len(buckets[k]))

    out: list[Candidate] = []
    while any(buckets[k] for k in keys):
        for key in keys:
            if buckets[key]:
                out.append(buckets[key].pop(0))
    return out


def is_filler_text(text: str) -> bool:
    if any(p.search(text) for p in FILLER_PATTERNS):
        return True
    if any(p.search(text) for p in BANNED_STEM_PATTERNS):
        return True
    return False


def is_filler_question(q: dict) -> bool:
    text = (
        q.get("question", "")
        + " "
        + " ".join(q.get("options", []))
        + " "
        + q.get("answer", "")
    )
    return is_filler_text(text)


def load_global_stems(exclude_file: str | None = None) -> set[str]:
    existing: set[str] = set()
    for path in BASE.glob("*.json"):
        if path.name in SKIP_GLOBAL or path.name == exclude_file:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for q in data.get("questions", []):
            stem = q.get("question", "").strip()
            if stem:
                existing.add(stem)
    return existing


def max_id_num(questions: list[dict], prefix: str) -> int:
    pat = re.compile(rf"^{re.escape(prefix)}(\d+)$")
    mx = 0
    for q in questions:
        m = pat.match(q.get("id", ""))
        if m:
            mx = max(mx, int(m.group(1)))
    return mx


def id_width(target: int) -> int:
    return max(3, len(str(target)))


def make_entry(prefix: str, num: int, q: str, opts: list[str], ans: str, diff: str, width: int = 3) -> dict:
    shuffled = list(opts)
    random.shuffle(shuffled)
    return {
        "id": f"{prefix}{num:0{width}d}",
        "question": q,
        "options": shuffled,
        "answer": ans,
        "difficulty": diff,
    }


def pick3(pool: list[str], correct: str, rng: random.Random) -> list[str]:
    wrong = list(dict.fromkeys(x for x in pool if x != correct))
    rng.shuffle(wrong)
    opts = [correct] + wrong[:3]
    while len(opts) < 4:
        opts.append("ഒന്നുമില്ല")
    return opts[:4]


def add_candidate(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    q: str,
    ans: str,
    wrong: list[str],
    diff: str = "medium",
    pool: list[str] | None = None,
) -> None:
    q = q.strip()
    if not q or q in existing or is_filler_text(q):
        return
    opts = pick3(pool or wrong + [ans], ans, rng)
    if len(set(opts)) != 4 or ans not in opts:
        return
    from option_type_utils import option_type_mismatch
    if option_type_mismatch(q, opts, ans):
        return
    out.append((q, opts, ans, diff))
    existing.add(q)


def refill_file(
    filename: str,
    prefix: str,
    target: int,
    candidates: list[Candidate],
    rng: random.Random,
    *,
    keep_existing: bool = True,
) -> dict[str, int]:
    """Refill one JSON bank to target with unique factual candidates."""
    path = BASE / filename
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"questions": []}

    if keep_existing:
        kept = [q for q in data.get("questions", []) if not is_filler_question(q)]
    else:
        kept = []

    existing: set[str] = load_global_stems(exclude_file=filename)
    existing.update(q.get("question", "").strip() for q in kept if q.get("question"))

    rng.shuffle(candidates)
    combined: list[dict] = list(kept)
    width = id_width(target)

    for q, opts, ans, diff in candidates:
        if len(combined) >= target:
            break
        if q in existing:
            continue
        combined.append(make_entry(prefix, len(combined) + 1, q, opts, ans, diff, width))

    # dedupe by stem
    final: list[dict] = []
    seen: set[str] = set()
    for i, q in enumerate(combined[:target], start=1):
        stem = q.get("question", "").strip()
        if not stem or stem in seen:
            continue
        seen.add(stem)
        entry = dict(q)
        entry["id"] = f"{prefix}{i:0{width}d}"
        final.append(entry)

    final = spread_consecutive_templates(final, rng, max_run=2)

    data["questions"] = final
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "file": filename,
        "target": target,
        "final": len(final),
        "kept": len(kept),
        "added": len(final) - len(kept),
        "shortfall": max(0, target - len(final)),
    }
