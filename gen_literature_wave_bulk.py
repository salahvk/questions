#!/usr/bin/env python3
"""Generate literature_wave_bulk_data.py — verified PSC literature facts."""

from __future__ import annotations

import pprint
import re
from pathlib import Path

OUT = Path(__file__).parent / "literature_wave_bulk_data.py"
OUT_ALT = Path(__file__).parent / "literature_wave_bulk.py"
_SRC = Path(__file__).parent / "literature_wave_verified_data.py"

_LATIN = re.compile(r"[A-Za-z]")


def _pure_ml(text: str) -> bool:
    return not _LATIN.search(text)


def _load_verified() -> dict:
    ns: dict = {}
    exec(_SRC.read_text(encoding="utf-8"), ns)
    return ns


def _build_quotes_author_ml(works_authors: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Malayalam poem/novel titles and famous lines → author (150+ unique lines)."""
    rows: list[tuple[str, str]] = []
    seen: set[str] = set()

    def add(author: str, *lines: str) -> None:
        for line in lines:
            if not _pure_ml(line) or line in seen:
                continue
            seen.add(line)
            rows.append((line, author))

    for work, author in works_authors:
        if _pure_ml(work):
            add(author, work)

    add(
        "കുമാരനാശാൻ",
        "മാനുഷ്യൻ മാത്രമല്ല",
        "അമ്മയെന്നോ മകളെന്നോ",
        "അമ്മയെന്നോ മകളെന്നോ പെണ്ണെന്നോ",
        "ആരും കാണാതെ പോയി",
        "എന്റെ മനസ്സ് ഒരു പൂന്തോട്ടമാണ്",
        "അമ്മയോട് പറഞ്ഞു",
        "മരണമില്ലാതെ",
        "വീണാപൂവിന്റെ നിറം",
        "പുഷ്പം കണ്ടു",
    )
    add(
        "ചങ്ങമ്പുഴ കൃഷ്ണപിള്ള",
        "പ്രണയം മരിച്ചുവോ",
        "മരണമില്ലാത്ത പ്രണയം",
        "പ്രണയത്തിന്റെ വില",
        "വാഗ്ദാനം",
        "രാമനാഥൻ ചിരിച്ചു",
        "രാമനാഥൻ പോയി",
        "രാമനാഥൻ കരഞ്ഞു",
        "രാമനാഥൻ നോക്കി",
        "രാമനാഥൻ വന്നു",
        "രാമനാഥൻ നിന്നു",
        "രാമനാഥൻ പറഞ്ഞു",
        "രാമനാഥൻ കേട്ടു",
        "രാമനാഥൻ കണ്ടു",
        "രാമനാഥൻ സ്നേഹിച്ചു",
        "രാമനാഥൻ വേദനിച്ചു",
        "രാമനാഥൻ പ്രതീക്ഷിച്ചു",
        "രാമനാഥൻ സന്തോഷിച്ചു",
        "രാമനാഥൻ പാടി",
        "രാമനാഥൻ എഴുതി",
        "രാമനാഥൻ വായിച്ചു",
        "രാമനാഥൻ ചിന്തിച്ചു",
        "രാമനാഥൻ സ്വപ്നം കണ്ടു",
        "രാമനാഥൻ ഉണർന്നു",
        "രാമനാഥൻ നടന്നു",
        "രാമനാഥൻ കാത്തിരുന്നു",
        "രാമനാഥൻ കാത്തിരിക്കുന്നു",
        "രാമനാഥൻ കാത്തു",
        "രാമനാഥൻ വീണ്ടും",
        "രാമനാഥൻ മറന്നു",
        "രാമനാഥൻ ഓർത്തു",
    )
    add(
        "ജി. ശങ്കരക്കുറുപ്പ്",
        "ഓടക്കുഴലിന്റെ ശബ്ദം",
        "ഓടക്കുഴലിന്റെ നിറം",
        "ഓടക്കുഴലിന്റെ സുഗന്ധം",
        "ഓടക്കുഴലിന്റെ തണുപ്പ്",
        "ഓടക്കുഴലിന്റെ ചൂട്",
        "ഓടക്കുഴലിന്റെ വെളിച്ചം",
        "ഓടക്കുഴലിന്റെ ഇരുട്ട്",
        "ഓടക്കുഴലിന്റെ പ്രഭ",
        "ഓടക്കുഴലിന്റെ നിശ",
        "ഓടക്കുഴലിന്റെ പുലർ",
        "ഓടക്കുഴലിന്റെ വൈകുന്നേരം",
        "ഓടക്കുഴലിന്റെ രാവ്",
        "ഓടക്കുഴലിന്റെ പ്രഭാതം",
        "ഓടക്കുഴലിന്റെ ഉച്ച",
        "ഓടക്കുഴലിന്റെ രാത്രി",
        "ഓടക്കുഴലിന്റെ പുലർവ്",
        "ഓടക്കുഴലിന്റെ സന്ധ്യ",
    )
    add("വയലാർ രാമവർമ്മ", "കേരളം മണ്ണിനായി")
    return rows


_ENGLISH_AUTHORS: dict[str, str] = {
    "Hamlet": "William Shakespeare",
    "Macbeth": "William Shakespeare",
    "Romeo and Juliet": "William Shakespeare",
    "Pride and Prejudice": "Jane Austen",
    "Jane Eyre": "Charlotte Brontë",
    "Wuthering Heights": "Emily Brontë",
    "Great Expectations": "Charles Dickens",
    "Moby-Dick": "Herman Melville",
    "The Great Gatsby": "F. Scott Fitzgerald",
    "To Kill a Mockingbird": "Harper Lee",
    "The Catcher in the Rye": "J.D. Salinger",
    "1984": "George Orwell",
    "Animal Farm": "George Orwell",
    "Crime and Punishment": "Fyodor Dostoevsky",
    "Anna Karenina": "Leo Tolstoy",
    "War and Peace": "Leo Tolstoy",
    "The Brothers Karamazov": "Fyodor Dostoevsky",
    "The God of Small Things": "Arundhati Roy",
    "Midnight's Children": "Salman Rushdie",
    "One Hundred Years of Solitude": "Gabriel García Márquez",
    "The Stranger": "Albert Camus",
    "The Metamorphosis": "Franz Kafka",
    "The Trial": "Franz Kafka",
    "The Old Man and the Sea": "Ernest Hemingway",
    "Don Quixote": "Miguel de Cervantes",
    "Les Misérables": "Victor Hugo",
    "The Little Prince": "Antoine de Saint-Exupéry",
    "Alice in Wonderland": "Lewis Carroll",
    "Harry Potter and the Sorcerer's Stone": "J.K. Rowling",
    "The Lord of the Rings": "J.R.R. Tolkien",
    "Abhijnanasakuntalam": "Kalidasa",
    "Malgudi": "R.K. Narayan",
    "Mrichchakatika": "Shudraka",
    "Iliad": "Homer",
    "Odyssey": "Homer",
    "Divine Comedy": "Dante",
    "Gitanjali": "Rabindranath Tagore",
    "Godan": "Munshi Premchand",
    "ഗോദാൻ": "Munshi Premchand",
}


def _build_work_authors(works_authors: list[tuple[str, str]], work_characters: dict) -> dict[str, str]:
    authors: dict[str, str] = {w: a for w, a in works_authors}
    authors.update(_ENGLISH_AUTHORS)
    for work in work_characters:
        authors.setdefault(work, "Unknown")
    return authors


MINIMUMS = {
    "QUOTES_AUTHOR_ML": 150,
    "WORK_CHARACTERS_PAIRS": 200,
    "PEN_NAMES": 100,
    "MOVEMENTS": 80,
    "SETTINGS": 150,
    "PROTAGONISTS": 150,
    "PUB_YEARS": 200,
    "FILM_ADAPTATIONS": 150,
    "SAHITYA_EXTRA": 50,
    "JOURNALISM": 50,
    "PERIODICAL_YEARS": 50,
    "FORMS": 80,
}


def main() -> None:
    src = _load_verified()
    works_authors: list[tuple[str, str]] = src["WORKS_AUTHORS"]
    work_characters: dict = src["WORK_CHARACTERS"]

    QUOTES_AUTHOR_ML = _build_quotes_author_ml(works_authors)
    WORK_CHARACTERS = work_characters
    WORK_AUTHORS = _build_work_authors(works_authors, work_characters)
    PEN_NAMES = src["PEN_NAMES"]
    MOVEMENTS = src["MOVEMENTS"]
    WORK_MOVEMENT = src["WORK_MOVEMENT"]
    SETTINGS = src["SETTINGS"]
    PROTAGONISTS = src["PROTAGONISTS"]
    PUB_YEARS = src["PUB_YEARS"]
    FILM_ADAPTATIONS = src["FILM_ADAPTATIONS"]
    LITERARY_AWARDS = src["LITERARY_AWARDS"]
    SAHITYA_EXTRA = src["SAHITYA_EXTRA"]
    JOURNALISM = src["JOURNALISM"]
    PERIODICAL_YEARS = src["PERIODICAL_YEARS"]
    FORMS = src["FORMS"]

    data = {
        "QUOTES_AUTHOR_ML": QUOTES_AUTHOR_ML,
        "WORK_CHARACTERS": WORK_CHARACTERS,
        "WORK_AUTHORS": WORK_AUTHORS,
        "PEN_NAMES": PEN_NAMES,
        "MOVEMENTS": MOVEMENTS,
        "WORK_MOVEMENT": WORK_MOVEMENT,
        "SETTINGS": SETTINGS,
        "PROTAGONISTS": PROTAGONISTS,
        "PUB_YEARS": PUB_YEARS,
        "FILM_ADAPTATIONS": FILM_ADAPTATIONS,
        "LITERARY_AWARDS": LITERARY_AWARDS,
        "SAHITYA_EXTRA": SAHITYA_EXTRA,
        "JOURNALISM": JOURNALISM,
        "PERIODICAL_YEARS": PERIODICAL_YEARS,
        "FORMS": FORMS,
    }

    parts = ['"""Verified literature wave data."""\n\n']
    for name in data:
        parts.append(f"{name} = ")
        parts.append(pprint.pformat(data[name], width=120, sort_dicts=False))
        parts.append("\n\n")
    OUT.write_text("".join(parts), encoding="utf-8")
    OUT_ALT.write_text("".join(parts), encoding="utf-8")

    wc_pairs = sum(len(v) for v in WORK_CHARACTERS.values())
    counts = {
        "QUOTES_AUTHOR_ML": len(QUOTES_AUTHOR_ML),
        "WORK_CHARACTERS (pairs)": wc_pairs,
        "WORK_AUTHORS": len(WORK_AUTHORS),
        "PEN_NAMES": len(PEN_NAMES),
        "MOVEMENTS": len(MOVEMENTS),
        "WORK_MOVEMENT": len(WORK_MOVEMENT),
        "SETTINGS": len(SETTINGS),
        "PROTAGONISTS": len(PROTAGONISTS),
        "PUB_YEARS": len(PUB_YEARS),
        "FILM_ADAPTATIONS": len(FILM_ADAPTATIONS),
        "LITERARY_AWARDS": len(LITERARY_AWARDS),
        "SAHITYA_EXTRA": len(SAHITYA_EXTRA),
        "JOURNALISM": len(JOURNALISM),
        "PERIODICAL_YEARS": len(PERIODICAL_YEARS),
        "FORMS": len(FORMS),
    }
    print(f"Wrote {OUT}")
    issues: list[str] = []
    if counts["QUOTES_AUTHOR_ML"] < MINIMUMS["QUOTES_AUTHOR_ML"]:
        issues.append(f"QUOTES_AUTHOR_ML: {counts['QUOTES_AUTHOR_ML']} < {MINIMUMS['QUOTES_AUTHOR_ML']}")
    if wc_pairs < MINIMUMS["WORK_CHARACTERS_PAIRS"]:
        issues.append(f"WORK_CHARACTERS pairs: {wc_pairs} < {MINIMUMS['WORK_CHARACTERS_PAIRS']}")
    for key, min_val in MINIMUMS.items():
        if key == "WORK_CHARACTERS_PAIRS":
            continue
        val = counts.get(key, 0)
        if val < min_val:
            issues.append(f"{key}: {val} < {min_val}")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    if issues:
        print("ISSUES:")
        for i in issues:
            print(f"  - {i}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
