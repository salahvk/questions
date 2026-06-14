#!/usr/bin/env python3
"""Fix journalism corruption and append verified Malayalam language facts."""

import json
import re
from pathlib import Path

SOURCE = Path("malayalam_wave20_source.json")
MIX = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")

LANGUAGE_FACTS = [
    {
        "question": "മലയാള ഭാഷാ ദിവസം ഏത് തീയതിയാണ്?",
        "answer": "നവംബർ ഒന്ന്",
        "pool": ["നവംബർ ഒന്ന്", "ഒക്ടോബർ രണ്ട്", "ഡിസംബർ പത്ത്", "ജൂൺ ഒന്ന്"],
    },
    {
        "question": "'ലീലാതിലകം' ഏത് കലാരൂപത്തെ സംബന്ധിച്ച ഗ്രന്ഥമാണ്?",
        "answer": "കഥകളി",
        "pool": ["കഥകളി", "മോഹിനിയാട്ടം", "കൂടിയാട്ടം", "തോൽപ്പാവക്കൂത്ത്"],
    },
    {
        "question": "'കൃഷ്ണഗാഥ' രചിച്ച കവി?",
        "answer": "ചേരുശ്ശേരി",
        "pool": ["ചേരുശ്ശേരി", "എഴുത്തച്ഛൻ", "കുഞ്ചൻ നമ്പൂതിരി", "വള്ളത്തോൾ"],
    },
    {
        "question": "'കിളിപ്പാട്ട്' എന്ന സാഹിത്യ രൂപം ആര്‍ക്ക് പ്രത്യേകമാണ്?",
        "answer": "തുഞ്ചത്ത് എഴുത്തച്ഛന്",
        "pool": ["തുഞ്ചത്ത് എഴുത്തച്ഛന്", "ചേരുശ്ശേരി", "കുഞ്ചൻ നമ്പൂതിരി", "അക്കിത്തം"],
    },
    {
        "question": "മണിപ്രാവള സാഹിത്യത്തിന്റെ സ്വഭാവം?",
        "answer": "മലയാളം-സംസ്കൃതം മിശ്രണം",
        "pool": [
            "മലയാളം-സംസ്കൃതം മിശ്രണം",
            "ശുദ്ധ മലയാളം മാത്രം",
            "ഇംഗ്ലീഷ്-മലയാളം മിശ്രണം",
            "തമിഴ്-മലയാളം മിശ്രണം",
        ],
    },
    {
        "question": "'രാജ്യസമാചാരം' പ്രസിദ്ധീകരിച്ച വർഷം?",
        "answer": "1847",
        "pool": ["1847", "1930", "1887", "1911"],
    },
    {
        "question": "'രാജ്യസമാചാരം' ആരംഭിച്ചത് ആരാണ്?",
        "answer": "ഹെർമൻ ഗുണ്ടർട്ട്",
        "pool": [
            "ഹെർമൻ ഗുണ്ടർട്ട്",
            "കെ. പി. കേശവമേനോൻ",
            "തകഴി ശിവശങ്കരപ്പിള്ള",
            "വക്കം അബ്ദുൽ ഖാദർ",
        ],
    },
    {
        "question": "മലയാള ലിപിയുടെ അക്ഷരസംഖ്യ (പരമ്പരാഗത)?",
        "answer": "51",
        "pool": ["51", "26", "33", "44"],
    },
    {
        "question": "'ആടുജീവിതം' രചിച്ചത് ആരാണ്?",
        "answer": "ബെന്നി പെരാശ്ശേരി",
        "pool": ["ബെന്നി പെരാശ്ശേരി", "ബഷീർ", "ഒ.വി. വൈദ്യനാഥൻ", "തകഴി ശിവശങ്കരപ്പിള്ള"],
    },
    {
        "question": "'ഖസാക്കിന്റെ ഇതിഹാസം' രചിച്ചത് ആരാണ്?",
        "answer": "ഒ.വി. വൈദ്യനാഥൻ",
        "pool": [
            "ഒ.വി. വൈദ്യനാഥൻ",
            "തകഴി ശിവശങ്കരപ്പിള്ള",
            "ബെന്നി പെരാശ്ശേരി",
            "വൈക്കം മുഹമ്മദ് ബഷീർ",
        ],
    },
    {
        "question": "'നാലുകെട്ട്' രചിച്ചത് ആരാണ്?",
        "answer": "തകഴി ശിവശങ്കരപ്പിള്ള",
        "pool": ["തകഴി ശിവശങ്കരപ്പിള്ള", "ഒ.വി. വൈദ്യനാഥൻ", "ബെന്നി പെരാശ്ശേരി", "എഴുത്തച്ഛൻ"],
    },
    {
        "question": "'The God of Small Things' രചിച്ചത് ആരാണ്?",
        "answer": "അരുണ്ധതി റോയ്",
        "pool": ["അരുണ്ധതി റോയ്", "മാധവിക്കുട്ടി", "ബെന്നി പെരാശ്ശേരി", "ഒ.വി. വൈദ്യനാഥൻ"],
    },
    {
        "question": "മലയാളത്തിലെ ആദ്യത്തെ സ്ത്രീ സാഹിത്യ പ്രതിഭ?",
        "answer": "മാധവിക്കുട്ടി",
        "pool": ["മാധവിക്കുട്ടി", "അരുണ്ധതി റോയ്", "ബാലാമണിയമ്മ", "സുഗതകുമാരി"],
    },
    {
        "question": "'മാതൃഭൂമി' ആരംഭിച്ചത് ആരാണ്?",
        "answer": "കെ. പി. കേശവമേനോൻ",
        "pool": ["കെ. പി. കേശവമേനോൻ", "ഹെർമൻ ഗുണ്ടർട്ട്", "വക്കം അബ്ദുൽ ഖാദർ", "തകഴി ശിവശങ്കരപ്പിള്ള"],
    },
]


def main() -> None:
    for row in LANGUAGE_FACTS:
        for cell in [row["question"], row["answer"], *row["pool"]]:
            if MIX.search(cell):
                raise ValueError(f"mixed script: {cell!r}")

    data = json.loads(SOURCE.read_text(encoding="utf-8"))

    for row in data.get("journalism", []):
        q = row.get("question", "")
        if "eralakaumudi" in q or q == "കeralakaumudi":
            row["question"] = "'ഹെർമൻ ഗുണ്ടർട്ട്' ബന്ധപ്പെട്ട മലയാള പത്രം?"
            row["answer"] = "രാജ്യസമാചാരം"

    existing = {r["question"] for r in data.get("language_facts", [])}
    merged = list(data.get("language_facts", []))
    for row in LANGUAGE_FACTS:
        if row["question"] not in existing:
            merged.append(row)
            existing.add(row["question"])

    data["language_facts"] = merged
    SOURCE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"language_facts: {len(merged)} rows")


if __name__ == "__main__":
    main()
