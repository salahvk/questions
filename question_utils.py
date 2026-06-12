#!/usr/bin/env python3
"""Shared utilities for generating unique MCQ questions."""
import json
import os
import random
import re

random.seed(42)

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
