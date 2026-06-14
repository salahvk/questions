#!/usr/bin/env python3
"""Append tail categories to _gen_economics_ml_rest.py using unicode-safe strings."""
from __future__ import annotations

import pprint
from pathlib import Path

INS = "\u0d07\u0d7b\u0d37\u0d41\u0d31\u0d3e\u0d7b\u0d38"  # ഇൻഷുറൻസ്

REST = Path(__file__).parent / "_gen_economics_ml_rest.py"

INSURANCE_INST = [
    ("LIC", f"ജീവൻ {INS}"),
    ("IRDAI", f"{INS} നിയന്ത്രണം"),
    ("EPFO", "തൊഴിലാളി ഭവിഷ്യ നിധി"),
    ("NPS", "ദേശീയ പെൻഷൻ"),
    ("PFRDA", "പെൻഷൻ നിയന്ത്രണം"),
    ("PMJJBY", f"ജീവൻ {INS} പദ്ധതി"),
    ("PMSBY", f"അപകട {INS} പദ്ധതി"),
    ("PMJAY", f"ആരോഗ്യ {INS} പദ്ധതി"),
    ("GIC", "പുനരിശ്വാസന"),
    ("ULIP", f"യൂണിറ്റ് ലിങ്ക് {INS}"),
    ("PMFBY", f"വിള {INS}"),
    ("APY", "അatal പENSION"),
]

ECONOMIC_THINKERS = [
    ("ആഡം സ്മിത്ത്", "ദേശത്തിന്റെ സമ്പദ്‌വിത്തം", "ശാസ്ത്രീയ സാമ്പത്തികശാസ്ത്രം"),
    ("കാൾ മാർക്സ്", "മൂലധനം", "മാർക്സിയൻ സാമ്പത്തികശാസ്ത്രം"),
    ("ജോൺ മെയിൻാർഡ് കെയ്ൻസ്", "പൊതു സിദ്ധാന്തം", "ചോദനാധിഷ്ഠിത സാമ്പത്തികശാസ്ത്രം"),
    ("ഡേവിഡ് റിക്കാർഡോ", "താരതമ്യ മേന്മ", "വ്യാപാര സിദ്ധാന്തം"),
    ("ആൽഫ്രഡ് മാർഷൽ", "സാമ്പത്തികശാസ്ത്രത്തിന്റെ തത്വങ്ങൾ", "ഭാഗിക സമതുല്യം"),
    ("മിൽട്ടൺ ഫ്രീഡ്മാൻ", "നാണയവാദം", "നാണയ നയം"),
    ("അമർത്യ സെൻ", "വികസനം സ്വാതന്ത്ര്യമായി", "സാമർത്ഥ്യ സമീപനം"),
    ("പി. സി. മഹാലനോബിസ്", "മഹാലനോബിസ് മാതൃക", "ഭാരമേറിയ വ്യവസായം"),
    ("തോമസ് മാൽത്തസ്", "ജനസംഖ്യാ സിദ്ധാന്തം", "ഭക്ഷ്യ പരിമിതി"),
    ("ജോസഫ് ഷംപീറ്റർ", "സർജനാവകാശ നശിപ്പ്", "നവീകരണ സിദ്ധാന്തം"),
    ("ഇർവിംഗ് ഫിഷർ", "ഫിഷർ സമവാക്യം", "പലിശ-പണപ്പെരുപ്പം"),
    ("വിൽഫ്രെഡോ പരേറ്റോ", "പരേറ്റോ കാര്യക്ഷമത", "ക്ഷേമ സാമ്പത്തികശാസ്ത്രം"),
]

THINKER_EXTRA = [
    ("ഇന്ത്യയിലെ സാമ്പത്തികശാസ്ത്ര നൊബൽ?", "അമർത്യ സെൻ", ["രഘുരാം രാജൻ", "മന്മോഹൻ സിംഗ്", "വിജയ് കേൽക്കർ"], "medium"),
    ("വികസനം സ്വാതന്ത്ര്യമായി രചിച്ചത്?", "അമർത്യ സെൻ", ["ആഡം സ്മിത്ത്", "കാൾ മാർക്സ്", "ജോൺ മെയിൻാർഡ് കെയ്ൻസ്"], "hard"),
    ("ഗാന്ധിയൻ സാമ്പത്തിക ചിന്ത?", "സ്വadeshi ഗ്രാമ ekonomi", ["ഭാരമേറിയ വ്യവസായം മാത്രം", "വidesh dependence", "monopoly capital"], "medium"),
]

def emit(name: str, hint: str, rows: list) -> str:
    return f"{name}: list[{hint}] = {pprint.pformat(rows, width=120, sort_dicts=False)}\n"

def main() -> None:
    text = REST.read_text(encoding="utf-8")
    text = text.replace("അatal പENSION", "അatal പENSION")
    text = text.replace('("അatal പENSION യോജന?",', '("അatal പENSION യോജന?",')
    if "INSURANCE_INST:" in text:
        print("Tail already present")
        return
    parts = [
        emit("INSURANCE_INST", "Pair", INSURANCE_INST),
        emit("ECONOMIC_THINKERS", "Triple", ECONOMIC_THINKERS),
        emit("THINKER_EXTRA", "Fact", THINKER_EXTRA),
    ]
    REST.write_text(text.rstrip() + "\n\n" + "".join(parts), encoding="utf-8")
    print("Appended partial tail to", REST)

if __name__ == "__main__":
    main()
