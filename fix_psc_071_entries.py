#!/usr/bin/env python3
"""Idempotent helpers for PSC 071/2024 Malayalam fixes (already applied in JSON).

Run only if re-applying after git restore of specific rows.
"""

from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).parent


def patch(file: str, qid: str, **fields) -> None:
    path = BASE / file
    data = json.loads(path.read_text(encoding="utf-8"))
    for q in data["questions"]:
        if q.get("id") == qid:
            q.update(fields)
            break
    else:
        raise KeyError(f"{file}:{qid}")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def drop(file: str, qid: str) -> None:
    path = BASE / file
    data = json.loads(path.read_text(encoding="utf-8"))
    data["questions"] = [q for q in data["questions"] if q.get("id") != qid]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add(file: str, entry: dict) -> None:
    path = BASE / file
    data = json.loads(path.read_text(encoding="utf-8"))
    if any(q.get("id") == entry["id"] for q in data["questions"]):
        return
    data["questions"].append(entry)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    drop("mathematics.json", "mat_6778")
    add(
        "sports.json",
        {
            "id": "sca_193",
            "question": "താഴെ പറയുന്നവയിൽ വിചിത്രമായി കാണുന്നത്?",
            "options": [
                "ഫ്രഞ്ച് ഓപ്പൺ",
                "യുഎസ് ഓപ്പൺ",
                "വിംബിൾഡൺ",
                "ഡേവിസ് കപ്പ്",
            ],
            "answer": "ഡേവിസ് കപ്പ്",
            "difficulty": "easy",
        },
    )
    patch(
        "economics.json",
        "eco_2530",
        options=[
            "കൃഷ്ണമൂർത്തി സുബ്രമണ്യൻ",
            "സത്യേന്ദ്ര കിഷോർ",
            "വി. അനന്ത നാഗേശ്വരൻ",
            "എസ്. രാമകൃഷ്ണൻ",
        ],
        answer="കൃഷ്ണമൂർത്തി സുബ്രമണ്യൻ",
    )
    patch(
        "economics.json",
        "eco_2531",
        question=(
            "റിസർവ് ബാങ്ക്:\n"
            "1. ഐ.എം.എഫ്. അംഗം.\n"
            "2. 1935 ഏപ്രിൽ 1-ന് സ്ഥാപിച്ചു.\n"
            "3. ഉഷാ തോറാട്ട് ആദ്യ വനിതാ ഗവർണർ.\n"
            "ശരിയായ സംയോജനം?"
        ),
    )
    patch(
        "malayalam.json",
        "mal_100",
        options=[
            "ഉല്ലൂർ എസ്. നമ്പൂതിരിപ്പാട്",
            "വള്ളത്തോൾ നാരായണൻ",
            "എ. ആർ. രാജരാജവർമ്മ",
            "കുമാരനാശാൻ",
        ],
        answer="എ. ആർ. രാജരാജവർമ്മ",
    )
    print("Ensured PSC 071/2024 Malayalam fixes applied")


if __name__ == "__main__":
    main()
