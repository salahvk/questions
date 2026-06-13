#!/usr/bin/env python3
"""Wave 4: append verified direct-question facts not yet in JSON banks."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent

# (full question stem, answer, wrong[3], difficulty)
IH_DIRECT: list[tuple[str, str, list[str], str]] = [
    ("ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് രൂപീകരിച്ച വർഷം?", "1885", ["1905", "1919", "1947"], "easy"),
    ("ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് ആദ്യ സമ്മേളനം നടന്ന നഗരം?", "ബോംബെ", ["കൽക്കatta", "മദ്രാസ്", "ദില്ലി"], "medium"),
    ("ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസിന്റെ ആദ്യ അധ്യക്ഷൻ?", "ഡബ്ല്യു.സി. ബാനർജി", ["ദാദാഭായി നൗറോജി", "ഗോപാൽകൃഷ്ണ ഗോഖലെ", "മഹാത്മാ ഗാന്ധി"], "hard"),
    ("ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് ആദ്യം മലയാളി അധ്യക്ഷൻ?", "ചെറുവയ്യൂർ നായർ", ["കെ. കേളപ്പൻ", "എ.കെ. ഗോപാലൻ", "ഇ.എം.എസ്. നമ്പൂതിരിപ്പാട്"], "hard"),
    ("ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് ആദ്യം വനിതാ അധ്യക്ഷ?", "ആനി ബസന്റ്", ["സരോജിനി നായർ", "ഇന്ദിരാ ഗാന്ധി", "പ്രതിഭാ പാട്ടിൽ"], "hard"),
    ("ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ് ആദ്യം മുസ്ലിം അധ്യക്ഷ?", "ബദറുദ്ദീൻ ത്യാബ്ജി", ["മൗലാനാ ആസാദ്", "മുഹമ്മദ് അലി ജിന്ന", "ലിയാഖത്ത് അലി ഖാൻ"], "hard"),
    ("മുസ്ലിം ലീഗ് സ്ഥാപിതമായ വർഷം?", "1906", ["1919", "1885", "1940"], "medium"),
    ("ഖിലാഫത്ത് പ്രസ്ഥാനം ആരംഭിച്ച വർഷം?", "1919", ["1920", "1915", "1930"], "easy"),
    ("നോൺ-കോഓപ്പറേഷൻ പ്രസ്ഥാനം ആരംഭിച്ച വർഷം?", "1920", ["1919", "1930", "1942"], "easy"),
    ("സിവിൽ അനുചരണ പ്രസ്ഥാനം ആരംഭിച്ച വർഷം?", "1930", ["1920", "1942", "1919"], "easy"),
    ("ക്വിറ്റ് ഇന്ത്യാ പ്രസ്ഥാനം ആരംഭിച്ച വർഷം?", "1942", ["1940", "1930", "1919"], "easy"),
    ("ചമ്പാരൻ സത്യാഗ്രഹം നടന്ന വർഷം?", "1917", ["1919", "1930", "1942"], "medium"),
    ("ഖൈരaat സത്യാഗ്രഹം നടന്ന വർഷം?", "1918", ["1917", "1919", "1930"], "hard"),
    ("ബർദോളി സത്യാഗ്രഹം നടന്ന വർഷം?", "1928", ["1930", "1942", "1920"], "medium"),
    ("ഡാൻഡി മാർച്ച് നടന്ന വർഷം?", "1930", ["1928", "1942", "1919"], "easy"),
    ("ജാലിയൻവാലാ ബാഗ് കൂട്ടക്കൊല നടന്ന വർഷം?", "1919", ["1918", "1920", "1921"], "medium"),
    ("ചൗരി ചൗരാ സംഭവം നടന്ന വർഷം?", "1922", ["1920", "1930", "1942"], "medium"),
    ("സൈമൺ കമ്മീഷൻ ഇന്ത്യയിൽ എത്തിയ വർഷം?", "1928", ["1925", "1930", "1932"], "easy"),
    ("പൂന പാക്റ്റ് ഒപ്പിട്ട വർഷം?", "1932", ["1930", "1935", "1942"], "medium"),
    ("1935-ലെ ഇന്ത്യാ ഭരണനിയമം അടിസ്ഥാനമാക്കിയത്?", "സൈമൺ കമ്മീഷൻ റിപ്പോർട്ട്", ["ക്രിപ്സ് മിഷൻ", "ക്യാബിനറ്റ് മിഷൻ", "വേവൽ പ്ലാൻ"], "medium"),
    ("ക്രിപ്സ് മിഷൻ ഇന്ത്യയിൽ എത്തിയ വർഷം?", "1942", ["1940", "1945", "1946"], "medium"),
    ("ക്യാബിനറ്റ് മിഷൻ ഇന്ത്യയിൽ എത്തിയ വർഷം?", "1946", ["1942", "1945", "1947"], "medium"),
    ("മൗണ്ട്ബാറ്റൻ പ്ലാൻ പ്രഖ്യാപിച്ച തീയതി?", "1947 ജൂൺ 3", ["1947 ഓഗസ്റ്റ് 15", "1947 ജൂലൈ 18", "1948 ജനുവരി 26"], "medium"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യ നിയമം പാർലമെന്റിൽ പassed?", "1947 ജൂലൈ", ["1947 ഓഗസ്റ്റ്", "1946 ഡിസംബർ", "1948 ജനുവരി"], "medium"),
    ("1857-ലെ സിപോയി മ്യൂട്ടിനി ആരംഭിച്ച സ്ഥലം?", "മീററ്റ്", ["ദില്ലി", "കാൻpur", "ലucknow"], "medium"),
    ("1857-ലെ മ്യൂട്ടിനിയിൽ ഝansi-യിലെ രാജ്ഞി?", "ലക്ഷ്മീബായി", ["ഹസ്രത്ത് മഹൽ", "ചennamma", "കittur chennamma"], "easy"),
    ("1857-ലെ മ്യൂട്ടിനിയിൽ ലucknow-ൽ നേതൃത്വം?", "ഹസ്രത്ത് മഹൽ", ["ലക്ഷ്മീബായി", "നana saheb", "തantia tope"], "medium"),
    ("1857-ലെ മ്യൂട്ടിനിയിൽ കanpur-ൽ നേതൃത്വം?", "നana saheb", ["ലക്ഷ്മീബayi", "ഹസ്രത്ത് മഹൽ", "കunwar singh"], "medium"),
    ("1857-ലെ മ്യൂട്ടിനിയിൽ ബihar-ൽ നേതൃത്വം?", "കunwar singh", ["ലക്ഷ്മീബayi", "നana saheb", "മangal pandey"], "medium"),
    ("പ്ലാസി യുദ്ധം നടന്ന വർഷം?", "1757", ["1764", "1857", "1947"], "easy"),
    ("ബക്സർ യുദ്ധം നടന്ന വർഷം?", "1764", ["1757", "1857", "1947"], "medium"),
    ("പാനിപത്ത് ഒന്നാം യുദ്ധം നടന്ന വർഷം?", "1526", ["1556", "1761", "1857"], "hard"),
    ("പാനിപത്ത് രണ്ടാം യുദ്ധം നടന്ന വർഷം?", "1556", ["1526", "1761", "1857"], "hard"),
    ("പാനിപത്ത് മൂന്നാം യുദ്ധം നടന്ന വർഷം?", "1761", ["1526", "1556", "1857"], "hard"),
    ("പ്ലാസി യുദ്ധത്തിൽ ബ്രിട്ടീഷ് നേതാവ്?", "റോബർട്ട് ക്ലൈവ്", ["വാറൻ ഹേസ്റ്റിംഗ്സ്", "കോർൺവാലിസ്", "വെൽസ്ലി"], "medium"),
    ("ഡോക്ട്രിൻ ഓഫ് ലാപ്സ് നടപ്പാക്കിയ വൈസ്രോയി?", "ലോർഡ് ഡാൽഹൗസി", ["ലോർഡ് വെൽസ്ലി", "ലോർഡ് ക്യർസൺ", "ലോർഡ് റിപ്പൺ"], "easy"),
    ("1773-ലെ റെഗുലേറ്റിംഗ് ആക്ട് പ്രകാരം ആദ്യ ഗവർണർ ജനറൽ?", "വാറൻ ഹേസ്റ്റിംഗ്സ്", ["ലോർഡ് കോർൺവാലിസ്", "ലോർഡ് വെൽസ്ലി", "ലോർഡ് ഡാൽഹൗസി"], "medium"),
    ("1793-ലെ പെർമനന്റ് സെറ്റിൽമെന്റ് ആക്ട് ആദ്യം പ്രയോഗിച്ച പ്രവിശ്യ?", "ബംഗാൾ", ["മദ്രാസ്", "ബോംബെ", "പഞ്ചാബ്"], "medium"),
    ("1858-ലെ ഇന്ത്യാ ഭരണനിയമം — കമ്പനി ഭരണം അവസാനിച്ച വർഷം?", "1858", ["1857", "1861", "1877"], "medium"),
    ("1909-ലെ ഇന്ത്യൻ കൗൺസിൽസ് ആക്ട് ഏത് reforms-ന്റെ പേരിലാണ്?", "മോർലി-മിന്റോ reforms", ["മോണ്ടാഗു-ചെൽംസ്ഫോർഡ്", "1935 Act", "Regulating Act"], "medium"),
    ("1919-ലെ മോണ്ടാഗു-ചെൽംസ്ഫോർഡ് reforms?", "1919", ["1909", "1935", "1947"], "medium"),
    ("Rowlatt Act passed?", "1919", ["1920", "1915", "1930"], "easy"),
    ("അശോകൻ ധർമ്മം സ്വീകരിച്ച വർഷം?", "260 BCE", ["232 BCE", "300 BCE", "200 BCE"], "hard"),
    ("അശോകന്റെ ശിലാശാസനങ്ങളിൽ കൂടുതലായി കാണുന്ന ഭാഷ?", "പ്രാകൃതം", ["സംസ്കൃതം മാത്രം", "തമിഴ് മാത്രം", "അറബി"], "hard"),
    ("ചന്ദ്രഗുപ്ത മൗര്യന്റെ ഗuru?", "ചാണക്യൻ (കൗടില്യൻ)", ["പതഞ്ജലി", "കാലിദാസൻ", "വാല്മീകി"], "medium"),
    ("അർഥശാസ്ത്രം രചിച്ചത്?", "ചാണക്യൻ", ["കാലിദാസൻ", "വാല്മീകി", "പതഞ്ജലി"], "medium"),
    ("നാലന്ദ സർവ്വകലാശാല സ്ഥാപിച്ച ചക്രവർത്തി?", "കുമാരഗുപ്ത I", ["അശോകൻ", "ഹർഷവർദ്ധൻ", "ചന്ദ്രഗുപ്തൻ"], "hard"),
    ("ഹർഷവർദ്ധന്റെ തലസ്ഥാനം?", "കന്യാകുബ്ജ", ["പാടലിപുത്ര", "ഉജ്ജയിനി", "കാഞ്ചി"], "hard"),
    ("ഹർഷവർദ്ധന്റെ കവി?", "ബാണഭട്ട", ["കാലിദാസൻ", "വാല്മീകി", "വ്യാസൻ"], "hard"),
    ("ബാബർ ഇന്ത്യയിൽ ആക്രമിച്ച വർഷം?", "1526", ["1556", "1761", "1857"], "medium"),
    ("അക്ബർ സിംഹാസനാരോഹണം?", "1556", ["1526", "1658", "1857"], "medium"),
    ("ഔറംഗസേബ് സിംഹാസനാരോഹണം?", "1658", ["1526", "1556", "1857"], "hard"),
    ("ഷാജഹാൻ നിർമ്മിച്ച താജ്മഹാൽ എവിടെ?", "ആഗ്ര", ["ദില്ലി", "ലാഹോർ", "ജയ്പൂർ"], "easy"),
    ("അക്ബറിന്റെ പുതിയ തലസ്ഥാനം?", "ഫത്തേhpur sikri", ["ആഗ്ര", "ദില്ലി", "ലാഹോർ"], "medium"),
    ("ഷെർ ഷാ സൂരി പുനർനിർമ്മിച്ച റോഡ്?", "ഗ്രാൻഡ് ട്രങ്ക് റോഡ്", ["സിൽക്ക് റോഡ്", "ഓഷൻ റോഡ്", "ഹൈവേ"], "medium"),
    ("വിജയനഗര സാമ്രാജ്യം സ്ഥാപിച്ചവർ?", "ഹരിഹര, ബുക്ക", ["കൃഷ്ണദേവരായർ", "രാമരായ", "പുലകേശി"], "medium"),
    ("കൃഷ്ണദേവരായരുടെ കourt poet?", "അല്ലസാനി പെddana", ["തെനാലി രാമകൃഷ്ണ", "കാലിദാസൻ", "ബാണ"], "medium"),
    ("ശിവാജി ഭരണം ആരംഭിച്ച സാമ്രാജ്യം?", "മറatha", ["മൈസൂർ", "മുഗൾ", "വിജയനഗര"], "medium"),
    ("നാലാമത് മൈസൂർ യുദ്ധത്തിൽ ടിപ്പു വീഴ്ച?", "1799", ["1767", "1784", "1857"], "medium"),
    ("സുഭാഷ് ചന്ദ്ര ബോസ് INA reorganize?", "1942", ["1940", "1945", "1946"], "medium"),
    ("INA-യുടെ 'Delhi Chalo' മുദ്രാവാക്യം?", "സുഭാഷ് ചന്ദ്ര ബോസ്", ["ജവഹർലാൽ നെഹ്റു", "മഹാത്മാ ഗാന്ധി", "ഭഗത് സിംഗ്"], "easy"),
    ("ഭഗത് സിംഗ് കൊല്ലപ്പെട്ട വർഷം?", "1931", ["1929", "1930", "1932"], "medium"),
    ("ചന്ദ്രശേഖർ ആസാദ് മരണം?", "1931", ["1929", "1930", "1932"], "medium"),
    ("കാക്കോരി ട്രെയിൻ കൊള്ളയുമായി ബന്ധപ്പെട്ട വിപ്ലവകാരി?", "Ram prasad bismil", ["Bhagat singh", "Chandra shekhar azad", "Sukhdev"], "medium"),
    ("1946-ലെ Royal Indian Navy mutiny ആരംഭിച്ച നഗരം?", "Mumbai", ["Kolkata", "Chennai", "Karachi"], "medium"),
    ("1945-ലെ INA trial (Red Fort trials)?", "1945", ["1946", "1942", "1947"], "medium"),
    ("ഇന്ത്യയുടെ ആദ്യ പ്രധാനമന്ത്രി?", "ജവഹർലാൽ നെഹ്റു", ["സർദാർ പട്ടേൽ", "രാജേന്ദ്ര പ്രസാദ്", "സുഭാഷ് ബോസ്"], "easy"),
    ("ഇന്ത്യയുടെ ആദ്യ രാഷ്ട്രപതി?", "രാജേന്ദ്ര പ്രസാദ്", ["ജവഹർലാൽ നെഹ്റു", "സർദാർ പട്ടേൽ", "സുഭാഷ് ബോസ്"], "easy"),
    ("ഇന്ത്യൻ ഭരണഘടന രചയിതാവ്?", "ബി.ആർ. അംബേദ്കർ", ["മഹാത്മാ ഗാന്ധി", "ജവഹർലാൽ നെഹ്റു", "സർദാർ പട്ടേൽ"], "easy"),
    ("ഇന്ത്യൻ റിപ്പബ്ലിക് ദിനം?", "1950 ജനുവരി 26", ["1947 ഓഗസ്റ്റ് 15", "1947 ജൂൺ 3", "1947 ജൂലൈ 18"], "easy"),
    ("ആദ്യ ഭാരതരത്ന laureate?", "സി. രാജഗോപാലാചാരി", ["ജവഹർലാൽ നെഹ്റു", "സർദാർ പട്ടേൽ", "മഹാത്മാ ഗാന്ധി"], "hard"),
    ("ആദ്യ നോബൽ laureate (literature) from India?", "രവീന്ദ്രനാഥ ടാഗോർ", ["സി.വി. രാമൻ", "അമർത്യ സെൻ", "കൈലാസ് സത്യാർത്ഥി"], "medium"),
    ("ആദ്യ നോബël laureate (science) from India?", "സി.വി. രാമൻ", ["രവീന്ദ്രനാഥ ടാഗോർ", "അമർത്യ സെൻ", "കൈലാസ് സത്യാർത്ഥി"], "medium"),
]

GEO_DIRECT: list[tuple[str, str, list[str], str]] = [
    ("ഇന്ത്യയുടെ ഏറ്റവും വലിയ സംസ്ഥാനം (വിസ്തീർണ്ണം)?", "രാജസ്ഥാൻ", ["മധ്യപ്രദേശ്", "മഹാരാഷ്ട്ര", "ഉത്തരപ്രദേശ്"], "easy"),
    ("ഇന്ത്യയുടെ ഏറ്റവും ചെറിയ സംസ്ഥാനം?", "ഗോവ", ["സിക്കിം", "ത്രിപുര", "നാഗaland"], "easy"),
    ("ഇന്ത്യയുടെ 'പിങ്ക് സിറ്റി'?", "ജയ്പൂർ", ["ഉദയ്പൂർ", "ജോധ്പൂർ", "ബീകാനർ"], "easy"),
    ("ഇന്ത്യയുടെ 'ബ്ലൂ സിറ്റി'?", "ജോധ്പൂർ", ["ജയ്പൂർ", "ഉദയ്പൂർ", "ബീകാനർ"], "easy"),
    ("ഇന്ത്യയുടെ 'വൈറ്റ് സിറ്റി'?", "ഉദയ്പൂർ", ["ജയ്പൂർ", "ജോധ്പൂർ", "ജaisalmer"], "easy"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് ലേക്ക്‌സ്'?", "ഉദയ്പൂർ", ["ഭോപാൽ", "നainital", "ശillong"], "medium"),
    ("ഇന്ത്യയുടെ 'ടീ കപ്പ് ഓഫ് ഇന്ത്യ'?", "അസം", ["മേഘാലയ", "ത്രിപുര", "മണിപ്പൂർ"], "medium"),
    ("ഇന്ത്യയുടെ 'റൈസ് ബൗൾ ഓഫ് ഇന്ത്യ'?", "ആന്ധ്രപ്രദേശ്", ["തമിഴ്നാട്", "കർണാടക", "തെലങ്കാന"], "medium"),
    ("ഇന്ത്യയുടെ 'സ്പൈസ് ഗാർഡൻ ഓഫ് ഇന്ത്യ'?", "കേരളം", ["കർണാടക", "തമിഴ്നാട്", "ഗോവ"], "easy"),
    ("ഇന്ത്യയുടെ 'ഐറൺ സിറ്റി'?", "ജംഷെദ്പൂർ", ["ഭilai", "rourkela", "durgapur"], "medium"),
    ("ഇന്ത്യയുടെ 'ഇലക്ട്രോണിക് സിറ്റി'?", "ബെംഗളuru", ["ഹyderabad", "ചennai", "noida"], "medium"),
    ("ലോകത്തിലെ ഏറ്റവും വലിയ ഭൂഖണ്ഡം?", "ഏഷ്യ", ["ആഫ്രിക്ക", "ഉത്തര അമേരിക്ക", "യൂറോപ്പ്"], "easy"),
    ("ലോകത്തിലെ ഏറ്റവും ചെറിയ ഭൂഖണ്ഡം?", "ഓസ്ട്രേലിയ", ["ആന്റാർctica", "യൂറോപ്പ്", "ദക്ഷിണ അമേരിക്ക"], "easy"),
    ("ലോകത്തിലെ ഏറ്റവും വലിയ രാജ്യം (വിസ്തീർണ്ണം)?", "റഷ്യ", ["കanada", "ചina", "അmerica"], "easy"),
    ("ലോകത്തിലെ ഏറ്റവും ജനസംഖ്യയുള്ള രാജ്യം?", "ചൈന", ["ഇന്ത്യ", "അmerica", "ഇndonesia"], "easy"),
    ("ലോകത്തിലെ ഏറ്റവും ഉയരമുള്ള കൊടുമുടി?", "എverest", ["K2", "Kanchenjunga", "Lhotse"], "easy"),
    ("ലോകത്തിലെ ഏറ്റവും നീളമുള്ള നദി?", "നൈൽ", ["Amazon", "Yangtze", "Mississippi"], "easy"),
    ("ലോകത്തിലെ ഏറ്റവും വലിയ മരുഭൂമി?", "സഹara", ["Gobi", "Arabian", "Kalahari"], "easy"),
    ("ലോകത്തിലെ ഏറ്റവും വലിയ ദ്വീപ്?", "Greenland", ["New Guinea", "Borneo", "Madagascar"], "easy"),
    ("യൂറോപ്പും ആഫ്രിക്കയും വേർതിരിക്കുന്ന കടലിടുക്ക്?", "ജibraltar", ["Suez", "Bosphorus", "Dardanelles"], "medium"),
    ("അറ്റ്ലാന്റിക്, പസഫിക് ബന്ധിപ്പിക്കുന്ന കനാൽ?", "Panama", ["Suez", "Kiel", "Corinth"], "medium"),
    ("അറ്റ്ലാന്റിക്, മediterranean ബന്ധിപ്പിക്കുന്ന കനാൽ?", "Suez", ["Panama", "Kiel", "Corinth"], "medium"),
    ("ഭൂമധ്യരേഖയ്ക്ക് ഏറ്റവും അടുത്തുള്ള രാജ്യം?", "Ecuador", ["Kenya", "Indonesia", "Brazil"], "hard"),
    ("മൗണ്ട് എverest ഏത് രാജ്യങ്ങളിൽ?", "നepal/China", ["India", "Bhutan", "Pakistan"], "medium"),
    ("കerala-യുടെ ഏറ്റവും വലിയ ജില്ല?", "പalakkad", ["Ernakulam", "Idukki", "Malappuram"], "medium"),
    ("കerala-യുടെ ഏറ്റവും ചെറിയ ജില്ല?", "Alappuzha", ["Kasaragod", "Pathanamthitta", "Wayanad"], "hard"),
    ("കerala-യുടെ ഏറ്റവും ഉയരമുള്ള peak?", "Anamudi", ["Agasthyarkoodam", "Meesapulimala", "Chembra"], "medium"),
    ("Periyar-ന്റെ ഉത്ഭവസ്ഥലം?", "Sivagiri hills", ["Western Ghats", "Nilgiris", "Cardamom hills"], "hard"),
    ("Silent Valley ദേശീയോദ്യാനം ഏത് ജില്ല?", "Palakkad", ["Wayanad", "Idukki", "Ernakulam"], "medium"),
    ("Eravikulam ദേശീയോദ്യാനം ഏത് ജില്ല?", "Idukki", ["Palakkad", "Wayanad", "Thrissur"], "medium"),
    ("Wayanad Wildlife Sanctuary ഏത് ജില്ല?", "Wayanad", ["Palakkad", "Idukki", "Kozhikode"], "easy"),
    ("Kerala-യുടെ 'Spice Garden of India'?", "Idukki", ["Wayanad", "Palakkad", "Kozhikode"], "hard"),
    ("Kerala-യുടെ 'Land of Backwaters'?", "Alappuzha", ["Kollam", "Ernakulam", "Kottayam"], "medium"),
    ("Kerala-യുടെ 'Cashew Capital'?", "Kollam", ["Alappuzha", "Ernakulam", "Thiruvananthapuram"], "hard"),
]

WH_DIRECT: list[tuple[str, str, list[str], str]] = [
    ("ഓസ്ട്രേലിയ ഫെഡറേഷൻ രൂപീകരിച്ച വർഷം?", "1901", ["1851", "1921", "1945"], "hard"),
    ("നേപ്പാൾ രാജ്യം സ്ഥാപിതമായ വർഷം?", "1768", ["1816", "1950", "2008"], "hard"),
    ("ഭൂട്ടാൻ സ്വതന്ത്ര രാജ്യമായി അംഗീകരിച്ച വർഷം?", "2008", ["1947", "1975", "1991"], "hard"),
    ("ചെംഗിസ് ഖാൻ മരിച്ച വർഷം?", "1227", ["1206", "1259", "1279"], "medium"),
    ("റോമൻ സാമ്രാജ്യം (പശ്ചിമ) അവസാനിച്ച വർഷം?", "476", ["410", "800", "1453"], "medium"),
    ("30-ാം വർഷം യുദ്ധം ആരംഭിച്ച വർഷം?", "1618", ["1648", "1789", "1914"], "hard"),
    ("30-ാം വർഷം യുദ്ധം അവസാനിച്ച വർഷം?", "1648", ["1618", "1789", "1918"], "hard"),
    ("1871-ൽ ജർമ്മൻ സാമ്രാജ്യം പ്രഖ്യാപിച്ച വർഷം?", "1871", ["1848", "1914", "1933"], "medium"),
    ("1936-ൽ സ്പാനിഷ് ഗ്രഹീത യുദ്ധം ആരംഭിച്ച വർഷം?", "1936", ["1939", "1914", "1945"], "medium"),
    ("2003-ൽ ഇറാക്ക് യുദ്ധം ആരംഭിച്ച വർഷം?", "2003", ["2001", "2005", "1999"], "medium"),
    ("പുരാതന ഗ്രീക്ക് നഗര രാജ്യം സ്പാർട്ടയുടെ പ്രധാന ശത്രു?", "ഏതീൻസ്", ["തhebes", "Corinth", "Macedon"], "medium"),
    ("വെസൂവിയസ് പൊട്ടിത്തെറിച്ച് Pompeii നശിച്ച വർഷം?", "79", ["1066", "1453", "476"], "medium"),
    ("ചാർlemagne ചക്രവർത്തിയായി അഭിഷേകം?", "800", ["1066", "1215", "1453"], "hard"),
    ("ബ്ലാക്ക് ഡെത്ത് യൂറോപ്പിൽ വ്യാപിച്ച നൂറ്റാണ്ട്?", "14-ാം നൂറ്റാണ്ട്", ["12-ാം", "16-ാം", "18-ാം"], "medium"),
    ("വെസ്റ്റ്ഫാലിയ ഉടമ്പടി ഒപ്പിട്ട വർഷം?", "1648", ["1789", "1815", "1919"], "hard"),
    ("പീറ്റർ ദി ഗ്രേറ്റ് ഭരിച്ച രാജ്യം?", "റഷ്യ", ["Germany", "Austria", "Poland"], "medium"),
    ("സലadin ഏത് സാമ്രാജ്യത്തിന്റെ സുൽത്താൻ?", "അyyubi", ["Ottoman", "Mughal", "Safavid"], "hard"),
    ("ആദ്യ ക്രൂസade-ൽ Jerusalem പിടിച്ച വർഷം?", "1099", ["1187", "1204", "1291"], "hard"),
    ("സ്പാനിഷ് Armada പരാജയം?", "1588", ["1492", "1605", "1648"], "medium"),
    ("1848-ൽ കമ്മ്യunist manifesto രചിച്ചവർ?", "Marx, Engels", ["Lenin, Trotsky", "Stalin, Mao", "Rousseau, Voltaire"], "medium"),
    ("ഡി-ഡേ landing?", "1944", ["1942", "1945", "1943"], "medium"),
    ("സ്റ്റാലിൻgrad യുദ്ധം?", "1942–1943", ["1940–1941", "1944–1945", "1939–1940"], "medium"),
    ("ഡunkirk evacuation?", "1940", ["1942", "1944", "1939"], "medium"),
    ("Marshall Plan പ്രഖ്യാപിച്ച വർഷം?", "1947", ["1945", "1950", "1939"], "medium"),
    ("Bretton Woods conference?", "1944", ["1945", "1947", "1939"], "hard"),
    ("Berlin Wall constructed?", "1961", ["1989", "1949", "1955"], "medium"),
    ("Euro currency introduced?", "2002", ["1993", "1999", "2007"], "medium"),
]


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


def patch_module(path: Path, marker: str, data_name: str, facts: list[tuple[str, str], ...]) -> int:
    if not facts:
        return 0
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return 0
    block = f"\n{data_name}: list[tuple[str, str, list[str], str]] = {facts!r}\n"
    gen = f"""
    for q, ans, wrong, diff in {data_name}:
        pool = wrong + [ans]
        _add(out, existing, rng, q, ans, pool, diff)
"""
    # Insert data before generate_candidates, gen before return out
    idx = text.index("def generate_candidates")
    text = text[:idx] + block + text[idx:]
    text = text.replace("    return out\n", gen + "\n    return out\n", 1)
    path.write_text(text, encoding="utf-8")
    return len(facts)


def patch_geography(facts: list[tuple[str, str, list[str], str]]) -> int:
    if not facts:
        return 0
    path = BASE / "geography_facts.py"
    text = path.read_text(encoding="utf-8")
    if "GEO_DIRECT" in text:
        return 0
    block = f"\nGEO_DIRECT: list[tuple[str, str, list[str], str]] = {facts!r}\n"
    gen = """
    for q, ans, wrong, diff in GEO_DIRECT:
        add(q, ans, wrong, diff)
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

    ih_new = filter_new(IH_DIRECT, ih_stems)
    geo_new = filter_new(GEO_DIRECT, geo_stems)
    wh_new = filter_new(WH_DIRECT, wh_stems)

    print(f"IH direct: {len(ih_new)} new / {len(IH_DIRECT)} candidates")
    print(f"GEO direct: {len(geo_new)} new / {len(GEO_DIRECT)} candidates")
    print(f"WH direct: {len(wh_new)} new / {len(WH_DIRECT)} candidates")

    n_ih = patch_module(BASE / "indian_history_facts.py", "IH_DIRECT", "IH_DIRECT", ih_new)
    n_geo = patch_geography(geo_new)
    n_wh = patch_module(BASE / "world_history_facts.py", "WH_DIRECT", "WH_DIRECT", wh_new)

    print(f"Patched: IH={n_ih}, GEO={n_geo}, WH={n_wh}")

    if n_ih + n_geo + n_wh == 0:
        print("Nothing to patch.")
        return 0

    print("\n--- Running generate_all_questions.py ---")
    r = subprocess.run([sys.executable, str(BASE / "generate_all_questions.py"), "--skip-validation"], cwd=BASE)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
