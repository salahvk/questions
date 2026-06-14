#!/usr/bin/env python3
"""One-shot writer for build_economics_wave20_data.py — pure Malayalam facts."""

from __future__ import annotations

import importlib.util
import pprint
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "build_economics_wave20_data.py"
SRC = OUT

Fact = tuple[str, str, list[str], str]
Pair = tuple[str, str]
Triple = tuple[str, str, str]

BANNED = [
    re.compile(r"സൂചിപ്പിക്കുന്ന പ്രവർത്തി"),
    re.compile(r"^ബാങ്കിംഗ് സേവനങ്ങളിൽ"),
]

HEADER = '''#!/usr/bin/env python3
"""Verified economics facts for 20 PSC topic categories — wave 20 expansion."""

from __future__ import annotations

# Fact = (stem, answer, [wrong×3], difficulty)
Fact = tuple[str, str, list[str], str]
Pair = tuple[str, str]
Triple = tuple[str, str, str]


def _facts() -> dict[str, list[Fact]]:
    """Return 20 category lists; each category targets ~25–35 unique stems."""
    return {
        "macro_indicators": MACRO_INDICATORS,
        "rbi_monetary": RBI_MONETARY,
        "plans_niti": PLANS_NITI,
        "reforms_1991": REFORMS_1991,
        "finance_commission": FINANCE_COMMISSION,
        "bop_trade": BOP_TRADE,
        "intl_institutions": INTL_INSTITUTIONS,
        "kerala_economy": KERALA_ECONOMY,
        "microeconomics": MICROECONOMICS,
        "market_structures": MARKET_STRUCTURES,
        "inflation_cycles": INFLATION_CYCLES,
        "fiscal_deficit": FISCAL_DEFICIT,
        "agriculture_food": AGRICULTURE_FOOD,
        "labour_employment": LABOUR_EMPLOYMENT,
        "capital_markets": CAPITAL_MARKETS,
        "insurance_pension": INSURANCE_PENSION,
        "economic_thinkers": THINKER_EXTRA,
        "industrial_sez": INDUSTRIAL_SEZ,
        "public_finance_tax": PUBLIC_FINANCE_TAX,
        "digital_consumer": DIGITAL_CONSUMER,
    }


'''


def _load_first_four() -> tuple[list[Fact], list[Fact], list[Fact], list[Fact]]:
    spec = importlib.util.spec_from_file_location("_eco_src", SRC)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SRC}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    reforms: list[Fact] = []
    for stem, ans, wrong, diff in mod.REFORMS_1991:
        def _fix(s: str) -> str:
            s = s.replace("സ്വകാര്യ സECTOR-ൽ", "സ്വകാര്യ മേഖലയിൽ")
            s = s.replace("സ്വകാര്യ സECTOR", "സ്വകാര്യ മേഖല")
            s = s.replace("സ്വകാര്യ മേഖലയിൽ-ൽ", "സ്വകാര്യ മേഖലയിൽ")
            return s
        reforms.append((_fix(stem), _fix(ans), [_fix(w) for w in wrong], diff))
    return mod.MACRO_INDICATORS, mod.RBI_MONETARY, mod.PLANS_NITI, reforms


FINANCE_COMMISSION: list[Fact] = [
    ("ധനകമ്മിഷൻ ഭരണഘടനയുടെ ഏത് അനുച്ഛേദത്തിന് കീഴിലാണ്?", "അനുച്ഛേദം 280", ["അനുച്ഛേദം 281", "അനുച്ഛേദം 282", "അനുച്ഛേദം 279"], "medium"),
    ("ധനകമ്മിഷൻ രൂപീകരിക്കുന്നത് ആരാണ്?", "രാഷ്ട്രപതി", ["പ്രധാനമന്ത്രി", "ധനകാര്യ മന്ത്രി", "പാർലമെന്റ്"], "medium"),
    ("ധനകമ്മിഷന്റെ പ്രധാന കർത്തവ്യം ഏത്?", "കേന്ദ്ര-സംസ്ഥാന നികുതി വിതരണം ശുപാർശ ചെയ്യൽ", ["നാണയ നിരക്ക് നിശ്ചയം", "വ്യാപാര നയം നിർണ്ണയം", "ബജറ്റ് തയ്യാറാക്കൽ"], "medium"),
    ("ലംബ വിതരണം (vertical devolution) എന്നാൽ?", "കേന്ദ്ര-സംസ്ഥാന നികുതി വിഹിതം", ["സംസ്ഥാനങ്ങൾക്കിടയിലെ വിഹിതം", "പഞ്ചായത്ത് നികുതി", "കസ്റ്റംസ് തീരുവ"], "medium"),
    ("തിരശ്ചീന വിതരണം (horizontal devolution) എന്നാൽ?", "സംസ്ഥാനങ്ങൾക്കിടയിലെ നികുതി വിഹിതം", ["കേന്ദ്ര-സംസ്ഥാന വിഹിതം", "വിദേശ വ്യാപാര വിഹിതം", "GST വിഹിതം മാത്രം"], "hard"),
    ("ഇന്ത്യയിലെ ആദ്യത്തെ ധനകമ്മിഷൻ നിയമിച്ച വർഷം?", "1951", ["1950", "1952", "1947"], "hard"),
    ("15-ാം ധനകമ്മിഷന്റെ കാലാവധി?", "2021-26", ["2015-20", "2020-25", "2026-31"], "medium"),
    ("15-ാം ധനകമ്മിഷന്റെ ചെയർമാൻ ആരാണ്?", "എൻ.കെ. സിംഗ്", ["വിജയ് കേൽക്കർ", "യ.V. റെഡ്ഡി", "സി. രംഗരാജൻ"], "hard"),
    ("14-ാം ധനകമ്മിഷന്റെ കാലാവധി?", "2015-20", ["2010-15", "2020-25", "2005-10"], "medium"),
    ("14-ാം ധനകമ്മിഷന്റെ ചെയർമാൻ ആരായിരുന്നു?", "യ.V. റെഡ്ഡി", ["എൻ.കെ. സിംഗ്", "വിജയ് കേൽക്കർ", "സി. രംഗരാജൻ"], "hard"),
    ("13-ാം ധനകമ്മിഷന്റെ ചെയർമാൻ ആരായിരുന്നു?", "വിജയ് എൽ. കേൽക്കർ", ["എൻ.കെ. സിംഗ്", "യ.V. റെഡ്ഡി", "സി. രംഗരാജൻ"], "hard"),
    ("12-ാം ധനകമ്മിഷന്റെ ചെയർമാൻ ആരായിരുന്നു?", "സി. രംഗരാജൻ", ["യ.V. റെഡ്ഡി", "എൻ.കെ. സിംഗ്", "വിജയ് കേൽക്കർ"], "hard"),
    ("11-ാം ധനകമ്മിഷന്റെ ചെയർമാൻ ആരായിരുന്നു?", "എ.എം. അഹമദി", ["എൻ.കെ. സിംഗ്", "കെ.സി. പന്ത്", "വിജയ് കേൽക്കർ"], "hard"),
    ("10-ാം ധനകമ്മിഷന്റെ ചെയർമാൻ ആരായിരുന്നു?", "കെ.സി. പന്ത്", ["എൻ.കെ. സിംഗ്", "യ.V. റെഡ്ഡി", "സി. രംഗരാജൻ"], "hard"),
    ("ധനകമ്മിഷൻ ശുപാർശകൾ സംബന്ധിച്ച അനുച്ഛേദം?", "അനുച്ഛേദം 281", ["അനുച്ഛേദം 280", "അനുച്ഛേദം 282", "അനുച്ഛേദം 279"], "hard"),
    ("ധനകമ്മിഷൻ ഏത് തരം സ്ഥാപനമാണ്?", "ഭരണഘടനാ സ്ഥാപനം", ["സ്ഥാപിത നിയമ സ്ഥാപനം", "സ്വയംഭരണ സ്ഥാപനം", "സ്വകാര്യ സ്ഥാപനം"], "medium"),
    ("ധനകമ്മിഷൻ എത്ര വർഷം കൂടുമ്പോൾ നിയമിക്കപ്പെടുന്നു?", "അഞ്ച്", ["പത്ത്", "മൂന്ന്", "ഏഴ്"], "medium"),
    ("ധനകമ്മിഷൻ ശുപാർശകൾക്ക് നിയമപരമായ ബാധ്യത?", "പാർലമെന്റ് പരിഗണിക്കേണ്ടത്", ["നിർബന്ധിതമായി നടപ്പാക്കേണ്ടത്", "RBI അംഗീകരിക്കേണ്ടത്", "SEBI അംഗീകരിക്കേണ്ടത്"], "hard"),
    ("സംസ്ഥാനങ്ങൾക്ക് കേന്ദ്ര നികുതി വിതരണം ശുപാർശ ചെയ്യുന്നത്?", "ധനകമ്മിഷൻ", ["നീതി ആയോഗ്", "RBI", "SEBI"], "easy"),
    ("പഞ്ചായത്തുകൾക്കും നഗരസഭകൾക്കുമുള്ള നികുതി വിതരണം ശുപാർശ ചെയ്യുന്നത്?", "ധനകമ്മിഷൻ", ["പ്ലാനിംഗ് കമ്മീഷൻ", "ഇലക്ഷൻ കമ്മീഷൻ", "UGC"], "medium"),
    ("15-ാം ധനകമ്മിഷൻ കേന്ദ്ര-സംസ്ഥാന വിതരണത്തിന് ശുപാർശ നൽകിയ ശതമാനം?", "41%", ["42%", "32%", "50%"], "hard"),
    ("വിജയ് കേൽക്കർ ഏത് ധനകമ്മിഷന്റെ ചെയർമാനായിരുന്നു?", "13-ാം", ["15-ാം", "14-ാം", "10-ാം"], "hard"),
    ("യ.V. റെഡ്ഡി ഏത് ധനകമ്മിഷന്റെ ചെയർമാനായിരുന്നു?", "14-ാം", ["11-ാം", "15-ാം", "13-ാം"], "hard"),
    ("സി. രംഗരാജൻ ഏത് ധനകമ്മിഷന്റെ ചെയർമാനായിരുന്നു?", "12-ാം", ["15-ാം", "14-ാം", "10-ാം"], "hard"),
    ("ധനകമ്മിഷൻ ഗ്രാന്റ്-ഇൻ-എയ്ഡ് ശുപാർശകൾ ഏതിനാണ്?", "സംസ്ഥാനങ്ങൾക്കും പ്രാദേശിക സ്ഥാപനങ്ങൾക്കും", ["കേന്ദ്ര സർക്കാർ മാത്രം", "സ്വകാര്യ കമ്പനികൾ", "വിദേശ സർക്കാർ"], "medium"),
    ("ധനകമ്മിഷന്റെ അംഗങ്ങൾ നിയമിക്കുന്നത്?", "രാഷ്ട്രപതി", ["പ്രധാനമന്ത്രി", "ധനകാര്യ മന്ത്രി", "സുപ്രീം കോർട്ട്"], "medium"),
    ("ധനകമ്മിഷൻ റിപ്പോർട്ട് സമർപ്പിക്കുന്നത്?", "രാഷ്ട്രപതിക്ക്", ["പ്രധാനമന്ത്രിക്ക്", "പാർലമെന്റിന് മാത്രം", "സംസ്ഥാനങ്ങളுக்க്"], "medium"),
    ("ആദ്യ ധനകമ്മിഷന്റെ ചെയർമാൻ ആരായിരുന്നു?", "കെ.സി. നിയോഗി", ["എൻ.കെ. സിംഗ്", "വിജയ് കേൽക്കർ", "സി. രംഗരാജൻ"], "hard"),
    ("15-ാം ധനകമ്മിഷൻ പ്രാദേശിക സ്വയംഭരണ സ്ഥാപനങ്ങൾക്ക് ശുപാർശ നൽകിയത്?", "4.11% വരുമാന പൂലി", ["10% വരുമാന പൂലി", "2% വരുമാന പൂലി", "20% വരുമാന പൂലി"], "hard"),
    ("ധനകമ്മിഷൻ കേന്ദ്ര-സംസ്ഥാന ധനകാര്യ ഫെഡറലിസത്തിന്റെ?", "പ്രധാന സംവിധാനം", ["അനുബന്ധ സംവിധാനം", "നിയമ നിർമ്മാണ സംവിധാനം", "നീതി നിർവ്വചന സംവിധാനം"], "medium"),
    ("എ.എം. അഹമദി ഏത് ധനകമ്മിഷന്റെ ചെയർമാനായിരുന്നു?", "11-ാം", ["10-ാം", "12-ാം", "14-ാം"], "hard"),
    ("കെ.സി. പന്ത് ഏത് ധനകമ്മിഷന്റെ ചെയർമാനായിരുന്നു?", "10-ാം", ["9-ാം", "11-ാം", "15-ാം"], "hard"),
    ("സംസ്ഥാനങ്ങളുടെ സാമ്പത്തിക ആവശ്യങ്ങൾ പരിഗണിക്കുന്ന ഭരണഘടനാ സംവിധാനം?", "ധനകമ്മിഷൻ", ["സുപ്രീം കോർട്ട്", "ഇലക്ഷൻ കമ്മീഷൻ", "UGC"], "easy"),
]

BOP_TRADE: list[Fact] = [
    ("വിദേശ വ്യാപാര സമതുല്യം എന്നാൽ?", "കയറ്റുമതി-ഇറക്കുമതി തുല്യത", ["വ്യാപാര കമ്മി", "വ്യാപാര മിച്ചം", "വ്യാപാര നിരോധനം"], "medium"),
    ("വ്യാപാര കമ്മി എന്നാൽ?", "ഇറക്കുമതി കയറ്റുമതിയേക്കാൾ കൂടുതൽ", ["കയറ്റുമതി കൂടുതൽ", "തുല്യം", "വ്യാപാര നിരോധനം"], "easy"),
    ("വ്യാപാര മിച്ചം എന്നാൽ?", "കയറ്റുമതി ഇറക്കുമതിയേക്കാൾ കൂടുതൽ", ["ഇറക്കുമതി കൂടുതൽ", "തുല്യം", "വ്യാപാര നിരോധനം"], "easy"),
    ("പേയ്മെന്റ് സമതുല്യം എന്നാൽ?", "ഒരു രാജ്യത്തിന്റെ അന്താരാഷ്ട്ര സാമ്പത്തിക ഇടപാടുകളുടെ രേഖ", ["കേന്ദ്ര ബജറ്റ്", "സംസ്ഥാന ബജറ്റ്", "കമ്പനി ബാലൻസ് ഷീറ്റ്"], "medium"),
    ("നിലവിൽ കണക്ക് എന്ത് ഉൾക്കൊള്ളുന്നു?", "വസ്തു-സേവന വ്യാപാരവും വരുമാന കൈമാറ്റങ്ങളും", ["കേവലം മൂലധന പ്രവാഹം", "കേവലം സർക്കാർ വായ്പ", "കേവലം നാണയ ശേഖരം"], "hard"),
    ("മൂലധന കണക്ക് എന്ത് ഉൾക്കൊള്ളുന്നു?", "FDI, FII, വായ്പാ പ്രവാഹങ്ങൾ", ["വസ്തു-സേവന വ്യാപാരം", "ചില്ലറ വ്യാപാരം", "കാർഷിക ഉൽപ്പാദനം"], "hard"),
    ("FDI (വിദേശ നേരിട്ടുള്ള നിക്ഷേപം) എന്നാൽ?", "വിദേശ സ്ഥാപനങ്ങളുടെ ദീർഘകാല നിക്ഷേപം", ["ചില്ലറ വ്യാപാരം", "കാർഷിക സബ്സിഡി", "GST ശേഖരണം"], "medium"),
    ("FII (വിദേശ സ്ഥാപന നിക്ഷേപകർ) എന്നാൽ?", "വിദേശ സ്ഥാപനങ്ങളുടെ ഓഹരി വിപണി നിക്ഷേപം", ["കാർഷിക വായ്പ", "സർക്കാർ ബോണ്ട് മാത്രം", "GST നികുതി"], "medium"),
    ("വിദേശ നാണ്യ കരുതൽ ശേഖരം നിയന്ത്രിക്കുന്നത്?", "RBI", ["SEBI", "GST കൗൺസിൽ", "നീതി ആയോഗ്"], "medium"),
    ("ഇന്ത്യയുടെ പ്രധാന കയറ്റുമതി വസ്തു?", "പെട്രോളിയം ഉൽപ്പന്നങ്ങൾ", ["ചായ", "കോഫി", "സുഗന്ധവ്യഞ്ജനങ്ങൾ"], "medium"),
    ("ഇന്ത്യയുടെ ഐടി കയറ്റുമതി പ്രധാനമായി?", "സേവന കയറ്റുമതി", ["കാർഷിക കയറ്റുമതി", "ഖനന കയറ്റുമതി", "വസ്ത്ര കയറ്റുമതി മാത്രം"], "medium"),
    ("WTO-യുടെ പ്രധാന ലക്ഷ്യം?", "അന്താരാഷ്ട്ര വ്യാപാരം സ്വതന്ത്രമാക്കൽ", ["വിനിമയ നിരക്ക് നിശ്ചയം", "വിദേശ നിക്ഷേപം നിരോധനം", "കാർഷിക നികുതി ഉയർത്തൽ"], "medium"),
    ("ഇന്ത്യ WTO-യിൽ അംഗമായി?", "1995", ["1991", "2000", "1985"], "hard"),
    ("GST-യുടെ വ്യാപാര-സാമ്പത്തിക പ്രഭാവം?", "ഇന്ത്യയിൽ ഒറ്റ വിപണി", ["വിദേശ വ്യാപാരം മാത്രം", "കാർഷിക വ്യാപാരം മാത്രം", "ഓഹരി വിപണി"], "medium"),
    ("ഇറക്കുമതി പകരക്കാരൻ നയത്തിന്റെ ലക്ഷ്യം?", "ആഭ്യന്തര ഉൽപ്പാദനം പ്രോത്സാഹിപ്പിക്കൽ", ["കയറ്റുമതി കുറയ്ക്കൽ", "FDI നിരോധനം", "വിനിമയ നിരക്ക് നിശ്ചയം"], "medium"),
    ("നാണയ മൂല്യനിർണ്ണയത്തിന്റെ വ്യാപാര ഫലം?", "കയറ്റുമതി പ്രോത്സാഹനം", ["കയറ്റുമതി കുറവ്", "ഇറക്കുമതി കുറവ്", "വ്യാപാര മിച്ചം കുറവ്"], "medium"),
    ("താരതമ്യ മേന്മയുടെ ആശയകർത്താവ്?", "ഡേവിഡ് റിക്കാർഡോ", ["ആഡം സ്മിത്ത്", "കാൾ മാർക്സ്", "ജോൺ മെയിൻാർഡ് കെയ്ൻസ്"], "hard"),
    ("ഇന്ത്യയുടെ വ്യാപാര നയത്തിന്റെ പ്രധാന മന്ത്രാലയം?", "വാണിജ്യ മന്ത്രാലയം", ["RBI", "SEBI", "IRDAI"], "easy"),
    ("EXIM ബാങ്കിന്റെ പ്രധാന ലക്ഷ്യം?", "കയറ്റുമതി-ഇറക്കുമതി ധനസഹായം", ["കാർഷിക വായ്പ", "ഉപഭോക്തൃ വായ്പ", "വീട് വായ്പ"], "medium"),
    ("FEMA നിയമം നടപ്പിലാക്കുന്നത്?", "RBI", ["SEBI", "ധനകാര്യ മന്ത്രാലയം", "WTO"], "medium"),
    ("ഇന്ത്യയുടെ പ്രധാന വ്യാപാര പങ്കാളി?", "അമേരിക്ക", ["ചൈന", "ജപ്പാൻ", "റഷ്യ"], "hard"),
    ("സ്വതന്ത്ര വ്യാപാര കരാറിന്റെ ലക്ഷ്യം?", "കസ്റ്റംസ് തീരുവ കുറയ്ക്കൽ", ["FDI നിരോധനം", "വിനിമയ നിരക്ക് നിശ്ചയം", "ഇറക്കുമതി നിരോധനം"], "medium"),
    ("ഇറക്കുമതി തീരുവയുടെ വ്യാപാര പ്രഭാവം?", "ഇറക്കുമതി വില ഉയർത്തൽ", ["കയറ്റുമതി വില കുറയ്ക്കൽ", "FDI വർദ്ധന", "GDP കുറവ്"], "medium"),
    ("ഇറക്കുമതി പോട്ടയുടെ വ്യാപാര പ്രഭാവം?", "ഇറക്കുമതി അളവ് പരിമിതപ്പെടുത്തൽ", ["കയറ്റുമതി പ്രോത്സാഹനം", "FDI സ്വതന്ത്രീകരണം", "നികുതി കുറവ്"], "medium"),
    ("അദൃശ്യ വ്യാപാരത്തിൽ ഉൾപ്പെടുന്നത്?", "സേവന വ്യാപാരം", ["വസ്തു വ്യാപാരം മാത്രം", "കാർഷിക വ്യാപാരം മാത്രം", "ഖനന വ്യാപാരം മാത്രം"], "medium"),
    ("നിലവിൽ കണക്ക് കമ്മിയുടെ അർത്ഥം?", "നിലവിൽ കണക്കിൽ ശുദ്ധ ഒഴുക്ക്", ["മൂലധന കണക്ക് മിച്ചം", "വ്യാപാര മിച്ചം", "ധനകാര്യ മിച്ചം"], "hard"),
    ("ഇന്ത്യയുടെ പേയ്മെന്റ് സമതുല്യ സ്ഥിതിവിവരം പ്രസിദ്ധീകരിക്കുന്നത്?", "RBI", ["ദേശീയ സ്ഥിതിവിവരക്കണക്ക് കാര്യാലയം", "SEBI", "വാണിജ്യ മന്ത്രാലയം"], "medium"),
    ("SEZ-ന്റെ വ്യാപാര ലക്ഷ്യം?", "കയറ്റുമതി പ്രോത്സാഹനം", ["ഇറക്കുമതി നിയന്ത്രണം മാത്രം", "ആഭ്യന്തര വിൽപ്പന മാത്രം", "കാർഷിക മേഖല മാത്രം"], "medium"),
    ("രൂപയുടെ മൂല്യനിർണ്ണയം കുറയുമ്പോൾ വ്യാപാര ഫലം?", "അന്താരാഷ്ട്ര വിപണിയിൽ കയറ്റുമതി വില കുറവ്", ["കയറ്റുമതി വില കൂടുതൽ", "ഇറക്കുമതി വില കുറവ്", "വ്യാപാര മിച്ചം എപ്പോഴും കുറയുന്നു"], "medium"),
    ("ഇന്ത്യയുടെ വ്യാപാര കമ്മി പ്രധാനമായും ധനസഹായം നൽകുന്നത്?", "മൂലധന പ്രവാഹവും നാണയ ശേഖരവും", ["നാണയ മുദ്രണം മാത്രം", "കാർഷിക മേഖല മാത്രം", "GST മാത്രം"], "hard"),
    ("ഇന്ത്യയുടെ പ്രധാന കാർഷിക കയറ്റുമതി?", "അരി", ["ഗോതമ്പ്", "പയർവർഗ്ഗങ്ങൾ", "ചായ മാത്രം"], "medium"),
    ("ഇന്ത്യയുടെ സോഫ്റ്റ്വെയർ കയറ്റുമതിയുടെ സ്ഥാനം?", "സേവന കയറ്റുമതിയുടെ പ്രധാന ഭാഗം", ["കാർഷിക കയറ്റുമതി", "ഖനന കയറ്റുമതി", "വസ്ത്ര മാത്രം"], "medium"),
    ("ബഹിരാക്ത വ്യാപാരം എന്നാൽ?", "രണ്ട് രാജ്യങ്ങൾക്കിടയിലെ വസ്തു-സേവന കൈമാറ്റം", ["കേന്ദ്ര ബജറ്റ് കൈമാറ്റം", "സംസ്ഥാന വായ്പ", "കമ്പനി ലാഭം"], "easy"),
    ("അന്താരാഷ്ട്ര വ്യാപാരത്തിലെ നേട്ടം?", "താരതമ്യ മേന്മയുള്ള ഉൽപ്പന്നങ്ങൾ കയറ്റുമതി", ["എല്ലാ ഉൽപ്പന്നങ്ങളും ഇറക്കുമതി", "വ്യാപാരം നിർത്തൽ", "നാണയ നിരോധനം"], "medium"),
]

# Import remaining large blocks from companion module
from _eco_wave20_ml_blocks import (  # noqa: E402
    INTL_INSTITUTIONS,
    INTL_HQ,
    KERALA_ECONOMY,
    MICROECONOMICS,
    MARKET_STRUCTURES,
    INFLATION_CYCLES,
    FISCAL_DEFICIT,
    AGRICULTURE_FOOD,
    AGRI_INST,
    LABOUR_EMPLOYMENT,
    CAPITAL_MARKETS,
    INSURANCE_PENSION,
    INSURANCE_INST,
    ECONOMIC_THINKERS,
    THINKER_EXTRA,
    ECONOMIC_THINKER_TRIPLES,
    INDUSTRIAL_SEZ,
    PUBLIC_FINANCE_TAX,
    DIGITAL_CONSUMER,
)

TYPE_HINTS: dict[str, str] = {
    "INTL_HQ": "list[Pair]",
    "AGRI_INST": "list[Pair]",
    "INSURANCE_INST": "list[Pair]",
    "ECONOMIC_THINKER_TRIPLES": "list[Triple]",
}

NEW_VARS = [
    ("FINANCE_COMMISSION", FINANCE_COMMISSION),
    ("BOP_TRADE", BOP_TRADE),
    ("INTL_INSTITUTIONS", INTL_INSTITUTIONS),
    ("INTL_HQ", INTL_HQ),
    ("KERALA_ECONOMY", KERALA_ECONOMY),
    ("MICROECONOMICS", MICROECONOMICS),
    ("MARKET_STRUCTURES", MARKET_STRUCTURES),
    ("INFLATION_CYCLES", INFLATION_CYCLES),
    ("FISCAL_DEFICIT", FISCAL_DEFICIT),
    ("AGRICULTURE_FOOD", AGRICULTURE_FOOD),
    ("AGRI_INST", AGRI_INST),
    ("LABOUR_EMPLOYMENT", LABOUR_EMPLOYMENT),
    ("CAPITAL_MARKETS", CAPITAL_MARKETS),
    ("INSURANCE_PENSION", INSURANCE_PENSION),
    ("INSURANCE_INST", INSURANCE_INST),
    ("ECONOMIC_THINKERS", ECONOMIC_THINKERS),
    ("THINKER_EXTRA", THINKER_EXTRA),
    ("ECONOMIC_THINKER_TRIPLES", ECONOMIC_THINKER_TRIPLES),
    ("INDUSTRIAL_SEZ", INDUSTRIAL_SEZ),
    ("PUBLIC_FINANCE_TAX", PUBLIC_FINANCE_TAX),
    ("DIGITAL_CONSUMER", DIGITAL_CONSUMER),
]


def validate(facts: dict[str, list[Fact]]) -> None:
    stems: set[str] = set()
    for cat, rows in facts.items():
        for stem, ans, wrong, diff in rows:
            if stem in stems:
                raise ValueError(f"Duplicate stem in {cat}: {stem[:60]}")
            stems.add(stem)
            if len(wrong) != 3:
                raise ValueError(f"Need 3 wrong options: {stem[:60]}")
            if len(set(wrong)) != 3:
                raise ValueError(f"Wrong options not distinct: {stem[:60]}")
            if ans in wrong:
                raise ValueError(f"Answer in wrong options: {stem[:60]}")
            if f"'{ans}'" in stem or f'"{ans}"' in stem:
                raise ValueError(f"Answer quoted in stem: {stem[:60]}")
            blob = stem + ans + "".join(wrong)
            for pat in BANNED:
                if pat.search(blob):
                    raise ValueError(f"Banned pattern in {cat}: {stem[:60]}")


def main() -> None:
    macro, rbi, plans, reforms = _load_first_four()
    all_facts = {
        "macro_indicators": macro,
        "rbi_monetary": rbi,
        "plans_niti": plans,
        "reforms_1991": reforms,
        "finance_commission": FINANCE_COMMISSION,
        "bop_trade": BOP_TRADE,
        "intl_institutions": INTL_INSTITUTIONS,
        "kerala_economy": KERALA_ECONOMY,
        "microeconomics": MICROECONOMICS,
        "market_structures": MARKET_STRUCTURES,
        "inflation_cycles": INFLATION_CYCLES,
        "fiscal_deficit": FISCAL_DEFICIT,
        "agriculture_food": AGRICULTURE_FOOD,
        "labour_employment": LABOUR_EMPLOYMENT,
        "capital_markets": CAPITAL_MARKETS,
        "insurance_pension": INSURANCE_PENSION,
        "economic_thinkers": THINKER_EXTRA,
        "industrial_sez": INDUSTRIAL_SEZ,
        "public_finance_tax": PUBLIC_FINANCE_TAX,
        "digital_consumer": DIGITAL_CONSUMER,
    }
    validate(all_facts)

    sections: list[str] = [HEADER]
    first_four = [
        ("MACRO_INDICATORS", macro, "1. Macroeconomic indicators & indices"),
        ("RBI_MONETARY", rbi, "2. RBI monetary policy"),
        ("PLANS_NITI", plans, "3. Five Year Plans & NITI Aayog"),
        ("REFORMS_1991", reforms, "4. 1991 economic reforms (LPG)"),
    ]
    for i, (name, val, title) in enumerate(first_four, start=1):
        sections.append("# ---------------------------------------------------------------------------\n")
        sections.append(f"# {title}\n")
        sections.append("# ---------------------------------------------------------------------------\n")
        sections.append(f"{name}: list[Fact] = ")
        sections.append(pprint.pformat(val, width=120, sort_dicts=False))
        sections.append("\n\n\n")

    for i, (name, val) in enumerate(NEW_VARS, start=5):
        hint = TYPE_HINTS.get(name, "list[Fact]")
        sections.append("# ---------------------------------------------------------------------------\n")
        sections.append(f"# {i}. {name}\n")
        sections.append("# ---------------------------------------------------------------------------\n")
        sections.append(f"{name}: {hint} = ")
        sections.append(pprint.pformat(val, width=120, sort_dicts=False))
        sections.append("\n\n\n")

    OUT.write_text("".join(sections), encoding="utf-8")
    lines = OUT.read_text(encoding="utf-8").count("\n") + 1
    total = sum(len(v) for v in all_facts.values())
    print(f"LINES={lines}")
    print(f"TOTAL_FACTS={total}")
    for cat, rows in all_facts.items():
        print(f"{cat}={len(rows)}")


if __name__ == "__main__":
    main()
