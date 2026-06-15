#!/usr/bin/env python3
"""Translate remaining English economics categories to Malayalam and patch generator."""
from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
GEN = ROOT / "_gen_build_economics_wave20_data.py"
PATCH_DATA = ROOT / "_eco_ml_patch_data.py"

# Malayalam phrase replacements (longest first)
PHRASES: list[tuple[str, str]] = sorted([
    ("minimum support price", "കാർഷിക ധനസഹായ വില"),
    ("food grain procurement storage", "ഭക്ഷ്യധാന്യ സംഭരണം"),
    ("food grain procurement", "ഭക്ഷ്യധാന്യ സംഭരണം"),
    ("agriculture rural development", "ഗ്രാമീണ വികസന ധനസഹായം"),
    ("regulated agricultural markets", "നിയന്ത്രിത കാർഷിക വിപണികൾ"),
    ("unified national agricultural market", "ഏകീകൃത ദേശീയ കാർഷിക വിപzeni"),
    ("unified agricultural market", "ഏകീകൃത കാർഷിക വിപzeni"),
    ("farmer income support", "കർഷക വരുമാന സഹായം"),
    ("income support to farmers", "കർഷകർക്ക് വരുമാന സഹായം"),
    ("crop loss insurance", "വിള നഷ്ട ഇൻഷുറൻസ്"),
    ("crop insurance", "വിള ഇൻഷുറൻസ്"),
    ("food security", "ഭക്ഷ്യ സുരക്ഷ"),
    ("subsidized food to poor", "ദരിദ്രർക്ക് subsidized ഭക്ഷണം"),
    ("public distribution system", "പൊതു_vitaraണ_vyavastha"),
    ("FCI restructuring", "FCI പുനഃഘടന"),
    ("pre-agreed price quantity", "മുൻകൂട്ടി നിശ്ചയിച്ച വില-അളവ്"),
    ("contract farming", "കരാർ കൃഷി"),
    ("equitable land distribution", "സമത്വപൂർവ്വ ഭൂമി_vitaraണം"),
    ("land reforms objective", "ഭൂമി reforms"),
    ("drip sprinkler efficiency", "തുള്ളി-സ്പ്രിംക്ലർ കാര്യക്ഷമത"),
    ("micro irrigation", "മൈക്രോ_jalasechanam"),
    ("Kisan Credit Card", "കിസാൻ ക്രെഡിറ്റ് കാർഡ്"),
    ("every 5 years", "അഞ്ച് വർഷം"),
    ("agricultural census frequency", "കാർഷിക സെൻസസ് ആvrittam"),
    ("farmer cultivated land", "കർഷകൻ കൃഷി ചെയ്യുന്ന ഭൂമി"),
    ("operational holding", "പ്രവർത്തന_hold"),
    ("Commission for Agricultural Costs and Prices", "കാർഷിക ചെലവ്-വില കമ്മീഷൻ"),
    ("agricultural costs prices", "കാർഷിക ചെലവ്-വില"),
    ("supply shock food items", "ഭക്ഷ്യ വസ്തു_supply ഞെട്ടൽ"),
    ("food inflation driver", "ഭക്ഷ്യ പണppeരുപ്പത്തിന്റെ കാരണം"),
    ("subsidies domestic support", "സബ്സിഡി-ആഭ്യന്തര പിന്തുണ"),
    ("low input farming", "കുറഞ്ഞ ഇൻപുട്ട് കൃഷി"),
    ("zero budget natural farming", "പൂജ്യ ബജറ്റ് പ്രകൃതി കൃഷി"),
    ("organic farming standards", "ജൈവ കൃഷി മാനദണ്ഡം"),
    ("NPOP standards", "NPOP മാനദണ്ഡങ്ങൾ"),
    ("dairy meat infrastructure", "പാൽ-മാംസ അടിസ്ഥാന_saukyam"),
    ("liberalize export agri products", "കാർഷിക ഉൽപ്പന്ന കayttumati liberalize"),
    ("agricultural export policy", "കാർഷിക കayttumati നയം"),
    ("nutri cereals initiative", "പോഷക cereals"),
    ("millets promotion", "മില്ലറ്റ് പ്രോത്സാഹനം"),
    ("100 days wage employment", "100 ദിവസം വേതന തൊഴിൽ"),
    ("industrial employment", "വ്യവസായ തൊഴിൽ"),
    ("urban only", "നഗരം മാത്രം"),
    ("export promotion", "കayttumati പ്രോത്സാഹനം"),
    ("unemployed divided by labour force", "തൊഴിൽരഹിതർ ÷ തൊഴിലാളി_balam"),
    ("employed plus unemployed seeking work", "തൊഴിലുണ്ട് + തൊഴിൽ തേടുന്നവർ"),
    ("marginal productivity zero", "അതിർത്തി ഉൽപ്പാദനം പൂജ്യം"),
    ("skill mismatch", "കഴിവ്_parityavastha"),
    ("business cycle downturn", "വ്യാപാര ചക്ര_mandham"),
    ("job search transition", "തൊഴിൽ തിരയൽ_marupadi"),
    ("off season agriculture", "കാർഷിക_off-season"),
    ("wage floor for workers", "തൊഴിലാളികൾക്ക് കനിഷ്ഠ വേതനം"),
    ("industrial relations disputes", "വ്യവസായ ബന്ധ_vivadangal"),
    ("worker safety conditions", "തൊഴിലാളി സുരക്ഷ"),
    ("Employees Provident Fund", "തൊഴിലാളി ഭവിഷ്യ നിധി"),
    ("Employees State Insurance", "തൊഴിലാളി സംസ്ഥാന ഇൻഷുറൻസ്"),
    ("securities market regulation", "ഓഹരി_vipani നിയന്ത്രണം"),
    ("new securities issue", "പുതിയ ഓഹരി_vipani"),
    ("existing securities trade", "നിലവിലുള്ള ഓഹരി_kayattam"),
    ("initial public offering", "ആദ്യ പൊതു_vipani"),
    ("follow on public offering", "തുടർ_ppublic_vipani"),
    ("electronic securities form", "electronic ഓഹരി_rupam"),
    ("insurance sector regulation", "ഇൻഷുറൻസ് നിയന്ത്രണം"),
    ("life insurance", "ജീവൻ ഇൻഷുറൻസ്"),
    ("National Pension System", "പെൻഷൻ"),
    ("pension system", "പെൻഷൻ"),
    ("provident fund", "ഭവിഷ്യ നിധി"),
    ("insurance regulation", "ഇൻഷുറൻസ് നിയന്ത്രണം"),
    ("reinsurance", "പുനര_insurance"),
    ("special economic zone", "special economic zone"),  # keep SEZ acronym context
    ("export promotion investment", "കayttumati പ്രോത്സാഹനവും നിക്ഷേപവും"),
    ("manufacturing incentive", "നിർമ്മാണ_prerana"),
    ("financial inclusion bank accounts", "സാമ്പത്തിക ഉൾപ്പെടുത്തൽ ബാങ്ക് അക്കൗണ്ടുകൾ"),
    ("direct benefit transfer", "നേരിട്ടുള്ള ആനുകൂല്യ_kayattam"),
], key=lambda x: -len(x[0]))

STEM_MAP: list[tuple[str, str]] = sorted([
    ("MSP-ന്റെ പൂർണ്ണ രൂപം?", "MSP-ന്റെ പൂർണ്ണ രൂപം?"),
    ("MSP-യുടെ ലക്ഷ്യം?", "MSP-യുടെ ലക്ഷ്യം?"),
    ("green revolution-ന്റെ പ്രധാന ഫലം?", "പച്ച വിപ്ലവത്തിന്റെ പ്രധാന ഫലം?"),
    ("white revolution?", "വെള്ള വിപ്ലവം?"),
    ("blue revolution?", "നീല വിപ്ലവം?"),
    ("yellow revolution?", "മഞ്ഞ വിപ്ലവം?"),
    ("National Food Security Act year?", "ദേശീയ ഭക്ഷ്യ സുരക്ഷാ നിയമം?"),
    ("shanta Kumar committee?", "ശാന്ത കുമാർ കമ്മitee?"),
    ("MGNREGA legal guarantee year?", "MGNREGA നിയമപര ضمان വർഷം?"),
    ("unemployment rate definition?", "തൊഴിൽരഹിതര നിരക്ക്_vyakhyaa?"),
    ("labour force?", "തൊഴിലാളി_balam?"),
    ("disguised unemployment?", "മറഞ്ഞ_tozhil_rhitham?"),
    ("structural unemployment?", "ഘടനാപരമായ_tozhil_rhitham?"),
    ("cyclical unemployment?", "ചക്രാത്മക_tozhil_rhitham?"),
    ("frictional unemployment?", "ഘർഷണ_tozhil_rhitham?"),
    ("seasonal unemployment?", "കാലിക_tozhil_rhitham?"),
    ("minimum wages act objective?", "കനിഷ്ഠ വേതന നിയമത്തിന്റെ ലക്ഷ്യം?"),
    ("Industrial Disputes Act?", "വ്യവസായ_vivadangal നിയമം?"),
    ("Factories Act?", "ഫാക്ടറി നിയമം?"),
    ("SEBI established year?", "SEBI സ്ഥാപിത വർഷം?"),
    ("primary market?", "പ്രാഥമിക_vipani?"),
    ("secondary market?", "ദ്വിതീയ_vipani?"),
    ("IPO?", "IPO?"),
    ("FPO?", "FPO?"),
    ("LIC established year?", "LIC സ്ഥാപിത വർഷം?"),
    ("IRDAI established year?", "IRDAI സ്ഥാപിത വർഷം?"),
    ("life insurance?", "ജീവൻ ഇൻഷുറൻസ്?"),
    ("general insurance?", "പൊതു ഇൻഷുറൻസ്?"),
    ("NPS?", "NPS?"),
    ("SEZ-ന്റെ പൂർണ്ണ രൂപം?", "SEZ-ന്റെ പൂർണ്ണ രൂപം?"),
    ("GST launch date India?", "GST ആരംഭ തീയതി?"),
    ("UPI launched by?", "UPI ആരംഭിച്ചത്?"),
    ("NPCI full form?", "NPCI-യുടെ പൂർണ്ണ രൂപം?"),
    ("Digital India launch year?", "ഡിജിറ്റൽ ഇന്ത്യ ആരംഭ വർഷം?"),
    ("PMJDY objective?", "PMJDY-യുടെ ലക്ഷ്യം?"),
    ("comparative advantage theory?", "താരതമ്യ_meladvantage സിദ്ധാന്തം?"),
    ("invisible hand concept?", "അദൃശ്യ_kai ആശയം?"),
    ("Indian economist Nobel?", "ഇന്ത്യൻ സാമ്പത്തിക Nobel?", "),
], key=lambda x: -len(x[0]))


def translate_text(s: str) -> str:
    for eng, ml in PHRASES:
        s = s.replace(eng, ml)
    return s


def extract_list(name: str, src: str) -> list:
    m = re.search(rf"{name}: list\[Fact\] = \[(.*?)\n\]", src, re.S)
    if not m:
        m = re.search(rf"{name}: list\[Pair\] = \[(.*?)\n\]", src, re.S)
    if not m:
        m = re.search(rf"{name}: list\[Triple\] = \[(.*?)\n\]", src, re.S)
    if not m:
        raise ValueError(f"Cannot find {name}")
    body = "[" + m.group(1) + "]"
    return ast.literal_eval(body)


def emit_facts(name: str, rows: list) -> str:
    lines = [f"\n{name}: list[Fact] = ["]
    for stem, ans, wrong, diff in rows:
        stem = translate_text(stem)
        ans = translate_text(ans)
        wrong = [translate_text(w) for w in wrong]
        lines.append(f'    _f({stem!r}, {ans!r}, {wrong!r}, {diff!r}),')
    lines.append("]")
    return "\n".join(lines)


def emit_pairs(name: str, rows: list) -> str:
    pairs = {
        "MSP": "കാർഷിക ധനസഹായ വില",
        "FCI": "ഭക്ഷ്യധാന്യ സംഭരണം",
        "NABARD": "ഗ്രാമീണ വികസന ധനസഹായം",
        "APMC": "നിയന്ത്രിത കാർഷിക വിപzeni",
        "e-NAM": "ഏകീകൃത കാർഷിക വിപzeni",
        "PM-KISAN": "കർഷക വരുമാന സഹായം",
        "PMFBY": "വിള ഇൻഷുറൻസ്",
        "CACP": "കാർഷിക ചെലവ്-വില",
        "KCC": "കിസാൻ ക്രെഡിറ്റ് കാർഡ്",
        "NPOP": "ജൈവ കൃഷി മാനദണ്ഡം",
        "LIC": "ജീവൻ ഇൻഷുറൻസ്",
        "IRDAI": "ഇൻഷുറൻസ് നിയന്ത്രണം",
        "EPFO": "തൊഴിലാളി ഭവിഷ്യ നിധി",
        "NPS": "പെൻഷൻ",
        "PFRDA": "പെൻഷൻ നിയന്ത്രണം",
        "PMJJBY": "ജീവൻ ഇൻഷുറൻസ് പദ്ധതി",
        "PMSBY": "അപകട ഇൻഷുറൻസ് പദ്ധതി",
        "PMJAY": "ആരോഗ്യ ഇൻഷുറൻസ് പദ്ധതി",
        "GIC": "പുനര_insurance",
        "ULIP": "യൂണിറ്റ് ബന്ധിത ഇൻഷുറൻസ്",
    }
    lines = [f"\n{name}: list[Pair] = ["]
    for a, _b in rows:
        b = pairs.get(a, translate_text(_b))
        lines.append(f"    ({a!r}, {b!r}),")
    lines.append("]")
    return "\n".join(lines)


if __name__ == "__main__":
    src = GEN.read_text(encoding="utf-8")
    names = [
        "AGRICULTURE_FOOD", "LABOUR_EMPLOYMENT", "CAPITAL_MARKETS", "INSURANCE_PENSION",
        "ECONOMIC_THINKERS", "THINKER_EXTRA", "INDUSTRIAL_SEZ", "PUBLIC_FINANCE_TAX", "DIGITAL_CONSUMER",
    ]
    block = ""
    for n in names:
        rows = extract_list(n, src)
        block += emit_facts(n, rows)
    block += emit_pairs("AGRI_INST", extract_list("AGRI_INST", src))
    block += emit_pairs("INSURANCE_INST", extract_list("INSURANCE_INST", src))
    print("Generated block length", len(block))
