#!/usr/bin/env python3
"""Surgically rebuild _ii_cat_pairs.py."""
from __future__ import annotations

import ast
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "_ii_cat_pairs.py"
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def ok(s: str) -> str:
    if MIXED.search(s):
        raise ValueError(repr(s))
    return s


CANARA = ok("ക" + "ാ" + "ന" + "ര" + "ാ" + " ബാങ്ക്")
KOTAK = ok("ക" + "ോ" + "ട" + "ക" + " മഹ" + "ീ" + "ന്ദ" + "്" + "്ര" + "ാ" + " ബാങ്ക്")
BOM = ok("ബാങ്ക് ഓഫ് മ" + "ഹ" + "ാ" + "ര" + "ാ" + "ഷ" + "്" + "ട" + "്ര")
PNB = ok("പ" + "ം" + "ജ" + "ാ" + "ബ" + "്" + " നാഷണൽ ബാങ്ക്")
IIST = ok("ഐ" + "." + "ഐ" + "." + "എ" + "." + "സ്" + "." + "ട" + "ി" + ".")
NCW = ok("എ" + "ൻ" + "." + "സ" + "ി" + "." + "ഡ" + "ബ" + "്" + "ല" + "്" + "യ" + "ു")
SEBI = ok("സ" + "െ" + "." + "ഇ" + "." + "ബ" + "ി" + "." + "ഐ" + ".")
NCB = ok("എ" + "ൻ" + "." + "സ" + "ി" + "." + "ബ" + "ി" + ".")


def q(s: str) -> str:
    return repr(s)


def main() -> None:
    spec = importlib.util.spec_from_file_location("g", ROOT / "_gen_ii_wave30.py")
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)  # type: ignore[union-attr]

    old = (ROOT / "_ii_cat_pairs.py").read_text(encoding="utf-8")
    lines = old.splitlines(keepends=True)
    head = "".join(lines[:76])
    mid = "".join(lines[105:206])

    replacements = {
        '("ബാങ്ക് ഓഫ് ബറോഡ", "MUM")': f"({q(BOM)}, \"MUM\")",
        '("കാനara ബാങ്ക്", "MNG")': f"({q(CANARA)}, \"MNG\")",
        '("കോടak മഹindra ബാങ്ക്", "MUM")': f"({q(KOTAK)}, \"MUM\")",
        '("ബാങ്ക് ഓഫ് മഹarashtra", "PUN")': f"({q(BOM)}, \"PUN\")",
        '("പunjab നാഷണൽ ബാങ്ക്", "DEL")': f"({q(PNB)}, \"DEL\")",
        '("ഐ.ഐ.എസ്.ടt.", "VAL")': f"({q(IIST)}, \"VAL\")",
        '("ഐ.ഐ.എസ്.ടt.", "VAL")': f"({q(IIST)}, \"VAL\")",
    }
    for old_s, new_s in replacements.items():
        mid = mid.replace(old_s, new_s)
    mid = mid.replace('("ഐ.ഐ.എസ്.ടt.", "VAL")', f"({q(IIST)}, \"VAL\")", 1)

    # REGULATOR rows from gen_ii clean HQ + extras from same module strings
    reg: list[tuple[str, str]] = []
    city_key = {
        g.HQ_PAIRS[0][1]: "MUM",
        g.HQ_PAIRS[1][1]: "DEL",
        g.HQ_PAIRS[14][1]: "BLR",
        g.HQ_PAIRS[27][1]: "PUN",
    }
    for a, b in g.HQ_PAIRS:
        if MIXED.search(a + b):
            continue
        reg.append((a, city_key.get(b, "DEL")))
    extra_names = [
        "സെ.ബi.ഐ.", "ഐ.ആർ.ഡi.എ.ഐ.", "പi.എഫ്.ആർ.ഡi.എ.",
    ]
    # load SEBI etc from gen if present else skip
    for a, k in [
        (SEBI, "MUM"), (NCB, "DEL"), (NCW, "DEL"),
        ("എൻ.സി.പi.സi.ആർ.", "DEL"),
    ]:
        ok(a)
        reg.append((a, k))

    reg_lines = ["    d[\"REGULATOR_HQ\"] = rk(["]
    for a, k in reg[:31]:
        reg_lines.append(f"        ({q(a)}, {q(k)}),")
    reg_lines.append("    ], c)\n")

    premier = f'''
    d["PREMIER_INST_HQ"] = rk([
        ("ഐ.ഐ.ടി മുംബൈ", "MUM"), ("ഐ.ഐ.ടി ഡൽഹി", "DEL"), ("ഐ.ഐ.ടി മദ്രാസ്", "CHN"),
        ("ഐ.ഐ.ടി കാൻപൂർ", "KNP"), ("ഐ.ഐ.ടി ഖരഗ്പൂർ", "KGP"), ("ഐ.ഐ.ടി റൂർക്കി", "RKE"),
        ("ഐ.ഐ.ടി ഹൈദരാബാദ്", "HYD"), ("ഐ.ഐ.ടി ഗാന്ധിനഗർ", "GNT"), ("ഐ.ഐ.ടി ഭuvoeneശ്വർ", "BBS"),
        ("ഐ.ഐ.ടി ഇന്ദോർ", "IND"), ("ഐ.ഐ.ടി മണ്ഡി", "MND"), ("ഐ.ഐ.ടി ഗുവാഹാടി", "GWH"),
        ("ഐ.ഐ.ടി രോപ്രാഗ്രം", "RPR"), ("ഐ.ഐ.ടി ജോധ്പൂർ", "JDH"), ("ഐ.ഐ.ടി പട്ന", "PTN"),
        ("ഐ.ഐ.എം അഹമദാബാദ്", "AHM"), ("ഐ.ഐ.എം കൊൽക്കത്ത", "KOL"),
        ("ഐ.ഐ.എം ലഖ\u200cനൗ", "LKO"), ("ഐ.ഐ.എം കോഴിക്കോട്", "KOZ"), ("ഐ.ഐ.എം ഇന്ദോർ", "IND"),
        ("എൻ.ഐ.ടി. കാലിക്കറ്റ്", "KOZ"), ("എൻ.ഐ.ടി. തിരുച്ചി", "TRI"), ("എൻ.ഐ.ടി. സുരത്തികൽ", "SUR"),
        ("ഐ.ഐ.എസ്.സി.", "BLR"), ("ഐ.ഐ.എസ്.ഇ.ആർ. തിരുവനന്തപുരം", "TVM"),
        ("ഐ.ഐ.എസ്.ഇ.ആർ. പൂണെ", "PUN"), ("ഐ.ഐ.എസ്.ഇ.ആർ. കൊൽക്കത്ത", "KOL"),
        ({q(IIST)}, "VAL"),
    ], c)
    d["PREMIER_INST_HQ"] += [
        ("ഐ.ഐ.എം " + c["BLR"], c["BLR"]),
        ("ഐ.ഐ.ടി " + c["BLR"], c["BLR"]),
        ("എൻ.ഐ.ടി. " + c["VNS"], c["VNS"]),
    ]
'''
    premier = premier.replace("ഭuvoeneശwxr", "ഭuvoeneശwxr")

    print("Script needs manual BBS fix and tail categories")


if __name__ == "__main__":
    main()
