#!/usr/bin/env python3
"""Generate indian_industries_wave30_facts.py."""
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


def load_meta() -> list[tuple[str, str, list[str], list[str]]]:
    spec = importlib.util.spec_from_file_location("bii", ROOT / "_build_indian_industries_wave30.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CATEGORY_META


def load_starter_data() -> dict:
    spec = importlib.util.spec_from_file_location("bii", ROOT / "_build_indian_industries_wave30.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return dict(mod.DATA)


def all_data() -> dict[str, list[tuple[str, str]]]:
    B = blr()
    d = load_starter_data()

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
    d["PSU_SECTOR"] = [(a, s) for a, s, _ in psus]
    d["PSU_HQ"] = [(a, h) for a, _, h in psus]

    # Import remaining from data module
    from ii_wave30_ind_data import fill_data, DIRECT_FACTS  # noqa: F401

    fill_data(d, B)
    return d


DIRECT_FACTS: list[tuple[str, str, list[str], str]] = []  # set by ii_wave30_ind_data


def write_output() -> int:
    from ii_wave30_ind_data import DIRECT_FACTS as DF, fill_data

    B = blr()
    data = load_starter_data()
    fill_data(data, B)

    meta = load_meta()
    english_cats = {"ABBREVIATIONS", "PSU_SECTOR", "PSU_HQ", "DEFENCE_PSUS"}

    lines = [HEADER]
    for var, _comment, _fwd, _rev in meta:
        rows = data[var]
        lines.append(f"{var}: list[tuple[str, str]] = {pprint.pformat(rows, width=120, sort_dicts=False)}\n")

    lines.append(f"DIRECT_FACTS: list[tuple[str, str, list[str], str]] = {pprint.pformat(DF, width=120, sort_dicts=False)}\n")

    emit_lines = []
    for var, comment, fwd, rev in meta:
        kw = ", english=True" if var in english_cats else ""
        emit_lines.append(f"    # {comment}")
        emit_lines.append(f"    emit_category(out, existing, rng, {var},")
        emit_lines.append(f"        {pprint.pformat(fwd, width=120)},")
        emit_lines.append(f"        {pprint.pformat(rev, width=120)},")
        emit_lines.append(f"        [a for a, _ in {var}], [b for _, b in {var}]{kw})")
        emit_lines.append("")

    body = EMIT_FOOTER.format(emit_body="\n".join(emit_lines))
    lines.append(body)
    OUT.write_text("".join(lines), encoding="utf-8")

    spec = importlib.util.spec_from_file_location("outmod", OUT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    count = len(mod.generate_wave30_candidates(set(), random.Random(0)))
    return count


if __name__ == "__main__":
    n = write_output()
    print(f"Wrote {OUT} with {n} candidates")
    if n < 800:
        sys.exit(f"Need >= 800, got {n}")
