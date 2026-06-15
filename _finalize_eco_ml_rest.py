#!/usr/bin/env python3
"""Write complete validated _gen_economics_ml_rest.py."""
from __future__ import annotations

import re
import sys
from pathlib import Path

OUT = Path(__file__).parent / "_gen_economics_ml_rest.py"

ALLOWED = re.compile(
    r"\b(RBI|SEBI|GST|IMF|WTO|CPI|GDP|FDI|FII|HDI|MSP|NPS|UPI|NPCI|FRBM|SEZ|PLI|PMJDY|"
    r"FCI|NABARD|APMC|PMFBY|CACP|KCC|NPOP|EPFO|ESIC|PMKVY|PLFS|NSDL|CDSL|"
    r"IPO|FPO|ETF|QIP|ADR|GDR|LIC|IRDAI|ULIP|PFRDA|PMJJBY|PMSBY|PMJAY|GIC|"
    r"CCI|STPI|EOU|CGST|SGST|IGST|GSTN|CBDT|CBIC|GAAR|DTAA|UIDAI|DBT|OCEN|ONDC|"
    r"PMKISAN)\b",
    re.I,
)
LATIN4 = re.compile(r"[a-zA-Z]{4,}")
E, M, H = "ലളിതം", "മധ്യം", "കഠിനം"

HEADER = '''"""Remaining categories for economics_wave20_ml_data.py generation."""
from __future__ import annotations

Fact = tuple[str, str, list[str], str]
Pair = tuple[str, str]
Triple = tuple[str, str, str]

'''

LABOUR_EMPLOYMENT = [
    ("മഹാത്മാ ഗാന്ധി ദേശീയ ഗ്രാമീണ തൊഴിൽ പദ്ധതിയുടെ ലക്ഷ്യം?", "100 ദിവസം വേതന തൊഴിൽ", ["വ്യവസായ തൊഴിൽ", "നഗരം മാത്രം", "കയറ്റുമതി പ്രോത്സാഹനം"], M),
    ("മഹാത്മാ ഗാന്ധി ദേശീയ ഗ്രാമീണ തൊഴിൽ നിയമപര ഉറപ്പ് വർഷം?", "2005", ["1991", "2015", "1980"], H),
    ("തൊഴിൽരഹിതര നിരക്ക്?", "തൊഴിൽരഹിതർ ÷ തൊഴിൽശക്തി", ["ജനസംഖ്യ ÷", "GDP ÷", "വ്യാപാര ÷"], M),
    ("തൊഴിൽശക്തി?", "തൊഴിലുണ്ട് + തൊഴിൽ തേടുന്നവർ", ["കുട്ടികൾ മാത്രം", "വിരമിച്ചവർ മാത്രം", "വിദ്യാർത്ഥികൾ മാത്രം"], M),
    ("മറഞ്ഞിരിക്കുന്ന തൊഴിൽരഹിതി?", "അതിർത്തി ഉൽപ്പാദനം പൂജ്യം", ["പൂർണ്ണ തൊഴിൽ", "ഘടനാപരം മാത്രം", "ചക്രീയം മാത്രം"], H),
    ("ഘടനാപര തൊഴിൽരഹിതി?", "കഴിവ് പൊരുത്തക്കേട്", ["കാലികം മാത്രം", "ഘർഷണം മാത്രം", "സ്വമനസ്സാലുള്ളത് മാത്രം"], M),
    ("ചക്രീയ തൊഴിൽരഹിതി?", "വ്യാപാര ചക്ര മന്ദം", ["സാങ്കേതിക മാറ്റം", "കാർഷിക ഒഴിച്ക്കൽ കാലം", "വിരമണം"], M),
    ("ഘർഷണ തൊഴിൽരഹിതി?", "തൊഴിൽ തിരയൽ മാറ്റം", ["സ്ഥിരമായ പിരിച്ചുവിടൽ", "കഴിവ് കാലഹരണം", "മന്ദം"], M),
    ("കാലിക തൊഴിൽരഹിതി?", "കാർഷിക ഒഴിച്ക്കൽ കാലം", ["സാങ്കേതിക മാറ്റം", "മന്ദം", "കഴിവ് പൊരുത്തക്കേട്"], M),
    ("കനിഷ്ഠ വേതന നിയമത്തിന്റെ ലക്ഷ്യം?", "തൊഴിലാളികൾക്ക് വേതന കനിഷ്ഠം", ["വസ്തു വില പരമാവധി", "പലിശ കനിഷ്ഠം", "കയറ്റുമതി കനിഷ്ഠം"], M),
    ("വ്യവസായ തർക്ക നിയമം?", "വ്യവസായ ബന്ധവും തർക്കങ്ങളും", ["കാർഷികം മാത്രം", "വിദേശ വ്യാപാരം", "നാണയ നയം"], H),
    ("ഫാക്ടറി നിയമം?", "തൊഴിലാളി സുരക്ഷയും അവസ്ഥകളും", ["വ്യാപാര നയം", "നാണയ നയം", "വിദേശ നയം"], H),
    ("EPFO-യുടെ പൂർണ്ണരൂപം?", "തൊഴിലാളി ഭവിഷ്യ നിധി", ["തൊഴിലുടമ പെൻഷൻ", "കയറ്റുമതി പ്രോത്സാഹന നിധി", "അടിയന്തര നിധി"], M),
    ("ESIC-യുടെ പൂർണ്ണരൂപം?", "തൊഴിലാളി സംസ്ഥാന ഇൻഷുറൻസ്", ["തൊഴിലുടമ ഓഹരി ഇൻഷുറൻസ്", "കയറ്റുമതി ഇൻഷുറൻസ്", "അടിയന്തര ഇൻ shutil"], M),
]

# Fix ESIC typo before continuing - use proper Malayalam in final
