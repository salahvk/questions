#!/usr/bin/env python3
"""Expand and clean malayalam_wave20_source.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).parent
SOURCE = BASE / "malayalam_wave20_source.json"


def clean_ml(text: str) -> bool:
    if not text or not re.search(r"[\u0D00-\u0D7F]", text):
        return False
    if re.search(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]", text):
        return False
    stripped = re.sub(r"'[A-Za-z .,'\-]+'", "", text)
    return not re.search(r"[a-zA-Z]{4,}", stripped)


def clean_author_works(rows: list[dict]) -> list[dict]:
    seen: set[tuple[str, str]] = set()
    out: list[dict] = []
    for row in rows:
        a, w = row["author"], row["work"]
        if not clean_ml(a):
            continue
        if w.startswith("രാമനാഥൻ "):
            continue
        if w.startswith("ഓടക്കുഴലിന്റെ "):
            continue
        key = (a, w)
        if key in seen:
            continue
        seen.add(key)
        out.append({"author": a, "work": w})
    return out


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    data["author_works"] = clean_author_works(data.get("author_works", []))

    data["antonyms"] = [
        {"a": "ദീർഘ", "b": "ഹ്രസ്വ"},
        {"a": "ഉയർന്ന", "b": "താഴ്ന്ന"},
        {"a": "വലിയ", "b": "ചെറിയ"},
        {"a": "നല്ല", "b": "മോശം"},
        {"a": "പുതിയ", "b": "പഴയ"},
        {"a": "സന്തോഷം", "b": "ദുഃഖം"},
        {"a": "സ്നേഹം", "b": "വൈരം"},
        {"a": "ധൈര്യം", "b": "ഭയം"},
        {"a": "വേഗം", "b": "നിശ്ചലത"},
        {"a": "വെളിച്ചം", "b": "ഇരുട്ട്"},
        {"a": "ചൂട്", "b": "തണുപ്പ്"},
        {"a": "മേൽ", "b": "താഴ"},
        {"a": "ആദ്യ", "b": "അവസാന"},
        {"a": "അകലെ", "b": "സമീപ"},
        {"a": "അധികം", "b": "കുറവ"},
        {"a": "സത്യം", "b": "അസത്യം"},
        {"a": "ജ്ഞാനം", "b": "അജ്ഞത"},
        {"a": "ശക്തി", "b": "ദൗർബല്യം"},
        {"a": "സമ്പന്ന", "b": "ദരിദ്ര"},
        {"a": "സുഖം", "b": "ദുഃഖം"},
        {"a": "ജീവൻ", "b": "മരണം"},
        {"a": "മധുരം", "b": "കയ്പ"},
        {"a": "നഗരം", "b": "ഗ്രാമം"},
        {"a": "പൂർണ്ണ", "b": "അപൂർണ്ണ"},
        {"a": "ഉഷ", "b": "സായ"},
        {"a": "ദിവസ", "b": "രാത"},
        {"a": "ഏക", "b": "ബഹു"},
        {"a": "ആണ", "b": "പെൺ"},
        {"a": "മുകള", "b": "താഴ"},
        {"a": "ആരംഭ", "b": "അവസാന"},
        {"a": "ഉയർ", "b": "താഴ"},
        {"a": "ശുഭ", "b": "അശുഭ"},
        {"a": "ധന", "b": "ദാരിദ്ര"},
        {"a": "യുദ്ധ", "b": "സമാധാന"},
        {"a": "ബല", "b": "ദൗർബല"},
        {"a": "ദൂര", "b": "സമീപ"},
        {"a": "പ്രധാന", "b": "ഗൗണ"},
        {"a": "വിശേഷ", "b": "സാധാരണ"},
        {"a": "പ്രകാശ", "b": "ഇര"},
        {"a": "സുന്ദര", "b": "അസുന്ദര"},
    ]

    data["idioms"] = [
        {"phrase": "കണ്ണിൽ കോടി", "meaning": "വളരെ വിലപ്പെട്ടത്"},
        {"phrase": "കാതിൽ കയറി", "meaning": "ശ്രദ്ധിക്കാതിരിക്കുക"},
        {"phrase": "കയ്യിൽ കിട്ടിയത്", "meaning": "ലഭിച്ച അവസരം"},
        {"phrase": "വായിൽ വരാത്തത്", "meaning": "പറയാൻ കഴിയാത്തത്"},
        {"phrase": "മനസ്സിൽ കയറി", "meaning": "ഓർമ്മയിൽ നിൽക്കുക"},
        {"phrase": "തലയിൽ കയറി", "meaning": "അധികാരം കാണിക്കുക"},
        {"phrase": "കാലിൽ ചവിട്ടി", "meaning": "അവഹേലിക്കുക"},
        {"phrase": "നെഞ്ചിൽ ചേർത്തു", "meaning": "സ്നേഹിച്ചു"},
        {"phrase": "കൈവിട്ടു", "meaning": "ഉപേക്ഷിച്ചു"},
        {"phrase": "കണ്ണുനീർ കുടിച്ചു", "meaning": "ദുഃഖിച്ചു"},
        {"phrase": "തലയിൽ കുത്തി", "meaning": "അപമാനിച്ചു"},
        {"phrase": "കയ്യിൽ പിടിച്ചു", "meaning": "സഹായിച്ചു"},
        {"phrase": "വായ് തുറന്നു", "meaning": "സംസാരിച്ചു"},
        {"phrase": "കാൽ നീട്ടി", "meaning": "ആഗ്രഹിച്ചു"},
        {"phrase": "കണ്ണ് തുറന്നു", "meaning": "ശ്രദ്ധിച്ചു"},
        {"phrase": "മനസ്സ് തുറന്നു", "meaning": "സ്വീകരിച്ചു"},
        {"phrase": "കൈ കൊടുത്തു", "meaning": "സഹായിച്ചു"},
        {"phrase": "തല കുനിച്ചു", "meaning": "അനുയമിച്ചു"},
        {"phrase": "നെഞ്ച് പൊടിഞ്ഞു", "meaning": "വളരെ ദുഃഖിച്ചു"},
        {"phrase": "കണ്ണ് നിറഞ്ഞു", "meaning": "കരഞ്ഞു"},
        {"phrase": "വായ് പൊളിഞ്ഞു", "meaning": "വളരെ ഞെട്ടി"},
        {"phrase": "കാൽ വഴുതി", "meaning": "വീണു"},
        {"phrase": "കൈ വിട്ടു", "meaning": "ഉപേക്ഷിച്ചു"},
        {"phrase": "മനസ്സ് മായ്ച്ചു", "meaning": "മറന്നു"},
        {"phrase": "തലയിൽ വെച്ചു", "meaning": "ഗൗരവിച്ചു"},
        {"phrase": "കണ്ണിൽ കാണാതെ", "meaning": "ശ്രദ്ധിക്കാതെ"},
        {"phrase": "കാതിൽ കേൾക്കാതെ", "meaning": "ഗൗരവിക്കാതെ"},
        {"phrase": "കയ്യിൽ എടുത്തു", "meaning": "സ്വീകരിച്ചു"},
        {"phrase": "വായിൽ വെച്ചു", "meaning": "പറഞ്ഞു"},
        {"phrase": "കാലിൽ വീണു", "meaning": "ശരണം പ്രാപിച്ചു"},
    ]

    data["proverbs"] = [
        {"proverb": "ആന വായിൽ അമ്പഴങ്ങ", "meaning": "അസാധ്യമായ കാര്യം"},
        {"proverb": "കാക്ക കുളിച്ചാലും കറുത്തതു തന്നെ", "meaning": "സ്വഭാവം മാറില്ല"},
        {"proverb": "കuirichaalum", "meaning": "placeholder"},
    ]

    SOURCE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("partial write - needs completion")


if __name__ == "__main__":
    main()
