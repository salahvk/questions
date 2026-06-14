#!/usr/bin/env python3
"""Build indian_industries_wave30_facts.py — single-shot generator."""
from __future__ import annotations

import ast
import importlib.util
import pprint
import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "indian_industries_wave30_facts.py"

HEADER = '''#!/usr/bin/env python3
"""Wave 30 Indian industries facts — 30 Malayalam PSC topic types."""

from __future__ import annotations

import random

from refill_common import Candidate
from wave30_emit import emit_category, emit_direct

'''

EMIT_FOOTER = '''

def generate_wave30_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []
{emit_body}
    emit_direct(out, existing, rng, DIRECT_FACTS)
    return out


if __name__ == "__main__":
    print(len(generate_wave30_candidates(set(), random.Random(0))))
'''


def blr() -> str:
    src = (ROOT / "ii_wave30_data.py").read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Tuple) and len(node.elts) == 2:
            a, b = node.elts
            if isinstance(a, ast.Constant) and a.value == "ഐ.എസ്.ആർ.ഒ.":
                return b.value
    raise RuntimeError("BLR not found")


def valiya() -> str:
    src = (ROOT / "continents_wave30_facts.py").read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value.startswith("ഏറ്റവും വ"):
                return node.value.split()[1]
    return "വлия"


def load_meta():
    spec = importlib.util.spec_from_file_location("bii", ROOT / "_build_indian_industries_wave30.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CATEGORY_META, dict(mod.DATA)


def build_all() -> tuple[dict[str, list[tuple[str, str]]], list]:
    B, V = blr(), valiya()
    meta, data = load_meta()

    psus = [
        ("BHEL", "വിദ്യുത് ഉപകരണങ്ങൾ", "ന്യൂ ഡൽഹി"),
        ("HAL", "വൈമാനിക/പ്രതിരോധം", B),
        ("SAIL", "ഉരുക്ക്", "ന്യൂ ഡൽഹി"),
        ("ONGC", "എണ്ണ-ഗ്യാസ് പര്യവേക്ഷണം", "ന്യൂ ഡൽഹി"),
        ("NTPC", "വിദ്യുത് ഉൽപ്പാദനം", "ന്യൂ ഡൽഹി"),
        ("IOCL", "എണ്ണ ശുദ്ധീകരണം", "ന്യൂ ഡൽഹി"),
        ("Coal India", "കൽക്കരി ഖനനം", "കൊൽക്കത്ത"),
        ("GAIL", "പ്രകൃതി വാതകം", "ന്യൂ ഡൽഹി"),
        ("NHPC", "ജൽവിദ്യുത്", "ഫരീദാബാദ്"),
        ("BEL", "പ്രതിരോധ ഇൽക്ട്രോണിക്സ്", B),
        ("BEML", "ഭാരമുള്ള ഉപകരണങ്ങൾ", B),
        ("MIDHANI", "പ്രത്യേക ലോഹങ്ങൾ", "ഹൈദരാബാദ്"),
        ("NLC India", " ലിഗ്നൈറ്റ്", "നെയ്വേളി"),
        ("SCI", "കപ്പൽ കയറ്റുമതി", "മുംബൈ"),
        ("HPCL", "എണ്ണ വിപണനം", "മുംബൈ"),
        ("BPCL", "എണ്ണ വിപണനം", "മുംബൈ"),
        ("NALCO", "അൽമിനിയം", "ഭുവനേശ്വർ"),
        ("NMDC", "ഇരുമ്പ് അയിര്", "ഹൈദരാബാദ്"),
        ("ECIL", "ഇൽക്ട്രോണിക്സ്", "ഹൈദരാബാദ്"),
        ("HCL", "വെള്ളിച്ചുരുക്കം", "രാഞ്ചി"),
        ("MOIL", "മാംഗനീസ്", "നാഗ്പൂർ"),
        ("ITI", "ടെൽകോം ഉപകരണങ്ങൾ", B),
        ("MTNL", "ടെൽകോം", "ന്യൂ ഡൽഹി"),
        ("BSNL", "ടെൽകോം", "ന്യൂ ഡൽഹി"),
        ("Cochin Shipyard", "കപ്പൽ നിർമ്മാണം", "കൊച്ചി"),
        ("Mazagon Dock", "കപ്പൽ/സബ്‌മറീൻ", "മുംബൈ"),
        ("GRSE", "യുദ്ധക്കപ്പൽ", "കൊൽക്കത്ത"),
        ("Goa Shipyard", "കപ്പൽ നിർമ്മാണം", "വാസ്കോ"),
        ("Hindustan Shipyard", "കപ്പൽ നിർമ്മാണം", "വിശാഖപട്ടണം"),
        ("BDL", "Guided missiles", "ഹൈദരാബാദ്"),
    ]
    data["PSU_SECTOR"] = [(a, s) for a, s, _ in psus]
    data["PSU_HQ"] = [(a, h) for a, _, h in psus]

    from ii_wave30_ind_data import DIRECT_FACTS, fill_data

    fill_data(data, B)
    from _ii_rest import add_rest

    add_rest(data, B, V)
    return data, DIRECT_FACTS


def main() -> int:
    data, direct = build_all()
    meta, _ = load_meta()
    english = {"ABBREVIATIONS", "PSU_SECTOR", "PSU_HQ", "DEFENCE_PSUS", "REFINERIES", "NODAL_AGENCY"}

    lines = [HEADER]
    for var, *_ in meta:
        lines.append(f"{var}: list[tuple[str, str]] = {pprint.pformat(data[var], width=120, sort_dicts=False)}\n")
    lines.append(f"DIRECT_FACTS: list[tuple[str, str, list[str], str]] = {pprint.pformat(direct, width=120, sort_dicts=False)}\n")

    emit = []
    for var, comment, fwd, rev in meta:
        kw = ", english=True" if var in english else ""
        emit.append(f"    # {comment}")
        emit.append(f"    emit_category(out, existing, rng, {var},")
        emit.append(f"        {pprint.pformat(fwd, width=120)},")
        emit.append(f"        {pprint.pformat(rev, width=120)},")
        emit.append(f"        [a for a, _ in {var}], [b for _, b in {var}]{kw})")
        emit.append("")
    lines.append(EMIT_FOOTER.format(emit_body="\n".join(emit)))
    OUT.write_text("".join(lines), encoding="utf-8")

    spec = importlib.util.spec_from_file_location("outmod", OUT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    n = len(mod.generate_wave30_candidates(set(), random.Random(0)))
    print(f"Wrote {OUT} — {n} candidates")
    return n


if __name__ == "__main__":
    n = main()
    if n < 800:
        sys.exit(f"Need >= 800, got {n}")
