#!/usr/bin/env python3
"""Wave 20 Malayalam PSC facts — 20 categories from malayalam_wave20_source.json."""

from __future__ import annotations

import json
import random
import re
from pathlib import Path

from refill_common import Candidate, add_candidate, interleave_candidates

BASE = Path(__file__).parent
SOURCE = BASE / "malayalam_wave20_source.json"


def _pool(items: list[str], correct: str) -> list[str]:
    return [x for x in items if x != correct]


def _emit(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    stem: str,
    ans: str,
    wrong: list[str],
    pool: list[str],
    diff: str = "medium",
) -> None:
    add_candidate(out, existing, rng, stem, ans, wrong, diff, pool=pool)


def _load() -> dict:
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def _cat_synonyms(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    rows = data.get("synonyms", [])
    all_syns = list(dict.fromkeys(s for r in rows for s in r["syns"]))
    for row in rows:
        word, syns, non = row["word"], row["syns"], row["wrong"]
        pool = syns + [non, word]
        _emit(out, existing, rng, f"'{word}' — പര്യായം?", syns[0], syns[1:] + [non], pool)
        _emit(out, existing, rng, f"'{word}' — പര്യായമല്ലാത്തത്?", non, syns[:3], pool)
        _emit(out, existing, rng, f"പര്യായമായി '{word}' ഉപയോഗിക്കാവുന്ന പദം?", syns[0], _pool(all_syns, syns[0])[:3], all_syns)
        _emit(out, existing, rng, f"'{word}'-ന്റെ പര്യായം?", syns[0], syns[1:] + [non], pool)


def _cat_antonyms(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    pairs = [(r["a"], r["b"]) for r in data.get("antonyms", [])]
    all_b = list(dict.fromkeys(b for _, b in pairs))
    all_a = list(dict.fromkeys(a for a, _ in pairs))
    for a, b in pairs:
        pool = [b] + _pool(all_b, b)[:5]
        _emit(out, existing, rng, f"'{a}' — വിപരീതം?", b, _pool(pool, b)[:3], pool)
        pool2 = [a] + _pool(all_a, a)[:5]
        _emit(out, existing, rng, f"'{b}' — വിപരീതം?", a, _pool(pool2, a)[:3], pool2)
        _emit(out, existing, rng, f"'{a}'-ന്റെ വിപരീത പദം?", b, _pool(pool, b)[:3], pool)


def _cat_author_works(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    rows = [(r["author"], r["work"]) for r in data.get("author_works", [])]
    authors = list(dict.fromkeys(a for a, _ in rows))
    works = list(dict.fromkeys(w for _, w in rows if not re.fullmatch(r"[A-Za-z .,'\-]+", w)))
    ml_works = [w for w in works if re.search(r"[\u0D00-\u0D7F]", w)]
    for author, work in rows:
        if re.search(r"[\u0D00-\u0D7F]", work):
            _emit(out, existing, rng, f"{author}യുടെ പ്രസിദ്ധ കൃതി ഏത്?", work, _pool(ml_works, work)[:3], ml_works)
            _emit(out, existing, rng, f"{author} രചിച്ച പ്രസിദ്ധ കൃതി ഏത്?", work, _pool(ml_works, work)[:3], ml_works)
            _emit(out, existing, rng, f"{author} — പ്രധാന കൃതി?", work, _pool(ml_works, work)[:3], ml_works)
            _emit(out, existing, rng, f"{author} എഴുതിയ പ്രധാന ഗ്രന്ഥം?", work, _pool(ml_works, work)[:3], ml_works)
        _emit(out, existing, rng, f"'{work}' എന്ന കൃതി രചിച്ചത് ആര്?", author, _pool(authors, author)[:3], authors)
        _emit(
            out,
            existing,
            rng,
            f"'{work}' ഏത് രചയിതാവിന്റെ കൃതിയാണ്?",
            author,
            _pool(authors, author)[:3],
            authors,
        )


def _cat_grammar(out: list[Candidate], existing: set[str], rng: random.Random) -> None:
    try:
        from malayalam_facts import FACTS
    except ImportError:
        return
    answers = list(dict.fromkeys(a for _, a, _, _ in FACTS if re.search(r"[\u0D00-\u0D7F]", a)))
    for q, ans, wrong, diff in FACTS:
        if not re.search(r"[\u0D00-\u0D7F]", q):
            continue
        if re.search(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]", q + ans):
            continue
        clean_wrong = [w for w in wrong if re.search(r"[\u0D00-\u0D7F]", w)][:3]
        if len(clean_wrong) < 3:
            continue
        _emit(out, existing, rng, q, ans, clean_wrong, answers, diff)
        m = re.search(r"മലയാള വ്യാകരണത്തിൽ (.+?) എന്നത് എന്താണ്\?", q)
        if m:
            term = m.group(1)
            _emit(out, existing, rng, f"'{term}' — അർത്ഥം?", ans, clean_wrong, answers, diff)
            _emit(out, existing, rng, f"'{term}' എന്താണ്?", ans, clean_wrong, answers, diff)
        m2 = re.search(r"'([^']+)' എന്ന വാക്കിന്റെ അർത്ഥം ഏതാണ്\?", q)
        if m2:
            word = m2.group(1)
            _emit(out, existing, rng, f"'{word}' — അർത്ഥം?", ans, clean_wrong, answers, diff)


def _cat_sandhi(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    rows = data.get("sandhi", [])
    combined = [r["combined"] for r in rows]
    stem_pool = [" + ".join(r["parts"]) for r in rows]
    for row in rows:
        parts, ans = row["parts"], row["combined"]
        stem_parts = " + ".join(parts)
        _emit(out, existing, rng, f"'{stem_parts}' — ശരിയായ സന്ധി?", ans, _pool(combined, ans)[:3], combined)
        _emit(
            out,
            existing,
            rng,
            f"'{ans}' — ഏത് പദങ്ങളുടെ സന്ധി?",
            stem_parts,
            _pool(stem_pool, stem_parts)[:3],
            stem_pool,
        )


def _cat_samasam(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    types_ = list(dict.fromkeys(r["type"] for r in data.get("samasam", [])))
    compounds = list(dict.fromkeys(r["compound"] for r in data.get("samasam", [])))
    for row in data.get("samasam", []):
        compound, typ = row["compound"], row["type"]
        _emit(out, existing, rng, f"'{compound}' — സമാസം?", typ, _pool(types_, typ)[:3], types_)
        _emit(out, existing, rng, f"'{typ}' — ഉദാഹരണം?", compound, _pool(compounds, compound)[:3], compounds)


def _cat_padashuddhi(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    correct = list(dict.fromkeys(r["correct"] for r in data.get("padashuddhi", [])))
    for row in data.get("padashuddhi", []):
        right = row["correct"]
        hint = row.get("hint", right)
        stem = f"'{hint}' — ശരിയായ പദം?"
        wrong_opts = _pool(correct + [row["wrong"]], right)[:3]
        _emit(out, existing, rng, stem, right, wrong_opts, correct)


def _cat_literary_history(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    answers = list(dict.fromkeys(r["answer"] for r in data.get("literary_history", [])))
    for row in data.get("literary_history", []):
        q, ans = row["question"], row["answer"]
        _emit(out, existing, rng, q, ans, _pool(answers, ans)[:3], answers)


def _cat_idioms(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    meanings = list(dict.fromkeys(r["meaning"] for r in data.get("idioms", [])))
    for row in data.get("idioms", []):
        phrase, meaning = row["phrase"], row["meaning"]
        _emit(out, existing, rng, f"'{phrase}' — അർത്ഥം?", meaning, _pool(meanings, meaning)[:3], meanings)
        _emit(out, existing, rng, f"'{meaning}' — ഏത് പ്രയോഗത്തിന്റെ അർത്ഥം?", phrase, _pool([r["phrase"] for r in data["idioms"]], phrase)[:3], [r["phrase"] for r in data["idioms"]])
        _emit(out, existing, rng, f"പ്രയോഗം '{phrase}' — അർത്ഥം?", meaning, _pool(meanings, meaning)[:3], meanings)


def _cat_proverbs(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    meanings = list(dict.fromkeys(r["meaning"] for r in data.get("proverbs", [])))
    for row in data.get("proverbs", []):
        prov, meaning = row["proverb"], row["meaning"]
        _emit(out, existing, rng, f"'{prov}' — അർത്ഥം?", meaning, _pool(meanings, meaning)[:3], meanings)
        _emit(out, existing, rng, f"പഴഞ്ചൊല്ല് '{prov}' — അർത്ഥം?", meaning, _pool(meanings, meaning)[:3], meanings)


def _cat_one_word(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    words = list(dict.fromkeys(r["word"] for r in data.get("one_word", [])))
    for row in data.get("one_word", []):
        definition, word = row["definition"], row["word"]
        _emit(out, existing, rng, f"{definition}?", word, _pool(words, word)[:3], words)
        _emit(out, existing, rng, f"ഒറ്റപദം: {definition}?", word, _pool(words, word)[:3], words)


def _cat_compounds(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    compounds = list(dict.fromkeys(r["compound"] for r in data.get("compounds", [])))
    for row in data.get("compounds", []):
        compound, meaning = row["compound"], row["meaning"]
        _emit(out, existing, rng, f"'{compound}' — അർത്ഥം?", meaning, _pool([r["meaning"] for r in data["compounds"]], meaning)[:3], [r["meaning"] for r in data["compounds"]])
        _emit(out, existing, rng, f"'{meaning}' — ഏത് ഘടകപദം?", compound, _pool(compounds, compound)[:3], compounds)


def _cat_splits(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    for row in data.get("splits", []):
        word, parts = row["word"], row["parts"]
        ans = " + ".join(parts)
        wrong = [r["word"] for r in data["splits"] if r["word"] != word][:3]
        pool = [r["word"] for r in data["splits"]]
        _emit(out, existing, rng, f"'{word}' — ഘടകങ്ങളായി പിരിച്ചെഴുതുക?", ans, wrong, pool + parts)
        _emit(out, existing, rng, f"'{word}' — ഏത് പദത്തിന്റെ ചേർത്തെഴുത്താണ്?", ans, wrong, pool)


def _cat_gender_vacana(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    attrs = list(dict.fromkeys(r["attr"] for r in data.get("gender_vacana", [])))
    for row in data.get("gender_vacana", []):
        word, attr = row["word"], row["attr"]
        _emit(out, existing, rng, f"'{word}' — ലിംഗം/വചനം?", attr, _pool(attrs, attr)[:3], attrs)


def _cat_vibhakti(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    vibhaktis = list(dict.fromkeys(r["vibhakti"] for r in data.get("vibhakti", [])))
    for row in data.get("vibhakti", []):
        example, vib = row["example"], row["vibhakti"]
        _emit(out, existing, rng, f"'{example}' — വിഭക്തി?", vib, _pool(vibhaktis, vib)[:3], vibhaktis)


def _cat_translations(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    malayalam = list(dict.fromkeys(r["malayalam"] for r in data.get("translations", [])))
    for row in data.get("translations", []):
        eng, ml = row["english"], row["malayalam"]
        _emit(out, existing, rng, f"ഇംഗ്ലീഷ് വാക്യം: '{eng}' — മലയാള പരിഭാഷ?", ml, _pool(malayalam, ml)[:3], malayalam)
        _emit(out, existing, rng, f"'{eng}' — മലയാള പരിഭാഷ?", ml, _pool(malayalam, ml)[:3], malayalam)


def _cat_alankaram(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    types_ = list(dict.fromkeys(r["type"] for r in data.get("alankaram", [])))
    for row in data.get("alankaram", []):
        example, typ = row["example"], row["type"]
        _emit(out, existing, rng, f"'{example}' — അലങ്കാരം?", typ, _pool(types_, typ)[:3], types_)
        _emit(out, existing, rng, f"അലങ്കാരം — '{example}'?", typ, _pool(types_, typ)[:3], types_)


def _cat_vritha(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    vrithas = list(dict.fromkeys(r["vritha"] for r in data.get("vritha", [])))
    for row in data.get("vritha", []):
        work, vr = row["work"], row["vritha"]
        _emit(out, existing, rng, f"'{work}' — വൃത്തം?", vr, _pool(vrithas, vr)[:3], vrithas)
        _emit(out, existing, rng, f"'{work}' — ചന്ദസ്സ്?", vr, _pool(vrithas, vr)[:3], vrithas)


def _cat_movements(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    for row in data.get("movements", []):
        movement, detail = row["movement"], row["detail"]
        pool = [r["detail"] for r in data["movements"]]
        _emit(out, existing, rng, f"'{movement}' — പ്രധാന വിവരം?", detail, _pool(pool, detail)[:3], pool)


def _cat_pen_names(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    real_names = list(dict.fromkeys(r["real"] for r in data.get("pen_names", [])))
    pen_names = list(dict.fromkeys(r["pen"] for r in data.get("pen_names", [])))
    for row in data.get("pen_names", []):
        pen, real = row["pen"], row["real"]
        _emit(out, existing, rng, f"'{pen}' — തൂലികാനാമം?", real, _pool(real_names, real)[:3], real_names)
        _emit(out, existing, rng, f"'{real}' — തൂലികാനാമം?", pen, _pool(pen_names, pen)[:3], pen_names)


def _cat_characters(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    works = list(dict.fromkeys(r["work"] for r in data.get("characters", [])))
    for row in data.get("characters", []):
        char, work = row["character"], row["work"]
        _emit(out, existing, rng, f"'{char}' — ഏത് കൃതിയിലെ കഥാപാത്രം?", work, _pool(works, work)[:3], works)


def _cat_quotes(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    authors = list(dict.fromkeys(r["author"] for r in data.get("quotes", [])))
    for row in data.get("quotes", []):
        quote, author = row["quote"], row["author"]
        _emit(out, existing, rng, f"'{quote}' — ആരുടെ വരി?", author, _pool(authors, author)[:3], authors)


def _cat_ancient(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    for row in data.get("ancient_works", []):
        work, detail = row["work"], row["detail"]
        pool = [r["detail"] for r in data["ancient_works"]]
        _emit(out, existing, rng, f"'{work}' — പ്രധാന വിവരം?", detail, _pool(pool, detail)[:3], pool)


def _cat_folk(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    for row in data.get("folk", []):
        qtext, ans = row["question"], row["answer"]
        pool = [r["answer"] for r in data["folk"]]
        _emit(out, existing, rng, qtext, ans, _pool(pool, ans)[:3], pool)


def _cat_chandass(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    for row in data.get("chandass", []):
        example, ans = row["example"], row["answer"]
        pool = [r["answer"] for r in data["chandass"]]
        _emit(out, existing, rng, f"'{example}' — ചന്ദസ്സ്?", ans, _pool(pool, ans)[:3], pool)


def _cat_mappila(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    for row in data.get("mappila", []):
        qtext, ans = row["question"], row["answer"]
        pool = [r["answer"] for r in data["mappila"]]
        _emit(out, existing, rng, qtext, ans, _pool(pool, ans)[:3], pool)


def _cat_journalism(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    for row in data.get("journalism", []):
        qtext, ans = row["question"], row["answer"]
        pool = [r["answer"] for r in data["journalism"]]
        _emit(out, existing, rng, qtext, ans, _pool(pool, ans)[:3], pool)


def _cat_language_facts(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    rows = data.get("language_facts", [])
    if not rows:
        return
    answers = list(dict.fromkeys(r["answer"] for r in rows))
    for row in rows:
        qtext, ans = row["question"], row["answer"]
        pool = row.get("pool") or answers
        _emit(out, existing, rng, qtext, ans, _pool(pool, ans)[:3], pool)


def _cat_misc(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    for row in data.get("misc", []):
        qtext, ans = row["question"], row["answer"]
        pool = row.get("pool") or [r["answer"] for r in data["misc"]]
        _emit(out, existing, rng, qtext, ans, _pool(pool, ans)[:3], pool)


def _emit_all(out: list[Candidate], existing: set[str], rng: random.Random, data: dict) -> None:
    _cat_synonyms(out, existing, rng, data)
    _cat_antonyms(out, existing, rng, data)
    _cat_idioms(out, existing, rng, data)
    _cat_proverbs(out, existing, rng, data)
    _cat_one_word(out, existing, rng, data)
    _cat_compounds(out, existing, rng, data)
    _cat_splits(out, existing, rng, data)
    _cat_gender_vacana(out, existing, rng, data)
    _cat_vibhakti(out, existing, rng, data)
    _cat_translations(out, existing, rng, data)
    _cat_alankaram(out, existing, rng, data)
    _cat_vritha(out, existing, rng, data)
    _cat_movements(out, existing, rng, data)
    _cat_pen_names(out, existing, rng, data)
    _cat_characters(out, existing, rng, data)
    _cat_quotes(out, existing, rng, data)
    _cat_ancient(out, existing, rng, data)
    _cat_folk(out, existing, rng, data)
    _cat_mappila(out, existing, rng, data)
    _cat_sandhi(out, existing, rng, data)
    _cat_samasam(out, existing, rng, data)
    _cat_padashuddhi(out, existing, rng, data)
    _cat_literary_history(out, existing, rng, data)
    _cat_chandass(out, existing, rng, data)
    _cat_journalism(out, existing, rng, data)
    _cat_language_facts(out, existing, rng, data)
    _cat_misc(out, existing, rng, data)
    _cat_author_works(out, existing, rng, data)
    _cat_grammar(out, existing, rng)


def generate_wave20_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    data = _load()
    out: list[Candidate] = []
    _emit_all(out, existing, rng, data)
    return interleave_candidates(out, rng)


if __name__ == "__main__":
    c = generate_wave20_candidates(set(), random.Random(42))
    stems = {q for q, _, _, _ in c}
    print(len(c), "candidates,", len(stems), "unique stems")
