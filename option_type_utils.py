#!/usr/bin/env python3
"""Detect and fix quiz option type mismatches (e.g. year distractors on person questions)."""

from __future__ import annotations

import random
import re

# Century filler years used as bogus bulk distractors — never valid for person/place answers.
BOGUS_YEAR_DISTRACTORS = frozenset(
    {"1440", "1500", "1600", "1700", "1800", "1900", "1885", "1886", "1887", "1889"}
)

PURE_YEAR = re.compile(r"^\d{3,4}$")
PURE_NUMERIC = re.compile(r"^[\d°₹,.%+\-–—/\s]+(?:°|%)?$")

MALAYALAM_MONTHS = frozenset(
    {
        "ജനുവരി", "ഫെബ്രുവരി", "മാർച്ച്", "ഏപ്രിൽ", "മേയ്", "ജൂൺ",
        "ജൂലൈ", "ഓഗസ്റ്റ്", "സെപ്റ്റംബർ", "ഒക്ടോബർ", "നവംബർ", "ഡിസംബർ",
    }
)

MONTH_Q = re.compile(r"മാസം\s*ഏത്|ഏത്\s*മാസ|which\s*month", re.I)

AWARD_DESC = re.compile(
    r"സിവിലിയൻ ബഹുമതി|സാഹിത്യ ബഹുമതി|കായിക ബഹുമതി|ദേശീയ ബഹുമതി|"
    r"പരിശീലകർക്കുള്ള|മേഖലകളിലെ ബഹുമതി|ഉയർന്ന\s+.*ബഹുമതി",
)

AWARD_NAME_Q = re.compile(r"പുരസ്കാര|അവാർഡ|ബഹുമതി|സമ്മാന", re.I)

AWARD_OPTION = re.compile(
    r"പുരസ്കാര|അവാർഡ|ബഹുമതി|ഖേൽ രത്ന|പുലിറ്റ്സർ|ഓസ്കാർ|ട്യൂറിംഗ്|"
    r"ഫാൽക്കെ|ഭാരതരത്ന|പത്മ(?:ശ്രീ|ഭൂഷൺ|വിഭൂഷൺ)|ബുക്കർ|ഫീൽഡ്സ്|"
    r"ആൽഫ്രഡ് നോബൽ|ഗോൾഡൻ ഗ്ലോബ്|എമ്മി",
    re.I,
)

PERSON_Q = re.compile(
    r"ആരാണ്|ആര്\?|ആരായിരുന്നു|ആരെ\s|ആരുടെ|"
    r"പ്രസിഡന്റ്|പ്രധാനമന്ത്രി|രാജാവ്|രാജ്ഞി|ചക്രവർത്തി|"
    r"സ്ഥാപകൻ|കണ്ടെത്തിയ|കണ്ടെത്തിയത്|കണ്ടുപിടിച്ച|നേതാവ്|"
    r"രചിച്ചത്\s+ആര|സ്ഥാപിച്ചത്\s+ആര|ഭരിച്ച|"
    r"ആദ്യ(?:ത്തെ|മ)?\s*(?:കറുത്ത|വനിത|മനുഷ്യ|ഇന്ത്യൻ|ആഫ്രിക്കൻ|"
    r"അമേരിക്കൻ|ബ്രിട്ടീഷ്|ഫ്രഞ്ച്|റഷ്യൻ|ചൈനീസ്|ജർമൻ|"
    r"വനിത|പുരുഷ|നടൻ|നടി|രചയിതാവ്|കവി|ശാസ്ത്രജ്ഞൻ|"
    r"സൈനികൻ|സൈനികനായ|നാവികൻ|"
    r"അധ്യക്ഷൻ|സുൽത്താൻ|ചancellor|discovered by|who|founder|president|author)",
    re.I,
)

PLACE_Q = re.compile(
    r"ഏത്\s*(?:രാജ്യ|നഗര|സംസ്ഥാന|ജില്ല|ദ്വീപ|നദി|"
    r"തലസ്ഥാന|ആസ്ഥാന|ഭൂഖണ്ഡ|ഖണ്ഡ|സ്ഥല|സ്ഥാന|സ്ഥലം|"
    r"വേദി|നഗരത്തിൽ|രാജ്യത്തിൽ|ഗ്രഹം|ഉപഗ്രഹ)|"
    r"(?:രാജ്യ|നഗര|സംസ്ഥാന|ജില്ല|തലസ്ഥാന|ദ്വീപ)ം?\s*ഏത്|"
    r"നൽകുന്ന\s*രാജ്യം\s*ഏത്",
    re.I,
)

YEAR_Q = re.compile(
    r"വർഷം|ഏത്\s*വർഷ|എപ്പോ|എത്ര\s*വർഷ|year|when|date|"
    r"തീയതി|ആരംഭിച്ച|നടന്ന|ഇടിച്ചുമറിച്ച|പൊട്ടിത്തെറിച്ച|"
    r"സ്വാതന്ത്ര്യ|വിപ്ലവം.*വർഷ|മഹായുദ്ധം.*വർഷ|"
    r"ഏത്\s*നൂറ്റാണ്ട|ദശാബ്ദ",
    re.I,
)

WH_PERSONS = [
    "നെൽസൺ മണ്ടേല", "ജോർജ് വാഷിംഗ്ടൺ", "അബ്രഹാം ലിങ്കൺ", "തോമസ് ജെഫേഴ്സൺ",
    "വ്ലാഡിമിർ ലെനിൻ", "ജോസഫ് സ്റ്റാലിൻ", "മിഖായിൽ ഗോർബച്ചോവ്", "മാവോ സെതുങ്",
    "ദെങ്ക് സിയാപിങ്", "നീൽ ആംസ്ട്രോങ്", "യൂറി ഗഗാരിൻ", "വാലന്റീന ടെരഷ്കോവ",
    "തോമസ് എഡിസൺ", "അലക്സാണ്ടർ ഗ്രഹം ബെൽ", "ഗുലീൽമോ മാർക്കോണി", "ജോഹാൻ ഗുട്ടൻബർഗ്",
    "മാർട്ടിൻ ലൂഥർ", "വോൾട്ടയർ", "നെപ്പോളിയൻ ബോണപ്പാർട്ട്", "മാക്സിമില്യൻ റോബസ്പിയർ",
    "ഹിറ്റ്ലർ", "മൗസോളിനി", "വിൻസ്റ്റൺ ചർച്ചിൽ", "ഫ്രാങ്ക്ലിൻ ഡി. റൂസവെൽട്ട്",
    "ജോൺ എഫ്. കെന്നഡി", "മാർട്ടിൻ ലൂഥർ കിംഗ് ജൂനിയർ", "ട്രൈഗ്വേ ലൈ",
    "ജ്യൂസെപ്പ് പിയാസി", "മാർട്ടിൻ ഷ്മിഡ്", "നിക്കോളസ് കോപ്പർണിക്കസ്",
    "എ.പി.ജെ. അബ്ദുൽ കലാം", "അഗസ്റ്റസ് സീസർ", "ടൂട്ടങ്കാമുൻ", "ബാബർ", "ഷാഹ് ജഹാൻ",
    "അക്ബർ", "മഹാത്മാ ഗാന്ധി", "ജവഹർലാൽ നെഹ്റു", "സുഭാഷ് ചന്ദ്ര ബോസ്",
    "സർദാർ വല്ലഭഭായി പട്ടേൽ", "ബാല ഗംഗാധർ തിലക്", "ഗൗതമ ബുദ്ധൻ", "മഹാവീരൻ",
    "മുഹമ്മദ് നബി", "യേശു ക്രിസ്തു", "ചാർlemagne", "റിച്ചാർഡ് ദി ലയൺഹാർട്ട്",
    "ജോയൻ ഓഫ് ആർക്ക്", "പീറ്റർ ദി ഗ്രേറ്റ്", "കാതറിൻ ദി ഗ്രേറ്റ്",
    "ഫെ.ഡബ്ല്യു. ഡി ക്ലർക്ക്", "താബോ മbeki", "സിരിൽ റാമാഫോസ",
]

WH_COUNTRIES = [
    "ജർമ്മനി", "ഇറ്റലി", "ഫ്രാൻസ്", "ഇംഗ്ലണ്ട്", "അമേരിക്ക", "ജപ്പാൻ", "റഷ്യ",
    "ചൈന", "ഇന്ത്യ", "പോർച്ചുഗൽ", "സ്പെയിൻ", "ബ്രിട്ടൻ", "ഓട്ടോമൻ", "മുഗൾ",
    "ഓസ്ട്രിയ", "പോളണ്ട്", "ആഫ്രിക്ക", "ദക്ഷിണാഫ്രിക്ക", "ഓസ്ട്രേലിയ",
    "ബാബിലോണിയ", "ഗ്രീസ്", "റോം", "മാസിഡോണിയ", "സോവിയറ്റ് യൂണിയൻ",
    "ക്യൂബ", "ഇറാൻ", "ഇറാഖ്", "മെക്സിക്കോ", "കാനഡ", "ബെൽജിയം",
    "നോർവേ", "സ്വീഡൻ", "ഡെൻമാർക്ക്", "ഫിൻലാന്റ്", "ഐസ്ലാൻഡ്", "നെതർലാൻഡ്",
    "സ്വിറ്സർലാൻഡ്",
]

WH_CITIES = [
    "ബെർlin", "റോം", "പാരീസ്", "ലണ്ടൻ", "വാഷിംഗ്ടൺ", "അഥീൻസ്", "ജനീവ",
    "സരാജെവോ", "ഒളിമ്പിയ", "കരാക്കോറം", "ഷിയാൻ", "ഫിലാഡൽഫിയ",
    "ബോസ്റ്റൺ", "ന്യൂയോർക്ക്", "ലാഹോർ", "കാൻപൂർ", "ലഖ്നൗ", "ചെന്നൈ",
    "കൊൽക്കത്ത", "മുംബൈ", "നാഗ്പൂർ", "അമൃത്സർ", "സൂറത്ത്", "അഹമദാബാദ്",
    "പൂണ", "ഗയ", "ഹരിപുര", "ബanka", "ദില്ലി", "മeira",
]

INC_PRESIDENTS = [
    "ഡബ്ല്യു.സി. ബാനർജി", "ദാദാഭായി നൗറോജി", "ബദrududdin tyabji",
    "സർദാർ വല്ലഭഭായി പട്ടേൽ", "പി.എൻ. ബാനർജി", "പി.ആൻ. ചിപ്പാംകൾ",
    "സുരേന്ദ്രനാഥ ബാനർജി", "ചെറുവയ്യൂർ നായർ", "ആനി ബസന്റ്",
    "ഗോപാൽകൃഷ്ണ ഗോഖലെ", "മദൻ മോഹൻ മാലവ്യ", "ബിപിൻ ചന്ദ്ര പാൽ",
    "ജവഹർലാൽ നെഹ്റു", "സുഭാഷ് ചന്ദ്ര ബോസ്", "മോത്തിലാൽ നെഹ്റു",
    "സി.ആർ. ദാസ്", "സരോജിനി നായർ", "ലാലാ lajpat rai", "ആൽഫ്രഡ് വെബ്",
    "അബുൽ kalam azad",
]

INC_VENUES = [
    "ബോംബെ", "കൽക്കത്ത", "മദ്രാസ്", "നാഗ്പൂർ", "അല്ലahabad", "ലahore",
    "ചennai", "പൂണ", "അമൃത്സർ", "ലucknow", "അഹമദാബാദ്", "സൂറത്ത്",
    "ബanka", "കarachi", "ഗaya", "കanpur", "ഗuwahati", "ഹaripura",
    "തripuri", "റamgarh", "മeira", "ദilli", "മumbai", "ബനാറസ്", "ഫൈzpur",
]

INC_YEARS = [
    "1885", "1886", "1887", "1889", "1890", "1891", "1892", "1893", "1894",
    "1895", "1896", "1897", "1898", "1899", "1900", "1901", "1902", "1903",
    "1904", "1905", "1906", "1907", "1908", "1909", "1910", "1911", "1912",
    "1913", "1914", "1915", "1916", "1917", "1918", "1919", "1920", "1921",
    "1922", "1923", "1924", "1925", "1926", "1927", "1928", "1929", "1930",
    "1931", "1932", "1933", "1934", "1936", "1937", "1938", "1939", "1940", "1946",
]

DEFINITION_Q = re.compile(r"എന്ത്\?|എന്താണ്\?|എന്ന് പറയുന്നത് എന്ത്")

INDIAN_NATIONAL_SYMBOLS = frozenset(
    {"ആൽമരം", "താമര", "മാമ്പഴം", "മയിൽ", "കടുവ", "പേരാൽ"},
)

NON_PERSON_GARBAGE = INDIAN_NATIONAL_SYMBOLS | frozenset(
    {"ശക കലണ്ടർ", "ഗ്രെഗോറിയൻ കലണ്ടർ"},
)

AWARD_DEFINITION_POOL = [
    "ഇന്ത്യയിലെ പരമോന്നത സിവിലിയൻ ബഹുമതി",
    "ഇന്ത്യയുടെ രണ്ടാമത്തെ ഉയർന്ന സിവിലിയൻ ബഹുമതി",
    "ഇന്ത്യയുടെ മൂന്നാമത്തെ ഉയർന്ന സിവിലിയൻ ബഹുമതി",
    "ഇന്ത്യയുടെ നാലാമത്തെ ഉയർന്ന സിവിലിയൻ ബഹുമതി",
]

INDIAN_NOTABLE_PERSONS = [
    "ഡോ. രാജേന്ദ്ര പ്രസാദ്", "ജവാഹർലാൽ നെഹ്റു", "സരോജിനി നായഡു", "വിജയലക്ഷ്മി പണ്ഡിറ്റ്",
    "ഇന്ദിരാ ഗാന്ധി", "രവീന്ദ്രനാഥ ടാഗോർ", "സി.വി. രാമൻ", "എ.പി.ജെ. അബ്ദുൾ കലാം",
    "രാജീവ് ഗാന്ധി", "ജനറൽ ബിപിൻ റാവത്ത്", "ഫീൽഡ് മാർഷൽ സമ് മാനേക്ഷവർ",
    "ജനറൽ കെ. എം. കാരിയപ്പ", "സുഭാഷ് ചന്ദ്ര ബോസ്", "സർദാർ വല്ലഭഭായി പട്ടേൽ",
    "ചന്ദ്രശേഖർ ആസാദ്", "ലാല ബഹാദൂർ ശാസ്ത്രി",
]

INDIAN_WOMEN_POOL = [
    "ഇന്ദിരാ ഗാന്ധി", "സരോജിനി നായഡു", "സരോജിനി നായിഡു", "വിജയലക്ഷ്മി പണ്ഡിറ്റ്",
    "മദർ തെരേസ", "കൽപ്പന ചൗള", "പ്രതിഭാ പാട്ടീൽ", "സുധാ മൂർത്തി",
    "അമൃത ക്ഷിപ്രാണി", "സുനിതാ വില്യംസ്", "കെ.ആർ. ഗൗരിയമ്മ", "മേരി കോം",
]

INDIAN_WOMEN_SET = frozenset(INDIAN_WOMEN_POOL)

INDIAN_MEN_POOL = [
    p for p in INDIAN_NOTABLE_PERSONS if p not in INDIAN_WOMEN_SET
] + [
    "ഡോ. ബി.ആർ. അംബേദ്കർ", "മഹാത്മാ ഗാന്ധി", "മഹാത്മാഗാന്ധി", "ജവാഹർലാൽ നെഹ്റു",
    "സർദാർ വല്ലഭഭായി പട്ടേൽ", "സുഭാഷ് ചന്ദ്ര ബോസ്", "ലാല ബഹാദൂർ ശാസ്ത്രി",
    "രവീന്ദ്രനാഥ ടാഗോർ", "സി.വി. രാമൻ", "ഡോ. രാജേന്ദ്ര പ്രസാദ്", "രാജീവ് ഗാന്ധി",
    "ചന്ദ്രശേഖർ ആസാദ്", "എ.പി.ജെ. അബ്ദുൾ കലാം", "ജനറൽ ബിപിൻ റാവത്ത്",
    "ജനറൽ കെ. എം. കാരിയപ്പ", "ഫീൽഡ് മാർഷൽ സമ് മാനേക്ഷവർ",
    "അലക്സാണ്ടർ ഗ്രഹാം ബെൽ", "തോമസ് അൽവ എഡിസൺ", "തോമസ് ആൽവ എഡിസൺ",
]

INDIAN_MEN_SET = frozenset(INDIAN_MEN_POOL)

WOMAN_Q = re.compile(r"വനിത[\s?.，]|വനിതാ|അധ്യക്ഷയായ")

INVENTOR_POOL = [
    "ജെയിംസ് വാട്ട്", "റൈറ്റ് സഹോദരന്മാർ", "ജോൺ ലോഗി ബെയർഡ്", "തോമസ് അൽവ എഡിസൺ",
    "അലക്സാണ്ടർ ഗ്രഹം ബെൽ", "ജോഹാൻസ് ഗുട്ടൻബർഗ്", "എഡ്വേഡ് ജെന്നർ", "അലക്സാണ്ടർ ഫ്ലെമിംഗ്",
    "തോമസ് എഡിസൺ", "ഗുലീൽമോ മാർക്കോണി", "ഐസക് ന്യൂട്ടൺ",
]

MOUNTAINEER_POOL = [
    "എഡ്മണ്ട് ഹിലാരി", "ടെൻസിൻ നോർഗേ", "റൈൻഹോൾഡ് മെസ്നർ", "ബങ്കിംചന്ദ്ര ചട്ടോപാധ്യായ",
    "എഡ്മണ്ട് ഹിലാരി", "ടെൻസിങ് നോർഗേ",
]

INVENTOR_SET = frozenset(INVENTOR_POOL)

# Pools for astronomy option repair (same semantic kind as answer).
ASTRO_PERIOD_POOL = [
    "9-14 വർഷം", "1-2 വർഷം", "11 വർഷം", "27.3 ദിവസം", "23 മണിക്കൂർ 56 മിനിറ്റ്",
    "365.25 ദിവസം", "27 ദിവസം", "365 ദിവസം", "225 ദിവസം", "88 ദിവസം",
    "687 ദിവസം", "12 വർഷം", "29 വർഷം", "84 വർഷം", "165 വർഷം", "248 വർഷം",
    "90 മിനിറ്റ്", "76 വർഷം",
]
ASTRO_AU_POOL = ["2.2 AU", "3.2 AU", "50 AU", "2000 AU", "1 AU"]
ASTRO_SPEED_POOL = [
    "400 കി.മീ./സെ.", "2 കി.മീ./സെ.", "7.66 കി.മീ./സെ.",
]
ASTRO_YEAR_POOL = [
    "1609", "1668", "1789", "1917", "1948", "1990", "2021", "2019", "2011",
    "1998", "1993", "2016", "2015", "1989", "2013", "2008", "2014", "2023",
    "1997", "2005", "1986", "2061",
]
ASTRO_LAGRANGE_POOL = ["L1", "L2", "L3", "L4", "L5"]
ASTRO_DIRECTION_POOL = [
    "കിഴക്കുനിന്ന് പടിഞ്ഞാറോട്ട്", "പടിഞ്ഞാറുനിന്ന് കിഴക്കോട്ട്",
    "അക്ഷം ഏതാണ്ട് തിരിച്ച്", "ഭ്രമണ ദിശ വ്യത്യസ്തം", "വിപരീത ഭ്രമണ ദിശ",
]
ASTRO_DIAMETER_POOL = [
    "4879 കി.മീ.", "12104 കി.മീ.", "12742 കി.മീ.", "6779 കി.മീ.",
    "139820 കി.മീ.", "116460 കി.മീ.", "50724 കി.മീ.", "49244 കി.മീ.",
]
ASTRO_DIAMETER_NUM_POOL = ["4879", "12104", "12742", "6779", "139820", "116460", "50724", "49244"]
ASTRO_DISTANCE_LY_POOL = [
    "4.37", "8.6", "11.46", "37", "51", "59", "83", "93", "116", "250", "310",
    "642", "1200", "1300", "179", "268", "303", "431", "2615",
]
ASTRO_MISSION_TYPE_POOL = [
    "നാവിഗേഷൻ", "വിദ്യാഭ്യാസ ഉപഗ്രഹം", "ഭൂമി നിരീക്ഷണം", "ബഹിരാകാശ ദൂരദർശിനി",
    "മെസോസ്ഫിയർ പഠനം", "റഡാർ ഇമേജിംഗ്", "സമുദ്ര പഠനം", "ഹൈപ്പർസ്പെക്ട്രൽ ഇമേജിംഗ്",
    "എക്സ്-റേ പോളാരിമെട്രി", "ഇലക്ട്രോമാഗ്നറ്റിക് ഇന്റലിജൻസ്",
]
ASTRO_MISSION_GOAL_POOL = [
    "സൂര്യൻ", "ചന്ദ്രൻ", "ചൊവ്വ", "മംഗൾ ഗ്രഹം", "ഭൂമി",
    "മനുഷ്യ ബഹിരാകാശ യാത്ര",
]
ASTRO_LANDER_POOL = ["വിക്രം", "പ്രജ്ഞാൻ", "പെർസിവറൻസ്", "ക്യൂരിയോസിറ്റി"]
ASTRO_MODULE_POOL = ["Zarya", "കുവോൺ", "നൗക", "Destiny", "Harmony", "Columbus"]
ASTRO_PERSON_POOL = [
    "ജൊഹാൻ കെപ്ലർ", "സുബ്രഹ്മണ്യൻ ചന്ദ്രശേഖർ", "വിക്രം സാരാഭായി", "എ.പി.ജെ. അബ്ദുൾ കലാം",
    "വാലന്റീന ടെരഷ്കോവ", "കൽപ്പന ചൗള", "നീൽ ആംസ്ട്രോങ്", "യൂറി ഗഗാരിൻ",
    "ഗലീലിയോ ഗലീലി", "എഡ്വിൻ ഹബിൾ", "സ്റ്റീഫൻ ഹോക്കിംഗ്", "അല്ബർട്ട് ഐൻസ്റ്റീൻ",
]
ASTRO_LANDING_SITE_POOL = [
    "ട്രാൻക്വിലിറ്റി ബേസിൻ", "ടൗറസ്-ലിറ്റ്രോ", "ഹാഡ്ലി-റിൽ", "ഡെസ്കാർട്ടസ്",
    "ദക്ഷിണ ധ്രുവം", "ക്രിസേ മേഖല", "ജെസീറോ ക്രേറ്റർ", "ഗെയ്‌ൽ ക്രേറ്റർ", "മെരിഡിയാനി പ്ലാനം",
]
ASTRO_PLANET_POOL = [
    "ബുധൻ", "ശുക്രൻ", "ഭൂമി", "ചൊവ്വ", "വ്യാഴം", "ശനി", "യുറാനസ്", "നെപ്റ്റ്യൂൺ",
    "ജൂപിറ്റർ", "മംഗൾ ഗ്രഹം", "പ്ലൂട്ടോ",
]
ASTRO_CONCEPT_POOL = ["മൈക്രോഗ്രാവിറ്റി", "സൺസ്പോട്ട് കൂടുതൽ", "സൺസ്പോട്ട് കുറവ്"]
ASTRO_REGION_POOL = [
    "ആസ്ട്രോയിഡ് ബെൽറ്റ് (ക്ഷുദ്രഗ്രഹ മേഖല)", "കൈപ്പർ ബെൽറ്റ്", "ഓർട്ട് മേഘം",
    "സ്കാറ്റേഡ് ബെൽറ്റ്", "ക്ഷുദ്രഗ്രഹ വലയം", "ജൂപിറ്ററിന്റെ L4/L5",
]
ASTRO_MISSION_NAME_POOL = [
    "IRS-1എ", "INSAT-2A", "XPoSat", "GSAT-1", "EMISAT", "ചന്ദ്രയാൻ-1", "ചന്ദ്രയാൻ-3",
    "മംഗള്യാൻ", "ആദിത്യ-എൽ1", "ആസ്ട്രോസാറ്റ്", "IRNSS-1A", "സരാൾ", "ഹൈസിസ്",
]
ASTRO_ASTEROID_NUM_POOL = [
    "1", "2", "4", "433", "951", "4179", "162173", "99942", "1999", "2005",
]
ASTRO_DISTANCE_LY_LARGE_POOL = [
    "100000 പ്രകാശവർഷം", "200000 പ്രകാശവർഷം", "50000 പ്രകാശവർഷം", "10000 പ്രകാശവർഷം",
]

ASTRO_DISTANCE_LY_INT_POOL = [
    "4", "8", "10", "11", "25", "33", "37", "48", "51", "59", "65", "66", "68", "79",
    "81", "83", "88", "93", "97", "99", "116", "179", "250", "268",
]
ASTRO_COUNT_POOL = [
    "0", "1", "2", "4", "5", "8", "10", "14", "16", "27", "28", "67", "88", "200",
]
ASTRO_MASS_RATIO_POOL = [
    "0.0123", "0.055", "0.08", "0.107", "0.39", "0.46", "0.61", "0.76", "0.815", "0.85",
    "14.5", "95.2", "318",
]
ASTRO_MASS_NUM_POOL = [
    "333000", "4879", "6779", "12104", "12742", "49244", "50724", "139820", "116460",
]

ASTRO_KIND_POOLS: dict[str, list[str]] = {
    "period": ASTRO_PERIOD_POOL,
    "au": ASTRO_AU_POOL,
    "speed": ASTRO_SPEED_POOL,
    "year": ASTRO_YEAR_POOL,
    "lagrange": ASTRO_LAGRANGE_POOL,
    "direction": ASTRO_DIRECTION_POOL,
    "diameter": ASTRO_DIAMETER_POOL,
    "diameter_num": ASTRO_DIAMETER_NUM_POOL,
    "distance_ly": ASTRO_DISTANCE_LY_POOL,
    "distance_ly_large": ASTRO_DISTANCE_LY_LARGE_POOL,
    "distance_ly_int": ASTRO_DISTANCE_LY_INT_POOL,
    "mission_type": ASTRO_MISSION_TYPE_POOL,
    "planet": ASTRO_PLANET_POOL,
    "concept": ASTRO_CONCEPT_POOL,
    "place": ASTRO_REGION_POOL,
    "mission_name": ASTRO_MISSION_NAME_POOL,
    "mission_goal": ASTRO_MISSION_GOAL_POOL,
    "lander_name": ASTRO_LANDER_POOL,
    "module_name": ASTRO_MODULE_POOL,
    "landing_site": ASTRO_LANDING_SITE_POOL,
    "asteroid_num": ASTRO_ASTEROID_NUM_POOL,
    "count": ASTRO_COUNT_POOL,
    "mass_ratio": ASTRO_MASS_RATIO_POOL,
    "mass_num": ASTRO_MASS_NUM_POOL,
}

ASTRO_PERIOD_RE = re.compile(r"വർഷം|ദിവസം|മിനിറ്റ്|മണിക്കൂർ")
ASTRO_AU_RE = re.compile(r"\bAU\b")
ASTRO_SPEED_RE = re.compile(r"കി\.മീ\./സെ")
ASTRO_LY_RE = re.compile(r"പ്രകാശവർഷം")
ASTRO_DIRECTION_RE = re.compile(
    r"കിഴക്കുനിന്ന്|പടിഞ്ഞാറുനിന്ന്|കിഴക്ക്|പടിഞ്ഞാറ്|അക്ഷം|ഭ്രമണ ദിശ",
)


def is_bare_month(opt: str) -> bool:
    return opt.strip() in MALAYALAM_MONTHS


def is_month_name(opt: str) -> bool:
    o = opt.strip()
    if o in MALAYALAM_MONTHS:
        return True
    return any(o.startswith(m + " ") for m in MALAYALAM_MONTHS)


def is_award_description(opt: str) -> bool:
    return bool(AWARD_DESC.search(opt))


def is_award_option(opt: str) -> bool:
    return is_award_description(opt) or bool(AWARD_OPTION.search(opt))


def is_woman_question(question: str) -> bool:
    return bool(WOMAN_Q.search(question))


def is_male_person_option(name: str) -> bool:
    text = name.strip()
    if text in INDIAN_WOMEN_SET:
        return False
    if text in INDIAN_MEN_SET or text in INVENTOR_SET:
        return True
    return bool(
        re.search(
            r"ജനറൽ|മഹാത്മാ|അംബേദ്കർ|അബ്ദുൾ കലാം|ചന്ദ്രശേഖർ|നെഹ്റു|പട്ടേൽ|"
            r"രാജേന്ദ്ര|ബോസ്|ശാസ്ത്രി|ടാഗോർ|രാമൻ|എഡിസൺ|ബെൽ|വാട്ട്|"
            r"ബിപിൻ|കാരിയപ്പ|മാനേക്ഷവർ|റാവത്ത്|ഗ്രഹാം ബെൽ|ജെന്നർ|ഗുട്ടൻബർഗ്|ഫ്ലെമിംഗ്",
            text,
        )
    )


def is_pure_year(opt: str) -> bool:
    return bool(PURE_YEAR.match(opt.strip()))


def is_pure_numeric(opt: str) -> bool:
    return bool(PURE_NUMERIC.match(opt.strip()))


def has_malayalam_text(opt: str) -> bool:
    return bool(re.search(r"[\u0D00-\u0D7F]", opt))


def is_year_answer(answer: str) -> bool:
    a = answer.strip()
    if "പ്രകാശവർഷം" in a:
        return False
    if PURE_YEAR.match(a):
        return True
    if re.match(r"^\d{3,4}[–\-]\d{2,4}$", a):
        return True
    if ASTRO_PERIOD_RE.search(a) and not PURE_YEAR.match(a):
        return False
    if re.search(r"\d{3,4}", a) and YEAR_Q.search(a):
        return True
    return False


def classify_answer_kind(question: str, answer: str) -> str:
    """Return: year | numeric | month | person | place | text."""
    if is_year_answer(answer) or (is_pure_numeric(answer) and YEAR_Q.search(question)):
        return "year"
    if is_pure_numeric(answer):
        return "numeric"
    if MONTH_Q.search(question) and is_bare_month(answer):
        return "month"
    if PERSON_Q.search(question):
        return "person"
    if PLACE_Q.search(question):
        return "place"
    if has_malayalam_text(answer) or re.match(r"^[A-Za-z]", answer):
        return "text"
    return "text"


def option_kind(opt: str) -> str:
    if is_pure_year(opt):
        return "year"
    if is_pure_numeric(opt):
        return "numeric"
    return "text"


def has_bogus_year_distractors(options: list[str], answer: str) -> bool:
    """True when non-year answer has century/INC filler years as distractors."""
    if is_year_answer(answer) or is_pure_numeric(answer):
        return False
    year_opts = [o for o in options if o != answer and is_pure_year(o)]
    if not year_opts:
        return False
    if all(o in BOGUS_YEAR_DISTRACTORS for o in year_opts):
        return True
    if len(year_opts) >= 3:
        return True
    return False


def is_measurement_kind(kind: str) -> bool:
    return kind in {
        "period", "year", "speed", "au", "lagrange", "count",
        "distance_ly", "distance_ly_int", "distance_ly_large",
        "diameter", "diameter_num", "mass_num",
    }


def is_descriptive_astronomy_question(question: str) -> bool:
    if re.search(
        r"എത്ര|വർഷം ഏത്|ഇടവേള\?|കാലം\?|ദൂരം.*എത്ര|വ്യാസ.*എത്ര|വേഗത|ഭ്രമണകാലം|പരിക്രമണകാലം",
        question,
    ):
        return False
    return bool(re.search(
        r"ലക്ഷ്യം|ദൗത്യ തരം|പേര്\?|മൊഡ്യുൾ|ഇറങ്ങിയ.*ഭാഗം|ഇറങ്ങിയ.*പ്രദേശം|"
        r"സവിശേഷത|ആരാണ്|ഗുരുത്വാകർഷണം",
        question,
    ))


def astronomy_answer_kind(text: str, question: str = "") -> str:
    """Classify astronomy option/answer for type-coherence checks."""
    t = text.strip()
    q = question
    if t == "ഒന്നുമില്ല":
        return "none"
    if "പ്രകാശവർഷം" in t:
        return "distance_ly_large"
    if ASTRO_AU_RE.search(t):
        return "au"
    if ASTRO_SPEED_RE.search(t):
        return "speed"
    if ASTRO_PERIOD_RE.search(t):
        return "period"
    if re.match(r"^L\d", t):
        return "lagrange"
    if ASTRO_DIRECTION_RE.search(t):
        return "direction"
    if "കി.മീ." in t and re.search(r"\d", t):
        return "diameter"
    if re.match(r"^0\.\d+$", t):
        return "mass_ratio"
    if PURE_YEAR.match(t) and "വർഷം" in q:
        return "year"
    if re.match(r"^\d+$", t):
        n = int(t)
        if "സംഖ്യാ പേര്" in q or ("നമ്പർ" in q and "ക്ഷുദ്രഗ്രഹം" in q):
            return "asteroid_num"
        if "പിണ്ഡം" in q and n >= 10000:
            return "mass_num"
        if ("എത്ര" in q or "എണ്ണം" in q) and "ദൂരം" not in q and "പ്രകാശവർഷം" not in q:
            return "count"
        if "വ്യാസാർധം" in q or ("വ്യാസം" in q and "കി.മീ" in q):
            return "diameter_num"
        if "പ്രകാശവർഷം" in q or ("ദൂരം" in q and "നക്ഷത്രം" in q):
            return "distance_ly_int"
        if n >= 1000:
            return "diameter_num"
        if n >= 100 and "ക്ഷുദ്രഗ്രഹം" in q:
            return "asteroid_num"
        if n <= 300:
            return "distance_ly_int"
        return "asteroid_num"
    if re.match(r"^[\d.]+$", t):
        return "distance_ly"
    if "ദൗത്യ ലക്ഷ്യം" in q:
        if (
            t in ASTRO_MISSION_GOAL_POOL
            or t in ASTRO_PLANET_POOL
            or t == "സൂര്യൻ"
            or "യാത്ര" in t
        ):
            return "mission_goal"
    if re.search(r"ലാൻഡർ പേര്|റോവർ പേര്", q):
        if t in ASTRO_LANDER_POOL:
            return "lander_name"
    if "മൊഡ്യുൾ" in q and t in ASTRO_MODULE_POOL:
        return "module_name"
    if re.search(r"ഇറങ്ങിയ ചന്ദ്ര ഭാഗം|ഇറങ്ങിയ ചൊവ്വാ പ്രദേശം", q):
        if t in ASTRO_LANDING_SITE_POOL or t in ASTRO_REGION_POOL:
            return "landing_site"
    if t in ASTRO_MISSION_NAME_POOL or re.match(r"^(IRS|INSAT|GSAT|IRNSS|XPoSat|EMISAT|ചന്ദ്രയാൻ|മംഗള്യാൻ|ആദിത്യ)", t):
        return "mission_name"
    if (
        t in ASTRO_MISSION_TYPE_POOL
        or "ഉപഗ്രഹം" in t
        or "പഠനം" in t
        or "ദൂരദർശിനി" in t
        or "ഇമേജിംഗ്" in t
        or "ഇന്റലിജൻസ്" in t
        or "പോളാരിമെട്രി" in t
    ):
        return "mission_type"
    if t in ASTRO_PLANET_POOL or t.endswith(" ഗ്രഹം"):
        return "planet"
    if t in ASTRO_CONCEPT_POOL or "സൺസ്പോട്ട്" in t:
        return "concept"
    if t in ASTRO_REGION_POOL or re.search(r"ക്രേറ്റർ|പ്ലാനം|ബേസിൻ|ധ്രുവം|മേഖല|L4/L5|ബെൽറ്റ്", t):
        return "place"
    if re.match(r"^[A-Za-z0-9]", t) and len(t) < 24:
        return "mission_name"
    return "text"


def astronomy_kinds_compatible(ans_kind: str, opt_kind: str) -> bool:
    if ans_kind == opt_kind:
        return True
    if ans_kind in {"diameter", "diameter_num"} and opt_kind in {"diameter", "diameter_num"}:
        return True
    if ans_kind in {"distance_ly", "distance_ly_int"} and opt_kind in {"distance_ly", "distance_ly_int"}:
        return True
    if ans_kind == "direction" and opt_kind in {"direction", "none"}:
        return True
    if ans_kind == "count" and opt_kind == "count":
        return True
    if ans_kind in {"mass_ratio", "mass_num"} and opt_kind in {"mass_ratio", "mass_num"}:
        return True
    if ans_kind == "asteroid_num" and opt_kind in {"asteroid_num"}:
        return True
    if ans_kind in {"mission_goal", "planet"} and opt_kind in {"mission_goal", "planet"}:
        return True
    if ans_kind in {"mission_type", "concept"} and opt_kind in {"mission_type", "concept"}:
        return True
    if ans_kind in {"lander_name", "module_name", "mission_name"} and opt_kind == ans_kind:
        return True
    if ans_kind == "landing_site" and opt_kind in {"landing_site", "place"}:
        return True
    return False


def astronomy_option_mismatch(question: str, options: list[str], answer: str) -> str | None:
    """Return code when astronomy options mix periods, years, directions, AU, etc."""
    if len(options) != 4 or answer not in options:
        return None
    # Heuristic: astronomy file stems rarely use history person patterns
    if not re.search(
        r"ഗ്രഹ|ചന്ദ്ര|സൂര്യ|നക്ഷത്ര|ധൂമകേതു|ക്ഷുദ്രഗ്രഹ|ബഹിരാകാശ|ഉപഗ്രഹ|ദൂരം|വ്യാസ|"
        r"ഭ്രമണ|പരിക്രമണ|ഇസ്റോ|ദൗത്യ|ഓർട്ട്|കൈപ്പർ|സൗര|അന്താരാഷ്ട്ര ബഹിരാകാശ",
        question,
    ):
        return None

    ans_kind = astronomy_answer_kind(answer, question)

    if is_descriptive_astronomy_question(question):
        meas_wrong = [
            o for o in options
            if o != answer and is_measurement_kind(astronomy_answer_kind(o, question))
        ]
        if meas_wrong:
            return "astro_descriptive_q_measurement_distractors"

    if ans_kind == "text":
        return None

    wrong_mixed = [
        o for o in options
        if o != answer and not astronomy_kinds_compatible(
            ans_kind, astronomy_answer_kind(o, question)
        )
    ]
    if not wrong_mixed:
        return None

    # Bare calendar years on period/AU/speed/direction answers
    if ans_kind in {"period", "au", "speed", "direction", "lagrange", "diameter", "diameter_num"}:
        if any(is_pure_year(o) for o in wrong_mixed):
            return "astro_mixed_year_on_measurement"
        if len(wrong_mixed) >= 2:
            return "astro_mixed_option_kinds"

    if len(wrong_mixed) >= 2:
        return "astro_mixed_option_kinds"
    return None


def suggest_astronomy_distractors(
    answer: str,
    rng: random.Random | None = None,
    question: str = "",
) -> list[str]:
    rng = rng or random.Random(42)
    if "ദൗത്യ ലക്ഷ്യം" in question:
        return _pick_pool(ASTRO_MISSION_GOAL_POOL, answer, rng)
    if "ദൗത്യ തരം" in question:
        return _pick_pool(ASTRO_MISSION_TYPE_POOL, answer, rng)
    if re.search(r"ലാൻഡർ പേര്|റോവർ പേര്", question):
        return _pick_pool(ASTRO_LANDER_POOL, answer, rng)
    if "മൊഡ്യുൾ" in question:
        return _pick_pool(ASTRO_MODULE_POOL, answer, rng)
    if re.search(r"ഇറങ്ങിയ ചന്ദ്ര ഭാഗം|ഇറങ്ങിയ ചൊവ്വാ പ്രദേശം", question):
        return _pick_pool(ASTRO_LANDING_SITE_POOL, answer, rng)
    if "ഗുരുത്വാകർഷണം" in question:
        return _pick_pool(ASTRO_CONCEPT_POOL, answer, rng)

    kind = astronomy_answer_kind(answer, question)
    pool = ASTRO_KIND_POOLS.get(kind, [])
    if kind == "distance_ly" and "." in answer:
        pool = [x for x in ASTRO_DISTANCE_LY_POOL if "." in x]
    if kind == "mass_ratio":
        try:
            pool = [
                x for x in ASTRO_MASS_RATIO_POOL
                if (float(answer) < 2 and float(x) < 2) or (float(answer) >= 2 and float(x) >= 2)
            ]
        except ValueError:
            pool = ASTRO_MASS_RATIO_POOL
    if not pool:
        return _pick_pool(ASTRO_PERIOD_POOL + ASTRO_PLANET_POOL, answer, rng)
    return _pick_pool(pool, answer, rng)


def option_type_mismatch(question: str, options: list[str], answer: str) -> str | None:
    """Return mismatch code or None if options match question/answer type."""
    if len(options) != 4 or answer not in options:
        return None

    ans_kind = classify_answer_kind(question, answer)
    year_opts = [o for o in options if is_pure_year(o)]
    text_opts = [o for o in options if not is_pure_numeric(o)]

    if ans_kind == "month":
        non_month = [o for o in options if not is_bare_month(o)]
        if non_month:
            return "month_q_non_month_distractors"
        if any(is_award_description(o) for o in options):
            return "month_q_award_description_distractors"

    if ans_kind != "month" and not MONTH_Q.search(question):
        bare_month_wrong = [o for o in options if o != answer and is_bare_month(o)]
        if bare_month_wrong and AWARD_NAME_Q.search(question):
            return "month_distractor_on_award_q"

    astro_code = astronomy_option_mismatch(question, options, answer)
    if astro_code:
        return astro_code

    if DEFINITION_Q.search(question) and is_award_description(answer):
        sym_wrong = [o for o in options if o != answer and o in NON_PERSON_GARBAGE]
        if sym_wrong:
            return "definition_q_symbol_distractors"

    if is_woman_question(question):
        male_wrong = [o for o in options if o != answer and is_male_person_option(o)]
        if male_wrong:
            return "woman_q_male_distractors"

    if ans_kind == "person" or PERSON_Q.search(question):
        sym_wrong = [o for o in options if o != answer and o in NON_PERSON_GARBAGE]
        if sym_wrong:
            return "person_q_symbol_distractors"
        if re.search(r"ഇന്ത്യ|ഭാരത|യു\.എൻ", question):
            inv_wrong = [o for o in options if o != answer and o in INVENTOR_SET]
            if len(inv_wrong) >= 2:
                return "indian_person_q_inventor_distractors"

    if ans_kind == "place" and re.search(r"രാജ്യ", question):
        award_wrong = [o for o in options if o != answer and is_award_option(o)]
        if len(award_wrong) >= 2:
            return "country_q_award_distractors"

    if ans_kind in {"person", "place", "text"}:
        if has_bogus_year_distractors(options, answer):
            return "bogus_year_distractors"
        if len(year_opts) >= 3:
            return "year_options_for_name_answer"
        if year_opts and ans_kind == "person" and PERSON_Q.search(question):
            if len(year_opts) >= 2:
                return "person_q_year_distractors"

    if ans_kind == "year" and text_opts and not year_opts:
        # year question but all options are names — rare, flag it
        if len(text_opts) >= 3 and not any(is_pure_numeric(o) for o in options):
            return "name_options_for_year_answer"

    return None


def _pick_pool(pool: list[str], correct: str, rng: random.Random, n: int = 3) -> list[str]:
    wrong = [x for x in pool if x != correct]
    rng.shuffle(wrong)
    return wrong[:n]


def suggest_distractors(
    question: str,
    answer: str,
    rng: random.Random | None = None,
) -> list[str]:
    """Return three plausible wrong options matching answer type."""
    rng = rng or random.Random(42)
    kind = classify_answer_kind(question, answer)

    if kind == "month":
        return _pick_pool(list(MALAYALAM_MONTHS), answer, rng)

    if DEFINITION_Q.search(question) and is_award_description(answer):
        return _pick_pool(AWARD_DEFINITION_POOL, answer, rng)

    if kind == "year":
        pool = WH_PERSONS  # fallback; caller should pass year pool when known
        if "INC" in question or "സമ്മേളന" in question:
            pool = INC_YEARS
        elif re.search(r"\b(17|18|19|20)\d{2}\b", question):
            m = re.search(r"(1[789]\d{2}|20\d{2})", question)
            if m:
                base = int(m.group(1))
                pool = [str(y) for y in range(base - 15, base + 16) if str(y) != answer]
        else:
            pool = [
                "1776", "1789", "1815", "1914", "1917", "1918", "1939", "1945",
                "1969", "1989", "1991", "1492", "1066", "1215", "1453", "1865",
            ]
        return _pick_pool(pool, answer, rng)

    if kind == "person":
        if re.search(r"കണ്ടുപിടിച്ച|കണ്ടെത്തിയ|വികസനത്തിനായുള്ള", question):
            return _pick_pool(INVENTOR_POOL, answer, rng)
        if re.search(r"എവറസ്റ്റ്|കീഴടക്കിയ", question):
            return _pick_pool(MOUNTAINEER_POOL, answer, rng)
        if is_woman_question(question):
            return _pick_pool(INDIAN_WOMEN_POOL, answer, rng)
        if re.search(r"ഇന്ത്യ|ഭാരത|യു\.എൻ", question):
            return _pick_pool(INDIAN_NOTABLE_PERSONS, answer, rng)
        if re.search(r"ബഹിരാകാശ|ഇസ്റോ|ഗ്രഹചലന|ചന്ദ്ര|കെപ്ലർ|സാരാഭായി|കലാം", question):
            return _pick_pool(ASTRO_PERSON_POOL, answer, rng)
        if "INC" in question or "കോൺഗ്രസ്" in question and "അധ്യക്ഷ" in question:
            return _pick_pool(INC_PRESIDENTS, answer, rng)
        return _pick_pool(WH_PERSONS, answer, rng)

    if kind == "place":
        if "INC" in question or "സമ്മേളന" in question:
            if "അധ്യക്ഷ" not in question:
                return _pick_pool(INC_VENUES, answer, rng)
        if "രാജ്യ" in question or "ഭരിച്ച" in question or "ദൗത്യം" in question:
            return _pick_pool(WH_COUNTRIES, answer, rng)
        return _pick_pool(WH_CITIES + WH_COUNTRIES, answer, rng)

    if re.search(
        r"ഗ്രഹ|ചന്ദ്ര|സൂര്യ|നക്ഷത്ര|ധൂമകേതു|ക്ഷുദ്രഗ്രഹ|ബഹിരാകാശ|ഉപഗ്രഹ|ദൂരം|വ്യാസ|"
        r"ഭ്രമണ|പരിക്രമണ|ഇസ്റോ|ദൗത്യ|ഓർട്ട്|കൈപ്പർ|സൗര|അന്താരാഷ്ട്ര ബഹിരാകാശ",
        question,
    ):
        ak = astronomy_answer_kind(answer, question)
        if ak in ASTRO_KIND_POOLS or is_descriptive_astronomy_question(question):
            return suggest_astronomy_distractors(answer, rng, question)

    # text / concept
    return _pick_pool(WH_COUNTRIES + WH_PERSONS, answer, rng)


def build_options(
    question: str,
    answer: str,
    wrong: list[str] | None,
    rng: random.Random | None = None,
) -> list[str]:
    """Build four distinct options; replace mismatched wrong list when needed."""
    rng = rng or random.Random(42)
    if wrong and not option_type_mismatch(question, wrong + [answer], answer):
        opts = [answer] + [w for w in wrong if w != answer][:3]
    else:
        opts = [answer] + suggest_distractors(question, answer, rng)

    seen: set[str] = set()
    out: list[str] = []
    for o in opts:
        if o not in seen:
            seen.add(o)
            out.append(o)
    while len(out) < 4:
        extra = suggest_distractors(question, answer, rng)
        for e in extra:
            if e not in seen:
                seen.add(e)
                out.append(e)
            if len(out) >= 4:
                break
        if len(out) < 4:
            out.append("ഒന്നുമില്ല")
            break
    return out[:4]
