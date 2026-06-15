#!/usr/bin/env python3
"""Malayalam QC for malayalam.json question candidates."""

from __future__ import annotations

import re

from apply_malayalam_rules import (
    BANNED_OPTION_ENGLISH,
    MALAYALAM,
    strip_for_validation,
)
from giveaway_utils import is_answer_in_stem_giveaway
from refill_common import is_filler_text

PRESERVE = re.compile(
    r"\b(?:ODI|T20|IPL|ICC|FIFA|GST|ISRO|NASA|WHO|IMF|WTO|"
    r"INC|BJP|CPI|CPM|UDF|LDF|NDA|NFDC|DFF|UA|U|A)\b",
    re.I,
)

TRANSLATION_STEM = re.compile(r"പരിഭാഷ|ഇംഗ്ലീഷ്\s*വാക്യ", re.I)


def passes_malayalam_qc(question: str, options: list[str], answer: str) -> bool:
    if not question or not options or not answer:
        return False
    if is_filler_text(question):
        return False
    if is_answer_in_stem_giveaway(question, answer):
        return False
    if len(options) != 4 or len(set(options)) != 4 or answer not in options:
        return False
    if not MALAYALAM.search(question):
        return False

    allow_english_stem = bool(TRANSLATION_STEM.search(question))
    if not allow_english_stem and re.search(r"[a-zA-Z]{4,}", strip_for_validation(question)):
        return False

    has_ml = any(MALAYALAM.search(o) for o in options)
    for opt in options:
        if BANNED_OPTION_ENGLISH.search(opt):
            return False
        if (
            has_ml
            and not MALAYALAM.search(opt)
            and re.search(r"[a-zA-Z]{4,}", opt)
            and not re.fullmatch(r"[\d%./\s\-+()A-Za-z]+", opt)
        ):
            return False

    for text in [question, *options, answer]:
        cleaned = strip_for_validation(text)
        cleaned = PRESERVE.sub("", cleaned)
        if allow_english_stem and text == question:
            continue
        if re.search(r"[a-zA-Z]{4,}", cleaned) and MALAYALAM.search(text):
            return False
    return True
