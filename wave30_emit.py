#!/usr/bin/env python3
"""Shared wave-30 fact emitters — verified pairs, typed distractor pools."""

from __future__ import annotations

import re
from typing import Callable

from refill_common import Candidate, add_candidate

MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def pool_without(items: list[str], correct: str) -> list[str]:
    return [x for x in items if x != correct]


def emit_pairs(
    out: list[Candidate],
    existing: set[str],
    rng,
    rows: list[tuple[str, str]],
    fwd_templates: list[str],
    rev_templates: list[str],
    pool_a: list[str],
    pool_b: list[str],
    diff: str = "medium",
    *,
    english: bool = False,
) -> None:
    """Emit forward + reverse questions from (entity_a, entity_b) fact pairs."""
    for a, b in rows:
        for tmpl in fwd_templates:
            q = tmpl.format(a=a, b=b)
            if not english and MIXED.search(q + b):
                continue
            add_candidate(out, existing, rng, q, b, pool_without(pool_b, b)[:3], diff, pool_b)
        for tmpl in rev_templates:
            q = tmpl.format(a=a, b=b)
            if not english and MIXED.search(q + a):
                continue
            add_candidate(out, existing, rng, q, a, pool_without(pool_a, a)[:3], diff, pool_a)


def emit_direct(
    out: list[Candidate],
    existing: set[str],
    rng,
    facts: list[tuple[str, str, list[str], str]],
    *,
    english: bool = False,
) -> None:
    """Emit pre-written (question, answer, wrong[], difficulty) tuples."""
    for q, ans, wrong, diff in facts:
        if not english and MIXED.search(q + ans + "".join(wrong)):
            continue
        pool = wrong + [ans]
        add_candidate(out, existing, rng, q, ans, pool_without(pool, ans)[:3], diff, pool)


def emit_category(
    out: list[Candidate],
    existing: set[str],
    rng,
    rows: list[tuple[str, str]],
    fwd: list[str],
    rev: list[str],
    pool_a: list[str],
    pool_b: list[str],
    diff: str = "medium",
    *,
    english: bool = False,
) -> None:
    emit_pairs(out, existing, rng, rows, fwd, rev, pool_a, pool_b, diff, english=english)


def count_by_prefix(stems: list[str], prefix: str) -> int:
    return sum(1 for s in stems if s.startswith(prefix))


def make_emitter(
    rows: list[tuple[str, str]],
    fwd: list[str],
    rev: list[str],
    pool_a: list[str],
    pool_b: list[str],
    diff: str = "medium",
    *,
    english: bool = False,
) -> Callable:
    def _emit(out, existing, rng):
        emit_category(out, existing, rng, rows, fwd, rev, pool_a, pool_b, diff, english=english)
    return _emit
