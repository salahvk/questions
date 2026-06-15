#!/usr/bin/env python3
"""Patch geography_facts.py with expanded data from _expand.py."""

from __future__ import annotations

import ast
import importlib.util
import random
import textwrap
from pathlib import Path

BASE = Path(__file__).parent
TARGET = BASE / "geography_facts.py"

existing = TARGET.read_text(encoding="utf-8")
header_end = existing.index("def _pick3")
HEADER = existing[:header_end]

mod = ast.parse(existing)
states_list: list[tuple[str, str]] = []
for node in mod.body:
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        if node.target.id == "INDIAN_STATE_CAPITALS":
            states_list = ast.literal_eval(node.value)
            break

state_names = [s for s, _ in states_list]
KL = next(s for s, c in states_list if c == "തിരുവനന്തപുരം")

spec = importlib.util.spec_from_file_location("_expand", BASE / "_expand.py")
exp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exp)


def emit(name: str, rows: list[tuple], comment: str = "") -> str:
    lines: list[str] = []
    if comment:
        lines.append(f"# {comment}")
    lines.append(f"{name}: list[tuple[str, ...]] = [")
    for row in rows:
        lines.append("    (" + ", ".join(repr(c) for c in row) + "),")
    lines.append("]")
    return "\n".join(lines)


def emit_dict(name: str, mapping: dict[str, list[str]]) -> str:
    lines = [f"{name}: dict[str, list[str]] = {{"]
    for k, vals in mapping.items():
        lines.append(f"    {k!r}: [{', '.join(repr(v) for v in vals)}],")
    lines.append("}")
    return "\n".join(lines)


KERALA_DISTRICTS = [
    ("തിരുവനന്തപുരം", "തിരുവനന്തപുരം"),
    ("കൊല്ലം", "കൊല്ലം"),
    ("പത്തനംതിട്ട", "പത്തനംതിട്ട"),
    ("ആലപ്പുഴ", "ആലപ്പുഴ"),
    ("കോട്ടയം", "കോട്ടയം"),
    ("ഇടുക്കി", "പൈനാവ്"),
    ("എറണാകുളം", "കൊച്ചി"),
    ("തൃശ്ശൂർ", "തൃശ്ശൂർ"),
    ("പാലക്കാട്", "പാലക്കാട്"),
    ("മലപ്പുറം", "മലപ്പുറം"),
    ("കോഴിക്കോട്", "കോഴിക്കോട്"),
    ("വയനാട്", "കല്പ്പറ്റ"),
    ("കണ്ണൂർ", "കണ്ണൂർ"),
    ("കാസർഗോഡ്", "കാസർഗോഡ്"),
]

INDIA_PORTS = [
    ("കൊച്ചി", KL),
    ("വിഴിഞ്ഞം", KL),
    ("എന്സം", KL),
    ("മുംബൈ", "മഹാരാഷ്ട്ര"),
    ("നാവാ മുംബൈ", "മഹാരാഷ്ട്ര"),
    ("ചെന്നൈ", "തമിഴ്നാട്"),
    ("വിശാഖപട്ടണം", "ആന്ധ്രപ്രദേശ്"),
    ("പാരദീപ്", "ഒഡിഷ"),
    ("ട്യൂട്ടികോറിൻ", "തമിഴ്നാട്"),
    ("പോർട് ബ്ലെയർ", "അണ്ടമാൻ"),
]

NI = {
    11: [22, 10],
    22: [11, 10, 0],
    10: [11, 22, 0, 23, 13, 5],
    0: [22, 10, 23, 18, 4],
    23: [10, 0, 13, 4, 18],
    13: [5, 10, 23, 4, 12, 6],
    5: [13, 10],
    6: [13, 12, 20],
    20: [6, 12, 25, 7, 19],
    12: [20, 6, 13, 4, 25],
    4: [12, 13, 23, 18, 9, 25],
    18: [4, 23, 0, 9, 27],
    9: [4, 18, 27, 3, 25],
    3: [9, 27, 25],
    27: [18, 9, 3, 21, 2],
    2: [27, 21, 1, 17, 14, 15, 24, 16],
    21: [27, 2],
    1: [2],
    17: [2, 14],
    14: [2, 17, 16],
    15: [2],
    24: [2, 16],
    16: [2, 24, 14],
    25: [20, 12, 4, 9, 3, 7, 28, 26],
    7: [20, 19, 8, 26, 25, 28],
    19: [20, 7, 8, 29],
    8: [19, 7, 26],
    26: [25, 7, 8],
    28: [25, 7],
    29: [19, 8, 30],
    30: [29, 8],
}
STATE_NEIGHBORS = {state_names[k]: [state_names[i] for i in v] for k, v in NI.items()}

TROPIC_CANCER_STATES = [
    "ഗുജറാത്ത്", "രാജസ്ഥാൻ", "മധ്യപ്രദേശ്", "ഛത്തീസ്ഗഢ്",
    "ഝാർഖണ്ഡ്", "പശ്ചിമബംഗാൾ", "ത്രിപുര", "മിസോറം",
]

INDIAN_RIVER_ORIGIN = [
    ("ഗംഗാ", "ഉത്തരാഖണ്ഡ്"),
    ("യമുന", "ഉത്തരാഖണ്ഡ്"),
    ("ബ്രഹ്മപുത്ര", "അരുണാചൽ പ്രദേശ്"),
    ("ഗോദാവരി", "മഹാരാഷ്ട്ര"),
    ("കൃഷ്ണ", "മഹാരാഷ്ട്ര"),
    ("നർമ്മദ", "മധ്യപ്രദേശ്"),
    ("താപ്തി", "മഹാരാഷ്ട്ര"),
    ("കാവേരി", "കർണാടക"),
    ("മഹാനദി", "ഛത്തീസ്ഗഢ്"),
    ("പെരിയാർ", KL),
    ("പമ്പ", KL),
    ("ഭാരതപ്പുഴ", KL),
    ("ചാലിയാർ", KL),
    ("നെയ്യാർ", KL),
    ("സത്ലജ്", "ഹിമാചൽ പ്രദേശ്"),
    ("ചംബൽ", "മധ്യപ്രദേശ്"),
    ("സോൺ", "മധ്യപ്രദേശ്"),
    ("ഡാമോദർ", "ഝാർഖണ്ഡ്"),
]

UNESCO_INDIA = [
    ("താജ് മഹൽ", "ഉത്തരപ്രദേശ്"),
    ("ഹുമായൂന്റെ കബ്ര", "ദില്ലി"),
    ("ഹംപി", "കർണാടക"),
    ("സുന്ദർബൻസ്", "പശ്ചിമബംഗാൾ"),
    ("കജുരാഹോ", "മധ്യപ്രദേശ്"),
    ("പട്മാവതി", "രാജസ്ഥാൻ"),
    ("മനാസ്", "അസം"),
    ("\u0d15\u0d3e\u0d1c\u0d40\u0d30\u0d3e\u0d02\u0d17", "അസം"),
]

GENERATE = textwrap.dedent("""
def _pick3(pool: list[str], correct: str, rng: random.Random) -> list[str]:
    wrong = [x for x in pool if x != correct]
    rng.shuffle(wrong)
    opts = [correct] + wrong[:3]
    while len(opts) < 4:
        opts.append("ഒന്നുമില്ല")
    return opts[:4]


def generate_candidates(existing: set[str], rng: random.Random) -> list[tuple[str, list[str], str, str]]:
    out: list[tuple[str, list[str], str, str]] = []
    capitals = [c for _, c in CAPITALS]
    countries = [c for c, _ in CAPITALS]
    seas = list({s for _, s in ISLAND_SEAS})
    states = [s for s, _ in INDIAN_STATE_CAPITALS]
    state_caps = [c for _, c in INDIAN_STATE_CAPITALS]

    def add(q: str, ans: str, wrong: list[str], diff: str = "medium") -> None:
        q = q.strip()
        if not q or q in existing:
            return
        opts = _pick3(wrong + [ans], ans, rng)
        if len(set(opts)) != 4 or ans not in opts:
            return
        out.append((q, opts, ans, diff))
        existing.add(q)

    for state, capital in INDIAN_STATE_CAPITALS:
        add(
            f"{state} സംസ്ഥാനത്തിന്റെ തലസ്ഥാനം ഏതാണ്?",
            capital,
            [c for c in state_caps if c != capital],
            "easy",
        )
        add(
            f"'{capital}' ഏത് സംസ്ഥാനത്തിന്റെ തലസ്ഥാനമാണ്?",
            state,
            [s for s in states if s != state],
            "easy",
        )

    for country, capital in CAPITALS:
        add(
            f"{country} രാജ്യത്തിന്റെ തലസ്ഥാനം ഏതാണ്?",
            capital,
            [c for c in capitals if c != capital],
            "easy",
        )
        add(
            f"'{capital}' ഏത് രാജ്യത്തിന്റെ തലസ്ഥാനമാണ്?",
            country,
            [c for c in countries if c != country],
            "medium",
        )

    for place, sea in ISLAND_SEAS:
        add(
            f"{place} ഏത് സമുദ്രത്തിലാണ് സ്ഥിതി ചെയ്യുന്നത്?",
            sea,
            [s for s in seas if s != sea],
            "medium",
        )

    for nick, country in COUNTRY_NICKNAMES:
        add(
            f"ഏത് രാജ്യമാണ് '{nick}' എന്നറിയപ്പെടുന്നത്?",
            country,
            [c for c in countries if c != country],
            "medium",
        )

    for landmark, country in LANDMARKS:
        add(
            f"ഏത് രാജ്യത്താണ് '{landmark}' സ്ഥിതി ചെയ്യുന്നത്?",
            country,
            [c for c in countries if c != country],
            "easy",
        )

    for river, flows in RIVERS:
        add(
            f"{river} നദി ഏത് സമുദ്രത്തിലേക്ക്/നദിയിലേക്ക് പതിക്കുന്നു?",
            flows,
            [s for s in seas + ["അറബിക്കടൽ", "ബംഗാൾ കടൽ"] if s != flows],
            "medium",
        )

    for item in KERALA_FACTS + INDIA_FACTS + WORLD_FACTS:
        add(item[0], item[1], item[2], item[3])

    rivers_d = list({r for _, r, _ in INDIAN_DAMS})
    states_d = list({s for _, _, s in INDIAN_DAMS})
    for dam, river, state in INDIAN_DAMS:
        add(f"'{dam}' അണക്കെട്ട് ഏത് നദിയിലാണ്?", river, [r for r in rivers_d if r != river], "medium")
        add(f"'{dam}' അണക്കെട്ട് ഏത് സംസ്ഥാനത്താണ്?", state, [s for s in states_d if s != state], "medium")
        add(f"{river} നദിയിലെ '{dam}' അണക്കെട്ട് ഏത് സംസ്ഥാനത്താണ്?", state, [s for s in states_d if s != state], "medium")

    parks_states = list({s for _, s in INDIAN_NATIONAL_PARKS})
    for park, state in INDIAN_NATIONAL_PARKS:
        add(
            f"'{park}' ദേശീയോദ്യാനം ഏത് സംസ്ഥാനത്താണ്?",
            state,
            [s for s in parks_states if s != state],
            "medium",
        )

    heights = list({h for _, _, h in MOUNTAIN_PEAKS})
    ranges = list({r for _, r, _ in MOUNTAIN_PEAKS})
    for peak, rng_name, height in MOUNTAIN_PEAKS:
        add(f"'{peak}' ഉയരം എത്ര?", height, [h for h in heights if h != height], "hard")
        add(
            f"{height} ഉയരമുള്ള '{peak}' ഏത് പർവതനിരയിലാണ്?",
            rng_name,
            [r for r in ranges if r != rng_name],
            "hard",
        )
        add(
            f"'{peak}' ഏത് പർവതനിരയിലെ ശിഖരമാണ്?",
            rng_name,
            [r for r in ranges if r != rng_name],
            "hard",
        )

    dist_names = [d for d, _ in KERALA_DISTRICTS]
    hqs = [h for _, h in KERALA_DISTRICTS]
    for district, hq in KERALA_DISTRICTS:
        add(
            f"കേരളത്തിലെ '{district}' ജില്ലയുടെ ആസ്ഥാനം ഏതാണ്?",
            hq,
            [h for h in hqs if h != hq],
            "easy",
        )
        add(
            f"കേരളത്തിലെ '{hq}' ഏത് ജില്ലയുടെ ആസ്ഥാനമാണ്?",
            district,
            [d for d in dist_names if d != district],
            "medium",
        )

    port_states = list({s for _, s in INDIA_PORTS})
    for port, state in INDIA_PORTS:
        add(
            f"'{port}' തുറമുഖം ഏത് സംസ്ഥാനത്താണ്?",
            state,
            [s for s in port_states if s != state],
            "medium",
        )

    for state, neighbors in STATE_NEIGHBORS.items():
        if state not in states:
            continue
        non_neighbors = [s for s in states if s != state and s not in neighbors]
        if len(non_neighbors) >= 3:
            add(
                f"'{state}' സംസ്ഥാനവുമായി അതിർത്തി പങ്കിടാത്ത സംസ്ഥാനം ഏത്?",
                non_neighbors[0],
                non_neighbors[1:4],
                "hard",
            )
        for nb in neighbors:
            if nb in states:
                add(
                    f"'{state}' സംസ്ഥാനവുമായി അതിർത്തി പങ്കിടുന്ന സംസ്ഥാനം ഏത്?",
                    nb,
                    [s for s in states if s != nb and s != state][:3],
                    "medium",
                )

    for st in TROPIC_CANCER_STATES:
        add(
            f"കർക്കരേഖ (ട്രോപ്പിക് ഓഫ് കാൻസർ) കടന്നുപോകുന്ന ഇന്ത്യൻ സംസ്ഥാനം ഏത്?",
            st,
            [s for s in TROPIC_CANCER_STATES if s != st],
            "medium",
        )

    origin_states = list({s for _, s in INDIAN_RIVER_ORIGIN})
    for river, origin in INDIAN_RIVER_ORIGIN:
        add(
            f"{river} നദിയുടെ ഉത്ഭവസ്ഥാനം ഏത് സംസ്ഥാനത്താണ്?",
            origin,
            [s for s in origin_states if s != origin],
            "medium",
        )

    unesco_locs = list({loc for _, loc in UNESCO_INDIA})
    for place, location in UNESCO_INDIA:
        add(
            f"യുനെസ്കോ ലോക പൈതൃക കേന്ദ്രമായ '{place}' എവിടെയാണ്?",
            location,
            [l for l in unesco_locs if l != location],
            "hard",
        )

    return out
""")

tropic_block = "TROPIC_CANCER_STATES: list[str] = [\n"
for s in TROPIC_CANCER_STATES:
    tropic_block += f"    {s!r},\n"
tropic_block += "]\n"

extra = "\n".join([
    emit("INDIAN_DAMS", exp.INDIAN_DAMS, "Indian dams (name, river, state)"),
    emit("INDIAN_NATIONAL_PARKS", exp.INDIAN_NATIONAL_PARKS, "National parks"),
    emit("MOUNTAIN_PEAKS", exp.MOUNTAIN_PEAKS, "Mountain peaks"),
    emit("KERALA_DISTRICTS", KERALA_DISTRICTS, "Kerala districts (district, HQ)"),
    emit("INDIA_PORTS", INDIA_PORTS, "Major ports"),
    emit_dict("STATE_NEIGHBORS", STATE_NEIGHBORS),
    tropic_block,
    emit("INDIAN_RIVER_ORIGIN", INDIAN_RIVER_ORIGIN, "River origin states"),
    emit("UNESCO_INDIA", UNESCO_INDIA, "UNESCO sites in India"),
    "",
])

out_text = HEADER + extra + GENERATE
TARGET.write_text(out_text, encoding="utf-8")

rng = random.Random(42)
import importlib
import geography_facts as gf
importlib.reload(gf)
n = len(gf.generate_candidates(set(), rng))
print(f"Patched geography_facts.py — {n} candidates")
