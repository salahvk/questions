#!/usr/bin/env python3
"""Fill all category JSON files to at least 500 unique questions."""
import json
import os
import re

from question_utils import (
    add_unique,
    load_existing,
    make_mcq,
    max_id,
    reindex_questions,
    space_inverse_question_pairs,
)

from gen_general import (
    facts_awards_current,
    facts_basic_gk,
    facts_cinema,
    facts_communication_journalism,
    facts_continents,
    facts_english,
    facts_information_technology,
    facts_international_orgs,
    facts_literature,
    facts_malayalam,
    facts_philosophy,
    facts_sports_current,
    facts_world_history,
)
from gen_india import (
    facts_constitution,
    facts_indian_history,
    facts_indian_industries,
    facts_modern_india,
    facts_national_schemes,
    facts_social_welfare_schemes,
)
from gen_kerala import (
    facts_history_of_kerala,
    facts_important_institutions,
    facts_kerala_districts,
    facts_kerala_renaissance,
    facts_politics_of_kerala,
)
from gen_science import (
    facts_astronomy,
    facts_biology,
    facts_chemistry,
    facts_mathematics,
    facts_natural_science,
    facts_physics,
)

TARGET = 500
MATH_TARGET = 1000

DIFF_MAP = {
    "easy": "easy",
    "medium": "medium",
    "hard": "hard",
    "ലഘു": "easy",
    "ഇടത്തരം": "medium",
    "കഠിനം": "hard",
}


def norm_diff(value):
    return DIFF_MAP.get(str(value).strip(), "medium")


def append_facts(seen, questions, prefix, counter, facts, need):
    added = 0
    for item in facts:
        if added >= need:
            break
        if len(item) == 4:
            qtext, answer, wrong, diff = item
        else:
            continue
        mcq = make_mcq(qtext, answer, wrong, norm_diff(diff))
        counter, ok = add_unique(seen, questions, prefix, counter, mcq)
        if ok:
            added += 1
    return counter, added


def fill(fname, prefix, fact_sources, target=TARGET):
    seen, files = load_existing()
    existing = files.get(fname, {}).get("questions", [])
    questions = list(existing)
    for q in existing:
        seen.add(q["question"].strip())
    counter = max_id(questions, prefix)

    for facts_fn in fact_sources:
        if len(questions) >= target:
            break
        need = target - len(questions)
        counter, _ = append_facts(seen, questions, prefix, counter, facts_fn(), need)

    questions = space_inverse_question_pairs(questions)
    reindex_questions(questions, prefix)

    with open(fname, "w", encoding="utf-8") as f:
        json.dump({"questions": questions}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return len(questions)


CATEGORIES = [
    ("kerala_through_districts.json", "ktd", [facts_kerala_districts]),
    ("kerala_renaissance.json", "kr", [facts_kerala_renaissance]),
    ("history_of_kerala.json", "hok", [facts_history_of_kerala]),
    ("politics_of_kerala.json", "pok", [facts_politics_of_kerala]),
    ("important_institutions.json", "ii", [facts_important_institutions]),
    ("indian_history.json", "ih", [facts_indian_history]),
    ("modern_india.json", "mi", [facts_modern_india]),
    ("constitution_of_india.json", "coi", [facts_constitution]),
    ("national_schemes.json", "ns", [facts_national_schemes]),
    ("social_welfare_schemes.json", "sws", [facts_social_welfare_schemes]),
    ("indian_industries.json", "ind", [facts_indian_industries]),
    ("physics.json", "phy", [facts_physics]),
    ("chemistry.json", "che", [facts_chemistry]),
    ("biology.json", "bio", [facts_biology]),
    ("astronomy.json", "ast", [facts_astronomy]),
    ("natural_science.json", "nsc", [facts_natural_science]),
    ("mathematics.json", "mat", [facts_mathematics], MATH_TARGET),
    ("world_history.json", "wh", [facts_world_history]),
    ("continents_of_the_world.json", "cow", [facts_continents]),
    ("international_organizations.json", "io", [facts_international_orgs]),
    ("information_technology.json", "it", [facts_information_technology]),
    ("basic_general_knowledge.json", "bgk", [facts_basic_gk]),
    ("english_language.json", "eng", [facts_english]),
    ("malayalam.json", "mal", [facts_malayalam]),
    ("philosophy.json", "phi", [facts_philosophy]),
    ("literature.json", "lit", [facts_literature]),
    ("communication_journalism.json", "cj", [facts_communication_journalism]),
    ("cinema.json", "cin", [facts_cinema]),
    ("sports.json", "sca", [facts_sports_current]),
    ("awards.json", "aca", [facts_awards_current]),
]

SKIP = {
    "arts.json",
    "economics.json",
    "education.json",
    "geography.json",
    "historical_monuments_of_kerala.json",
}


def validate():
    seen = set()
    issues = []
    for fname in sorted(os.listdir(".")):
        if not fname.endswith(".json") or fname.startswith("current_affairs"):
            continue
        if fname in SKIP or fname == "current_affairs_manifest.json":
            continue
        with open(fname, encoding="utf-8") as f:
            data = json.load(f)
        qs = data.get("questions", [])
        texts = [q["question"].strip() for q in qs]
        min_target = MATH_TARGET if fname == "mathematics.json" else TARGET
        if len(qs) < min_target:
            issues.append(f"{fname}: only {len(qs)} questions")
        if len(set(texts)) != len(texts):
            issues.append(f"{fname}: duplicate questions locally")
        bad = [q for q in qs if q["answer"] not in q["options"]]
        if bad:
            issues.append(f"{fname}: {len(bad)} answers not in options")
        for t in texts:
            if t in seen:
                issues.append(f"CROSS-DUP: {fname} -> {t[:70]}")
            seen.add(t)
    return issues


def main():
    for entry in CATEGORIES:
        fname, prefix, sources = entry[:3]
        target = entry[3] if len(entry) > 3 else TARGET
        count = fill(fname, prefix, sources, target=target)
        status = "OK" if count >= target else "SHORT"
        print(f"{status} {fname}: {count}")

    issues = validate()
    if issues:
        print("\nVALIDATION ISSUES:")
        for i in issues[:50]:
            print(" ", i)
        if len(issues) > 50:
            print(f"  ... and {len(issues) - 50} more")
    else:
        print("\nAll categories validated OK (500+ unique, answers match).")


if __name__ == "__main__":
    main()
