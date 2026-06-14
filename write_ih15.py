#!/usr/bin/env python3
"""Emit ih_wave15_facts.py with codepoint-safe Malayalam data."""

from __future__ import annotations

import pprint
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
HEADER = (ROOT / "ih_wave15_facts.py").read_text(encoding="utf-8").split("# 1 — Bhakti")[0]

_g: dict = {"__file__": str(ROOT / "gen_ih15.py")}
exec((ROOT / "gen_ih15.py").read_text(encoding="utf-8"), _g)
BHAKTI: list[tuple[str, str, str]] = _g["BHAKTI"]

MONUMENTS: list[tuple[str, str]] = [
    ("താജ്മഹൽ", "ഷാജഹാൻ"),
    ("ചെങ്കോട്ട", "ഷാജഹാൻ"),
    ("ജാമാ മസjid", "ഷാജഹാൻ"),
    ("ദിൽവാരാ മസjid", "ഷാജഹാൻ"),
    ("ഹുമായൂന്റെ കബr", "ഹുമായൂൺ"),
    ("പുർana ഖില", "ഹുമായൂൺ"),
    ("ഫatehpur sikri", "അക്ബർ"),
    ("ബുൾand darwaza", "അക്ബർ"),
    ("ഐതുമുദ്ദുല്ല", "അക്ബർ"),
    ("ജോധാ ബായി കുഴ", "അക്ബർ"),
    ("അകbar tomb", "ജഹാംഗീർ"),
    ("ഇത്മാദ്-ഉദ്-ദൗല", "ജഹാംഗീർ"),
    ("ഷalimar bagh", "ജഹാംഗീർ"),
    ("ലal qila", "ഷാജഹാൻ"),
    ("പearl mosque", "ഔറംഗസേബ്"),
    ("badshahi masjid", "ഔറംഗസേബ്"),
    ("bibi ka maqbara", "ഔറംഗസേബ്"),
    ("charminar", "മുഹമ്മദ് ഖുലി ഖുതുബ് ഷാ"),
    ("golconda fort", "കാകത്തiya"),
    ("qutub minar", "ഖുതുബ്-ഉദ്-ദിൻ ഐബക്"),
    ("alai darwaza", "അലാവുദ്-ദിൻ ഖൽji"),
    ("hauz khas", "അലാവുദ്-ദിൻ ഖൽji"),
    ("tughlaqabad fort", "ഗhiyasuddin tughlaq"),
    ("firoz shah kotla", "ഫiruz shah tughlaq"),
    ("purana qila delhi", "ഷer shah suri"),
    ("sher shah tomb", "ഷer shah suri"),
    ("hampi virupaksha", "വijayanagara"),
    ("vittala temple", "വijayanagara"),
    ("konark sun temple", "നarasimhadeva"),
    ("lingaraj temple", "somvanshi"),
    ("khajuraho", "chandel"),
    ("mahabodhi temple", "guptas"),
    ("sanchi stupa", "ashoka"),
    ("elephanta caves", "rashtrakuta"),
    ("ajanta caves", "vakataka"),
    ("ellora kailasa", "rashtrakuta"),
    ("meenakshi temple", "pandyas"),
    ("brihadeeswara", "raja raja chola"),
    ("gangaikonda cholapuram", "rajendra chola"),
    ("qutb shahi tombs", "qutb shahi"),
    ("jama masjid delhi", "ഷാജഹാൻ"),
    ("red fort agra", "അക്ബർ"),
    ("itimad ud daulah", "നൂർ ജഹാൻ"),
    ("safdarjung tomb", "safdarjung"),
    ("jantar mantar delhi", "jaisingh"),
    ("jantar mantar jaipur", "jaisingh"),
    ("city palace jaipur", "jaisingh"),
    ("amber fort", "kachwaha"),
    ("chittorgarh fort", "sisodia"),
    ("gwalior fort", "tomars"),
    ("red fort srinagar", "shah jahan"),
    ("shalimar srinagar", "jahangir"),
    ("nishat bagh", "asaf khan"),
    ("shalimar delhi", "shah jahan"),
    ("humayun gate", "humayun"),
    ("agra fort", "akbar"),
    ("fatehpur sikri palace", "akbar"),
    ("buland darwaza sikri", "akbar"),
    ("jama masjid agra", "shah jahan"),
    ("motī masjid agra", "shah jahan"),
    ("peacock throne", "shah jahan"),
]
