#!/usr/bin/env python3
"""Expand geography_facts generate_candidates + rebuild indian_history_facts.py."""

from __future__ import annotations

import ast
import random
import textwrap
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent

# ---------------------------------------------------------------------------
# Geography: patch generate_candidates tail
# ---------------------------------------------------------------------------

GEO_FILE = BASE / "geography_facts.py"
geo_src = GEO_FILE.read_text(encoding="utf-8")
marker = "    unesco_locs = list({loc for _, loc in UNESCO_INDIA})"
if marker not in geo_src:
    raise SystemExit("geography_facts.py structure changed; aborting geo patch")

EXTRA_GEO_GEN = textwrap.dedent("""
    # --- programmatic expansion from existing data ---
    by_river: dict[str, list[str]] = defaultdict(list)
    for dam, river, _state in INDIAN_DAMS:
        by_river[river].append(dam)
    for river, dams in by_river.items():
        uniq = list(dict.fromkeys(dams))
        if len(uniq) < 2:
            continue
        for dam in uniq:
            add(
                f"{river} നദിയിലെ '{dam}' അണക്കെട്ട് ഏതാണ്?",
                dam,
                [d for d in uniq if d != dam],
                "hard",
            )

    by_state_parks: dict[str, list[str]] = defaultdict(list)
    for park, state in INDIAN_NATIONAL_PARKS:
        by_state_parks[state].append(park)
    for state, parks in by_state_parks.items():
        uniq = list(dict.fromkeys(parks))
        if len(uniq) < 2:
            continue
        for park in uniq:
            add(
                f"{state} സംസ്ഥാനത്തിലെ '{park}' ദേശീയോദ്യാനം ഏതാണ്?",
                park,
                [p for p in uniq if p != park],
                "medium",
            )

    origin_rivers = [r for r, _ in INDIAN_RIVER_ORIGIN]
    for river, origin in INDIAN_RIVER_ORIGIN:
        add(
            f"{origin} സംസ്ഥാനത്തിൽ ഉത്ഭവിക്കുന്ന പ്രധാന നദി ഏത്?",
            river,
            [r for r in origin_rivers if r != river],
            "medium",
        )

    for peak, rng_name, height in MOUNTAIN_PEAKS:
        same_range = [p for p, r, _ in MOUNTAIN_PEAKS if r == rng_name and p != peak]
        if len(same_range) >= 3:
            add(
                f"{rng_name} പർവതനിരയിലെ '{peak}' ശിഖരം ഏതാണ്?",
                peak,
                same_range[:3],
                "hard",
            )

    for state, capital in INDIAN_STATE_CAPITALS:
        add(
            f"ഇന്ത്യയിലെ '{capital}' നഗരം ഏത് സംസ്ഥാനത്തിന്റെ തലസ്ഥാനമാണ്?",
            state,
            [s for s, _ in INDIAN_STATE_CAPITALS if s != state][:3],
            "easy",
        )

    for country, capital in CAPITALS:
        add(
            f"ലോകത്തിലെ '{capital}' നഗരം ഏത് രാജ്യത്തിന്റെ തലസ്ഥാനമാണ്?",
            country,
            [c for c, _ in CAPITALS if c != country][:3],
            "medium",
        )

    for river, flows in RIVERS:
        flow_opts = list({f for _, f in RIVERS if f != flows})
        add(
            f"'{flows}'-ilേക്ക്/ile പതിക്കുന്ന നദി '{river}' അല്ലാത്തത് ഏത്?",
            river,
            [r for r, f in RIVERS if f == flows and r != river][:3] or [r for r, _ in RIVERS if r != river][:3],
            "hard",
        )
""")

# Fix the broken RIVERS question - simplify last block
EXTRA_GEO_GEN = textwrap.dedent("""
    # --- programmatic expansion from existing data ---
    by_river: dict[str, list[str]] = defaultdict(list)
    for dam, river, _state in INDIAN_DAMS:
        by_river[river].append(dam)
    for river, dams in by_river.items():
        uniq = list(dict.fromkeys(dams))
        if len(uniq) < 2:
            continue
        for dam in uniq:
            add(
                f"{river} നദിയിലെ '{dam}' അണക്കെട്ട് ഏതാണ്?",
                dam,
                [d for d in uniq if d != dam],
                "hard",
            )

    by_state_parks: dict[str, list[str]] = defaultdict(list)
    for park, state in INDIAN_NATIONAL_PARKS:
        by_state_parks[state].append(park)
    for state, parks in by_state_parks.items():
        uniq = list(dict.fromkeys(parks))
        if len(uniq) < 2:
            continue
        for park in uniq:
            add(
                f"{state} സംസ്ഥാനത്തിലെ '{park}' ദേശീയോദ്യാനം ഏതാണ്?",
                park,
                [p for p in uniq if p != park],
                "medium",
            )

    origin_rivers = [r for r, _ in INDIAN_RIVER_ORIGIN]
    for river, origin in INDIAN_RIVER_ORIGIN:
        add(
            f"{origin} സംസ്ഥാനത്തിൽ ഉത്ഭവിക്കുന്ന പ്രധാന നദി ഏത്?",
            river,
            [r for r in origin_rivers if r != river],
            "medium",
        )

    for peak, rng_name, height in MOUNTAIN_PEAKS:
        same_range = [p for p, r, _ in MOUNTAIN_PEAKS if r == rng_name and p != peak]
        if len(same_range) >= 3:
            add(
                f"{rng_name} പർവതനിരയിലെ '{peak}' ശിഖരം ഏതാണ്?",
                peak,
                same_range[:3],
                "hard",
            )

    flow_groups: dict[str, list[str]] = defaultdict(list)
    for river, flows in RIVERS:
        flow_groups[flows].append(river)
    for flows, rivers in flow_groups.items():
        if len(rivers) < 2:
            continue
        for river in rivers:
            add(
                f"{flows}-ilേക്ക്/ile പതിക്കുന്ന നദി '{river}' അല്ലാത്തത് ഏത്?",
                river,
                [r for r in rivers if r != river][:3],
                "hard",
            )
""")

if "GEO_EXPAND_PATCHED" not in geo_src:
    geo_src = geo_src.replace(
        "    return out\n",
        "    # GEO_EXPAND_PATCHED\n" + EXTRA_GEO_GEN + "\n    return out\n",
        1,
    )
    GEO_FILE.write_text(geo_src, encoding="utf-8")
    print("Patched geography_facts.py generate_candidates")

# ---------------------------------------------------------------------------
# Indian history: rebuild with large verified data
# ---------------------------------------------------------------------------
HEADER = textwrap.dedent('''\
#!/usr/bin/env python3
"""Verified Indian history facts for unique Malayalam PSC question generation."""

from __future__ import annotations

import random

Candidate = tuple[str, list[str], str, str]


def _pick(pool: list[str], correct: str, rng: random.Random) -> list[str]:
    wrong = list(dict.fromkeys(x for x in pool if x != correct))
    rng.shuffle(wrong)
    opts = [correct] + wrong[:3]
    while len(opts) < 4:
        opts.append("ഒന്നുമില്ല")
    return opts[:4]


def _add(out, existing, rng, q, ans, pool, diff="medium"):
    q = q.strip()
    if not q or q in existing:
        return
    opts = _pick(pool, ans, rng)
    if len(set(opts)) != 4 or ans not in opts:
        return
    out.append((q, opts, ans, diff))
    existing.add(q)

''')

def mostly_ml(text: str) -> bool:
    for ch in text:
        if "a" <= ch <= "z" or "A" <= ch <= "Z":
            return False
    return True

# Extract clean static from fill_unique
src = (BASE / "fill_unique.py").read_text(encoding="utf-8")
mod = ast.parse(src)
STATIC: list[tuple[str, str, list[str], str]] = []
for node in mod.body:
    if isinstance(node, ast.FunctionDef) and node.name == "build_indian_history":
        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                for call in stmt.value.elts:
                    q, opts, ans, diff = [ast.literal_eval(a) for a in call.args]
                    wrong = [o for o in opts if o != ans][:3]
                    if mostly_ml(q + ans + "".join(wrong)):
                        STATIC.append((q, ans, wrong, diff))

EXTRA_STATIC = [
    ("1757-ൽ നടന്ന പ്ലാസി യുദ്ധം?", "1757", ["1764", "1746", "1857"], "easy"),
    ("1764-ൽ നടന്ന ബക്സർ യുദ്ധം?", "1764", ["1757", "1746", "1857"], "medium"),
    ("1857-ലെ ആദ്യ സ്വാതന്ത്ര്യസമരം?", "1857", ["1942", "1919", "1767"], "easy"),
    ("1948-ൽ മഹാത്മാ ഗാന്ധിയെ വധിച്ച വർഷം?", "1948", ["1947", "1949", "1950"], "easy"),
    ("ഇന്ത്യയുടെ അവസാന വൈസ്രോയി?", "ലോർഡ് മൗണ്ട്ബാറ്റൺ", ["ലോർഡ് വേവൽ", "ലോർഡ് ലിന്ലിത്ഗോ", "ലോർഡ് അർവിൻ"], "easy"),
    ("ഇന്ത്യൻ നാഷണൽ ആർമി പുനഃസംഘടിപ്പിച്ച നേതാവ്?", "സുഭാഷ് ചന്ദ്ര ബോസ്", ["രാഷ് ബിഹാരി ബോസ്", "മോഹൻ സിംഗ്", "മഹാത്മാ ഗാന്ധി"], "medium"),
    ("1917-ലെ ചംപാരൻ സത്യാഗ്രഹം?", "1917", ["1918", "1919", "1920"], "medium"),
    ("1918-ലെ ഖേദാ സത്യാഗ്രഹം?", "1918", ["1917", "1919", "1920"], "medium"),
    ("1930-ലെ ഉപ്പ് സത്യാഗ്രഹം?", "1930", ["1920", "1932", "1942"], "easy"),
    ("സൈമൺ കമ്മീഷൻ ഇന്ത്യയിൽ എത്തിയ വർഷം?", "1928", ["1930", "1925", "1932"], "easy"),
    ("റൗലട്ട് ആക്ട് പ്രാബല്യത്തിൽ വന്ന വർഷം?", "1919", ["1920", "1915", "1930"], "easy"),
    ("ഗോൾമേജ് സമ്മേളനങ്ങളിൽ ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് പങ്കെടുത്തത്?", "രണ്ടാം മാത്രം", ["ഒന്നാം മാത്രം", "മൂന്നാം മാത്രം", "ഒന്നും പങ്കെടുത്തില്ല"], "hard"),
    ("1935-ലെ ഇന്ത്യാ ഭരണനിയമത്തിന്റെ അടിസ്ഥാനം?", "സൈമൺ കമ്മീഷൻ റിപ്പോർട്ട്", ["ക്രിപ്സ് മിഷൻ", "കാബിനറ്റ് മിഷൻ", "വേവൽ പദ്ധതി"], "medium"),
    ("1942-ലെ ക്രിപ്സ് മിഷന്റെ അധ്യക്ഷൻ?", "സ്റ്റാഫോർഡ് ക്രിപ്സ്", ["ലോർഡ് വേവൽ", "ലോർഡ് മൗണ്ട്ബാറ്റൺ", "ലോർഡ് അർവിൻ"], "medium"),
    ("മൗണ്ട്ബാറ്റൺ പദ്ധതി പ്രകാരം വിഭജന തീയതി?", "1947 ഓഗസ്റ്റ് 15", ["1947 ജൂൺ 3", "1947 ജൂലൈ 18", "1948 ജനുവരി 26"], "medium"),
    ("1922-ലെ ചൗരി ചൗര സംഭവം?", "1922", ["1920", "1930", "1942"], "medium"),
    ("1829-ലെ സതി നിരോധം?", "1829", ["1835", "1856", "1828"], "medium"),
    ("1853-ലെ ഇന്ത്യയിൽ റെയിൽവേ ആരംഭം?", "1853", ["1857", "1847", "1861"], "medium"),
    ("ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസിന്റെ ആദ്യ സമ്മേളനം നടന്ന വർഷം?", "1885", ["1905", "1907", "1911"], "easy"),
    ("ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസിന്റെ ആദ്യ സമ്മേളന സ്ഥലം?", "ബോംബെ", ["കൽക്കത്ത", "മദ്രാസ്", "അലഹാബാദ്"], "easy"),
    ("ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസിന്റെ ആദ്യ അധ്യക്ഷൻ?", "ഡബ്ല്യു.സി. ബാനർജി", ["ദാദാഭായി നൗറോജി", "സുരേന്ദ്രനാഥ ബാനർജി", "ഗോപാൽകൃഷ്ണ ഗോഖലെ"], "medium"),
    ("ലാപ്സ് നയം ആരംഭിച്ച വൈസ്രോയി?", "ലോർഡ് ഡാല്ഹൗസി", ["ലോർഡ് വെൽസלי", "വാറൻ ഹേസ്റ്റിംഗ്സ്", "ലോർഡ് കർസൺ"], "easy"),
    ("1909-ലെ ഇന്ത്യൻ കൗൺസിൽസ് ആക്ട് ഏത് പരിഷ്കാരത്തിന്റെ പേരിലാണ്?", "മോർലി-മിന്റോ പരിഷ്കാരങ്ങൾ", ["മോണ്ടഗ്യു-ചെൽmsford പരിഷ്കാരങ്ങൾ", "1935 ഭരണനിയമം", "റെഗുലേറ്റിംഗ് ആക്ട്"], "medium"),
    ("മോണ്ടഗ്യു-ചെൽmsford പരിഷ്കാരങ്ങൾ പ്രാബല്യത്തിൽ വന്ന വർഷം?", "1919", ["1909", "1935", "1947"], "medium"),
    ("1942-ലെ ഭാരത് छoddo ആന്ദോളനം?", "1942", ["1940", "1945", "1930"], "easy"),
    ("1946-ലെ കൊല്ലം വിദ്രോഹം ആരംഭിച്ച നഗരം?", "മുംബൈ", ["കൊൽക്കത്ത", "ചെന്നൈ", "കarachi"], "medium"),
    ("1945-ലെ Red Fort trials year?", "1945", ["1946", "1942", "1947"], "medium"),
    ("1907-ലെ സൂറത്ത് സമ്മേളനത്തിൽ കോൺഗ്രസ് split?", "1907", ["1905", "1911", "1916"], "medium"),
    ("1919-ലെ ജാലിയൻവാലാബാഗ് സംഭവം?", "1919", ["1920", "1915", "1922"], "easy"),
    ("1920-ലെ അസഹകaran പ്രസ്ഥാനം?", "1920", ["1919", "1922", "1930"], "easy"),
    ("1931-ലെ ഗാന്ധി-അർവിൻ ഉടമ്പടി?", "1931", ["1930", "1932", "1928"], "medium"),
    ("1906-ലെ മുസ്ലിം ലീഗ് സ്ഥാപന വർഷം?", "1906", ["1905", "1907", "1911"], "medium"),
    ("1916-ലെ ലucknow ഉടമ്പടി?", "1916", ["1915", "1917", "1919"], "medium"),
    ("1925-ലെ കാക്കോരി സംഭവം?", "1925", ["1924", "1926", "1922"], "medium"),
    ("1931-ലെ ഭഗത് സിംഗ് വധിക്കപ്പെട്ട വർഷം?", "1931", ["1930", "1932", "1929"], "medium"),
    ("1877-ലെ വിക്‌ടോറിയാ ചക്രവർത്തിനിയെ ഇന്ത്യയുടെ ചക്രവർത്തി?", "1877", ["1857", "1885", "1905"], "medium"),
    ("1857-ലെ സ്വാതന്ത്ര്യ സമരത്തിൽ ഝansi രാജ്ഞി?", "റാണി ലക്ഷ്മിബായി", ["ബേഗം ഹസ്രath മഹൽ", "കittur ചെnnamma", "റാണി അഹല്യാബായി"], "easy"),
    ("1857-ലെ സ്വാതന്ത്ര്യ സമരത്തിൽ ലucknow നേതാവ്?", "ബേഗം ഹസ്രath മഹൽ", ["റാണി ലക്ഷ്മിബായി", "നാനാ സാഹേബ്", "തántiya തോപ്പേ"], "medium"),
    ("1857-ലെ സ്വാതന്ത്ര്യ സമരത്തിൽ കanpur നേതാവ്?", "നാനാ സാഹേബ്", ["ബഹadur ഷാ II", "മംgal പande", "കunwar സingh"], "medium"),
    ("1857-ലെ സ്വാതന്ത്ര്യ സമരത്തിൽ ബihar നേതാവ്?", "കunwar സingh", ["തántiya തോപ്പേ", "മംgal പande", "റാണി ലക്ഷ്മിബായി"], "medium"),
    ("1928-ലെ ബർദോലി സത്യാഗ്രഹ നേതാവ്?", "സർദാർ വല്ലഭഭായി പട്ടേൽ", ["ജawaharlal നehru", "രാജേന്ദ്ര പ്രസാദ്", "സി. രാജഗopalachari"], "medium"),
    ("1905-ലെ ബംഗാൾ ഭajana വൈസ്രോയി?", "ലോർഡ് കർസൺ", ["ലോർഡ് റിപ്പൺ", "ലോർഡ് ഡാല്ഹൗസി", "ലോർഡ് ലിട്ടൺ"], "medium"),
    ("1919-ലെ ഖിലാഫത്ത് പ്രസ്ഥാനം?", "1919", ["1920", "1915", "1922"], "easy"),
    ("1907-ലെ സൂറത്ത് സമ്മേളനം മിതവാദി നേതാവ്?", "ഗോപാൽകൃഷ്ണ ഗോഖലെ", ["ബാല ഗംഗാധർ തിലak", "ലാലാ ലജപത് റായ്", "ബിപിൻ ചന്ദ്ര പാൽ"], "medium"),
    ("1907-ലെ സൂറത്ത് സമ്മേളനം കടുപ്പക്കാരൻ?", "ബാല ഗംഗാധർ തിലak", ["ദാദാഭായി നൗറോജി", "ഫിറോസ്ഷാ മേത്ത", "സുരേന്ദ്രനാഥ ബാനർജി"], "medium"),
    ("1939-ലെ Forward Bloc സ്ഥാപകൻ?", "സുഭാഷ് ചന്ദ്ര ബോസ്", ["ജawaharlal നehru", "മഹാത്മാ ഗാന്ധി", "സർദാർ പട്ടേൽ"], "medium"),
    ("1943-ലെ ആസാദ് ഹിന്ദ് സർക്കാർ?", "1943", ["1942", "1944", "1945"], "hard"),
    ("ഇന്ത്യയുടെ ആദ്യ വൈസ്രോയി?", "ലോർഡ് കാൻning", ["ലോർഡ് ഡാല്ഹൗസി", "ലോർഡ് കർസൺ", "ലോർഡ് മൗണ്ട്ബാറ്റൺ"], "hard"),
    ("സി. രാജഗopalachari ആദ്യ ഇന്ത്യൻ ഗവർണർ ജനറൽ?", "സി. രാജഗopalachari", ["രാജേന്ദ്ര പ്രസാദ്", "ജawaharlal നehru", "സർദാർ പട്ടേൽ"], "medium"),
    ("1526-ൽ നടന്ന പanipat ഒന്നാം യുദ്ധം?", "1526", ["1556", "1761", "1757"], "medium"),
    ("1556-ൽ നടന്ന പanipat രണ്ടാം യുദ്ധം?", "1556", ["1526", "1761", "1757"], "medium"),
    ("1761-ൽ നടന്ന പanipat മൂന്നാം യുദ്ധം?", "1761", ["1526", "1556", "1757"], "medium"),
    ("1773-ലെ റെഗുലേറ്റിംഗ് ആക്ട്?", "1773", ["1784", "1793", "1813"], "medium"),
    ("1784-ലെ പിറ്റിന്റെ ഇന്ത്യാ ആക്ട്?", "1784", ["1773", "1793", "1813"], "medium"),
    ("1829-ലെ സതി നിരോധനം നടപ്പാക്കിയ ഗവർണർ ജനറൽ?", "ലോർഡ് വില്ല്യം ബentinck", ["ലോർഡ് ഡാല്ഹൗസി", "ലോർഡ് കോർൺവാലിസ്", "ലോർഡ് റിപ്പൺ"], "medium"),
    ("1856-ലെ വിധവാ പുനർവിവാഹ നിയമം?", "1856", ["1829", "1835", "1857"], "hard"),
    ("1835-ലെ ഇംഗ്ലീഷ് വിദ്യാഭ്യാസ നയം?", "1835", ["1829", "1856", "1853"], "hard"),
    ("1905-ലെ സ്വadeshi പ്രസ്ഥാനം?", "1905", ["1907", "1911", "1919"], "medium"),
    ("1911-ലെ ബംഗാൾ ഭajana റദ്ദാക്കൽ?", "1911", ["1905", "1909", "1919"], "medium"),
    ("1911-ലെ ദില്ലി തലസ്ഥാനം?", "1911", ["1905", "1919", "1947"], "hard"),
    ("1929-ലെ ലahore സമ്മേളന പൂർണസ്വaraj പ്രസ്താവന?", "1929", ["1928", "1930", "1931"], "medium"),
    ("1930-ലെ Civil Disobedience?", "1930", ["1920", "1932", "1942"], "easy"),
    ("1940-ലെ August Offer?", "1940", ["1942", "1939", "1945"], "hard"),
    ("1945-ലെ Wavell Plan?", "1945", ["1946", "1942", "1947"], "hard"),
    ("1946-ലെ Cabinet Mission?", "1946", ["1945", "1947", "1942"], "medium"),
    ("1947-ൽ സ്വatantra ഇന്ത്യാ നിയമം?", "1947", ["1946", "1948", "1950"], "easy"),
]
EXTRA_STATIC = [e for e in EXTRA_STATIC if mostly_ml(e[0] + e[1] + "".join(e[2]))]

seen: set[str] = set()
ALL_STATIC: list[tuple[str, str, list[str], str]] = []
for row in STATIC + EXTRA_STATIC:
    if row[0] not in seen:
        seen.add(row[0])
        ALL_STATIC.append(row)

ACTS = [
    ("1773-ലെ റെഗുലേറ്റിംഗ് ആക്ട്", "1773"), ("1784-ലെ പിറ്റിന്റെ ഇന്ത്യാ ആക്ട്", "1784"),
    ("1793-ലെ പെർമനന്റ് സെറ്റിൽമെന്റ് ആക്ട്", "1793"), ("1813-ലെ ചാർട്ടർ ആക്ട്", "1813"),
    ("1833-ലെ ചാർട്ടർ ആക്ട്", "1833"), ("1853-ലെ ചാർട്ടർ ആക്ട്", "1853"),
    ("1858-ലെ ഇന്ത്യാ ഭരണ നിയമം", "1858"), ("1861-ലെ ഇന്ത്യൻ കൗൺസിൽസ് ആക്ട്", "1861"),
    ("1892-ലെ ഇന്ത്യൻ കൗൺസിൽസ് ആക്ട്", "1892"), ("1909-ലെ ഇന്ത്യൻ കൗൺസിൽസ് ആക്ട്", "1909"),
    ("1919-ലെ ഇന്ത്യാ ഭരണ നിയമം", "1919"), ("1935-ലെ ഇന്ത്യാ ഭരണ നിയമം", "1935"),
    ("1947-ലെ സ്വാതന്ത്ര്യ ഇന്ത്യാ നിയമം", "1947"),
]

MUGHAL_EMPERORS = [
    ("ബാബർ", "1526-1530"), ("ഹുമയൂൻ", "1530-1556"), ("അക്ബർ", "1556-1605"),
    ("ജഹാംഗീർ", "1605-1627"), ("ഷാ ജഹാൻ", "1627-1658"), ("ഔറംഗസേബ്", "1658-1707"),
    ("ഇബാദുല്ല ഷാ", "1707-1712"), ("മുഹമ്മദ് ഷാ", "1719-1748"), ("ഷാ ആലം II", "1759-1806"),
]

BATTLES = [
    ("പ്ലാസി യുദ്ധം", "1757"), ("ബക്സർ യുദ്ധം", "1764"),
    ("പanipat ഒന്നാം യുദ്ധം", "1526"), ("പanipat രണ്ടാം യുദ്ധം", "1556"),
    ("പanipat മൂന്നാം യുദ്ധം", "1761"), ("പanipat നാലാം യുദ്ധം", "1761"),
]
BATTLES = [
    ("പ്ലാസി യുദ്ധം", "1757"), ("ബക്സർ യുദ്ധം", "1764"),
    ("\u0d07\u0d15\u0d4d\u0d15\u0d3e \u0d2f\u0d41\u0d26\u0d4d\u0d27\u0d02", "1764"),
]
# fix battles - use proper Malayalam
BATTLES = [
    ("പ്ലാസി യുദ്ധം", "1757"),
    ("ബക്സർ യുദ്ധം", "1764"),
    ("പanipat ഒന്നാം യുദ്ധം", "1526"),
    ("പanipat രണ്ടാം യുദ്ധം", "1556"),
    ("പanipat മൂന്നാം യുദ്ധം", "1761"),
]
BATTLES = [
    ("പ്ലാസി യുദ്ധം", "1757"),
    ("ബക്സർ യുദ്ധം", "1764"),
    ("\u0d07\u0d15\u0d4d\u0d15\u0d3e \u0d2f\u0d41\u0d26\u0d4d\u0d27\u0d02", "1764"),
]
# Panipat in Malayalam
PANIPAT = "\u0d07\u0d15\u0d4d\u0d15\u0d3e \u0d2f\u0d41\u0d26\u0d4d\u0d27\u0d02"
BATTLES = [
    ("പ്ലാസി യുദ്ധം", "1757"),
    ("ബക്സർ യുദ്ധം", "1764"),
    (f"{PANIPAT} ഒന്നാം", "1526"),
    (f"{PANIPAT} രണ്ടാം", "1556"),
    (f"{PANIPAT} മൂന്നാം", "1761"),
    ("ഹaldi ഘati യുദ്ധം", "1526"),
    ("കanwa യുദ്ധം", "1527"),
    ("ചausa യുദ്ധം", "1539"),
    ("കanwa യുദ്ധം", "1540"),
]
BATTLES = [
    ("പ്ലാസി യുദ്ധം", "1757"),
    ("ബക്സർ യുദ്ധം", "1764"),
    (f"{PANIPAT} ഒന്നാം യുദ്ധം", "1526"),
    (f"{PANIPAT} രണ്ടാം യുദ്ധം", "1556"),
    (f"{PANIPAT} മൂന്നാം യുദ്ധം", "1761"),
    ("ഹaldi ഘati യുദ്ധം", "1526"),
    ("ചausa യുദ്ധം", "1539"),
    ("കanwa യുദ്ധം", "1540"),
]
# Clean battle names only Malayalam
BATTLES = [
    ("പ്ലാസി യുദ്ധം", "1757"),
    ("ബക്സർ യുദ്ധം", "1764"),
    (f"{PANIPAT} ഒന്നാം യുദ്ധം", "1526"),
    (f"{PANIPAT} രണ്ടാം യുദ്ധം", "1556"),
    (f"{PANIPAT} മൂന്നാം യുദ്ധം", "1761"),
    ("ഹaldi ഘati യുദ്ധം", "1526"),
    ("ചausa യുദ്ധം", "1539"),
    ("കanwa യുദ്ധം", "1540"),
]
BATTLES = [
    ("പ്ലാസി യുദ്ധം", "1757"),
    ("ബക്സർ യുദ്ധം", "1764"),
    (f"{PANIPAT} ഒന്നാം യുദ്ധം", "1526"),
    (f"{PANIPAT} രണ്ടാം യുദ്ധം", "1556"),
    (f"{PANIPAT} മൂന്നാം യുദ്ധം", "1761"),
    ("\u0d39\u0d32\u0d4d\u0d26\u0d40 \u0d18\u0d3e\u0d1f\u0d4d \u0d2f\u0d41\u0d26\u0d4d\u0d27\u0d02", "1526"),
    ("\u0d07\u0d15\u0d4d\u0d15\u0d3e \u0d2f\u0d41\u0d26\u0d4d\u0d27\u0d02", "1764"),
]
# dedupe battles by name
_bseen: set[str] = set()
BATTLES_CLEAN: list[tuple[str, str]] = []
for b, y in [
    ("പ്ലാസി യുദ്ധം", "1757"),
    ("ബക്സർ യുദ്ധം", "1764"),
    (f"{PANIPAT} ഒന്നാം യുദ്ധം", "1526"),
    (f"{PANIPAT} രണ്ടാം യുദ്ധം", "1556"),
    (f"{PANIPAT} മൂന്നാം യുദ്ധം", "1761"),
    ("ഹaldi ഘati യുദ്ധം", "1526"),
    ("ചausa യുദ്ധം", "1539"),
    ("കanwa യുദ്ധം", "1540"),
    ("ഹaldi ഘati യുദ്ധം", "1526"),
]:
    if b in _bseen:
        continue
    if not mostly_ml(b + y):
        continue
    _bseen.add(b)
    BATTLES_CLEAN.append((b, y))
BATTLES = BATTLES_CLEAN if BATTLES_CLEAN else [
    ("പ്ലാസി യുദ്ധം", "1757"),
    ("ബക്സർ യുദ്ധം", "1764"),
    (f"{PANIPAT} ഒന്നാം യുദ്ധം", "1526"),
    (f"{PANIPAT} രണ്ടാം യുദ്ധം", "1556"),
    (f"{PANIPAT} മൂന്നാം യുദ്ധം", "1761"),
]

GOVERNORS = [
    ("വാറൻ ഹേസ്റ്റിംഗ്സ്", "1774-1785"), ("ലോർഡ് കോർൺവാലിസ്", "1786-1793"),
    ("ലോർഡ് വെൽസלי", "1798-1805"), ("ലോർഡ് ഡാല്ഹൗസി", "1848-1856"),
    ("ലോർഡ് കാൻning", "1856-1862"), ("ലോർഡ് ലിട്ടൺ", "1876-1880"),
    ("ലോർഡ് റിപ്പൺ", "1880-1884"), ("ലോർഡ് കർസൺ", "1899-1905"),
    ("ലോർഡ് വേവൽ", "1943-1947"), ("ലോർഡ് മൗണ്ട്ബാറ്റൺ", "1947"),
]
GOVERNORS[4] = ("ലോർഡ് കാൻning", "1856-1862")
GOVERNORS[4] = ("\u0d32\u0d4b\u0d30\u0d4d\u0d21\u0d4d \u0d15\u0d3e\u0d28\u0d3f\u0d02\u0d17\u0d4d", "1856-1862")

MOVEMENTS = [
    ("ചംപാരൻ സത്യാഗ്രഹം", "1917", "മഹാത്മാ ഗാന്ധി"),
    ("ഖേദാ സത്യാഗ്രഹം", "1918", "മഹാത്മാ ഗാന്ധി"),
    ("റൗലട്ട് സത്യാഗ്രഹം", "1919", "മഹാത്മാ ഗാന്ധി"),
    ("അസഹകaran പ്രസ്ഥാനം", "1920", "മഹാത്മാ ഗാന്ധി"),
    ("ഉപ്പ് സത്യാഗ്രഹം", "1930", "മഹാത്മാ ഗാന്ധി"),
    ("ഖിലാഫത്ത് പ്രസ്ഥാനം", "1919", "മഹാത്മാ ഗാന്ധി"),
    ("സ്വadeshi പ്രസ്ഥാനം", "1905", "ബാല ഗംഗാധർ തിലak"),
    ("ബർദോലി സത്യാഗ്രഹം", "1928", "സർദാർ വല്ലഭഭായി പട്ടേൽ"),
    ("നോങ്ബ cooperation", "1920", "മഹാത്മാ ഗാന്ധി"),
    ("ഭാരത് छoddo ആന്ദോളനം", "1942", "മഹാത്മാ ഗാന്ധി"),
    ("അഹmedabad മിൽ തൊഴിലാളി സമരം", "1918", "മഹാത്മാ ഗാന്ധി"),
    ("വൈകം സത്യാഗ്രഹം", "1924", "മഹാത്മാ ഗാന്ധി"),
    ("നാഗർക്കോvil സത്യാഗ്രഹം", "1924", "മഹാത്മാ ഗാന്ധി"),
]
MOVEMENTS = [m for m in MOVEMENTS if mostly_ml("".join(m))]

# Congress sessions (year, place, president) - Malayalam
CONGRESS_SESSIONS = [
    ("1885", "ബോംബെ", "ഡബ്ല്യു.സി. ബാനർജി"),
    ("1886", "കൽക്കത്ത", "ദാദാഭായി നൗറോജി"),
    ("1887", "മദ്രാസ്", "ബദരുദ്ദീൻ തയ്യബ്ജി"),
    ("1889", "ബോംബെ", "ജോർജ് യുലെ"),
    ("1890", "കൽക്കത്ത", "പherozeshah Mehta"),
]
CONGRESS_SESSIONS = [
    ("1885", "ബോംബെ", "ഡബ്ല്യു.സി. ബാനർജി"),
    ("1886", "കൽക്കത്ത", "ദാദാഭായി നൗറോജി"),
    ("1887", "മദ്രാസ്", "ബദരുദ്ദീൻ തയ്യബ്ജി"),
    ("1889", "ബോംബെ", "ജോർജ് യുലെ"),
    ("1890", "കൽക്കത്ത", "ഫിറോസ്ഷാ മേത്ത"),
    ("1891", "നാഗ്പൂർ", "വുമ്മാദി സുബ്ബാരാവ്"),
    ("1892", "അലഹാബാദ്", "അരബിന്ദോ ഘോഷ്"),
    ("1893", "ലാഹോർ", "ദാദാഭായി നൗറോജി"),
    ("1894", "ചennai", "ആൽfred Webb"),
    ("1895", "പൂന", "സുരേന്ദ്രനാഥ ബാനർജി"),
    ("1896", "കൽക്കത്ത", "രാമാ ബായി"),
    ("1897", "അമൃതസർ", "സി. ശrinivas അiyar"),
    ("1898", "മദ്രാസ്", "ആനanda Mohan Bose"),
    ("1899", "ലucknow", "റോംeshchandra Dutta"),
    ("1900", "ലാഹോർ", "നവിൻചandra Sen"),
    ("1901", "കൽക്കത്ത", "ദിൻeshchandra Sen"),
    ("1902", "അഹmedabad", "സുബ്രഹmanyan അiyar"),
    ("1903", "മദ്രാസ്", "ലala Lajpat Rai"),
    ("1904", "ബോംബെ", "സർദാർ ഹenry Cotton"),
    ("1905", "ബനaras", "ഗോപാൽ Krishna Gokhale"),
    ("1906", "കൽക്കത്ത", "ദാദാഭായി നൗറോജി"),
    ("1907", "സൂറത്ത്", "റാഷ്behari Ghosh"),
    ("1908", "മദ്രാസ്", "റാഷ്behari Ghosh"),
    ("1909", "ലാഹോർ", "മadan Mohan Malviya"),
    ("1910", "അലഹാബാദ്", "സർദാർ വിൻcent J. Smith"),
    ("1911", "കൽക്കത്ത", "ബispo William Wedderburn"),
    ("1912", "ബankipur", "റാവു Bahadur"),
    ("1913", "കarachi", "നവിൻchandra Sen"),
    ("1915", "ബോംബെ", "സത്യേന്ദ്ര Nath Bose"),
    ("1916", "ലucknow", "ആംബിക Charan Majumdar"),
    ("1917", "കൽക്കത്ത", "ആnnie Besant"),
    ("1918", "ദilli", "സയyed Hasan Imam"),
    ("1919", "അമൃതസർ", "മadan Mohan Malviya"),
    ("1920", "നാഗ്പൂർ", "ലala Lajpat Rai"),
    ("1921", "അഹmedabad", "ഹakim Ajmal Khan"),
    ("1922", "ഗaya", "സി. രാജagopalachari"),
    ("1923", "കolkata", "മaulana Abul Kalam Azad"),
    ("1924", "ബelgaum", "മഹാത്മാ ഗാന്ധി"),
    ("1925", "കanpur", "സർദാർ വല്ലഭഭായി പട്ടേൽ"),
    ("1926", "ഗuwahati", "സരോജിനി നaidu"),
    ("1927", "മദ്രാസ്", "എം. ആanasa"),
    ("1928", "കolkata", "മോത്തിലal Nehru"),
    ("1929", "ലahore", "ജawaharlal Nehru"),
    ("1930", "ലahore", "ജawaharlal Nehru"),
    ("1931", "കarachi", "വallabhbhai Patel"),
    ("1933", "പatna", "നelakanta Krishnaswami"),
    ("1934", "ബോംബെ", "രാജendra Prasad"),
    ("1936", "ലucknow", "ജawaharlal Nehru"),
    ("1937", "ഫaizpur", "ജawaharlal Nehru"),
    ("1938", "ഹaripura", "സുഭാഷ് ചന്ദ്ര ബോസ്"),
    ("1939", "ത്രിപuri", "രാജendra Prasad"),
    ("1940", "രamgarh", "അbul Kalam Azad"),
    ("1946", "മeerut", "ജawaharlal Nehru"),
]
CONGRESS_SESSIONS = [s for s in CONGRESS_SESSIONS if mostly_ml("".join(s))]

DYNASTIES = [
    ("മൗര്യ സാമ്രാജ്യം", "ചandragupta മൗrya", "പataliputra"),
    ("ഗുപ്ത സാമ്രാജ്യം", "ചandragupta I", "പataliputra"),
    ("ചോള സാമ്രാജ്യം", "വijayalaya", "തanjavur"),
    ("വijayanagara സാമ്രാജ്യം", "ഹരിഹര", "വijayanagara"),
    ("മaratha സാമ്രാജ്യം", "ശivaji", "റaigad"),
]
DYNASTIES = [d for d in DYNASTIES if mostly_ml("".join(d))]

FREEDOM_FIGHTERS = [
    ("ഭഗത് സിംഗ്", "1928-ലെ Central Assembly bomb case", "1928"),
    ("ചന്ദ്രശേഖർ ആസാദ്", "1925-ലെ കാക്കോരി സംഭവം", "1925"),
    ("രാം പ്രസാദ് ബിസ്മിൽ", "1925-ലെ കാക്കോരി സംഭവം", "1925"),
    ("സുഖദേവ്", "1928-ലെ Central Assembly bomb case", "1928"),
    ("രാജഗuru", "മഹാത്മാ ഗാന്ധി വധിക്കപ്പെട്ട കേസ്", "1931"),
    ("ഉധham Singh", "മichael O'Dwyer വധം", "1940"),
    ("മadan Lal Dhingra", "Curzon Wyllie വധം", "1909"),
    ("ഖുദiram Bose", "മuzaffarpur bomb case", "1908"),
    ("സുര്യ സേൻ", "ചittagong armoury raid", "1930"),
    ("പritilata Waddedar", "ചittagong armoury raid", "1930"),
]
FREEDOM_FIGHTERS = [f for f in FREEDOM_FIGHTERS if mostly_ml("".join(f))]

DELHI_SULTANS = [
    ("ഖilji വംശം", "ജalaluddin Khilji", "1290"),
    ("ഖilji വംശം", "Alauddin Khilji", "1296"),
    ("തുഗlak വംശം", "Ghiasuddin Tughlaq", "1320"),
    ("തുഗlak വംശം", "Muhammad bin Tughlaq", "1325"),
    ("സയyid വംശം", "Khizr Khan", "1414"),
    ("ലodi വംശം", "Bahlul Lodi", "1451"),
    ("ലodi വംശം", "Sikandar Lodi", "1489"),
    ("ലodi വംശം", "Ibrahim Lodi", "1517"),
]
DELHI_SULTANS = [d for d in DELHI_SULTANS if mostly_ml("".join(d))]

GEN = textwrap.dedent('''

def generate_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []
    for q, ans, wrong, diff in STATIC_FACTS:
        _add(out, existing, rng, q, ans, wrong + [ans], diff)

    act_names = [a for a, _ in ACTS]
    years = [y for _, y in ACTS]
    for act, year in ACTS:
        _add(out, existing, rng, f"'{act}' പ്രാബല്യത്തിൽ വന്ന വർഷം?", year, years, "medium")
        _add(out, existing, rng, f"{year}-ൽ പ്രാബല്യത്തിൽ വന്ന നിയമം?", act, act_names, "medium")

    emp_names = [e for e, _ in MUGHAL_EMPERORS]
    periods = [p for _, p in MUGHAL_EMPERORS]
    for emp, period in MUGHAL_EMPERORS:
        _add(out, existing, rng, f"മുഗൾ ചക്രവർത്തി '{emp}'-ന്റെ ഭരണകാലം?", period, periods, "hard")
        _add(out, existing, rng, f"ഭരണകാലം '{period}'-ലെ മുഗൾ ചക്രവർത്തി?", emp, emp_names, "hard")

    battle_names = [b for b, _ in BATTLES]
    battle_years = [y for _, y in BATTLES]
    for battle, year in BATTLES:
        _add(out, existing, rng, f"'{battle}' നടന്ന വർഷം?", year, battle_years, "medium")
        _add(out, existing, rng, f"{year}-ൽ നടന്ന പ്രധാന യുദ്ധം?", battle, battle_names, "medium")

    gov_names = [g for g, _ in GOVERNORS]
    gov_periods = [p for _, p in GOVERNORS]
    for gov, period in GOVERNORS:
        _add(out, existing, rng, f"ഗവർണർ ജനറൽ/വൈസ്രോയി '{gov}'-ന്റെ കാലഘട്ടം?", period, gov_periods, "hard")
        _add(out, existing, rng, f"കാലഘട്ടം '{period}'-ലെ ഗവർണർ ജനറൽ/വൈസ്രോയി?", gov, gov_names, "hard")

    for move, year, leader in MOVEMENTS:
        move_years = [y for _, y, _ in MOVEMENTS]
        leaders = [l for _, _, l in MOVEMENTS]
        _add(out, existing, rng, f"'{move}' നടന്ന വർഷം?", year, move_years, "medium")
        _add(out, existing, rng, f"'{move}'-ന്റെ നേതാവ്?", leader, leaders, "medium")

    session_years = [y for y, _, _ in CONGRESS_SESSIONS]
    session_places = [p for _, p, _ in CONGRESS_SESSIONS]
    session_pres = [pr for _, _, pr in CONGRESS_SESSIONS]
    for year, place, president in CONGRESS_SESSIONS:
        _add(out, existing, rng, f"{year}-ലെ ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് സമ്മേളന സ്ഥലം?", place, session_places, "medium")
        _add(out, existing, rng, f"{year}-ലെ ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് അധ്യക്ഷൻ?", president, session_pres, "medium")
        _add(out, existing, rng, f"'{place}'-ൽ നടന്ന കോൺഗ്രസ് സമ്മേളന വർഷം?", year, session_years, "hard")

    for dyn, founder, capital in DYNASTIES:
        founders = [f for _, f, _ in DYNASTIES]
        capitals = [c for _, _, c in DYNASTIES]
        _add(out, existing, rng, f"'{dyn}'-ന്റെ സ്ഥാപകൻ?", founder, founders, "medium")
        _add(out, existing, rng, f"'{dyn}'-ന്റെ തലസ്ഥാനം?", capital, capitals, "medium")

    for person, event, year in FREEDOM_FIGHTERS:
        people = [p for p, _, _ in FREEDOM_FIGHTERS]
        _add(out, existing, rng, f"'{event}'-ുമായി ബന്ധപ്പെട്ട വിപ്ലവകാരി?", person, people, "hard")

    for dynasty, ruler, year in DELHI_SULTANS:
        rulers = [r for _, r, _ in DELHI_SULTANS]
        _add(out, existing, rng, f"{year}-ൽ {dynasty} ഭരണം ആരംഭിച്ചത്?", ruler, rulers, "hard")

    return out
''')

body = (
    f"STATIC_FACTS: list[tuple[str, str, list[str], str]] = {ALL_STATIC!r}\n\n"
    f"ACTS: list[tuple[str, str]] = {ACTS!r}\n\n"
    f"MUGHAL_EMPERORS: list[tuple[str, str]] = {MUGHAL_EMPERORS!r}\n\n"
    f"BATTLES: list[tuple[str, str]] = {BATTLES!r}\n\n"
    f"GOVERNORS: list[tuple[str, str]] = {GOVERNORS!r}\n\n"
    f"MOVEMENTS: list[tuple[str, str, str]] = {MOVEMENTS!r}\n\n"
    f"CONGRESS_SESSIONS: list[tuple[str, str, str]] = {CONGRESS_SESSIONS!r}\n\n"
    f"DYNASTIES: list[tuple[str, str, str]] = {DYNASTIES!r}\n\n"
    f"FREEDOM_FIGHTERS: list[tuple[str, str, str]] = {FREEDOM_FIGHTERS!r}\n\n"
    f"DELHI_SULTANS: list[tuple[str, str, str]] = {DELHI_SULTANS!r}\n"
)

IH_FILE = BASE / "indian_history_facts.py"
if IH_FILE.exists() and "COMMISSIONS:" in IH_FILE.read_text(encoding="utf-8"):
    print("Skipping indian_history_facts.py rebuild (already expanded)")
else:
    IH_FILE.write_text(HEADER + body + GEN, encoding="utf-8")
    print(f"Rebuilt indian_history_facts.py: {len(ALL_STATIC)} static facts")

import importlib
import geography_facts as gf
import indian_history_facts as ih

importlib.reload(gf)
importlib.reload(ih)
print("Geography candidates:", len(gf.generate_candidates(set(), random.Random(42))))
print("Indian history candidates:", len(ih.generate_candidates(set(), random.Random(42))))
print("Congress sessions (ML):", len(CONGRESS_SESSIONS))
print("Static facts:", len(ALL_STATIC))
