# -*- coding: utf-8 -*-
"""Complete data + writer for indian_industries_wave30_facts.py"""
from __future__ import annotations
import pprint, random, sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "indian_industries_wave30_facts.py"

# Import base from build script
import importlib.util
spec = importlib.util.spec_from_file_location("bii", ROOT / "_build_indian_industries_wave30.py")
bii = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bii)

HEADER = bii.HEADER
EMIT_FOOTER = bii.EMIT_FOOTER
CATEGORY_META = bii.CATEGORY_META
DATA = dict(bii.DATA)

PSUS = [
    ("BHEL", "വിദ്യുത് ഉപകരണങ്ങൾ", "ന്യൂ ഡൽഹി"),
    ("HAL", "വൈമാനിക/പ്രതിരോധം", "ബെംഗളൂരു"),
    ("SAIL", "ഉരുക്ക്", "ന്യൂ ഡൽഹി"),
    ("ONGC", "എണ്ണ-ഗ്യാസ് പര്യവേക്ഷണം", "ന്യൂ ഡൽഹി"),
    ("NTPC", "വിദ്യുത് ഉൽപ്പാദനം", "ന്യൂ ഡൽഹി"),
    ("IOCL", "എണ്ണ ശുദ്ധീകരണം", "ന്യൂ ഡൽഹി"),
    ("Coal India", "കൽക്കരി ഖനനം", "കൊൽക്കത്ത"),
    ("GAIL", "പ്രകൃതി വാതകം", "ന്യൂ ഡൽഹി"),
    ("NHPC", "ജൽവിദ്യുത്", "ഫരീദാബാദ്"),
    ("BEL", "പ്രതിരോധ ഇൽക്ട്രോണിക്സ്", "ബെംഗളൂuru"),
    ("BEML", "ഭാരമുള്ള ഉപകരണങ്ങൾ", "ബെംഗളൂuru"),
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
    ("ITI", "ടെൽകോം ഉപകരണങ്ങൾ", "ബെംഗളൂuru"),
    ("MTNL", "ടെൽകോം", "ന്യൂ ഡൽഹി"),
    ("BSNL", "ടെൽകോം", "ന്യൂ ഡൽഹി"),
    ("Cochin Shipyard", "കപ്പൽ നിർമ്മാണം", "കൊച്ചി"),
    ("Mazagon Dock", "കപ്പൽ/സബ്‌മറീൻ", "മുംബൈ"),
    ("GRSE", "യുദ്ധക്കപ്പൽ", "കൊൽക്കത്ത"),
    ("Goa Shipyard", "കപ്പൽ നിർമ്മാണം", "വാസ്കോ"),
    ("Hindustan Shipyard", "കപ്പൽ നിർമ്മാണം", "വിശാഖപട്ടണം"),
    ("BDL", "Guided missiles", "ഹൈദരാബാദ്"),
]
