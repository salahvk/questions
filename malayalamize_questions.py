#!/usr/bin/env python3
"""Convert English/mixed quiz text to pure Malayalam in JSON question files."""

import json
import re
from pathlib import Path

from malayalam_translations import EXACT_MAP, ID_OVERRIDES, PHRASE_SUBS

BASE = Path(__file__).parent

SKIP_FILES = {"english_language.json", "current_affairs_manifest.json"}


def target_files() -> list[str]:
    return sorted(
        p.name
        for p in BASE.glob("*.json")
        if p.name not in SKIP_FILES
    )

PRESERVE = re.compile(
    r"\b("
    r"GST|ISRO|FIFA|UPI|NEP|IMEC|ECI|IMD|DRDO|NASA|UNFCCC|WHO|IMF|WTO|G20|KFON|"
    r"IN-SPACe|PM-JAY|ICC|IPL|ISL|I-League|EPL|ODI|T20|BJP|UDF|LDF|NDA|CPI|CPM|"
    r"RSP|IUML|BDJS|PTA|PWD|NGT|PLI|PM-KISAN|NITI|ICDS|NSAP|PMMVY|NRHM|NUHM|"
    r"DAY-NRLM|DAY-NULM|HRIDAY|AMRUT|SAUBHAGYA|POSHAN|ABDM|WANI|"
    r"PVTG|SVANidhi|FME|MITRA|NMEO|ICRC|GATT|NATO|OPEC|BRICS|ASEAN|SAARC|"
    r"ILO|FAO|IAEA|UNICEF|UNHCR|EU|DPIIT|STPI|SEZ|KVIC|NALCO|HAL|BHEL|SAIL|"
    r"ONGC|NTPC|IOCL|GAIL|NHPC|BEL|BEML|HMT|MIDHANI|SCI|DMIC|DFC|MSME|SIDBI|"
    r"IDI|PSU|ABDM|IGS|Huddle Global|Oscars|Wimbledon|Compliance|"
    r"Huddle Global/IGS|80G|AYUSH|PwD|SC/ST|LPG|USA|IMEC|NASA|IN-SPACe"
    r")\b",
    re.I,
)


def has_english_descriptive(text: str) -> bool:
    cleaned = PRESERVE.sub("", text)
    return bool(re.search(r"[a-zA-Z]{3,}", cleaned))


def apply_phrase_subs(text: str) -> str:
    result = text
    for old, new in PHRASE_SUBS:
        if old in result:
            result = result.replace(old, new)
    return result


def malayalamize_text(text: str) -> str:
    if not text:
        return text
    if text in EXACT_MAP:
        return EXACT_MAP[text]
    mapped = apply_phrase_subs(text)
    if mapped in EXACT_MAP:
        return EXACT_MAP[mapped]
    return mapped


def malayalamize_question(q: dict) -> tuple[dict, bool]:
    qid = q.get("id", "")
    if qid in ID_OVERRIDES:
        new_q = dict(q)
        override = ID_OVERRIDES[qid]
        new_q["question"] = override["question"]
        new_q["options"] = list(override["options"])
        new_q["answer"] = override["answer"]
        changed = (
            new_q["question"] != q["question"]
            or new_q["options"] != q["options"]
            or new_q["answer"] != q["answer"]
        )
        return new_q, changed

    changed = False
    new_q = dict(q)

    old_q = q.get("question", "")
    new_q_text = malayalamize_text(old_q)
    if new_q_text != old_q:
        new_q["question"] = new_q_text
        changed = True

    old_ans = q.get("answer", "")
    new_ans = malayalamize_text(old_ans)
    if new_ans != old_ans:
        new_q["answer"] = new_ans
        changed = True

    new_opts = []
    for opt in q.get("options", []):
        new_opt = malayalamize_text(opt)
        if new_opt != opt:
            changed = True
        new_opts.append(new_opt)
    new_q["options"] = new_opts

    return new_q, changed


def process_file(filename: str) -> tuple[int, list[tuple[str, str, str]]]:
    path = BASE / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.get("questions", [])
    updated = 0
    samples: list[tuple[str, str, str]] = []

    for i, q in enumerate(questions):
        new_q, changed = malayalamize_question(q)
        if changed:
            if filename == "current_affairs_2026_06.json" and len(samples) < 5:
                samples.append((q.get("id", ""), q.get("question", ""), new_q["question"]))
            questions[i] = new_q
            updated += 1

    data["questions"] = questions
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return updated, samples


def main() -> None:
    total = 0
    all_samples: list[tuple[str, str, str]] = []

    print("Malayalamizing quiz questions...\n")
    for filename in target_files():
        count, samples = process_file(filename)
        total += count
        print(f"  {filename}: {count} questions updated")
        if samples:
            all_samples.extend(samples)

    print(f"\nTotal updated: {total}")

    if all_samples:
        print("\n--- Sample before/after (current_affairs) ---")
        for qid, before, after in all_samples[:5]:
            print(f"\n[{qid}]")
            print(f"  BEFORE: {before}")
            print(f"  AFTER:  {after}")


if __name__ == "__main__":
    main()
