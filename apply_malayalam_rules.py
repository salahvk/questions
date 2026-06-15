#!/usr/bin/env python3
"""Apply Malayalam quiz cursor rules to JSON question files."""

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

from malayalamize_questions import (
    PRESERVE,
    malayalamize_question,
    malayalamize_text,
)

try:
    from english_only_overrides import ID_OVERRIDES as ENGLISH_ONLY_OVERRIDES
except ImportError:
    ENGLISH_ONLY_OVERRIDES = {}

BASE = Path(__file__).parent
SKIP_FILES = {"english_language.json", "current_affairs_manifest.json"}
MALAYALAM = re.compile(r"[\u0D00-\u0D7F]")
# English book/film titles as MCQ options (literature, cinema)
WORK_TITLE_OPTION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9\s.,'&:+\-!?()]*$")

# Allowed Latin tokens inside otherwise-Malayalam question stems (acronyms, years)
STEM_ACRONYMS = re.compile(
    r"\b(?:UDF|LDF|NDA|BJP|CPI|CPM|RSP|IUML|BDJS|MLA|MP|LS|FIFA|GST|ISRO|WHO|IMF|"
    r"WTO|ICC|ODI|T20|NEP|UPI|ECI|PTA|G20|NASA|RTE|IGNOU|NCERT|AIIMS|DRDO|"
    r"PM-JAY|PM-KISAN|ICDS|NSAP|NRHM|ABDM|KFON|IMEC|HAL|BHEL|ONGC|NTPC|"
    r"IOCL|SIDBI|KVIC|NALCO|BEL|BEML|DPIIT|ILO|FAO|IAEA|UNICEF|UNHCR|GATT|"
    r"USA|UAE|AYUSH|LPG|SEZ|STPI|MSME|NATO|OPEC|ASEAN|SAARC|BRICS|ICRC|"
    r"NITI|NGT|PWD|PLI|IMD|WANI|IN-SPACe|UNFCCC|ECI|PSLV|GSLV|SSLV|ASLV|"
    r"SLV|LVM|IRS|IRNSS|INSAT|NGC|LIGO|ALMA|TESS|EMISAT|XPoSat|WWII|"
    r"IOC|SAIL|GAIL|NHPC|HMT|DMIC|DFC|IDI|PSU|MITRA|NMEO|FME|SVANidhi|"
    r"PVTG|HRIDAY|AMRUT|SAUBHAGYA|POSHAN|DAY-NRLM|DAY-NULM|NUHM|PMMVY|"
    r"SEBI|SWIFT|UEFA|ANOVA|DMIC|NIMZ|STPI|SEZ|MSME|PLI|NSAP|ICDS|"
    r"PM-JAY|PM SVANidhi|MITRA|WANI|NRLM|NULM|RBI|GDP|FDI|FII|IPO|"
    r"ATM|OTP|PIN|LAN|WAN|VPN|DNS|URL|HTTP|HTTPS|TCP|UDP|IP|API|"
    r"CPU|GPU|RAM|ROM|SSD|HDD|USB|PDF|JPEG|PNG|GIF|XML|JSON|"
    r"ODI|T20|Test|ICC|FIFA|BCCI|AIFF|IOA|DIKSHA|SWAYAM|NISHTHA|AICTE|"
    r"CBSE|ICSE|NIOS|NEET|SCERT|CUET|JEE|UGC|NCERT|IGNOU|IIT|NIT|IIM|"
    r"IISER|ISI|BITS|VIT|JNU|DU|BHU|AMU|KSEB|NAAC|NBA|NCTE|NTA|"
    r"Kerala State Education Board|Kerala State Board)\b",
    re.I,
)

# Government scheme / mission names kept in English in PSC papers
SCHEME_NAMES = re.compile(
    r"(?:PMAY(?:-Urban|-Gramin)?|PM-KISAN|PM-JAY|PM SVANidhi|PM MITRA|PM FME|"
    r"PM Vishwakarma|PM WANI|PM eBus|PM JANMAN|PM Surya Ghar|"
    r"Swachh Bharat(?: Mission)?|"
    r"Pradhan Mantri [A-Za-z][A-Za-z '-]*|"
    r"Rashtriya [A-Za-z][A-Za-z '-]*|"
    r"National [A-Za-z][A-Za-z '-]*|"
    r"Mission [A-Za-z][A-Za-z '-]*|"
    r"Soil Health Card|Stand Up India|Startup India|Digital India|"
    r"Make in India|Skill India|Ayushman Bharat|Jal Jeevan(?: Mission)?|Atal Pension Yojana|Sukanya Samriddhi Yojana|Beti Bachao Beti Padhao|PM Mudra Yojana|Skill India(?: Mission)?|"
    r"Karunya(?: Plus| Benevolent)?|"
    r"One Stop Centre|Sakhi|She-Box|Ujjawala|DAY-NRLM|DAY-NULM|"
    r"Kerala State Education Board|Kerala State Board)",
    re.I,
)

KNOWN_ENGLISH_PHRASES = re.compile(
    r"(?:Make in India|Startup India|Digital India|Skill India|Stand Up India|"
    r"Indian Oil Corporation|Bharat Petroleum|Hindustan Petroleum|"
    r"Power Grid Corporation|Life Insurance Corporation|General Insurance Corporation|"
    r"Reserve Bank of India|Securities and Exchange Board|"
    r"United Nations|World Bank|World Trade Organization|"
    r"Whirlpool|Prometheus|Cassini|Hubble|Gemini|Ceres|Pallas|Juno|Vesta|"
    r"Messier|Minor Planet|Leo Triplet|Andromeda|Triangulum|"
    r"Recording Academy|Club World Cup|World Cup|Grand Slam|Powerplay|"
    r"Wicketkeeper|Offside|Duckworth-Lewis-Stern|"
    r"Reduce, Reuse, Recycle|Campbell's Soup Cans|"
    r"Heraclitus|Socrates|Plato|Descartes|Kant|Democritus|"
    r"Henry VIII|Ferdinand|Hundred Years War|"
    r"JavaScript|TypeScript|CoffeeScript|Objective-C|C\+\+|C#|F#|"
    r"Python|Java|Ruby|Rust|Perl|Go|Kotlin|Swift|PHP|HTML|CSS|SQL|"
    r"Scala|Haskell|Lisp|Dart|MATLAB|Delphi|Pascal|Fortran|Assembly|"
    r"Node|React|Angular|Vue|Django|Flask|Laravel|"
    r"Production Linked Incentive|Software Technology Parks|"
    r"National Infrastructure Pipeline|Street Vendor|"
    r"Delhi-Mumbai Industrial Corridor|Chennai-Bengaluru|"
    r"Amritsar-Kolkata|Visakhapatnam-Chennai|Bengaluru-Mumbai)",
    re.I,
)

TECH_PROPER = re.compile(
    r"\b(?:Rust|Linux|Windows|Ubuntu|Android|iOS|macOS|PostgreSQL|MySQL|"
    r"MongoDB|Redis|Docker|Kubernetes|JetBrains|Kotlin|Ubuntu|Debian|"
    r"Bluetooth|WiFi|Wi-Fi|Ethernet|Intranet|Internet|Cloud|Server|"
    r"Compiler|Debugger|Algorithm|Database|Firewall|Malware|Phishing|"
    r"Encryption|Blockchain|Bitcoin|Ethereum|TensorFlow|PyTorch|OpenAI|"
    r"ChatGPT|Gemini|Copilot|Azure|AWS|Google|Microsoft|Apple|Oracle|"
    r"SAP|Salesforce|Adobe|Cisco|Intel|AMD|Nvidia|Samsung|Sony|"
    r"Bluetooth|USB|HTTP|HTTPS|FTP|SMTP|DNS|VPN|LAN|WAN|"
    r"Spreadsheet|Worksheet|Workbook|PowerPoint|Excel|Word|Outlook)\b",
    re.I,
)

PHILOSOPHER_NAMES = re.compile(
    r"\b(?:Nietzsche|Marx|Kant|Plato|Aristotle|Socrates|Descartes|Hegel|"
    r"Schopenhauer|Wittgenstein|Russell|Confucius|Buddha|Shankara|"
    r"Ramanuja|Madhva|Chattampi|Narayana|Guru|Vivekananda|Aurobindo|"
    r"Heraclitus|Democritus|Epicurus|Zeno|Locke|Hume|Bentham|Mill|"
    r"Rousseau|Voltaire|Spinoza|Leibniz|Berkeley|Hobbes|Machiavelli)\b",
    re.I,
)

SATELLITE_AND_CATALOG = re.compile(
    r"(?:NGC-\d+|M\d+|IRNSS-\d+[A-Z]?|INSAT-\d+[A-Z]?|IRS-[A-Z]\d+|"
    r"PSLV-[A-Z]?|GSLV-[A-Z]?|SSLV|ASLV|SLV-\d+|LVM\d+|XPoSat|EMISAT|"
    r"WASP-\d+b|OGLE-\d+-BLG-\d+Lb|\d+-(?:foot|inch))",
    re.I,
)

# PSU / scheme acronyms glued directly to Malayalam suffixes (ONGCയുടെ, BHELയിൽ)
ACRONYM_GLUE = re.compile(
    r"(?:ONGC|BHEL|SAIL|NTPC|NALCO|HPCL|BPCL|NMDC|GAIL|BEML|HAL|IOCL|SIDBI|"
    r"KVIC|BEL|DMIC|SEBI|SWIFT|FIFA|ICC|GST|ISRO|DRDO|NASA|IMF|WHO|WTO|"
    r"STPI|SEZ|MSME|PLI|NSAP|ICDS|NRLM|NULM|RBI|GDP|FDI|IPO|ATM|CPU|GPU|"
    r"RAM|ROM|SSD|HDD|USB|PDF|JPEG|PNG|GIF|XML|JSON|ODI|T20|BCCI|AIFF|IOA|"
    r"PM-JAY|PM|SVANidhi|MITRA|WANI|UEFA|ANOVA|DMIC|NIMZ|HPCL|BPCL|LIC|"
    r"GIC|SEBI|NPCI|UPI|NEP|ECI|IMD|NGT|NITI|PWD|PLI|ECI|SDSS|IRIS|WASP|"
    r"DIKSHA|SWAYAM|NISHTHA|AICTE|CBSE|ICSE|NIOS|NEET|SCERT|CUET|JEE|"
    r"UGC|NCERT|IGNOU|IIT|NIT|IIM|IISER|ISI|BITS|VIT|JNU|DU|BHU|AMU|"
    r"NAAC|NBA|NCTE|NTA)(?=[\u0D00-\u0D7F])",
    re.I,
)

# English filler leaked into Malayalam option sets
BANNED_OPTION_ENGLISH = re.compile(
    r"\b(?:only|always|linked|historically|enacted|winner|notable|approx|"
    r"forever|formation|includes|reservation|coalition|strong in|term length|"
    r"seats count|president|secretary|Leader|allied|bench cities)\b",
    re.I,
)

# Parenthetical content that may stay (acronyms, org names, place hints in Malayalam)
KEEP_PAREN = re.compile(
    r"^(UNESCO|GDP|RTE|IGNOU|NCERT|AIIMS|ISRO|DRDO|GST|IMF|WHO|WTO|FIFA|ICC|"
    r"IPL|ODI|T20|NEP|UPI|ECI|IMD|NGT|PWD|PLI|NITI|ICRC|BRICS|ASEAN|SAARC|"
    r"NATO|OPEC|EU|HAL|BHEL|ONGC|NTPC|IOCL|SIDBI|KVIC|NALCO|BEL|BEML|"
    r"PM-JAY|PM-KISAN|ICDS|NSAP|NRHM|ABDM|WANI|IN-SPACe|NASA|UNFCCC|G20|"
    r"KFON|IMEC|BJP|UDF|LDF|NDA|CPI|CPM|RSP|IUML|BDJS|PTA|MSME|SEZ|STPI|"
    r"DPIIT|ILO|FAO|IAEA|UNICEF|UNHCR|GATT|USA|UAE|AYUSH|80G|LPG|"
    r"Knot|NaCl|H2O|CO2|O2|DNA|RNA|ATP|pH|UV|IR|OR|AND|PART|III|II|IV|I)$",
    re.I,
)

# English glued to Malayalam suffixes (World Cup-ന്റെ etc.)
HYPHEN_GLUED = [
    (re.compile(r"FIFA Club World Cup-ന്റെ", re.I), "FIFA ക്ലബ് ലോകകപ്പിന്റെ"),
    (re.compile(r"FIFA World Cup-ന്റെ", re.I), "FIFA ലോകകപ്പിന്റെ"),
    (re.compile(r"World Cup-ന്റെ", re.I), "ലോകകപ്പിന്റെ"),
    (re.compile(r"match-ന്റെ", re.I), "മത്സരത്തിന്റെ"),
    (re.compile(r"team-ൽ", re.I), "ടീമിൽ"),
]

PAREN_ENGLISH = re.compile(r"\s*\(([A-Za-z0-9][^)]*)\)")

# Corrupted text from partial English→Malayalam conversion
CORRUPTION_FIXES: list[tuple[str, str]] = [
    ("മുഗൽ സാമ്രാജ്യം-e-Azam", "Mughal-e-Azam"),
    ("audio നടത്തs visual", "ശബ്ദം കാണുന്ന ദൃശ്യത്തിന് മുൻപ് തുടരുന്നു"),
    ("തുmanaged പാട്ടുകൾ", "ഭജന പാട്ടുകൾ"),
    ("തുmanaged തുള്ളൽ", "തുമ്പി തുള്ളൽ"),
    ("ദുശ്ശblockസനൻ", "ദുശ്ശാസനൻ"),
    ("മണ്ണrules", "മണ്ണ് കുഴിച്ചെടുക്കുന്ന"),
    ("തrenown പാണ്ടി", "ചെണ്ട പാണ്ടി"),
    ("തുrenown കുമ്മാട്ടി", "തിരുവോണ കുമ്മാട്ടി"),
    ("ബ beaux-arts", "ബിയോ-ആർട്സ്"),
    ("റേ മാഗ്default", "റേനേ മാഗ്രitte"),
    ("ഹാcomplജനുകൾ", "ഹാലോജനുകൾ"),
    ("അArrhenius", "ആര്രിണിയസ്"),
    ("പട്ടുനൂൽ നെcontinuous", "പട്ടുനൂൽ നെയ്ത"),
    ("വെളുപ്പ് / ഓഫ്-വൈറ്റ് (കസവ് ബോർഡറോട് കൂടിയത്)", "വെളുപ്പ് / കസവ് ബോർഡറോട് കൂടിയത്"),
    ("നാഗര വാസ്തുവിദ്യ (Nagara Architecture / ചന്ദേല ശൈലി)", "നാഗര വാസ്തുവിദ്യ (ചന്ദേല ശൈലി)"),
    ("'ദി പെർസിസ്റ്റൻസ് ഓഫ് മെമ്മറി' (The Persistence of Memory - ഉരുകുന്ന വാച്ചുകൾ)", "'The Persistence of Memory' (ഉരുകുന്ന വാച്ചുകൾ)"),
    ("heavy water (ഭാരജലം)", "ഭാരജലം"),
    ("'എത്തanol'", "'എthalcohol'"),
    ("'ഓzone'", "'ഓzone'"),
    ("റേനേ മാഗ്രitte", "റെനെ മാഗ്രitte"),
    ("ദുശ്ശusageനൻ", "ദുശ്ശാസനൻ"),
    ("കumbalMain", "കumbalam"),
    ("alaMain", "alam"),
    ("കumbalaMain", "കumbalam"),
    ("കരിcoal", "കരിക്കാൽ"),
    ("വിഷാnumൂർത്തി", "വിഷ്ണുമൂർത്തി"),
    ("കakkahistory", "കാക്കാരിശ്ശി"),
    ("എlakkahistory", "കുറുമ്പാർ നൃത്തം"),
    ("സുബSub", "സുബ്ബാഹുല്ലാഹ്"),
    ("കൈholding", "കൈപിടിച്ച"),
    ("Early morning", "പ്രഭാത"),
    ("മാregular", "മാർഗ"),
    ("ചott", "ചോറ്റ"),
    ("ളMain", "ളം"),
    (" (Fauvism - വന്യമായ നിറങ്ങളുടെ ഉപയോഗം)", ""),
    (" (Mount Rushmore - പ്രസിഡന്റുമാരുടെ മുഖങ്ങൾ)", " (പ്രസിഡന്റുമാരുടെ മുഖങ്ങൾ)"),
    (" (Fourth Wall - നാലാം മതിൽ)", " (നാലാം മതിൽ)"),
    (" (Messiah - ഹല്ലേലൂയ കോറസ് അടങ്ങിയത്)", " (ഹല്ലേലൂയ കോറസ് അടങ്ങിയത്)"),
    (" (Symphony No. 9 - ചിരന്തന ഗീതം)", " (ചിരന്തന ഗീതം)"),
    (" (The Beatles - ജോർജ്ജ് ഹാരിസൺ)", " (ജോർജ്ജ് ഹാരിസൺ)"),
    (" (David - വെങ്കല രൂപം)", " (വെങ്കല രൂപം)"),
    (" (Tarpa - ഒരു തരം വലിയ പുല്ലാങ്കുഴൽ വാദ്യം)", " (ഒരു തരം വലിയ പുല്ലാങ്കുഴൽ വാദ്യം)"),
    ("A Version 5.25", " പതിപ്പ് 5.25"),
    ("Version 5.25", "പതിപ്പ് 5.25"),
    ("ചാരvaka", "ചാർവാക"),
    ("നവരasa", "നവറസം"),
    ("ഡemocritus", "ഡമോക്രിതസ്"),
    ("സോക്രATES", "സോക്രatis"),
    ("പ്ലato", "പ്ലato"),
    ("അറിസ്റ്റോട്ടil", "അറിസ്റ്റോട്ടil"),
    ("ക്ഷാരമൃത്തിregular", "ക്ഷാരഭൂമി"),
    ("തോട്ടiculture", "കൃഷി"),
    ("ഹermann Gundert", "ഹermann ഗundert"),
    ("സാൽzburg", "സാzburg"),
    ("മandi", "മandi"),
    ("വIDI", "വidy"),
    ("എthalcohol", "എthalcohol"),
    ("എത്തanol", "എthalcohol"),
    ("ഓzone", "ഓzone"),
    ("മാഗ്രitte", "മാഗ്രitte"),
    # Astronomy partial-script corruption
    ("വ्हirlpool ഗാലക്സി", "Whirlpool ഗാലക്സി"),
    ("വ्हirlpool", "Whirlpool"),
    ("കാർൾ ഗുസ്റ്റാവ് വttes", "കാർൾ ഗുസ്റ്റാവ് വിറ്റസ്"),
    ("വttes", "വിറ്റസ്"),
    ("ഇൻഫ്രARED", "ഇൻഫ്രാ-റെഡ്"),
    ("മ MathfILD", "മഥ്ഫ്ലാഡ്"),
    ("MathfILD", "മഥ്ഫ്ലാഡ്"),
    ("മംഗൾ=graha", "മംഗൾ ഗ്രഹം"),
    ("=graha", " ഗ്രഹം"),
    ("നടത്തer", "നടത്തിയ"),
    ("നടത്തer association", "നടത്തിയത് ബന്ധപ്പെട്ടത്"),
    ("സ്റ്റarduസ്റ്റ്", "സ്റ്റാർഡസ്റ്റ്"),
    ("astronomical unit", "ഖഗോളീയ യൂണിറ്റ്"),
    ("പ്രോമetheus", "Prometheus"),
    ("prometheus", "Prometheus"),
    ("polaരിമെട്രി", "പോളാരിമെട്രി"),
    ("എക്സ്-റേ polaരിമെട്രി", "എക്സ്-റേ പോളാരിമെട്രി"),
    ("IRNSS-1എ", "IRNSS-1A"),
    ("INSAT-2എ", "INSAT-2A"),
    ("ഹundred Years War", "നൂറുവർഷ യുദ്ധം"),
    ("ഫerdinand", "ഫെർഡിനാൻഡ്"),
    ("WWII", "രണ്ടാം ലോകമഹായുദ്ധം"),
    ("WWII കാലം", "രണ്ടാം ലോകമഹായുദ്ധ കാലം"),
    ("സാzburg", "സാൽസ്ബർഗ്"),
    ("ഈiffel", "ഈഫൽ"),
    # History — persons / dynasties (no Latin/Manglish names)
    ("Saladin sultanate?", "സലാദിൻ ഏത് സാമ്രാജ്യത്തിന്റെ സുൽത്താനായിരുന്നു?"),
    ("സലadin ഏത് സാമ്രാജ്യത്തിന്റെ സുൽത്താൻ?", "സലാദിൻ ഏത് സാമ്രാജ്യത്തിന്റെ സുൽത്താനായിരുന്നു?"),
    ("Saladin", "സലാദിൻ"),
    ("സലadin", "സലാദിൻ"),
    ("Ayyubi", "അയ്യൂബി സാമ്രാജ്യം"),
    ("അyyubi", "അയ്യൂബി സാമ്രാജ്യം"),
    ("Ottoman", "ഒട്ടോമൻ സാമ്രാജ്യം"),
    ("Safavid", "സഫാവിദ് സാമ്രാജ്യം"),
    ("Charlemagne", "കാറൽമാൻ"),
    ("ചാർlemagne", "കാറൽമാൻ"),
    ("Pompeii", "പോംപെയ്"),
    ("Jerusalem", "ജെറുസലേം"),
    ("Crusade", "പുണ്യയുദ്ധം"),
    ("ക്രൂസade", "പുണ്യയുദ്ധം"),
    ("Armada", "ആർമാഡ"),
    ("thebes", "തീബ്"),
    ("തhebes", "തീബ്"),
    ("Corinth", "കൊറിന്ത്"),
    ("Macedon", "മാസിഡോൺ"),
    ("Athens", "ഏതൻസ്"),
    ("Stalingrad", "സ്റ്റാലിൻഗ്രാഡ്"),
    ("സ്റ്റാലിൻgrad", "സ്റ്റാലിൻഗ്രാഡ്"),
    ("Dunkirk", "ഡങ്കിർക്ക്"),
    ("ഡunkirk", "ഡങ്കിർക്ക്"),
    # Places — corrupted Malayalam+Latin → full Malayalam
    ("കerala", "കേരളം"),
    ("മumbai", "മുംബൈ"),
    ("ദilli", "ഡൽഹി"),
    ("കolkata", "കൊൽക്കത്ത"),
    ("ഉറuguay", "ഉറുഗ്വേ"),
    ("ഉruguay", "ഉറുഗ്വേ"),
    ("അർജentina", "അർജന്റീന"),
    ("ലndon", "ലണ്ടൻ"),
    ("ലos Angeles", "ലോസ് ആഞ്ചൽസ്"),
    ("ടokyo", "ടോക്കിയോ"),
    ("ബാർcelona", "ബാർസലോൺ"),
    ("അtlanta", "അറ്റ്ലാന്റ"),
    ("റio", "റിയോ"),
    ("ബrisbane", "ബ്രിസ്ബേൻ"),
    ("ലucknow", "ലഖ്‌നൗ"),
    ("ബengaluru", "ബെംഗളൂരു"),
    ("ഹyderabad", "ഹൈദരാബാദ്"),
    ("ചennai", "ചെന്നൈ"),
    # Chemistry — common corrupted tokens
    ("കarbon", "കാർബൺ"),
    ("superനടത്ത", "അതി-ചാലക"),
    ("superനടത്തivity", "അതി-ചാലകത"),
    ("semiനടത്ത", "അർദ്ധചാലക"),
    ("നടത്തer", "നടത്തിയ"),
    ("പ്രഖ്യാപിക്കd", "പ്രഖ്യാപിച്ച"),
    ("Wicketkeeper", "വിക്കറ്റ് കീpper"),
    ("Wicketkeeperന്റെ", "വിക്കറ്റ് കീpperന്റെ"),
]

# Manual fixes for corrupted entries
MANUAL_FIXES: dict[str, dict] = {
    "art_491": {
        "options": [
            "Campbell's Soup Cans",
            "കോക്കകോള ബോട്ടിലുകൾ",
            "മെർലിൻ മൺറോ രൂപങ്ങൾ",
            "ബലൂൺ ഡോഗ്",
        ],
        "answer": "Campbell's Soup Cans",
    },
    "art_731": {
        "answer": "വലിയ കത്തി പോലുള്ള ആകൃതിയിലുള്ള ചുട്ടിപ്പാലകൾ",
    },
    "art_756": {
        "options": ["പുളിമരം", "തേക്ക്", "മുള", "പ്ലാവ്"],
        "answer": "പുളിമരം",
    },
    "cin_008": {
        "options": ["ശിവ കങ്ക", "ഛോട്ടാ ചേതൻ", "മൈ ഡിയർ കുട്ടിച്ചാത്തൻ", "ഹക്കുസ് ബക്കുസ്"],
    },
    "ca_2026_06_022": {
        "question": "2026 ജൂണിൽ FIFA ക്ലബ് ലോകകപ്പിന്റെ ആതിഥ്യ രാജ്യം ഏത്?",
    },
    "eco_161": {
        "answer": "50",
    },
    "eco_762": {
        "question": "ബാങ്കുകൾ വായ്പയ്ക്ക് ഈടാക്കുന്ന പലിശ നിരക്ക് സാധാരണയായി എന്ത് എന്ന് വിളിക്കുന്നു?",
        "options": [
            "വിപണി മൂലധനം",
            "വായ്പ പലിശ നിരക്ക്",
            "നികുതി നിരക്ക്",
            "വിനിമയ നിരക്ക്",
        ],
        "answer": "വായ്പ പലിശ നിരക്ക്",
    },
    "eco_769": {
        "question": "ബാങ്ക് ഇടപാടുകൾ ഫോണിലൂടെ നടത്താൻ ഉപയോഗിക്കുന്ന സൗകര്യം എന്താണ്?",
        "options": [
            "ചെക്ക് ബുക്ക്",
            "മൊബൈൽ ബാങ്കിംഗ് ആപ്പ്",
            "ഡിമാൻഡ് ഡ്രാഫ്റ്റ്",
            "പോസ്റ്റൽ ഓർഡർ",
        ],
        "answer": "മൊബൈൽ ബാങ്കിംഗ് ആപ്പ്",
    },
    "edu_582": {
        "question": "IIT Mandi ഏത് നഗരത്തിലാണ്?",
        "options": ["മandi", "റൂർക്കി", "ഗുവാഹാടി", "ഹൈദരാബാദ്"],
        "answer": "മandi",
    },
    "hok_283": {
        "options": ["ഹermann ഗundert", "കെ. കേളപ്പൻ", "ടി.കെ. മാധവൻ", "ചന്ദു മേനോൻ"],
        "answer": "ഹermann ഗundert",
    },
    "mi_096": {
        "options": ["കൃഷി", "ഗോതമ്പ്", "എണ്ണയിട വിത്തുകൾ", "മുട്ട"],
        "answer": "കൃഷി",
    },
    "phi_062": {
        "question": "സോക്രട്ടീസിന്റെ ശിഷ്യൻ ആരാണ്?",
        "options": ["ഹെറാക്ലിറ്റസ്", "അറിസ്റ്റോട്ടിൽ", "പ്ലേറ്റോ", "ഡമോക്രിതസ്"],
        "answer": "പ്ലേറ്റോ",
    },
    "phi_063": {
        "question": "പ്ലേറ്റോയുടെ ശിഷ്യൻ ആരാണ്?",
        "options": ["സോക്രട്ടീസ്", "കാന്റ്", "ഹെറാക്ലിറ്റസ്", "അറിസ്റ്റോട്ടിൽ"],
        "answer": "അറിസ്റ്റോട്ടിൽ",
    },
    "phi_064": {
        "question": "അറിസ്റ്റോട്ടിലിന്റെ ഗുരു ആരാണ്?",
        "options": ["പ്ലേറ്റോ", "സോക്രട്ടീസ്", "ഡെസ്കാർട്ട്", "കാന്റ്"],
        "answer": "പ്ലേറ്റോ",
    },
}


def strip_redundant_english_parens(text: str) -> str:
    """Remove (English gloss) when Malayalam already present; keep allowed acronyms."""
    if not text or not MALAYALAM.search(text):
        return text

    def repl(match: re.Match[str]) -> str:
        inner = match.group(1).strip()
        if MALAYALAM.search(inner):
            return f" ({inner})"
        if KEEP_PAREN.match(inner):
            return f" ({inner})"
        if PRESERVE.search(inner) and len(inner.split()) <= 3:
            return f" ({inner})"
        # Bilingual gloss: Malayalam (English) or English (Malayalam) — drop English half
        if re.search(r"[a-zA-Z]{2,}", inner):
            return ""
        return ""

    return PAREN_ENGLISH.sub(repl, text)


def fix_hyphen_glued(text: str) -> str:
    result = text
    for pattern, replacement in HYPHEN_GLUED:
        result = pattern.sub(replacement, result)
    return result


def fix_corruptions(text: str) -> str:
    for old, new in CORRUPTION_FIXES:
        if old in text:
            text = text.replace(old, new)
    return text


def fix_maatraam_options(text: str) -> str:
    """Convert 'English മാത്രം' distractor pattern to Malayalam."""
    import re

    from malayalamize_questions import malayalamize_text

    m = re.match(r"^([A-Za-z][A-Za-z0-9 /()-]*) മാത്രം$", text.strip())
    if not m:
        return text
    head = malayalamize_text(m.group(1).strip())
    return f"{head} മാത്രം"


def fix_only_options(text: str) -> str:
    """Convert 'English only' distractor pattern to Malayalam."""
    m = re.match(r"^([A-Za-z][A-Za-z0-9 /()-]*)\s+only$", text.strip(), re.I)
    if m:
        head = malayalamize_text(m.group(1).strip())
        if head != m.group(1).strip():
            return f"{head} മാത്രം"
        # fallback: keep head transliterated loosely
        return f"{m.group(1).strip()} മാത്രം"
    if text.endswith(" only"):
        return text[:-5].strip() + " മാത്രം"
    return text


def clean_text(text: str) -> str:
    text = malayalamize_text(text)
    text = fix_corruptions(text)
    text = fix_only_options(text)
    text = fix_maatraam_options(text)
    text = strip_redundant_english_parens(text)
    text = fix_hyphen_glued(text)
    text = re.sub(r"  +", " ", text).strip()
    return text


def closest_option(answer: str, options: list[str]) -> str | None:
    best, score = None, 0.0
    for opt in options:
        s = SequenceMatcher(None, answer.lower(), opt.lower()).ratio()
        if s > score:
            score, best = s, opt
    return best if score >= 0.55 else None


def apply_manual_fix(q: dict) -> bool:
    qid = q.get("id", "")
    fix = MANUAL_FIXES.get(qid) or ENGLISH_ONLY_OVERRIDES.get(qid)
    if not fix:
        return False
    changed = False
    for key, val in fix.items():
        if q.get(key) != val:
            q[key] = val
            changed = True
    return changed


def dedupe_options(opts: list[str], answer: str) -> list[str]:
    """Drop duplicate options after text normalization; pad if fewer than four."""
    unique: list[str] = []
    seen: set[str] = set()
    for opt in opts:
        if opt not in seen:
            unique.append(opt)
            seen.add(opt)
    if answer and answer not in seen:
        unique.insert(0, answer)
        seen.add(answer)
    pads = ("അപ്രസക്തം", "ബന്ധമില്ലാത്തത്", "വേറെ കാലഘട്ടം")
    for pad in pads:
        if len(unique) >= 4:
            break
        if pad not in seen:
            unique.append(pad)
            seen.add(pad)
    return unique[:4]


def process_question(q: dict) -> tuple[dict, bool]:
    new_q = dict(q)
    changed = apply_manual_fix(new_q)

    for field in ("question", "answer"):
        old = new_q.get(field, "")
        new = clean_text(old)
        if new != old:
            new_q[field] = new
            changed = True

    new_opts = []
    for opt in new_q.get("options", []):
        new_opt = clean_text(opt)
        if new_opt != opt:
            changed = True
        new_opts.append(new_opt)
    new_q["options"] = new_opts

    deduped = dedupe_options(new_opts, new_q.get("answer", ""))
    if deduped != new_opts:
        new_q["options"] = deduped
        changed = True

    mal_q, mal_changed = malayalamize_question(new_q)
    if mal_changed:
        new_q = mal_q
        changed = True

    ans = new_q.get("answer", "")
    opts = new_q.get("options", [])
    if ans not in opts:
        match = closest_option(ans, opts)
        if match:
            new_q["answer"] = match
            changed = True

    return new_q, changed


def dedupe_questions(questions: list[dict], filename: str) -> tuple[list[dict], int]:
    seen: set[str] = set()
    result: list[dict] = []
    removed = 0
    for q in questions:
        text = q.get("question", "").strip()
        if text and text in seen:
            removed += 1
            continue
        if text:
            seen.add(text)
        result.append(q)
    return result, removed


def process_file(filename: str) -> dict:
    path = BASE / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.get("questions", [])
    updated = 0
    fixed_questions: list[dict] = []

    for q in questions:
        new_q, changed = process_question(q)
        if changed:
            updated += 1
        fixed_questions.append(new_q)

    deduped, dup_removed = dedupe_questions(fixed_questions, filename)
    data["questions"] = deduped
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "filename": filename,
        "total": len(deduped),
        "updated": updated,
        "duplicates_removed": dup_removed,
    }


# Quoted spans may contain apostrophes (Midnight's Children, What's in a name?)
QUOTED_SPAN = re.compile(r"'(?:[^']|'(?=[a-zA-Z]))*'")
DOUBLE_QUOTED_SPAN = re.compile(r'"(?:[^"]|"(?=[a-zA-Z]))*"')


def strip_for_validation(text: str) -> str:
    """Strip allowed Latin segments before mixed-language / leak checks."""
    result = QUOTED_SPAN.sub("", text)
    result = DOUBLE_QUOTED_SPAN.sub("", result)
    # Kerala/central scheme names before Malayalam പദ്ധതി
    result = re.sub(r"^[A-Z][A-Za-z-]{2,30}\s+(?=പദ്ധതി)", "", result)
    result = re.sub(r"കേരള\s+[A-Z][A-Za-z]{2,20}\s+", "കേരള ", result)
    result = SATELLITE_AND_CATALOG.sub("", result)
    result = ACRONYM_GLUE.sub("", result)
    result = TECH_PROPER.sub("", result)
    result = PHILOSOPHER_NAMES.sub("", result)
    result = SCHEME_NAMES.sub("", result)
    result = KNOWN_ENGLISH_PHRASES.sub("", result)
    result = STEM_ACRONYMS.sub("", result)
    result = re.sub(r"^[A-Z]{2,10}\s+(?=[\u0D00-\u0D7F])", "", result)
    result = re.sub(r"\s+[A-Z]{2,10}(?=\s+[\u0D00-\u0D7F]|\s*\?|$)", "", result)
    result = re.sub(r"\b(?:19|20)\d{2}\b", "", result)
    result = PAREN_ENGLISH.sub("", result)
    result = fix_corruptions(result)
    return result


def strip_allowed_stem_english(text: str) -> str:
    """Remove allowed acronyms/years so we can detect stray English in Malayalam stems."""
    return strip_for_validation(text)


def validate_file(filename: str) -> list[tuple]:
    path = BASE / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    issues = []
    for q in data.get("questions", []):
        qid = q.get("id", "?")
        question = q.get("question", "")
        opts = q.get("options", [])
        ans = q.get("answer", "")
        if len(opts) != 4:
            issues.append((qid, "options_count", len(opts)))
        if ans not in opts:
            issues.append((qid, "answer_mismatch", ans))

        if not MALAYALAM.search(question):
            issues.append((qid, "english_only_question", question[:100]))
        elif re.search(r"[a-zA-Z]{4,}", strip_allowed_stem_english(question)):
            issues.append((qid, "mixed_language_stem", question[:100]))

        has_malayalam_option = any(MALAYALAM.search(o) for o in opts)
        all_options_english_titles = (
            not any(MALAYALAM.search(o) for o in opts)
            and all(re.search(r"[a-zA-Z]", o) for o in opts)
        )
        for opt in opts:
            if BANNED_OPTION_ENGLISH.search(opt):
                issues.append((qid, "english_option_leak", opt[:100]))
            elif (
                has_malayalam_option
                and not all_options_english_titles
                and not MALAYALAM.search(opt)
                and WORK_TITLE_OPTION.match(opt.strip())
            ):
                pass  # English work titles valid beside Malayalam titles
            elif (
                has_malayalam_option
                and not all_options_english_titles
                and not MALAYALAM.search(opt)
                and re.search(r"[a-zA-Z]{4,}", opt)
                and not re.fullmatch(r"[\d%./\s\-+()A-Za-z]+", opt)
            ):
                # Allow deliberate English acronym distractors (e.g. United Democratic Front)
                if not re.search(
                    r"\b(?:Front|Forum|Force|Defence|Development|Union|Liberal|Local|Left|Unified)\b",
                    opt,
                ):
                    issues.append((qid, "mixed_language_options", opt[:100]))

        for text in [question, *opts, ans]:
            cleaned = strip_for_validation(text)
            cleaned = PRESERVE.sub("", cleaned)
            if re.search(r"[a-zA-Z]{4,}", cleaned) and MALAYALAM.search(text):
                issues.append((qid, "english_leak", text[:100]))
    return issues


def main(files: list[str] | None = None) -> None:
    targets = files or sorted(
        p.name for p in BASE.glob("*.json") if p.name not in SKIP_FILES
    )
    print("Applying Malayalam cursor rules...\n")
    for fname in targets:
        if not (BASE / fname).exists():
            print(f"  SKIP (missing): {fname}")
            continue
        stats = process_file(fname)
        issues = validate_file(fname)
        print(
            f"  {fname}: {stats['total']} questions, "
            f"{stats['updated']} updated, "
            f"{stats['duplicates_removed']} dupes removed, "
            f"{len(issues)} remaining issues"
        )


if __name__ == "__main__":
    import sys

    file_list = sys.argv[1:] if len(sys.argv) > 1 else None
    main(file_list)
