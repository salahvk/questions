#!/usr/bin/env python3
"""Wave 20 biology facts — 20 Malayalam PSC topic categories."""

from __future__ import annotations

import random

from geography_facts import INDIAN_NATIONAL_PARKS
from refill_common import Candidate, add_candidate

Fact = tuple[str, str, list[str], str]

C3_PLANTS = [
    "നെല്ല്", "ഗോതമ്പ്", "ഉലuva", "പയർ", "സോയാബീൻ", "ആപ്പിൾ", "ഓട്", "ബാർലി", "റൈ",
    "പത്താമര", "കാപ്സിക്കം", "ഉരുളക്കിഴങ്ങ്", "തക്കാളി", "വെണ്ട", "പയർവിള", "മല്ലി",
    "ജീരകം", "ഉലർവ", "കാച്ചില", "ചക്ക", "മാവ്", "തേങ്ങ", "വാഴ", "ഏല", "കുരുമുളക്",
    "ഇഞ്ചി", "മഞ്ഞൾ", "കാപ്പി", "ചായ", "പomegranate",
]
C4_PLANTS = [
    "ചോളം", "മുതിര", "ചോളമുല്ല", "പഞ്ചസാര", "മുള", "കരിമ്പ്", "അമaranth", "മillet",
    "നാച്ചURAL ഗ്രാസ്", "വരigated", "സorghum", "മize",
]
CAM_PLANTS = [
    "കള്ളി", "കറ്റാർവാഴ", "അനanas", "ബromeliad", "സedum", "agave", "ഓർchid",
    "പൈneapple", "കactus", "മെസemb",
]

BIOSPHERE_RESERVES: list[tuple[str, str]] = [
    ("നീൽഗിരി", "തമിഴ്നാട്"), ("സുന്ദർബൻസ്", "പശ്ചിമബംഗാൾ"), ("ഗൾഫ് ഓഫ് മന്നാർ", "തമിഴ്നാട്"),
    ("നന്ദാ ദേവി", "ഉത്തരാഖണ്ഡ്"), ("നോക്കെക്", "മേഘാലയ"), ("ദിബ്രു-സൈഖോവ", "അസം"),
    ("പച്ചമര്ഹി", "മധ്യപ്രദേശ്"), ("ഖാങ്ചെൻഡ്സോങ്ഗ", "സിക്കിം"), ("സിംലിപാൽ", "ഒഡിഷ"),
    ("മാനസ്", "അസം"), ("അചനാക്മാർ-അമർകണ്ടák", "മധ്യപ്രദേശ്"), ("ഗ്രേറ്റ് റann ഓഫ് കutch", "ഗുജറാത്ത്"),
    ("കോൾഡ് ഡെസർട്ട്", "ഹിമാചൽ പ്രദേശ്"), ("ശേഷാചലം", "ആന്ധ്രപ്രദേശ്"), ("പന്ന", "മധ്യപ്രദേശ്"),
    ("അഗസ്ത്യമല", "കേരളം"), ("ഗ്രേറ്റർ നികോബാർ", "അണ്ടമാൻ"), ("ദിഹാങ്-ദിപാവു", "അരുണാചൽ പ്രദേശ്"),
    ("പയർ", "മണിപ്പൂർ"), ("നീൽഗിരി ബയോസ്ഫിയർ", "കerala"), ("സുന്ദർബൻസ് റിസർവ്", "പശ്ചിമബംഗാൾ"),
    ("ഗൾഫ് ഓഫ് മന്നാർ റിസർവ്", "തമിഴ്നാട്"), ("നന്ദാ ദേവി ബയോസ്ഫിയർ", "ഉത്തരാഖണ്ഡ്"),
    ("സിമ്ലിപാൽ ബയോസ്ഫിയർ", "ഒഡിഷ"), ("മാനസ് ബയോസ്ഫിയർ", "അസം"), ("അഗസ്ത്യമല ബയോസ്ഫിയർ", "കerala"),
    ("ഖാങ്ചെൻഡ്സോങ്ഗ ബയോസ്ഫിയർ", "സikkim"), ("പച്ചമര്ഹി ബയോസ്ഫിയർ", "മധ്യപ്രദേശ്"),
    ("ദിബ്രു-സൈഖോവ ബയോസ്ഫിയർ", "അസം"), ("നോക്കെക് ബയോസ്ഫിയർ", "മേഘാലയ"),
]

BINOMIAL: list[tuple[str, str]] = [
    ("മനുഷ്യൻ", "Homo sapiens"), ("കടുവ", "Panthera tigris"), ("സിംഹം", "Panthera leo"),
    ("യാനം", "Elephas maximus"), ("നെല്ല്", "Oryza sativa"), ("ഗോതമ്പ്", "Triticum aestivum"),
    ("ചോളം", "Zea mays"), ("മാങ്ങ", "Mangifera indica"), ("താമര", "Nelumbo nucifera"),
    ("വാഴ", "Musa paradisiaca"), ("പശു", "Bos taurus"), ("കുതിര", "Equus caballus"),
    ("നായ", "Canis familiaris"), ("പൂച്ച", "Felis catus"), ("കോഴി", "Gallus gallus"),
    ("തേനീച്ച", "Apis mellifera"), ("യീസ്റ്റ്", "Saccharomyces cerevisiae"),
    ("E.coli", "Escherichia coli"), ("മലേറിയ", "Plasmodium falciparum"),
    ("ക്ഷയരോഗം", "Mycobacterium tuberculosis"), ("പാമ്പ്", "Serpentes"), ("തവള", "Anura"),
    ("ഇലഞ്ഞി", "Azadirachta indica"), ("റബ്ബർ", "Hevea brasiliensis"),
    ("ചായ", "Camellia sinensis"), ("കാപ്പി", "Coffea arabica"), ("പയർ", "Phaseolus vulgaris"),
    ("ഉലuva", "Trigonella foenum-graecum"), ("മഞ്ഞൾ", "Curcuma longa"), ("ഏലം", "Elettaria cardamomum"),
    ("കുരുമുളക്", "Piper nigrum"), ("തെങ്ങ", "Cocos nucifera"), ("പയർവിള", "Vigna radiata"),
    ("ഉരുളക്കിഴങ്ങ്", "Solanum tuberosum"), ("തക്കാളി", "Solanum lycopersicum"),
    ("പയസ", "Lactobacillus"), ("സ്റ്റാഫ്", "Staphylococcus aureus"), ("സ്റ്റ്രെപ്റ്റോ", "Streptococcus"),
    ("ബാക്ടilus", "Bacillus"), ("ക്ലോസ്ട്രിഡിയം", "Clostridium"), ("സാൽമോണella", "Salmonella typhi"),
    ("വിബ്രിയോ", "Vibrio cholerae"), ("HIV", "Human immunodeficiency virus"),
    ("കോവിഡ്", "SARS-CoV-2"), ("പോളിയോ", "Poliovirus"), ("ഡെങ്കു", "Dengue virus"),
    ("റേബീസ്", "Rabies virus"), ("ഹെപ്പറ്റൈറ്റിസ് B", "Hepatitis B virus"),
    ("Homo erectus", "Homo erectus"), ("Homo habilis", "Homo habilis"),
    ("Homo neanderthalensis", "Homo neanderthalensis"), ("Australopithecus", "Australopithecus afarensis"),
    ("കടൽ തട്ടി", "Chelonia"), ("ഡോൾഫിൻ", "Delphinidae"), ("ചിത്ത്", "Acinonyx jubatus"),
    ("മയിൽ", "Pavo cristatus"), ("കാക്ക", "Corvus"), ("തിമിംഗലം", "Cetacea"),
    ("വവ്വാൽ", "Chiroptera"), ("കോബ്ര", "Naja"), ("പ്ലാറ്റിപസ്", "Ornithorhynchus"),
    ("ശതാവരി", "Asparagus racemosus"), ("അശോകം", "Saraca asoca"), ("തulasി", "Ocimum sanctum"),
    ("ബ്രഹ്മി", "Bacopa monnieri"), ("ആമ്പൽ", "Phyllanthus emblica"),
]


def _pool(items: list[str], correct: str) -> list[str]:
    return [x for x in items if x != correct]


def _emit(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    prefix: str,
    facts: list[Fact],
    *,
    function_entity: str | None = None,
) -> None:
    terms = list(dict.fromkeys(t for t, _, _, _ in facts))
    answers = list(dict.fromkeys(a for _, a, _, _ in facts))
    for term, ans, wrong, diff in facts:
        add_candidate(
            out, existing, rng,
            f"{prefix} '{term}'?",
            ans, wrong, diff, pool=answers,
        )
        add_candidate(
            out, existing, rng,
            f"'{ans}' ഏതിനെ സൂചിപ്പിക്കുന്നു?",
            term, _pool(terms, term)[:6], diff, pool=terms,
        )
        if function_entity:
            add_candidate(
                out, existing, rng,
                f"'{ans}' ഏത് {function_entity}-ന്റെ പ്രവർത്തനമാണ്?",
                term, _pool(terms, term)[:6], diff, pool=terms,
            )


def _emit_pairs(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    prefix: str,
    rows: list[tuple[str, str]],
    templates_ab: list[str],
    templates_ba: list[str] | None = None,
    diff: str = "medium",
) -> None:
    bs = list(dict.fromkeys(b for _, b in rows))
    as_ = list(dict.fromkeys(a for a, _ in rows))
    for a, b in rows:
        for tmpl in templates_ab:
            add_candidate(
                out, existing, rng,
                prefix + tmpl.format(a=a, b=b),
                b, _pool(bs, b)[:3], diff, pool=bs,
            )
        if templates_ba:
            for tmpl in templates_ba:
                add_candidate(
                    out, existing, rng,
                    prefix + tmpl.format(a=a, b=b),
                    a, _pool(as_, a)[:3], diff, pool=as_,
                )


def _plant_physiology_facts() -> list[Fact]:
    facts: list[Fact] = []
    for p in C3_PLANTS:
        facts.append((f"{p} — CO₂ ഫിക്സേഷൻ പഥം", "C3 പഥം", ["C4 പഥം", "CAM പഥം", "ഫെറ്മെന്റേഷൻ"], "medium"))
    for p in C4_PLANTS:
        facts.append((f"{p} — CO₂ ഫിക്സേഷൻ പഥം", "C4 പഥം", ["C3 പഥം", "CAM പഥം", "ഗ്ലൈക്കോളിസിസ്"], "medium"))
    for p in CAM_PLANTS:
        facts.append((f"{p} — CO₂ ഫിക്സേഷൻ പഥം", "CAM പഥം", ["C3 പഥം", "C4 പഥം", "ക്രെബ്സ് ചക്രം"], "hard"))
    facts.extend([
        ("പ്രകാശസംശ്ലേഷണത്തിന്റെ ആദ്യ ഘട്ടം", "ലൈറ്റ് റിയാക്ഷൻ", ["ഡാർക്ക് റിയാക്ഷൻ", "ശ്വസനം", "പചനം"], "medium"),
        ("കാൽവിൻ ചക്രം", "ഡാർക്ക് റിയാക്ഷൻ", ["ലൈറ്റ് റിയാക്ഷൻ", "ഗ്ലൈക്കോളിസിസ്", "ക്രെബ്സ് ചക്രം"], "hard"),
        ("സ്റ്റോമാറ്റ", "വാതക കൈമാറ്റം", ["ജലം ശോഷണം", "പ്രകാശസംശ്ലേഷണം", "പോഷക ശോഷണം"], "easy"),
        ("ട്രാൻസ്പിരേഷൻ", "ജലാപവനം", ["CO₂ ഉപയോഗം", "പ്രകാശസംശ്ലേഷണം", "ശ്വസനം"], "easy"),
        ("ക്സൈലം", "ജലവും ധാതുക്കളും കൊണ്ടുപോകൽ", ["പോഷകങ്ങൾ മാത്രം", "പരാഗം", "ശർക്കര"], "medium"),
        ("ഫ്ലോയം", "പോഷകങ്ങൾ കൊണ്ടുപോകൽ", ["ജലം മാത്രം", "ഓക്സിജൻ", "CO₂"], "medium"),
        ("റുബിസ്കോ", "CO₂ ഫിക്സേഷൻ", ["ജലം ഫിക്സേഷൻ", "നൈട്രജൻ ഫിക്സേഷൻ", "ഓക്സിജൻ ഫിക്സേഷൻ"], "hard"),
        ("ക്ലോറോഫിൽ", "പ്രകാശ ഊർജം കൈമാറ്റം", ["CO₂ ഉപയോഗം", "ജലം ഉപയോഗം", "ശ്വസനം"], "easy"),
        ("ഹാച്ച്-സ്ലാക്ക് പഥം", "C4 സസ്യങ്ങളിൽ", ["C3 സസ്യങ്ങളിൽ", "CAM സസ്യങ്ങളിൽ", "ഫംഗിയിൽ"], "hard"),
        ("ദീർഘദിന സസ്യം", "തക്കാളി", ["വാഴ", "ചോളം", "നെല്ല്"], "medium"),
        ("ചെറുദിന സസ്യം", "വാഴ", ["തക്കാളി", "ചോളം", "ഗോതമ്പ്"], "medium"),
        ("നിഷ്പക്ഷദിന സസ്യം", "നെല്ല്", ["വാഴ", "തക്കാളി", "ചോളം"], "hard"),
        ("നൈട്രജൻ സ്ഥിരീകരണം", "റൈസോബിയം", ["യീസ്റ്റ്", "പ്ലാസ്മോഡിയം", "അസpergillus"], "medium"),
        ("ഹലോഫൈറ്റ്", "മണ്ണുചെടി", ["നെല്ല്", "താമര", "മാവ്"], "hard"),
        ("ക്സെറോഫൈറ്റ്", "കള്ളി", ["നെല്ല്", "താമര", "വാഴ"], "medium"),
        ("ഹൈഡ്രോഫൈറ്റ്", "താമര", ["കള്ളി", "ചോളം", "ഗോതമ്പ്"], "medium"),
        ("ജല പരാഗണം", "താമര", ["വാഴ", "ചോളം", "നെല്ല്"], "medium"),
        ("തേനീച്ച പരാഗണം", "പരപരാഗണം", ["സ്വയംപരാഗണം", "വിഭജനം", "ബൈനറി ഫിഷൻ"], "easy"),
        ("സ്വയംപരാഗണം", "ഒരേ പുഷ്പത്തിൽ", ["വ്യത്യസ്ത സസ്യത്തിൽ", "കാറ്റിൽ", "ജലത്തിലൂടെ"], "medium"),
        ("പരപരാഗണം", "വ്യത്യസ്ത സസ്യത്തിൽ", ["ഒരേ പുഷ്പത്തിൽ", "ഒരേ തണ്ടിൽ മാത്രം", "മണ്ണിലൂടെ"], "easy"),
        ("വേരിന്റെ പ്രധാന പ്രവർത്തനം", "ജലവും ധാതുക്കളും ശോഷണം", ["പ്രകാശസംശ്ലേഷണം", "പരാഗണം", "വിത്ത് ഉൽപ്പാദനം"], "easy"),
        ("ഇലയുടെ പ്രധാന പ്രവർത്തനം", "പ്രകാശസംശ്ലേഷണം", ["വിത്ത് ഉൽപ്പാദനം", "ജലം സംഭരണം", "പരാഗണം"], "easy"),
        ("ഫോട്ടോപീരിയഡിസം", "പ്രകാശ ദൈർഘ്യം പ്രതികരണം", ["താപനില പ്രതികരണം", "ജലം പ്രതികരണം", "CO₂ പ്രതികരണം"], "hard"),
        ("ഓപൻ സ്റ്റോമാറ്റ", "വേഗമുള്ള ട്രാൻസ്പിരേഷൻ", ["കുറഞ്ഞ ട്രാൻസ്പിരേഷൻ", "അവസാനിപ്പിച്ച ട്രാൻസ്പിരേഷൻ", "ശ്വസനം"], "medium"),
        ("സംവൃത സ്റ്റോമാറ്റ", "കുറഞ്ഞ ജലനഷ്ടം", ["ഉയർന്ന ജലനഷ്ടം", "അധിക പരാഗണം", "അധിക ശ്വസനം"], "medium"),
        ("കായ്കാലിക വേര്", "വാഴ", ["നെല്ല്", "ചോളം", "തക്കാളി"], "medium"),
        ("ഫിബ്രസ് വേര്", "മാവ്", ["വാഴ", "നെല്ല്", "തക്കാളി"], "medium"),
        ("വായുവായ വേര്", "പയർ", ["നെല്ല്", "ചോളം", "ഗോതമ്പ്"], "medium"),
        ("പരാഗം", "പുരുഷ ഗാമറ്റ് (സസ്യം)", ["സ്ത്രീ ഗാമറ്റ്", "സിഗോട്ട്", "എംബ്രിയോ"], "medium"),
        ("അണ്ഡകോശം", "സ്ത്രീ ഗാമറ്റ് (സസ്യം)", ["പുരുഷ ഗാമറ്റ്", "പരാഗം", "വിത്ത്"], "medium"),
        ("ഫോട്ടോറെസ്പിരേഷൻ", "ഓക്സിജൻ ഉപയോഗിച്ച് CO₂ ഉൽപ്പാദനം", ["CO₂ ഉപയോഗിച്ച് O₂", "ജലം ഉൽപ്പാദനം", "ഗ്ലൂക്കോസ് ഉൽപ്പാദനം"], "hard"),
        ("ബണ്ടിൽ ഷീത്ത് സെൽ", "C4 സസ്യത്തിൽ CO₂ സ്ഥിരീകരണം", ["C3 സസ്യത്തിൽ", "CAM സസ്യത്തിൽ", "ഫംഗിയിൽ"], "hard"),
        ("CO₂ സ്ഥിരീകരണം C4-ൽ ആദ്യം", "മാലിക് ആസിഡ്", ["റുബിസ്കോ", "ഗ്ലൂക്കോസ്", "ഓക്സിജൻ"], "hard"),
        ("ലെഗ്ഹീമോഗ്ലോബിൻ", "പയർവിളകളിൽ", ["നെല്ലിൽ", "ഗോതമ്പിൽ", "ചോളത്തിൽ"], "hard"),
        ("എപ്പിഫൈറ്റ്", "ഇലഞ്ഞി", ["നെല്ല്", "ചോളം", "ഗോതമ്പ്"], "hard"),
        ("ലാറ്റിക്സ് സസ്യം", "റബ്ബർ", ["നെല്ല്", "ചോളം", "തക്കാളി"], "medium"),
    ])
    return facts


def _phytohormone_facts() -> list[Fact]:
    return [
        ("ഓക്സിൻ", "കോശ നീളം വർദ്ധന", ["ഇല വീഴ്ച", "പുഷ്പം വീഴ്ച", "വിത്ത് അങ്കുരണം"], "medium"),
        ("ജിബറെല്ലിൻ", "തണ്ട് നീളം വർദ്ധന", ["ഇല വീഴ്ച", "വേര് വ്യാപനം", "പരാഗണം"], "medium"),
        ("സൈറ്റോകിനിൻ", "കോശ വിഭജനം", ["ഇല വീഴ്ച", "വിത്ത് അങ്കുരണം തടയൽ", "വേര് വ്യാപനം"], "hard"),
        ("എബ്സിസിക് ആസിഡ്", "ഇല വീഴ്ച", ["കോശ നീളം", "പുഷ്പം വികാസം", "വിത്ത് അങ്കുരണം"], "hard"),
        ("എതിലീൻ", "ഫല പക്വതന", ["വിത്ത് അങ്കുരണം", "വേര് വ്യാപനം", "പരാഗണം"], "medium"),
        ("ഓക്സിൻ", "അപൈക്കൽ പ്രഭാവം", ["ബസൽ പ്രഭാവം", "പരാഗണം", "ശ്വസനം"], "hard"),
        ("ഓക്സിൻ", "വേര് രൂപീകരണം", ["ഇല വീഴ്ച", "പുഷ്പം വീഴ്ച", "വിത്ത് വിതറൽ"], "medium"),
        ("ജിബറെല്ലിൻ", "വിത്ത് അങ്കുരണം", ["ഇല വീഴ്ച", "പുഷ്പം വീഴ്ച", "വേര് വ്യാപനം തടയൽ"], "medium"),
        ("ട്രൈപ്റ്റോഫാൻ ഉത്പന്നം", "ഓക്സിൻ", ["ജിബറെല്ലിൻ", "സൈറ്റോകിനിൻ", "എതിലീൻ"], "hard"),
        ("മെത്തിയോനിൻ ഉത്പന്നം", "എതിലീൻ", ["ഓക്സിൻ", "ജിബറെല്ലിൻ", "സൈറ്റോകിനിൻ"], "hard"),
        ("ആഡെനിൻ ഉത്പന്നം", "സൈറ്റോകിനിൻ", ["ഓക്സിൻ", "ജിബറെല്ലിൻ", "എതിലീൻ"], "hard"),
        ("ഓക്സിൻ പ്രയോഗം", "റൂട്ടിംഗ്", ["ഡിഫോളിയേഷൻ", "പരാഗണം", "വിത്ത് വിതറൽ"], "medium"),
        ("ജിബറെല്ലിൻ പ്രയോഗം", "തണ്ട് നീളം", ["ഇല വീഴ്ച", "വേര് വ്യാപനം", "പരാഗണം"], "medium"),
        ("എബ്സിസിക് ആസിഡ് പ്രയോഗം", "ഇല വീഴ്ച", ["വിത്ത് അങ്കുരണം", "പുഷ്പം വികാസം", "പരാഗണം"], "hard"),
        ("എതിലീൻ പ്രയോഗം", "ഫല പക്വതന", ["വിത്ത് അങ്കുരണം", "വേര് വ്യാപനം", "പരാഗണം"], "medium"),
        ("ഓക്സിൻ", "ഫോട്ടോട്രോപിസം", ["ഗ്രാവിട്രോപിസം", "തിക്ടിനോസ്ട്രോപിസം", "ഹൈഡ്രോട്രോപിസം"], "hard"),
        ("എബ്സിസിക് ആസിഡ്", "സ്റ്റോമാറ്റ അവസാനിപ്പിക്കൽ", ["സ്റ്റോമാറ്റ തുറക്കൽ", "പരാഗണം", "വിത്ത് വിതറൽ"], "hard"),
        ("എതിലീൻ", "സ്റ്റോമാറ്റ തുറക്കൽ", ["സ്റ്റോമാറ്റ അവസാനിപ്പിക്കൽ", "വിത്ത് അങ്കുരണം", "പരാഗണം"], "hard"),
        ("ജിബറെല്ലിൻ", "പുഷ്പം വികാസം", ["ഇല വീഴ്ച", "വിത്ത് അങ്കുരണം തടയൽ", "പരാഗണം"], "medium"),
        ("ഓക്സിൻ", "കല്ലസ് രൂപീകരണം", ["ഇല വീഴ്ച", "പരാഗണം", "വിത്ത് വിതറൽ"], "hard"),
        ("എബ്സിസിക് ആസിഡ്", "ഡോർമൻസി", ["വിത്ത് അങ്കുരണം", "പുഷ്പം വികാസം", "പരാഗണം"], "hard"),
        ("സൈറ്റോകിനിൻ", "ഷൂട്ട് അക്സിസ് രൂപീകരണം", ["ഇല വീഴ്ച", "വിത്ത് അങ്കുരണം", "പരാഗണം"], "hard"),
        ("ജിബറെല്ലിൻ", "ബോൾട്ടിംഗ്", ["ഇല വീഴ്ച", "വിത്ത് അങ്കുരണം", "പരാഗണം"], "hard"),
        ("എതിലീൻ", "ഇല വീഴ്ച", ["വിത്ത് അങ്കുരണം", "വേര് വ്യാപനം", "പരാഗണം"], "medium"),
        ("ഓക്സിൻ", "പാർത്തെനോകാർപ്പി", ["പരാഗണം", "വിത്ത് വിതറൽ", "ശ്വസനം"], "hard"),
        ("ജിബറെല്ലിൻ", "അല്ഫ-അമൈലേസ് ഉത്പാദനം", ["ക്ലോറോഫിൽ ഉത്പാദനം", "പരാഗണം", "വിത്ത് വിതറൽ"], "hard"),
        ("എതിലീൻ", "ട്രിപ്പിംഗ് ഫലം", ["വിത്ത് അങ്കുരണം", "വേര് വ്യാപനം", "പരാഗണം"], "hard"),
        ("എബ്സിസിക് ആസിഡ്", "വിത്ത് അങ്കുരണം തടയൽ", ["വിത്ത് അങ്കുരണം ഉത്തേജനം", "പുഷ്പം വികാസം", "പരാഗണം"], "hard"),
        ("സൈറ്റോകിനിൻ", "ഇല വീഴ്ച തടയൽ", ["ഇല വീഴ്ച ഉത്തേജനം", "വിത്ത് അങ്കുരണം തടയൽ", "പരാഗണം"], "hard"),
        ("ഓക്സിൻ", "ഗ്രാവിട്രോപിസം", ["ഫോട്ടോട്രോപിസം", "തിക്ടിനോസ്ട്രോപിസം", "കെമോട്രോപിസം"], "hard"),
    ]


def _respiration_facts() -> list[Fact]:
    facts = [
        ("ഗ്ലൈക്കോളിസിസ് സ്ഥലം", "സൈറ്റോസോൾ", ["മൈറ്റോകോൺഡ്രിയ", "ക്ലോറോപ്ലാസ്റ്റ്", "ന്യൂക്ലിയസ്"], "medium"),
        ("ക്രെബ്സ് ചക്രം സ്ഥലം", "മൈറ്റോകോൺഡ്രിയ", ["സൈറ്റോസോൾ", "ക്ലോറോപ്ലാസ്റ്റ്", "ഗോൾജി"], "medium"),
        ("ഇലക്ട്രോൺ ട്രാൻസ്പോർട്ട് ചെയിൻ", "മൈറ്റോകോൺഡ്രിയ", ["സൈറ്റോസോൾ", "ന്യൂക്ലിയസ്", "റൈബോസോം"], "hard"),
        ("ആക്സിഡിക് ശ്വസനം", "ഗ്ലൈക്കോളിസിസ്", ["ക്രെബ്സ് ചക്രം", "ഫെറ്മെന്റേഷൻ", "പ്രകാശസംശ്ലേഷണം"], "medium"),
        ("ആനറോബിക് ശ്വസനം", "ഫെറ്മെന്റേഷൻ", ["ക്രെബ്സ് ചക്രം", "പ്രകാശസംശ്ലേഷണം", "ഗ്ലൈക്കോളിസിസ് മാത്രം"], "medium"),
        ("യീസ്റ്റ് ഫെറ്മെന്റേഷൻ ഉൽപ്പന്നം", "എത്തനോൾ", ["ലാക്ടിക് ആസിഡ്", "ഓക്സിജൻ", "ഗ്ലൂക്കോസ്"], "medium"),
        ("പേശി ഫെറ്മെന്റേഷൻ ഉൽപ്പന്നം", "ലാക്ടിക് ആസിഡ്", ["എത്തനോൾ", "ഓക്സിജൻ", "CO₂"], "medium"),
        ("ശ്വസനത്തിന്റെ അന്തിമ ഇലക്ട്രോൺ സ്വീകർത്താവ്", "ഓക്സിജൻ", ["നൈട്രജൻ", "CO₂", "ഹൈഡ്രജൻ"], "medium"),
        ("ഗ്ലൈക്കോളിസിസ് ഉൽപ്പന്നം", "പൈരുവേറ്റ്", ["ഗ്ലൂക്കോസ്", "CO₂", "ഓക്സിജൻ"], "hard"),
        ("ആക്സിഡിക് ശ്വസന ATP ഉൽപ്പാദനം", "38 ATP", ["2 ATP", "4 ATP", "76 ATP"], "hard"),
        ("ആനറോബിക് ഗ്ലൈക്കോളിസിസ് ATP", "2 ATP", ["38 ATP", "36 ATP", "4 ATP"], "medium"),
        ("ശ്വസനത്തിന്റെ ആദ്യ ഘട്ടം", "ഗ്ലൈക്കോളിസിസ്", ["ക്രെബ്സ് ചക്രം", "ETC", "ഫെറ്മെന്റേഷൻ"], "easy"),
        ("ശ്വസനത്തിന്റെ അവസാന ഘട്ടം", "ഇലക്ട്രോൺ ട്രാൻസ്പോർട്ട്", ["ഗ്ലൈക്കോളിസിസ്", "ഫെറ്മെന്റേഷൻ", "പ്രകാശസംശ്ലേഷണം"], "medium"),
        ("ക്രെബ്സ് ചക്രം മറ്റു പേര്", "ട്രൈകാർബോക്സിലിക് ആസിഡ് ചക്രം", ["ഗ്ലൈക്കോളിസിസ്", "കാൽവിൻ ചക്രം", "ഫെറ്മെന്റേഷൻ"], "hard"),
        ("ATP സിന്തേസ്", "ഇലക്ട്രോൺ ട്രാൻസ്പോർട്ട്", ["ഗ്ലൈക്കോളിസിസ്", "ഫെറ്മെന്റേഷൻ", "പ്രകാശസംശ്ലേഷണം"], "hard"),
        ("ശ്വസനത്തിന്റെ CO₂ ഉത്പന്നം", "ക്രെബ്സ് ചക്രം", ["ഗ്ലൈക്കോളിസിസ്", "ETC", "ഫെറ്മെന്റേഷൻ"], "hard"),
        ("RQ കാർബോഹൈഡ്രേറ്റ്", "1.0", ["0.7", "0.8", "1.2"], "hard"),
        ("RQ കൊഴുപ്പ്", "0.7", ["1.0", "0.8", "1.2"], "hard"),
        ("RQ പ്രോട്ടീൻ", "0.8", ["1.0", "0.7", "1.2"], "hard"),
        ("ആനറോബിക് ശ്വസനം മനുഷ്യനിൽ", "പേശി", ["ഫെഫുസ്സ്", "കരൾ", "മസ്തിഷ്കം"], "medium"),
        ("ആക്സിഡിക് ശ്വസനം ആവശ്യം", "ഓക്സിജൻ", ["നൈട്രജൻ", "CO₂", "ഹൈഡ്രജൻ"], "easy"),
        ("ഫെറ്മെന്റേഷൻ ആവശ്യം", "ഓക്സിജൻ ഇല്ല", ["ഓക്സിജൻ അത്യാവശ്യം", "CO₂ അത്യാവശ്യം", "നൈട്രജൻ അത്യാവശ്യം"], "easy"),
        ("സൈറ്റോക്രോം c", "ഇലക്ട്രോൺ ട്രാൻസ്പോർട്ട്", ["ഗ്ലൈക്കോളിസിസ്", "ക്രെബ്സ് ചക്രം", "ഫെറ്മെന്റേഷൻ"], "hard"),
        ("ഓക്സിഡേറ്റീവ് ഫോസ്ഫറിലേഷൻ", "3 എടിപി", ["2 എടിപി", "1 എടിപി", "4 എടിപി"], "hard"),
        ("FADH₂ ATP ഉൽപ്പാദനം", "2 ATP", ["3 ATP", "1 ATP", "4 ATP"], "hard"),
        ("പൈരുവേറ്റ് ഡിഹൈഡ്രജനേസ്", "ഗ്ലൈക്കോളിസിസ്", ["ക്രെബ്സ് ചക്രം", "ETC", "ഫെറ്മെന്റേഷൻ"], "hard"),
        ("ഓക്സിഡേറ്റീവ് ഫോസ്ഫൊറിലേഷൻ", "ഇലക്ട്രോൺ ട്രാൻസ്പോർട്ട്", ["ഗ്ലൈക്കോളിസിസ്", "ക്രെബ്സ് ചക്രം", "ഫെറ്മെന്റേഷൻ"], "hard"),
        ("സബ്സ്ട്രേറ്റ് ലെവൽ ഫോസ്ഫൊറിലേഷൻ", "ഗ്ലൈക്കോളിസിസ്", ["ETC", "ക്രെബ്സ് ചക്രം", "ഫെറ്മെന്റേഷൻ"], "hard"),
    ]
    for carb in ["ഗ്ലൂക്കോസ്", "സ്റ്റാർച്ച്", "സുക്രോസ്", "നെല്ല്", "ഗോതമ്പ്", "ചോളം"]:
        facts.append((f"RQ ({carb})", "1.0", ["0.7", "0.8", "1.2"], "hard"))
    for fat in ["കൊഴുപ്പ്", "പാമായിൽ", "വെണ്ണ", "എണ്ണ", "നെയ്യ്"]:
        facts.append((f"RQ ({fat})", "0.7", ["1.0", "0.8", "1.2"], "hard"))
    krebs = ["സിട്രേറ്റ്", "ഐസോസിട്രേറ്റ്", "ആൽഫ-കീറ്റോഗ്ലൂട്ടറേറ്റ്", "സക്സിനേറ്റ്", "ഫ്യൂമറേറ്റ്", "മാലേറ്റ്", "ഓക്സലോഅസിറ്റേറ്റ്"]
    for i, comp in enumerate(krebs):
        nxt = krebs[(i + 1) % len(krebs)]
        facts.append((f"ക്രെബ്സ് ചക്രം — {comp} അടുത്തം", nxt, [krebs[(i + 2) % len(krebs)], krebs[(i + 3) % len(krebs)], "ഗ്ലൂക്കോസ്"], "hard"))
    return facts

def _nervous_facts() -> list[Fact]:
    return [
        ("നാഡീ കോശം", "ന്യൂറോൺ", ["ഗ്ലിയൽ കോശം", "മസ്തിഷ്ക കോശം", "പേശി കോശം"], "easy"),
        ("ന്യൂറോൺ — ദീർഘ ശാഖ", "ആക്സോൺ", ["ഡെൻഡ്രൈറ്റ്", "സിനാപ്സ്", "മയലിൻ"], "medium"),
        ("ന്യൂറോൺ — ചെറു ശാഖ", "ഡെൻഡ്രൈറ്റ്", ["ആക്സോൺ", "സിനാപ്സ്", "മയലിൻ"], "medium"),
        ("നാഡീ സിഗ്നൽ കൈമാറ്റം", "സിനാപ്സ്", ["ആക്സോൺ", "ഡെൻഡ്രൈറ്റ്", "മയലിൻ"], "easy"),
        ("മയലിൻ", "നാഡീ ആവേഗം വേഗത്തിലാക്കൽ", ["സിനാപ്സ്", "ഡെൻഡ്രൈറ്റ്", "ഗ്ലിയൽ"], "hard"),
        ("റിഫ്ലക്സ് ആർക്ക് — സംവേദനം", "റിസപ്റ്റർ", ["ഇന്റർന്യൂൺ", "മോട്ടർ ന്യൂറോൺ", "സിനാപ്സ്"], "medium"),
        ("റിഫ്ലക്സ് ആർക്ക് — പ്രോസസ്സിംഗ്", "സ്പൈനൽ കോർഡ്", ["മസ്തിഷ്കം", "ചെറുമുതൽ", "ഹൃദയം"], "medium"),
        ("റിഫ്ലക്സ് ആർക്ക് — പ്രതികരണം", "ഇഫക്ടർ", ["റിസപ്റ്റർ", "സിനാപ്സ്", "ഡെൻഡ്രൈറ്റ്"], "medium"),
        ("കണ്ണടിപ്പ് റിഫ്ലക്സ്", "കണ്ണടിപ്പ്", ["കണ്ണുനീർ", "കോർണിയ", "ററ്റിന"], "easy"),
        ("സെറിബ്രം", "ചിന്തയും യാഥാർത്ഥ്യബോധവും", ["ശ്വാസനം", "ഹൃദയം നിയന്ത്രണം", "പചനം"], "easy"),
        ("സെറെബെല്ലം", "സമതുലനവും ഏകാഗ്രതയും", ["ചിന്ത", "ശ്വാസനം", "പചനം"], "medium"),
        ("മെഡുല്ല ഒബ്ലോങ്ഗാറ്റ", "ശ്വാസനവും ഹൃദയവും നിയന്ത്രണം", ["ചിന്ത", "സമതുലനം", "ദൃഷ്ടി"], "hard"),
        ("ഹൈപ്പോത്തലാമസ്", "ഹോർമോൺ നിയന്ത്രണ കേന്ദ്രം", ["ചിന്ത", "സമതുലനം", "പചനം"], "hard"),
        ("പിറ്റ്യൂട്ടറി", "മാസ്റ്റർ ഗ്രന്ഥി", ["തൈറോയ്ഡ്", "അഡ്രീനൽ", "പാൻക്രിയാസ്"], "medium"),
        ("സ്പൈനൽ കോർഡ്", "റിഫ്ലക്സ് നിയന്ത്രണം", ["ചിന്ത", "സമതുലനം", "ദൃഷ്ടി"], "medium"),
        ("ഓട്ടോനോമിക് നാഡീവ്യൂഹം", "അനൈച്ഛിക അവയവ നിയന്ത്രണം", ["ഇച്ഛാധീന പേശി", "അസ്ഥി", "ത്വക്ക്"], "hard"),
        ("സിമ്പതറ്റിക്", "പോരാട്ടം-ഓർ-പലായനം", ["വിശ്രമം-അമർ്ക്കം", "പചനം", "ശ്വസനം"], "hard"),
        ("പാരാസിമ്പതറ്റിക്", "വിശ്രമം-അമർ്ക്കം", ["പോരാട്ടം-ഓർ-പലായനം", "പചനം", "ശ്വസനം"], "hard"),
        ("അസെറ്റൈൽകോലിൻ", "നാഡീ സംകേതകം", ["അഡ്രിനലിൻ", "ഇൻസുലിൻ", "തൈറോക്സിൻ"], "hard"),
        ("ഡോപമിൻ", "സന്തോഷ ഹോർമോൺ", ["അഡ്രിനലിൻ", "ഇൻസുലിൻ", "തൈറോക്സിൻ"], "hard"),
        ("പാർക്കിൻസൺ", "ഡോപമിൻ കുറവ്", ["ഇൻസുലിൻ കുറവ്", "തൈറോക്സിൻ കുറവ്", "അഡ്രിനലിൻ കുറവ്"], "hard"),
        ("അൽഷൈമേഴ്സ്", "ഓർമ്മ നഷ്ടം", ["ദൃഷ്ടി നഷ്ടം", "ശ്രവണം നഷ്ടം", "ചലന നഷ്ടം"], "medium"),
        ("സ്റ്റെപ്പ് റിഫ്ലക്സ്", "കണങ്കാൽ റിഫ്ലക്സ്", ["കണ്ണടിപ്പ്", "കണ്ണു", "ചെവി"], "hard"),
        ("കണ്ടീഷൻഡ് റിഫ്ലക്സ്", "പാവലോവ് പരീക്ഷണം", ["കണ്ണടിപ്പ്", "കണ്ണു", "ചെവി"], "hard"),
        ("മോട്ടർ ന്യൂറോൺ", "പ്രതികരണം നിർവഹിക്കുന്നു", ["റിസപ്റ്റർ", "സെൻസറി", "ഗ്ലിയൽ"], "medium"),
        ("സെൻസറി ന്യൂറോൺ", "സംവേദനം നിർവഹിക്കുന്നു", ["മോട്ടർ", "ഇന്റർന്യൂൺ", "ഗ്ലിയൽ"], "medium"),
        ("ക്രാനിയൽ നാഡി എണ്ണം", "12", ["10", "14", "8"], "hard"),
        ("ഓപ്റ്റിക് നാഡി", "ദൃഷ്ടി", ["ശ്രവണം", "ഘ്രാണം", "രുചി"], "medium"),
        ("വേഗസ് നാഡി", "ഹൃദയവും പചനവും", ["ദൃഷ്ടി", "ശ്രവണം", "ചലനം"], "hard"),
        ("സൈയാട്ടിക് നാഡി", "കാൽ നാഡി", ["കൈ നാഡി", "കണ്ണ് നാഡി", "ചെവി നാഡി"], "hard"),
        ("ആക്ഷൻ പൊട്ടൻഷ്യൽ", "നാഡീ ആവേഗം", ["സിനാപ്സ്", "ഡെൻഡ്രൈറ്റ്", "മയലിൻ"], "hard"),
        ("റെസ്റ്റിംഗ് പൊട്ടൻഷ്യൽ", "-70 mV", ["-50 mV", "+30 mV", "0 mV"], "hard"),
        ("സെറിബ്രോസ്പൈനൽ ദ്രാവകം", "മസ്തിഷ്ക-മുതൽ സംരക്ഷണം", ["രക്തം", "ലിംഫ്", "പ്ലാസ്മ"], "hard"),
        ("ഇന്റർന്യൂൺ", "കണക്ടിംഗ് ന്യൂറോൺ", ["റിസപ്റ്റർ", "ഇഫക്ടർ", "ഗ്ലിയൽ"], "hard"),
        ("ഗ്ലിയൽ കോശം", "ന്യൂറോൺ പിന്തുണ", ["പേശി കോശം", "രക്ത കോശം", "അസ്ഥി കോശം"], "medium"),
    ]


def _cardiac_facts() -> list[Fact]:
    phases = [
        ("ഹൃദയ ചക്രം — ആദ്യ ഘട്ടം", "അatriale systole", ["ventricular systole", "diastole", "isovolumetric"], "hard"),
        ("ഹൃദയ ചക്രം — ventricular systole", "ventricular systole", ["atrial systole", "diastole", "isovolumetric contraction"], "hard"),
        ("ഹൃദയ ചക്രം — വിശ്രമം", "diastole", ["systole", "contraction", "ejection"], "medium"),
        ("SA node", "pacemaker", ["AV node", "Purkinje", "Bundle of His"], "medium"),
        ("AV node", "delay conduction", ["SA node", "Purkinje", "Bundle of His"], "hard"),
        ("Bundle of His", "ventricles conduct", ["SA node", "AV node", "atria only"], "hard"),
    ]
    facts = [
        ("ഹൃദയത്തിലെ pacemaker", "SA node", ["AV node", "Purkinje fibres", "Bundle of His"], "medium"),
        ("ഹൃദയത്തിലെ AV node", "delay conduction", ["pacemaker", "Purkinje only", "atria only"], "hard"),
        ("ഹൃദയത്തിലെ Bundle of His", "ventricles-ilēkku conduction", ["SA node", "AV node", "atria only"], "hard"),
        ("ഹൃദയത്തിലെ Purkinje fibres", "ventricular contraction spread", ["SA node", "AV node", "atria only"], "hard"),
        ("ഹൃദയത്തിലെ bicuspid valve", "left AV valve", ["tricuspid", "aortic", "pulmonary"], "medium"),
        ("ഹൃദയത്തിലെ tricuspid valve", "right AV valve", ["bicuspid", "aortic", "pulmonary"], "medium"),
        ("ഹൃദയത്തിലെ aortic valve", "left ventricle to aorta", ["pulmonary", "tricuspid", "bicuspid"], "medium"),
        ("ഹൃദയത്തിലെ pulmonary valve", "right ventricle to pulmonary artery", ["aortic", "tricuspid", "bicuspid"], "medium"),
        ("ഹൃദയത്തിലെ left ventricle", "systemic circulation pump", ["right ventricle", "right atrium", "left atrium"], "medium"),
        ("ഹൃദയത്തിലെ right ventricle", "pulmonary circulation pump", ["left ventricle", "left atrium", "right atrium"], "medium"),
        ("ഹൃദയത്തിലെ coronary circulation", "heart muscle blood supply", ["pulmonary", "systemic", "hepatic portal"], "hard"),
        ("ഹൃദയത്തിലെ cardiac output", "stroke volume × heart rate", ["blood pressure only", "respiratory rate", "venous return only"], "hard"),
        ("ഹൃദയത്തിലെ systole", "contraction phase", ["relaxation", "diastole", "isovolumetric relaxation"], "easy"),
        ("ഹൃദയത്തിലെ diastole", "relaxation phase", ["contraction", "systole", "ejection"], "easy"),
        ("ഹൃദയത്തിലെ lub sound", "AV valves close", ["semilunar close", "ventricular open", "atrial close"], "medium"),
        ("ഹൃദയത്തിലെ dub sound", "semilunar valves close", ["AV close", "atrial open", "ventricular open"], "medium"),
        ("ഹൃദയത്തിലെ normal heart rate", "72/min", ["120/min", "40/min", "100/min"], "easy"),
        ("ഹൃദയത്തിലെ ECG P wave", "atrial depolarization", ["ventricular depolarization", "repolarization", "SA block"], "hard"),
        ("ഹൃദയത്തിലെ ECG QRS complex", "ventricular depolarization", ["atrial depolarization", "atrial repolarization", "T wave"], "hard"),
        ("ഹൃദയത്തിലെ ECG T wave", "ventricular repolarization", ["atrial depolarization", "QRS", "P wave"], "hard"),
        ("ഹൃദയത്തിലെ angina", "reduced coronary blood flow", ["valve defect", "arrhythmia only", "hypertension only"], "hard"),
        ("ഹൃദയത്തിലെ myocardial infarction", "heart muscle damage", ["valve stenosis", "arrhythmia only", "anemia only"], "hard"),
        ("ഹൃദയത്തിലെ hypertension effect", "increased afterload", ["decreased stroke volume always", "bradycardia always", "hypotension"], "hard"),
        ("ഹൃദയത്തിലെ stroke volume", "blood pumped per beat", ["heart rate", "cardiac output only", "blood pressure"], "medium"),
        ("ഹൃദയത്തിലെ heart rate", "beats per minute", ["stroke volume", "cardiac output only", "blood pressure"], "easy"),
        ("ഹൃദയത്തിലെ pericardium", "heart covering membrane", ["endocardium", "myocardium", "epicardium only"], "hard"),
        ("ഹൃദയത്തിലെ myocardium", "cardiac muscle layer", ["pericardium", "endocardium only", "epicardium only"], "medium"),
        ("ഹൃദയത്തിലെ endocardium", "inner heart lining", ["pericardium", "myocardium only", "epicardium only"], "hard"),
        ("ഹൃദയത്തിലെ semilunar valves", "aortic and pulmonary", ["AV valves", "tricuspid only", "bicuspid only"], "medium"),
        ("ഹൃദയത്തിലെ AV valves", "tricuspid and bicuspid", ["semilunar valves", "aortic only", "pulmonary only"], "medium"),
    ]
    for term, ans, wrong, diff in phases:
        facts.append((term, ans, wrong, diff))
    return facts


def _excretory_facts() -> list[Fact]:
    nephron = ["ഗ്ലോമെറുലസ്", "ബോwmans capsule", "പ്രോക്സിമൽ tubule", "ലൂപ്പ് ഓഫ് Henle", "distal tubule", "collecting duct"]
    facts = [
        ("നെഫ്രോൺ", "മൂത്രം ഉൽപ്പാദനത്തിന്റെ അടിസ്ഥാന ഘടകം", ["ശ്വസനം", "പചനം", "പ്രകാശസംശ്ലേഷണം"], "hard"),
        ("ഗ്ലോമെറുലസ്", "രക്തം фильтр ചെയ്യൽ", ["reabsorption", "secretion", "digestion"], "hard"),
        ("ബോwmans capsule", "filtrate collection", ["reabsorption site", "secretion site", "ureter"], "hard"),
        ("പ്രോക്സിമൽ tubule", "glucose reabsorption", ["filtration", "secretion only", "ureter"], "hard"),
        ("ലൂപ്പ് ഓഫ് Henle", "water reabsorption concentrate urine", ["filtration", "glucose reabsorption", "ureter"], "hard"),
        ("distal tubule", "fine tuning reabsorption secretion", ["filtration only", "Bowmans only", "ureter"], "hard"),
        ("collecting duct", "final urine concentration", ["filtration", "Bowmans only", "glomerulus"], "hard"),
        ("മൂത്രപിണ്ഡം", "മൂത്രം ഉൽപ്പാദനം", ["ഇൻസുലിൻ", "പിത്തം", "ശ്വസനം"], "easy"),
        ("മൂത്രാശയം", "മൂത്രം സംഭരണം", ["രക്തം", "പചനം", "ശ്വസനം"], "easy"),
        ("യൂറിഥ്ര", "മൂത്രം പുറത്ത്", ["വായു", "ഭക്ഷണം", "രക്തം"], "medium"),
        ("യൂറിയ", "മൂത്രത്തിലെ പ്രധാന നൈട്രജൻ waste", ["ഗ്ലൂക്കോസ്", "ഓക്സിജൻ", "CO₂"], "medium"),
        ("ക്രെatinine", "muscle metabolism waste", ["urea", "glucose", "oxygen"], "hard"),
        ("hemodialysis", "artificial kidney", ["liver transplant", "lung dialysis", "heart bypass"], "hard"),
        ("ADH hormone", "water reabsorption increase", ["insulin", "adrenaline", "thyroxine"], "hard"),
        ("aldosterone", "sodium reabsorption", ["insulin", "adrenaline", "FSH"], "hard"),
        ("ureter", "kidney to bladder tube", ["urethra", "nephron", "glomerulus"], "medium"),
        ("nephron count human", "about 1 million per kidney", ["1000", "100 million", "100 per kidney"], "hard"),
        ("kidney stone main component", "calcium oxalate", ["urea", "glucose", "protein"], "hard"),
        ("dialysis principle", "diffusion across membrane", ["photosynthesis", "fermentation", "mitosis"], "hard"),
        ("glomerular filtration rate", "kidney function measure", ["heart rate", "respiratory rate", "blood pressure only"], "hard"),
        ("countercurrent multiplier", "loop of Henle", ["proximal tubule", "Bowmans capsule", "ureter"], "hard"),
        ("juxtaglomerular apparatus", "renin secretion", ["insulin secretion", "bile secretion", "saliva"], "hard"),
        ("renin", "blood pressure regulation", ["insulin", "bile", "pepsin"], "hard"),
        ("urine formation step 1", "filtration", ["reabsorption", "secretion", "digestion"], "medium"),
        ("urine formation step 2", "reabsorption", ["filtration", "photosynthesis", "respiration"], "medium"),
        ("urine formation step 3", "secretion", ["filtration only", "photosynthesis", "digestion"], "medium"),
        ("normal urine pH", "slightly acidic", ["strongly alkaline", "neutral always", "strongly basic"], "hard"),
        ("urea formation organ", "liver", ["kidney", "heart", "lung"], "medium"),
        ("ammonia toxic converted to", "urea", ["glucose", "oxygen", "CO₂"], "hard"),
        ("kidney hormone erythropoietin", "RBC production stimulate", ["insulin", "bile", "pepsin"], "hard"),
    ]
    for part in nephron:
        facts.append((f"നെഫ്രോൺ ഭാഗം — {part}", part, [x for x in nephron if x != part][:3], "hard"))
    return facts


def _tissue_facts() -> list[Fact]:
    types = [
        ("എപിതീലിയൽ", "ആവരണവും secretion", ["support only", "contraction", "impulse conduction"]),
        ("കണക്ടീവ്", "support bind protect", ["contraction", "impulse conduction", "secretion only"]),
        ("പേശി", "contraction movement", ["support only", "impulse conduction", "secretion only"]),
        ("നാഡീ", "impulse conduction", ["contraction", "support only", "secretion only"]),
    ]
    facts = [(f"കലാ തരം — {t}", a, w, "medium") for t, a, w in types]
    facts += [
        ("blood tissue type", "connective", ["epithelial", "muscular", "nervous"], "easy"),
        ("bone tissue type", "connective", ["epithelial", "muscular", "nervous"], "easy"),
        ("cartilage tissue type", "connective", ["epithelial", "muscular", "nervous"], "medium"),
        ("adipose tissue", "fat storage", ["bone formation", "impulse conduction", "secretion"], "medium"),
        ("areolar tissue", "fills space between organs", ["bone only", "muscle only", "nerve only"], "hard"),
        ("dense regular connective", "tendons ligaments", ["blood", "adipose", "bone marrow"], "hard"),
        ("squamous epithelium", "diffusion filtration", ["contraction", "support", "impulse"], "hard"),
        ("cuboidal epithelium", "secretion absorption", ["contraction", "support only", "impulse"], "hard"),
        ("columnar epithelium", "secretion absorption", ["contraction", "support only", "impulse"], "hard"),
        ("ciliated epithelium", "move mucus particles", ["fat storage", "bone formation", "blood clotting"], "hard"),
        ("striated muscle", "skeletal muscle", ["smooth muscle", "cardiac only", "nerve"], "medium"),
        ("unstriated muscle", "smooth muscle", ["skeletal muscle", "cardiac only", "nerve"], "medium"),
        ("cardiac muscle", "heart muscle", ["skeletal only", "smooth only", "nerve"], "medium"),
        ("neuron tissue", "nervous", ["connective", "epithelial", "muscular"], "easy"),
        ("neuroglia", "support neurons", ["contract muscle", "secrete bile", "filter blood"], "hard"),
        ("hyaline cartilage", "nose trachea", ["bone marrow", "tendon", "ligament"], "hard"),
        ("fibrocartilage", "intervertebral disc", ["hyaline only", "blood", "adipose"], "hard"),
        ("elastic cartilage", "ear epiglottis", ["hyaline only", "bone marrow", "tendon"], "hard"),
        ("compact bone", "dense outer bone", ["spongy only", "cartilage", "blood"], "hard"),
        ("spongy bone", "contains marrow", ["compact only", "cartilage", "tendon"], "hard"),
        ("tendon", "muscle to bone", ["ligament bone to bone", "nerve", "blood vessel"], "medium"),
        ("ligament", "bone to bone", ["tendon muscle to bone", "nerve", "blood vessel"], "medium"),
        ("meristematic tissue plants", "growth division", ["permanent tissue", "xylem", "phloem"], "hard"),
        ("xylem tissue function", "water conduction", ["food conduction", "photosynthesis", "respiration"], "medium"),
        ("phloem tissue function", "food conduction", ["water conduction", "photosynthesis", "respiration"], "medium"),
        ("parenchyma plant tissue", "photosynthesis storage", ["conduction only", "support only", "protection only"], "hard"),
        ("collenchyma plant tissue", "support flexibility", ["conduction only", "photosynthesis only", "protection only"], "hard"),
        ("sclerenchyma plant tissue", "dead support cells", ["photosynthesis", "conduction", "meristem"], "hard"),
        ("epidermis plant tissue", "protection", ["conduction", "photosynthesis only", "support only"], "medium"),
        ("stomata guard cells", "epidermal modification", ["xylem", "phloem", "cork"], "hard"),
        ("cork cambium", "protective bark", ["xylem", "phloem", "guard cells"], "hard"),
    ]
    return facts


def _skeletal_facts() -> list[Fact]:
    joints = [
        ("fixed joint", "skull sutures", ["hinge", "ball and socket", "pivot"]),
        ("hinge joint", "elbow knee", ["ball and socket", "pivot", "fixed"]),
        ("pivot joint", "neck atlas-axis", ["hinge", "ball and socket", "fixed"]),
        ("ball and socket joint", "hip shoulder", ["hinge", "pivot", "fixed"]),
        ("gliding joint", "wrist ankle", ["ball and socket", "pivot", "fixed"]),
        ("saddle joint", "thumb", ["hinge", "pivot", "fixed"]),
    ]
    facts = [(f"സന്ധി തരം — {t}", a, w, "medium") for t, a, w in joints]
    bones = [
        ("femur", "longest bone", ["humerus", "tibia", "radius"]),
        ("stapes", "smallest bone", ["femur", "humerus", "skull"]),
        ("humerus", "upper arm bone", ["femur", "tibia", "fibula"]),
        ("tibia", "shin bone", ["femur", "humerus", "radius"]),
        ("radius", "forearm bone thumb side", ["ulna", "femur", "tibia"]),
        ("ulna", "forearm bone pinky side", ["radius", "femur", "tibia"]),
        ("skull", "protects brain", ["ribs", "pelvis", "vertebrae"]),
        ("ribs", "protect heart lungs", ["skull", "pelvis", "femur"]),
        ("vertebrae", "spinal column", ["skull", "femur", "humerus"]),
        ("pelvis", "supports lower body", ["skull", "ribs", "radius"]),
        ("scapula", "shoulder blade", ["pelvis", "skull", "stapes"]),
        ("clavicle", "collar bone", ["femur", "tibia", "skull"]),
        ("patella", "knee cap", ["skull", "stapes", "clavicle"]),
        ("mandible", "lower jaw bone", ["maxilla", "femur", "skull only"]),
        ("maxilla", "upper jaw bone", ["mandible", "femur", "stapes"]),
        ("cranium", "brain case", ["mandible", "femur", "ribs"]),
        ("sternum", "breast bone", ["skull", "femur", "pelvis"]),
        ("phalanges", "finger toe bones", ["femur", "skull", "vertebrae"]),
        ("carpals", "wrist bones", ["tarsals", "femur", "skull"]),
        ("tarsals", "ankle bones", ["carpals", "femur", "skull"]),
        ("metacarpals", "palm bones", ["metatarsals", "femur", "skull"]),
        ("metatarsals", "foot bones", ["metacarpals", "femur", "skull"]),
        ("red bone marrow", "blood cell formation", ["yellow marrow fat", "cartilage", "ligament"]),
        ("yellow bone marrow", "fat storage", ["red marrow blood", "cartilage", "ligament"]),
        ("ossification", "bone formation", ["muscle formation", "nerve formation", "blood formation"]),
        ("synovial fluid", "joint lubrication", ["blood plasma", "lymph", "cerebrospinal fluid"]),
        ("arthritis", "joint inflammation", ["bone fracture", "muscle tear", "nerve damage"]),
        ("osteoporosis", "bone density loss", ["muscle atrophy", "nerve degeneration", "cartilage only"]),
        ("rickets", "vitamin D bone defect", ["scurvy", "beriberi", "anemia"]),
        ("sprain", "ligament injury", ["fracture", "dislocation only", "muscle tear only"]),
        ("fracture", "bone break", ["sprain", "strain only", "arthritis only"]),
    ]
    facts += [(f"അസ്ഥി/സkeletal — {t}", a, w, "medium") for t, a, w in bones]
    return facts


def _nomenclature_facts() -> list[Fact]:
    facts = []
    for ml, sci in BINOMIAL:
        facts.append((f"ശാസ്ത്രീയ നാമം — {ml}", sci, [s for _, s in BINOMIAL if s != sci][:3], "medium"))
    facts += [
        ("binomial nomenclature author", "Carl Linnaeus", ["Darwin", "Mendel", "Pasteur"], "medium"),
        ("genus name rule", "capital first letter", ["small always", "all caps", "no genus"], "hard"),
        ("species name rule", "small letters", ["capital always", "all caps", "no species"], "hard"),
        ("scientific name language", "Latin", ["Malayalam", "English", "Greek only"], "medium"),
        ("Homo sapiens genus", "Homo", ["Panthera", "Elephas", "Canis"], "easy"),
        ("Panthera tigris species", "tigris", ["leo", "sapiens", "maximus"], "medium"),
        ("trinomial nomenclature third name", "subspecies", ["genus", "family", "order"], "hard"),
        ("type specimen", "reference specimen", ["holotype only wrong", "genus only", "family only"], "hard"),
        ("ICZN full form", "International Code Zoological Nomenclature", ["Indian Code", "Internal Code", "International Chemical"], "hard"),
        ("ICN full form", "International Code Nomenclature algae fungi plants", ["Zoological Code", "Indian Code", "Internal Code"], "hard"),
    ]
    return facts


def _virus_facts() -> list[Fact]:
    rows = [
        ("HIV", "AIDS", ["TB", "malaria", "cholera"]),
        ("SARS-CoV-2", "COVID-19", ["HIV", "polio", "TB"]),
        ("Influenza virus", "flu", ["HIV", "rabies", "HBV"]),
        ("Hepatitis B virus", "hepatitis B", ["HIV", "polio", "TB"]),
        ("Poliovirus", "polio", ["HIV", "rabies", "dengue"]),
        ("Rabies virus", "rabies", ["HIV", "polio", "TB"]),
        ("Dengue virus", "dengue fever", ["HIV", "polio", "TB"]),
        ("Nipah virus", "Nipah", ["HIV", "polio", "TB"]),
        ("Ebola virus", "Ebola", ["HIV", "polio", "TB"]),
        ("Measles virus", "measles", ["HIV", "polio", "TB"]),
        ("Varicella virus", "chickenpox", ["HIV", "polio", "TB"]),
        ("Rotavirus", "diarrhea children", ["HIV", "polio", "TB"]),
        ("Papillomavirus", "warts cancer risk", ["HIV", "polio", "TB"]),
        ("Herpes virus", "cold sores", ["HIV", "polio", "TB"]),
        ("TMV", "tobacco mosaic plant virus", ["HIV", "polio", "bacteriophage only"]),
        ("Bacteriophage", "infects bacteria", ["infects plants only", "infects humans only", "infects fungi only"]),
        ("Retrovirus", "RNA to DNA reverse transcriptase", ["DNA only virus", "protein only", "bacteria"]),
        ("Viroid", "infects plants RNA only no protein coat", ["bacteria", "animal virus", "fungi only"]),
        ("Prion", "infectious protein no nucleic acid", ["bacteria", "virus with DNA", "fungi"]),
        ("virus genetic material DNA example", "herpes", ["TMV RNA", "HIV only", "prion"]),
        ("virus genetic material RNA example", "HIV", ["herpes DNA", "prion", "viroid only"]),
        ("virus replication site animal", "host cell", ["outside cell only", "soil only", "water only"]),
        ("virus size comparison bacteria", "smaller than bacteria", ["larger than bacteria", "same size", "visible naked eye"]),
        ("virus crystal form", "non-living crystal", ["always living", "always bacteria", "always fungi"]),
        ("Widal test detects", "typhoid antibodies", ["HIV", "malaria", "TB direct"]),
        ("ELISA used for", "antigen antibody detection", ["DNA sequencing only", "blood grouping only", "x-ray"]),
        ("viral vaccine type live attenuated example", "OPV polio", ["BCG bacteria", "tetanus toxoid only", "rabies killed only"]),
        ("viral vaccine killed example", "rabies vaccine", ["OPV live", "BCG", "MMR live only"]),
        ("antiviral oseltamivir for", "influenza", ["HIV", "hepatitis B", "TB"]),
        ("antiretroviral drugs for", "HIV", ["influenza", "hepatitis B", "TB"]),
    ]
    return [(f"വൈറസ് — {t}", a, w, "medium") for t, a, w in rows]


def _microbiology_facts() -> list[Fact]:
    rows = [
        ("Gram positive bacteria", "thick peptidoglycan purple stain", ["thin peptidoglycan pink", "no cell wall", "no stain"]),
        ("Gram negative bacteria", "thin peptidoglycan pink stain", ["thick peptidoglycan purple", "no cell wall", "no stain"]),
        ("E.coli", "Gram negative intestine", ["Gram positive", "acid fast", "no cell wall"]),
        ("Staphylococcus", "Gram positive cocci clusters", ["Gram negative rods", "spirilla", "acid fast"]),
        ("Streptococcus", "Gram positive cocci chains", ["Gram negative rods", "spirilla", "acid fast"]),
        ("Bacillus", "Gram positive rods", ["Gram negative cocci", "spirilla only", "acid fast"]),
        ("Salmonella typhi", "typhoid Gram negative", ["Gram positive", "acid fast", "no wall"]),
        ("Vibrio cholerae", "cholera comma shaped", ["Gram positive cocci", "acid fast", "spore only"]),
        ("Mycobacterium tuberculosis", "TB acid fast", ["Gram positive cocci", "Gram negative cocci", "no wall"]),
        ("Clostridium", "anaerobic spore forming", ["aerobic only", "no spores", "Gram negative cocci"]),
        ("Lactobacillus", "curd formation lactic acid", ["alcohol only", "acetic acid only", "no fermentation"]),
        ("Rhizobium", "nitrogen fixation legumes", ["nitrification", "denitrification", "photosynthesis"]),
        ("Azotobacter", "free living nitrogen fixation", ["parasitic only", "nitrification only", "denitrification only"]),
        ("Nitrosomonas", "ammonia to nitrite", ["nitrite to nitrate", "nitrate to nitrogen", "nitrogen fixation"]),
        ("Nitrobacter", "nitrite to nitrate", ["ammonia to nitrite", "nitrate to nitrogen", "nitrogen fixation"]),
        ("Pseudomonas", "denitrification", ["nitrogen fixation", "nitrification", "photosynthesis"]),
        ("Spirillum", "spiral bacteria", ["cocci only", "rods only", "no flagella"]),
        ("Cyanobacteria", "photosynthetic bacteria", ["chemosynthetic only", "parasitic only", "no pigment"]),
        ("Nostoc", "cyanobacteria nitrogen fixer", ["Rhizobium animal", "E.coli only", "virus"]),
        ("Anabaena", "cyanobacteria heterocyst nitrogen", ["E.coli", "Staph", "virus"]),
        ("Penicillium", "fungus antibiotic source", ["bacteria", "virus", "protozoa"]),
        ("Yeast", "unicellular fungus fermentation", ["bacteria", "virus", "algae only"]),
        ("Mycoplasma", "no cell wall smallest bacteria", ["largest bacteria", "virus", "fungi"]),
        ("Rickettsia", "obligatory intracellular parasite", ["free living", "virus", "fungi"]),
        ("Chlamydia", "intracellular bacteria STD", ["free living", "virus", "fungi"]),
        ("Actinomycetes", "filamentous bacteria soil", ["cocci only", "virus", "protozoa"]),
        ("Lactobacillus bulgaricus", "yogurt", ["alcohol yeast only", "acetic only", "no fermentation"]),
        ("Acetobacter", "acetic acid vinegar", ["lactic acid only", "alcohol only", "no fermentation"]),
        ("Koch postulates", "identify pathogen causation", ["Linnaeus classification", "Mendel genetics", "Darwin evolution"]),
        ("Pasteurization", "kill pathogens heat", ["cold only", "radiation only", "filtration only"]),
        ("autoclave", "121°C 15 psi sterilization", ["60°C only", "room temp", "freezing"]),
        ("antibiotic penicillin source", "Penicillium fungus", ["Streptomyces only", "E.coli", "virus"]),
        ("antibiotic streptomycin source", "Streptomyces bacteria", ["Penicillium only", "E.coli", "virus"]),
        ("disinfectant phenol coefficient", "germicidal strength", ["nutrient medium", "culture plate", "microscope"]),
    ]
    return [(f"സൂക്ഷ്മജീവശാസ്ത്രത്തിൽ '{t}'", a, w, "medium") for t, a, w in rows]


def _biotech_facts() -> list[Fact]:
    rows = [
        ("PCR full form", "Polymerase Chain Reaction", ["Protein Chain Reaction", "Plasmid Copy Reaction", "Polynucleotide Cell Reaction"]),
        ("PCR inventor", "Kary Mullis", ["Watson", "Crick", "Darwin"]),
        ("PCR purpose", "DNA amplification", ["protein synthesis", "RNA destruction", "cell division"]),
        ("restriction enzyme", "DNA cut specific sites", ["DNA join", "RNA copy", "protein digest"]),
        ("EcoRI", "restriction enzyme", ["DNA ligase", "RNA polymerase", "amylase"]),
        ("DNA ligase", "join DNA fragments", ["cut DNA", "copy RNA", "digest protein"]),
        ("plasmid", "extrachromosomal DNA vector", ["chromosome only", "RNA only", "protein only"]),
        ("recombinant DNA", "foreign gene inserted", ["natural DNA only", "RNA only", "protein only"]),
        ("genetic engineering", "manipulate genes", ["classify species", "count cells", "measure pH"]),
        ("transgenic organism", "foreign gene inserted", ["natural only", "no DNA", "RNA virus only"]),
        ("Bt cotton", "insect resistant transgenic", ["drought only", "salt only", "virus only"]),
        ("Golden rice", "vitamin A enriched", ["vitamin C only", "iron only", "protein only"]),
        ("insulin production recombinant", "E.coli bacteria", ["human directly", "plant only", "virus only"]),
        ("DNA fingerprinting", "identify individuals", ["measure blood pressure", "count RBC", "x-ray"]),
        ("gel electrophoresis", "separate DNA fragments size", ["count cells", "measure pH", "sterilize"]),
        ("Southern blot", "detect DNA", ["detect protein", "detect RNA only", "detect lipid"]),
        ("Northern blot", "detect RNA", ["detect DNA", "detect protein only", "detect lipid"]),
        ("Western blot", "detect protein", ["detect DNA", "detect RNA only", "detect lipid"]),
        ("ELISA biotechnology", "antibody antigen detection", ["DNA sequencing", "cell culture only", "x-ray"]),
        ("DNA sequencing Sanger method", "determine base order", ["protein order only", "RNA only", "lipid only"]),
        ("Human Genome Project completion", "2003", ["1990", "2010", "2020"]),
        ("CRISPR Cas9", "gene editing tool", ["DNA sequencing only", "PCR only", "electrophoresis only"]),
        ("CRISPR Nobel year", "2020", ["2003", "2010", "1990"]),
        ("clone Dolly sheep", "1996 somatic cell nuclear transfer", ["1990", "2000", "2010"]),
        ("stem cells", "undifferentiated divide differentiate", ["fully differentiated only", "dead cells", "protein only"]),
        ("embryonic stem cells", "pluripotent", ["unipotent only", "no division", "adult only"]),
        ("bioreactor", "large scale culture vessel", ["microscope", "centrifuge only", "autoclave only"]),
        ("fermentor biotechnology", "microbial product production", ["photosynthesis only", "respiration measure", "x-ray"]),
        ("single cell protein", "microbial biomass food", ["plant leaf only", "animal meat only", "mineral only"]),
        ("biopesticide Bacillus thuringiensis", "insect control", ["weed only", "fungus only", "nematode only"]),
        ("biofertilizer Rhizobium", "nitrogen fixation", ["phosphate only", "potash only", "pesticide"]),
        ("gene therapy", "correct defective genes", ["surgery only", "diet only", "exercise only"]),
        ("DNA probe", "detect specific sequence", ["detect pH", "detect temperature", "detect pressure"]),
        ("microarray", "analyze many genes", ["one gene only", "protein only", "lipid only"]),
        ("RNA interference", "silence gene expression", ["amplify gene", "delete chromosome", "mutate protein only"]),
        ("vector in cloning", "carries foreign DNA", ["cuts DNA", "joins protein", "digests RNA"]),
        ("competent cells", "take up plasmid DNA", ["reject all DNA", "produce bile", "form bone"]),
        ("selectable marker gene", "identify transformed cells", ["cut DNA", "join protein", "digest RNA"]),
        ("Ti plasmid", "Agrobacterium plant transformation", ["E.coli animal", "virus human", "yeast only"]),
        ("cDNA", "complementary DNA from mRNA", ["genomic DNA only", "protein", "lipid"]),
        ("reverse transcriptase", "RNA to DNA", ["DNA to RNA only", "protein synthesis", "lipid synthesis"]),
    ]
    return [(f"ജൈവസാങ്കേതികതയിൽ '{t}'", a, w, "medium") for t, a, w in rows]


def _evolution_facts() -> list[Fact]:
    rows = [
        ("natural selection", "Darwin survival of fittest", ["Mendel inheritance", "Linnaeus classification", "Pasteur germ theory"]),
        ("survival of the fittest", "best adapted reproduce", ["weakest survive", "random only", "no reproduction"]),
        ("adaptation", "trait increases fitness", ["decreases fitness", "no change", "extinction always"]),
        ("homologous organs", "same origin different function", ["same function different origin", "no relation", "vestigial only"]),
        ("analogous organs", "same function different origin", ["same origin different function", "no relation", "homologous"]),
        ("vestigial organs human", "appendix coccyx", ["heart lungs", "brain", "liver"]),
        ("fossil evidence evolution", "extinct life forms preserved", ["only living forms", "only bacteria", "only plants"]),
        ("comparative anatomy evidence", "structural similarities", ["only behavior", "only chemistry", "only physics"]),
        ("embryological evidence", "similar embryonic stages", ["no similarity", "adult only", "old age only"]),
        ("biogeographical evidence", "species distribution patterns", ["random distribution", "no patterns", "only ocean"]),
        ("molecular evidence evolution", "DNA protein similarities", ["no molecular data", "only fossils", "only anatomy"]),
        ("Lamarckism", "inheritance of acquired characters", ["natural selection", "Mendel genetics", "mutation only"]),
        ("use and disuse Lamarck", "organs develop with use", ["no change", "sudden creation", "only mutation"]),
        ("industrial melanism", "peppered moth dark form", ["bird migration", "plant growth", "fish evolution"]),
        ("speciation", "new species formation", ["extinction only", "no change", "cloning only"]),
        ("allopatric speciation", "geographic isolation", ["same area", "no isolation", "cloning"]),
        ("sympatric speciation", "same area new species", ["geographic isolation required", "no reproduction", "extinction"]),
        ("genetic drift", "random allele frequency change", ["natural selection only", "no change", "deterministic always"]),
        ("founder effect", "small group new population", ["large population", "no migration", "no change"]),
        ("bottleneck effect", "population size crash reduces diversity", ["increases diversity", "no effect", "extinction always"]),
        ("gene flow", "migration changes allele frequency", ["no migration", "no change", "isolation only"]),
        ("mutation evolution role", "ultimate source variation", ["no role", "only harmful", "only beneficial always"]),
        ("adaptive radiation", "many species from ancestor", ["one species only", "extinction only", "no diversity"]),
        ("Darwin finches", "adaptive radiation beak shapes", ["same beak all", "no birds", "only mammals"]),
        ("human evolution evidence", "fossils anatomy DNA", ["only mythology", "only astrology", "only physics"]),
        ("comparative biochemistry", "cytochrome c similarities", ["no biochemical data", "only fossils", "only behavior"]),
        ("convergent evolution", "analogous structures evolve", ["homologous only", "no evolution", "creation only"]),
        ("divergent evolution", "homologous from common ancestor", ["analogous only", "no ancestor", "creation only"]),
        ("molecular clock", "estimate divergence time", ["measure weight", "measure temperature", "measure pressure"]),
        ("endosymbiotic theory", "mitochondria chloroplast origin", ["nucleus origin", "ribosome origin", "cell wall origin"]),
        ("hardy weinberg equilibrium", "no evolution conditions", ["always evolving", "extinction", "speciation always"]),
        ("paleontology", "study fossils", ["study living only", "study stars", "study rocks only"]),
        ("anthropology human evolution", "study human origins", ["study plants only", "study stars", "study minerals"]),
        ("missing link meaning", "transitional fossil", ["no fossils", "living species", "mythical creature"]),
        ("Archaeopteryx", "link reptile bird", ["fish mammal", "plant fungus", "bacteria virus"]),
        ("Miller Urey experiment", "origin life molecules", ["DNA sequencing", "PCR", "cloning"]),
        ("abiogenesis", "life from non-life", ["biogenesis only", "no origin", "eternal life"]),
        ("biogenesis principle", "life from life", ["life from non-life always", "spontaneous always", "no reproduction"]),
        ("Oparin Haldane hypothesis", "primordial soup origin life", ["extraterrestrial only", "creation only", "no hypothesis"]),
    ]
    return [(f"പരിണാമശാസ്ത്രത്തിൽ '{t}'", a, w, "medium") for t, a, w in rows]


def _human_evolution_facts() -> list[Fact]:
    rows = [
        ("Homo habilis", "tool maker early human", ["Homo sapiens modern", "Neanderthal", "Australopithecus only"]),
        ("Homo erectus", "upright walker fire user", ["Homo habilis only", "modern human", "ape only"]),
        ("Homo neanderthalensis", "Europe archaic human", ["Homo sapiens only", "Homo habilis", "ape"]),
        ("Homo sapiens", "modern human", ["Homo erectus only", "Neanderthal only", "ape"]),
        ("Australopithecus afarensis", "Lucy fossil", ["Homo sapiens", "Neanderthal", "Java man"]),
        ("Ramapithecus", "human ape common ancestor candidate", ["modern human", "Neanderthal", "Homo erectus"]),
        ("Dryopithecus", "old world ape ancestor", ["modern human", "Neanderthal", "Homo sapiens"]),
        ("Cro-Magnon", "early Homo sapiens Europe", ["Neanderthal", "Homo habilis", "Australopithecus"]),
        ("Java man", "Homo erectus fossil", ["Homo sapiens", "Neanderthal", "Lucy"]),
        ("Peking man", "Homo erectus China", ["Homo sapiens", "Neanderthal", "Lucy"]),
        ("Neanderthal", "archaic human Europe Asia", ["modern human only", "Homo habilis", "Lucy"]),
        ("Cromagnon man period", "Upper Paleolithic", ["Lower Paleolithic only", "Mesozoic", "Cenozoic only"]),
        ("human brain size trend", "increased over evolution", ["decreased", "no change", "same as ape always"]),
        ("bipedalism", "walk on two legs", ["quadrupedal always", "swim only", "fly"]),
        ("opposable thumb", "tool use grip", ["no thumb", "webbed feet", "tail grip"]),
        ("cranial capacity Homo sapiens", "about 1350 ml", ["400 ml", "500 ml", "2000 ml"]),
        ("cranial capacity Australopithecus", "about 450 ml", ["1350 ml", "1200 ml", "2000 ml"]),
        ("Laetoli footprints", "bipedalism evidence", ["quadruped only", "swimming", "flying"]),
        ("Olduvai Gorge", "early human fossils Africa", ["Europe only", "Asia only", "Australia only"]),
        ("Out of Africa theory", "modern humans Africa origin", ["Europe origin", "Asia origin only", "America origin"]),
        ("multiregional hypothesis", "parallel evolution regions", ["single origin only", "no migration", "extraterrestrial"]),
        (" mitochondrial Eve", "maternal lineage origin", ["paternal only", "no genetics", "Y chromosome only"]),
        ("Y chromosomal Adam", "paternal lineage origin", ["maternal only", "no genetics", "mtDNA only"]),
        ("Neanderthal interbreeding", "some DNA in modern humans", ["no interbreeding", "complete replacement no DNA", "identical species always"]),
        ("Stone Age tools", "Paleolithic evidence culture", ["Iron Age only", "Modern only", "No tools"]),
        ("fire use human evolution", "Homo erectus associated", ["Homo sapiens only", "no fire use", "modern only"]),
        ("language development", "Homo sapiens advanced", ["no language ever", "ape same", "plant communication"]),
        ("cave paintings", "Upper Paleolithic art", ["Iron Age only", "Modern only", "No art"]),
        ("agriculture Neolithic revolution", "domestication plants animals", ["hunting only forever", "no change", "Industrial Revolution"]),
    ]
    return [(f"മനുഷ്യ പരിണാമത്തിൽ '{t}'", a, w, "medium") for t, a, w in rows]


def _pollution_facts() -> list[Fact]:
    rows = [
        ("eutrophication", "excess nutrients algal bloom", ["acid rain", "ozone depletion", "noise"]),
        ("biomagnification", "toxin concentration increases food chain", ["decreases up chain", "no effect", "only air"]),
        ("BOD", "biological oxygen demand water pollution", ["blood oxygen", "atmospheric oxygen", "soil nitrogen"]),
        ("COD", "chemical oxygen demand", ["biological only", "atmospheric", "soil"]),
        ("acid rain main gases", "SO2 NOx", ["O2 N2", "CO only", "CH4 only"]),
        ("greenhouse effect gases", "CO2 CH4 N2O", ["O2 only", "N2 only", "He only"]),
        ("ozone depletion cause", "CFCs", ["CO2 only", "O2 only", "N2 only"]),
        ("smog type photochemical", "NOx hydrocarbons sunlight", ["SO2 only", "CO only", "O3 only beneficial"]),
        ("minamata disease", "mercury poisoning", ["lead", "arsenic", "cadmium"]),
        ("itai-itai disease", "cadmium poisoning", ["mercury", "lead", "arsenic"]),
        ("blue baby syndrome", "nitrate water", ["phosphate", "sulfate", "chloride"]),
        ("fluorosis", "excess fluoride water", ["chlorine", "nitrate", "lead"]),
        ("arsenicosis", "arsenic groundwater", ["fluoride", "nitrate", "mercury"]),
        ("plastic pollution microplastics", "marine food chain harm", ["beneficial always", "no harm", "soil only"]),
        ("oil spill effect", "marine ecosystem damage", ["beneficial", "no effect", "soil only benefit"]),
        ("thermal pollution", "elevated water temperature", ["lower temperature", "no change", "air only"]),
        ("noise pollution unit", "decibel dB", ["pascal only", "joule only", "watt only"]),
        ("radioactive pollution unit", "becquerel gray sievert", ["pascal", "joule only", "liter"]),
        ("solid waste landfill", "non biodegradable persist", ["all biodegradable fast", "no waste", "only liquid"]),
        ("sewage treatment primary", "physical removal solids", ["biological only", "chemical only", "no treatment"]),
        ("sewage treatment secondary", "biological degradation", ["physical only", "no treatment", "radiation only"]),
        ("sewage treatment tertiary", "nutrient removal disinfection", ["physical only", "no treatment", "primary only"]),
        ("agrochemical pollution", "pesticide fertilizer runoff", ["no runoff", "beneficial always", "air only"]),
        ("deforestation pollution link", "CO2 increase habitat loss", ["CO2 decrease", "no effect", "O2 decrease only"]),
        ("industrial effluent", "toxic chemicals water", ["pure water", "beneficial", "air only"]),
        ("heavy metal pollution", "lead mercury cadmium", ["oxygen", "nitrogen", "hydrogen"]),
        ("cultural eutrophication", "human caused nutrient enrichment", ["natural only", "no algae", "desertification"]),
        ("global warming primary gas", "carbon dioxide", ["oxygen", "nitrogen", "argon"]),
        ("methane source pollution", "rice paddies cattle landfill", ["photosynthesis", "respiration only", "ocean absorption only"]),
        ("Montreal Protocol", "CFC phase out ozone", ["Kyoto CO2", "Paris accord only", "Ramsar wetlands"]),
        ("Kyoto Protocol", "greenhouse gas reduction", ["CFC only", "wetlands only", "wildlife trade"]),
        ("Paris Agreement", "climate change mitigation", ["CFC only", "wetlands only", "ozone only"]),
        ("Rio Earth Summit year", "1992", ["1982", "2002", "2012"]),
        ("World Environment Day", "June 5", ["June 1", "April 22", "March 22"]),
        ("World Water Day", "March 22", ["June 5", "April 22", "March 21"]),
        ("chipko movement", "forest conservation Himalaya", ["water pollution", "air pollution", "soil erosion only"]),
        ("silent spring author", "Rachel Carson", ["Darwin", "Mendel", "Linnaeus"]),
        ("PCB pollution", "persistent organic pollutant", ["biodegradable fast", "beneficial", "natural only"]),
        ("D DT effect", "biomagnification birds eggshell thinning", ["beneficial birds", "no effect", "soil enrichment"]),
    ]
    return [(f"പാരിസ്ഥിതി മലിനീകരണത്തിൽ '{t}'", a, w, "medium") for t, a, w in rows]


def _symbiosis_facts() -> list[Fact]:
    rows = [
        ("mutualism", "both species benefit", ["one harmed", "one benefits other unaffected", "both harmed"]),
        ("commensalism", "one benefits other unaffected", ["both benefit", "one harmed", "both harmed"]),
        ("parasitism", "one benefits other harmed", ["both benefit", "one unaffected", "both harmed"]),
        ("lichen", "fungus algae mutualism", ["parasitism", "predation", "competition only"]),
        ("mycorrhiza", "fungus root mutualism", ["parasitism", "predation", "no interaction"]),
        ("Rhizobium legume", "nitrogen fixation mutualism", ["parasitism", "predation", "no fixation"]),
        ("tapeworm human", "parasitism intestine", ["mutualism", "commensalism", "predation"]),
        ("orchid tree epiphyte", "commensalism", ["mutualism", "parasitism", "predation"]),
        ("cattle egret buffalo", "commensalism insects", ["parasitism", "mutualism strict", "predation"]),
        ("clownfish sea anemone", "mutualism protection", ["parasitism", "commensalism only", "predation"]),
        ("human gut bacteria", "mutualism digestion vitamin", ["parasitism always", "no bacteria", "predation"]),
        ("mosquito human", "parasitism blood", ["mutualism", "commensalism", "predation"]),
        ("tick dog", "parasitism blood", ["mutualism", "commensalism", "predation"]),
        ("plasmodium mosquito human", "parasitism malaria", ["mutualism", "commensalism", "predation"]),
        ("predation", "one kills eats other", ["mutualism", "commensalism", "parasitism no kill"]),
        ("competition", "both need same resource", ["mutualism", "commensalism", "parasitism"]),
        ("interspecific competition", "different species compete", ["same species only", "no competition", "mutualism"]),
        ("intraspecific competition", "same species compete", ["different species only", "no competition", "mutualism"]),
        ("proto cooperation", "both benefit not obligatory", ["obligate mutualism", "parasitism", "predation"]),
        ("endosymbiosis mitochondria", "cell bacteria origin", ["virus origin", "plant origin", "fungi origin"]),
        ("biological control ladybird", "aphid predator", ["parasite aphid", "mutualism aphid", "no control"]),
        ("brood parasitism cuckoo", "lay eggs other nest", ["mutualism", "commensalism", "predation adult"]),
        ("cleaning symbiosis fish", "mutualism remove parasites", ["parasitism", "predation", "competition"]),
        ("nitrogen fixing cyanobacteria Azolla", "rice paddy mutualism", ["parasitism", "predation", "no fixation"]),
        ("termite gut protozoa", "mutualism cellulose digestion", ["parasitism", "predation", "no digestion"]),
        ("rumen bacteria cow", "mutualism cellulose digestion", ["parasitism", "predation", "no digestion"]),
        ("epiphyte orchid", "commensalism on tree", ["parasitism tree", "mutualism strict", "predation"]),
        ("saprophytism", "feed dead organic matter", ["parasitism living", "predation", "photosynthesis"]),
        ("amensalism", "one inhibited other unaffected", ["both benefit", "both harmed", "mutualism"]),
        (" antibiosis", "one secretes inhibits other", ["mutualism", "commensalism", "predation"]),
    ]
    return [(f"പാരസ്പര്യശാസ്ത്രത്തിൽ '{t}'", a, w, "medium") for t, a, w in rows]


def _plant_repro_facts() -> list[Fact]:
    veg = [
        ("stem cutting", "rose sugarcane", ["seed only", "leaf only", "root only"]),
        ("root cutting", "lemon tamarind", ["stem only", "leaf only", "seed only"]),
        ("leaf cutting", "bryophyllum begonia", ["stem only", "root only", "seed only"]),
        ("layering", "jasmine", ["seed only", "spore only", "graft only"]),
        ("grafting", "mango rose citrus", ["seed only", "layering only", "spore only"]),
        ("budding", "rose citrus", ["seed only", "layering only", "spore only"]),
        ("tissue culture", "micropropagation", ["seed only", "graft only", "layering only"]),
        ("runner", "grass strawberry", ["tuber", "bulb", "rhizome"]),
        ("stolon", "mint jasmine", ["tuber", "bulb", "seed only"]),
        ("rhizome", "ginger turmeric", ["tuber potato", "bulb onion", "runner"]),
        ("tuber", "potato", ["bulb onion", "rhizome ginger", "runner"]),
        ("bulb", "onion garlic", ["tuber potato", "rhizome ginger", "runner"]),
        ("corm", "gladiolus", ["bulb onion", "tuber potato", "runner"]),
        ("offset", "aloe banana", ["seed only", "spore only", "graft only"]),
        ("eye bud potato", "tuber vegetative", ["seed", "spore", "fruit"]),
        ("sucker banana pineapple", "vegetative", ["seed only", "spore only", "graft only"]),
        ("bulbil", "dioscorea agave", ["seed only", "spore only", "runner only"]),
        ("parthenocarpy", "seedless fruit", ["seeded fruit", "spore", "vegetative only"]),
        ("parthenogenesis", "development without fertilization", ["always fertilization", "only animals never plants", "only seeds"]),
        ("apomixis", "seed without fertilization", ["always fertilization", "spore only", "vegetative only"]),
        ("microspore", "male gametophyte pollen", ["female gametophyte", "embryo", "endosperm"]),
        ("megaspore", "female gametophyte embryo sac", ["pollen", "embryo", "endosperm"]),
        ("pollen tube", "deliver male gametes", ["produce seed coat", "photosynthesis", "root growth"]),
        ("double fertilization", "angiosperm characteristic", ["gymnosperm only", "fern only", "moss only"]),
        ("triple fusion", "one sperm two polar nuclei endosperm", ["no fusion", "single fusion only", "no endosperm"]),
        ("syngamy", "egg sperm fusion zygote", ["endosperm only", "pollen only", "no fusion"]),
        ("endosperm", "triploid nutritive tissue", ["diploid embryo", "haploid pollen", "sporophyte only"]),
        ("embryo sac 7 cells 8 nuclei", "female gametophyte", ["male gametophyte", "embryo", "endosperm only"]),
        ("anther", "pollen production", ["ovule", "stigma", "style"]),
        ("stigma", "pollen reception", ["anther", "filament", "petal only"]),
        ("ovule", "contains embryo sac", ["pollen", "anther", "filament"]),
        ("seed dispersal wind", "drumstick maple", ["water only", "animal only", "explosive only"]),
        ("seed dispersal water", "coconut lotus", ["wind only", "animal only", "explosive only"]),
        ("seed dispersal animal", "mango guava", ["wind only", "water only", "explosive only"]),
        ("seed dispersal explosive", "castor balsam", ["wind only", "water only", "animal only"]),
    ]
    facts = [(f"സസ്യ പ്രജനനത്തിൽ '{t}'", a, w, "medium") for t, a, w in veg]
    return facts


def _biomolecule_facts() -> list[Fact]:
    rows = [
        ("glucose formula", "C6H12O6", ["C12H22O11", "CH4", "CO2"]),
        ("sucrose type", "disaccharide", ["monosaccharide", "polysaccharide", " amino acid"]),
        ("starch storage plant", "polysaccharide glucose", ["glycogen", "cellulose", "protein"]),
        ("glycogen storage animal", "liver muscle", ["starch plant", "cellulose", " chitin"]),
        ("cellulose", "plant cell wall", ["starch", "glycogen", " chitin animal"]),
        ("amino acid general formula", "NH2 CH COOH R", ["CO2 only", "CH4 only", "H2O only"]),
        ("peptide bond", "amino acids join", ["glycosidic", "ester", "phosphodiester"]),
        ("primary protein structure", "amino acid sequence", ["alpha helix", "beta sheet", "quaternary"]),
        ("secondary protein structure", "alpha helix beta sheet", ["sequence only", "quaternary", "denatured only"]),
        ("enzyme nature", "protein biological catalyst", ["carbohydrate catalyst", "lipid catalyst", "DNA catalyst"]),
        ("active site enzyme", "substrate binding", ["DNA binding", "lipid binding", "water binding"]),
        ("fatty acid", "carboxyl long chain", ["amino group", "phosphate", "sugar"]),
        ("triglyceride", "glycerol three fatty acids", ["one fatty acid", "amino acids", "nucleotides"]),
        ("phospholipid", "membrane bilayer", ["DNA", "protein only", "carbohydrate only"]),
        ("cholesterol", "steroid membrane", ["triglyceride", "phospholipid only", "protein"]),
        ("DNA bases", "A T G C", ["A U G C", "A T G U", "G C U T"]),
        ("RNA bases", "A U G C", ["A T G C", "A T G U", "G C T U"]),
        ("DNA double helix", "Watson Crick antiparallel", ["single strand", "triple helix", "no helix"]),
        ("RNA types mRNA", "protein coding message", ["ribosomal", "transfer", "DNA"]),
        ("tRNA", "carries amino acid translation", ["mRNA message", "rRNA ribosome", "DNA"]),
        ("rRNA", "ribosome component", ["mRNA", "tRNA", "DNA"]),
        ("ATP", "energy currency cell", ["DNA", "RNA", "glucose storage"]),
        ("NAD", "electron carrier coenzyme", ["ATP", "DNA", " glucose"]),
        ("FAD", "electron carrier coenzyme", ["ATP", "DNA", " glucose"]),
        ("hemoglobin", "oxygen transport protein", ["enzyme digest", "antibody", "hormone insulin"]),
        ("antibody", "immunoglobulin protein", ["enzyme", "hemoglobin", "collagen only"]),
        ("collagen", "connective tissue protein", ["hemoglobin", "enzyme", "antibody"]),
        ("keratin", "hair nail protein", ["collagen", "hemoglobin", "enzyme"]),
        ("vitamin C chemical name", "ascorbic acid", ["retinol", "calciferol", "tocopherol"]),
        ("vitamin D", "calciferol bone calcium", ["ascorbic acid", "thiamine", "niacin"]),
        ("vitamin B1", "thiamine", ["ascorbic acid", "calciferol", "retinol"]),
        ("DNA replication enzyme", "DNA polymerase", ["RNA polymerase", "ligase only", "amylase"]),
        ("denaturation protein", "loss structure heat pH", ["gain structure", "no change", "DNA only"]),
        ("saturated fat", "no double bonds", ["many double bonds", "phosphate", "amino"]),
        ("unsaturated fat", "double bonds present", ["no double bonds", "phosphate", "amino"]),
        ("nucleotide components", "base sugar phosphate", ["base only", "sugar only", "protein"]),
        ("purines", "adenine guanine", ["cytosine thymine", "uracil only", "glucose"]),
        ("pyrimidines", "cytosine thymine uracil", ["adenine guanine", "glucose", "fatty acid"]),
    ]
    return [(f"ജൈവഘടകശാസ്ത്രത്തിൽ '{t}'", a, w, "medium") for t, a, w in rows]


def _diagnostic_facts() -> list[Fact]:
    rows = [
        ("Widal test", "typhoid fever", ["malaria", "TB", "HIV"]),
        ("Mantoux test", "tuberculosis", ["typhoid", "malaria", "HIV"]),
        ("ELISA test", "HIV antibodies", ["blood sugar", "blood pressure", "hemoglobin only"]),
        ("PCR test", "DNA detection amplification", ["protein only", "sugar only", "x-ray"]),
        ("stool test ova parasite", "intestinal parasites", ["blood glucose", "blood pressure", "x-ray bone"]),
        ("blood smear malaria", "Plasmodium", ["TB bacteria", "HIV virus", "typhoid"]),
        ("Gram stain", "bacteria classification", ["virus", "fungus only", "parasite only"]),
        ("AFB stain", "acid fast bacilli TB", ["Gram positive cocci", "virus", "fungi only"]),
        ("biopsy", "tissue examination cancer", ["blood sugar", "urine sugar", "x-ray only"]),
        ("amniocentesis", "fetal chromosomal disorders", ["maternal blood sugar", "x-ray", "ECG"]),
        ("chorionic villus sampling", "prenatal genetic diagnosis", ["blood sugar", "x-ray", "ECG"]),
        ("karyotyping", "chromosome number structure", ["protein sequence", "sugar level", "blood pressure"]),
        ("ECG", "heart electrical activity", ["brain activity", "lung function", "kidney function"]),
        ("EEG", "brain electrical activity", ["heart activity", "lung function", "kidney function"]),
        ("spirometry", "lung function", ["heart function", "kidney function", "liver function"]),
        ("blood glucose test", "diabetes monitoring", ["malaria", "TB", "typhoid"]),
        ("HbA1c", "long term blood sugar", ["acute infection", "malaria", "TB"]),
        ("liver function test", "SGOT SGPT bilirubin", ["kidney only", "heart only", "lung only"]),
        ("kidney function test", "urea creatinine", ["liver only", "heart only", "lung only"]),
        ("lipid profile", "cholesterol triglycerides", ["blood sugar only", "malaria", "TB"]),
        ("RA factor test", "rheumatoid arthritis", ["malaria", "TB", "typhoid"]),
        ("CRP test", "inflammation marker", ["blood sugar", "malaria", "TB only"]),
        ("pap smear", "cervical cancer screening", ["blood sugar", "malaria", "TB"]),
        ("mammography", "breast cancer screening", ["blood sugar", "malaria", "TB"]),
        ("X-ray", "bone chest imaging", ["DNA sequence", "blood sugar", "stool parasite"]),
        ("CT scan", "cross sectional imaging", ["DNA sequence", "blood sugar", "stool parasite"]),
        ("MRI", "magnetic resonance imaging", ["DNA sequence", "blood sugar", "stool parasite"]),
        ("ultrasound", "sound wave imaging pregnancy", ["DNA sequence", "blood sugar", "stool parasite"]),
        ("urine dipstick", "glucose protein blood urine", ["DNA sequence", "ECG", "EEG"]),
        ("pregnancy test hCG", "urine blood", ["malaria", "TB", "typhoid"]),
        ("blood grouping ABO", "blood transfusion compatibility", ["malaria", "TB", "typhoid"]),
        ("Rh factor test", "hemolytic disease newborn", ["malaria", "TB", "typhoid"]),
        ("coomb's test", "autoimmune hemolytic anemia", ["malaria", "TB", "typhoid"]),
        ("sputum culture", "TB bacteria", ["malaria parasite", "HIV", "typhoid only"]),
        ("throat swab culture", "streptococcus", ["malaria", "HIV", "typhoid only"]),
        ("CSF analysis", "meningitis", ["malaria only", "diabetes", "hypertension"]),
        ("RPR VDRL", "syphilis", ["malaria", "TB", "typhoid"]),
        ("rapid antigen COVID", "SARS-CoV-2 protein", ["HIV only", "TB only", "malaria only"]),
        ("RT-PCR COVID", "viral RNA detection", ["bacteria only", "parasite only", "fungus only"]),
    ]
    return [(f"രോഗനിര്ണയശാസ്ത്രത്തിൽ '{t}'", a, w, "medium") for t, a, w in rows]


def generate_wave20_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []

    _emit(out, existing, rng, "സസ്യശാസ്ത്രത്തിൽ", _plant_physiology_facts())
    _emit(out, existing, rng, "സസ്യ ഹോർമോൺശാസ്ത്രത്തിൽ", _phytohormone_facts(), function_entity="സസ്യ ഹോർമോൺ")
    _emit(out, existing, rng, "ശ്വസനശാസ്ത്രത്തിൽ", _respiration_facts())
    _emit(out, existing, rng, "നാഡീവ്യൂഹശാസ്ത്രത്തിൽ", _nervous_facts())
    _emit(out, existing, rng, "ഹൃദയശാസ്ത്രത്തിൽ", _cardiac_facts())
    _emit(out, existing, rng, "മൂത്രപ്രത്യേകശാസ്ത്രത്തിൽ", _excretory_facts())
    _emit(out, existing, rng, "കലാശാസ്ത്രത്തിൽ", _tissue_facts())
    _emit(out, existing, rng, "അസ്ഥിപേശിശാസ്ത്രത്തിൽ", _skeletal_facts())
    _emit(out, existing, rng, "ജീവനാമകരണത്തിൽ", _nomenclature_facts())
    _emit(out, existing, rng, "വൈറസ് വിജ്ഞാനത്തിൽ", _virus_facts())
    _emit(out, existing, rng, "സൂക്ഷ്മജീവശാസ്ത്രത്തിൽ", _microbiology_facts())
    _emit(out, existing, rng, "ജൈവസാങ്കേതികതയിൽ", _biotech_facts())
    _emit(out, existing, rng, "പരിണാമശാസ്ത്രത്തിൽ", _evolution_facts())
    _emit(out, existing, rng, "മനുഷ്യ പരിണാമത്തിൽ", _human_evolution_facts())
    _emit(out, existing, rng, "പാരിസ്ഥിതി മലിനീകരണത്തിൽ", _pollution_facts())
    _emit(out, existing, rng, "പാരസ്പര്യശാസ്ത്രത്തിൽ", _symbiosis_facts())
    _emit(out, existing, rng, "സസ്യ പ്രജനനത്തിൽ", _plant_repro_facts())
    _emit(out, existing, rng, "ജൈവഘടകശാസ്ത്രത്തിൽ", _biomolecule_facts())
    _emit(out, existing, rng, "രോഗനിര്ണയശാസ്ത്രത്തിൽ", _diagnostic_facts())

    # Conservation — biosphere reserves
    _emit_pairs(
        out, existing, rng, "സംരക്ഷണശാസ്ത്രത്തിൽ ",
        BIOSPHERE_RESERVES,
        ["'{a}' ബയോസ്ഫിയർ റിസർവ് ഏത് സംസ്ഥാനത്താണ്?", "'{a}' ഏത് സംസ്ഥാനത്തിലെ ബയോസ്ഫിയർ റിസർവ് ആണ്?"],
        ["'{b}' സംസ്ഥാനത്തിലെ ബയോസ്ഫിയർ റിസർവ് ഏത്?", "'{b}'-ൽ സ്ഥിതി ചെയ്യുന്ന ബയോസ്ഫിയർ റിസർവ് '{a}' — ശരിയോ?"],
    )

    # Conservation — national parks (from geography_facts)
    parks = [(p, s) for p, s in INDIAN_NATIONAL_PARKS if p and s]
    _emit_pairs(
        out, existing, rng, "സംരക്ഷണശാസ്ത്രത്തിൽ ",
        parks,
        [
            "'{a}' ദേശീയോദ്യാനം ഏത് സംസ്ഥാനത്താണ്?",
            "'{a}' ദേശീയോദ്യാനം സ്ഥിതി ചെയ്യുന്ന സംസ്ഥാനം?",
            "'{a}' ഏത് സംസ്ഥാനത്തിലെ ദേശീയോദ്യാനമാണ്?",
        ],
        ["'{b}' സംസ്ഥാനത്തിലെ ദേശീയോദ്യാനം ഏത്?", "'{b}'-ൽ സ്ഥിതി ചെയ്യുന്ന ദേശീയോദ്യാനം ഏത്?"],
    )

    # Binomial reverse pairs
    binom_facts: list[Fact] = []
    for ml, sci in BINOMIAL:
        binom_facts.append((f"ശാസ്ത്രീയ നാമം '{sci}'", ml, [m for m, _ in BINOMIAL if m != ml][:3], "medium"))
    _emit(out, existing, rng, "ജീവനാമകരണത്തിൽ", binom_facts)

    # Enzyme function style for biomolecules enzymes subset
    enzymes = [
        ("അമൈലേസ്", "സ്റ്റാർച്ച് പചനം", ["പ്രോട്ടീൻ പചനം", "ലിപിഡ് പചനം", "DNA പചനം"], "medium"),
        ("പെപ്സിൻ", "പ്രോട്ടീൻ പചനം (അമ്ലാശയം)", ["സ്റ്റാർച്ച് പചനം", "ലിപിഡ് പചനം", "DNA പചനം"], "medium"),
        ("ട്രിപ്സിൻ", "പ്രോട്ടീൻ പചനം (ചെറുകുടൽ)", ["സ്റ്റാർച്ച് പചനം", "ലിപിഡ് പചനം", "DNA പചനം"], "medium"),
        ("ലൈപേസ്", "കൊഴുപ്പ് പചനം", ["സ്റ്റാർച്ച് പചനം", "പ്രോട്ടീൻ പചനം", "DNA പചനം"], "medium"),
        ("DNA പോളിമറേസ്", "DNA പുനരുല്പാദനം", ["RNA പുനരുല്പാദനം", "പ്രോട്ടീൻ പചനം", "ലിപിഡ് പചനം"], "hard"),
        ("RNA പോളിമറേസ്", "RNA സംശ്ലേഷണം", ["DNA പുനരുല്പാദനം", "പ്രോട്ടീൻ പചനം", "ലിപിഡ് പചനം"], "hard"),
        ("റെസ്ട്രിക്ഷൻ എൻഡോന്യൂക്ലിയേസ്", "DNA കട്ട് ചെയ്യൽ", ["DNA പുനരുല്പാദനം", "പ്രോട്ടീൻ പചനം", "ലിപിഡ് പചനം"], "hard"),
        ("ലിഗേസ്", "DNA ഫ്രാഗ്മെന്റുകൾ ബന്ധിപ്പിക്കൽ", ["DNA പുനരുല്പാദനം", "പ്രോട്ടീൻ പചനം", "ലിപിഡ് പചനം"], "hard"),
        ("കാറ്റലേസ്", "ഹൈഡ്രജൻ പെറോക്സൈഡ് വിഭജനം", ["സ്റ്റാർച്ച് പചനം", "പ്രോട്ടീൻ പചനം", "DNA പചനം"], "hard"),
        ("റുബിസ്കോ", "CO₂ ഫിക്സേഷൻ", ["DNA പുനരുല്പാദനം", "പ്രോട്ടീൻ പചനം", "ലിപിഡ് പചനം"], "hard"),
        ("ടൈറോസിനേസ്", "മെലനിൻ ഉൽപ്പാദനം", ["DNA പുനരുല്പാദനം", "പ്രോട്ടീൻ പചനം", "ലിപിഡ് പചനം"], "hard"),
        ("പൈരുവേറ്റ് ഡിഹൈഡ്രജനേസ്", "ഗ്ലൈക്കോളിസിസ്", ["DNA പുനരുല്പാദനം", "പ്രോട്ടീൻ പചനം", "ലിപിഡ് പചനം"], "hard"),
        ("സൈറ്റോക്രോം c", "ഇലക്ട്രോൺ ട്രാൻസ്പോർട്ട്", ["DNA പുനരുല്പാദനം", "പ്രോട്ടീൻ പചനം", "ലിപിഡ് പചനം"], "hard"),
    ]
    _emit(out, existing, rng, "ജൈവഘടകശാസ്ത്രത്തിൽ", enzymes, function_entity="എൻസൈം")

    # Alternate Malayalam stems — doubles coverage per fact pool
    alt_pools: list[tuple[str, list[Fact], str | None]] = [
        ("സസ്യശാസ്ത്രത്തിൽ", _plant_physiology_facts(), None),
        ("ശ്വസനശാസ്ത്രത്തിൽ", _respiration_facts(), None),
        ("നാഡീവ്യൂഹശാസ്ത്രത്തിൽ", _nervous_facts(), None),
        ("ഹൃദയശാസ്ത്രത്തിൽ", _cardiac_facts(), None),
        ("മൂത്രപ്രത്യേകശാസ്ത്രത്തിൽ", _excretory_facts(), None),
        ("കലാശാസ്ത്രത്തിൽ", _tissue_facts(), None),
        ("അസ്ഥിപേശിശാസ്ത്രത്തിൽ", _skeletal_facts(), None),
        ("വൈറസ് വിജ്ഞാനത്തിൽ", _virus_facts(), None),
        ("സൂക്ഷ്മജീവശാസ്ത്രത്തിൽ", _microbiology_facts(), None),
        ("ജൈവസാങ്കേതികതയിൽ", _biotech_facts(), None),
        ("പരിണാമശാസ്ത്രത്തിൽ", _evolution_facts(), None),
        ("മനുഷ്യ പരിണാമത്തിൽ", _human_evolution_facts(), None),
        ("പാരിസ്ഥിതി മലിനീകരണത്തിൽ", _pollution_facts(), None),
        ("പാരസ്പര്യശാസ്ത്രത്തിൽ", _symbiosis_facts(), None),
        ("സസ്യ പ്രജനനത്തിൽ", _plant_repro_facts(), None),
        ("ജൈവഘടകശാസ്ത്രത്തിൽ", _biomolecule_facts(), None),
        ("രോഗനിര്ണയശാസ്ത്രത്തിൽ", _diagnostic_facts(), None),
    ]
    for prefix, pool, func_ent in alt_pools:
        terms = list(dict.fromkeys(t for t, _, _, _ in pool))
        answers = list(dict.fromkeys(a for _, a, _, _ in pool))
        for term, ans, wrong, diff in pool:
            add_candidate(
                out, existing, rng,
                f"{prefix} '{term}'-ന്റെ ഉത്തരം ഏത്?",
                ans, wrong, diff, pool=answers,
            )
            add_candidate(
                out, existing, rng,
                f"'{term}' — {prefix.strip()} — ഏത്?",
                ans, wrong, diff, pool=answers,
            )
            add_candidate(
                out, existing, rng,
                f"{prefix} '{ans}' ഏതിനെ കுறിക്കുന്നു?",
                term, _pool(terms, term)[:6], diff, pool=terms,
            )

    # Disease–pathogen pairs (Malayalam)
    diseases = [
        ("മലേറിയ", "പ്ലാസ്മോഡിയം", ["HIV", "വിബ്രിയോ", "സാൽമോണella"]),
        ("ക്ഷയരോഗം", "മൈക്കോബാക്ടീരിയം ട്യൂബerculosis", ["പ്ലാസ്മോഡിയം", "HIV", "വിബ്രിയോ"]),
        ("കോളറ", "വിബ്രിയോ കോlerae", ["പ്ലാസ്മോഡിയം", "HIV", "സാൽമോണella"]),
        ("ടൈഫോയ്ഡ്", "സാൽമോണella typhi", ["പ്ലാസ്മോഡിയം", "HIV", "വിബ്രിയോ"]),
        ("എയ്ഡ്സ്", "HIV", ["പ്ലാസ്മോഡിയം", "HBV", "വിബ്രിയോ"]),
        ("കോവിഡ്-19", "SARS-CoV-2", ["HIV", "പ്ലാസ്മോഡിയം", "HBV"]),
        ("ഡെങ്കിപ്പനി", "ഡെങ്കു വൈറസ്", ["പ്ലാസ്മോഡിയം", "HIV", "വിബ്രിയോ"]),
        ("റേബീസ്", "റേബീസ് വൈറസ്", ["HIV", "പ്ലാസ്മോഡിയം", "HBV"]),
        ("പോളിയോ", "പോളiyo വൈറസ്", ["HIV", "പ്ലാസ്മോഡിയം", "HBV"]),
        ("നിപാ", "നിപാ വൈറസ്", ["HIV", "പ്ലാസ്മോഡിയം", "HBV"]),
        ("പെരുമ്പടവി", "മീസിൾസ് വൈറസ്", ["HIV", "പ്ലാസ്മോഡിയം", "HBV"]),
        ("ചിക്കൻപോക്സ്", "വാരisella വൈറസ്", ["HIV", "പ്ലാസ്മോഡിയം", "HBV"]),
        ("ടെറ്റനസ്", "ക്ലോസ്ട്രിഡിയം ടെറ്റani", ["പ്ലാസ്മോഡിയം", "HIV", "വിബ്രിയോ"]),
        ("ഡിഫ്തീരിയ", "കോർynibacterium diphtheriae", ["പ്ലാസ്മോഡിയം", "HIV", "വിബ്രിയോ"]),
        ("അമീബiasis", "എന്റamoiba histolytica", ["പ്ലാസ്മോഡിയം", "HIV", "വിബ്രിയോ"]),
        ("ഗിയാർഡിയasis", "Giardia lamblia", ["പ്ലാസ്മോഡിയം", "HIV", "വിബ്രിയോ"]),
        ("ആന്ത്രാക്സ്", "Bacillus anthracis", ["പ്ലാസ്മോഡിയം", "HIV", "വിബ്രിയോ"]),
        ("നയഗ്രiasis", "Naegleria fowleri", ["പ്ലാസ്മോഡിയം", "HIV", "വിബ്രിയോ"]),
        ("അൽഷർസ്", "Helicobacter pylori", ["പ്ലാസ്മോഡിയം", "HIV", "വിബ്രിയോ"]),
        ("അന്യുനീയmia", "പോഷക കുറവ്", ["HIV", "പ്ലാസ്മോഡിയം", "വിബ്രിയോ"]),
    ]
    dnames = [d for d, _, _ in diseases]
    dagents = [a for _, a, _ in diseases]
    for dis, agent, wrong, diff in [(d, a, w, "medium") for d, a, w in diseases]:
        add_candidate(out, existing, rng, f"രോഗനിര്ണയശാസ്ത്രത്തിൽ '{dis}'-ന്റെ കാരണം?", agent, wrong, diff, pool=dagents)
        add_candidate(out, existing, rng, f"'{agent}' ഏത് രോഗത്തിന് കാരണമാകുന്നു?", dis, _pool(dnames, dis)[:3], diff, pool=dnames)

    # Vitamin–deficiency (Malayalam)
    vitdef = [
        ("വിറ്റാമിൻ A", "രാത്രി അന്ധത", ["സ്കurvey", "rickets", "anemia"]),
        ("വിറ്റാമിൻ B1", "ബെriberi", ["scurvy", "rickets", "anemia"]),
        ("വിറ്റാമിൻ B12", "pernicious anemia", ["scurvy", "rickets", "beriberi"]),
        ("വിറ്റാമിൻ C", "സ്കurvey", ["rickets", "beriberi", "anemia"]),
        ("വിറ്റാമിൻ D", "rickets", ["scurvy", "beriberi", "anemia"]),
        ("വിറ്റാമിൻ K", "രക്തം കട്ടയാക്കൽ കുറവ്", ["scurvy", "rickets", "beriberi"]),
        ("അയോഡിൻ", "ഗോiter", ["scurvy", "rickets", "anemia"]),
        ("അയസ്", "anemia", ["scurvy", "rickets", "beriberi"]),
        ("കാൽcium", "osteoporosis", ["scurvy", "beriberi", "anemia"]),
    ]
    vnames = [v for v, _, _ in vitdef]
    for vit, deficiency, wrong in vitdef:
        add_candidate(out, existing, rng, f"ജൈവഘടകശാസ്ത്രത്തിൽ '{vit}' കുറവ്?", deficiency, wrong, "medium", pool=[d for _, d, _ in vitdef])
        add_candidate(out, existing, rng, f"'{deficiency}' — '{vit}' കുറവ്?", vit, _pool(vnames, vit)[:3], "medium", pool=vnames)

    # Organ–function (Malayalam)
    organs = [
        ("ഹൃദയം", "രക്തം പമ്പ് ചെയ്ത് circulation", ["ശ്വസനം", "പചനം", "മൂത്രം"]),
        ("ഫെഫുസ്സുകൾ", "ശ്വസനം", ["രക്തം പമ്പ്", "പചനം", "മൂത്രം"]),
        ("കരൾ", "വിഷാംശങ്ങൾ നീക്കം", ["ഇൻസുലിൻ", "ശ്വസനം", "ചിന്ത"]),
        ("മൂത്രപിണ്ഡം", "മൂത്രം ഉൽപ്പാദനം", ["ഇൻസുലിൻ", "പിത്തം", "ശ്വസനം"]),
        ("മസ്തിഷ്കം", "ചിന്തയും നിയന്ത്രണവും", ["പചനം", "ശ്വസനം", "മൂത്രം"]),
        ("അഗ്നാശയം", "ഇൻസുലിൻ ഉൽപ്പാദനം", ["പിത്തം", "അമ്ലം", "മൂത്രം"]),
        ("പിത്താശയം", "പിത്തരസം സംഭരണം", ["ഇൻസുലിൻ", "മൂത്രം", "ശ്വസനം"]),
        ("അമ്ലാശയം", "ഭക്ഷ്യ പചനം", ["ശ്വസനം", "ചിന്ത", "മൂത്രം"]),
        ("ചെറുകുടൽ", "പോഷക ശോഷണം", ["ജലം മാത്രം", "ശ്വസനം", "മൂത്രം"]),
        ("വലക്കുടൽ", "ജല ശോഷണം", ["പോഷക മാത്രം", "ശ്വസനം", "മൂത്രം"]),
        ("തൈറോയ്ഡ്", "മെറ്റാബോളിസം നിയന്ത്രണം", ["രക്തം പമ്പ്", "ശ്വസനം", "പചനം"]),
        ("പ്ലീഹ", "രക്ത ശുദ്ധീകരണം", ["ശ്വസനം", "പചനം", "ചിന്ത"]),
        ("പാൻക്രിയാസ്", "ഇൻസുലിൻ", ["പിത്തം", "മൂത്രം", "ശ്വസനം"]),
        ("നെഫ്രോൺ", "മൂത്രം ഉൽപ്പാദനം", ["വാതക കൈമാറ്റം", "പചനം", "പ്രകാശസംശ്ലേഷണം"]),
        ("സിനാപ്സ്", "നാഡീ സിഗ്നൽ കൈമാറ്റം", ["വാതക കൈമാറ്റം", "പചനം", "മൂത്രം"]),
    ]
    onames = [o for o, _, _ in organs]
    for organ, func, wrong in organs:
        add_candidate(out, existing, rng, f"ഹൃദയശാസ്ത്രത്തിൽ '{organ}'-ന്റെ പ്രവർത്തനം?", func, wrong, "medium")
        add_candidate(out, existing, rng, f"'{func}' ഏത് അവയവത്തിന്റെ പ്രവർത്തനമാണ്?", organ, _pool(onames, organ)[:3], "medium", pool=onames)

    # Wildlife sanctuaries / conservation extras
    sanctuaries = [
        ("പെരിയാർ", "കerala"), ("ഇടുക്കി", "കerala"), ("ചിന്നാർ", "കerala"),
        ("ആരളം", "കerala"), ("പeppara", "കerala"), ("നെല്ലiyampathy", "കerala"),
        ("ഭാരത്പൂർ", "രാജസ്ഥാൻ"), ("സariska", "രാജസ്ഥാൻ"), ("രanthambore", "രാജസ്ഥാൻ"),
        ("കaziranga", "അസം"), ("മanaas", "അസം"), ("പobitora", "അസം"),
        ("ജിമ് കോർബെറ്റ്", "ഉത്തരാഖണ്ഡ്"), ("വalley of flowers", "ഉത്തരാഖണ്ഡ്"),
        ("സunderban", "പശ്ചിമബംഗാൾ"), ("ഗir", "ഗുജറാത്ത്"), ("കanha", "മധ്യപ്രദേശ്"),
        ("ബandhavgarh", "മധ്യപ്രദേശ്"), ("പanna", "മധ്യപ്രദേശ്"), ("ടadoba", "മഹാരാഷ്ട്ര"),
        ("നागർഹോlé", "കarnataka"), ("ബandipur", "കarnataka"), ("മudumalai", "തമിഴ്നാട്"),
        ("സsilent valley", "കerala"), ("അnamudi shola", "കerala"), ("മundanthurai", "തമിഴ്നാട്"),
        ("പulicat", "തമിഴ്നാട്"), ("പoint calimere", "തമിഴ്നാട്"), ("വedanthangal", "തമിഴ്നാട്"),
        ("ഭitaraka", "ഒdisha"), ("Chilika", "ഒdisha"), ("Nandankanan", "ഒdisha"),
    ]
    _emit_pairs(
        out, existing, rng, "സംരക്ഷണശാസ്ത്രത്തിൽ ",
        sanctuaries,
        ["'{a}' വന്യജീവി santuary ഏത് സംസ്ഥാനത്താണ്?", "'{a}' sanctuary സംസ്ഥാനം?"],
        ["'{b}' സംസ്ഥാനത്തിലെ sanctuary '{a}'?", "'{b}'-ലെ sanctuary ഏത്?"],
    )

    # Extra national park templates
    _emit_pairs(
        out, existing, rng, "സംരക്ഷണശാസ്ത്രത്തിൽ ",
        parks,
        ["'{a}' ഏത് സംസ്ഥാനത്താണ്?", "ദേശീയോദ്യാനം '{a}' — സംസ്ഥാനം?"],
        None,
    )

    # Scientist contributions (Malayalam)
    scientists = [
        ("പ്രകൃതി തിരഞ്ഞെടുപ്പ്", "ചാർൾസ് ഡാർവിൻ", ["മെൻഡൽ", "ലിന്നേ", "പാസ്റ്റർ"]),
        ("ജനിതകശാസ്ത്രം", "ഗ്രേഗർ മെൻഡൽ", ["ഡാർവിൻ", "ലിന്നേ", "പാസ്റ്റർ"]),
        ("വർഗ്ഗീകരണം", "കാർൾ ലിന്നേ", ["ഡാർവിൻ", "മെൻഡൽ", "പാസ്റ്റർ"]),
        ("കീടാണു സിദ്ധാന്തം", "ലൂയി പാസ്റ്റർ", ["കോച്ച്", "ഡാർവിൻ", "മെൻഡൽ"]),
        ("DNA ദ്വിതന്ത്രം", "വാട്സൺ & ക്രിക്", ["ഡാർവിൻ", "മെൻഡൽ", "പാസ്റ്റർ"]),
        ("പെനിസിലിൻ", "ഫ്ലെമിംഗ്", ["പാസ്റ്റർ", "കോച്ച്", "മെൻഡൽ"]),
        ("PCR", "കാരി മുല്ലിസ്", ["വാട്സൺ", "ക്രിക്", "ഡാർവിൻ"]),
        ("ഇൻസുലിൻ", "ബാൻ്റിംഗ് & ബെസ്റ്റ്", ["ഫ്ലെമിംഗ്", "പാസ്റ്റർ", "കോച്ച്"]),
        ("പച്ചവിപ്ലവം", "എം.എസ്. സ്വാമിനാഥൻ", ["വർഗീസ് കുരിയൻ", "ബോർലോഗ്", "ഡാർവിൻ"]),
        ("വെള്ളവിപ്ലവം", "വർഗീസ് കുരിയൻ", ["സ്വാമിനാഥൻ", "ബോർലോഗ്", "ഡാർവിൻ"]),
    ]
    topics = [t for t, _, _ in scientists]
    pers = [p for _, p, _ in scientists]
    for topic, person, wrong in scientists:
        add_candidate(out, existing, rng, f"പരിണാമശാസ്ത്രത്തിൽ '{topic}'?", person, wrong, "medium", pool=pers)
        add_candidate(out, existing, rng, f"'{person}'-ന്റെ സംഭാവന?", topic, _pool(topics, topic)[:3], "medium", pool=topics)

    # Homo species extra stems
    homo_rows = _human_evolution_facts()
    _emit(out, existing, rng, "മനുഷ്യ പരിണാമത്തിൽ", [
        (f"Homo species — {t}", a, w, d) for t, a, w, d in homo_rows
    ])

    # Numeric biomolecule / cell facts (unique stems)
    numeric_facts: list[Fact] = [
        ("മനുഷ്യ ഡിപ്ലോയിഡ് ക്രോമോസോം ജോഡികൾ", "23", ["46", "22", "24"], "easy"),
        ("മനുഷ്യ somatic ക്രോമോസോം എണ്ണം", "46", ["23", "44", "48"], "easy"),
        ("മനുഷ്യ gamete ക്രോമോസോം", "23", ["46", "22", "24"], "easy"),
        ("മനുഷ്യ ഓട്ടോസോം ജോഡികൾ", "22", ["23", "46", "21"], "medium"),
        ("മനുഷ്യ ലൈംഗിക ക്രോമോസോം ജോഡികൾ", "1", ["2", "22", "23"], "medium"),
        ("ഡൗൺ സിൻഡ്രോം അധിക ക്രോമോസോം", "21", ["18", "13", "X"], "hard"),
        ("ടേർണർ സിൻഡ്രോം", "XO", ["XX", "XY", "XXY"], "hard"),
        ("ക്ലൈൻഫെൽട്ടർ", "XXY", ["XX", "XY", "XO"], "hard"),
        ("സാധാരണ ശരീര temp", "37°C", ["27°C", "47°C", "32°C"], "easy"),
        ("RBC lifespan days", "120", ["12", "1200", "30"], "hard"),
        ("normal heart rate per min", "72", ["120", "40", "100"], "easy"),
        ("human kidney nephron count", "about 1 million", ["1000", "100 million", "100"], "hard"),
        ("human cranial capacity ml sapiens", "1350", ["450", "500", "2000"], "hard"),
        ("Human Genome Project year", "2003", ["1990", "2010", "2020"], "hard"),
        ("Dolly clone year", "1996", ["1990", "2000", "2010"], "hard"),
        ("World Environment Day date", "June 5", ["June 1", "April 22", "March 22"], "easy"),
        ("Rio Summit year", "1992", ["1982", "2002", "2012"], "medium"),
    ]
    _emit(out, existing, rng, "ജൈവഘടകശാസ്ത്രത്തിൽ", numeric_facts)
    _emit(out, existing, rng, "മനുഷ്യ പരിണാമത്തിൽ", numeric_facts[:5])
    _emit(out, existing, rng, "ഹൃദയശാസ്ത്രത്തിൽ", numeric_facts[9:11])
    _emit(out, existing, rng, "മൂത്രപ്രത്യേകശാസ്ത്രത്തിൽ", [numeric_facts[11]])
    _emit(out, existing, rng, "പാരിസ്ഥിതി മലിനീകരണത്തിൽ", numeric_facts[15:17])

    # Extra binomial templates
    for ml, sci in BINOMIAL:
        scis = [s for _, s in BINOMIAL if s != sci]
        add_candidate(out, existing, rng, f"ജീവനാമകരണത്തിൽ '{ml}' genus?", sci.split()[0] if " " in sci else sci, [s.split()[0] if " " in s else s for s in scis][:3], "hard", pool=[s.split()[0] if " " in s else s for s in scis])
        add_candidate(out, existing, rng, f"'{sci}' — '{ml}'-ന്റെ?", "ശാസ്ത്രീയ നാമം", ["സാധാരണ നാമം", "കുടുംബ നാമം", "വർഗ്ഗ നാമം"], "medium")

    # Kerala PSC biology misc facts
    misc: list[Fact] = [
        ("ഇന്ത്യയുടെ ദേശീയ പുഷ്പം", "താമര", ["പനിനീർ", "ചെമ്പരത്തി", "മുല്ല"], "easy"),
        ("ഇന്ത്യയുടെ ദേശീയ വൃക്ഷം", "ആലമരം", ["വെട്ടി", "മാവ്", "നാരങ്ങ"], "easy"),
        ("ഇന്ത്യയുടെ ദേശീയ ഫലം", "മാങ്ങ", ["വാഴ", "ആപ്പിൾ", "പേര"], "easy"),
        ("ഇന്ത്യയുടെ ദേശീയ മൃഗം", "കടുവ", ["സിംഹം", "യാനം", "ചിരുത"], "easy"),
        ("ഇന്ത്യയുടെ ദേശീയ പക്ഷി", "മയിൽ", ["കാക്ക", "കഴുകൻ", "കുരുവി"], "easy"),
        ("ഇന്ത്യയുടെ ദേശീയ aquatic animal", "ഡോൾഫിൻ", ["തിമിംഗലം", "സ്രാവ്", "തവള"], "medium"),
        ("ഇന്ത്യയുടെ ദേശീയ river dolphin", "ഗംഗാ ഡോൾഫിൻ", ["സ്രാവ്", "തിമിംഗലം", "തവള"], "hard"),
        ("BCG vaccine disease", "ക്ഷയരോഗം", ["പോളിയോ", "മീസിൾസ്", "ഹെപ്പറ്റൈറ്റിസ്"], "medium"),
        ("OPV vaccine disease", "പോളിയോ", ["BCG", "മീസിൾസ്", "DPT"], "medium"),
        ("DPT vaccine diseases", "ഡിഫ്തീരിയ പെർടുസിസ് ടെറ്റനസ്", ["BCG", "OPV", "മീസിൾസ്"], "hard"),
        ("insulin deficiency disease", "diabetes mellitus", ["rickets", "scurvy", "anemia"], "medium"),
        ("thyroxine deficiency", "hypothyroidism goiter", ["diabetes", "rickets", "scurvy"], "hard"),
        ("adrenaline function", "fight or flight", ["digestion", "sleep", "photosynthesis"], "medium"),
        ("insulin function", "glucose uptake", ["oxygen transport", "blood clotting", "digestion only"], "medium"),
        ("hemoglobin function", "oxygen transport", ["immunity", "clotting", "digestion"], "easy"),
        ("platelet function", "blood clotting", ["oxygen transport", "immunity", "digestion"], "easy"),
        ("WBC function", "immunity", ["oxygen transport", "clotting", "digestion"], "easy"),
        ("mitosis result", "two identical cells", ["four haploid", "one cell", "gametes"], "medium"),
        ("meiosis result", "four haploid gametes", ["two identical", "one diploid", "cloning"], "medium"),
        ("photosynthesis product", "glucose oxygen", ["CO2 only", "N2", "ATP only"], "easy"),
        ("respiration product", "CO2 water ATP", ["O2 glucose", "N2", "glucose only"], "easy"),
    ]
    _emit(out, existing, rng, "സംരക്ഷണശാസ്ത്രത്തിൽ", misc[:6])
    _emit(out, existing, rng, "രോഗനിര്ണയശാസ്ത്രത്തിൽ", misc[6:10])
    _emit(out, existing, rng, "ജൈവഘടകശാസ്ത്രത്തിൽ", misc[10:])
    _emit(out, existing, rng, "ശ്വസനശാസ്ത്രത്തിൽ", [misc[19], misc[20]])

    # Extra PSC biology (count boost)
    extra_psc: list[Fact] = [
        ("ആക്സിജൻ ഹാരംഗതി", "ഹീമോഗ്ലോബിൻ", ["മയോഗ്ലോബിൻ", "ഇൻസുലിൻ", "ട്രിപ്സിൻ"], "easy"),
        ("രക്തം coagulation", "പ്ലേറ്റ്‌ലെറ്റ്", ["RBC", "WBC", "പ്ലാസ്മ"], "medium"),
        ("പച്ച chlorophyll pigment", "chlorophyll a", ["carotene only", "xanthophyll only", "anthocyanin"], "medium"),
        ("DNA double helix discoverers", "Watson Crick", ["Darwin", "Mendel", "Pasteur"], "hard"),
        ("DNA structure year", "1953", ["1865", "1928", "2003"], "hard"),
        ("Mendel law year", "1865", ["1953", "1859", "1900"], "hard"),
        ("Origin of Species year", "1859", ["1865", "1953", "1831"], "hard"),
        ("first antibiotic", "penicillin", ["streptomycin", "tetracycline", "insulin"], "medium"),
        ("penicillin discoverer", "Alexander Fleming", ["Pasteur", "Koch", "Jenner"], "hard"),
        ("smallpox vaccine discoverer", "Edward Jenner", ["Pasteur", "Koch", "Fleming"], "hard"),
        ("germ theory", "Louis Pasteur", ["Darwin", "Mendel", "Watson"], "hard"),
        ("Koch postulates", "Robert Koch", ["Pasteur", "Jenner", "Fleming"], "hard"),
        ("Green Revolution father India", "M S Swaminathan", ["Norman Borlaug", "Verghese Kurien", "C V Raman"], "hard"),
        ("Father of Green Revolution", "Norman Borlaug", ["Swaminathan", "Mendel", "Darwin"], "hard"),
        ("Father of White Revolution", "Verghese Kurien", ["Swaminathan", "Borlaug", "Pasteur"], "hard"),
        ("Father of Genetics", "Gregor Mendel", ["Darwin", "Watson", "Lamarck"], "easy"),
        ("Father of Evolution", "Charles Darwin", ["Mendel", "Lamarck", "Wallace"], "easy"),
        ("Father of Taxonomy", "Carolus Linnaeus", ["Darwin", "Mendel", "Aristotle"], "medium"),
        ("Father of Microbiology", "Louis Pasteur", ["Koch", "Leeuwenhoek", "Jenner"], "medium"),
        ("Father of Indian Botany", "William Roxburgh", ["Birbal Sahni", "Hooker", "Linnaeus"], "hard"),
    ]
    _emit(out, existing, rng, "ജൈവഘടകശാസ്ത്രത്തിൽ", extra_psc[:3])
    _emit(out, existing, rng, "ജൈവസാങ്കേതികതയിൽ", extra_psc[3:5])
    _emit(out, existing, rng, "പരിണാമശാസ്ത്രത്തിൽ", extra_psc[5:8])
    _emit(out, existing, rng, "സൂക്ഷ്മജീവശാസ്ത്രത്തിൽ", extra_psc[8:12])
    _emit(out, existing, rng, "സസ്യശാസ്ത്രത്തിൽ", extra_psc[12:15])
    _emit(out, existing, rng, "പരിണാമശാസ്ത്രത്തിൽ", extra_psc[15:])

    return out


if __name__ == "__main__":
    import random as _r
    print(len(generate_wave20_candidates(set(), _r.Random(42))))
