#!/usr/bin/env python3
"""Generate communication_journalism_wave30_facts.py — 30 Malayalam PSC topic types."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "communication_journalism_wave30_facts.py"

HEADER = '''#!/usr/bin/env python3
"""Wave 30 communication / journalism facts — 30 Kerala PSC topic types."""

from __future__ import annotations

import random

from refill_common import Candidate
from wave30_emit import emit_category, emit_direct

'''

EMIT = '''
def generate_wave30_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []

    emit_category(out, existing, rng, COMM_MODELS,
        ["'{a}' ആശയവിനിമയ മോഡലുമായി ബന്ധപ്പെട്ട വസ്തുത?", "'{a}'-ന്റെ പ്രധാന സവിശേഷത?", "'{a}' മോഡൽ സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട ആശയവിനിമയ മോഡൽ?", "'{b}' വിവരമുള്ള കമ്മ്യൂണിക്കേഷൻ മോഡൽ?", "'{b}'-ന് ഏത് മോഡൽ?"],
        [a for a, _ in COMM_MODELS], [b for _, b in COMM_MODELS])

    emit_category(out, existing, rng, COMM_THEORIES,
        ["'{a}' സിദ്ധാന്തം ആരുടേതാണ്?", "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന സിദ്ധാന്തജ്ഞൻ?", "'{a}' സിദ്ധാന്തത്തിന്റെ പ്രതിപാദകൻ?"],
        ["'{b}' ആരുടെ സിദ്ധാന്തമാണ്?", "'{b}'-ന്റെ പ്രധാന സിദ്ധാന്തം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സിദ്ധാന്തം?"],
        [a for a, _ in COMM_THEORIES], [b for _, b in COMM_THEORIES])

    emit_category(out, existing, rng, THEORY_MEANING,
        ["'{a}' സിദ്ധാന്തത്തിന്റെ പ്രധാന ആശയം?", "'{a}'-ന്റെ കേന്ദ്ര സങ്കല്പം?", "'{a}' സിദ്ധാന്തം എന്ത് പറയുന്നു?"],
        ["'{b}' ആശയമുള്ള മാധ്യമ സിദ്ധാന്തം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സിദ്ധാന്തം?", "'{b}' പ്രതിപാദിക്കുന്ന സിദ്ധാന്തം?"],
        [a for a, _ in THEORY_MEANING], [b for _, b in THEORY_MEANING])

    emit_category(out, existing, rng, MALAYALAM_FIRST,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' മലയാള പത്രചരിത്ര വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട മലയാള പത്രചരിത്ര വസ്തുത?", "'{b}' വിവരമുള്ള മലയാള മാധ്യമം?", "'{b}'-ന് ഏത്?"],
        [a for a, _ in MALAYALAM_FIRST], [b for _, b in MALAYALAM_FIRST])

    emit_category(out, existing, rng, MALAYALAM_FOUNDER,
        ["'{a}' ഏത് മലയാള പത്രവുമായി ബന്ധപ്പെട്ട വ്യക്തി?", "'{a}'-ന്റെ പ്രധാന പത്രപ്രവർത്തന സംബന്ധം?", "'{a}' ആരംഭിച്ച/സമ്പാദിച്ച പത്രം?"],
        ["'{b}'-ന്റെ സ്ഥാപകൻ/പത്രാധിപർ ആര്?", "'{b}' പത്രവുമായി ബന്ധപ്പെട്ട വ്യക്തി?", "'{b}'-ന് ഏത് വ്യക്തി?"],
        [a for a, _ in MALAYALAM_FOUNDER], [b for _, b in MALAYALAM_FOUNDER])

    emit_category(out, existing, rng, MALAYALAM_PRESS_YEAR,
        ["'{a}' പത്രം സ്ഥാപിതമായ/ആരംഭിച്ച വർഷം?", "'{a}'-ന്റെ സ്ഥാപന വർഷം?", "'{a}' ആരംഭിച്ച വർഷം?"],
        ["'{b}' വർഷം ആരംഭിച്ച മലയാള പത്രം?", "'{b}'-ൽ പ്രസിദ്ധീകരണം ആരംഭിച്ച പത്രം?", "'{b}' വർഷത്തിലെ പ്രധാന മലയാള പത്രം?"],
        [a for a, _ in MALAYALAM_PRESS_YEAR], [b for _, b in MALAYALAM_PRESS_YEAR])

    emit_category(out, existing, rng, INDIA_PRESS_HISTORY,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' ഇന്ത്യൻ പത്രചരിത്ര വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട ഇന്ത്യൻ പത്രചരിത്ര വസ്തുത?", "'{b}' വിവരമുള്ള ഇന്ത്യൻ പത്രം/സംഭവം?", "'{b}'-ന് ഏത്?"],
        [a for a, _ in INDIA_PRESS_HISTORY], [b for _, b in INDIA_PRESS_HISTORY])

    emit_category(out, existing, rng, INDIA_PRESS_PIONEER,
        ["'{a}' ഏത് പത്രപ്രവർത്തന സംബന്ധത്തിലാണ്?", "'{a}'-ന്റെ പ്രധാന പത്രപ്രവർത്തന സംഭാവന?", "'{a}'-യുമായി ബന്ധപ്പെട്ട പത്രം/സംഭവം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട ഇന്ത്യൻ പത്രനായകൻ?", "'{b}' സംബന്ധിച്ച പ്രധാന വ്യക്തി?", "'{b}'-ന് ഏത് വ്യക്തി?"],
        [a for a, _ in INDIA_PRESS_PIONEER], [b for _, b in INDIA_PRESS_PIONEER])

    emit_category(out, existing, rng, JOURNALISM_TERMS,
        ["'{a}'-ന്റെ അർത്ഥം/വ്യാഖ്യാനം?", "'{a}' എന്ന പദം എന്താണ്?", "'{a}'-ന്റെ പ്രധാന സവിശേഷത?"],
        ["'{b}' അർത്ഥമുള്ള പത്രപ്രവർത്തന പദം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട ജേർണലിസം പദം?", "'{b}'-ന് ഏത് പദം?"],
        [a for a, _ in JOURNALISM_TERMS], [b for _, b in JOURNALISM_TERMS])

    emit_category(out, existing, rng, PRESS_LAWS,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' പത്ര/മാധ്യമ നിയമ വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട പത്ര/മാധ്യമ നിയമം?", "'{b}' വിവരമുള്ള മാധ്യമ നിയമം?", "'{b}'-ന് ഏത് നിയമം?"],
        [a for a, _ in PRESS_LAWS], [b for _, b in PRESS_LAWS])

    emit_category(out, existing, rng, PRASAR_BHARATI,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' പ്രേഷണ വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട പ്രേഷണ വസ്തുത?", "'{b}' വിവരമുള്ള പ്രസാർ ഭാരതി/ആകാശവാണി/ദൂരദർശൻ?", "'{b}'-ന് ഏത്?"],
        [a for a, _ in PRASAR_BHARATI], [b for _, b in PRASAR_BHARATI])

    emit_category(out, existing, rng, PCI,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' പ്രസ് കൗൺസിൽ/PCI വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട PCI/പ്രസ് കൗൺസിൽ വസ്തുത?", "'{b}' വിവരമുള്ള PCI?", "'{b}'-ന് ഏത്?"],
        [a for a, _ in PCI], [b for _, b in PCI])

    emit_category(out, existing, rng, TRP_BARC,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' TRP/BARC/ABC വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട TRP/റേറ്റിംഗ്/പ്രചാരണ വസ്തുത?", "'{b}' വിവരമുള്ള BARC/ABC?", "'{b}'-ന് ഏത്?"],
        [a for a, _ in TRP_BARC], [b for _, b in TRP_BARC])

    emit_category(out, existing, rng, DIGITAL_MEDIA,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' ഡിജിറ്റൽ മാധ്യമ വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട ഡിജിറ്റൽ മാധ്യമം?", "'{b}' വിവരമുള്ള ഡിജിറ്റൽ മാധ്യമ പദം?", "'{b}'-ന് ഏത്?"],
        [a for a, _ in DIGITAL_MEDIA], [b for _, b in DIGITAL_MEDIA])

    emit_category(out, existing, rng, NEWS_AGENCIES,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' വാർത്താ ഏജൻസി വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട വാർത്താ ഏജൻസി?", "'{b}' വിവരമുള്ള വാർത്താ ഏജൻസി?", "'{b}'-ന് ഏത് ഏജൻസി?"],
        [a for a, _ in NEWS_AGENCIES], [b for _, b in NEWS_AGENCIES])

    emit_category(out, existing, rng, BROADCAST_TERMS,
        ["'{a}'-ന്റെ അർത്ഥം/വ്യാഖ്യാനം?", "'{a}' പ്രക്ഷേപണ പദം എന്താണ്?", "'{a}'-ന്റെ പ്രധാന സവിശേഷത?"],
        ["'{b}' അർത്ഥമുള്ള പ്രക്ഷേപണ പദം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട ടിവി/റേഡിയോ പദം?", "'{b}'-ന് ഏത് പദം?"],
        [a for a, _ in BROADCAST_TERMS], [b for _, b in BROADCAST_TERMS])

    emit_category(out, existing, rng, JOURNALISM_TYPES,
        ["'{a}'-ന്റെ പ്രധാന സവിശേഷത?", "'{a}' ജേർണലിസം തരം എന്താണ്?", "'{a}'-ന്റെ വ്യാഖ്യാനം?"],
        ["'{b}' അർത്ഥമുള്ള ജേർണലിസം തരം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട റിപ്പോർട്ടിംഗ് രീതി?", "'{b}'-ന് ഏത് ജേർണലിസം?"],
        [a for a, _ in JOURNALISM_TYPES], [b for _, b in JOURNALISM_TYPES])

    emit_category(out, existing, rng, MASS_MEDIA,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' മാസ് മീഡിയ വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട മാസ് മീഡിയ?", "'{b}' വിവരമുള്ള മാധ്യമം?", "'{b}'-ന് ഏത് മാധ്യമം?"],
        [a for a, _ in MASS_MEDIA], [b for _, b in MASS_MEDIA])

    emit_category(out, existing, rng, ADVERTISING_PR,
        ["'{a}'-ന്റെ അർത്ഥം/വ്യാഖ്യാനം?", "'{a}' പരസ്യ/PR പദം എന്താണ്?", "'{a}'-ന്റെ പ്രധാന സവിശേഷത?"],
        ["'{b}' അർത്ഥമുള്ള പരസ്യ/PR പദം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട മാർക്കറ്റിംഗ് പദം?", "'{b}'-ന് ഏത് പദം?"],
        [a for a, _ in ADVERTISING_PR], [b for _, b in ADVERTISING_PR])

    emit_category(out, existing, rng, MEDIA_FREEDOM,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' മാധ്യമ സ്വാതന്ത്ര്യ വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട മാധ്യമ സ്വാതന്ത്ര്യം?", "'{b}' വിവരമുള്ള ഭരണഘടന/അവകാശം?", "'{b}'-ന് ഏത്?"],
        [a for a, _ in MEDIA_FREEDOM], [b for _, b in MEDIA_FREEDOM])

    emit_category(out, existing, rng, PRINT_HISTORY,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' അച്ചടി/മുദ്രണ ചരിത്ര വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട അച്ചടി/മുദ്രണ ചരിത്രം?", "'{b}' വിവരമുള്ള മുദ്രണ സംഭവം?", "'{b}'-ന് ഏത്?"],
        [a for a, _ in PRINT_HISTORY], [b for _, b in PRINT_HISTORY])

    emit_category(out, existing, rng, SOCIAL_MEDIA,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' സോഷ്യൽ മീഡിയ വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട സോഷ്യൽ മീഡിയ?", "'{b}' വിവരമുള്ള പ്ലാറ്റ്ഫോം?", "'{b}'-ന് ഏത് പ്ലാറ്റ്ഫോം?"],
        [a for a, _ in SOCIAL_MEDIA], [b for _, b in SOCIAL_MEDIA])

    emit_category(out, existing, rng, MEDIA_ETHICS,
        ["'{a}'-ന്റെ അർത്ഥം/വ്യാഖ്യാനം?", "'{a}' മാധ്യമ നൈതികത പദം?", "'{a}'-ന്റെ പ്രധാന സവിശേഷത?"],
        ["'{b}' അർത്ഥമുള്ള മാധ്യമ നൈതികത/നിയമ പദം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട പത്രപ്രവർത്തന കുറ്റം?", "'{b}'-ന് ഏത് പദം?"],
        [a for a, _ in MEDIA_ETHICS], [b for _, b in MEDIA_ETHICS])

    emit_category(out, existing, rng, NEWSPAPER_LAYOUT,
        ["'{a}'-ന്റെ അർത്ഥം/വ്യാഖ്യാനം?", "'{a}' പത്ര ലേഔട്ട് പദം?", "'{a}'-ന്റെ പ്രധാന സവിശേഷത?"],
        ["'{b}' അർത്ഥമുള്ള പത്ര ലേഔട്ട് പദം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട പത്ര ഘടകം?", "'{b}'-ന് ഏത് പദം?"],
        [a for a, _ in NEWSPAPER_LAYOUT], [b for _, b in NEWSPAPER_LAYOUT])

    emit_category(out, existing, rng, FILM_MEDIA_BODIES,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' സിനിമ/മാധ്യമ സ്ഥാപന വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട സിനിമ/മാധ്യമ സ്ഥാപനം?", "'{b}' വിവരമുള്ള സർട്ടിഫിക്കേഷൻ/സ്ഥാപനം?", "'{b}'-ന് ഏത്?"],
        [a for a, _ in FILM_MEDIA_BODIES], [b for _, b in FILM_MEDIA_BODIES])

    emit_category(out, existing, rng, KERALA_MEDIA,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' കേരള മാധ്യമ വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട കേരള മാധ്യമം?", "'{b}' വിവരമുള്ള കേരള ചാനൽ/റേഡിയോ?", "'{b}'-ന് ഏത്?"],
        [a for a, _ in KERALA_MEDIA], [b for _, b in KERALA_MEDIA])

    emit_category(out, existing, rng, MEDIA_ABBREV,
        ["'{a}' എന്ന സംക്ഷേപത്തിന്റെ പൂർണ്ണരൂപം?", "'{a}'-ന്റെ വിപുലീകരണം?", "'{a}' എന്തിനെ സൂചിപ്പിക്കുന്നു?"],
        ["'{b}' പൂർണ്ണരൂപമുള്ള മാധ്യമ സംക്ഷേപം?", "'{b}' ഏത് ചുരുക്കെഴുത്തിൽ?", "'{b}'-ന് ഏത് സംക്ഷേപം?"],
        [a for a, _ in MEDIA_ABBREV], [b for _, b in MEDIA_ABBREV], english=True)

    emit_category(out, existing, rng, INTERNATIONAL_PRESS,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' അന്താരാഷ്ട്ര പത്രപ്രവർത്തന വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട അന്താരാഷ്ട്ര പത്രസംഭവം?", "'{b}' വിവരമുള്ള പ്രശസ്ത പത്രം/സംഭവം?", "'{b}'-ന് ഏത്?"],
        [a for a, _ in INTERNATIONAL_PRESS], [b for _, b in INTERNATIONAL_PRESS])

    emit_category(out, existing, rng, COMM_LEVELS,
        ["'{a}'-ന്റെ അർത്ഥം/വ്യാഖ്യാനം?", "'{a}' ആശയവിനിമയ തലം?", "'{a}'-ന്റെ പ്രധാന സവിശേഷത?"],
        ["'{b}' അർത്ഥമുള്ള ആശയവിനിമയ തലം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട കമ്മ്യൂണിക്കേഷൻ?", "'{b}'-ന് ഏത് തലം?"],
        [a for a, _ in COMM_LEVELS], [b for _, b in COMM_LEVELS])

    emit_category(out, existing, rng, MEDIA_REGULATION,
        ["'{a}'-ന്റെ പ്രധാന വിവരം?", "'{a}' മാധ്യമ നിയന്ത്രണ സ്ഥാപന വസ്തുത?", "'{a}' സംബന്ധിച്ച വിവരം?"],
        ["'{b}'-യുമായി ബന്ധപ്പെട്ട മാധ്യമ നിയന്ത്രണ സ്ഥാപനം?", "'{b}' വിവരമുള്ള നിയന്ത്രക സ്ഥാപനം?", "'{b}'-ന് ഏത്?"],
        [a for a, _ in MEDIA_REGULATION], [b for _, b in MEDIA_REGULATION])

    emit_direct(out, existing, rng, DIRECT_FACTS)
    return out


if __name__ == "__main__":
    print(len(generate_wave30_candidates(set(), random.Random(0))))
'''

EMIT = EMIT.replace("പ്രസാർ ഭാരതി", "പ്രസാർ ഭാരതി")

from cj_wave30_data import (  # noqa: E402
    ADVERTISING_PR,
    BROADCAST_TERMS,
    COMM_LEVELS,
    COMM_MODELS,
    COMM_THEORIES,
    DIGITAL_MEDIA,
    DIRECT_FACTS,
    FILM_MEDIA_BODIES,
    INDIA_PRESS_HISTORY,
    INDIA_PRESS_PIONEER,
    INTERNATIONAL_PRESS,
    JOURNALISM_TERMS,
    JOURNALISM_TYPES,
    KERALA_MEDIA,
    MALAYALAM_FIRST,
    MALAYALAM_FOUNDER,
    MALAYALAM_PRESS_YEAR,
    MASS_MEDIA,
    MEDIA_ABBREV,
    MEDIA_ETHICS,
    MEDIA_FREEDOM,
    MEDIA_REGULATION,
    NEWS_AGENCIES,
    NEWSPAPER_LAYOUT,
    PCI,
    PRESS_LAWS,
    PRINT_HISTORY,
    PRASAR_BHARATI,
    SOCIAL_MEDIA,
    THEORY_MEANING,
    TRP_BARC,
)

DATA_VARS = [
    "COMM_MODELS", "COMM_THEORIES", "THEORY_MEANING", "MALAYALAM_FIRST",
    "MALAYALAM_FOUNDER", "MALAYALAM_PRESS_YEAR", "INDIA_PRESS_HISTORY",
    "INDIA_PRESS_PIONEER", "JOURNALISM_TERMS", "PRESS_LAWS", "PRASAR_BHARATI",
    "PCI", "TRP_BARC", "DIGITAL_MEDIA", "NEWS_AGENCIES", "BROADCAST_TERMS",
    "JOURNALISM_TYPES", "MASS_MEDIA", "ADVERTISING_PR", "MEDIA_FREEDOM",
    "PRINT_HISTORY", "SOCIAL_MEDIA", "MEDIA_ETHICS", "NEWSPAPER_LAYOUT",
    "FILM_MEDIA_BODIES", "KERALA_MEDIA", "MEDIA_ABBREV", "INTERNATIONAL_PRESS",
    "COMM_LEVELS", "MEDIA_REGULATION", "DIRECT_FACTS",
]


def _fmt_list(name: str, rows: list, *, quad: bool = False) -> str:
    if quad:
        type_hint = "list[tuple[str, str, list[str], str]]"
        lines = [f"{name}: {type_hint} = ["]
        for q, a, w, d in rows:
            lines.append(f"    ({q!r}, {a!r}, {w!r}, {d!r}),")
    else:
        lines = [f"{name}: list[tuple[str, str]] = ["]
        for a, b in rows:
            lines.append(f"    ({a!r}, {b!r}),")
    lines.append("]")
    return "\n".join(lines)


def main() -> None:
    import random
    import importlib.util

    parts = [HEADER]
    ns = {
        "COMM_MODELS": COMM_MODELS, "COMM_THEORIES": COMM_THEORIES,
        "THEORY_MEANING": THEORY_MEANING, "MALAYALAM_FIRST": MALAYALAM_FIRST,
        "MALAYALAM_FOUNDER": MALAYALAM_FOUNDER,
        "MALAYALAM_PRESS_YEAR": MALAYALAM_PRESS_YEAR,
        "INDIA_PRESS_HISTORY": INDIA_PRESS_HISTORY,
        "INDIA_PRESS_PIONEER": INDIA_PRESS_PIONEER,
        "JOURNALISM_TERMS": JOURNALISM_TERMS, "PRESS_LAWS": PRESS_LAWS,
        "PRASAR_BHARATI": PRASAR_BHARATI, "PCI": PCI, "TRP_BARC": TRP_BARC,
        "DIGITAL_MEDIA": DIGITAL_MEDIA, "NEWS_AGENCIES": NEWS_AGENCIES,
        "BROADCAST_TERMS": BROADCAST_TERMS, "JOURNALISM_TYPES": JOURNALISM_TYPES,
        "MASS_MEDIA": MASS_MEDIA, "ADVERTISING_PR": ADVERTISING_PR,
        "MEDIA_FREEDOM": MEDIA_FREEDOM, "PRINT_HISTORY": PRINT_HISTORY,
        "SOCIAL_MEDIA": SOCIAL_MEDIA, "MEDIA_ETHICS": MEDIA_ETHICS,
        "NEWSPAPER_LAYOUT": NEWSPAPER_LAYOUT, "FILM_MEDIA_BODIES": FILM_MEDIA_BODIES,
        "KERALA_MEDIA": KERALA_MEDIA, "MEDIA_ABBREV": MEDIA_ABBREV,
        "INTERNATIONAL_PRESS": INTERNATIONAL_PRESS, "COMM_LEVELS": COMM_LEVELS,
        "MEDIA_REGULATION": MEDIA_REGULATION,
    }
    for name in DATA_VARS[:-1]:
        parts.append(_fmt_list(name, ns[name]))
        parts.append("\n")
    parts.append(_fmt_list("DIRECT_FACTS", DIRECT_FACTS, quad=True))
    parts.append("\n")
    parts.append(EMIT)
    OUT.write_text("".join(parts), encoding="utf-8")
    spec = importlib.util.spec_from_file_location("cj_w30", OUT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    n = len(mod.generate_wave30_candidates(set(), random.Random(0)))
    print(f"Wrote {OUT} — {n} candidates")


if __name__ == "__main__":
    main()
