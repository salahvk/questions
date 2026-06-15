#!/usr/bin/env python3
"""Unique mathematics problems — each tests distinct numeric/logic knowledge."""

from __future__ import annotations

import math
import random

from refill_common import add_candidate, Candidate


def _hcf(a: int, b: int) -> int:
    return math.gcd(a, b)


def _lcm(a: int, b: int) -> int:
    return a * b // math.gcd(a, b)


def generate_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []

    # Unique addition problems
    for a in range(12, 350):
        for b in range(5, 120, 5):
            ans = str(a + b)
            wrong = [str(a + b + k) for k in (1, 2, -1, 3, -2) if a + b + k > 0 and a + b + k != a + b]
            add_candidate(out, existing, rng, f"{a} + {b} എത്ര?", ans, wrong[:3], "easy")

    # Subtraction
    for a in range(50, 400, 7):
        for b in range(5, 60, 5):
            if b >= a:
                continue
            ans = str(a - b)
            wrong = [str(a - b + k) for k in (1, 2, 3) if a - b + k != a - b]
            add_candidate(out, existing, rng, f"{a} − {b} എത്ര?", ans, wrong[:3], "easy")

    # Unique multiplication
    for a in range(2, 55):
        for b in range(2, 35):
            ans = str(a * b)
            wrong = [str(a * b + k) for k in (1, 2, a, b) if a * b + k != a * b]
            add_candidate(out, existing, rng, f"{a} × {b} എത്ര?", ans, wrong[:3], "easy")

    # Division (exact)
    for b in range(2, 25):
        for q in range(2, 30):
            a = b * q
            ans = str(q)
            wrong = [str(q + k) for k in (1, 2, -1) if q + k > 0 and q + k != q]
            add_candidate(out, existing, rng, f"{a} ÷ {b} എത്ര?", ans, wrong[:3], "medium")

    # Squares
    for n in range(2, 80):
        ans = str(n * n)
        wrong = [str((n + k) ** 2) for k in (1, -1, 2) if (n + k) > 0]
        add_candidate(out, existing, rng,
            f"{n}² എത്ര?", ans, wrong[:3], "medium")

    # Cubes
    for n in range(2, 20):
        ans = str(n ** 3)
        wrong = [str((n + k) ** 3) for k in (1, -1, 2) if (n + k) > 0]
        add_candidate(out, existing, rng,
            f"{n}³ എത്ര?", ans, wrong[:3], "hard")

    # HCF
    for a in range(12, 120, 3):
        for b in range(8, 100, 5):
            if math.gcd(a, b) == 1:
                continue
            g = math.gcd(a, b)
            wrong = [str(g + k) for k in (1, 2, 3, 5) if g + k != g]
            add_candidate(out, existing, rng,
                f"{a} ഉം {b} ഉം തമ്മിലുള്ള ഏറ്റവും വലിയ പൊതുവിഭാജകം (HCF) ?", str(g), wrong[:3], "medium")

    # LCM
    for a in range(4, 60, 2):
        for b in range(6, 50, 3):
            l = _lcm(a, b)
            if l > 500:
                continue
            wrong = [str(l + k * 2) for k in (1, 2, 3) if l + k * 2 != l]
            add_candidate(out, existing, rng,
                f"{a} ഉം {b} ഉം തമ്മിലുള്ള ഏറ്റവും ചെറിയ പൊതുമൾഗുണിതം (LCM) ?", str(l), wrong[:3], "medium")

    # Percentages
    for pct in (5, 10, 12, 15, 20, 25, 30, 40, 50, 60, 75, 80):
        for base in (80, 100, 120, 150, 200, 250, 400, 500):
            ans = str(pct * base // 100)
            wrong = [str((pct + k) * base // 100) for k in (5, 10, -5) if (pct + k) * base // 100 != pct * base // 100]
            add_candidate(out, existing, rng,
                f"{base}-ന്റെ {pct}% എത്ര?", ans, wrong[:3], "medium")

    # Simple linear equations ax + b = c
    for a in range(2, 12):
        for x in range(2, 25):
            b = rng.randint(1, 20)
            c = a * x + b
            ans = str(x)
            wrong = [str(x + k) for k in (1, 2, -1, 3) if x + k > 0 and x + k != x]
            add_candidate(out, existing, rng,
                f"{a}x + {b} = {c} എന്ന സമീകരണത്തിൽ x-ന്റെ മൂല്യം?", ans, wrong[:3], "medium")

    # Triangle angle sums with one angle given
    for a1 in range(20, 80, 5):
        for a2 in range(20, 80, 5):
            a3 = 180 - a1 - a2
            if a3 <= 0 or a3 >= 170:
                continue
            ans = f"{a3}°"
            wrong = [f"{a3 + k}°" for k in (10, 20, -10) if 0 < a3 + k < 180]
            add_candidate(out, existing, rng,
                f"ഒരു ത്രികോണത്തിന്റെ രണ്ട് കോണങ്ങൾ {a1}° ഉം {a2}° ഉം ആണെങ്കിൽ മൂന്നാമത്തെ കോൺ?", ans, wrong[:3], "medium")

    # Perimeter of rectangle
    for l in range(5, 40, 3):
        for w in range(3, 25, 2):
            ans = str(2 * (l + w))
            wrong = [str(2 * (l + w) + k) for k in (2, 4, l)]
            add_candidate(out, existing, rng,
                f"ദൈർഘ്യം {l} സെ.മീ., വീതി {w} സെ.മീ. ഉള്ള ചതുരത്തിന്റെ ചുറ്റളവ്?", ans, wrong[:3], "easy")

    # Area of rectangle
    for l in range(4, 35, 2):
        for w in range(3, 20, 2):
            ans = str(l * w)
            wrong = [str(l * w + k) for k in (l, w, 2)]
            add_candidate(out, existing, rng,
                f"ദൈർഘ്യം {l} സെ.മീ., വീതി {w} സെ.മീ. ഉള്ള ചതുരത്തിന്റെ വിസ്തീർണ്ണം?", ans, wrong[:3], "easy")

    # Circle area (πr² approx with π=22/7)
    for r in range(2, 22):
        area = round(22 * r * r / 7)
        ans = f"{area} ച.സെ.മീ."
        wrong = [f"{area + k * r} ച.സെ.മീ." for k in (1, 2, 3)]
        add_candidate(out, existing, rng,
            f"ആരം {r} സെ.മീ. ഉള്ള വൃത്തത്തിന്റെ വിസ്തീർണ്ണം (π = 22/7)?", ans, wrong[:3], "hard")

    # Prime check
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    composites = [n for n in range(4, 100) if n not in primes]
    for p in primes:
        add_candidate(out, existing, rng,
            f"{p} ഒരു അഭാജ്യസംഖ്യയാണോ?", "അതെ", ["അല്ല", "നിർണ്ണയിക്ക 불가", "ഒന്നുമില്ല"], "easy")
    for c in composites[:60]:
        add_candidate(out, existing, rng,
            f"{c} ഒരു അഭാജ്യസംഖ്യയാണോ?", "അല്ല", ["അതെ", "നിർണ്ണയിക്ക 불가", "ഒന്നുമില്ല"], "easy")

    return out
