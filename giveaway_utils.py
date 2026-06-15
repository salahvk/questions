#!/usr/bin/env python3
"""Detect and rewrite MCQ stems where the quoted text equals the answer (giveaway)."""

from __future__ import annotations

import re

# Answer appears inside single quotes in the question stem.
QUOTED_ANSWER = re.compile(r"'([^']+)'")

GIVEAWAY_STEM_PATTERNS = [
    re.compile(r"^.+ സംസ്ഥാന(?:ത്തില(?:െ))? '[^']+' ദേശീയോദ്യാനം ഏതാണ്\?$"),
    re.compile(r"^.+ നദിയ(?:ile|ിൽ) '[^']+' അണക്കെട്ട് ഏതാണ്\?$"),
    re.compile(r"^.+ പർവതനിരയ(?:ile|ിൽ) '[^']+' ശിഖരം ഏതാണ്\?$"),
    re.compile(r"^'[^']+' തലസ്ഥാനമുള്ള '[^']+'-ന്റെ തലസ്ഥാനം\?$"),
    re.compile(r"^'[^']+' ഭൂഖണ്ഡത്തിലെ '[^']+'\?$"),
    re.compile(r"^ദൈർഘ്യം .+ ആയ പ്രധാന നദി '[^']+'\?$"),
    re.compile(r"^വിസ്തീർണ്ണം .+ sq .+ ആയ ഇന്ത്യൻ സംസ്ഥാനം '[^']+'\?$"),
    re.compile(r"^ജനസംഖ്യ .+ ആയ ഇന്ത്യൻ സംസ്ഥാനം '[^']+'\?$"),
]


def quoted_segments(stem: str) -> list[str]:
    return [m.group(1).strip() for m in QUOTED_ANSWER.finditer(stem)]


def is_answer_in_stem_giveaway(stem: str, answer: str) -> bool:
    """True when the correct answer text appears inside quotes in the question stem."""
    ans = answer.strip()
    if not ans:
        return False
    if ans in quoted_segments(stem):
        return True
    # Unquoted giveaway: entity named in stem, answer is that entity
    if re.search(rf"^.+ പർവതനിരയ(?:ile|ിൽ) {re.escape(ans)} ശിഖരം ഏതാണ്\?$", stem.strip()):
        return True
    if re.match(rf"^'{re.escape(ans)}' ഏത് സംസ്ഥാനത്താണ്\?$", stem.strip()):
        return True
    return False


def is_banned_giveaway_stem(stem: str) -> bool:
    return any(p.match(stem.strip()) for p in GIVEAWAY_STEM_PATTERNS)


def rewrite_giveaway_question(stem: str, answer: str) -> tuple[str, str] | None:
    """Return (new_stem, new_answer) or None if no rewrite applies."""
    s = stem.strip()
    ans = answer.strip()

    m = re.match(r"^(.+?) സംസ്ഥാന(?:ത്തില(?:െ))? '([^']+)' ദേശീയോദ്യാനം ഏതാണ്\?$", s)
    if m and ans == m.group(2).strip():
        park = m.group(2)
        state = m.group(1).replace("കerala", "കേരള").replace("കeralaം", "കേരളം")
        return f"'{park}' ദേശീയോദ്യാനം ഏത് സംസ്ഥാനത്താണ്?", state

    m = re.match(r"^(.+?) നദിയ(?:ile|ിൽ) '([^']+)' അണക്കെട്ട് ഏതാണ്\?$", s)
    if m and ans == m.group(2).strip():
        river, dam = m.group(1), m.group(2)
        return f"'{dam}' അണക്കെട്ട് ഏത് നദിയിൽ സ്ഥിതി ചെയ്യുന്നു?", river

    m = re.match(r"^(.+?) പർവതനിരയ(?:ile|ിൽ) '([^']+)' ശിഖരം ഏതാണ്\?$", s)
    if m and ans == m.group(2).strip():
        rng_name, peak = m.group(1), m.group(2)
        return f"'{peak}' ശിഖരം ഏത് പർവതനിരയിൽ സ്ഥിതി ചെയ്യുന്നു?", rng_name

    m = re.match(r"^(.+?) പർവതനിരയ(?:ile|ിൽ) ([^'?]+?) ശിഖരം ഏതാണ്\?$", s)
    if m and ans == m.group(2).strip():
        rng_name, peak = m.group(1), m.group(2).strip()
        return f"'{peak}' ശിഖരം ഏത് പർവതനിരയിൽ സ്ഥിതി ചെയ്യുന്നു?", rng_name

    m = re.match(rf"^'{re.escape(ans)}' ഏത് സംസ്ഥാനത്താണ്\?$", s)
    if m:
        return None  # nonsensical — remove in fix script

    m = re.match(r"^'([^']+)' തലസ്ഥാനമുള്ള '([^']+)'-ന്റെ തലസ്ഥാനം\?$", s)
    if m and ans == m.group(1).strip():
        capital, country = m.group(1), m.group(2)
        return f"'{country}' രാജ്യത്തിന്റെ തലസ്ഥാനം ഏതാണ്?", capital

    m = re.match(r"^'([^']+)' ഭൂഖണ്ഡത്തിലെ '([^']+)'\?$", s)
    if m and ans == m.group(2).strip():
        continent, country = m.group(1), m.group(2)
        return f"'{country}' ഏത് ഭൂഖണ്ഡത്തിലാണ്?", continent

    m = re.match(r"^ദൈർഘ്യം (.+?) ആയ പ്രധാന നദി '([^']+)'\?$", s)
    if m and ans == m.group(2).strip():
        length, river = m.group(1), m.group(2)
        return f"ദൈർഘ്യം {length} ആയ പ്രധാന നദി ഏത്?", river

    m = re.match(r"^വിസ്തീർണ്ണം (.+?) sq .+ ആയ ഇന്ത്യൻ സംസ്ഥാനം '([^']+)'\?$", s)
    if m and ans == m.group(2).strip():
        area, state = m.group(1), m.group(2)
        return f"വിസ്തീർണ്ണം {area} sq കി.മീ. ആയ ഇന്ത്യൻ സംസ്ഥാനം ഏത്?", state

    m = re.match(r"^ജനസംഖ്യ (.+?) ആയ ഇന്ത്യൻ സംസ്ഥാനം '([^']+)'\?$", s)
    if m and ans == m.group(2).strip():
        pop, state = m.group(1), m.group(2)
        return f"ജനസംഖ്യ {pop} ആയ ഇന്ത്യൻ സംസ്ഥാനം ഏത്?", state

    m = re.match(
        r"^കേരള(?:ം|ത്ത)?(?:ിലെ| സംസ്ഥാന(?:ത്തില(?:െ))?)? "
        r"'([^']+)' ജില്ല(?:യ)?(?:യ)?(?:ude|യുടെ) (?:പ്രശസ്തമായ )?'([^']+)' — ഏത്\?$",
        s,
    )
    if m and ans == m.group(2).strip():
        district, landmark = m.group(1), m.group(2)
        return f"കേരളത്തിലെ '{landmark}' ഏത് ജില്ലയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?", district

    m = re.match(
        r"^കേരള(?:ം|ത്ത)?(?:ിലെ| സംസ്ഥാന(?:ത്തില(?:െ))?)? "
        r"'([^']+)' ജില്ല(?:യ)?(?:യ)?(?:ude|യുടെ) (?:പ്രശസ്തമായ )?'([^']+)' — ശരിയോ\?$",
        s,
    )
    if m:
        return None  # yes/no — not handled here

    m = re.match(r"^'([^']+)' ജില്ല(?:യ)?(?:ude|യുടെ) ആസ്ഥാന(?:ം| നഗരം)\?$", s)
    if m and ans == m.group(1).strip():
        return None  # needs alternate fact — handled in fix script

    m = re.match(
        r"^കേരള(?:ം|ത്ത)?(?:ിലെ| സംസ്ഥാന(?:ത്തില(?:െ))?)? "
        r"'([^']+)' (?:ഏത് )?ജില്ല(?:യ)?(?:ude|യുടെ) ആസ്ഥാന(?:ം| നഗരം)?(?: ഏതാണ്)?\?$",
        s,
    )
    if m and ans == m.group(1).strip():
        return None  # same-name HQ — handled in fix script

    m = re.match(r"^കേരള(?:ം|ത്ത)?(?:ിലെ| സംസ്ഥാന(?:ത്തില(?:െ))?)? '([^']+)' ഏത് ജില്ല(?:യ)?(?:ude|യുടെ) ആസ്ഥാന(?:മ)?(?:ാണ്)?\?$", s)
    if m and ans == m.group(1).strip():
        return None  # same-name HQ reverse — handled in fix script

    # Generic: if only one quoted segment equals answer, try removing quotes from stem
    if is_answer_in_stem_giveaway(s, ans):
        segs = quoted_segments(s)
        if len(segs) == 1 and segs[0] == ans:
            new = s.replace(f"'{ans}'", ans, 1)
            if new != s and not is_answer_in_stem_giveaway(new, ans):
                return new, ans

    return None
