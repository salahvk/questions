#!/usr/bin/env python3
"""Build malayalam_wave20_data.py from curated lists + JSON extraction."""

from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).parent


def clean_ml(text: str) -> bool:
    if not text or not re.search(r"[\u0D00-\u0D7F]", text):
        return False
    if re.search(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]", text):
        return False
    stripped = re.sub(r"'[A-Za-z .,'\-]+'", "", text)
    if re.search(r"[a-zA-Z]{4,}", stripped):
        return False
    return True


def extract_author_works() -> list[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for fname in ("malayalam.json", "literature.json", "kerala_renaissance.json"):
        path = BASE / fname
        if not path.exists():
            continue
        for q in json.loads(path.read_text(encoding="utf-8")).get("questions", []):
            stem, ans = q.get("question", ""), q.get("answer", "")
            patterns = [
                (r"^(.+?)യുടെ പ്രസിദ്ധ കൃതി ഏത്\?$", lambda m: (m.group(1), ans)),
                (
                    r"^'([^']+)' എന്ന (?:കൃതി|വരി|കവിത) രചിച്ചത് ആര(?:്|ാണ്)\?$",
                    lambda m: (ans, m.group(1)),
                ),
                (
                    r"^'([^']+)' (?:രചിച്ചത്|എഴുതിയത്) ആര(?:്|ാണ്)\?$",
                    lambda m: (ans, m.group(1)),
                ),
                (r"^(.+?) രചിച്ച പ്രസിദ്ധ കൃതി ഏത്\?$", lambda m: (m.group(1), ans)),
            ]
            for pat, fn in patterns:
                m = re.match(pat, stem)
                if not m:
                    continue
                a, w = fn(m)
                if clean_ml(a) and (clean_ml(w) or re.fullmatch(r"[A-Za-z .,'\-]+", w)):
                    pairs.add((a, w))
    extra = [
        ("കുമാരനാശാൻ", "വീണാപൂവ്"),
        ("ഉള്ളൂർ", "ഉമാകേരളം"),
        ("വള്ളത്തോൾ", "ചിത്രയോഗം"),
        ("ചങ്ങമ്പുഴ", "രമണൻ"),
        ("വൈക്കം മുഹമ്മദ് ബഷീർ", "പാത്തുമ്മായുടെ ആട്"),
        ("തകഴി ശിവശങ്കരപ്പിള്ള", "കയറു"),
        ("എം.ടി. വാസുദേവൻ നായർ", "നാലുകെട്ട്"),
        ("ഒ.വി. വിജയൻ", "ഖസാക്കിന്റെ ഇതിഹാസം"),
        ("ബാലാമണിയമ്മ", "മുത്തശ്ശി"),
        ("സുഗതകുമാരി", "രാത്രിമഴ"),
        ("ഒ.എൻ.വി. കുറുപ്പ്", "ഭൂമിക്കൊരു ചരമഗീതം"),
        ("വൈലോപ്പിള്ളി ശ്രീധരമേനോൻ", "മാമ്പഴം"),
        ("തുഞ്ചത്ത് എഴുത്തച്ഛൻ", "ആധ്യാത്മരാമായണം"),
        ("ചെറുശ്ശേരി", "കൃഷ്ണഗാഥ"),
        ("ഒ. ചന്തുമേനോൻ", "ഇന്ദുലേഖ"),
        ("കുഞ്ചൻ നമ്പ്യാർ", "കുചേലവൃത്തം"),
        ("വയലാർ രാമവർമ", "സാഗരം"),
        ("ജി. ശങ്കരക്കുറുപ്പ്", "ഓടക്കുഴൽ"),
    ]
    for a, w in extra:
        if clean_ml(a) and clean_ml(w):
            pairs.add((a, w))
    return sorted(pairs)


def _repr_rows(name: str, rows) -> str:
    lines = [f"{name}: list = [\n"]
    for row in rows:
        lines.append(f"    {row!r},\n")
    lines.append("]\n")
    return "".join(lines)


def main() -> None:
    author_works = extract_author_works()
    parts = [
        '"""Malayalam wave20 curated data — 20 PSC categories."""\n\n',
        "from __future__ import annotations\n\n",
        _repr_rows("AUTHOR_WORKS", author_works),
    ]
    parts.append(_repr_rows("SYNONYMS", SYNONYMS))
    parts.append(_repr_rows("ANTONYMS", ANTONYMS))
    parts.append(_repr_rows("IDIOMS", IDIOMS))
    parts.append(_repr_rows("PROVERBS", PROVERBS))
    parts.append(_repr_rows("ONE_WORD", ONE_WORD))
    parts.append(_repr_rows("COMPOUNDS", COMPOUNDS))
    parts.append(_repr_rows("SPLITS", SPLITS))
    parts.append(_repr_rows("GENDER_VACANA", GENDER_VACANA))
    parts.append(_repr_rows("VIBHAKTI", VIBHAKTI))
    parts.append(_repr_rows("TRANSLATIONS", TRANSLATIONS))
    parts.append(_repr_rows("ALANKARAM", ALANKARAM))
    parts.append(_repr_rows("VRITHA", VRITHA))
    parts.append(_repr_rows("MOVEMENTS", MOVEMENTS))
    parts.append(_repr_rows("PEN_NAMES", PEN_NAMES))
    parts.append(_repr_rows("CHARACTERS", CHARACTERS))
    parts.append(_repr_rows("QUOTES", QUOTES))
    parts.append(_repr_rows("ANCIENT_WORKS", ANCIENT_WORKS))
    parts.append(_repr_rows("FOLK", FOLK))
    parts.append(_repr_rows("MAPPILA", MAPPILA))
    out = BASE / "malayalam_wave20_data.py"
    out.write_text("".join(parts), encoding="utf-8")
    print(f"wrote {out.name}: {len(author_works)} author-work pairs")


if __name__ == "__main__":
    main()
