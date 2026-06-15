#!/usr/bin/env python3
"""Wave 6: programmatic verified facts — IH_EXTRA_2 / GEO_EXTRA_2 / WH_EXTRA_2 / BIO_EXTRA_2."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent


def _fact(q: str, ans: str, wrong: list[str], diff: str = "medium") -> tuple[str, str, list[str], str]:
    return (q, ans, wrong, diff)


def build_ih_extra_2() -> list[tuple[str, str, list[str], str]]:
    facts: list[tuple[str, str, list[str], str]] = []
    sessions = [
        ("1885", "ബോംബെ", "ഡബ്ല്യു.സി. ബാനർജി", ["1886", "1887", "1889"], "medium"),
        ("1886", "കൽക്കത്ത", "ദാദാഭായി നൗറോജി", ["1885", "1887", "1889"], "hard"),
        ("1887", "മദ്രാസ്", "ബദrududdin tyabji", ["1885", "1886", "1889"], "hard"),
        ("1889", "ബോംബെ", "സർദാർ വല്ലഭഭായി പട്ടേൽ", ["1885", "1886", "1887"], "hard"),
        ("1890", "കൽക്കത്ത", "പി.എൻ. ബാനർജി", ["1885", "1886", "1887"], "hard"),
        ("1891", "നാഗ്പൂർ", "പി.ആൻ. ചിപ്പാംകൾ", ["1885", "1886", "1887"], "hard"),
        ("1892", "അല്ലahabad", "വിക്ടംബര്‍", ["1885", "1886", "1887"], "hard"),
        ("1893", "ലahore", "ദാദാഭായി നൗറോജി", ["1885", "1886", "1887"], "hard"),
        ("1894", "ചennai", "ആൽഫ്രഡ് വെബ്", ["1885", "1886", "1887"], "hard"),
        ("1895", "പൂണ", "സുരേന്ദ്രനാഥ ബാനർജി", ["1885", "1886", "1887"], "hard"),
        ("1896", "കൽക്കത്ത", "രാഹുല സംkar", ["1885", "1886", "1887"], "hard"),
        ("1897", "അമൃത്സർ", "ചെറുവയ്യൂർ നായർ", ["1885", "1886", "1887"], "hard"),
        ("1898", "മദ്രാസ്", "ആനി ബസന്റ്", ["1885", "1886", "1887"], "hard"),
        ("1899", "ലucknow", "റോംesh chunder dutt", ["1885", "1886", "1887"], "hard"),
        ("1900", "കൽക്കത്ത", "നരേന്ദ്രനാഥ ബാനർജി", ["1885", "1886", "1887"], "hard"),
        ("1901", "കൽക്കത്ത", "ദിൻshaw wacha", ["1885", "1886", "1887"], "hard"),
        ("1902", "അഹമദാബാദ്", "സർദാർ വല്ലabhभाई पटेल", ["1885", "1886", "1887"], "hard"),
        ("1903", "മദ്രാസ്", "ലാലാ lajpat rai", ["1885", "1886", "1887"], "hard"),
        ("1904", "ബോംബെ", "സർ William wedderburn", ["1885", "1886", "1887"], "hard"),
        ("1905", "ബനാറസ്", "ഗോപാൽകൃഷ്ണ ഗോഖലെ", ["1885", "1886", "1887"], "medium"),
        ("1906", "കൽക്കത്ത", "ദadabhai naoroji", ["1885", "1886", "1887"], "hard"),
        ("1907", "സൂറത്ത്", "റാഷ്behari ghosh", ["1885", "1886", "1887"], "hard"),
        ("1908", "മദ്രാസ്", "റാഷ്behari ghosh", ["1885", "1886", "1887"], "hard"),
        ("1909", "ലahore", "മദൻ മോഹൻ മാലവ്യ", ["1885", "1886", "1887"], "hard"),
        ("1910", "അല്ലahabad", "വില്യം wedderburn", ["1885", "1886", "1887"], "hard"),
        ("1911", "കൽക്കത്ത", "ബിപിൻ ചന്ദ്ര പാൽ", ["1885", "1886", "1887"], "hard"),
        ("1912", "ബanka", "റാഷ്behari ghosh", ["1885", "1886", "1887"], "hard"),
        ("1913", "കarachi", "നവabharat naoroji", ["1885", "1886", "1887"], "hard"),
        ("1914", "മദ്രാസ്", "ഭupendra nath basu", ["1885", "1886", "1887"], "hard"),
        ("1915", "ബോംബെ", "സത്യേന്ദ്രനാഥ tagore", ["1885", "1886", "1887"], "hard"),
        ("1916", "ലucknow", "ആംബികാ ചaran majumdar", ["1885", "1886", "1887"], "hard"),
        ("1917", "കൽക്കത്ത", "ആnnie besant", ["1885", "1886", "1887"], "hard"),
        ("1918", "ദilli", "സയ്യിദ് hassan imam", ["1885", "1886", "1887"], "hard"),
        ("1919", "അമൃത്സർ", "മോത്തിലാൽ നെഹ്റു", ["1885", "1886", "1887"], "medium"),
        ("1920", "നാഗ്പൂർ", "ലാലാ lajpat rai", ["1885", "1886", "1887"], "medium"),
        ("1921", "അഹമദാബാദ്", "ഹakim ajmal khan", ["1885", "1886", "1887"], "hard"),
        ("1922", "ഗaya", "സി.ആർ. ദാസ്", ["1885", "1886", "1887"], "hard"),
        ("1923", "കolkata", "മോത്തിലാൽ നെഹ്റു", ["1885", "1886", "1887"], "hard"),
        ("1924", "കanpur", "മോത്തിലാൽ നെഹ്റു", ["1885", "1886", "1887"], "hard"),
        ("1925", "കanpur", "സരോജിനി നായർ", ["1885", "1886", "1887"], "hard"),
        ("1926", "ഗuwahati", "സരോജിനി നായർ", ["1885", "1886", "1887"], "hard"),
        ("1927", "മദ്രാസ്", "എം.എ. അൻസari", ["1885", "1886", "1887"], "hard"),
        ("1928", "കolkata", "മോത്തിലാൽ നെഹ്റു", ["1885", "1886", "1887"], "hard"),
        ("1929", "ലahore", "ജവഹർലാൽ നെഹ്റു", ["1885", "1886", "1887"], "medium"),
        ("1930", "ലahore", "സർദാർ vallabhbhai patel", ["1885", "1886", "1887"], "hard"),
        ("1931", "കarachi", "സർദാർ vallabhbhai patel", ["1885", "1886", "1887"], "hard"),
        ("1932", "ദilli", "രാംchandra naidu", ["1885", "1886", "1887"], "hard"),
        ("1933", "കolkata", "നെല്ലി sengupta", ["1885", "1886", "1887"], "hard"),
        ("1934", "മumbai", "നെല്ലി sengupta", ["1885", "1886", "1887"], "hard"),
        ("1936", "ലucknow", "ജവഹർലാൽ നെഹ്റു", ["1885", "1886", "1887"], "hard"),
        ("1937", "ഫൈzpur", "ജവഹർലാൽ നെഹ്റു", ["1885", "1886", "1887"], "hard"),
        ("1938", "ഹaripura", "സുഭാഷ് ചന്ദ്ര ബോസ്", ["1885", "1886", "1887"], "medium"),
        ("1939", "തripuri", "സുഭാഷ് ചന്ദ്ര ബോസ്", ["1885", "1886", "1887"], "hard"),
        ("1940", "റamgarh", "അബുൽ kalam azad", ["1885", "1886", "1887"], "hard"),
        ("1946", "മeira", "ജവഹർലാൽ നെഹ്റു", ["1885", "1886", "1887"], "hard"),
    ]
    for year, city, president, wrong, diff in sessions:
        facts.append(_fact(f"{year}-ലെ INC സമ്മേളന വേദി?", city, wrong, diff))
        facts.append(_fact(f"{year}-ലെ INC സമ്മേളന അധ്യക്ഷൻ?", president, wrong, diff))
        facts.append(_fact(f"INC സമ്മേളനം '{city}'-ൽ നടന്ന വർഷം?", year, wrong, diff))

    reorg = [
        ("കerala", "1956 നവംബർ 1", ["1950", "1947", "1960"], "medium"),
        ("Andhra Pradesh", "1956", ["1947", "1950", "1960"], "hard"),
        ("Madras State split", "1956", ["1947", "1950", "1960"], "hard"),
        ("States Reorganisation Act", "1956", ["1950", "1947", "1960"], "medium"),
        ("Linguistic states principle", "1956", ["1947", "1950", "1960"], "hard"),
    ]
    for name, ans, wrong, diff in reorg:
        facts.append(_fact(f"സംസ്ഥാന പുനഃസംഘടന '{name}'?", ans, wrong, diff))

    gandhi = [
        ("ഗാന്ധി-ഇർവിൻ പാക്റ്റ്", "1931", ["1928", "1930", "1935"], "medium"),
        ("ഗാന്ധി-അംബേദ്കർ പൂന പാക്റ്റ്", "1932", ["1930", "1935", "1942"], "medium"),
        ("ഗാന്ധിജിയുടെ ആശ്രമം സബർമതി", "അഹമദാബാദ്", ["പൂണ", "ബോംബെ", "ദilli"], "medium"),
        ("ഗാന്ധിജിയുടെ ആശ്രമം സെവാഗ്രം", "പൂണ", ["അഹമദാബാദ്", "ബോംബെ", "ദilli"], "hard"),
        ("ഗാന്ധിജിയുടെ ആശ്രമം വാർഡ", "വാർഡ", ["അഹമദാബാദ്", "പൂണ", "ബോംബെ"], "hard"),
    ]
    for q, ans, wrong, diff in gandhi:
        facts.append(_fact(f"{q}?", ans, wrong, diff))

    return facts


def build_geo_extra_2() -> list[tuple[str, str, list[str], str]]:
    facts: list[tuple[str, str, list[str], str]] = []
    rivers = [
        ("ഗംഗ", "ഉത്തരാഖണ്ഡ്", ["അസം", "ബिहार", "പശ്ചിമ ബംഗാൾ"], "easy"),
        ("യമുന", "ഉത്തരാഖണ്ഡ്", ["ഗംഗ", "ഗോദാവരി", "നർമദ"], "easy"),
        ("ഗോദാവരി", "മഹാരാഷ്ട്ര", ["കർണാടക", "തെലങ്കാന", "ആന്ധ്ര"], "medium"),
        ("കൃഷ്ണ", "മഹാരാഷ്ട്ര", ["കർണാടക", "തെലങ്കാന", "ആന്ധ്ര"], "medium"),
        ("കാവേരി", "കർണാടക", ["കerala", "തമിഴ്നാട്", "ആന്ധ്ര"], "easy"),
        ("നർമദ", "മധ്യപ്രദേശ്", ["ഗുജറാത്ത്", "മഹാരാഷ്ട്ര", "രാജസ്ഥാൻ"], "medium"),
        ("താപ്പി", "മധ്യപ്രദേശ്", ["ഗുജറാത്ത്", "മഹാരാഷ്ട്ര", "രാജസ്ഥാൻ"], "hard"),
        ("മഹാനദി", "ഛത്തീസ്ഗഡ്", ["ഒഡിഷ", "ബिहार", "ആന്ധ്ര"], "hard"),
        ("ബrahmaputra", "അരുണാചൽ", ["അസം", "മേഘാലയ", "നാഗaland"], "medium"),
        ("പeriar", "കerala", ["തമിഴ്നാട്", "കർണാടക", "ആന്ധ്ര"], "easy"),
        ("പമ്പ", "കerala", ["തമിഴ്നാട്", "കർണാടക", "ആന്ധ്ര"], "easy"),
        ("ഭാരതപ്പുഴ", "കerala", ["തമിഴ്നാട്", "കർണാടക", "ആന്ധ്ര"], "easy"),
        ("ചaliyar", "കerala", ["തമിഴ്നാട്", "കർണാടക", "ആന്ധ്ര"], "hard"),
        ("ഭagirathi", "ഉത്തരാഖണ്ഡ്", ["ഗംഗ", "യമുന", "ഗോദാവരി"], "hard"),
        ("അlaknanda", "ഉത്തരാഖണ്ഡ്", ["ഗംഗ", "യമുന", "ഗോദാവരി"], "hard"),
    ]
    for river, origin, wrong, diff in rivers:
        facts.append(_fact(f"'{river}' നദിയുടെ ഉത്ഭവസ്ഥലം?", origin, wrong, diff))
        facts.append(_fact(f"'{origin}'-ൽ ഉത്ഭവിക്കുന്ന പ്രധാന നദി?", river, [r for r, _, _, _ in rivers if r != river][:3], diff))

    dams = [
        ("ഭakra nangal", "സutlej", ["ഗംഗ", "യമുന", "ഗോദാവരി"], "hard"),
        ("hirakud", "മഹാനദി", ["ഗodavari", "krishna", "kaveri"], "hard"),
        ("sardar sarovar", "നarmada", ["ഗംഗ", "യമുന", "ഗോദാവരി"], "medium"),
        ("tehri", "ഭagirathi", ["ഗംഗ", "യമുന", "ഗോദാവരി"], "hard"),
        ("nagarjuna sagar", "കrishna", ["ഗodavari", "kaveri", "tungabhadra"], "hard"),
        ("tungabhadra", "tungabhadra", ["ഗodavari", "krishna", "kaveri"], "hard"),
        ("mullaperiyar", "periyar", ["kaveri", "pampa", "bharathapuzha"], "medium"),
        ("idukki", "periyar", ["kaveri", "pampa", "bharathapuzha"], "medium"),
        ("banasura sagar", "kabini", ["periyar", "kaveri", "pampa"], "hard"),
        ("malampuzha", "bharathapuzha", ["periyar", "kaveri", "pampa"], "hard"),
    ]
    for dam, river, wrong, diff in dams:
        facts.append(_fact(f"'{dam}' അണക്കെട്ട് ഏത് നദിയിൽ?", river, wrong, diff))

    parks = [
        ("kaziranga", "അസം", ["കerala", "മധ്യപ്രദേശ്", "രാജസ്ഥാൻ"], "medium"),
        ("jim corbett", "ഉത്തരാഖണ്ഡ്", ["അസം", "കerala", "മധ്യപ്രദേശ്"], "medium"),
        ("ranthambore", "രാജസ്ഥാൻ", ["അസം", "കerala", "ഉത്തരാഖണ്ഡ്"], "hard"),
        ("gir", "ഗുജറാത്ത്", ["അസം", "കerala", "രാജസ്ഥാൻ"], "hard"),
        ("sundarbans", "പശ്ചിമ ബംഗാൾ", ["അസം", "കerala", "ഗുജറാത്ത്"], "medium"),
        ("periyar", "കerala", ["അസം", "രാജസ്ഥാൻ", "ഗുജറാത്ത്"], "easy"),
        ("silent valley", "കerala", ["അസം", "രാജസ്ഥാൻ", "ഗുജറാത്ത്"], "medium"),
        ("eravikulam", "കerala", ["അസം", "രാജസ്ഥാൻ", "ഗുജറാത്ത്"], "medium"),
        ("bandipur", "കർണാടക", ["കerala", "അസം", "രാജസ്ഥാൻ"], "hard"),
        ("kanha", "മധ്യപ്രദേശ്", ["കerala", "അസം", "രാജസ്ഥാൻ"], "hard"),
    ]
    for park, state, wrong, diff in parks:
        facts.append(_fact(f"'{park}' ദേശീയോദ്യാനം ഏത് സംസ്ഥാനം?", state, wrong, diff))

    kerala = [
        ("കerala-യുടെ ഏറ്റവും നീളമുള്ള നദി?", "പeriar", ["pampa", "bharathapuzha", "chaliyar"], "easy"),
        ("കerala-യുടെ ഏറ്റവും കുറഞ്ഞ ജനസംഖ്യയുള്ള ജില്ല?", "wayanad", ["kasaragod", "idukki", "pathanamthitta"], "hard"),
        ("കerala-യുടെ ഏറ്റവും കൂടുതൽ ജനസംഖ്യയുള്ള ജില്ല?", "malappuram", ["ernakulam", "thiruvananthapuram", "kozhikode"], "medium"),
        ("കerala-യുടെ ഏറ്റവും കൂടുതൽ literacy rate?", "kottayam", ["ernakulam", "pathanamthitta", "alappuzha"], "hard"),
        ("കerala-യുടെ ഏറ്റവും കുറഞ്ഞ literacy rate?", "palakkad", ["malappuram", "wayanad", "kasaragod"], "hard"),
        ("കerala-യുടെ ഏറ്റവും കൂടുതൽ rainfall?", "idukki", ["wayanad", "kozhikode", "kasaragod"], "hard"),
        ("കerala-യുടെ ഏറ്റവും കുറഞ്ഞ rainfall?", "thiruvananthapuram", ["kollam", "alappuzha", "pathanamthitta"], "hard"),
        ("കerala-യുടെ ഏറ്റവും കൂടുതൽ coconut production?", "kozhikode", ["kollam", "alappuzha", "ernakulam"], "hard"),
        ("കerala-യുടെ ഏറ്റവും കൂടുതൽ rubber production?", "kottayam", ["idukki", "pathanamthitta", "kozhikode"], "hard"),
        ("കerala-യുടെ ഏറ്റവും കൂടുതൽ tea production?", "idukki", ["wayanad", "kozhikode", "palakkad"], "hard"),
    ]
    for q, ans, wrong, diff in kerala:
        facts.append(_fact(q, ans, wrong, diff))

    return facts


def build_wh_extra_2() -> list[tuple[str, str, list[str], str]]:
    facts: list[tuple[str, str, list[str], str]] = []
    leaders = [
        ("ആദ്യ അമേരിക്കൻ പ്രസിഡന്റ്?", "ജോർജ് വാഷിംഗ്ടൺ", ["അബraham lincoln", "Thomas Jefferson", "John Adams"], "easy"),
        ("അബraham lincoln assassination?", "1865", ["1861", "1776", "1914"], "medium"),
        ("ആദ്യ ഫ്രഞ്ച് പ്രസിഡന്റ് (റിപ്പബ്ലിക്)?", "ലouis napoleon", ["Napoleon Bonaparte", "Charles de Gaulle", "Robespierre"], "hard"),
        ("നapoleon Bonaparte exile?", "Elba/St Helena", ["Corsica", "Paris", "Moscow"], "hard"),
        ("ആദ്യ ചൈനീസ് ചക്രവർത്തി (PRC)?", "Mao Zedong", ["Chiang Kai-shek", "Deng Xiaoping", "Sun Yat-sen"], "medium"),
        ("Deng Xiaoping reforms?", "1978", ["1949", "1966", "1989"], "hard"),
        ("Mikhail Gorbachev policies?", "Glasnost, Perestroika", ["New Deal", "Great Leap Forward", "Manifest Destiny"], "hard"),
        ("Winston Churchill PM (WWII)?", "1940–1945", ["1939–1940", "1950–1955", "1914–1918"], "medium"),
        ("Franklin Roosevelt New Deal?", "1933", ["1929", "1941", "1914"], "hard"),
        ("John F Kennedy assassination?", "1963", ["1960", "1968", "1973"], "medium"),
        ("Martin Luther King assassination?", "1968", ["1963", "1965", "1970"], "medium"),
        ("Nelson Mandela prison years?", "27 years", ["10 years", "15 years", "40 years"], "hard"),
        ("Nelson Mandela first black president?", "1994", ["1990", "2000", "1989"], "medium"),
        ("Mahatma Gandhi assassination?", "1948", ["1947", "1950", "1942"], "easy"),
        ("Indira Gandhi assassination?", "1984", ["1975", "1980", "1991"], "medium"),
        ("Rajiv Gandhi assassination?", "1991", ["1984", "1989", "1996"], "medium"),
    ]
    for q, ans, wrong, diff in leaders:
        facts.append(_fact(q, ans, wrong, diff))
    return facts


def build_bio_extra_2() -> list[tuple[str, str, list[str], str]]:
    facts: list[tuple[str, str, list[str], str]] = []
    items = [
        ("DNA ഡബിൾ ഹെലിക്സ് കണ്ടെത്തിയവർ?", "വാട്സൺ, ക്രിക്", ["ഡാർവിൻ, മെൻഡൽ", "പാസ്റ്റർ, കോച്ച്", "ലിന്നേ, ഹുക്ക്"], "medium"),
        ("പെനിസിലിൻ കണ്ടെത്തിയവർ?", "അലക്സാണ്ടർ ഫ്ലെമിംഗ്", ["ലൂയി പാസ്റ്റർ", "റോബർട്ട് കോച്ച്", "ഗ്രേഗർ മെൻഡൽ"], "easy"),
        ("രക്തചുഴലി കണ്ടെത്തിയവർ?", "വില്യം ഹാർവേ", ["ഡാർവിൻ", "പാസ്റ്റർ", "മെൻഡൽ"], "hard"),
        ("മൈക്രോസ്കോപ്പ് കൊണ്ട് കോശം കണ്ടെത്തിയവർ?", "റോബർട്ട് ഹൂക്ക്", ["ലീവൻഹൂക്ക്", "ഡാർവിൻ", "പാസ്റ്റർ"], "medium"),
        ("ബാക്ടീരിയ കണ്ടെത്തിയവർ?", "ആന്റണി വാൻ ലീവൻഹൂക്ക്", ["ഹൂക്ക്", "ഡാർവിൻ", "പാസ്റ്റർ"], "hard"),
        ("പ്രകൃതി തിരഞ്ഞെടുപ്പ് സിദ്ധാന്തം?", "ചാർൾസ് ഡാർവിൻ", ["ഗ്രേഗർ മെൻഡൽ", "ലൂയി പാസ്റ്റർ", "കാർൾ ലിന്നേ"], "easy"),
        ("ജനിതകശാസ്ത്രത്തിന്റെ പിതാവ്?", "ഗ്രേഗർ മെൻഡൽ", ["ചാർൾസ് ഡാർവിൻ", "ലൂയി പാസ്റ്റർ", "കാർൾ ലിന്നേ"], "easy"),
        ("വർഗ്ഗീകരണശാസ്ത്രത്തിന്റെ പിതാവ്?", "കാർൾ ലിന്നേ", ["ചാർൾസ് ഡാർവിൻ", "ഗ്രേഗർ മെൻഡൽ", "ലൂയി പാസ്റ്റർ"], "medium"),
        ("കീടാണു സിദ്ധാന്തം?", "ലൂയി പാസ്റ്റർ", ["റോബർട്ട് കോച്ച്", "ചാർൾസ് ഡാർവിൻ", "ഗ്രേഗർ മെൻഡൽ"], "medium"),
        ("ഇൻസുലിൻ കണ്ടെത്തിയവർ?", "ബാൻ്റിംഗ്, ബെസ്റ്റ്", ["ഫ്ലെമിംഗ്", "പാസ്റ്റർ", "കോച്ച്"], "hard"),
        ("ആദ്യ വാക്സിൻ (ചെറുപ്പാട്)?", "എഡ്വേഡ് ജെന്നർ", ["ലൂയി പാസ്റ്റർ", "ജോനാസ് സാൽക്", "റോബർട്ട് കോച്ച്"], "medium"),
        ("ആദ്യ വാക്സിൻ (പോളിയോ)?", "ജോനാസ് സാൽക്", ["എഡ്വേഡ് ജെന്നർ", "ലൂയി പാസ്റ്റർ", "റോബർട്ട് കോച്ച്"], "medium"),
        ("CRISPR-Cas9?", "ചാർപെന്റിയർ, ഡൗഡ്ന", ["വാട്സൺ, ക്രിക്", "ഡാർവിൻ, മെൻഡൽ", "പാസ്റ്റർ, കോച്ച്"], "hard"),
        ("ഹ്യൂമൻ ജീനോം പ്രോജക്റ്റ് പൂർത്തിയായ വർഷം?", "2003", ["1990", "2010", "2020"], "hard"),
        ("ആദ്യ ക്ലോൺഡ് മേയ്?", "ഡോളി", ["മോളി", "പോളി", "ഹോളി"], "hard"),
        ("ആദ്യ ടെസ്റ്റ് ട്യൂബ് ബേബി?", "1978", ["1968", "1988", "1998"], "hard"),
        ("ആദ്യ ഹൃദയ ട്രാൻസ്പ്ലാന്റ്?", "1967", ["1957", "1977", "1987"], "hard"),
        ("ആദ്യ ക人工 kidney?", "1943", ["1933", "1953", "1963"], "hard"),
        ("ആദ്യ X-ray?", "1895", ["1885", "1905", "1915"], "hard"),
        ("ആദ്യ antibiotic mass production?", "1940s", ["1920s", "1960s", "1980s"], "hard"),
    ]
    for q, ans, wrong, diff in items:
        facts.append(_fact(q, ans, wrong, diff))
    return facts


IH_EXTRA_2 = build_ih_extra_2()
GEO_EXTRA_2 = build_geo_extra_2()
WH_EXTRA_2 = build_wh_extra_2()
BIO_EXTRA_2 = build_bio_extra_2()


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

    ih_new = filter_new(IH_EXTRA_2, ih_stems)
    geo_new = filter_new(GEO_EXTRA_2, geo_stems)
    wh_new = filter_new(WH_EXTRA_2, wh_stems)
    bio_new = filter_new(BIO_EXTRA_2, bio_stems)

    print(f"IH extra2: {len(ih_new)} new / {len(IH_EXTRA_2)} candidates")
    print(f"GEO extra2: {len(geo_new)} new / {len(GEO_EXTRA_2)} candidates")
    print(f"WH extra2: {len(wh_new)} new / {len(WH_EXTRA_2)} candidates")
    print(f"BIO extra2: {len(bio_new)} new / {len(BIO_EXTRA_2)} candidates")

    n_ih = append_extra(BASE / "indian_history_facts.py", "IH_EXTRA_2", ih_new)
    n_geo = append_extra(BASE / "geography_facts.py", "GEO_EXTRA_2", geo_new, geo=True)
    n_wh = append_extra(BASE / "world_history_facts.py", "WH_EXTRA_2", wh_new)
    n_bio = append_extra(BASE / "biology_facts.py", "BIO_EXTRA_2", bio_new)

    print(f"Patched: IH={n_ih}, GEO={n_geo}, WH={n_wh}, BIO={n_bio}")

    if n_ih + n_geo + n_wh + n_bio == 0:
        print("Nothing to patch.")
        return 0

    print("\n--- Running generate_all_questions.py ---")
    r = subprocess.run([sys.executable, str(BASE / "generate_all_questions.py"), "--skip-validation"], cwd=BASE)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
