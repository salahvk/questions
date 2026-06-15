#!/usr/bin/env python3
"""Generate indian_industries_wave30_facts.py — verified Malayalam PSC facts."""
from __future__ import annotations

import importlib.util
import pprint
import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "indian_industries_wave30_facts.py"
BLR = "ബെംഗളൂuru"

spec = importlib.util.spec_from_file_location("bii", ROOT / "_build_indian_industries_wave30.py")
bii = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bii)

META = [(m[0], m[2], m[3]) for m in bii.CATEGORY_META]


def build_data() -> dict[str, list[tuple[str, str]]]:
    d: dict[str, list[tuple[str, str]]] = dict(bii.DATA)

    psus = [
        ("BHEL", "വിദ്യുത് ഉപകരണങ്ങൾ", "ന്യൂ ഡൽഹി"),
        ("HAL", "വൈമാനിക/പ്രതിരോധം", BLR),
        ("SAIL", "ഉരുക്ക്", "ന്യൂ ഡൽഹി"),
        ("ONGC", "എണ്ണ-ഗ്യാസ് പര്യവേക്ഷണം", "ന്യൂ ഡൽഹി"),
        ("NTPC", "വിദ്യുത് ഉൽപ്പാദനം", "ന്യൂ ഡൽഹി"),
        ("IOCL", "എണ്ണ ശുദ്ധീകരണം", "ന്യൂ ഡൽഹി"),
        ("Coal India", "കൽക്കരി ഖനനം", "കൊൽക്കത്ത"),
        ("GAIL", "പ്രകൃതി വാതകം", "ന്യൂ ഡൽഹി"),
        ("NHPC", "ജൽവിദ്യുത്", "ഫരീദാബാദ്"),
        ("BEL", "പ്രതിരോധ ഇൽക്ട്രോണിക്സ്", BLR),
        ("BEML", "ഭാരമുള്ള ഉപകരണങ്ങൾ", BLR),
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
        ("ITI", "ടെൽകോം ഉപകരണങ്ങൾ", BLR),
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

    d["MSME_CATEGORY"] = [
        ("മൈക്രോ എന്റർപ്രൈസ്", "നിക്ഷേപം ₹1 കോടി വരെ"),
        ("സ്മോൾ എന്റർപ്രൈസ്", "നിക്ഷേപം ₹10 കോടി വരെ"),
        ("മീഡിയം എന്റർപ്രൈസ്", "നിക്ഷേപം ₹50 കോടി വരെ"),
        ("മൈക്രോ എന്റർപ്രൈസ്", "വിറ്റുവരവ് ₹5 കോടി വരെ"),
        ("സ്മോൾ എന്റർപ്രൈസ്", "വിറ്റുവരവ് ₹50 കോടി വരെ"),
        ("മീഡിയം എന്റർപ്രൈസ്", "വിറ്റുവരവ് ₹250 കോടി വരെ"),
        ("എം.എസ്.എം.ഇ", "2020 പരിഷ്കരണം"),
        ("എം.എസ്.എം.ഇ", "നിക്ഷേപവും വിറ്റുവരവും അടിസ്ഥാനം"),
        ("ഉദ്യമി", "ഒറ്റ ഉടമസ്ഥൻ/പാർട്ണർഷിപ്പ്"),
        ("ചെറുകിട വ്യവസായി", "50 തൊഴിലാളികൾ വരെ"),
        ("വില്ലേജ് എന്റർപ്രൈസ്", "ഗ്രാമീണ മേഖള"),
        ("കുടീര വ്യവസായി", "വീട്ടുവഴി നിർമ്മാണം"),
        ("എം.എസ്.എം.ഇ", "GDP-യിൽ 30% സംഭാവന"),
        ("എം.എസ്.എം.ഇ", "കയറ്റുമതിയിൽ 45%"),
        ("എം.എസ്.എം.ഇ", "തൊഴിലിൽ 11 കോടി+"),
        ("എം.എസ്.എം.ഇ", "6.3 കോടി യൂണിറ്റുകൾ"),
        ("എം.എസ്.എം.ഇ", "Udyam പോർട്ടൽ"),
        ("Udyam", "2020 രജിസ്ട്രേഷൻ"),
        ("ZED സർട്ടിഫിക്കേഷൻ", "ഗുണനിലവാര മേമ്പാട്"),
        ("ചെറുകിട വ്യവസായി", "₹1 കോടി നിക്ഷേപ പരിധി"),
        ("എം.എസ്.എം.ഇ", "കൈമാറ്റ വിലയിരുത്തൽ അടിസ്ഥാനം"),
        ("എം.എസ്.എം.ഇ", "സേവന മേഖള ഉൾപ്പെടുന്നു"),
        ("എം.എസ്.എം.ഇ", "വ്യാപാര മേഖള ഉൾപ്പെടുന്നു"),
        ("എം.എസ്.എം.ഇ", "നിർമ്മാണ മേഖള ഉൾപ്പെടുന്നു"),
        ("എം.എസ്.എം.ഇ", "MSME Development Act 2006"),
        ("എം.എസ്.എം.ഇ", "2020 ഭേദഗതി"),
        ("മൈക്രോ എന്റർപ്രൈസ്", "ചെറിയ നിക്ഷേപം"),
        ("സ്മോൾ എന്റർപ്രൈസ്", "ഇടത്തരം നിക്ഷേപം"),
        ("മീഡിയം എന്റർപ്രൈസ്", "വеликая നിക്ഷേപം"),
        ("എം.എസ്.എം.ഇ", "ആധുനികീകരണം & സാങ്കേതികവിദ്യ"),
    ]

    # remaining categories loaded from part2
    from _ii_data_part2 import fill_rest  # noqa: WPS433

    fill_rest(d, BLR)
    return d


def build_direct() -> list:
    from _ii_data_part2 import DIRECT_FACTS  # noqa: WPS433

    return DIRECT_FACTS


def write_module(data: dict, direct: list) -> None:
    lines = [bii.HEADER]
    for var, rows in data.items():
        lines.append(f"{var}: list[tuple[str, str]] = {pprint.pformat(rows, width=120)}\n\n")
    lines.append(f"DIRECT_FACTS: list = {pprint.pformat(direct, width=120)}\n\n")
    emit = []
    for var, fwd, rev in META:
        eng = ", english=True" if var == "ABBREVIATIONS" else ""
        emit.append(
            f"    emit_category(out, existing, rng, {var},\n"
            f"        {fwd!r},\n        {rev!r},\n"
            f"        [a for a, _ in {var}], [b for _, b in {var}]{eng})"
        )
    body = "\n\n".join(emit)
    lines.append(
        f"\ndef generate_wave30_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:\n"
        f"    out: list[Candidate] = []\n\n{body}\n\n"
        f"    emit_direct(out, existing, rng, DIRECT_FACTS, english=True)\n"
        f"    return out\n\n\n"
        f'if __name__ == "__main__":\n'
        f"    print(len(generate_wave30_candidates(set(), random.Random(0))))\n"
    )
    OUT.write_text("".join(lines), encoding="utf-8")


def main() -> None:
    data = build_data()
    direct = build_direct()
    missing = [m[0] for m in META if m[0] not in data]
    if missing:
        sys.exit(f"Missing categories: {missing}")
    write_module(data, direct)
    spec2 = importlib.util.spec_from_file_location("outmod", OUT)
    mod = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(mod)
    n = len(mod.generate_wave30_candidates(set(), random.Random(0)))
    print(f"Wrote {OUT} — {n} candidates")
    if n < 800:
        sys.exit(f"Only {n} candidates (need 800+)")


if __name__ == "__main__":
    main()
