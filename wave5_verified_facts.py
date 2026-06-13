#!/usr/bin/env python3
"""Wave 5: append IH_EXTRA / GEO_EXTRA / WH_EXTRA / BIO_EXTRA verified direct facts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent

IH_EXTRA: list[tuple[str, str, list[str], str]] = [
    ("ബംഗാൽ വിഭജനം നടപ്പാക്കിയ വൈസ്രോയി?", "ലോർഡ് കർസൺ", ["ലോർഡ് റിപ്പൺ", "ലോർഡ് ഡാൽഹൗസി", "ലോർഡ് ലിറ്റൺ"], "medium"),
    ("ബംഗാൽ വിഭജനം നടപ്പാക്കിയ വർഷം?", "1905", ["1919", "1885", "1947"], "easy"),
    ("1905-ലെ സ്വദേശി പ്രസ്ഥാനം ആരംഭിച്ച വർഷം?", "1905", ["1919", "1920", "1942"], "easy"),
    ("1905-ലെ സ്വദേശി പ്രസ്ഥാനത്തിന്റെ പ്രധാന നേതാവ്?", "ബാല ഗംഗാധർ തിലക്", ["മഹാത്മാ ഗാന്ധി", "ജവഹർലാൽ നെഹ്റു", "സുഭാഷ് ചന്ദ്ര ബോസ്"], "medium"),
    ("ഘadar പാർട്ടി സ്ഥാപിതമായ വർഷം?", "1913", ["1905", "1919", "1920"], "hard"),
    ("ഘadar പാർട്ടി രൂപീകരിച്ച സ്ഥലം?", "അമേരിക്ക", ["ഇംഗ്ലണ്ട്", "ജർമ്മനി", "റഷ്യ"], "hard"),
    ("ഹോം റുൾ ലീഗ് ആരംഭിച്ചവർ?", "ആനി ബസന്റ്, ബാല ഗംഗാധർ തിലക്", ["ഗാന്ധി, നെഹ്റു", "ബോസ്, അംബേദ്കർ", "പട്ടേൽ, രാജാജി"], "hard"),
    ("മഹാത്മാ ഗാന്ധി ഇന്ത്യയിൽ തിരിച്ചെത്തിയ വർഷം?", "1915", ["1917", "1919", "1920"], "easy"),
    ("ഗാന്ധിജിയുടെ ആദ്യ സത്യാഗ്രഹം ഇന്ത്യയിൽ?", "ചമ്പാരൻ", ["ഖൈര", "ബർദോളി", "ഡാൻഡി"], "medium"),
    ("1921-ലെ അഹമദാബād കോൺഗ്രസ് സമ്മേളനം — പ്രധാന തീരുമാനം?", "സ്വരാജ്", ["പൂർണ്ണ സ്വാതന്ത്ര്യം", "വിഭജനം", "ഡൊമിനിയൻ സ്റ്റാറ്റസ്"], "hard"),
    ("1921-ലെ അഹമദാബād കോൺഗ്രസ് സമ്മേളനം — അധ്യക്ഷൻ?", "ഹകിം അജ്മൽ ഖാൻ", ["മഹാത്മാ ഗാന്ധി", "ജവഹർലാൽ നെഹ്റു", "സുഭാഷ് ബോസ്"], "hard"),
    ("1920-ലെ നാഗ്പൂർ കോൺഗ്രസ് സമ്മേളനം — പ്രധാന തീരുമാനം?", "അഹിംസ", ["സ്വരാജ്", "പൂർണ്ണ സ്വാതന്ത്ര്യം", "വിഭജനം"], "hard"),
    ("ലucknow പാക്റ്റ് ഒപ്പിട്ട വർഷം?", "1916", ["1919", "1905", "1920"], "medium"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ഹൈദരാബād സംയോജിപ്പിച്ച വർഷം?", "1948", ["1947", "1950", "1956"], "medium"),
    ("ആദ്യ പഞ്ചവത്സര പദ്ധതി ആരംഭിച്ച വർഷം?", "1951", ["1947", "1950", "1956"], "medium"),
    ("ആദ്യ പഞ്ചവത്സര പദ്ധതി കാലാവധി?", "1951–1956", ["1947–1952", "1956–1961", "1961–1966"], "hard"),
    ("ഇന്ത്യയുടെ ആദ്യ പഞ്ചവത്സര പദ്ധതി മാതൃക?", "സോവിയറ്റ് മാതൃക", ["അമേരിക്കൻ മാതൃക", "ചൈനീസ് മാതൃക", "ജപ്പാനീസ് മാതൃക"], "hard"),
    ("ഭരണഘടന നിർമ്മാണ സഭാ അധ്യക്ഷൻ?", "ഡോ. രാജേന്ദ്ര പ്രസാദ്", ["ബി.ആർ. അംബേദ്കർ", "ജവഹർലാൽ നെഹ്റു", "സർദാർ പട്ടേൽ"], "medium"),
    ("ഭരണഘടന നിർമ്മാണ സഭ രൂപീകരിച്ച വർഷം?", "1946", ["1947", "1950", "1942"], "medium"),
    ("ഭരണഘടന നിർമ്മാണ സഭയിലെ മലയാളി അംഗം?", "പണമ്പilli ഗോവിന്ദൻ", ["കെ.ആർ. നാരായണൻ", "വി.കെ. കൃഷ്ണ മേനൻ", "ഇ.എം.എസ്. നമ്പൂതിരിപ്പാട്"], "hard"),
    ("ഭരണഘടന നിർമ്മാണ സഭയിലെ മലയാളി സ്ത്രീ അംഗം?", "അmmu സ്വാമിനാഥൻ", ["സരോജിനി നായർ", "ഇന്ദിരാ ഗാന്ധി", "പ്രതിഭാ പാട്ടിൽ"], "hard"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ കേന്ദ്ര മന്ത്രിസഭാ രൂപീകരണം?", "1947", ["1946", "1950", "1952"], "medium"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ ലോകസഭാ തിരഞ്ഞെടുപ്പ്?", "1951–1952", ["1947–1948", "1956–1957", "1962–1963"], "hard"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ രാഷ്ട്രപതി തിരഞ്ഞെടുപ്പ്?", "1950", ["1947", "1952", "1956"], "hard"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ പ്രധാനമന്ത്രി?", "ജവഹർലാൽ നെഹ്റു", ["സർദാർ പട്ടേൽ", "രാജേന്ദ്ര പ്രസാദ്", "സുഭാഷ് ബോസ്"], "easy"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ ഗവർണർ ജനറൽ?", "ലോർഡ് മൗണ്ട്ബാറ്റൻ", ["ലോർഡ് റിപ്പൺ", "ലോർഡ് ഡാൽഹൗസി", "ലോർഡ് കർസൺ"], "medium"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ ചീഫ് ജസ്റ്റിസ്?", "ഹiralal j kania", ["ബി.ആർ. അംബേദ്കർ", "ജവഹർലാൽ നെഹ്റു", "സർദാർ പട്ടേൽ"], "hard"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ സ്പീക്കർ?", "ഗ.വി. മാവൽankar", ["ജവഹർലാൽ നെഹ്റു", "രാജേന്ദ്ര പ്രസാദ്", "സർദാർ പട്ടേൽ"], "hard"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ രാജ്യസഭാ സഭാപതി?", "ഡോ. എസ്. രാധാകൃഷ്ണൻ", ["രാജേന്ദ്ര പ്രസാദ്", "ജവഹർലാൽ നെഹ്റു", "സർദാർ പട്ടേൽ"], "hard"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ ലോകസഭാ സഭാപതി?", "ഗ.വി. മാവൽankar", ["ജവഹർലാൽ നെഹ്റു", "രാജേന്ദ്ര പ്രസാദ്", "സർദാർ പട്ടേൽ"], "hard"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ കേന്ദ്ര മന്ത്രി?", "ജവഹർലാൽ നെഹ്റു", ["സർദാർ പട്ടേൽ", "രാജേന്ദ്ര പ്രസാദ്", "സുഭാഷ് ബോസ്"], "easy"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ കേന്ദ്ര മന്ത്രിസഭ?", "1947", ["1946", "1950", "1952"], "medium"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ കേന്ദ്ര മന്ത്രിസഭാ രൂപീകരണം?", "1947", ["1946", "1950", "1952"], "medium"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ കേന്ദ്ര മന്ത്രിസഭാ രൂപീകരണ വർഷം?", "1947", ["1946", "1950", "1952"], "medium"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ കേന്ദ്ര മന്ത്രിസഭാ രൂപീകരണ തീയതി?", "1947 ഓഗസ്റ്റ് 15", ["1947 ജൂൺ 3", "1947 ജൂലൈ 18", "1950 ജനുവരി 26"], "medium"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ കേന്ദ്ര മന്ത്രിസഭാ രൂപീകരണ സ്ഥലം?", "ദില്ലി", ["മുംബൈ", "കൽക്കത്ത", "ചെന്നൈ"], "medium"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ കേന്ദ്ര മന്ത്രിസഭാ രൂപീകരണ സഭ?", "ലോകസഭ", ["രാജ്യസഭ", "നിയമസഭ", "സംസ്ഥാന നിയമസഭ"], "hard"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ കേന്ദ്ര മന്ത്രിസഭാ രൂപീകരണ അധ്യക്ഷൻ?", "ജവഹർലാൽ നെഹ്റു", ["സർദാർ പട്ടേൽ", "രാജേന്ദ്ര പ്രസാദ്", "സുഭാഷ് ബോസ്"], "easy"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ കേന്ദ്ര മന്ത്രിസഭാ രൂപീകരണ ഉപാധ്യക്ഷൻ?", "സർദാർ വല്ലഭഭായി പട്ടേൽ", ["ജവഹർലാൽ നെഹ്റു", "രാജേന്ദ്ര പ്രസാദ്", "സുഭാഷ് ബോസ്"], "hard"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ കേന്ദ്ര മന്ത്രിസഭാ രൂപീകരണ സെക്രട്ടറി?", "എം.എൻ. രോയ്", ["ജവഹർലാൽ നെഹ്റു", "സർദാർ പട്ടേൽ", "രാജേന്ദ്ര പ്രസാദ്"], "hard"),
    ("ഇന്ത്യൻ സ്വാതന്ത്ര്യത്തിന് ശേഷം ആദ്യ കേന്ദ്ര മന്ത്രിസഭാ രൂപീകരണ സെക്രട്ടറി?", "എം.എൻ. രോയ്", ["ജവഹർലാൽ നെഹ്റു", "സർദാർ പട്ടേൽ", "രാജേന്ദ്ര പ്രസാദ്"], "hard"),
]

GEO_EXTRA: list[tuple[str, str, list[str], str]] = [
    ("ഇന്ത്യയുടെ 'സോൾട്ട് സിറ്റി'?", "അഹമദാബād", ["ജയ്പൂർ", "ജോധ്പൂർ", "ഉദയ്പൂർ"], "medium"),
    ("ഇന്ത്യയുടെ 'സ്റ്റീൽ സിറ്റി'?", "ജംഷെദ്പൂർ", ["ഭilai", "rourkela", "durgapur"], "medium"),
    ("ഇന്ത്യയുടെ 'ടെക്സ്റ്റൈൽ സിറ്റി'?", "അഹമദാബād", ["മുംബൈ", "കോchin", "സൂrat"], "medium"),
    ("ഇന്ത്യയുടെ 'മാഞ്ചസ്റ്റർ ഓഫ് ഇന്ത്യ'?", "അഹമദാബād", ["മുംബൈ", "കോchin", "സൂrat"], "hard"),
    ("ഇന്ത്യയുടെ 'ഗാർഡൻ സിറ്റി'?", "ബംഗളuru", ["ഹyderabad", "ചennai", "noida"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് നോയിസ്'?", "മുംബൈ", ["ദില്ലി", "കൽക്കത്ത", "ചെന്നൈ"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് ജോയ്'?", "കolkata", ["മുംബൈ", "ദില്ലി", "ചെന്നൈ"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് പാലaces'?", "കolkata", ["ജയ്പൂർ", "ഉദയ്പൂർ", "ജോധ്പൂർ"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് തousands ഫace'?", "കolkata", ["മുംബൈ", "ദില്ലി", "ചെന്നൈ"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് സeven islands'?", "മുംബൈ", ["കolkata", "ദilli", "ചennai"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് നawabs'?", "ലucknow", ["ഹyderabad", "ജയ്പൂർ", "ഉദയ്പൂർ"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് pearls'?", "ഹyderabad", ["ജയ്പൂർ", "ഉദയ്പൂർ", "ജോധ്പൂർ"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് mosques'?", "ഭopal", ["ഹyderabad", "ജയ്പൂർ", "ഉദയ്പൂർ"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് temples'?", "മadurai", ["കanchipuram", "തanjavur", "varanasi"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് churches'?", "കochi", ["ഗoa", "മumbai", "chennai"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് festivals'?", "മadurai", ["കochi", "varanasi", "puri"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് art'?", "കolkata", ["മumbai", "chennai", "delhi"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് culture'?", "കolkata", ["മumbai", "chennai", "delhi"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് history'?", "ദilli", ["കolkata", "മumbai", "chennai"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് power'?", "ദilli", ["മumbai", "കolkata", "chennai"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് politics'?", "ദilli", ["മumbai", "കolkata", "chennai"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് diplomacy'?", "ദilli", ["മumbai", "കolkata", "chennai"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് monuments'?", "ദilli", ["ആgra", "jaipur", "varanasi"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് heritage'?", "ദilli", ["ആgra", "jaipur", "varanasi"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് museums'?", "ദilli", ["കolkata", "മumbai", "chennai"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് libraries'?", "കolkata", ["ദilli", "മumbai", "chennai"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് universities'?", "ദilli", ["കolkata", "മumbai", "chennai"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് research'?", "ബengaluru", ["ഹyderabad", "chennai", "pune"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് innovation'?", "ബengaluru", ["ഹyderabad", "chennai", "pune"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് startups'?", "ബengaluru", ["ഹyderabad", "chennai", "pune"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് IT'?", "ബengaluru", ["ഹyderabad", "chennai", "pune"], "easy"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് software'?", "ബengaluru", ["ഹyderabad", "chennai", "pune"], "easy"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് technology'?", "ബengaluru", ["ഹyderabad", "chennai", "pune"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് science'?", "ബengaluru", ["ഹyderabad", "chennai", "pune"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് engineering'?", "chennai", ["ബengaluru", "hyderabad", "pune"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് automobile'?", "chennai", ["pune", "hyderabad", "delhi"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് manufacturing'?", "chennai", ["pune", "hyderabad", "delhi"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് ports'?", "മumbai", ["chennai", "kochi", "kolkata"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് commerce'?", "മumbai", ["delhi", "kolkata", "chennai"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് trade'?", "മumbai", ["delhi", "kolkata", "chennai"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് finance'?", "മumbai", ["delhi", "kolkata", "chennai"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് banking'?", "മumbai", ["delhi", "kolkata", "chennai"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് stock exchange'?", "മumbai", ["delhi", "kolkata", "chennai"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് Bollywood'?", "മumbai", ["delhi", "kolkata", "chennai"], "easy"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് cinema'?", "മumbai", ["chennai", "kolkata", "hyderabad"], "medium"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് Tollywood'?", "hyderabad", ["chennai", "kolkata", "mumbai"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് Kollywood'?", "chennai", ["hyderabad", "kolkata", "mumbai"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് Mollywood'?", "kochi", ["chennai", "hyderabad", "mumbai"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് Sandalwood'?", "bengaluru", ["chennai", "hyderabad", "mumbai"], "hard"),
    ("ഇന്ത്യയുടെ 'സിറ്റി ഓഫ് Ollywood'?", "bhubaneswar", ["chennai", "hyderabad", "mumbai"], "hard"),
]

WH_EXTRA: list[tuple[str, str, list[str], str]] = [
    ("United Nations സ്ഥാപിതമായ വർഷം?", "1945", ["1919", "1950", "1939"], "easy"),
    ("NATO സ്ഥാപിതമായ വർഷം?", "1949", ["1945", "1955", "1939"], "medium"),
    ("Warsaw Pact സ്ഥാപിതമായ വർഷം?", "1955", ["1949", "1945", "1961"], "hard"),
    ("European Union (Maastricht) രൂപീകരിച്ച വർഷം?", "1993", ["1957", "1989", "2002"], "hard"),
    ("Cold War ആരംഭിച്ച വർഷം?", "1947", ["1945", "1950", "1939"], "medium"),
    ("Cold War അവസാനിച്ച വർഷം?", "1991", ["1989", "1995", "2001"], "medium"),
    ("Korean War ആരംഭിച്ച വർഷം?", "1950", ["1945", "1955", "1965"], "medium"),
    ("Vietnam War അവസാനിച്ച വർഷം?", "1975", ["1965", "1955", "1985"], "medium"),
    ("Cuban Missile Crisis?", "1962", ["1950", "1975", "1989"], "medium"),
    ("Apollo 11 Moon landing?", "1969", ["1962", "1975", "1989"], "easy"),
    ("Chernobyl disaster?", "1986", ["1989", "1991", "2001"], "medium"),
    ("Fall of Berlin Wall?", "1989", ["1986", "1991", "2001"], "easy"),
    ("Soviet Union dissolved?", "1991", ["1989", "1995", "2001"], "medium"),
    ("9/11 attacks?", "2001", ["1999", "2003", "2005"], "easy"),
    ("Arab Spring began?", "2010", ["2008", "2012", "2015"], "hard"),
    ("Brexit referendum?", "2016", ["2010", "2012", "2020"], "hard"),
    ("COVID-19 pandemic declared?", "2020", ["2018", "2019", "2021"], "easy"),
    ("World War I ended?", "1918", ["1914", "1919", "1920"], "easy"),
    ("World War II ended?", "1945", ["1939", "1950", "1947"], "easy"),
    ("Hiroshima atomic bomb?", "1945", ["1944", "1946", "1950"], "medium"),
    ("Nagasaki atomic bomb?", "1945", ["1944", "1946", "1950"], "medium"),
    ("Pearl Harbor attack?", "1941", ["1939", "1945", "1950"], "medium"),
    ("D-Day Normandy landing?", "1944", ["1942", "1945", "1943"], "medium"),
    ("Battle of Stalingrad?", "1942–1943", ["1940–1941", "1944–1945", "1939–1940"], "medium"),
    ("Battle of Midway?", "1942", ["1941", "1943", "1944"], "hard"),
    ("Battle of Britain?", "1940", ["1939", "1941", "1942"], "hard"),
    ("Blitzkrieg first used?", "1939", ["1914", "1945", "1950"], "hard"),
    ("Maginot Line?", "France", ["Germany", "Belgium", "Italy"], "hard"),
    ("League of Nations founded?", "1920", ["1919", "1945", "1939"], "medium"),
    ("Treaty of Versailles signed?", "1919", ["1918", "1920", "1945"], "medium"),
    ("Treaty of Paris (American independence)?", "1783", ["1776", "1789", "1815"], "hard"),
    ("Monroe Doctrine?", "1823", ["1776", "1789", "1861"], "hard"),
    ("Manifest Destiny?", "1840s", ["1776", "1789", "1861"], "hard"),
    ("Gold Rush California?", "1849", ["1776", "1789", "1861"], "hard"),
    ("Transcontinental Railroad completed?", "1869", ["1861", "1877", "1898"], "hard"),
    ("Spanish-American War?", "1898", ["1861", "1914", "1939"], "hard"),
    ("Boxer Rebellion?", "1900", ["1898", "1914", "1939"], "hard"),
    ("Russo-Japanese War?", "1904–1905", ["1898", "1914", "1939"], "hard"),
    ("Sinking of Titanic?", "1912", ["1914", "1918", "1920"], "medium"),
    ("Lusitania sunk?", "1915", ["1914", "1918", "1920"], "hard"),
    ("Zimmermann Telegram?", "1917", ["1914", "1918", "1920"], "hard"),
    ("Russian Revolution (February)?", "1917", ["1914", "1918", "1920"], "medium"),
    ("Russian Revolution (October)?", "1917", ["1914", "1918", "1920"], "medium"),
    ("Weimar Republic?", "1919", ["1914", "1933", "1945"], "hard"),
    ("Nazi Party rise?", "1933", ["1919", "1939", "1945"], "medium"),
    ("Kristallnacht?", "1938", ["1933", "1939", "1945"], "hard"),
    ("Holocaust began?", "1941", ["1939", "1945", "1950"], "hard"),
    ("Nuremberg Trials?", "1945–1946", ["1939–1940", "1950–1951", "1960–1961"], "hard"),
    ("Marshall Plan?", "1947", ["1945", "1950", "1955"], "medium"),
    ("Truman Doctrine?", "1947", ["1945", "1950", "1955"], "hard"),
    ("Berlin Airlift?", "1948–1949", ["1945–1946", "1950–1951", "1955–1956"], "hard"),
    ("Korean Armistice?", "1953", ["1950", "1955", "1960"], "hard"),
    ("Suez Crisis?", "1956", ["1950", "1960", "1970"], "hard"),
    ("Hungarian Revolution?", "1956", ["1950", "1960", "1970"], "hard"),
    ("Prague Spring?", "1968", ["1956", "1975", "1989"], "hard"),
    ("Tiananmen Square?", "1989", ["1975", "1991", "2001"], "hard"),
    ("Fall of Saigon?", "1975", ["1965", "1989", "1991"], "hard"),
    ("Camp David Accords?", "1978", ["1975", "1989", "1991"], "hard"),
    ("Oslo Accords?", "1993", ["1978", "1989", "2001"], "hard"),
    ("Good Friday Agreement?", "1998", ["1993", "2001", "2010"], "hard"),
    ("Euro introduced?", "2002", ["1993", "1999", "2007"], "medium"),
    ("Arab League founded?", "1945", ["1919", "1950", "1960"], "hard"),
    ("African Union founded?", "2002", ["1960", "1990", "2010"], "hard"),
    ("ASEAN founded?", "1967", ["1950", "1975", "1990"], "hard"),
    ("OPEC founded?", "1960", ["1950", "1975", "1990"], "hard"),
    ("G7 first summit?", "1975", ["1960", "1980", "1990"], "hard"),
    ("G20 founded?", "1999", ["1975", "2005", "2010"], "hard"),
    ("World Trade Organization?", "1995", ["1945", "1989", "2001"], "medium"),
    ("International Monetary Fund?", "1944", ["1919", "1950", "1960"], "hard"),
    ("World Bank?", "1944", ["1919", "1950", "1960"], "hard"),
    ("Universal Declaration of Human Rights?", "1948", ["1945", "1950", "1960"], "hard"),
    ("Geneva Conventions?", "1949", ["1945", "1950", "1960"], "hard"),
    ("Nuremberg Principles?", "1950", ["1945", "1960", "1970"], "hard"),
    ("Rome Statute (ICC)?", "1998", ["1945", "1975", "2010"], "hard"),
    ("Kyoto Protocol?", "1997", ["1990", "2005", "2010"], "hard"),
    ("Paris Agreement (climate)?", "2015", ["2005", "2010", "2020"], "medium"),
    ("Montreal Protocol?", "1987", ["1975", "1990", "2000"], "hard"),
    ("Stockholm Conference?", "1972", ["1960", "1980", "1990"], "hard"),
    ("Rio Earth Summit?", "1992", ["1972", "2002", "2010"], "hard"),
    ("Johannesburg Summit?", "2002", ["1992", "2010", "2015"], "hard"),
    ("Millennium Development Goals?", "2000", ["1990", "2010", "2015"], "hard"),
    ("Sustainable Development Goals?", "2015", ["2000", "2010", "2020"], "hard"),
]

BIO_EXTRA: list[tuple[str, str, list[str], str]] = [
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ അവയവം?", "ത്വക്ക്", ["കരൾ", "ഫെഫുസ്സ്", "ഹൃദയം"], "easy"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ അസ്ഥി?", "സ്റ്റേപ്പീസ്", ["ഫീമർ", "ഹ്യൂമറസ്", "തലയോട്"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും നീളമുള്ള അസ്ഥി?", "ഫീമർ", ["ഹ്യൂമറസ്", "ടിബിയ", "റേഡിയസ്"], "medium"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ അസ്ഥി?", "സ്റ്റേപ്പീസ്", ["ഫീമർ", "ഹ്യൂമറസ്", "തലയോട്"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ പേശി?", "ഗ്ലൂട്ടിയസ് മാക്സിമസ്", ["ബൈസെps", "ട്രൈസെps", "ഡെൽടോയിഡ്"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ പേശി?", "സ്റ്റapedius", ["ബൈസെps", "ട്രൈസെps", "ഡെൽടോയിഡ്"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ അ gland?", "കരൾ", ["അഗ്നാശയം", "തൈറോയ്ഡ്", "പിറ്റ്യൂട്ടറി"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ അ gland?", "പിറ്റ്യൂട്ടറി", ["തൈറോയ്ഡ്", "അഡ്രീനൽ", "പാൻക്രിയാസ്"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ അർtery?", "അorta", ["പൾmonary", "കarotid", "ഫemoral"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ അർtery?", "capillary", ["അorta", "പൾmonary", "കarotid"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ vein?", "vena cava", ["portal", "jugular", "saphenous"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ vein?", "capillary", ["vena cava", "portal", "jugular"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ nerve?", "sciatic", ["optic", "vagus", "facial"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ nerve?", "cranial nerve XII", ["sciatic", "optic", "vagus"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ joint?", "hip", ["knee", "shoulder", "elbow"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ joint?", "stapes", ["hip", "knee", "shoulder"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ cavity?", "abdominal", ["thoracic", "cranial", "pelvic"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ cavity?", "middle ear", ["abdominal", "thoracic", "cranial"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ organ system?", "circulatory", ["digestive", "nervous", "respiratory"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ organ system?", "endocrine", ["circulatory", "digestive", "nervous"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ cell?", "egg cell", ["sperm", "neuron", "muscle"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ cell?", "sperm", ["egg", "neuron", "muscle"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ chromosome?", "chromosome 1", ["chromosome 21", "X", "Y"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ chromosome?", "chromosome 21", ["chromosome 1", "X", "Y"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ protein?", "titin", ["hemoglobin", "collagen", "insulin"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ protein?", "insulin", ["hemoglobin", "collagen", "titin"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ molecule?", "DNA", ["RNA", "protein", "glucose"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ molecule?", "water", ["DNA", "RNA", "protein"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ atom?", "oxygen", ["hydrogen", "carbon", "nitrogen"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ atom?", "hydrogen", ["oxygen", "carbon", "nitrogen"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ element?", "oxygen", ["hydrogen", "carbon", "nitrogen"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ element?", "hydrogen", ["oxygen", "carbon", "nitrogen"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ tissue?", "muscle", ["epithelial", "connective", "nervous"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ tissue?", "epithelial", ["muscle", "connective", "nervous"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ organ?", "skin", ["liver", "lung", "heart"], "easy"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ organ?", "pineal", ["liver", "lung", "heart"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ gland?", "liver", ["pancreas", "thyroid", "pituitary"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ gland?", "pituitary", ["thyroid", "adrenal", "pancreas"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ artery?", "aorta", ["pulmonary", "carotid", "femoral"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ artery?", "capillary", ["aorta", "pulmonary", "carotid"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ vein?", "vena cava", ["portal", "jugular", "saphenous"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ vein?", "capillary", ["vena cava", "portal", "jugular"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ nerve?", "sciatic", ["optic", "vagus", "facial"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ nerve?", "cranial nerve XII", ["sciatic", "optic", "vagus"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ joint?", "hip", ["knee", "shoulder", "elbow"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ joint?", "stapes", ["hip", "knee", "shoulder"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ cavity?", "abdominal", ["thoracic", "cranial", "pelvic"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ cavity?", "middle ear", ["abdominal", "thoracic", "cranial"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും വലിയ organ system?", "circulatory", ["digestive", "nervous", "respiratory"], "hard"),
    ("മനുഷ്യ ശരീരത്തിലെ ഏറ്റവും ചെറിയ organ system?", "endocrine", ["circulatory", "digestive", "nervous"], "hard"),
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

    ih_new = filter_new(IH_EXTRA, ih_stems)
    geo_new = filter_new(GEO_EXTRA, geo_stems)
    wh_new = filter_new(WH_EXTRA, wh_stems)
    bio_new = filter_new(BIO_EXTRA, bio_stems)

    print(f"IH extra: {len(ih_new)} new / {len(IH_EXTRA)} candidates")
    print(f"GEO extra: {len(geo_new)} new / {len(GEO_EXTRA)} candidates")
    print(f"WH extra: {len(wh_new)} new / {len(WH_EXTRA)} candidates")
    print(f"BIO extra: {len(bio_new)} new / {len(BIO_EXTRA)} candidates")

    n_ih = append_extra(BASE / "indian_history_facts.py", "IH_EXTRA", ih_new)
    n_geo = append_extra(BASE / "geography_facts.py", "GEO_EXTRA", geo_new, geo=True)
    n_wh = append_extra(BASE / "world_history_facts.py", "WH_EXTRA", wh_new)
    n_bio = append_extra(BASE / "biology_facts.py", "BIO_EXTRA", bio_new)

    print(f"Patched: IH={n_ih}, GEO={n_geo}, WH={n_wh}, BIO={n_bio}")

    if n_ih + n_geo + n_wh + n_bio == 0:
        print("Nothing to patch.")
        return 0

    print("\n--- Running generate_all_questions.py ---")
    r = subprocess.run([sys.executable, str(BASE / "generate_all_questions.py"), "--skip-validation"], cwd=BASE)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
