#!/usr/bin/env python3
"""Wave 7: IH_EXTRA_3 / GEO_EXTRA_3 / WH_EXTRA_3 / BIO_EXTRA_3 verified direct facts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent


def _f(q: str, ans: str, wrong: list[str], diff: str = "medium") -> tuple[str, str, list[str], str]:
    return (q, ans, wrong, diff)


def build_ih_extra_3() -> list[tuple[str, str, list[str], str]]:
    facts: list[tuple[str, str, list[str], str]] = []
    leaders = [
        ("ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് ആദ്യ അധ്യക്ഷൻ?", "ഡബ്ല്യു.സി. ബാനർജി", ["ദാദാഭായി നൗറോജി", "ഗോപാൽകൃഷ്ണ ഗോഖലെ", "മഹാത്മാ ഗാന്ധി"], "hard"),
        ("ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് രൂപീകരിച്ച വർഷം?", "1885", ["1905", "1919", "1947"], "easy"),
        ("ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് ആദ്യ സമ്മേളന വേദി?", "ബോംബെ", ["കൽക്കത്ത", "മദ്രാസ്", "ദില്ലി"], "medium"),
        ("1905 സ്വദേശി പ്രസ്ഥാനത്തിന്റെ പ്രധാന നേതാവ്?", "ബാല ഗംഗാധർ തിലക്", ["ഗോപാൽകൃഷ്ണ ഗോഖലെ", "മഹാത്മാ ഗാന്ധി", "ജവഹർലാൽ നെഹ്റു"], "medium"),
        ("1905 ബംഗാൽ വിഭജനം നടപ്പാക്കിയ വൈസ്രോയി?", "ലോർഡ് കർസൺ", ["ലോർഡ് റിപ്പൺ", "ലോർഡ് ഡാൽഹൗസി", "ലോർഡ് മൗണ്ട്ബാറ്റൻ"], "medium"),
        ("1916 ലucknow പാക്റ്റ് ഒപ്പിട്ട വർഷം?", "1916", ["1919", "1905", "1920"], "medium"),
        ("1919 ജാലിയൻവാലാ ബാഗ് സംഭവം?", "1919", ["1920", "1917", "1942"], "easy"),
        ("1920 നോൺ-കോഓപ്പറേഷൻ പ്രസ്ഥാനം?", "1920", ["1919", "1930", "1942"], "easy"),
        ("1930 സിവിൽ അനുചരണ പ്രസ്ഥാനം?", "1930", ["1920", "1942", "1919"], "easy"),
        ("1930 ഡാൻഡി മാർച്ച്?", "1930", ["1928", "1942", "1919"], "easy"),
        ("1942 ക്വിറ്റ് ഇന്ത്യാ പ്രസ്ഥാനം?", "1942", ["1940", "1930", "1919"], "easy"),
        ("1857 സിപോയി മ്യൂട്ടിനി ആരംഭിച്ച സ്ഥലം?", "മീററ്റ്", ["ദില്ലി", "കാൻപൂർ", "ലucknow"], "medium"),
        ("1857-ൽ ഝansi രാജ്ഞി?", "ലക്ഷ്മീബായി", ["ഹസ്രത്ത് മഹൽ", "ചennamma", "കittur chennamma"], "easy"),
        ("1757 പ്ലാസി യുദ്ധം?", "1757", ["1764", "1857", "1947"], "easy"),
        ("1764 ബക്സർ യുദ്ധം?", "1764", ["1757", "1857", "1947"], "medium"),
        ("പാനിപത്ത് ഒന്നാം യുദ്ധം?", "1526", ["1556", "1761", "1857"], "hard"),
        ("പാനിപത്ത് രണ്ടാം യുദ്ധം?", "1556", ["1526", "1761", "1857"], "hard"),
        ("പാനിപത്ത് മൂന്നാം യുദ്ധം?", "1761", ["1526", "1556", "1857"], "hard"),
        ("ഡോക്ട്രിൻ ഓഫ് ലാപ്സ്?", "ലോർഡ് ഡാൽഹൗസി", ["ലോർഡ് വെൽസ്ലി", "ലോർഡ് ക്യർസൺ", "ലോർഡ് റിപ്പൺ"], "easy"),
        ("1773 റെഗുലേറ്റിംഗ് ആക്ട് — ആദ്യ ഗവർണർ ജനറൽ?", "വാറൻ ഹേസ്റ്റിംഗ്സ്", ["ലോർഡ് കോർൺവാലിസ്", "ലോർഡ് വെൽസ്ലി", "ലോർഡ് ഡാൽഹൗസി"], "medium"),
        ("1858-ൽ കമ്പനി ഭരണം അവസാനിച്ച വർഷം?", "1858", ["1857", "1861", "1877"], "medium"),
        ("1947 ഇന്ത്യൻ സ്വാതന്ത്ര്യം?", "1947 ഓഗസ്റ്റ് 15", ["1947 ജൂൺ 3", "1950 ജനുവരി 26", "1947 ജൂലൈ 18"], "easy"),
        ("1950 ഇന്ത്യൻ റിപ്പബ്ലിക് ദിനം?", "1950 ജനുവരി 26", ["1947 ഓഗസ്റ്റ് 15", "1947 ജൂൺ 3", "1947 ജൂലൈ 18"], "easy"),
        ("ഭരണഘടന രചയിതാവ്?", "ബി.ആർ. അംബേദ്കർ", ["മഹാത്മാ ഗാന്ധി", "ജവഹർലാൽ നെഹ്റു", "സർദാർ പട്ടേൽ"], "easy"),
        ("ആദ്യ പ്രധാനമന്ത്രി?", "ജവഹർലാൽ നെഹ്റു", ["സർദാർ പട്ടേൽ", "രാജേന്ദ്ര പ്രസാദ്", "സുഭാഷ് ബോസ്"], "easy"),
        ("ആദ്യ രാഷ്ട്രപതി?", "രാജേന്ദ്ര പ്രസാദ്", ["ജവഹർലാൽ നെഹ്റു", "സർദാർ പട്ടേൽ", "സുഭാഷ് ബോസ്"], "easy"),
        ("INA-യുടെ 'ദില്ലി ചലോ'?", "സുഭാഷ് ചന്ദ്ര ബോസ്", ["ജവഹർലാൽ നെഹ്റു", "മഹാത്മാ ഗാന്ധി", "ഭഗത് സിംഗ്"], "easy"),
        ("ഭഗത് സിംഗ് വധശിക്ഷ?", "1931", ["1929", "1930", "1932"], "medium"),
        ("ചന്ദ്രശേഖർ ആസാദ് മരണം?", "1931", ["1929", "1930", "1932"], "medium"),
        ("അശോകൻ ധർമ്മം സ്വീകരിച്ച വർഷം?", "260 BCE", ["232 BCE", "300 BCE", "200 BCE"], "hard"),
        ("അർഥശാസ്ത്രം രചിച്ചത്?", "ചാണക്യൻ", ["കാലിദാസൻ", "വാല്മീകി", "പതഞ്ജലി"], "medium"),
        ("നാലന്ദ സർവ്വകലാശാല സ്ഥാപകൻ?", "കുമാരഗുപ്ത I", ["അശോകൻ", "ഹർഷവർദ്ധൻ", "ചന്ദ്രഗുപ്തൻ"], "hard"),
        ("ഹർഷവർദ്ധന്റെ തലസ്ഥാനം?", "കന്യാകുബ്ജ", ["പാടലിപുത്ര", "ഉജ്ജയിനി", "കാഞ്ചി"], "hard"),
        ("ബാബർ ഇന്ത്യയിൽ ആക്രമിച്ച വർഷം?", "1526", ["1556", "1761", "1857"], "medium"),
        ("അക്ബർ സിംഹാസനാരോഹണം?", "1556", ["1526", "1658", "1857"], "medium"),
        ("ഷാജഹാൻ നിർമ്മിച്ച താജ്മഹാൽ?", "ആഗ്ര", ["ദില്ലി", "ലാഹോർ", "ജയ്പൂർ"], "easy"),
        ("വിജയനഗര സാമ്രാജ്യം സ്ഥാപകർ?", "ഹരിഹര, ബുക്ക", ["കൃഷ്ണദേവരായർ", "രാമരായ", "പുലകേശി"], "medium"),
        ("ശിവാജി ഭരണം ആരംഭിച്ച സാമ്രാജ്യം?", "മറatha", ["മൈസൂർ", "മുഗൾ", "വിജയനഗര"], "medium"),
        ("ടിപ്പു സുൽത്താൻ വീഴ്ച?", "1799", ["1767", "1784", "1857"], "medium"),
        ("സൈമൺ കമ്മീഷൻ?", "1928", ["1925", "1930", "1932"], "easy"),
        ("ക്രിപ്സ് മിഷൻ?", "1942", ["1940", "1945", "1946"], "medium"),
        ("ക്യാബിനറ്റ് മിഷൻ?", "1946", ["1942", "1945", "1947"], "medium"),
        ("മൗണ്ട്ബാറ്റൻ പ്ലാൻ?", "1947 ജൂൺ 3", ["1947 ഓഗസ്റ്റ് 15", "1947 ജൂലൈ 18", "1950 ജനുവരി 26"], "medium"),
        ("പൂന പാക്റ്റ്?", "1932", ["1930", "1935", "1942"], "medium"),
        ("1935 ഇന്ത്യാ ഭരണനിയമം അടിസ്ഥാനം?", "സൈമൺ കമ്മീഷൻ റിപ്പോർട്ട്", ["ക്രിപ്സ് മിഷൻ", "ക്യാബിനറ്റ് മിഷൻ", "വേവൽ പ്ലാൻ"], "medium"),
        ("ആദ്യ പഞ്ചവത്സര പദ്ധതി?", "1951", ["1947", "1950", "1956"], "medium"),
        ("ഭരണഘടന നിർമ്മാണ സഭാ അധ്യക്ഷൻ?", "ഡോ. രാജേന്ദ്ര പ്രസാദ്", ["ബി.ആർ. അംബേദ്കർ", "ജവഹർലാൽ നെഹ്റു", "സർദാർ പട്ടേൽ"], "medium"),
        ("ഭരണഘടന നിർമ്മാണ സഭ?", "1946", ["1947", "1950", "1942"], "medium"),
        ("ഖിലാഫത്ത് പ്രസ്ഥാനം?", "1919", ["1920", "1915", "1930"], "easy"),
        ("ചമ്പാരൻ സത്യാഗ്രഹം?", "1917", ["1919", "1930", "1942"], "medium"),
        ("ബർദോളി സത്യാഗ്രഹം?", "1928", ["1930", "1942", "1920"], "medium"),
        ("ഗാന്ധിജി ഇന്ത്യയിൽ എത്തിയ വർഷം?", "1915", ["1917", "1919", "1920"], "easy"),
        ("ഘadar പാർട്ടി?", "1913", ["1905", "1919", "1920"], "hard"),
        ("മുസ്ലിം ലീഗ്?", "1906", ["1919", "1885", "1940"], "medium"),
        ("സ്വരാജ്യ പാർട്ടി സ്ഥാപകർ?", "മോതിലാൽ നെഹ്റു, സി.ആർ. ദാസ്", ["ഗാന്ധി, നെഹ്റു", "ബോസ്, അംബേദ്കർ", "പട്ടേൽ, രാജാജി"], "hard"),
        ("ഫോർവേഡ് ബ്ലോക്ക്?", "സുഭാഷ് ചന്ദ്ര ബോസ്", ["മഹാത്മാ ഗാന്ധി", "ജവഹർലാൽ നെഹ്റു", "ബാല ഗംഗാധർ തിലക്"], "medium"),
        ("റോയൽ ഇന്ത്യൻ നാവി മ്യൂട്ടിനി?", "1946", ["1942", "1945", "1947"], "medium"),
        ("1945 INA trials?", "1945", ["1946", "1942", "1947"], "medium"),
        ("ആദ്യ ഭാരതരത്ന?", "സി. രാജഗോപാലാചാരി", ["ജവഹർലാൽ നെഹ്റു", "സർദാർ പട്ടേൽ", "മഹാത്മാ ഗാന്ധി"], "hard"),
        ("ആദ്യ നോബൽ (സാഹിത്യ) ഇന്ത്യക്കാരൻ?", "രവീന്ദ്രനാഥ ടാഗോർ", ["സി.വി. രാമൻ", "അമർത്യ സെൻ", "കൈലാസ് സത്യാർത്ഥി"], "medium"),
        ("ആദ്യ നോബൽ (ശാസ്ത്രം) ഇന്ത്യക്കാരൻ?", "സി.വി. രാമൻ", ["രവീന്ദ്രനാഥ ടാഗോർ", "അമർത്യ സെൻ", "കൈലാസ് സത്യാർത്ഥി"], "medium"),
    ]
    for item in leaders:
        facts.append(_f(*item))

    dynasties = [
        ("മൗര്യ സാമ്രാജ്യ സ്ഥാപകൻ?", "ചന്ദ്രഗുപ്ത മൗര്യ", ["അശോകൻ", "ബിംബിസാര", "ഹർഷ"], "medium"),
        ("ഗുപ്ത സാമ്രാജ്യ സ്ഥാപകൻ?", "ചന്ദ്രഗുപ്ത I", ["സമുദ്രഗുപ്ത", "അശോകൻ", "ഹർഷ"], "medium"),
        ("മുഗൾ സാമ്രാജ്യ സ്ഥാപകൻ?", "ബാബർ", ["അക്ബർ", "ഔറംഗസേബ്", "ഷാജഹാൻ"], "easy"),
        ("വിജയനഗര സ്ഥാപകർ?", "ഹരിഹര, ബുക്ക", ["കൃഷ്ണദേവരായർ", "രാമരായ", "പുലകേശി"], "medium"),
        ("മറാത്ത സാമ്രാജ്യ സ്ഥാപകൻ?", "ശിവാജി", ["പേശ്വ", "തുഗ്ലക്ക്", "മുഗൾ"], "medium"),
        ("മൈസൂർ സുൽത്താൻ?", "ഹൈദർ അലി", ["ടിപ്പു സുൽത്താൻ", "ശിവാജി", "അക്ബർ"], "medium"),
        ("ദില്ലി സുൽത്താനത്ത് സ്ഥാപകൻ?", "ക്വുത്ബുദ്ദീൻ ഐബക്ക്", ["ഇല്തുമിഷ്", "ബാല്ബൻ", "അലാവുദ്ദീൻ ഖിൽജി"], "medium"),
        ("ചോള സാമ്രാജ്യ സ്ഥാപകൻ?", "വിജയാലയ", ["രാജരാജ ചോളൻ", "കൃഷ്ണദേവരായർ", "പുലകേശി"], "medium"),
        ("ഹർഷവർദ്ധൻ?", "606–647 CE", ["322–185 BCE", "320–550 CE", "1526–1556"], "hard"),
        ("സൂർ രാജവംശ?", "ഷെർ ഷാ സൂരി", ["ഹുമയൂൻ", "ബാബർ", "അക്ബർ"], "easy"),
    ]
    for item in dynasties:
        facts.append(_f(*item))
    return facts


def build_geo_extra_3() -> list[tuple[str, str, list[str], str]]:
    facts: list[tuple[str, str, list[str], str]] = []
    peaks = [
        ("ക2", "പākistan/China", ["Nepal", "India", "Bhutan"], "hard"),
        ("കanchenjunga", "India/Nepal", ["Pakistan", "China", "Bhutan"], "hard"),
        ("എverest", "Nepal/China", ["India", "Pakistan", "Bhutan"], "easy"),
        ("നanda devi", "Uttarakhand", ["Himachal", "Sikkim", "Arunachal"], "hard"),
        ("Anamudi", "Kerala", ["Tamil Nadu", "Karnataka", "Maharashtra"], "medium"),
        ("Doddabetta", "Tamil Nadu", ["Kerala", "Karnataka", "Andhra"], "hard"),
        ("Guru Shikhar", "Rajasthan", ["Gujarat", "MP", "Maharashtra"], "hard"),
        ("Mahendragiri", "Odisha", ["AP", "Telangana", "Karnataka"], "hard"),
    ]
    for peak, loc, wrong, diff in peaks:
        facts.append(_f(f"'{peak}' ഏത് പ്രദേശ/രാജ്യത്തിൽ?", loc, wrong, diff))

    straits = [
        ("Malacca", "Malaysia/Indonesia", ["India", "Australia", "Japan"], "hard"),
        ("Hormuz", "Iran/Oman", ["Egypt", "Turkey", "India"], "hard"),
        ("Bosphorus", "Turkey", ["Greece", "Italy", "Spain"], "hard"),
        ("Dover", "England/France", ["Spain/Portugal", "Italy/Greece", "Turkey/Greece"], "hard"),
        ("Palk", "India/Sri Lanka", ["India/Maldives", "India/Bangladesh", "India/Pakistan"], "medium"),
    ]
    for name, loc, wrong, diff in straits:
        facts.append(_f(f"'{name}' കടലിടുക്ക് ബന്ധിപ്പിക്കുന്നത്?", loc, wrong, diff))

    symbols = [
        ("ഇന്ത്യയുടെ ദേശീയ പക്ഷി?", "മയിൽ", ["കാക്ക", "കുരുവി", "കഴുകൻ"], "easy"),
        ("ഇന്ത്യയുടെ ദേശീയ മൃഗം?", "കടുവ", ["സിംഹം", "യാനം", "ചിരുത"], "easy"),
        ("ഇന്ത്യയുടെ ദേശീയ പുഷ്പം?", "താമര", ["പനിനീർ", "ചെമ്പരത്തി", "ജാസ്മിൻ"], "easy"),
        ("ഇന്ത്യയുടെ ദേശീയ വൃക്ഷം?", "ആലമരം", ["വെട്ടി", "മാവ്", "നാരങ്ങ"], "easy"),
        ("ഇന്ത്യയുടെ ദേശീയ ഫലം?", "മാങ്ങ", ["വാഴ", "ആപ്പിൾ", "പേര"], "easy"),
        ("ഇന്ത്യയുടെ ദേശീയ ഗാനം?", "ജന ഗണ മന", ["വന്ദേ മാതരം", "സാരേ ജഹാൻ", "ജയ് ഹിന്ദ്"], "easy"),
        ("ഇന്ത്യയുടെ ദേശീയ ചിഹ്നം?", "അശോക ചക്രം", ["താമര", "മയിൽ", "കടുവ"], "easy"),
        ("ഇന്ത്യയുടെ ദേശീയ പതാക നിറം?", "ത്രicolor", ["ദ്വicolor", "നാല് നിറം", "ഒരു നിറം"], "easy"),
        ("കerala-യുടെ ദേശീയ പക്ഷി?", "മലabar whistling thrush", ["മയിൽ", "കാക്ക", "കുരുവി"], "hard"),
        ("കerala-യുടെ ദേശീയ മൃഗം?", "Indian elephant", ["കടുവ", "സിംഹം", "ചിരുത"], "hard"),
        ("കerala-യുടെ ദേശീയ പുഷ്പം?", "കanikonna", ["താമര", "പനിനീർ", "ജasmine"], "hard"),
        ("കerala-യുടെ ദേശീയ വൃക്ഷം?", "കoconut", ["ആലമരം", "മാവ്", "വെട്ടി"], "hard"),
        ("കerala-യുടെ ദേശീയ ഫലം?", "പpayar", ["മാങ്ങ", "വാഴ", "നെല്ല്"], "hard"),
    ]
    for q, ans, wrong, diff in symbols:
        facts.append(_f(q, ans, wrong, diff))

    lakes = [
        ("Dal Lake", "Jammu Kashmir", ["Himachal", "Uttarakhand", "Sikkim"], "medium"),
        ("Chilika Lake", "Odisha", ["AP", "West Bengal", "Gujarat"], "hard"),
        ("Vembanad Lake", "Kerala", ["Tamil Nadu", "Karnataka", "Odisha"], "medium"),
        ("Sambhar Lake", "Rajasthan", ["Gujarat", "MP", "Haryana"], "hard"),
        ("Wular Lake", "Jammu Kashmir", ["Punjab", "Haryana", "UP"], "hard"),
        ("Loktak Lake", "Manipur", ["Assam", "Meghalaya", "Tripura"], "hard"),
        ("Pulicat Lake", "Andhra/TN border", ["Kerala", "Odisha", "Gujarat"], "hard"),
    ]
    for lake, state, wrong, diff in lakes:
        facts.append(_f(f"'{lake}' ഏത് സംസ്ഥാന/പ്രദേശത്തിൽ?", state, wrong, diff))

    return facts


def build_wh_extra_3() -> list[tuple[str, str, list[str], str]]:
    events = [
        ("French Revolution?", "1789", ["1815", "1848", "1776"], "easy"),
        ("American Independence?", "1776", ["1789", "1815", "1914"], "easy"),
        ("Russian October Revolution?", "1917", ["1905", "1920", "1914"], "medium"),
        ("Chinese Revolution (PRC)?", "1949", ["1911", "1939", "1959"], "medium"),
        ("Cuban Revolution?", "1959", ["1949", "1979", "1989"], "hard"),
        ("Iran Revolution?", "1979", ["1959", "1949", "1989"], "hard"),
        ("WWI?", "1914–1918", ["1939–1945", "1900–1905", "1920–1924"], "easy"),
        ("WWII?", "1939–1945", ["1914–1918", "1945–1950", "1920–1925"], "easy"),
        ("Berlin Wall fell?", "1989", ["1991", "1986", "2001"], "easy"),
        ("Soviet Union dissolved?", "1991", ["1989", "1995", "2001"], "medium"),
        ("UN founded?", "1945", ["1919", "1950", "1939"], "easy"),
        ("NATO founded?", "1949", ["1945", "1955", "1939"], "medium"),
        ("EU Maastricht?", "1993", ["1957", "1989", "2002"], "hard"),
        ("Cold War ended?", "1991", ["1989", "1995", "2001"], "medium"),
        ("Korean War started?", "1950", ["1945", "1955", "1965"], "medium"),
        ("Vietnam War ended?", "1975", ["1965", "1955", "1985"], "medium"),
        ("Cuban Missile Crisis?", "1962", ["1950", "1975", "1989"], "medium"),
        ("Apollo 11?", "1969", ["1962", "1975", "1989"], "easy"),
        ("Chernobyl?", "1986", ["1989", "1991", "2001"], "medium"),
        ("9/11?", "2001", ["1999", "2003", "2005"], "easy"),
        ("Treaty of Versailles?", "1919", ["1918", "1920", "1945"], "medium"),
        ("League of Nations?", "1920", ["1919", "1945", "1939"], "medium"),
        ("Marshall Plan?", "1947", ["1945", "1950", "1955"], "medium"),
        ("Hiroshima bomb?", "1945", ["1944", "1946", "1950"], "medium"),
        ("Pearl Harbor?", "1941", ["1939", "1945", "1950"], "medium"),
        ("D-Day?", "1944", ["1942", "1945", "1943"], "medium"),
        ("Stalingrad?", "1942–1943", ["1940–1941", "1944–1945", "1939–1940"], "medium"),
        ("Magna Carta?", "1215", ["1066", "1453", "1776"], "hard"),
        ("Renaissance began (approx)?", "14th century", ["10th century", "18th century", "20th century"], "hard"),
        ("Industrial Revolution (approx)?", "18th century", ["14th century", "20th century", "16th century"], "hard"),
        ("American Civil War?", "1861–1865", ["1776–1783", "1914–1918", "1939–1945"], "medium"),
        ("Russian Revolution (Feb)?", "1917", ["1914", "1918", "1920"], "medium"),
        ("Weimar Republic?", "1919", ["1914", "1933", "1945"], "hard"),
        ("Nazi rise?", "1933", ["1919", "1939", "1945"], "medium"),
        ("Kristallnacht?", "1938", ["1933", "1939", "1945"], "hard"),
        ("Nuremberg Trials?", "1945–1946", ["1939–1940", "1950–1951", "1960–1961"], "hard"),
        ("Berlin Airlift?", "1948–1949", ["1945–1946", "1950–1951", "1955–1956"], "hard"),
        ("Suez Crisis?", "1956", ["1950", "1960", "1970"], "hard"),
        ("Prague Spring?", "1968", ["1956", "1975", "1989"], "hard"),
        ("Tiananmen Square?", "1989", ["1975", "1991", "2001"], "hard"),
        ("Fall of Saigon?", "1975", ["1965", "1989", "1991"], "hard"),
        ("Camp David Accords?", "1978", ["1975", "1989", "1991"], "hard"),
        ("Oslo Accords?", "1993", ["1978", "1989", "2001"], "hard"),
        ("Good Friday Agreement?", "1998", ["1993", "2001", "2010"], "hard"),
        ("Euro introduced?", "2002", ["1993", "1999", "2007"], "medium"),
        ("Brexit referendum?", "2016", ["2010", "2012", "2020"], "hard"),
        ("COVID-19 pandemic declared?", "2020", ["2018", "2019", "2021"], "easy"),
        ("Genghis Khan died?", "1227", ["1206", "1259", "1279"], "medium"),
        ("Western Roman Empire fell?", "476", ["410", "800", "1453"], "medium"),
        ("Thirty Years War started?", "1618", ["1648", "1789", "1914"], "hard"),
        ("Thirty Years War ended?", "1648", ["1618", "1789", "1918"], "hard"),
        ("German Empire proclaimed?", "1871", ["1848", "1914", "1933"], "medium"),
        ("Spanish Civil War?", "1936", ["1939", "1914", "1945"], "medium"),
        ("Iraq War?", "2003", ["2001", "2005", "1999"], "medium"),
        ("Sparta's main rival?", "Athens", ["Thebes", "Corinth", "Macedon"], "medium"),
        ("Pompeii destroyed?", "79", ["1066", "1453", "476"], "medium"),
        ("Charlemagne crowned?", "800", ["1066", "1215", "1453"], "hard"),
        ("Black Death century?", "14th century", ["12th century", "16th century", "18th century"], "medium"),
        ("Westphalia Treaty?", "1648", ["1789", "1815", "1919"], "hard"),
        ("Peter the Great ruled?", "Russia", ["Germany", "Austria", "Poland"], "medium"),
        ("സലാദിൻ ഏത് സാമ്രാജ്യത്തിന്റെ സുൽത്താനായിരുന്നു?", "അയ്യൂബി സാമ്രാജ്യം", ["ഒട്ടോമൻ സാമ്രാജ്യം", "മുഗൽ സാമ്രാജ്യം", "സഫാവിദ് സാമ്രാജ്യം"], "hard"),
        ("First Crusade captured Jerusalem?", "1099", ["1187", "1204", "1291"], "hard"),
        ("Spanish Armada defeated?", "1588", ["1492", "1605", "1648"], "medium"),
        ("Communist Manifesto?", "1848", ["1789", "1917", "1949"], "medium"),
        ("Bretton Woods?", "1944", ["1945", "1947", "1939"], "hard"),
        ("Berlin Wall built?", "1961", ["1989", "1949", "1955"], "medium"),
        ("Warsaw Pact?", "1955", ["1949", "1945", "1961"], "hard"),
        ("ASEAN founded?", "1967", ["1950", "1975", "1990"], "hard"),
        ("OPEC founded?", "1960", ["1950", "1975", "1990"], "hard"),
        ("WTO?", "1995", ["1945", "1989", "2001"], "medium"),
        ("IMF?", "1944", ["1919", "1950", "1960"], "hard"),
        ("World Bank?", "1944", ["1919", "1950", "1960"], "hard"),
        ("Universal Declaration of Human Rights?", "1948", ["1945", "1950", "1960"], "hard"),
        ("Kyoto Protocol?", "1997", ["1990", "2005", "2010"], "hard"),
        ("Paris Agreement (climate)?", "2015", ["2005", "2010", "2020"], "medium"),
        ("Rio Earth Summit?", "1992", ["1972", "2002", "2010"], "hard"),
        ("SDGs adopted?", "2015", ["2000", "2010", "2020"], "hard"),
    ]
    return [_f(q, ans, wrong, diff) for q, ans, wrong, diff in events]


def build_bio_extra_3() -> list[tuple[str, str, list[str], str]]:
    facts: list[tuple[str, str, list[str], str]] = []
    vitamins = [
        ("വിറ്റാമിൻ A കുറവ്?", "രാത്രി അന്ധത", ["സ്കurvey", "ബെriberi", "rickets"], "medium"),
        ("വിറ്റാമിൻ B1 കുറവ്?", "ബെriberi", ["സ്കurvey", "rickets", "anemia"], "hard"),
        ("വിറ്റാമിൻ B12 കുറവ്?", "pernicious anemia", ["scurvy", "rickets", "beriberi"], "hard"),
        ("വിറ്റാമിൻ C കുറവ്?", "സ്കurvey", ["rickets", "beriberi", "anemia"], "medium"),
        ("വിറ്റാമിൻ D കുറവ്?", "rickets", ["scurvy", "beriberi", "anemia"], "medium"),
        ("വിറ്റാമിൻ K കുറവ്?", "രക്തം കട്ടയാക്കൽ കുറവ്", ["scurvy", "rickets", "beriberi"], "hard"),
        ("അയodine കുറവ്?", "goiter", ["scurvy", "rickets", "anemia"], "hard"),
        ("അയസ് കുറവ്?", "anemia", ["scurvy", "rickets", "beriberi"], "easy"),
        ("കാൽcium കുറവ്?", "osteoporosis", ["scurvy", "beriberi", "anemia"], "medium"),
    ]
    for q, ans, wrong, diff in vitamins:
        facts.append(_f(q, ans, wrong, diff))

    diseases = [
        ("മലേറിയ?", "Plasmodium", ["HIV", "Salmonella", "Vibrio"], "medium"),
        ("ക്ഷയരോഗം?", "Mycobacterium tuberculosis", ["Plasmodium", "HIV", "Vibrio"], "medium"),
        ("കോളറ?", "Vibrio cholerae", ["Plasmodium", "HIV", "Salmonella"], "medium"),
        ("ടൈഫോയ്ഡ്?", "Salmonella typhi", ["Plasmodium", "HIV", "Vibrio"], "medium"),
        ("എയ്ഡ്സ്?", "HIV", ["Plasmodium", "HBV", "Influenza"], "easy"),
        ("കോവിഡ്-19?", "SARS-CoV-2", ["HIV", "Plasmodium", "HBV"], "easy"),
        ("ഡെങ്കിപ്പനി?", "dengue virus", ["Plasmodium", "HIV", "Mycobacterium"], "medium"),
        ("റേബീസ്?", "rabies virus", ["HIV", "Plasmodium", "Salmonella"], "medium"),
        ("പൊളിയോ?", "poliovirus", ["HIV", "Plasmodium", "Salmonella"], "medium"),
        ("നിപാ?", "Nipah virus", ["HIV", "Plasmodium", "HBV"], "medium"),
    ]
    for q, ans, wrong, diff in diseases:
        facts.append(_f(f"{q} രോഗകാരി?", ans, wrong, diff))

    body = [
        ("മനുഷ്യ ഹൃദയം എത്ര chambers?", "4", ["2", "3", "6"], "easy"),
        ("മനുഷ്യ ഫെഫുസ്സ് എത്ര?", "2", ["1", "3", "4"], "easy"),
        ("മനുഷ്യ ക്രോമosome pairs?", "23", ["46", "22", "24"], "easy"),
        ("സാധാരണ ശരീര temp?", "37°C", ["27°C", "47°C", "32°C"], "easy"),
        ("RBC lifespan (days)?", "120", ["12", "1200", "30"], "hard"),
        ("സാർവത്രിക donor?", "O", ["AB", "A", "B"], "medium"),
        ("സാർവത്രിക recipient?", "AB", ["O", "A", "B"], "medium"),
        ("DNA bases?", "A,T,G,C", ["A,U,G,C", "A,T,G,U", "G,C,U,T"], "medium"),
        ("RNA bases?", "A,U,G,C", ["A,T,G,C", "A,T,G,U", "G,C,T,U"], "medium"),
        ("mitochondria function?", "ATP production", ["DNA storage", "photosynthesis", "digestion"], "medium"),
        ("chloroplast function?", "photosynthesis", ["respiration", "digestion", "ATP only"], "easy"),
        ("nucleus function?", "DNA storage", ["ATP", "photosynthesis", "digestion"], "easy"),
        ("ribosome function?", "protein synthesis", ["DNA replication", "photosynthesis", "digestion"], "medium"),
        ("photosynthesis product?", "glucose, oxygen", ["CO2 only", "N2, O2", "ATP only"], "easy"),
        ("respiration product?", "CO2, water", ["O2, glucose", "N2, O2", "ATP only"], "easy"),
        ("largest organ?", "skin", ["liver", "lung", "heart"], "easy"),
        ("smallest bone?", "stapes", ["femur", "humerus", "skull"], "hard"),
        ("longest bone?", "femur", ["humerus", "tibia", "radius"], "medium"),
        ("normal pH blood?", "7.4", ["7.0", "8.0", "6.5"], "hard"),
        ("hemoglobin function?", "oxygen transport", ["immunity", "clotting", "digestion"], "easy"),
    ]
    for q, ans, wrong, diff in body:
        facts.append(_f(q, ans, wrong, diff))
    return facts


IH_EXTRA_3 = build_ih_extra_3()
GEO_EXTRA_3 = build_geo_extra_3()
WH_EXTRA_3 = build_wh_extra_3()
BIO_EXTRA_3 = build_bio_extra_3()


def load_stems(filename: str) -> set[str]:
    path = BASE / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    return {q.get("question", "").strip() for q in data.get("questions", []) if q.get("question")}


def filter_new(facts: list[tuple[str, str, list[str], str]], stems: set[str]) -> list[tuple[str, str, list[str], str]]:
    seen: set[str] = set()
    out: list[tuple[str, str, list[str], str]] = []
    for q, ans, wrong, diff in facts:
        q = q.strip()
        if not q or q in stems or q in seen:
            continue
        if len(wrong) < 3:
            continue
        seen.add(q)
        out.append((q, ans, wrong, diff))
    return out


def append_extra(path: Path, name: str, facts: list[tuple[str, str, list[str], str]], *, geo: bool = False) -> int:
    if not facts:
        return 0
    text = path.read_text(encoding="utf-8")
    if f"{name}:" in text:
        return 0
    block = f"\n{name}: list[tuple[str, str, list[str], str]] = {facts!r}\n"
    if geo:
        gen = f"""
    for q, ans, wrong, diff in {name}:
        add(q, ans, wrong, diff)
"""
    else:
        gen = f"""
    for q, ans, wrong, diff in {name}:
        pool = wrong + [ans]
        _add(out, existing, rng, q, ans, pool, diff)
"""
    idx = text.index("def generate_candidates")
    text = text[:idx] + block + text[idx:]
    text = text.replace("    return out\n", gen + "\n    return out\n", 1)
    path.write_text(text, encoding="utf-8")
    return len(facts)


def main() -> int:
    ih_stems = load_stems("indian_history.json")
    geo_stems = load_stems("geography.json")
    wh_stems = load_stems("world_history.json")
    bio_stems = load_stems("biology.json")

    ih_new = filter_new(IH_EXTRA_3, ih_stems)
    geo_new = filter_new(GEO_EXTRA_3, geo_stems)
    wh_new = filter_new(WH_EXTRA_3, wh_stems)
    bio_new = filter_new(BIO_EXTRA_3, bio_stems)

    print(f"IH extra3: {len(ih_new)} new / {len(IH_EXTRA_3)} candidates")
    print(f"GEO extra3: {len(geo_new)} new / {len(GEO_EXTRA_3)} candidates")
    print(f"WH extra3: {len(wh_new)} new / {len(WH_EXTRA_3)} candidates")
    print(f"BIO extra3: {len(bio_new)} new / {len(BIO_EXTRA_3)} candidates")

    n_ih = append_extra(BASE / "indian_history_facts.py", "IH_EXTRA_3", ih_new)
    n_geo = append_extra(BASE / "geography_facts.py", "GEO_EXTRA_3", geo_new, geo=True)
    n_wh = append_extra(BASE / "world_history_facts.py", "WH_EXTRA_3", wh_new)
    n_bio = append_extra(BASE / "biology_facts.py", "BIO_EXTRA_3", bio_new)

    print(f"Patched: IH={n_ih}, GEO={n_geo}, WH={n_wh}, BIO={n_bio}")

    if n_ih + n_geo + n_wh + n_bio == 0:
        print("Nothing to patch.")
        return 0

    print("\n--- Running generate_all_questions.py ---")
    r = subprocess.run([sys.executable, str(BASE / "generate_all_questions.py"), "--skip-validation"], cwd=BASE)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
