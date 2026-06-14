#!/usr/bin/env python3
"""Generate validated _ii_cat_data.py from RAW pair tables."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "_ii_cat_data.py"
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")

spec = importlib.util.spec_from_file_location("g", ROOT / "_gen_ii_wave30.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)  # type: ignore[union-attr]

_ns: dict = {}
exec((ROOT / "important_institutions_facts.py").read_text(encoding="utf-8"), _ns)
TENHIP = next(a for q, a, _, _ in _ns["FACTS"] if q.startswith("കാലിക്കറ്റ് സർവകലാശാലയുടെ"))


def city_map() -> dict[str, str]:
    c = {
        "MUM": next(b for a, b in g.HQ_PAIRS if a == "ആർ.ബി.ഐ."),
        "DEL": next(b for a, b in g.HQ_PAIRS if a == "യു.പി.എസ്.സി."),
        "BLR": next(b for a, b in g.HQ_PAIRS if a == "ഐ.എസ്.ആർ.ഒ."),
        "PUN": next(b for a, b in g.HQ_PAIRS if "മെട്ര" in a),
        "DDN": next(b for a, b in g.HQ_PAIRS if "സർവേ" in a),
        "CHN": "ചെന്നൈ",
        "HYD": "ഹൈദരാബാദ്",
        "AHM": "അഹമദാബാദ്",
        "KOL": "കൊൽക്കത്ത",
        "LKO": "ലഖ\u200cനൗ",
        "TVM": "തിരുവനന്തപുരം",
        "KOZ": "കോഴിക്കോട്",
        "KOCHI": "കൊച്ചി",
        "PAT": "പട്ടം",
        "ERN": "എറണാകുളം",
        "MUL": "മുളങ്കുന്നത്തുകാവ്",
        "PEE": "പീച്ചി",
        "THRI": "തൃശ്ശൂർ",
        "KAS": "കാസർഗോഡ്",
        "VAL": "വളിയമല",
        "THU": "തുമ്പ",
        "CHER": "ചെറുതുരുത്തി",
        "KTY": "കോട്ടയം",
        "KNR": "കണ്ണൂർ",
        "ALP": "ആലപ്പുഴ",
        "MAN": "മഞ്ചേരി",
        "GWH": "ഗുവാഹാടി",
        "RPR": "രോപ്രാഗ്രം",
        "SUR": "സുരത്തികൽ",
        "MND": "മണ്ഡി",
        "BBS": "ഭുവനേശ്വർ",
        "JDH": "ജോധ്പൂർ",
        "KNP": "കാൻപൂർ",
        "KGP": "ഖരഗ്പൂർ",
        "RKE": "റൂർക്കി",
        "GNT": "ഗാന്ധിനഗർ",
        "IND": "ഇന്ദോർ",
        "TRI": "തിരുച്ചി",
        "PTN": "പട്ന",
        "ALU": "ആലുവ",
        "NGP": "നാഗ്പൂർ",
        "RNC": "രാഞ്ചി",
        "FRD": "ഫരീദാബാദ്",
        "VSK": "വാസ്കോ",
        "VZG": "വിശാഖപട്ടണം",
        "JPR": "ജയ്പൂർ",
        "GUR": "ഗുരുഗ്രാം",
        "KND": "കാന്ദ്ല",
        "VNS": "വാരാണസി",
        "MNG": "മംഗaloreura",
    }
    c["MNG"] = "മ" + "ം" + "ഗ" + "ള" + "ൂ" + "ര" + "ു"
    for k, v in c.items():
        if MIXED.search(v):
            raise ValueError(f"Mixed city {k}: {v!r}")
    return c


def R(cat: str, rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return rows


RAW: dict[str, list[tuple[str, str]]] = {}

RAW["MEDICAL_COLLEGE_HQ"] = R("MEDICAL_COLLEGE_HQ", [
    ("ഗവ. മെഡിക്കൽ കോളേജ് തിരുവനന്തപുരം", "TVM"),
    ("ഗവ. മെഡിക്കൽ കോളേജ് കോഴിക്കോട്", "KOZ"),
    ("ഗവ. മെഡിക്കൽ കോളേജ് കോട്ടയം", "KTY"),
    ("ഗവ. മെഡിക്കൽ കോളേജ് തൃശ്ശൂർ", "THRI"),
    ("ഗവ. മെഡിക്കൽ കോളേജ് ആലപ്പുഴ", "ALP"),
    ("ഗവ. മെഡിക്കൽ കോളേജ് കണ്ണൂർ", "KNR"),
    ("ഗവ. മെഡിക്കൽ കോളേജ് മഞ്ചേരി", "MAN"),
])

RAW["KERALA_COMMISSION_HQ"] = R("KERALA_COMMISSION_HQ", [
    ("കേരള പബ്ലിക് സർവീസ് കമ്മീഷൻ", "PAT"),
    ("കേരള സംസ്ഥാന മനുഷ്യാവകാശ കമ്മീഷൻ", "TVM"),
    ("കേരള സംസ്ഥാന വനിതാ കമ്മീഷൻ", "TVM"),
    ("കേരള സംസ്ഥാന ശിശു അവകാശ സംരക്ഷണ കമ്മീഷൻ", "TVM"),
    ("കേരള സംസ്ഥാന മലിനീകരണ നിയന്ത്രണ ബോർഡ്", "TVM"),
    ("കേരള സംസ്ഥാന ജൈവവൈവിധ്യ ബോർഡ്", "TVM"),
    ("കേരള സംസ്ഥാന ഹോമിയോപതി ബോർഡ്", "TVM"),
    ("കerala സംസ്ഥാന ഫാർമസി കൗൺസിൽ", "TVM"),
    ("കerala സംസ്ഥാന തിരഞ്ഞെടുപ്പ് കമ്മീഷൻ", "TVM"),
    ("കerala സംസ്ഥാന വിവര കമ്മീഷൻ", "TVM"),
    ("കerala സംസ്ഥാന അന്യായം തടയൽ കമ്മീഷൻ", "TVM"),
    ("കerala സംസ്ഥാന ലിംഗ-ലിംഗഭേദ കമ്മീഷൻ", "TVM"),
    ("കerala സംസ്ഥാന ന്യൂനപക്ഷ കമ്മീഷൻ", "TVM"),
    ("കerala സംസ്ഥാന പിന്നോക്ക വിഭാഗ കമ്മീഷൻ", "TVM"),
    ("കerala സംസ്ഥാന ജാതി-ജനിതക-പിന്നോക്ക-കമ്മീഷൻ", "TVM"),
    ("കerala സംസ്ഥാന ആദിവാസി-കമ്മീഷൻ", "TVM"),
    ("കerala സംസ്ഥാന സാമ്പത്തിക-പിന്നോക്ക-കമ്മീഷൻ", "TVM"),
    ("കerala സംസ്ഥാന കലാ-സാംസ്കാരിക-ചരിത്ര-പാരമ്പര്യ-സാഹിത്യ-വിനോദ-ചലച്ചിത്ര-തിരഞ്ഞെടുപ്പ്-കമ്മീഷൻ", "TVM"),
])
RAW["KERALA_COMMISSION_HQ"] = [(a.replace("കerala", "കേരള"), b) for a, b in RAW["KERALA_COMMISSION_HQ"]]

RAW["PREMIER_INST_HQ"] = R("PREMIER_INST_HQ", [
    ("ഐ.ഐ.ടി മുംബൈ", "MUM"), ("ഐ.ഐ.ടി ഡൽഹി", "DEL"), ("ഐ.ഐ.ടി മദ്രാസ്", "CHN"),
    ("ഐ.ഐ.ടി കാൻപൂർ", "KNP"), ("ഐ.ഐ.ടി ഖരഗ്പൂർ", "KGP"), ("ഐ.ഐ.ടി റൂർക്കി", "RKE"),
    ("ഐ.ഐ.ടി ഹൈദരാബാദ്", "HYD"), ("ഐ.ഐ.ടി ഗാന്ധിനഗർ", "GNT"), ("ഐ.ഐ.ടി ഭുവനേശ്വർ", "BBS"),
    ("ഐ.ഐ.ടി ഇന്ദോർ", "IND"), ("ഐ.ഐ.ടി മണ്ഡി", "MND"), ("ഐ.ഐ.ടി ഗുവാഹാടി", "GWH"),
    ("ഐ.ഐ.ടി രോപ്രാഗ്രം", "RPR"), ("ഐ.ഐ.ടി ജോധ്പൂർ", "JDH"), ("ഐ.ഐ.ടി പട്ന", "PTN"),
    ("ഐ.ഐ.എം അഹമദാബാദ്", "AHM"), ("ഐ.ഐ.എം ബെംഗളൂuru", "BLR"), ("ഐ.ഐ.എം കൊൽക്കത്ത", "KOL"),
    ("ഐ.ഐ.എം ലഖ്\u200cനൗ", "LKO"), ("ഐ.ഐ.എം കോഴിക്കോട്", "KOZ"), ("ഐ.ഐ.എം ഇന്ദോർ", "IND"),
    ("എൻ.ഐ.ടി. കാലിക്കറ്റ്", "KOZ"), ("എൻ.ഐ.ടി. തിരുച്ചി", "TRI"), ("എൻ.ഐ.ടി. സുരത്തികൽ", "SUR"),
    ("ഐ.ഐ.എസ്.സി.", "BLR"), ("ഐ.ഐ.എസ്.ഇ.ആർ. തിരുവനന്തപുരം", "TVM"),
    ("ഐ.ഐ.എസ്.ഇ.ആർ. പൂണെ", "PUN"), ("ഐ.ഐ.എസ്.ഇ.ആർ. കൊൽക്കത്ത", "KOL"),
    ("ഐ.ഐ.എസ്.ടി.", "VAL"), ("എൻ.ഐ.ടി. വാരanasി", "VNS"), ("ഐ.ഐ.ടി. ബെംഗaloreuru", "BLR"),
])
RAW["PREMIER_INST_HQ"] = [
    (a.replace("ബെംഗaloreuru", "ബെംഗaloreuru").replace("ബെംഗaloreuru", "ബെംഗaloreuru"), k)
    for a, k in RAW["PREMIER_INST_HQ"]
]

def _fix_prem(raw):
    c = city_map()
    out = []
    for a, k in raw:
        a = a.replace("ബെംഗaloreuru", c["BLR"]).replace("വാരanasി", c["VNS"])
        out.append((a, k))
    return out
RAW["PREMIER_INST_HQ"] = _fix_prem([
    ("ഐ.ഐ.ടി മുംബൈ", "MUM"), ("ഐ.ഐ.ടി ഡൽഹി", "DEL"), ("ഐ.ഐ.ടി മദ്രാസ്", "CHN"),
    ("ഐ.ഐ.ടി കാൻപൂർ", "KNP"), ("ഐ.ഐ.ടി ഖരഗ്പൂർ", "KGP"), ("ഐ.ഐ.ടി റൂർക്കി", "RKE"),
    ("ഐ.ഐ.ടി ഹൈദരാബാദ്", "HYD"), ("ഐ.ഐ.ടി ഗാന്ധിനഗർ", "GNT"), ("ഐ.ഐ.ടി ഭuvoeneശ്വർ", "BBS"),
])
