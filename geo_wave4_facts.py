#!/usr/bin/env python3
"""Wave 4 geography facts — PSC topics not heavily covered in geography.json."""

from __future__ import annotations

import random
import re
from collections import defaultdict

from geography_facts import (
    INDIAN_DAMS,
    INDIAN_NATIONAL_PARKS,
    INDIAN_STATE_CAPITALS,
    INDIA_PORTS,
    KERALA_DISTRICTS,
    STATE_NEIGHBORS,
    TROPIC_CANCER_STATES,
)
from refill_common import Candidate, add_candidate

MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")

STATES = [s for s, _ in INDIAN_STATE_CAPITALS]
KL = "കേരള"
_STATE_NORM = {"കേരളം": KL}

KUTRALAM = 'കുത്റലം'
PACHMARHI = 'പച്ചമര്ഹി'
RAWATBHATA = 'രാവത്ത്ഭാട'
KALPAKKAM = 'കാല്പാഅ്കം'
NARORA = 'നാരോര'
KAKRAPAR = 'കാഅ്രാඪാൻ'
KAIGA = 'കൈഗ'
KUDANKULAM = 'കൂടന്കുലം'
JAISALMER = 'ജെയസല്മേൻ'
TARAPUR = 'താരാപ്പൂൻ'
PALARUVI = 'പാലരുവി'
HOGENAKKAL = 'ഹോഗേനക്കല്'
NOHKALIKAI = 'നോഹ്കലികാഇ'
MEGHALAYA = 'മേഘാലയ'
PALAKKAD = 'പാലക്കാട'
MALAPPURAM = 'മലപ്ചുറം'
KODUNGALLUR = 'കൊട്ടംഗല്ലൂര്'
STAMBHAM = 'സ്തംഭം'
CHEMBRA = 'ചെംബ്രകാളം'
MAWSYNRAM = 'മൌസിംറം'
CHERRAPUNJI = 'ചെരാപുഞ്ജി'
LEH = 'ലേഹ്'
GUWAHATI = 'ഗുവാഹാടി'
HUBLI = 'ഹുബ്ലി'
SIMHADRI = 'സിംഹാദ്രി'
KORBA = 'കോര്ബ'
KAIM = 'കൈം'
SOOCHIPARA = 'സൂച്ചിപാറ'

CROPS: list[tuple[str, str]] = [
    ('നെല്ല്', 'പശ്ചിമബംഗാൾ'),
    ('ഗോതമ്പ്', 'ഉത്തർപ്രദേശ്'),
    ('ചായ', 'അസം'),
    ('റബ്ബർ', 'കേരള'),
    ('കാപ്പി', 'കർണാടക'),
    ('പഞ്ചാട', 'ഗുജറാത്ത്'),
    ('കരിമ്പ്', 'ഉത്തർപ്രദേശ്'),
    ('പുകയില', 'ആന്ധ്രപ്രദേശ്'),
    ('ചവറ്റ്', 'പശ്ചിമബംഗാൾ'),
    ('നിലക്കടല', 'ഗുജറാത്ത്'),
    ('തെങ്ങ്', 'കേരള'),
    ('മാങ്ങ', 'ഉത്തർപ്രദേശ്'),
    ('വാഴ', 'തമിഴ്നാട്'),
    ('കുരുമുളക്', 'കേരള'),
    ('ഏലം', 'കേരള'),
    ('ഇഞ്ചി', 'കേരള'),
    ('മഞ്ഞൾ', 'തെലങ്കാന'),
    ('ജ്വാര', 'മഹാരാഷ്ട്ര'),
    ('ചാമ', 'രാജസ്ഥാൻ'),
    ('രാഗി', 'കർണാടക'),
    ('സൂര്യകാന്തി', 'കർണാടക'),
    ('കടുക', 'രാജസ്ഥാൻ'),
    ('സോയാബീൻ', 'മധ്യപ്രദേശ്'),
    ('തുവര', 'മഹാരാഷ്ട്ര'),
    ('ഉഴുന്ന്', 'മധ്യപ്രദേശ്'),
    ('പയർ', 'രാജസ്ഥാൻ'),
    ('ഉരുളക്കിഴങ്ങ്', 'ഉത്തർപ്രദേശ്'),
    ('ഉള്ളി', 'മഹാരാഷ്ട്ര'),
    ('തക്കാളി', 'ആന്ധ്രപ്രദേശ്'),
    ('കയർ', 'കേരള'),
    ('പാക്ക്', 'കർണാടക'),
    ('കുങ്കുമപ്പൂ', 'ജമ്മു കശ്മീർ'),
    ('ആപ്പിൾ', 'ജമ്മു കശ്മീർ'),
    ('അക്രോട്ട്', 'ജമ്മു കശ്മീർ'),
    ('മുന്തിരി', 'മഹാരാഷ്ട്ര'),
    ('മാതള', 'മഹാരാഷ്ട്ര'),
    ('കശുവണ്ടി', 'മഹാരാഷ്ട്ര'),
    ('മല്ലി', 'രാജസ്ഥാൻ'),
    ('ജീരകം', 'രാജസ്ഥാൻ'),
    ('കാപ്പ്', 'കേരള'),
    ('വെള്ളരിക്ക', 'കേരള'),
    ('കാച്ചിൽ', 'ത്രിപുര'),
    ('പൈനാപ്പിൾ', 'കേരള'),
    ('അരി', 'പശ്ചിമബംഗാൾ'),
    ('പയർവർഗ്ഗം', 'മധ്യപ്രദേശ്'),
    ('അട', 'അസം'),
    ('കാച്ചാ', 'അസം'),
    ('ഇള', 'അസം'),
    ('ഓറഞ്ച്', 'മഹാരാഷ്ട്ര'),
    ('ലെമൺ', 'ആന്ധ്രപ്രദേശ്'),
    ('ബീറ്റ്റൂട്ട്', 'ഹരിയാന'),
    ('കാരറ്റ്', 'പഞ്ചാബ്'),
    ('മാതളം', 'മഹാരാഷ്ട്ര'),
    ('വാഴപ്പഴം', 'തമിഴ്നാട്'),
    ('പപ്പായ', 'കേരള'),
    ('വെള്ളം', 'പശ്ചിമബംഗാൾ'),
    ('അരക്ക', 'കേരള'),
    ('കശുമാവ്', 'കേരള'),
    ('തേന', 'കേരള'),
    ('അലഫ്', 'കേരള'),
    ('കാച്ചവ്', 'കേരള'),
]

CITY_RIVER: list[tuple[str, str]] = [
    ('കാശി', 'ഗംഗ'),
    ('കാൻപൂർ', 'ഗംഗ'),
    ('പാട്ന', 'ഗംഗ'),
    ('ഹരിദ്വാർ', 'ഗംഗ'),
    ('പ്രയാഗ്രാജ്', 'ഗംഗ'),
    ('കൊൽക്കത്ത', 'ഹൂഗ്ലി'),
    ('ലഖ്\u200cനൗ', 'ഗോമതി'),
    ('ആഗ്ര', 'യമുന'),
    ('ദില്ലി', 'യമുന'),
    ('പൂണ', 'മുഥ'),
    ('നാഗ്പൂർ', 'വാർധ'),
    ('അഹമദാബാദ്', 'സബർമതി'),
    ('ജബൽപൂർ', 'നർമ്മദ'),
    ('നാഷിക്', 'ഗോദാവരി'),
    ('റാജമുണ്ട്രി', 'ഗോദാവരി'),
    ('വിജയവാഡ', 'കൃഷ്ണ'),
    ('ധാർവാഡ', 'മാഹ'),
    ('മദുരൈ', 'വൈഗ'),
    ('തിരുച്ചി', 'കാവേരി'),
    ('കൊച്ചി', 'പെരിയാർ'),
    ('ഹൈദരാബാദ്', 'മൂസി'),
    ('ചെന്നൈ', 'കൂവം'),
    ('കടലുണ്ടി', 'പാലാർ'),
    ('ഭുവനേശ്വർ', 'മഹാനദി'),
    ('റായ്പൂർ', 'മഹാനദി'),
    ('കോട്ട', 'ചംബൽ'),
    ('ഉജ്ജയിൻ', 'ശിപ്ര'),
    ('അമൃതസർ', 'ബിയാസ്'),
    ('സൂറത്ത്', 'താപ്തി'),
    ('ഭോപാൽ', 'ബേത്വ'),
]

HILL_STATIONS: list[tuple[str, str]] = [
    ('ഷിംല', 'ഹിമാചൽ പ്രദേശ്'),
    ('മണാലി', 'ഹിമാചൽ പ്രദേശ്'),
    ('ഊട്ടി', 'തമിഴ്നാട്'),
    ('കോടയിക്കനാൽ', 'തമിഴ്നാട്'),
    ('മസൂറി', 'ഉത്തരാഖണ്ഡ്'),
    ('ദാർജിലിംഗ്', 'പശ്ചിമബംഗാൾ'),
    ('പാച്ചമരി', 'മധ്യപ്രദേശ്'),
    ('ഗംഗ്ടോക്ക്', 'സിക്കിം'),
    ('യർക്കാട്', 'തമിഴ്നാട്'),
    ('ലാൻഡൺടോപ്പ്', 'ഉത്തരാഖണ്ഡ്'),
    ('പൊന്മുഡി', 'കേരള'),
    ('വാഗമൺ', 'കേരള'),
    ('മൂന്നാർ', 'കേരള'),
    ('അബു', 'രാജസ്ഥാൻ'),
]

STRAITS: list[tuple[str, str]] = [
    ('മലക്കാ കടലിടുക്ക്', 'മലേഷ്യയും സുമാത്ര'),
    ('ഹോർമുസ് കടലിടുക്ക്', 'ഓമാനും ഇറാനും'),
    ('ഡാർഡനെല്ലസ്', 'ഈജിയൻ കടലും മാർമാര'),
    ('പാൽക്ക് കടലിടുക്ക്', 'ഇന്ത്യയും ശ്രീലങ്കയും'),
    ('ടെൻ ഡിഗ്രി ചാനൽ', 'അണ്ടമാനും നികോബാരും'),
    ('സുണ്ട കടലിടുക്ക്', 'ജാവയും സുമാത്ര'),
    ('ഡോവർ കടലിടുക്ക്', 'ഇംഗ്ലണ്ടും ഫ്രാൻസും'),
    ('ബെറിംഗ് കടലിടുക്ക്', 'അലാസ്കയും റഷ്യയും'),
    ('ബാബ് അൽ മന്ദബ്', 'യെമനും ജിബൂട്ടിയും'),
    ('ബോസ്ഫോറസ്', 'ടർക്കിയും യൂറോപ്പും'),
]

INDIAN_LAKES: list[tuple[str, str]] = [
    ('ദൽ', 'ജമ്മു കശ്മീർ'),
    ('വൂളാർ', 'ജമ്മു കശ്മീർ'),
    ('ചില്കാ', 'ഒഡിഷ'),
    ('സാംഭാർ', 'രാജസ്ഥാൻ'),
    ('ലോക്തക്', 'മണിപ്പൂർ'),
    ('വേമ്പനാട്', 'കേരള'),
    ('കോളേരു', 'ആന്ധ്രപ്രദേശ്'),
    ('പുലികാട്', 'തമിഴ്നാട്'),
    ('രണ്ണ', 'ഒഡിഷ'),
    ('ഭോജ്', 'മധ്യപ്രദേശ്'),
    ('ദീപോർ', 'അസം'),
]

HIMALAYAN_PASSES: list[tuple[str, str]] = [
    ('നഥുലാ', 'സിക്കിം'),
    ('റോഹ്താങ്', 'ഹിമാചൽ പ്രദേശ്'),
    ('സോജി ലാ', 'ജമ്മു കശ്മീർ'),
    ('ബാനിഹാൽ', 'ജമ്മു കശ്മീർ'),
    ('പിർ പഞ്ചാൽ', 'ജമ്മു കശ്മീർ'),
    ('ഖാർദുംഗ് ലാ', 'ലദാക്ക്'),
    ('ചാങ് ലാ', 'ലദാക്ക്'),
    ('ഷിപ്കി ലാ', 'ഹിമാചൽ പ്രദേശ്'),
    ('ലിപുളേഖ്', 'ഉത്തരാഖണ്ഡ്'),
    ('മാനാ', 'ഉത്തരാഖണ്ഡ്'),
    ('ജെലിപ്പ് ലാ', 'സിക്കിം'),
    ('ബോംദില', 'അരുണാചൽ പ്രദേശ്'),
]

MINERAL_REGIONS: list[tuple[str, str]] = [
    ('ഝാരിയ', 'ഝാർഖണ്ഡ്'),
    ('ബോകാറോ', 'ഝാർഖണ്ഡ്'),
    ('ധനാബാദ്', 'ഝാർഖണ്ഡ്'),
    ('റാനിഗഞ്ജ്', 'പശ്ചിമബംഗാൾ'),
    ('സിംഗ്രൗലി', 'മധ്യപ്രദേശ്'),
    ('കോരാപ്പറ്റ്', 'ഒഡിഷ'),
    ('ബൈലാഡില', 'ഛത്തീസ്ഗഢ്'),
    ('ദുർഗ', 'ഛത്തീസ്ഗഢ്'),
    ('ഖേത്രി', 'രാജസ്ഥാൻ'),
    ('സിംഗ്ഭൂം', 'ഝാർഖണ്ഡ്'),
    ('കോളാർ', 'കർണാടക'),
    ('പന്നാ', 'മധ്യപ്രദേശ്'),
    ('ദിഗ്ബോയ്', 'അസം'),
    ('അസാം തീരം', 'അസം'),
    ('മുംബൈ ഉയർ', 'മഹാരാഷ്ട്ര'),
    ('കൃഷ്ണ ഗോദാവരി തീരം', 'ആന്ധ്രപ്രദേശ്'),
    ('ജാംഷേഡ്പൂർ', 'ഝാർഖണ്ഡ്'),
    ('ഭിലായി', 'ഛത്തീസ്ഗഢ്'),
    ('രൗർക്കേല', 'ഒഡിഷ'),
    ('ദുർഗാപൂർ', 'പശ്ചിമബംഗാൾ'),
    ('നാഗ്പൂർ', 'മഹാരാഷ്ട്ര'),
    ('രാഞ്ചി', 'ഝാർഖണ്ഡ്'),
    ('ബില്ലിത്ത', 'ഒഡിഷ'),
    ('മാലാഞ്ച', 'ഒഡിഷ'),
    ('കേന്ദ്രീയ', 'ഒഡിഷ'),
]

WATERFALLS: list[tuple[str, str]] = [
    ('ജോഗ്', 'കർണാടക'),
    ('ശിവസമുദ്രം', 'കർണാടക'),
    ('അതിർപ്പള്ളി', 'കേരള'),
    ('മീൻമുത്തട്ടി', 'കേരള'),
    ('വാഴച്ചൽ', 'കേരള'),
    ('തേക്കട', 'കേരള'),
    ('അരുവി', 'കേരള'),
    ('പാലരുവി', 'കേരള'),
    ('തോമൻകുത്ത്', 'കേരള'),
    ('ഹോഗേനക്കല്', 'തമിഴ്നാട്'),
    ('ദുധ്സാഗർ', 'ഗോവ'),
    ('നോഹ്കലികാഇ', 'മേഘാലയ'),
    ('കുത്റലം', 'തമിഴ്നാട്'),
    ('സൂച്ചിപാറ', 'കേരള'),
]

UNESCO_SITES: list[tuple[str, str]] = [
    ('താജ് മഹൽ', 'ഉത്തരപ്രദേശ്'),
    ('ഹുമായൂന്റെ കബ്ര', 'ദില്ലി'),
    ('ഹംപി', 'കർണാടക'),
    ('സുന്ദർബൻസ്', 'പശ്ചിമബംഗാൾ'),
    ('കജുരാഹോ', 'മധ്യപ്രദേശ്'),
    ('പട്മാവതി', 'രാജസ്ഥാൻ'),
    ('മനാസ്', 'അസം'),
    ('കാജീരാംഗ', 'അസം'),
    ('ആഗ്ര കോട്ട', 'ഉത്തരപ്രദേശ്'),
    ('ഫത്തേപുർ സിക്രി', 'ഉത്തരപ്രദേശ്'),
    ('എല്ലോറ', 'മഹാരാഷ്ട്ര'),
    ('ഗോൾഗുംബ', 'കർണാടക'),
    ('മഹാബോധി', 'ബിഹാർ'),
    ('കോൺവെന്റ്', 'ഗോവ'),
    ('ചമ്പനെറി', 'കർണാടക'),
    ('രാഷ്ട്രപതി ഭവൻ', 'ദില്ലി'),
    ('ജന്തർ മന്തർ', 'ദില്ലി'),
]

BIOSPHERE_RESERVES: list[tuple[str, str]] = [
    ('നീൽഗിരി', 'തമിഴ്നാട്'),
    ('സുന്ദർബൻസ്', 'പശ്ചിമബംഗാൾ'),
    ('ഗൾഫ് ഓഫ് മന്നാർ', 'തമിഴ്നാട്'),
    ('നോക്കെക്', 'മേഘാലയ'),
    ('ദിബ്രു സൈഖോവ', 'അസം'),
    ('പച്ചമര്ഹി', 'മധ്യപ്രദേശ്'),
    ('സൈലൻറ്', 'സിക്കിം'),
    ('ദേഹാര', 'മധ്യപ്രദേശ്'),
    ('ഗ്രേറ്റർ നികോബാർ', 'അണ്ടമാൻ'),
    ('മണിപ്പൂർ', 'മണിപ്പൂർ'),
]

KL_LANDMARKS: list[tuple[str, str, str]] = [
    ('തിരുവനന്തപുരം', 'പടിപ്പുരം', 'തിരുവനന്തപുരം'),
    ('കൊല്ലം', 'ആശ്രാമം', 'കൊല്ലം'),
    ('പത്തനംതിട്ട', 'സബരിമല', 'പത്തനംതിട്ട'),
    ('ആലപ്പുഴ', 'കായലുകൾ', 'ആലപ്പുഴ'),
    ('കോട്ടയം', 'വെമ്പനാട്', 'കോട്ടയം'),
    ('ഇടുക്കി', 'മൂന്നാർ', 'ഇടുക്കി'),
    ('എറണാകുളം', 'ഫോർട്ട് കൊച്ചി', 'എറണാകുളം'),
    ('തൃശ്ശൂർ', 'പൂരം', 'തൃശ്ശൂർ'),
    ('പാലക്കാട', 'പാലക്കാട് കോട്ട', 'പാലക്കാട'),
    ('മലപ്ചുറം', 'കൊട്ടംഗല്ലൂര്', 'മലപ്ചുറം'),
    ('കോഴിക്കോട്', 'കപ്പാട്', 'കോഴിക്കോട്'),
    ('വയനാട്', 'ചെംബ്രകാളം', 'വയനാട്'),
    ('കണ്ണൂർ', 'സ്തംഭം', 'കണ്ണൂർ'),
    ('കാസർഗോഡ്', 'ബേക്കൽ കോട്ട', 'കാസർഗോഡ്'),
]

RAILWAY_ZONES: list[tuple[str, str]] = [
    ('ദക്ഷിണ റെയിൽവേ', 'ചെന്നൈ'),
    ('സെന്ട്രൽ റെയിൽവേ', 'മുംബൈ'),
    ('പശ്ചിമ റെയിൽവേ', 'മുംബൈ'),
    ('കിഴക്കൻ റെയിൽവേ', 'കൊൽക്കത്ത'),
    ('തെക്കുകിഴക്കൻ റെയിൽവേ', 'കൊൽക്കത്ത'),
    ('ഉത്തര റെയിൽവേ', 'ദില്ലി'),
    ('വടക്കുകിഴക്കൻ റെയിൽവേ', 'ഗോരഖ്പൂർ'),
    ('വടക്കുകിഴക്കൻ അതിർത്തി റെയിൽവേ', 'ഗുവാഹാടി'),
    ('വടക്കു മധ്യ റെയിൽവേ', 'പ്രയാഗ്രാജ്'),
    ('വടക്ക് പശ്ചിമ റെയിൽവേ', 'ജയ്പൂർ'),
    ('ദക്ഷിണ മധ്യ റെയിൽവേ', 'സെക്കന്ദരാബാദ്'),
    ('ദക്ഷിണ പശ്ചിമ റെയിൽവേ', 'ഹുബ്ലി'),
]

POWER_STATIONS: list[tuple[str, str]] = [
    ('താരാപ്പൂൻ', 'മഹാരാഷ്ട്ര'),
    ('രാവത്ത്ഭാട', 'രാജസ്ഥാൻ'),
    ('കാല്പാഅ്കം', 'തമിഴ്നാട്'),
    ('നാരോര', 'ഉത്തരപ്രദേശ്'),
    ('കാഅ്രാඪാൻ', 'ഗുജറാത്ത്'),
    ('കൈഗ', 'കർണാടക'),
    ('കൂടന്കുലം', 'തമിഴ്നാട്'),
    ('കൈം', 'മഹാരാഷ്ട്ര'),
    ('കോര്ബ', 'ഒഡിഷ'),
    ('സിംഹാദ്രി', 'ആന്ധ്രപ്രദേശ്'),
    ('ജെയസല്മേൻ', 'രാജസ്ഥാൻ'),
]

CLIMATE_PLACES: list[tuple[str, str]] = [
    ('മൌസിംറം', 'മേഘാലയ'),
    ('ചെരാപുഞ്ജി', 'മേഘാലയ'),
    ('ജെയസല്മേൻ', 'രാജസ്ഥാൻ'),
    ('ലേഹ്', 'ലദാക്ക്'),
    ('ബികാനർ', 'രാജസ്ഥാൻ'),
    ('ഉദയ്പൂർ', 'രാജസ്ഥാൻ'),
]

TRIBUTARIES: list[tuple[str, str]] = [
    ('യമുന', 'ഗംഗ'),
    ('ചംബൽ', 'യമുന'),
    ('ബേത്വ', 'യമുന'),
    ('സോണ', 'ഗംഗ'),
    ('ഘാഗ്ര', 'ഗംഗ'),
    ('കോസി', 'ഗംഗ'),
    ('ഭീമ', 'കൃഷ്ണ'),
    ('തുംഗഭദ്ര', 'കൃഷ്ണ'),
    ('ഭരതപ്പുഴ', 'കാവേരി'),
    ('പാമ്പ', 'കാവേരി'),
    ('കബാനി', 'കാവേരി'),
    ('വാർധ', 'ഗോദാവരി'),
    ('പെന്ന', 'ഗോദാവരി'),
    ('മ്യൂ', 'ചംബൽ'),
    ('ഹിമാധ്രി', 'ഗംഗ'),
]

WILDLIFE_SANCTUARIES: list[tuple[str, str]] = [
    ('പെരിയാർ', 'കേരള'),
    ('അരളം', 'കേരള'),
    ('ചിന്നാർ', 'കേരള'),
    ('വേയ്മ്പാട്', 'കേരള'),
    ('നന്ദൻകണ്ണ്', 'തമിഴ്നാട്'),
    ('മുഡുമലൈ', 'തമിഴ്നാട്'),
    ('വേയങ്കോട്', 'കർണാടക'),
    ('ഭദ്ര', 'കർണാടക'),
    ('കാസിരംഗ', 'അസം'),
    ('മാനസ്', 'അസം'),
    ('വാല്മികി', 'ബിഹാർ'),
    ('സരിസ്ക', 'ഹരിയാന'),
    ('കേവലാദേവി', 'രാജസ്ഥാൻ'),
    ('രണതംഭോർ', 'രാജസ്ഥാൻ'),
]

INDIAN_PLATEAUS: list[tuple[str, str]] = [
    ('ദക്കൻ പീഠഭൂമി', 'ദക്ഷിണ ഇന്ത്യ'),
    ('ചോട്ടാ നാഗ്പൂർ പീഠഭൂമി', 'ഇടത്തുകിഴക്കൻ ഇന്ത്യ'),
    ('മാലവ പീഠഭൂമി', 'മധ്യ ഇന്ത്യ'),
    ('താർ', 'രാജസ്ഥാൻ'),
    ('മേഘാലയ പീഠഭൂമി', 'മേഘാലയ'),
]

WORLD_DESERTS: list[tuple[str, str]] = [
    ('സഹാര', 'ആഫ്രിക്ക'),
    ('ഗോബി', 'ഏഷ്യ'),
    ('കലഹാരി', 'ആഫ്രിക്ക'),
]

INDIAN_BEACHES: list[tuple[str, str]] = [
    ('മറീന', 'തമിഴ്നാട്'),
    ('കോവളം', 'കേരള'),
]

STATE_LANGUAGES: list[tuple[str, str]] = [
    ('കേരള', 'മലയാളം'),
    ('തമിഴിനാട്', 'തമിഴ്'),
    ('ആനംധ്രപ്രദേശ്', 'തെലുഗു'),
    ('മഹാരാഷ്ട്ര', 'മരാഠീ'),
    ('ഗുജരാത്', 'ഗുജരാതീ'),
    ('ഉത്തരപ്രദേശ്', 'ഹിംദീ'),
    ('അസം', 'അസമീയ'),
]

GEO_WAVE4_DIRECT: list[tuple[str, str, list[str], str]] = []

def _norm_state(name: str) -> str:
    return _STATE_NORM.get(name, name)


def _pool(items: list[str], correct: str) -> list[str]:
    return [x for x in items if x != correct]


def _w4_add(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    q: str,
    ans: str,
    wrong: list[str],
    diff: str = "medium",
    pool: list[str] | None = None,
) -> None:
    if MIXED.search(q + ans + "".join(wrong)):
        return
    add_candidate(out, existing, rng, q, ans, wrong, diff, pool)


def _pair2(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    rows: list[tuple[str, str]],
    q_fwd: str,
    q_rev: str,
    pool_a: list[str],
    pool_b: list[str],
) -> None:
    for a, b in rows:
        _w4_add(out, existing, rng, q_fwd.format(a=a, b=b), b, _pool(pool_b, b)[:3], "medium", pool_b)
        _w4_add(out, existing, rng, q_rev.format(a=a, b=b), a, _pool(pool_a, a)[:3], "hard", pool_a)


def _validate_rows(rows: list[tuple[str, ...]], name: str) -> None:
    for row in rows:
        if MIXED.search("".join(row)):
            raise ValueError(f"{name}: mixed script in {row!r}")


def _validate_all_data() -> None:
    for name, rows in [
        ("CROPS", CROPS), ("CITY_RIVER", CITY_RIVER), ("HILL_STATIONS", HILL_STATIONS),
        ("STRAITS", STRAITS), ("INDIAN_LAKES", INDIAN_LAKES),
        ("HIMALAYAN_PASSES", HIMALAYAN_PASSES), ("MINERAL_REGIONS", MINERAL_REGIONS),
        ("WATERFALLS", WATERFALLS), ("UNESCO_SITES", UNESCO_SITES),
        ("BIOSPHERE_RESERVES", BIOSPHERE_RESERVES), ("RAILWAY_ZONES", RAILWAY_ZONES),
        ("POWER_STATIONS", POWER_STATIONS), ("CLIMATE_PLACES", CLIMATE_PLACES),
        ("TRIBUTARIES", TRIBUTARIES), ("WILDLIFE_SANCTUARIES", WILDLIFE_SANCTUARIES),
    ]:
        _validate_rows(rows, name)
    _validate_rows(KL_LANDMARKS, "KL_LANDMARKS")

def generate_wave4_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []
    crop_names = [c for c, _ in CROPS]
    crop_states = list({s for _, s in CROPS})
    _pair2(out, existing, rng, CROPS,
        "'{a}' ഏറ്റവും കൂടുതൽ ഉത്പാദിക്കുന്ന ഇന്ത്യൻ സംസ്ഥാനം ഏത്?",
        "'{b}' സംസ്ഥാനത്തിന്റെ പ്രധാന കാർഷിക ഉൽപ്പന്നം '{a}' — ശരിയോ?",
        crop_names, crop_states)
    _pair2(out, existing, rng, CROPS,
        "'{a}' പ്രധാനമായി ഏത് സംസ്ഥാനത്തിൽ കൃഷി ചെയ്യുന്നു?",
        "'{b}' സംസ്ഥാനത്ത് പ്രധാന കാർഷിക വിള '{a}' — ശരിയാണോ?",
        crop_names, crop_states)
    cities = [c for c, _ in CITY_RIVER]
    rivers = list({r for _, r in CITY_RIVER})
    _pair2(out, existing, rng, CITY_RIVER,
        "'{a}' നഗരം ഏത് നദിയുടെ തീരത്താണ്?",
        "'{b}' നദിയുടെ തീരത്തുള്ള പ്രധാന നഗരം '{a}' — ശരിയോ?",
        cities, rivers)
    _pair2(out, existing, rng, CITY_RIVER,
        "'{a}' നഗരം സ്ഥിതി ചെയ്യുന്ന നദി ഏത്?",
        "'{b}' നദിയുടെ തീരത്ത് '{a}' — ശരിയാണോ?",
        cities, rivers)
    hills = [h for h, _ in HILL_STATIONS]
    hill_states = list({s for _, s in HILL_STATIONS})
    _pair2(out, existing, rng, HILL_STATIONS,
        "'{a}' ഏത് സംസ്ഥാനത്തിലെ ഹിൽ സ്റ്റേഷൻ?",
        "'{b}' സംസ്ഥാനത്തിലെ പ്രശസ്തമായ ഹിൽ സ്റ്റേഷൻ '{a}' — ശരിയോ?",
        hills, hill_states)
    strait_names = [s for s, _ in STRAITS]
    strait_conn = [c for _, c in STRAITS]
    for name, conn in STRAITS:
        _w4_add(out, existing, rng, f"ഏത് കടലിടുക്ക് {conn} ബന്ധിപ്പിക്കുന്നു?", name,
                _pool(strait_names, name)[:3], "medium", strait_names)
        _w4_add(out, existing, rng, f"'{name}' കടലിടുക്ക് ബന്ധിപ്പിക്കുന്ന പ്രദേശങ്ങൾ?", conn,
                _pool(strait_conn, conn)[:3], "hard", strait_conn)
    lakes = [l for l, _ in INDIAN_LAKES]
    lake_states = list({s for _, s in INDIAN_LAKES})
    _pair2(out, existing, rng, INDIAN_LAKES,
        "'{a}' ഏത് സംസ്ഥാനത്തിലെ പ്രധാന തടാകം?",
        "'{b}' സംസ്ഥാനത്തിലെ പ്രശസ്തമായ തടാകം '{a}' — ശരിയോ?",
        lakes, lake_states)
    passes = [p for p, _ in HIMALAYAN_PASSES]
    pass_states = list({s for _, s in HIMALAYAN_PASSES})
    _pair2(out, existing, rng, HIMALAYAN_PASSES,
        "'{a}' ഏത് സംസ്ഥാനത്തിലുള്ള ഹിമാലയൻ കയറ്റം?",
        "'{b}' സംസ്ഥാനത്തിലെ പ്രധാന കയറ്റം '{a}' — ശരിയോ?",
        passes, pass_states)
    regions = [r for r, _ in MINERAL_REGIONS]
    mineral_states = list({s for _, s in MINERAL_REGIONS})
    _pair2(out, existing, rng, MINERAL_REGIONS,
        "'{a}' ഏത് സംസ്ഥാനത്തിലെ പ്രധാന ഖനി/വ്യവസായ പ്രദേശം?",
        "'{b}' സംസ്ഥാനത്തിലെ പ്രശസ്തമായ ഖനി/വ്യവസായ കേന്ദ്രം '{a}' — ശരിയോ?",
        regions, mineral_states)
    falls = [f for f, _ in WATERFALLS]
    fall_states = list({s for _, s in WATERFALLS})
    _pair2(out, existing, rng, WATERFALLS,
        "'{a}' ജലപാതം ഏത് സംസ്ഥാനത്താണ്?",
        "'{b}' സംസ്ഥാനത്തിലെ പ്രശസ്തമായ ജലപാതം '{a}' — ശരിയോ?",
        falls, fall_states)
    sites = [u for u, _ in UNESCO_SITES]
    unesco_states = list({s for _, s in UNESCO_SITES})
    _pair2(out, existing, rng, UNESCO_SITES,
        "'{a}' യുനെസ്കോ ലോക പൈതൃക കേന്ദ്രം ഏത് സംസ്ഥാനത്താണ്?",
        "'{b}' സംസ്ഥാനത്തിലെ യുനെസ്കോ ലോക പൈതൃക കേന്ദ്രം '{a}' — ശരിയോ?",
        sites, unesco_states)
    bio_names = [b for b, _ in BIOSPHERE_RESERVES]
    bio_states = list({s for _, s in BIOSPHERE_RESERVES})
    _pair2(out, existing, rng, BIOSPHERE_RESERVES,
        "'{a}' ജൈവവൈവിധ്യ സംരക്ഷിത പ്രദേശം ഏത് സംസ്ഥാനത്താണ്?",
        "'{b}' സംസ്ഥാനത്തിലെ ജൈവവൈവിധ്യ സംരക്ഷിത പ്രദേശം '{a}' — ശരിയോ?",
        bio_names, bio_states)
    dists = [d for d, _, _ in KL_LANDMARKS]
    landmarks = [lm for _, lm, _ in KL_LANDMARKS]
    for district, landmark, _ in KL_LANDMARKS:
        _w4_add(out, existing, rng,
                f"കേരളത്തിലെ '{landmark}' ഏത് ജില്ലയുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?",
                district, _pool(dists, district)[:3], "medium", dists)
        _w4_add(out, existing, rng,
                f"കേരളത്തിലെ '{district}' ജില്ലയിലെ പ്രശസ്തമായ '{landmark}' — ഏത്?",
                landmark, _pool(landmarks, landmark)[:3], "hard", landmarks)
    zones = [z for z, _ in RAILWAY_ZONES]
    hqs = list({h for _, h in RAILWAY_ZONES})
    _pair2(out, existing, rng, RAILWAY_ZONES,
        "'{a}' റെയിൽവേ സോണിന്റെ ആസ്ഥാനം ഏതാണ്?",
        "'{b}' ഏത് റെയിൽവേ സോണിന്റെ ആസ്ഥാനമാണ്?",
        zones, hqs)
    stations = [s for s, _ in POWER_STATIONS]
    power_states = list({st for _, st in POWER_STATIONS})
    _pair2(out, existing, rng, POWER_STATIONS,
        "'{a}' ഏത് സംസ്ഥാനത്തിലെ ആണവ/വൈദ്യുത കേന്ദ്രം?",
        "'{b}' സംസ്ഥാനത്തിലെ പ്രധാന ആണവ/വൈദ്യുത കേന്ദ്രം '{a}' — ശരിയോ?",
        stations, power_states)
    wet_places = [p for p, _ in CLIMATE_PLACES]
    climate_states = list({s for _, s in CLIMATE_PLACES})
    _pair2(out, existing, rng, CLIMATE_PLACES,
        "'{a}' ഏത് സംസ്ഥാനത്തിലെ പ്രശസ്ത കാലാവസ്ഥാ പ്രദേശം?",
        "'{b}' സംസ്ഥാനത്തിലെ പ്രശസ്ത കാലാവസ്ഥാ പ്രദേശം '{a}' — ശരിയോ?",
        wet_places, climate_states)
    tribs = [t for t, _ in TRIBUTARIES]
    mains = list({m for _, m in TRIBUTARIES})
    _pair2(out, existing, rng, TRIBUTARIES,
        "'{a}' ഏത് പ്രധാന നദിയുടെ പോഷക നദി?",
        "'{b}' നദിയുടെ പോഷക നദി '{a}' — ശരിയോ?",
        tribs, mains)
    sanct_names = [s for s, _ in WILDLIFE_SANCTUARIES]
    sanct_states = list({st for _, st in WILDLIFE_SANCTUARIES})
    _pair2(out, existing, rng, WILDLIFE_SANCTUARIES,
        "'{a}' വന്യജീവി സങ്കേതം ഏത് സംസ്ഥാനത്താണ്?",
        "'{b}' സംസ്ഥാനത്തിലെ പ്രശസ്ത വന്യജീവി സങ്കേതം '{a}' — ശരിയോ?",
        sanct_names, sanct_states)
    parks_states = list({_norm_state(s) for _, s in INDIAN_NATIONAL_PARKS})
    for park, state in INDIAN_NATIONAL_PARKS:
        st = _norm_state(state)
        _w4_add(out, existing, rng,
                f"'{park}' സ്ഥിതി ചെയ്യുന്ന ദേശീയോദ്യാനം/വന്യജീവി സംരക്ഷിത പ്രദേശം ഏത് സംസ്ഥാനത്താണ്?",
                st, _pool(parks_states, st)[:3], "medium", parks_states)
    port_states = list({_norm_state(s) for _, s in INDIA_PORTS})
    for port, state in INDIA_PORTS:
        st = _norm_state(state)
        _w4_add(out, existing, rng,
                f"'{port}' തുറമുഖം സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം ഏത്?",
                st, _pool(port_states, st)[:3], "medium", port_states)
    tropic = [_norm_state(s) for s in TROPIC_CANCER_STATES]
    for st in tropic:
        _w4_add(out, existing, rng,
                "കർക്കരേഖ (ട്രോപ്പിക് ഓഫ് കാൻസർ) കടന്നുപോകുന്ന ഇന്ത്യൻ സംസ്ഥാനം ഏത്?",
                st, _pool(tropic, st)[:3], "medium", tropic)
    hqs_kl = [h for _, h in KERALA_DISTRICTS]
    dist_names = [d for d, _ in KERALA_DISTRICTS]
    for district, hq in KERALA_DISTRICTS:
        _w4_add(out, existing, rng,
                f"കേരളത്തിലെ '{district}' ജില്ലയുടെ ആസ്ഥാന നഗരം?",
                hq, _pool(hqs_kl, hq)[:3], "easy", hqs_kl)
    for state, neighbors in STATE_NEIGHBORS.items():
        st = _norm_state(state)
        if st not in STATES:
            continue
        nbs = [_norm_state(n) for n in neighbors if _norm_state(n) in STATES]
        for nb_n in nbs:
            _w4_add(
                out, existing, rng,
                f"'{st}' സംസ്ഥാനത്തിന്റെ അതിർത്തി പങ്കിടുന്ന സംസ്ഥാനം ഏത്?",
                nb_n,
                [s for s in STATES if s != nb_n and s != st][:3],
                "medium",
                STATES,
            )
        non = [s for s in STATES if s != st and s not in nbs]
        if len(non) >= 3:
            _w4_add(
                out, existing, rng,
                f"'{st}' സംസ്ഥാനവുമായി അതിർത്തി പങ്കിടാത്ത സംസ്ഥാനം ഏത്?",
                non[0],
                non[1:4],
                "hard",
                non,
            )
    rivers_d = list({r for _, r, _ in INDIAN_DAMS})
    states_d = list({s for _, _, s in INDIAN_DAMS})
    for dam, river, state in INDIAN_DAMS:
        st = _norm_state(state)
        _w4_add(
            out, existing, rng,
            f"'{dam}' അണക്കെട്ട് ഏത് നദിയിലാണ്?",
            river,
            [r for r in rivers_d if r != river],
            "medium",
            rivers_d,
        )
        _w4_add(
            out, existing, rng,
            f"'{dam}' അണക്കെട്ട് ഏത് സംസ്ഥാനത്താണ്?",
            st,
            [s for s in states_d if s != st],
            "medium",
            states_d,
        )
    by_state_parks: dict[str, list[str]] = defaultdict(list)
    for park, state in INDIAN_NATIONAL_PARKS:
        by_state_parks[_norm_state(state)].append(park)
    for state, parks in by_state_parks.items():
        uniq = list(dict.fromkeys(parks))
        if len(uniq) < 2:
            continue
        for park in uniq:
            _w4_add(
                out, existing, rng,
                f"{state} സംസ്ഥാനത്തിലെ '{park}' ദേശീയോദ്യാനം ഏതാണ്?",
                park,
                [p for p in uniq if p != park],
                "medium",
                uniq,
            )
    for port, state in INDIA_PORTS:
        st = _norm_state(state)
        ports_in = [p for p, s in INDIA_PORTS if _norm_state(s) == st]
        if len(ports_in) >= 2:
            for p in ports_in:
                _w4_add(
                    out, existing, rng,
                    f"{st} സംസ്ഥാനത്തിലെ പ്രധാന തുറമുഖം ഏത്?",
                    p,
                    [x for x in ports_in if x != p],
                    "hard",
                    ports_in,
                )
    for district, hq in KERALA_DISTRICTS:
        _w4_add(
            out, existing, rng,
            f"കേരളത്തിലെ '{hq}' ഏത് ജില്ലയുടെ ആസ്ഥാനമാണ്?",
            district,
            _pool(dist_names, district)[:3],
            "medium",
            dist_names,
        )

    # --- Wave 4b: extra topics with fresh stem templates ---
    plateaus = [p for p, _ in INDIAN_PLATEAUS]
    plateau_regions = list({r for _, r in INDIAN_PLATEAUS})
    for plateau, region in INDIAN_PLATEAUS:
        _w4_add(
            out, existing, rng,
            f"'{plateau}' ഏത് ഭാഗത്ത്/പ്രദേശത്താണ് സ്ഥിതി ചെയ്യുന്നത്?",
            region,
            [r for r in plateau_regions if r != region],
            "medium",
            plateau_regions,
        )

    deserts = [d for d, _ in WORLD_DESERTS]
    desert_locs = list({l for _, l in WORLD_DESERTS})
    for desert, loc in WORLD_DESERTS:
        _w4_add(
            out, existing, rng,
            f"ലോകത്തിലെ '{desert}' മരുഭൂമി ഏത് പ്രദേശത്താണ്?",
            loc,
            [x for x in desert_locs if x != loc],
            "medium",
            desert_locs,
        )

    beaches = [b for b, _ in INDIAN_BEACHES]
    beach_states = list({s for _, s in INDIAN_BEACHES})
    for beach, state in INDIAN_BEACHES:
        _w4_add(
            out, existing, rng,
            f"'{beach}' പ്രശസ്തമായ സമുദ്രത്തീരം ഏത് സംസ്ഥാനത്താണ്?",
            state,
            [s for s in beach_states if s != state],
            "easy",
            beach_states,
        )

    for state, lang in STATE_LANGUAGES:
        st = _norm_state(state)
        _w4_add(
            out, existing, rng,
            f"'{lang}' ഏത് സംസ്ഥാനത്തിന്റെ ഔദ്യോഗിക ഭാഷയാണ്?",
            st,
            [s for s, l in STATE_LANGUAGES if l != lang],
            "medium",
            [s for s, _ in STATE_LANGUAGES],
        )

    for q, ans, wrong, diff in GEO_WAVE4_DIRECT:
        _w4_add(out, existing, rng, q, ans, wrong, diff, wrong + [ans])

    # Alternate stems for extra unique questions
    for crop, state in CROPS:
        st = _norm_state(state)
        _w4_add(
            out, existing, rng,
            f"ഏത് സംസ്ഥാനം '{crop}' ഉൽപ്പാദനത്തിൽ ഇന്ത്യയിൽ മുൻനിരയിലാണ്?",
            st,
            [s for s in crop_states if s != st],
            "medium",
            crop_states,
        )
    for city, river in CITY_RIVER:
        _w4_add(
            out, existing, rng,
            f"'{city}' നഗരം സ്ഥിതി ചെയ്യുന്ന പ്രധാന നദി ഏത്?",
            river,
            [r for r in rivers if r != river],
            "medium",
            rivers,
        )
    for hill, state in HILL_STATIONS:
        st = _norm_state(state)
        _w4_add(
            out, existing, rng,
            f"'{hill}' ഹിൽ സ്റ്റേഷൻ ഏത് സംസ്ഥാനത്താണ്?",
            st,
            [s for s in hill_states if s != st],
            "easy",
            hill_states,
        )
    for trib, main in TRIBUTARIES:
        _w4_add(
            out, existing, rng,
            f"'{main}' നദിയുടെ പോഷക നദി '{trib}' — ശരിയോ?",
            "ശരി",
            ["തെറ്റ്", "പ്രധാന നദിയാണ്", "സമുദ്രത്തിലേക്ക് പതിക്കുന്നു"],
            "hard",
            ["ശരി", "തെറ്റ്", "പ്രധാന നദിയാണ്", "സമുദ്രത്തിലേക്ക് പതിക്കുന്നു"],
        )


    return out


_validate_all_data()
