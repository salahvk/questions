#!/usr/bin/env python3
"""Patch indian_history_facts.py with clean expanded Malayalam data."""

from __future__ import annotations

import random
import re
from pathlib import Path

BASE = Path(__file__).parent
PATH = BASE / "indian_history_facts.py"

CANNING = "\u0d32\u0d4b\u0d30\u0d4d\u0d21\u0d4d \u0d15\u0d3e\u0d28\u0d3f\u0d02\u0d17\u0d4d"
GUWAHATI = "\u0d17\u0d41\u0d35\u0d3e\u0d39\u0d3e\u0d24\u0d3f"
DELHI = "\u0d26\u0d3f\u0d32\u0d4d\u0d32\u0d3f"
GULBARGA = "\u0d17\u0d41\u0d32\u0d4d\u0d2c\u0d30\u0d4d\u0d17"
BAHMANI = "\u0d2c\u0d39\u0d4d\u0d2e\u0d28\u0d3f \u0d38\u0d41\u0d32\u0d4d\u0d24\u0d3e\u0d28\u0d24\u0d4d\u0d24\u0d4d"
SAROJINI = "\u0d38\u0d30\u0d4b\u0d1c\u0d3f\u0d28\u0d3f \u0d28\u0d3e\u0d2f\u0d41\u0d21\u0d41"
M_ANASA = "\u0d05\u0d28\u0d3e\u0d38"
KARACHI = "\u0d15\u0d3e\u0d30\u0d3e\u0d1a\u0d3f"
RAMGARH = "\u0d30\u0d3e\u0d02\u0d17\u0d1a\u0d02"
MEERUT = "\u0d2e\u0d40\u0d30\u0d1f\u0d4d\u0d1f\u0d41"
AZAD = "\u0d05\u0d2c\u0d41\u0d32\u0d4d \u0d15\u0d32\u0d3e\u0d02 \u0d06\u0d38\u0d3e\u0d26\u0d4d"
KHUDIRAM = "\u0d16\u0d41\u0d26\u0d40\u0d30\u0d3e\u0d02 \u0d2c\u0d4b\u0d38\u0d4d"
CHITTAGONG = "1930-\u0d32\u0d46 \u0d1a\u0d3f\u0d24\u0d4d\u0d24\u0d17\u0d02 \u0d06\u0d30\u0d4d\u0d2e\u0d30\u0d3f \u0d06\u0d15\u0d4d\u0d30\u0d2e\u0d23\u0d02"
ROMESH = "\u0d30\u0d4b\u0d02\u0d47\u0d37\u0d4d\u0d1a\u0d02\u0d26\u0d4d\u0d30 \u0d26\u0d24\u0d4d\u0d24"


def mostly_ml(s: str) -> bool:
    return not any("a" <= c <= "z" or "A" <= c <= "Z" for c in s)


GOVERNORS = [
    ("വാറൻ ഹേസ്റ്റിംഗ്സ്", "1774-1785"),
    ("ലോർഡ് കോർൺവാലിസ്", "1786-1793"),
    ("ലോർഡ് വെൽസלי", "1798-1805"),
    ("ലോർഡ് ഡാല്ഹൗസി", "1848-1856"),
    (CANNING, "1856-1862"),
    ("ലോർഡ് ലിട്ടൺ", "1876-1880"),
    ("ലോർഡ് റിപ്പൺ", "1880-1884"),
    ("ലോർഡ് കർസൺ", "1899-1905"),
    ("ലോർഡ് വേവൽ", "1943-1947"),
    ("ലോർഡ് മൗണ്ട്ബാറ്റൺ", "1947"),
]

BATTLES = [
    ("പ്ലാസി യുദ്ധം", "1757"),
    ("ബക്സർ യുദ്ധം", "1764"),
    ("പാനിപ്പട്ട് ഒന്നാം യുദ്ധം", "1526"),
    ("പാനിപ്പട്ട് രണ്ടാം യുദ്ധം", "1556"),
    ("പാനിപ്പട്ട് മൂന്നാം യുദ്ധം", "1761"),
    ("ഹൽദി ഘാട്ട് യുദ്ധം", "1526"),
    ("ചൗസ യുദ്ധം", "1539"),
    ("കണ്വ യുദ്ധം", "1540"),
]

MOVEMENTS = [
    ("ചംപാരൻ സത്യാഗ്രഹം", "1917", "മഹാത്മാ ഗാന്ധി"),
    ("ഖേദാ സത്യാഗ്രഹം", "1918", "മഹാത്മാ ഗാന്ധി"),
    ("റൗലട്ട് സത്യാഗ്രഹം", "1919", "മഹാത്മാ ഗാന്ധി"),
    ("\u0d05\u0d38\u0d39\u0d15\u0d30\u0d23 \u0d38\u0d24\u0d4d\u0d24\u0d4d\u0d2f\u0d3e\u0d17\u0d4d\u0d30\u0d39\u0d02", "1920", "മഹാത്മാ ഗാന്ധി"),
    ("ഉപ്പ് സത്യാഗ്രഹം", "1930", "മഹാത്മാ ഗാന്ധി"),
    ("ഖിലാഫത്ത് പ്രസ്ഥാനം", "1919", "മഹാത്മാ ഗാന്ധി"),
    ("ബർദോലി സത്യാഗ്രഹം", "1928", "സർദാർ വല്ലഭഭായി പട്ടേൽ"),
    ("വൈകം സത്യാഗ്രഹം", "1924", "മഹാത്മാ ഗാന്ധി"),
    ("\u0d28\u0d3e\u0d17\u0d30\u0d4d\u0d15\u0d4d\u0d15\u0d4b\u0d7a \u0d38\u0d24\u0d4d\u0d24\u0d4d\u0d2f\u0d3e\u0d17\u0d4d\u0d30\u0d39\u0d02", "1924", "മഹാത്മാ ഗാന്ധി"),
    ("\u0d07\u0d02\u0d24\u0d4d\u0d2f \u0d1b\u0d4b\u0d21\u0d4d\u0d21\u0d4b \u0d06\u0d28\u0d4d\u0d26\u0d4b\u0d33\u0d28\u0d02", "1942", "മഹാത്മാ ഗാന്ധി"),
    ("സ്വദേശി പ്രസ്ഥാനം", "1905", "\u0d2c\u0d3e\u0d32 \u0d17\u0d02\u0d17\u0d3e\u0d27\u0d30\u0d4d \u0d24\u0d3f\u0d32\u0d15\u0d4d"),
]

CONGRESS_SESSIONS = [
    ("1885", "ബോംബെ", "ഡബ്ല്യു.സി. ബാനർജി"),
    ("1886", "കൽക്കത്ത", "ദാദാഭായി നൗറോജി"),
    ("1887", "മദ്രാസ്", "ബദരുദ്ദീൻ തയ്യബ്ജി"),
    ("1889", "ബോംബെ", "ജോർജ് യുലെ"),
    ("1890", "കൽക്കത്ത", "ഫിറോസ്ഷാ മേത്ത"),
    ("1891", "നാഗ്പൂർ", "വുമേഷ ചന്ദ്ര ബാനർജി"),
    ("1892", "അലഹാബാദ്", "വുമേഷ ചന്ദ്ര ബാനർജി"),
    ("1893", "ലാഹോർ", "ദാദാഭായി നൗറോജി"),
    ("1895", "പൂണ", "സുരേന്ദ്രനാഥ ബാനർജി"),
    ("1896", "കൽക്കത്ത", "റഹിമത്തുല്ല സായാനി"),
    ("1898", "മദ്രാസ്", "ആനന്ദ മോഹൻ ബോസ്"),
    ("1899", "ലഖ്നൗ", ROMESH),
    ("1900", "ലാഹോർ", "നാരായണ ഗണേശ"),
    ("1901", "കൽക്കത്ത", "ദിനേശ്ചന്ദ്ര സെൻ"),
    ("1903", "മദ്രാസ്", "ലാലാ ലജപത് റായ്"),
    ("1905", "ബനാരസ്", "ഗോപാൽകൃഷ്ണ ഗോഖലെ"),
    ("1906", "കൽക്കത്ത", "ദാദാഭായി നൗറോജി"),
    ("1907", "സൂറത്ത്", "റാഷ്ബെഹരി ഘോഷ്"),
    ("1909", "ലാഹോർ", "മദൻ മോഹൻ മാൽവിയ"),
    ("1911", "കൽക്കത്ത", "വില്യം വെഡ്ഡെർബേൺ"),
    ("1916", "ലഖ്നൗ", "ആംബികാ ചരൺ മജുമദാർ"),
    ("1917", "കൽക്കത്ത", "അന്നി ബസന്റ്"),
    ("1918", DELHI, "സൈയ്യദ് ഹസൻ ഇമാം"),
    ("1919", "അമൃതസർ", "മദൻ മോഹൻ മാൽവിയ"),
    ("1920", "നാഗ്പൂർ", "ലാലാ ലജപത് റായ്"),
    ("1921", "അഹമദാബാദ്", "ഹക്കീം അജ്മൽ ഖാൻ"),
    ("1922", "ഗയ", "സി. രാജഗോപാലാചാരി"),
    ("1924", "ബെൽഗാം", "മഹാത്മാ ഗാന്ധി"),
    ("1925", "കാൻപുർ", "സർദാർ വല്ലഭഭായി പട്ടേൽ"),
    ("1926", GUWAHATI, SAROJINI),
    ("1927", "മദ്രാസ്", f"എം. {M_ANASA}"),
    ("1928", "കൽക്കത്ത", "മോത്തിലാൽ നെഹ്റു"),
    ("1929", "ലാഹോർ", "ജവഹർലാൽ നെഹ്റു"),
    ("1930", "ലാഹോർ", "ജവഹർലാൽ നെഹ്റു"),
    ("1931", KARACHI, "സർദാർ വല്ലഭഭായി പട്ടേൽ"),
    ("1934", "ബോംബെ", "രാജേന്ദ്ര പ്രസാദ്"),
    ("1936", "ലഖ്നൗ", "ജവഹർലാൽ നെഹ്റു"),
    ("1938", "ഹരിപുര", "സുഭാഷ് ചന്ദ്ര ബോസ്"),
    ("1939", "ത്രിപുരി", "രാജേന്ദ്ര പ്രസാദ്"),
    ("1940", RAMGARH, AZAD),
    ("1946", MEERUT, "ജവഹർലാൽ നെഹ്റു"),
]
CONGRESS_SESSIONS = [s for s in CONGRESS_SESSIONS if mostly_ml("".join(s))]

DYNASTIES = [
    ("മൗര്യ സാമ്രാജ്യം", "ചന്ദ്രഗുപ്ത മൗര്യ", "പാടലിപുത്ര"),
    ("ഗുപ്ത സാമ്രാജ്യം", "ചന്ദ്രഗുപ്തൻ", "പാടലിപുത്ര"),
    ("ചോള സാമ്രാജ്യം", "വിജയാലയ", "തഞ്ചാവൂർ"),
    ("വിജയനഗര സാമ്രാജ്യം", "ഹരിഹര", "വിജയനഗര"),
    ("മറാത്ത സാമ്രാജ്യം", "ശിവാജി", "റായ്ഗഡ്"),
    (BAHMANI, "അലാവുദ്ദിൻ ബഹ്മനി ഷാ", GULBARGA),
    ("സൂർ സാമ്രാജ്യം", "ഷെർ ഷാ സൂരി", DELHI),
]
DYNASTIES = [d for d in DYNASTIES if mostly_ml("".join(d))]

FREEDOM_FIGHTERS = [
    ("ഭഗത് സിംഗ്", "1928-ലെ നിയമസഭാ ബോംബ് കേസ്", "1928"),
    ("ചന്ദ്രശേഖർ ആസാദ്", "1925-ലെ കാക്കോരി സംഭവം", "1925"),
    ("രാം പ്രസാദ് ബിസ്മിൽ", "1925-ലെ കാക്കോരി സംഭവം", "1925"),
    ("സുഖദേവ്", "1928-ലെ നിയമസഭാ ബോംബ് കേസ്", "1928"),
    (KHUDIRAM, "1908-ലെ മുസാഫിർപൂർ ബോംബ് കേസ്", "1908"),
    ("സുര്യ സേൻ", CHITTAGONG, "1930"),
]

GEN_EXTRA = '''
    session_years = [y for y, _, _ in CONGRESS_SESSIONS]
    session_places = [p for _, p, _ in CONGRESS_SESSIONS]
    session_pres = [pr for _, _, pr in CONGRESS_SESSIONS]
    for year, place, president in CONGRESS_SESSIONS:
        _add(out, existing, rng, f"{year}-ലെ ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് സമ്മേളന സ്ഥലം?", place, session_places, "medium")
        _add(out, existing, rng, f"{year}-ലെ ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് അധ്യക്ഷൻ?", president, session_pres, "medium")
        _add(out, existing, rng, f"'{place}'-ൽ നടന്ന കോൺഗ്രസ് സമ്മേളന വർഷം?", year, session_years, "hard")

    for person, event, year in FREEDOM_FIGHTERS:
        people = [p for p, _, _ in FREEDOM_FIGHTERS]
        _add(out, existing, rng, f"'{event}'-ുമായി ബന്ധപ്പെട്ട വിപ്ലവകാരി?", person, people, "hard")
'''

text = PATH.read_text(encoding="utf-8")

block = (
    f"BATTLES: list[tuple[str, str]] = {BATTLES!r}\n\n"
    f"GOVERNORS: list[tuple[str, str]] = {GOVERNORS!r}\n\n"
    f"MOVEMENTS: list[tuple[str, str, str]] = {MOVEMENTS!r}\n\n"
    f"CONGRESS_SESSIONS: list[tuple[str, str, str]] = {CONGRESS_SESSIONS!r}\n\n"
    f"DYNASTIES: list[tuple[str, str, str]] = {DYNASTIES!r}\n\n"
    f"FREEDOM_FIGHTERS: list[tuple[str, str, str]] = {FREEDOM_FIGHTERS!r}\n"
)

text = re.sub(
    r"BATTLES: list\[tuple\[str, str\]\] = \[.*?\nFREEDOM_FIGHTERS: list\[tuple\[str, str, str\]\] = \[.*?\n\]\n",
    block,
    text,
    count=1,
    flags=re.DOTALL,
)

if "session_years" not in text:
    text = text.replace(
        "    for dyn, founder, capital in DYNASTIES:\n"
        "        _add(out, existing, rng, f\"'{dyn}'-ന്റെ സ്ഥാപകൻ?\", founder, founders, \"medium\")\n"
        "        _add(out, existing, rng, f\"'{dyn}'-ന്റെ തലസ്ഥാനം?\", capital, capitals, \"medium\")\n"
        "    return out\n",
        "    for dyn, founder, capital in DYNASTIES:\n"
        "        _add(out, existing, rng, f\"'{dyn}'-ന്റെ സ്ഥാപകൻ?\", founder, founders, \"medium\")\n"
        "        _add(out, existing, rng, f\"'{dyn}'-ന്റെ തലസ്ഥാനം?\", capital, capitals, \"medium\")\n"
        + GEN_EXTRA
        + "    return out\n",
    )

PATH.write_text(text, encoding="utf-8")

import importlib
import indian_history_facts as ih

importlib.reload(ih)
print("Congress:", len(CONGRESS_SESSIONS))
print("Movements:", len(MOVEMENTS))
print("Dynasties:", len(DYNASTIES))
print("Candidates:", len(ih.generate_candidates(set(), random.Random(42))))
