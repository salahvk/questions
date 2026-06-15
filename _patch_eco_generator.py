#!/usr/bin/env python3
"""Patch _gen_build_economics_wave20_data.py with Malayalam category blocks."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).parent
GEN = ROOT / "_gen_build_economics_wave20_data.py"


def _line(stem: str, ans: str, wrong: list[str], diff: str = "medium") -> str:
    return f"    _f({stem!r}, {ans!r}, {wrong!r}, {diff!r}),"


def emit_facts(name: str, rows: list) -> str:
    lines = [f"{name}: list[Fact] = ["]
    lines.extend(_line(*r) for r in rows)
    lines.append("]")
    return "\n".join(lines)


def replace_cat(text: str, name: str, block: str) -> str:
    start = text.index(f"\n{name}: list[Fact] = [")
    end = text.index("\n]", start) + 2
    return text[:start] + "\n" + block + text[end:]


def fix_fiscal(rows: list) -> list:
    out = []
    reps = [
        ("ധനകാര്യ konsolidation?", "ധനകാര്യ ഏകീകരണം?"),
        ("crowding out?", "സർക്കാർ വായ്പ തള്ളിക്ക挤 പ്രഭാവം?"),
        ("crowding in?", "സർക്കാർ ചെലവ് പ്രേരണ പ്രഭാവം?"),
        ("Excise", "ഉത്പാദന നികുതി"),
        ("കorporat നികുതി", "കോർപ്പറേറ്റ് നികുതി"),
        ("പ retrogressive", "പിൻഗാമി"),
        ("Appropriation Bill?", "ചെലവ് അനുമതി ബിൽ?"),
        ("Appropriation Bill മാത്രം", "ചെലവ് അനുമതി ബിൽ മാത്രം"),
        ("ധനകാര്യ multiplier?", "ധനകാര്യ ഗുണകം?"),
        ("Consolidated Fund?", "സംയുക്ത നിധി?"),
        ("Public Account?", "പൊതു അക്കൗണ്ട്?"),
        ("Contingency മാത്രം", "അ contingencies മാത്രം"),
        ("Contingency Fund", "അ contingencies Fund"),
        ("proposals", "നിർദ്ദേശങ്ങൾ"),
        ("അ unforeseen ചെലവ്", "അപ്രതീക്ഷിത ചെലവ്"),
    ]
    for stem, ans, wrong, diff in rows:
        for a, b in reps:
            stem, ans = stem.replace(a, b), ans.replace(a, b)
            wrong = [w.replace(a, b) for w in wrong]
        out.append((stem, ans, wrong, diff))
    return out


def fix_inflation(rows: list) -> list:
    out = []
    for stem, ans, wrong, diff in rows:
        stem = re.sub(r"[\u0400-\u04FF]", "", stem)
        ans = (
            ans.replace("ഇrosion", "ചുരുക്ക")
            .replace("നാമinal", "നാമമാത്ര")
            .replace("игнor", " игнor")
        )
        ans = re.sub(r"[\u0400-\u04FF]", "", ans)
        wrong = [
            re.sub(r"[\u0400-\u04FF]", "", w.replace("നാമinal", "നാമമാത്ര"))
            for w in wrong
        ]
        if "ചുരുക്ക" in ans and "ചെയ്യുന്നത്" in stem:
            pass
        if stem.endswith("പണപ്പെരുപ്പം ചുരുക്ക ചെയ്യുന്നത്?"):
            stem = "പണപ്പെരുപ്പം ചുരുക്കുന്നത്?"
        if "നാമമാത്ര −" in ans or "നാമinal" in ans:
            ans = ans.replace("നാമinal −", "നാമമാത്ര −")
        if " игнor" in ans:
            ans = ans.replace(" игнor", " игнor")
        out.append((stem, ans, wrong, diff))
    return out


def main() -> None:
    text = GEN.read_text(encoding="utf-8")

    old_load = """    reforms: list[Fact] = []
    for stem, ans, wrong, diff in mod.REFORMS_1991:
        ans = ans.replace("സ്വകാര്യ സECTOR-ൽ", "സ്വകാര്യ മേഖലയിൽ")
        wrong = [w.replace("സ്വകാര്യ സECTOR-ൽ", "സ്വകാര്യ മേഖലയിൽ") for w in wrong]
        reforms.append((stem, ans, wrong, diff))"""
    new_load = """    reforms: list[Fact] = []
    for stem, ans, wrong, diff in mod.REFORMS_1991:
        def _fix(s: str) -> str:
            s = s.replace("സ്വകാര്യ സECTOR-ൽ", "സ്വകാര്യ മേഖലയിൽ")
            s = s.replace("സ്വകാര്യ സECTOR", "സ്വകാര്യ മേഖല")
            s = s.replace("സ്വകാര്യ മേഖലയിൽ-ൽ", "സ്വകാര്യ മേഖലയിൽ")
            return s
        reforms.append((_fix(stem), _fix(ans), [_fix(w) for w in wrong], diff))"""
    if old_load not in text:
        raise SystemExit("_load_existing block not found")
    text = text.replace(old_load, new_load)

    spec = importlib.util.spec_from_file_location("mlb", ROOT / "_build_eco_ml_block.py")
    mlb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mlb)

    cats = {
        "KERALA_ECONOMY": mlb.KERALA_ECONOMY,
        "MICROECONOMICS": mlb.MICROECONOMICS,
        "MARKET_STRUCTURES": mlb.MARKET_STRUCTURES,
        "INFLATION_CYCLES": fix_inflation(mlb.INFLATION_CYCLES),
        "FISCAL_DEFICIT": fix_fiscal(mlb.FISCAL_DEFICIT),
    }
    for name, rows in cats.items():
        text = replace_cat(text, name, emit_facts(name, rows))
        print(f"patched {name} ({len(rows)} facts)")

    # type hints in write_output
    text = text.replace('f"{name}: list = "', 'f"{name}: list[Fact] = "')
    for pair in ("INTL_HQ", "AGRI_INST", "INSURANCE_INST"):
        text = text.replace(f"{pair}: list[Fact]", f"{pair}: list[Pair]")
    text = text.replace("ECONOMIC_THINKER_TRIPLES: list[Fact]", "ECONOMIC_THINKER_TRIPLES: list[Triple]")

    GEN.write_text(text, encoding="utf-8")
    print(f"Wrote {GEN}")


if __name__ == "__main__":
    main()
