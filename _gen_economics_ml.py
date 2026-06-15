#!/usr/bin/env python3
"""Generate economics_wave20_ml_data.py."""
from __future__ import annotations

import ast
import re
from pathlib import Path

OUT = Path(__file__).parent / "economics_wave20_ml_data.py"

HEADER = '''#!/usr/bin/env python3
"""Pure Malayalam PSC economics facts — wave 20 ML categories."""

from __future__ import annotations

Fact = tuple[str, str, list[str], str]
Pair = tuple[str, str]
Triple = tuple[str, str, str]

'''

ALLOWED = re.compile(
    r"\b(RBI|SEBI|GST|IMF|WTO|CPI|GDP|FDI|FII|HDI|MSP|NPS|UPI|NPCI|FRBM|SEZ|PLI|PMJDY|"
    r"FCI|NABARD|APMC|PMFBY|CACP|KCC|NPOP|ICAR|NAFED|EPFO|ESIC|PMKVY|PLFS|NSDL|CDSL|"
    r"IPO|FPO|ETF|QIP|ADR|GDR|LIC|IRDAI|ULIP|PFRDA|PMJJBY|PMSBY|PMJAY|GIC|"
    r"CCI|STPI|EOU|CGST|SGST|IGST|GSTN|CBDT|CBIC|GAAR|DTAA|UIDAI|DBT|OCEN|ONDC|"
    r"PMKISAN|PM-KISAN|e-NAM|APY|KISAN)\b",
    re.I,
)
LATIN4 = re.compile(r"[a-zA-Z]{4,}")


def check_ml(blob: str) -> None:
    stripped = ALLOWED.sub("", blob)
    for tok in ("easy", "medium", "hard"):
        stripped = stripped.replace(tok, "")
    if LATIN4.search(stripped):
        raise ValueError(f"English leak: {LATIN4.search(stripped).group()} in {blob[:80]}")


def emit(name: str, hint: str, rows: list) -> str:
    for row in rows:
        check_ml(" ".join(str(x) for x in row))
    lines = [f"{name}: list[{hint}] = ["]
    for row in rows:
        lines.append(f"    {row!r},")
    lines.append("]")
    return "\n".join(lines) + "\n\n"


AGRICULTURE_FOOD = [
    ("MSP-ന്റെ പൂർണ്ണ രൂപം?", "കാർഷിക ധനസഹായ വില", ["പരമാവധി വിൽപ്പന വില", "വിപണി സഹായ വില", "കനിഷ്ഠ വിൽപ്പന ഉൽപ്പന്നം"], "easy"),
    ("MSP നിശ്ചയിക്കുന്നത്?", "കേന്ദ്ര സർക്കാർ", ["RBI", "SEBI", "WTO"], "medium"),
    ("MSP-യുടെ ലക്ഷ്യം?", "കർഷകർക്ക് കനിഷ്ഠ വില", ["ഉപഭോക്തൃ സബ്സിഡി മാത്രം", "കയറ്റുമതി നിരോധനം", "ഇറക്കുമതി നിരോധനം"], "medium"),
    ("FCI-യുടെ പ്രധാന കർത്തവ്യം?", "ഭക്ഷ്യധാന്യ സംഭരണം", ["നാണയ നയം", "ഓഹരി വിപണി", "ഇൻഷുറൻസ്"], "medium"),
    ("പച്ച വിപ്ലവത്തിന്റെ പ്രധാന ഫലം?", "ഭക്ഷ്യധാന്യ ഉൽപ്പാദന വർദ്ധന", ["വ്യവസായ കുറവ്", "വ്യാപാര നിരോധനം", "വില കുറവ്"], "medium"),
    ("വെള്ള വിപ്ലവം?", "പാൽ ഉൽപ്പാദന വർദ്ധന", ["ഗോതമ്പ് വർദ്ധന", "അരി വർദ്ധന", "പരുത്തി വർദ്ധന"], "medium"),
    ("നീല വിപ്ലവം?", "മത്സ്യ വികസനം", ["പാൽ വികസനം", "ഗോതമ്പ് വികസനം", "പരുത്തി വികസനം"], "medium"),
    ("മഞ്ഞ വിപ്ലവം?", "എണ്ണയുരുക്കൾ ഉൽപ്പാദനം", ["പാൽ ഉൽപ്പാദനം", "മത്സ്യ ഉൽപ്പാദനം", "ഗോതമ്പ് ഉൽപ്പാദനം"], "hard"),
    ("NABARD-ന്റെ പ്രധാന മേഖല?", "ഗ്രാമീണ വികസന ധനസഹായം", ["മൂലധന വിപണി", "ഇൻഷുറൻസ്", "വിദേശ വ്യാപാരം"], "medium"),
    ("APMC-ന്റെ പ്രധാന വ്യവസ്ഥ?", "നിയന്ത്രിത കാർഷിക വിപണികൾ", ["ഓഹരി വിപണി", "നാണയ വിപണി", "ഇൻഷുറൻസ് വിപണി"], "hard"),
    ("e-NAM-ന്റെ ലക്ഷ്യം?", "ഏകീകൃത ദേശീയ കാർഷിക വിപണി", ["കയറ്റുമതി നിരോധനം", "MSP നീക്കം", "സ്വകാര്യ ഏകാധിപത്യം"], "medium"),
    ("PM-KISAN-ന്റെ ലക്ഷ്യം?", "കർഷകർക്ക് വരുമാന സഹായം", ["നഗര തൊഴിൽ", "വ്യവസായ സബ്സിഡി", "കയറ്റുമതി സബ്സിഡി"], "medium"),
    ("PMFBY-യുടെ ലക്ഷ്യം?", "വിള നഷ്ട ഇൻഷുറൻസ്", ["ആരോഗ്യ ഇൻഷുറൻസ്", "ജീവൻ ഇൻഷുറൻസ്", "വാഹന ഇൻഷുറൻസ്"], "medium"),
    ("ബഫർ സ്റ്റോക്കിന്റെ ലക്ഷ്യം?", "ഭക്ഷ്യ സുരക്ഷ", ["കയറ്റുമതി മാത്രം", "വില വർദ്ധന", "ഇറക്കുമതി നിരോധനം"], "medium"),
    ("പൊതുവിതരണ വ്യവസ്ഥയുടെ ലക്ഷ്യം?", "ദരിദ്രർക്ക് ചെലവുകുറഞ്ഞ ഭക്ഷണം", ["ആഡംബര വസ്തുക്കൾ", "മൂലധന വസ്തുക്കൾ", "കയറ്റുമതി മാത്രം"], "easy"),
    ("ദേശീയ ഭക്ഷ്യ സുരക്ഷാ നിയമം?", "2013", ["2005", "1991", "2020"], "hard"),
    ("ശാന്ത കുമാർ കമ്മിറ്റി?", "FCI പുനഃഘടന", ["RBI പുനഃഘടന", "SEBI പുനഃഘടന", "GST പുനഃഘടന"], "hard"),
    ("കരാർ കൃഷി?", "മുൻകൂട്ടി നിശ്ചയിച്ച വില-അളവ്", ["സർക്കാർ ഏകാധിപത്യം", "വിലയില്ല", "കയറ്റുമതി മാത്രം"], "medium"),
    ("ഭൂമി പരിഷ്‌ക്കാരത്തിന്റെ ലക്ഷ്യം?", "സമത്വപൂർവ്വ ഭൂമി വിതരണം", ["വ്യവസായ ഏകാധിപത്യം", "നഗരവൽക്കരണം മാത്രം", "കയറ്റുമതി മാത്രം"], "medium"),
    ("മൈക്രോ ജലസേചനം?", "തുള്ളി-സ്പ്രിംക്ലർ കാര്യക്ഷമത", ["വെള്ളപ്പൊാഴ കൃഷി മാത്രം", "ജലസേചനമില്ല", "മഴ മാത്രം"], "medium"),
    ("KCC?", "കിസാൻ ക്രെഡിറ്റ് കാർഡ്", ["ഉപഭോക്തൃ വായ്പ", "കോർപ്പറേറ്റ് വായ്പ", "കയറ്റുമതി വായ്പ"], "medium"),
    ("കാർഷിക സെൻസസ് ആവൃത്തി?", "അഞ്ച് വർഷം", ["എല്ലാ വർഷവും", "പത്ത് വർഷം", "ഇരുപത് വർഷം"], "hard"),
    ("പ്രവർത്തന ഭൂമി?", "കർഷകൻ കൃഷി ചെയ്യുന്ന ഭൂമി", ["വനഭൂമി മാത്രം", "നഗര ഭൂമി", "വ്യവസായ ഭൂമി"], "hard"),
    ("CACP?", "കാർഷിക ചെലവ്-വില കമ്മീഷൻ", ["മൂലധന വിപണി ബോർഡ്", "ഇൻഷുറൻസ് ബോർഡ്", "വ്യാപാര ബോർഡ്"], "hard"),
    ("ഭക്ഷ്യ പണപ്പെരുപ്പത്തിന്റെ കാരണം?", "ഭക്ഷ്യ വസ്തു വിതരണ ഞെട്ടൽ", ["മൂലധന ചോർച്ച", "ഓഹരി വിപണി", "SEBI നയം"], "medium"),
    ("WTO കാർഷിക കരാർ പ്രശ്നം?", "സബ്സിഡി-ആഭ്യന്തര പിന്തുണ", ["നാണയ നയം", "മൂലധന വിപണി", "ഇൻഷുറൻസ്"], "hard"),
    ("പൂജ്യ ബജറ്റ് പ്രകൃതി കൃഷി?", "കുറഞ്ഞ ഇൻപുട്ട് കൃഷി", ["ഉയർന്ന രാസ ഇൻപുട്ട്", "വ്യവസായ കൃഷി മാത്രം", "ഖനനം"], "hard"),
    ("ജൈവ കൃഷി സാക്ഷ്യപ്പെടുത്തൽ?", "NPOP മാനദണ്ഡങ്ങൾ", ["SEBI മാനദണ്ഡം", "RBI മാനദണ്ഡം", "GST മാനദണ്ഡം"], "hard"),
    ("പശു-മാംസ അടിസ്ഥാന സൗകര്യ നിധി?", "പാൽ-മാംസ അടിസ്ഥാന സൗകര്യം", ["ഓഹരി വിപണി", "നാണയ വിപണി", "ഭൂമി വിപണി"], "hard"),
    ("കാർഷിക കയറ്റുമതി നയം?", "കാർഷിക ഉൽപ്പന്ന കയറ്റുമതി സ്വതന്ത്രമാക്കൽ", ["എല്ലാ കയറ്റുമതി നിരോധനം", "എല്ലാ ഇറക്കുമതി നിരോധനം", "വ്യാപാരമില്ല"], "medium"),
    ("മില്ലറ്റ് പ്രോത്സാഹനം?", "പോഷക ധാന്യങ്ങൾ", ["പെട്രോളിയം പ്രോത്സാഹനം", "കോൽ പ്രോത്സാഹനം", "ഇരുമ്പ് പ്രോത്സാഹനം"], "medium"),
]

AGRI_INST = [
    ("MSP", "കാർഷിക ധനസഹായ വില"),
    ("FCI", "ഭക്ഷ്യധാന്യ സംഭരണം"),
    ("NABARD", "ഗ്രാമീണ വികസന ധനസഹായം"),
    ("APMC", "നിയന്ത്രിത കാർഷിക വിപണികൾ"),
    ("e-NAM", "ഏകീകൃത കാർഷിക വിപണി"),
    ("PM-KISAN", "കർഷക വരുമാന സഹായം"),
    ("PMFBY", "വിള ഇൻഷുറൻസ്"),
    ("CACP", "കാർഷിക ചെലവ്-വില"),
    ("KCC", "കിസാൻ ക്രെഡിറ്റ് കാർഡ്"),
    ("NPOP", "ജൈവ കൃഷി മാനദണ്ഡം"),
]

# Continue in part 2 - imported at runtime
from _gen_economics_ml_rest import (  # noqa: E402
    CAPITAL_MARKETS,
    DIGITAL_CONSUMER,
    ECONOMIC_THINKERS,
    ECONOMIC_THINKER_TRIPLES,
    INDUSTRIAL_SEZ,
    INSURANCE_INST,
    INSURANCE_PENSION,
    LABOUR_EMPLOYMENT,
    PUBLIC_FINANCE_TAX,
    THINKER_EXTRA,
)

SECTIONS = [
    ("AGRICULTURE_FOOD", "Fact", AGRICULTURE_FOOD),
    ("AGRI_INST", "Pair", AGRI_INST),
    ("LABOUR_EMPLOYMENT", "Fact", LABOUR_EMPLOYMENT),
    ("CAPITAL_MARKETS", "Fact", CAPITAL_MARKETS),
    ("INSURANCE_PENSION", "Fact", INSURANCE_PENSION),
    ("INSURANCE_INST", "Pair", INSURANCE_INST),
    ("ECONOMIC_THINKERS", "Fact", ECONOMIC_THINKERS),
    ("THINKER_EXTRA", "Fact", THINKER_EXTRA),
    ("ECONOMIC_THINKER_TRIPLES", "Triple", ECONOMIC_THINKER_TRIPLES),
    ("INDUSTRIAL_SEZ", "Fact", INDUSTRIAL_SEZ),
    ("PUBLIC_FINANCE_TAX", "Fact", PUBLIC_FINANCE_TAX),
    ("DIGITAL_CONSUMER", "Fact", DIGITAL_CONSUMER),
]


def main() -> None:
    parts = [HEADER]
    stems: set[str] = set()
    for name, hint, rows in SECTIONS:
        if hint == "Fact":
            for stem, ans, wrong, _ in rows:
                if stem in stems:
                    raise ValueError(f"dup stem: {stem}")
                stems.add(stem)
                if len(wrong) != 3 or len(set(wrong)) != 3 or ans in wrong:
                    raise ValueError(stem)
        parts.append(emit(name, hint, rows))
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.read_text().count(chr(10))+1} lines)")
    for name, hint, rows in SECTIONS:
        print(f"  {name}: {len(rows)}")


if __name__ == "__main__":
    main()
