#!/usr/bin/env python3
"""Wave 15 Indian history facts — 15 PSC topic types."""

from __future__ import annotations

import random
import re

from refill_common import Candidate, add_candidate

MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def _pool(items: list[str], correct: str) -> list[str]:
    return [x for x in items if x != correct]


def _add(
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


def _pairs(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    rows: list[tuple[str, str]],
    templates: list[str],
    pool_b: list[str],
    diff: str = "medium",
) -> None:
    for a, b in rows:
        for tmpl in templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b), b, _pool(pool_b, b)[:3], diff, pool_b)


def _pairs_rev(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    rows: list[tuple[str, str]],
    templates: list[str],
    pool_a: list[str],
    diff: str = "medium",
) -> None:
    for a, b in rows:
        for tmpl in templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b), a, _pool(pool_a, a)[:3], diff, pool_a)


def _triples(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    rows: list[tuple[str, str, str]],
    ab_templates: list[str],
    ac_templates: list[str],
    bc_templates: list[str],
    pool_b: list[str],
    pool_c: list[str],
    pool_a: list[str],
    diff: str = "medium",
) -> None:
    for a, b, c in rows:
        for tmpl in ab_templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b, c=c), b, _pool(pool_b, b)[:3], diff, pool_b)
        for tmpl in ac_templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b, c=c), c, _pool(pool_c, c)[:3], diff, pool_c)
        for tmpl in bc_templates:
            _add(out, existing, rng, tmpl.format(a=a, b=b, c=c), a, _pool(pool_a, a)[:3], diff, pool_a)


def _quads(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    rows: list[tuple[str, str, str, str]],
    year_templates: list[str],
    region_templates: list[str],
    leader_templates: list[str],
    name_templates: list[str],
    years: list[str],
    regions: list[str],
    leaders: list[str],
    names: list[str],
    diff: str = "medium",
) -> None:
    for name, year, region, leader in rows:
        for tmpl in year_templates:
            _add(out, existing, rng, tmpl.format(n=name, y=year, r=region, l=leader), year, _pool(years, year)[:3], diff, years)
        for tmpl in region_templates:
            _add(out, existing, rng, tmpl.format(n=name, y=year, r=region, l=leader), region, _pool(regions, region)[:3], diff, regions)
        for tmpl in leader_templates:
            _add(out, existing, rng, tmpl.format(n=name, y=year, r=region, l=leader), leader, _pool(leaders, leader)[:3], diff, leaders)
        for tmpl in name_templates:
            _add(out, existing, rng, tmpl.format(n=name, y=year, r=region, l=leader), name, _pool(names, name)[:3], diff, names)


# 1 — Bhakti / Sufi (saint, movement, region)
from pathlib import Path

_g: dict = {"__file__": str(Path(__file__).parent / "gen_ih15.py")}
exec((Path(__file__).parent / "gen_ih15.py").read_text(encoding="utf-8"), _g)
BHAKTI: list[tuple[str, str, str]] = _g["BHAKTI"]

# 2 — Monuments (name, builder/ruler)
MONUMENTS: list = [('താജ്മഹാല്', 'ഷാജഹാം'),
 ('ചെംകോട്', 'ഷാജഹാം'),
 ('ജാമാ മസ്ജിദ് (ദില്ലി)', 'ഷാജഹാം'),
 ('ദില്ലിവാരാ മസ്ജിദ്', 'ഷാജഹാം'),
 ('ഹുമായൂന്ന്റെ കംതിരം', 'ഹുമായൂന്'),
 ('ഇപുരാണ ഖില്', 'ഹുമായൂന്'),
 ('ഫത്തേഹ്പുര സിക്രീ', 'അക്ഇര'),
 ('ബുലംദ് ദര്വാസം', 'അക്ഇര'),
 ('ഇത്തുംദുല്ലാഹം', 'അക്ഇര'),
 ('ജോധാ ബാഇി കുഴി', 'അക്ഇര'),
 ('ആഗ്ര കോട്', 'അക്ഇര'),
 ('ഇത്താദ്-ഉദ്-ദൌല', 'നൂര് ജഹാം'),
 ('ഷാലിംതാര് ബാഗ് (ശ്രീനഗരം)', 'ജഹാംഗീര'),
 ('ലാല് ഖില്', 'ഷാജഹാം'),
 ('മോതി മസ്ജിദ്', 'ഌറംഗസേബ്'),
 ('ബാദ്ഷാഹി മസ്ജിദ്', 'ഌറംഗസേബ്'),
 ('ബീബി ക മഖ്ബരം', 'ഌറംഗസേബ്'),
 ('ചാര്മിനാര്', 'ഖുലി ആത്തുദ്ദീം ഇയകകകക'),
 ('ഗോല്കോംട് കോട്', 'കാകത്തിയ'),
 ('ഖുതുബ് മീനാര്', 'ആത്തുദ്ദീം ഇയകകകക'),
 ('അലൈ ദര്വാസം', 'അലാവുദ്ദീം ഖില്ജി'),
 ('ഹൌസ് ഖാസ്', 'അലാവുദ്ദീം ഖില്ജി'),
 ('തുഗ്ലഖാബാദ് കോട്', 'ഗിയാസുദ്ദീം തുഗ്ലക്'),
 ('ഫിറോസ് ഷാ തുഗ്ലക് കോട്', 'ഫിറോസ് ഷാ തുഗ്ലക്'),
 ('ഇപുരാണ ഖില് (ദില്ലി)', 'ഷേര് ഷാസാം സൂരീ'),
 ('ഷേര് ഷാസാം സൂരീ സംചിദം', 'ഷേര് ഷാസാം സൂരീ'),
 ('വിരുപാക്ഷ ക്ഷേത്രം', 'വിജയനഗര'),
 ('വിട്ടാല ക്ഷേത്രം', 'വിജയനഗര'),
 ('കോണാര്ക് സൂര്യ ക്ഷേത്രം', 'നരസിംഹംദേവ'),
 ('ഖാജുരാഹോ', 'ചാംഡെല'),
 ('മഹാബോധി ക്ഷേത്രം', 'ഗുപ്തര്'),
 ('സാഞ്ചി സ്തൂപം', 'അശോകം'),
 ('ഇലിഫംടാ ഗുഹകംലം', 'ഇരാഷ്ട്രകൂടംര്'),
 ('അജംത ഗുഹകംലം', 'വാകാടകംര്'),
 ('ഇല്ലോര കൈലാസം', 'ഇരാഷ്ട്രകൂടംര്'),
 ('മീനാക്ഷി ക്ഷേത്രം', 'ഇപാണ്ട്യംര്'),
 ('ബൃഹദീശ്വര ക്ഷേത്രം', 'ഇരാജരാജം ചോലന്'),
 ('ഗംഗൈകംണ്ട ചോലാപുരം', 'ഇരാജംദ്ര ചോലന്'),
 ('ഖുതുബ് ഷാഹി ഷാഹി സംചികംലം', 'ഖുതുബ് ഷാഹി'),
 ('ജംതര് മന്തര് (ജയ്പൂരം)', 'സവാഇീ ജന്സിംഗ്'),
 ('ആംബംര് കോട്', 'കച്ചവാഹ'),
 ('ചിത്തോര്ഗം കോട്', 'സിസോദിയ'),
 ('ഗ്വാലിയംര് കോട്', 'തോംര്'),
 ('നിഷത് ബാഗ്', 'ആസം ഇലിയ'),
 ('മയൂര് സിംഹാസനം', 'ഷാജഹാം'),
 ('സവാഇീ ജസിംഗ് സംചിദം', 'സവാഇീ ജസിംഗ്'),
 ('ജംതര് മന്തര് (ദില്ലി)', 'സവാഇീ ജന്സിംഗ്'),
 ('സിടിി ഇലംം (ജയ്പൂരം)', 'സവാഇീ ജന്സിംഗ്'),
 ('ലിംഗരാജം ക്ഷേത്രം', 'സോംവംശി'),
 ('ഹംപി വിശ്വനാഥ ക്ഷേത്രം', 'വിജയനഗര'),
 ('മീനാക്കി ഗോപുരം', 'നായക്'),
 ('ഹംപി ഇലിഹംതാ ഗുഹം', 'വിജയനഗര'),
 ('താജ്മഹൽ', 'ഷാജഹാൻ'),
 ('ചെങ്കോട്ട', 'ഷാജഹാൻ'),
 ('ജാമാ മസ്ജിദ് (ദില്ലി)', 'ഷാജഹാൻ')]

# 3 — Temple architecture (site, style)
TEMPLE_ARCH: list = [('ഖജുരാഹോ', 'നഗര ശൈലി'),
 ('ബൃഹദീശ്വര ക്ഷേത്രം', 'ദ്രവിഡ ശൈലി'),
 ('കോണാർക്ക് സൂര്യക്ഷേത്രം', 'ദ്രവിഡ ശൈലി'),
 ('ശോർ ക്ഷേത്രം', 'ദ്രവിഡ ശൈലി'),
 ('എലിഫണ്ടാ ഗുഹകൾ', 'ഇരുക്കിയ ശൈലി'),
 ('അജന്താ ഗുഹകൾ', 'ഇരുക്കിയ ശൈലി'),
 ('എല്ലോറ കൈലാസം', 'ഇരുക്കിയ ശൈലി'),
 ('മീനാക്ഷി ക്ഷേത്രം', 'ദ്രവിഡ ശൈലി'),
 ('വിട്ടാല ക്ഷേത്രം', 'വിജയനഗര ശൈലി'),
 ('വിരുപാക്ഷ ക്ഷേത്രം', 'വിജയനഗര ശൈലി'),
 ('ഹംപി വിശ്വനാഥ ക്ഷേത്രം', 'വിജയനഗര ശൈലി'),
 ('ലിംഗരാജ ക്ഷേത്രം', 'നഗര ശൈലി'),
 ('മഹാബാലിപുരം', 'നഗര ശൈലി'),
 ('ഹംപി എലിഫണ്ടാ ഗുഹ', 'ഇരുക്കിയ ശൈലി'),
 ('ഏലോറ ഗുഹകൾ', 'ഇരുക്കിയ ശൈലി'),
 ('കൈലാസം', 'ഇരുക്കിയ ശൈലി'),
 ('തിരുവണ്ണാമലൈ', 'ദ്രവിഡ ശൈലി'),
 ('ശ്രീനഗര ക്ഷേത്രം', 'ദ്രവിഡ ശൈലി'),
 ('മഹാബോധി ക്ഷേത്രം', 'നഗര ശൈലി'),
 ('കാഞ്ചിപുരം ക്ഷേത്രം', 'ദ്രവിഡ ശൈലി'),
 ('ഗംഗൈകൊണ്ട ചോളപുരം', 'ദ്രവിഡ ശൈലി'),
 ('തിരുവണ്ണാമലൈ ക്ഷേത്രം', 'ദ്രവിഡ ശൈലി'),
 ('അരുണാചല ക്ഷേത്രം', 'ദ്രവിഡ ശൈലി'),
 ('പല്ലവ ശൈലി ക്ഷേത്രം', 'ദ്രവിഡ ശൈലി')]

# 4 — Travellers (name, period/ruler)
TRAVELLERS: list = [('ഫാഹ്യൻ', 'ഗുപ്ത കാലഘട്ടം'),
 ('ഹുയൻ സാങ്', 'ഹർഷവർദ്ധനന്റെ കാലം'),
 ('മെഗസ്തനീസ്', 'മൗര്യ കാലം'),
 ('അൽ ബിരൂനി', 'മഹ്മൂദ് കാലം'),
 ('ഇബ്നു ബത്തൂത', 'ദില്ലി സുൽത്താനേറ്റ്'),
 ('മാർക്കോ പോലോ', 'പാണ്ഡ്യ കാലം'),
 ('തോമസ് റോ', 'ജഹാംഗീർ കാലം'),
 ('ഫ്രാൻസിസ് ബെർണർ', 'ഔറംഗസേബ് കാലം'),
 ('ടവർണിയർ', 'ഷാജഹാൻ കാലം'),
 ('നിക്കോലാറു', 'വിജയനഗര കാലം'),
 ('ഡുആര്തെ ബര്ബോസ', 'പോർച്ചുഗീസ് കാലം'),
 ('അബുല ഫാസല', 'അക്ബർ കാലം'),
 ('ബർണിയർ', 'ഷാജഹാൻ കാലം'),
 ('മാനുച്ചി', 'ഔറംഗസേബ് കാലം'),
 ('ഹീനൻ', 'ഹർഷവർദ്ധനന്റെ കാലം')]

# 5 — Newspapers (paper, founder/editor)
NEWSPAPERS: list = [('അമൃതാ ബാസാർ', 'ഇന്ത്യൻ പത്രപ്രവർത്തകർ'),
 ('ദി പയനീർ', 'ഇന്ത്യൻ എക്സ്പ്രസ്'),
 ('ബംഗാൾ ഗസറ്റ്', 'ജെയിംസ് അഗസ്റ്റസ് ഹിക്കി'),
 ('ബോംബെ സമാചാർ', 'ഫർദുൻജി മുർസ്ബാൻ'),
 ('സമാചാർ ദർപ്പൺ', 'മിഷനറി പ്രസിദ്ധീകരണം'),
 ('കേസരി', 'ബാല ഗംഗാധർ തിലക്'),
 ('അമൃത ബാസാർ പത്രിക', 'ഇന്ത്യൻ പത്രപ്രവർത്തകർ'),
 ('ദി ഹിന്ദു', 'ഇന്ത്യൻ പത്രപ്രവർത്തകർ'),
 ('ദി ഇന്ത്യൻ എക്സ്പ്രസ്', 'ഇന്ത്യൻ എക്സ്പ്രസ്'),
 ('ദി സ്റ്റേറ്റ്സ്മാൻ', 'ഇന്ത്യൻ എക്സ്പ്രസ്'),
 ('മഹാത്മ ഗാന്ധി (യംഗ് ഇന്ത്യ)', 'മഹാത്മ ഗാന്ധി'),
 ('യംഗ് ഇന്ത്യ', 'ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ്'),
 ('കേസരി (മഹാരാഷ്ട്ര)', 'ബാല ഗംഗാധർ തിലക്'),
 ('മദ്രാസ് മെയിൽ', 'ഇന്ത്യൻ എക്സ്പ്രസ്'),
 ('ബംഗാൾ ഗസറ്റ് (കൽക്കത്ത)', 'ജെയിംസ് അഗസ്റ്റസ് ഹിക്കി'),
 ('ബോംബെ സമാചാർ (മുംബൈ)', 'ഫർദുൻജി മുർസ്ബാൻ'),
 ('ദി ഹിന്ദു (ചെന്നൈ)', 'ഇന്ത്യൻ പത്രപ്രവർത്തകർ')]

# 6 — Revolts (name, year, region, leader)
REVOLTS: list = [('മുണ്ടാ വിദ്രോഹം', '1899', 'ബീഹാർ', 'ബിർസാ മുണ്ട'),
 ('ചൗരി-ചൗരാ', '1922', 'ഉത്തരപ്രദേശ്', 'മഹാത്മാ ഗാന്ധി'),
 ('വേലു തമ്പി വിദ്രോഹം', '1806', 'തിരുവിതാംകൂർ', 'വേലു തമ്പി'),
 ('പോലിഗർ വിദ്രോഹം', '1799', 'തമിഴ്നാട്', 'വീരപ്പൻ'),
 ('സാന്താൽ വിദ്രോഹം', '1855', 'ബംഗാൾ', 'സിദു-കാനു'),
 ('ഇൽത്തിഫാദ്', '1859', 'ബംഗാൾ', 'ദിഗംബർ'),
 ('കിസാൻ സഭ', '1936', 'ഉത്തരപ്രദേശ്', 'സ്വാമി സഹജാനന്ദ'),
 ('അഹോം revolt', '1826', 'അസം', 'ഗംഭിർ'),
 ('1857 വിപ്ലവം', '1857', 'ഉത്തരപ്രദേശം', 'ബഹാദൂർ ഷാ രണ്ടാം'),
 ('ഇന്ദിഗോ വിപ്ലവം', '1859', 'ബംഗാളം', 'ഇന്ത കഷിഷംകംരം'),
 ('ദക്കൻ കലാപം', '1875', 'മഹാരാഷ്ട്ര', 'ഡിക്കംകംരം'),
 ('ചമ്പാരൺ സത്യാഗ്രഹം', '1917', 'ബീഹാര്', 'മഹാതാ ഗാന്ധീ'),
 ('സർദാർ സർഹാദ്', '1928', 'ബീഹാര്', 'മഹാതാ ഗാന്ധീ'),
 ('സന്യാസി കലാപം', '1770', 'ബംഗാളം', 'സന്യാസികംലം'),
 ('പഗൽപന്തി കലാപം', '1820', 'ബംഗാളം', 'ഇപിംപം'),
 ('വഹാബി പ്രസ്ഥാനം', '1830', 'ബംഗാളം', 'വഹാബികംലം'),
 ('തീതു മീര് കലാപം', '1857', 'പാഞ്ചാബ്', 'തീതു മീര്'),
 ('നാനാ സാഹിബ്', '1857', 'ഉത്തരപ്രദേശം', 'നാനാ സാഹംബം'),
 ('കുംവരി സിംഹം', '1857', 'ഉത്തരപ്രദേശം', 'കുംവരി സിംഹം'),
 ('സന്താൽ കലാപം', '1855', 'ബംഗാളം', 'സിദ്ദു-കാനു'),
 ('സവർണ കലാപം', '1920', 'ബീഹാര്', 'മഹാതാ ഗാന്ധീ'),
 ('രാണീ ലക്ഷംയം', '1857', 'രാജസ്ഥാന്', 'രാണീ ലക്ഷംയം'),
 ('പോലിഗർ കലാപം', '1799', 'തമിള്നാട്', 'വീരംപ്പം')]

# 7 — Land revenue (system, ruler/period)
LAND_REVENUE: list = [('സ്ഥിര നികുതി', 'കോര്ന്വാലിസം'),
 ('റയത്ത്വാരി', 'തോംസ മുന്രം'),
 ('മഹൽവാരി', 'ഹോല്ട് മക്കെന്സം'),
 ('സാബ്ത്', 'അക്ഇര'),
 ('ഇക്ത', 'ദില്ലി സുല്താനെട്'),
 ('ഖുദ്കാഷ', 'അക്ഇര'),
 ('പാനി വ്യവസ്ഥ', 'ബ്രിട്ടീഷ് കാലം')]

# 8 — Mughal administration (term, meaning)
MUGHAL_ADMIN: list = [('മൻസബ്ദാരി', 'അക്ഇര'),
 ('ജാഗീർ', 'മുഘല സാംരാജ്ജ്യം'),
 ('സാത്ത്', 'മന്സംദാരി രാംക്'),
 ('സവാർ', 'കുഴി സംംനം'),
 ('ദിവാൻ', 'ഇനംതുംതംവിസ്രെസം'),
 ('സുബ', 'ഇത്താദേശം'),
 ('ഫൗജ്ദാർ', 'ജില്ലാ സൈനിക അധികാരി'),
 ('മിർസ', 'ഉന്നത ഭരണഘടകം'),
 ('വകീൽ', 'ചക്രവർത്തിയുടെ പ്രതിനിദി'),
 ('ജാഗീർ (മുഗൾ)', 'മുഘല സാംരാജ്ജ്യം'),
 ('മൻസബ്ദാരി (അക്ബർ)', 'അക്ഇര')]

# 9 — Coins (coin, period/ruler)
COINS: list = [('മുഹൂർ', 'മുഘല സാംരാജ്ജ്യം'),
 ('രൂപയ', 'ഷേര് ഷാസാ'),
 ('പഞ്ചമർക്ക് നാണയം', 'ജനംപദ'),
 ('ഗുപ്ത സ്വർണ്ണ നാണയം', 'ചന്ദ്രഗുഇത'),
 ('ദീനാർ', 'ഗുപ്തര്'),
 ('കാസു', 'വിജയനഗര'),
 ('ഹോൺസ്', 'വിജയനഗര'),
 ('രൂപയ (ഷെർഷാ)', 'ഷേര് ഷാസാ'),
 ('മുഹൂർ (മുഗൾ)', 'മുഘല സാംരാജ്ജ്യം'),
 ('പഞ്ചമർക്ക് (ജനംപദ)', 'ജനംപദ'),
 ('സ്വർണ്ണ നാണയം (ഗുപ്ത)', 'ചന്ദ്രഗുഇത'),
 ('ദീനാർ (ഗുപ്ത)', 'ഗുപ്തര്')]

# 10 — European factories (company, port/city)
EURO_FACTORIES: list = [('ഇംഗ്ലീഷ് കമ്പനി', 'സുരത്'),
 ('ഡച്ച് കമ്പനി', 'ഇലികുലിക്ടം'),
 ('ഫ്രഞ്ച് കമ്പനി', 'ഇപംതിസേരി'),
 ('പോർച്ചുഗീസ് കമ്പനി', 'ഗൊവ'),
 ('ഡാൻിഷ് കമ്പനി', 'താരംഗംംം'),
 ('ഇംഗ്ലീഷ് (മദ്രാസ)', 'മദ്രാസ്'),
 ('ഡച്ച് (കൊച്ചി)', 'കൊച്ചി'),
 ('ഫ്രഞ്ച് (പോണ്ടിച്ചേരി)', 'ഇപംതിസേരി'),
 ('പോർച്ചുഗീസ് (കൊച്ചി)', 'കൊച്ചി'),
 ('ഇംഗ്ലീഷ് (കൽക്കത്ത)', 'കല്കത്ത'),
 ('ഡച്ചം (നാഗംപിട്ടിനം)', 'നാഗംപിട്ടിനം'),
 ('ഇംഗ്ലീഷ് (സുരത്)', 'സുരത്')]

# 11 — Reformers (person, movement/org)
REFORMERS: list = [('രാജാ രാം മോഹൻ രായ്', 'ബ്രഹ്മോ സമാജം'),
 ('ദയാനന്ദ സരസ്വതി', 'ആര്യ സമാജം'),
 ('സ്വാമി വിവേകാനന്ദ', 'രാമകൃഷ്ണ മഠം'),
 ('ബാല ഗംഗാധർ തിലക്', 'ഹോം റുൾ'),
 ('ഇശ്വര ചന്ദ്ര വിദ്യാസാഗർ', 'വിധവാ വിവാഹ പരിഷ്കാരം'),
 ('ജ്യോതിബാ ഫുലേ', 'സതി നിരോധനം'),
 ('ഗോപാൽ കൃഷ്ണ ഗോഖലെ', 'ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ്'),
 ('കേശവ ചന്ദ്ര സെൻ', 'ബ്രഹ്മോ സമാജം'),
 ('ആന്നി ബെസന്റ്', 'ഹോം റുൾ'),
 ('പംഡിതാ രമാബായി', 'സ്ത്രീ വിദ്യാഭ്യാസം'),
 ('സർദാർ പട്ടേൽ', 'ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ്'),
 ('ഹരിദാസ്', 'ഭക്തി പ്രസ്ഥാനം')]

# 12 — Indus Valley (site/artifact, fact)
INDUS: list = [('മോഹഞ്ചദാരോ', 'സിന്ധു നഗരം'),
 ('ഹര്സം', 'പഞ്ചാബ് സ്ഥലം'),
 ('ലൊത്തം', 'ബندر കടലിടുക്ക്'),
 ('കാലിബംഗനം', 'രാജസ്ഥാൻ സ്ഥലം'),
 ('ഇതംലവീര', 'സിന്ധു നഗരം'),
 ('ഗ്രുത സനനാനം', 'മൊഹംന്രം'),
 ('നാനം പെണുക്പുടി', 'ഇതംക്രം'),
 ('ഇതംകുതി', 'ശിവനനു'),
 ('ഇതംകുരം', 'ഇലകംണ'),
 ('രൊകിഗീരീ', 'ഹരിയാണം'),
 ('ഇതംകുതി', 'ഇതംകുതി')]

# 13 — Sangam literature (work, description)
SANGAM: list = [('തൊല്കിത്യിം', 'സാംഗം വ്യാകരണം'),
 ('സില്ലതികിതികംരം', 'സാംഗം കൃതി'),
 ('ഇന്രികുളം', 'മുപ്പത്തിമൂന്ന് കാവിതകൾ'),
 ('തിരുവാതികിം', 'സാംഗം കൃതി'),
 ('ഇസ്വരം', 'സാംഗം കൃതി'),
 ('പരിപാടലം', 'സാംഗം കൃതി'),
 ('അഗത്തികംരം', 'സാംഗം കൃതി'),
 ('ഇന്രികുളം (ഇന്ത)', 'എട്ട് കാവിതകൾ'),
 ('തിരുവാതികിം (ഇന്ത)', 'സാംഗം കൃതി'),
 ('സില്ലതികിതികംരം (ഇന്ത)', 'സാംഗം കൃതി')]

# 14 — Foreign policy (event/treaty, fact)
FOREIGN_POLICY: list = [('താഷ്കന്റ് ഉടമ്പടി', '1966'),
 ('ഷിംല ഉടമ്പടി', '1972'),
 ('പഞ്ചശീൽ ഉടമ്പടി', '1954'),
 ('SAARC', '1985'),
 ('ലാഹോർ ഉടമ്പടി', '1999'),
 ('ഇന്ത്യ-ചൈന യുദ്ധം', '1962'),
 ('കാർഗിൽ യുദ്ധം', '1999'),
 ('പുരന്ദർ ഉടമ്പടി', 'അംഗലോ-മറാത്ത സന്ധി'),
 ('കർണാടക യുദ്ധങ്ങൾ', 'ഇംഗ്ലീഷ്-ഫ്രഞ്ച്'),
 ('സഹായക ഗഠനാപരിപാടി', '1798'),
 ('ലാപ്സ് നയം', '1848'),
 ('ഡിപ്പിക് സന്ധി', '1761'),
 ('പ്ലാസി യുദ്ധം', '1757'),
 ('ബക്സർ യുദ്ധം', '1764'),
 ('വസായ് സന്ധി', '1775'),
 ('വൈസ്രോയ് നയം', '1823'),
 ('മക്തിവാഹിനി', '1857'),
 ('അംഗലോ-മറാത്ത ഉടമ്പടി', '1802'),
 ('ഇന്ത്യൻ നാവിക സേന', '1830')]

# 15 — Match pairs (entity, fact)
MATCH_ROWS: list = [('താജ്മഹാല്', 'ഷാജഹാം'),
 ('ചെംകോട്', 'ഷാജഹാം'),
 ('ജാമാ മസ്ജിദ് (ദില്ലി)', 'ഷാജഹാം'),
 ('ദില്ലിവാരാ മസ്ജിദ്', 'ഷാജഹാം'),
 ('ഹുമായൂന്ന്റെ കംതിരം', 'ഹുമായൂന്'),
 ('ഇപുരാണ ഖില്', 'ഹുമായൂന്'),
 ('ഫത്തേഹ്പുര സിക്രീ', 'അക്ഇര'),
 ('ബുലംദ് ദര്വാസം', 'അക്ഇര'),
 ('ഇത്തുംദുല്ലാഹം', 'അക്ഇര'),
 ('ജോധാ ബാഇി കുഴി', 'അക്ഇര'),
 ('ആഗ്ര കോട്', 'അക്ഇര'),
 ('ഇത്താദ്-ഉദ്-ദൌല', 'നൂര് ജഹാം'),
 ('ഫാഹ്യൻ', 'ഗുപ്ത കാലഘട്ടം'),
 ('ഹുയൻ സാങ്', 'ഹർഷവർദ്ധനന്റെ കാലം'),
 ('മെഗസ്തനീസ്', 'മൗര്യ കാലം'),
 ('അൽ ബിരൂനി', 'മഹ്മൂദ് കാലം'),
 ('ഇബ്നു ബത്തൂത', 'ദില്ലി സുൽത്താനേറ്റ്'),
 ('മാർക്കോ പോലോ', 'പാണ്ഡ്യ കാലം'),
 ('തോമസ് റോ', 'ജഹാംഗീർ കാലം'),
 ('ഫ്രാൻസിസ് ബെർണർ', 'ഔറംഗസേബ് കാലം'),
 ('ടവർണിയർ', 'ഷാജഹാൻ കാലം'),
 ('നിക്കോലാറു', 'വിജയനഗര കാലം'),
 ('ഡുആര്തെ ബര്ബോസ', 'പോർച്ചുഗീസ് കാലം'),
 ('അബുല ഫാസല', 'അക്ബർ കാലം'),
 ('അമൃതാ ബാസാർ', 'ഇന്ത്യൻ പത്രപ്രവർത്തകർ'),
 ('ദി പയനീർ', 'ഇന്ത്യൻ എക്സ്പ്രസ്'),
 ('ബംഗാൾ ഗസറ്റ്', 'ജെയിംസ് അഗസ്റ്റസ് ഹിക്കി'),
 ('ബോംബെ സമാചാർ', 'ഫർദുൻജി മുർസ്ബാൻ'),
 ('സമാചാർ ദർപ്പൺ', 'മിഷനറി പ്രസിദ്ധീകരണം'),
 ('കേസരി', 'ബാല ഗംഗാധർ തിലക്'),
 ('അമൃത ബാസാർ പത്രിക', 'ഇന്ത്യൻ പത്രപ്രവർത്തകർ'),
 ('ദി ഹിന്ദു', 'ഇന്ത്യൻ പത്രപ്രവർത്തകർ'),
 ('ദി ഇന്ത്യൻ എക്സ്പ്രസ്', 'ഇന്ത്യൻ എക്സ്പ്രസ്'),
 ('ദി സ്റ്റേറ്റ്സ്മാൻ', 'ഇന്ത്യൻ എക്സ്പ്രസ്'),
 ('മഹാത്മ ഗാന്ധി (യംഗ് ഇന്ത്യ)', 'മഹാത്മ ഗാന്ധി'),
 ('യംഗ് ഇന്ത്യ', 'ഇന്ത്യൻ നാഷണൽ കോൺഗ്രസ്'),
 ('മുഹൂർ', 'മുഘല സാംരാജ്ജ്യം'),
 ('രൂപയ', 'ഷേര് ഷാസാ'),
 ('പഞ്ചമർക്ക് നാണയം', 'ജനംപദ'),
 ('ഗുപ്ത സ്വർണ്ണ നാണയം', 'ചന്ദ്രഗുഇത'),
 ('ദീനാർ', 'ഗുപ്തര്'),
 ('കാസു', 'വിജയനഗര'),
 ('ഹോൺസ്', 'വിജയനഗര'),
 ('രൂപയ (ഷെർഷാ)', 'ഷേര് ഷാസാ'),
 ('മുഹൂർ (മുഗൾ)', 'മുഘല സാംരാജ്ജ്യം'),
 ('പഞ്ചമർക്ക് (ജനംപദ)', 'ജനംപദ'),
 ('സ്വർണ്ണ നാണയം (ഗുപ്ത)', 'ചന്ദ്രഗുഇത'),
 ('ദീനാർ (ഗുപ്ത)', 'ഗുപ്തര്')]



def _match_pairs(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    rows: list[tuple[str, str]],
    templates: list[str],
    diff: str = "medium",
) -> None:
    pool = [f"{a} — {b}" for a, b in rows]
    for a, b in rows:
        correct = f"{a} — {b}"
        for tmpl in templates:
            _add(
                out,
                existing,
                rng,
                tmpl.format(a=a, b=b, m=correct),
                correct,
                _pool(pool, correct)[:3],
                diff,
                pool,
            )


def generate_wave15_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []

    saints = list({a for a, _, _ in BHAKTI})
    movements = list({b for _, b, _ in BHAKTI})
    regions = list({c for _, _, c in BHAKTI})
    _triples(
        out,
        existing,
        rng,
        BHAKTI,
        [
            "'{a}' ഏത് ഭക്തി/സൂഫി പ്രസ്ഥാനവുമായി ബന്ധപ്പെട്ട സന്തനാണ്?",
            "'{a}'-ന്റെ പ്രസ്ഥാനം ഏത്?",
            "'{a}' ഏത് ആത്മീയ പരമ്പരയുമായി അറിയപ്പെടുന്നു?",
            "'{b}' പ്രസ്ഥാനവുമായി ബന്ധപ്പെട്ട പ്രധാന വ്യക്തി?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സന്തൻ?",
            "'{a}' ഏത് '{b}' പ്രസ്ഥാനവുമായി ബന്ധപ്പെട്ട്?",
            "'{b}'-യുടെ പ്രതിനിധി '{a}'?",
        ],
        [
            "'{a}' പ്രധാനമായി ഏത് പ്രദേശവുമായി ബന്ധപ്പെട്ട് പ്രവർത്തിച്ചു?",
            "'{a}'-ന്റെ പ്രവർത്തന കേന്ദ്രം?",
            "'{c}' പ്രദേശവുമായി ബന്ധപ്പെട്ട സന്തൻ?",
            "'{c}'-ൽ പ്രധാനമായി പ്രവർത്തിച്ച സന്തൻ?",
        ],
        [
            "'{b}' പ്രസ്ഥാനം '{c}'-ൽ പ്രവർത്തിച്ച പ്രധാന വ്യക്തി?",
            "'{c}'-ലെ '{b}' പ്രസ്ഥാനത്തിന്റെ പ്രതിനിധി?",
            "'{b}'-യുമായി '{c}'-ൽ ബന്ധപ്പെട്ട സന്തൻ?",
            "'{c}' പ്രദേശവുമായി '{b}'-യുമായി ബന്ധപ്പെട്ട സന്തൻ?",
        ],
        movements,
        regions,
        saints,
    )

    builders = list({b for _, b in MONUMENTS})
    monuments = list({a for a, _ in MONUMENTS})
    _pairs(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{a}' നിർമ്മിച്ചത് ആർ?",
            "'{a}'-ന്റെ നിർമ്മാതാവ്/രാജാവ്?",
            "'{a}' നിർമ്മാണവുമായി ബന്ധപ്പെട്ട വ്യക്തി?",
            "'{a}' സ്ഥാപിച്ച/നിർമ്മിച്ച ഭരണാധികാരി?",
            "'{a}'-ന്റെ പിൻബലത്തിൽ നിർമ്മിച്ചത്?",
            "'{a}' നിർമ്മിച്ച പ്രധാന വ്യക്തി?",
            "'{a}'-ന്റെ നിർമ്മാതാവ് ആർ?",
            "'{a}'-യുടെ രചയിതാവ്/നിർമ്മാതാവ്?",
            "'{a}' ആരുടെ കാലത്ത് നിർമ്മിച്ചത്?",
        ],
        builders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{b}' നിർമ്മിച്ച പ്രധാന നിർമ്മാണം?",
            "'{b}'-ന്റെ കാലത്ത് നിർമ്മിച്ച പ്രശസ്ത സ്മാരകം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണം?",
            "'{b}' നിർമ്മിച്ച/കമാൻഡ് ചെയ്ത സ്മാരകം?",
            "'{b}'-ന്റെ പേരിലുള്ള പ്രധാന നിർമ്മാണം?",
        ],
        monuments,
    )

    styles = list({b for _, b in TEMPLE_ARCH})
    temples = list({a for a, _ in TEMPLE_ARCH})
    _pairs(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{a}' ഏത് ശില്പശൈലിയിലാണ്?",
            "'{a}'-ന്റെ വാസ്തുവിദ്യാ ശൈലി?",
            "'{a}' ഏത് നിർമ്മാണശൈലിയിൽ പണിതം?",
            "'{a}'-ന്റെ ശില്പശൈലി?",
            "'{a}' ഏത് ശൈലിയുടെ ഉദാഹരണമാണ്?",
        ],
        styles,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{b}' ശൈലിയിലെ പ്രധാന ഉദാഹരണം?",
            "'{b}'-യുടെ പ്രതിനിധി നിർമ്മാണം?",
            "'{b}' ശൈലിയിൽ പണിത പ്രശസ്ത ക്ഷേത്രം/നിർമ്മാണം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണം?",
        ],
        temples,
    )

    periods = list({b for _, b in TRAVELLERS})
    travellers = list({a for a, _ in TRAVELLERS})
    _pairs(
        out,
        existing,
        rng,
        TRAVELLERS,
        [
            "'{a}' ഏത് കാലഘട്ടവുമായി ബന്ധപ്പെട്ട് ഇന്ത്യ സന്ദർശിച്ചു?",
            "'{a}'-ന്റെ സഞ്ചാര കാലഘട്ടം/ഭരണകാലം?",
            "'{a}' ഇന്ത്യയിൽ എപ്പോൾ/ഏത് കാലത്ത്?",
            "'{a}'-ന്റെ ഇന്ത്യാ സന്ദർശനവുമായി ബന്ധപ്പെട്ട കാലം?",
        ],
        periods,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TRAVELLERS,
        [
            "'{b}' കാലഘട്ടത്തിൽ ഇന്ത്യ സന്ദർശിച്ച പ്രശസ്ത സഞ്ചാരി?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട് ഇന്ത്യ സന്ദർശിച്ചയാൾ?",
            "'{b}'-ൽ സന്ദർശിച്ച പ്രശസ്ത വ്യക്തി?",
        ],
        travellers,
    )

    founders = list({b for _, b in NEWSPAPERS})
    papers = list({a for a, _ in NEWSPAPERS})
    _pairs(
        out,
        existing,
        rng,
        NEWSPAPERS,
        [
            "'{a}' ആരംഭിച്ചത്/പ്രസിദ്ധീകരിച്ചത് ആർ?",
            "'{a}'-ന്റെ സ്ഥാപകൻ/പ്രസിദ്ധീകരണ ഉത്തരവാദി?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി?",
            "'{a}' ആരുടെ പേരിലാണ്?",
        ],
        founders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        NEWSPAPERS,
        [
            "'{b}' ആരംഭിച്ച/പ്രസിദ്ധീകരിച്ച പത്രം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പത്രം?",
            "'{b}'-ന്റെ പേരിലുള്ള പ്രസിദ്ധ പത്രം?",
        ],
        papers,
    )

    years = list({y for _, y, _, _ in REVOLTS})
    rev_regions = list({r for _, _, r, _ in REVOLTS})
    leaders = list({l for _, _, _, l in REVOLTS})
    names = list({n for n, _, _, _ in REVOLTS})
    _quads(
        out,
        existing,
        rng,
        REVOLTS,
        [
            "'{n}' സംഭവിച്ച വർഷം?",
            "'{n}'-ന്റെ പ്രധാന വർഷം?",
            "'{n}'-യുമായി ബന്ധപ്പെട്ട വർഷം?",
        ],
        [
            "'{n}' പ്രധാനമായി ഏത് പ്രദേശത്ത്?",
            "'{n}'-ന്റെ പ്രധാന പ്രദേശം?",
            "'{n}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം?",
        ],
        [
            "'{n}'-ന്റെ നേതാവ്/പ്രധാന വ്യക്തി?",
            "'{n}'-യുമായി ബന്ധപ്പെട്ട നേതാവ്?",
            "'{n}' നയിച്ച/നേതൃത്വം നൽകിയ വ്യക്തി?",
        ],
        [
            "'{l}' നേതൃത്വം നൽകിയ/ബന്ധപ്പെട്ട സംഘടന/സമരം?",
            "'{l}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന സമരം?",
            "'{r}'-ൽ '{l}'-യുമായി ബന്ധപ്പെട്ട സംഘടന?",
        ],
        years,
        rev_regions,
        leaders,
        names,
    )

    lr_terms = list({a for a, _ in LAND_REVENUE})
    lr_facts = list({b for _, b in LAND_REVENUE})
    _pairs(
        out,
        existing,
        rng,
        LAND_REVENUE,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി/കാലം?",
            "'{a}' ആരംഭിച്ച/നടപ്പാക്കിയത്?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
        ],
        lr_facts,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        LAND_REVENUE,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നികുതി/വ്യവസ്ഥ?",
            "'{b}'-ന്റെ പേരിലുള്ള നികുതി വ്യവസ്ഥ?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നികുതി/വ്യവസ്ഥ?",
        ],
        lr_terms,
    )

    ma_terms = list({a for a, _ in MUGHAL_ADMIN})
    ma_facts = list({b for _, b in MUGHAL_ADMIN})
    _pairs(
        out,
        existing,
        rng,
        MUGHAL_ADMIN,
        [
            "'{a}'-ന്റെ അർത്ഥം/വിവരണം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
            "'{a}' എന്തിനെ/ആരെ സൂചിപ്പിക്കുന്നു?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം?",
        ],
        ma_facts,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        MUGHAL_ADMIN,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ഭരണപദം?",
            "'{b}'-ന്റെ പേരിലുള്ള മുഗൾ ഭരണപദം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പദം?",
        ],
        ma_terms,
    )

    coin_names = list({a for a, _ in COINS})
    coin_facts = list({b for _, b in COINS})
    _pairs(
        out,
        existing,
        rng,
        COINS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട കാലം/ഭരണാധികാരി?",
            "'{a}' ഏത് കാലത്ത്/ആരുടെ കാലത്ത്?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം?",
        ],
        coin_facts,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        COINS,
        [
            "'{b}'-ന്റെ കാലത്ത്/പേരിലുള്ള നാണയം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നാണയം?",
        ],
        coin_names,
    )

    places = list({b for _, b in EURO_FACTORIES})
    companies = list({a for a, _ in EURO_FACTORIES})
    _pairs(
        out,
        existing,
        rng,
        EURO_FACTORIES,
        [
            "'{a}'-ന്റെ പ്രധാന ചരക്ക്/വ്യാപാര കേന്ദ്രം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട തുറമുഖ/നഗരം?",
            "'{a}'-ന്റെ പ്രധാന കച്ചവട കേന്ദ്രം?",
        ],
        places,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        EURO_FACTORIES,
        [
            "'{b}'-ൽ സ്ഥാപിച്ച/പ്രവർത്തിച്ച യൂറോപ്യൻ കമ്പനി?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട കച്ചവട കമ്പനി?",
        ],
        companies,
    )

    works = list({b for _, b in REFORMERS})
    reformers = list({a for a, _ in REFORMERS})
    _pairs(
        out,
        existing,
        rng,
        REFORMERS,
        [
            "'{a}'-ന്റെ പ്രധാന പ്രസ്ഥാനം/സംഘടന?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട സാമൂഹിക/മതപരിഷ്കരണ പ്രസ്ഥാനം?",
            "'{a}'-ന്റെ പ്രധാന സംഭാവന?",
        ],
        works,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        REFORMERS,
        [
            "'{b}'-ന്റെ സ്ഥാപകൻ/പ്രധാന വ്യക്തി?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പരിഷ്കരണവാദി?",
        ],
        reformers,
    )

    indus_sites = list({a for a, _ in INDUS})
    indus_facts = list({b for _, b in INDUS})
    _pairs(
        out,
        existing,
        rng,
        INDUS,
        [
            "'{a}'-ന്റെ പ്രധാന സവിശേഷത/വിവരണം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
            "'{a}' എന്തിനെ/എന്തിനെ സൂചിപ്പിക്കുന്നു?",
        ],
        indus_facts,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        INDUS,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സിന്ധു സംസ്കാര സ്ഥലം/കണ്ടെത്തൽ?",
            "'{b}'-ന്റെ പേരിലുള്ള സിന്ധു സംസ്കാര വസ്തു/സ്ഥലം?",
        ],
        indus_sites,
    )

    sangam_works = list({a for a, _ in SANGAM})
    sangam_facts = list({b for _, b in SANGAM})
    _pairs(
        out,
        existing,
        rng,
        SANGAM,
        [
            "'{a}'-ന്റെ പ്രധാന സവിശേഷത/രചയിതാവ്?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വിവരണം?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം?",
        ],
        sangam_facts,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        SANGAM,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സംഗം കൃതി?",
            "'{b}'-ന്റെ പേരിലുള്ള സാഹിത്യ കൃതി?",
        ],
        sangam_works,
    )

    fp_events = list({a for a, _ in FOREIGN_POLICY})
    fp_facts = list({b for _, b in FOREIGN_POLICY})
    _pairs(
        out,
        existing,
        rng,
        FOREIGN_POLICY,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി/രാജ്യം?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
        ],
        fp_facts,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        FOREIGN_POLICY,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ഉടമ്പടി/നയം?",
            "'{b}'-ന്റെ പേരിലുള്ള നയം/സംഭവം?",
        ],
        fp_events,
    )

    _match_pairs(
        out,
        existing,
        rng,
        MATCH_ROWS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ശരിയായ ജോഡി?",
            "താഴെ കൊടുത്തിരിക്കുന്നവയിൽ '{a}'-ന്റെ ശരിയായ ജോഡി?",
            "'{a}' — ഏത്?",
            "ശരിയായ ജോഡി '{a}' — ?",
            "'{a}'-ന് അനുയോജ്യമായ വിവരണം?",
            "'{a}'-യുടെ ശരിയായ വിവരണം?",
        ],
    )

    _wave15_extra(out, existing, rng)
    _wave15_more(out, existing, rng)
    _wave15_wave4(out, existing, rng)

    return out


def _wave15_wave4(out: list[Candidate], existing: set[str], rng: random.Random) -> None:
    """Fourth template pass — distinct stems for pool depth."""
    saints = list({a for a, _, _ in BHAKTI})
    movements = list({b for _, b, _ in BHAKTI})
    regions = list({c for _, _, c in BHAKTI})
    _triples(
        out,
        existing,
        rng,
        BHAKTI,
        [
            "ഭക്തി/സൂഫി ചരിത്രത്തിൽ '{a}'-ന്റെ പ്രസ്ഥാനം?",
            "'{a}' ഏത് ആത്മീയ പരമ്പരയുമായി ബന്ധപ്പെട്ട്?",
            "'{b}' പ്രസ്ഥാനത്തിന്റെ പ്രധാന സന്ത് '{a}'?",
        ],
        [
            "'{a}' പ്രധാനമായി പ്രവർത്തിച്ച പ്രദേശം?",
            "സന്ത് '{a}'-ന്റെ പ്രവർത്തന കേന്ദ്രം?",
            "'{c}'-യുമായി '{a}'-യെ ബന്ധിപ്പിക്കാം?",
        ],
        [
            "'{c}' പ്രദേശത്ത് '{b}' പ്രസ്ഥാനവുമായി ബന്ധപ്പെട്ടവർ?",
            "'{b}' '{c}'-ൽ പ്രചരിച്ച പ്രധാന വ്യക്തി?",
        ],
        movements,
        regions,
        saints,
    )

    builders = list({b for _, b in MONUMENTS})
    monuments = list({a for a, _ in MONUMENTS})
    _pairs(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "പ്രസിദ്ധ നിർമ്മാണം '{a}' നിർമ്മിച്ചത്?",
            "'{a}' ആരുടെ/ഏത് ഭരണാധികാരിയുടെ കാലത്ത് പണിതം?",
            "ചരിത്ര സ്മാരകം '{a}'-ന്റെ നിർമ്മാതാവ്?",
        ],
        builders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{b}' നിർമ്മിച്ച/കമാൻഡ് ചെയ്ത പ്രസിദ്ധ സ്മാരകം?",
            "'{b}'-യുടെ പേരിൽ അറിയപ്പെടുന്ന നിർമ്മാണം?",
        ],
        monuments,
    )

    styles = list({b for _, b in TEMPLE_ARCH})
    temples = list({a for a, _ in TEMPLE_ARCH})
    _pairs(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{a}' ഏത് വാസ്തുവിദ്യാ/ശില്പശൈലിയിൽ പെടുന്നു?",
            "നിർമ്മാണം '{a}'-ന്റെ ശൈലി?",
        ],
        styles,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{b}' ശൈലിയുടെ ഉദാഹരണമായി '{a}'?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ക്ഷേത്ര/ഗുഹ?",
        ],
        temples,
    )

    periods = list({b for _, b in TRAVELLERS})
    travellers = list({a for a, _ in TRAVELLERS})
    _pairs(
        out,
        existing,
        rng,
        TRAVELLERS,
        [
            "വിദേശ യാത്രികൻ '{a}' ഇന്ത്യ സന്ദർശിച്ച കാലം?",
            "'{a}'-ന്റെ ഇന്ത്യാ സന്ദർശനം ഏത് കാലഘട്ടവുമായി?",
        ],
        periods,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TRAVELLERS,
        [
            "'{b}' കാലത്ത് ഇന്ത്യ സന്ദർശിച്ച പ്രശസ്ത യാത്രികൻ?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട വിദേശ യാത്രികൻ?",
        ],
        travellers,
    )

    founders = list({b for _, b in NEWSPAPERS})
    papers = list({a for a, _ in NEWSPAPERS})
    _pairs(
        out,
        existing,
        rng,
        NEWSPAPERS,
        [
            "പത്രം '{a}' ആരാണ് ആരംഭിച്ചത്?",
            "'{a}'-യുടെ സ്ഥാപകൻ/പ്രസിദ്ധീകരണ ഉത്തരവാദി?",
        ],
        founders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        NEWSPAPERS,
        [
            "'{b}' ആരംഭിച്ച/പ്രസിദ്ധീകരിച്ച പത്രം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പത്രപ്രസിദ്ധീകരണം?",
        ],
        papers,
    )

    years = list({y for _, y, _, _ in REVOLTS})
    rev_regions = list({r for _, _, r, _ in REVOLTS})
    leaders = list({l for _, _, _, l in REVOLTS})
    names = list({n for n, _, _, _ in REVOLTS})
    _quads(
        out,
        existing,
        rng,
        REVOLTS,
        ["'{n}' നടന്ന/ആരംഭിച്ച വർഷം?", "'{n}'-യുമായി ബന്ധപ്പെട്ട വർഷം?"],
        ["'{n}' പ്രധാനമായി നടന്ന പ്രദേശം?", "'{n}'-യുടെ പ്രദേശം?"],
        ["'{n}'-യുടെ നേതാവ്/പ്രധാന വ്യക്തി?", "'{n}'-യുമായി ബന്ധപ്പെട്ട നേതാവ്?"],
        ["'{l}' നേതൃത്വം നൽകിയ സമരം/സംഘടന?", "'{l}'-യുമായി ബന്ധപ്പെട്ട വിദ്രോഹം?"],
        years,
        rev_regions,
        leaders,
        names,
    )

    for rows, pool_b, pool_a, fwd, rev in (
        (LAND_REVENUE, [b for _, b in LAND_REVENUE], [a for a, _ in LAND_REVENUE],
         "'{a}'-യുമായി ബന്ധപ്പെട്ട നികുതി/ഭൂമി വ്യവസ്ഥ?", "'{b}'-യുമായി ബന്ധപ്പെട്ട നികുതി പദം?"),
        (MUGHAL_ADMIN, [b for _, b in MUGHAL_ADMIN], [a for a, _ in MUGHAL_ADMIN],
         "മുഗൾ ഭരണപദം '{a}'-ന്റെ അർത്ഥം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട ഭരണപദം?"),
        (COINS, [b for _, b in COINS], [a for a, _ in COINS],
         "'{a}'-യുമായി ബന്ധപ്പെട്ട നാണയ/കാലം?", "'{b}'-ന്റെ കാലത്തെ നാണയം?"),
        (EURO_FACTORIES, [b for _, b in EURO_FACTORIES], [a for a, _ in EURO_FACTORIES],
         "'{a}'-ന്റെ പ്രധാന കച്ചവട/തുറമുഖ കേന്ദ്രം?", "'{b}'-യിലെ യൂറോപ്യൻ കച്ചവട കമ്പനി?"),
        (REFORMERS, [b for _, b in REFORMERS], [a for a, _ in REFORMERS],
         "സാമൂഹിക/മതപരിഷ്കരണവാദി '{a}'-ന്റെ പ്രസ്ഥാനം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട പരിഷ്കരണവാദി?"),
        (INDUS, [b for _, b in INDUS], [a for a, _ in INDUS],
         "സിന്ധു സംസ്കാരത്തിൽ '{a}'-ന്റെ പ്രധാന സവിശേഷത?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സിന്ധു സ്ഥലം?"),
        (SANGAM, [b for _, b in SANGAM], [a for a, _ in SANGAM],
         "സംഗം/പുരാതന സാഹിത്യത്തിൽ '{a}'-ന്റെ വിവരണം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട കൃതി?"),
        (FOREIGN_POLICY, [b for _, b in FOREIGN_POLICY], [a for a, _ in FOREIGN_POLICY],
         "'{a}'-യുമായി ബന്ധപ്പെട്ട രാജ്യം/വിവരണം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട നയം/ഉടമ്പടി?"),
    ):
        _pairs(out, existing, rng, rows, [fwd], pool_b)
        _pairs_rev(out, existing, rng, rows, [rev], pool_a)

    _match_pairs(
        out,
        existing,
        rng,
        MATCH_ROWS,
        [
            "താഴെപ്പറയുന്നവയിൽ '{a}'-യുമായി ശരിയായി ജോഡിച്ചത്?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ശരിയായ ജോഡി ഏത്?",
            "'{a}' — ശരിയായ വിവരണം?",
        ],
    )


def _wave15_extra(out: list[Candidate], existing: set[str], rng: random.Random) -> None:
    saints = list({a for a, _, _ in BHAKTI})
    movements = list({b for _, b, _ in BHAKTI})
    regions = list({c for _, _, c in BHAKTI})
    _triples(
        out,
        existing,
        rng,
        BHAKTI,
        ["'{a}'-ന്റെ ആത്മീയ പ്രസ്ഥാനം?", "'{a}' ഏത് പ്രസ്ഥാനവുമായി?"],
        ["'{a}' പ്രവർത്തിച്ച പ്രദേശം?", "'{a}'-ന്റെ പ്രവർത്തന കേന്ദ്രം?"],
        ["'{b}' പ്രസ്ഥാനത്തിന്റെ '{c}' പ്രതിനിധി?", "'{c}'-ൽ '{b}' പ്രസ്ഥാനം?"],
        movements,
        regions,
        saints,
    )

    builders = list({b for _, b in MONUMENTS})
    monuments = list({a for a, _ in MONUMENTS})
    _pairs(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{a}'-ന്റെ നിർമ്മാതാവ്?",
            "'{a}'-യുടെ നിർമ്മാണ ഉത്തരവാദി?",
        ],
        builders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{b}'-ന്റെ പേരിൽ അറിയപ്പെടുന്ന നിർമ്മാണം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണം?",
        ],
        monuments,
    )

    styles = list({b for _, b in TEMPLE_ARCH})
    temples = list({a for a, _ in TEMPLE_ARCH})
    _pairs(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{a}'-ന്റെ വാസ്തുവിദ്യാ ശൈലി?",
            "'{a}'-ന്റെ ശില്പശൈലി?",
        ],
        styles,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        ["'{b}' ശൈലിയിലെ പ്രധാന നിർമ്മാണം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട ക്ഷേത്രം?"],
        temples,
    )

    periods = list({b for _, b in TRAVELLERS})
    travellers = list({a for a, _ in TRAVELLERS})
    _pairs(
        out,
        existing,
        rng,
        TRAVELLERS,
        ["'{a}'-ന്റെ ഇന്ത്യാ സന്ദർശന കാലം?", "'{a}'-ന്റെ സഞ്ചാര കാലഘട്ടം?"],
        periods,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TRAVELLERS,
        ["'{b}'-യിൽ ഇന്ത്യ സന്ദർശിച്ചയാൾ?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സഞ്ചാരി?"],
        travellers,
    )

    founders = list({b for _, b in NEWSPAPERS})
    papers = list({a for a, _ in NEWSPAPERS})
    _pairs(
        out,
        existing,
        rng,
        NEWSPAPERS,
        ["'{a}'-ന്റെ സ്ഥാപകൻ?", "'{a}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി?"],
        founders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        NEWSPAPERS,
        ["'{b}'-ന്റെ പത്രം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട പത്രം?"],
        papers,
    )

    years = list({y for _, y, _, _ in REVOLTS})
    rev_regions = list({r for _, _, r, _ in REVOLTS})
    leaders = list({l for _, _, _, l in REVOLTS})
    names = list({n for n, _, _, _ in REVOLTS})
    _quads(
        out,
        existing,
        rng,
        REVOLTS,
        ["'{n}'-ന്റെ വർഷം?", "'{n}'-യുമായി ബന്ധപ്പെട്ട വർഷം?"],
        ["'{n}'-ന്റെ പ്രദേശം?", "'{n}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം?"],
        ["'{n}'-ന്റെ നേതാവ്?", "'{n}'-യുമായി ബന്ധപ്പെട്ട നേതാവ്?"],
        ["'{l}'-യുമായി ബന്ധപ്പെട്ട സംഘടന?", "'{l}'-ന്റെ സംഘടന/സമരം?"],
        years,
        rev_regions,
        leaders,
        names,
    )

    for rows, pool_b, pool_a, ab, ba in (
        (LAND_REVENUE, [b for _, b in LAND_REVENUE], [a for a, _ in LAND_REVENUE], "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?", "'{b}'-യുമായി ബന്ധപ്പെട്ട നികുതി/വ്യവസ്ഥ?"),
        (MUGHAL_ADMIN, [b for _, b in MUGHAL_ADMIN], [a for a, _ in MUGHAL_ADMIN], "'{a}'-ന്റെ അർത്ഥം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട പദം?"),
        (COINS, [b for _, b in COINS], [a for a, _ in COINS], "'{a}'-യുമായി ബന്ധപ്പെട്ട കാലം?", "'{b}'-ന്റെ കാലത്തെ നാണയം?"),
        (EURO_FACTORIES, [b for _, b in EURO_FACTORIES], [a for a, _ in EURO_FACTORIES], "'{a}'-ന്റെ കച്ചവട കേന്ദ്രം?", "'{b}'-യിലെ യൂറോപ്യൻ കമ്പനി?"),
        (REFORMERS, [b for _, b in REFORMERS], [a for a, _ in REFORMERS], "'{a}'-ന്റെ പ്രസ്ഥാനം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി?"),
        (INDUS, [b for _, b in INDUS], [a for a, _ in INDUS], "'{a}'-ന്റെ സവിശേഷത?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സ്ഥലം?"),
        (SANGAM, [b for _, b in SANGAM], [a for a, _ in SANGAM], "'{a}'-ന്റെ വിവരണം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട കൃതി?"),
        (FOREIGN_POLICY, [b for _, b in FOREIGN_POLICY], [a for a, _ in FOREIGN_POLICY], "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സംഭവം?"),
    ):
        _pairs(out, existing, rng, rows, [ab], pool_b)
        _pairs_rev(out, existing, rng, rows, [ba], pool_a)

    _match_pairs(
        out,
        existing,
        rng,
        MATCH_ROWS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ശരിയായ ജോഡി?",
            "'{a}'-ന്റെ ശരിയായ വിവരണം?",
            "'{a}'-യുടെ ശരിയായ ജോഡി?",
        ],
    )


def _wave15_more(out: list[Candidate], existing: set[str], rng: random.Random) -> None:
    saints = list({a for a, _, _ in BHAKTI})
    movements = list({b for _, b, _ in BHAKTI})
    regions = list({c for _, _, c in BHAKTI})
    _triples(
        out,
        existing,
        rng,
        BHAKTI,
        [
            "'{a}'-ന്റെ ആത്മീയ പരമ്പര?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രസ്ഥാനം?",
            "'{a}' ഏത് സൂഫി/ഭക്തി പരമ്പര?",
        ],
        [
            "'{a}'-ന്റെ പ്രവർത്തന പ്രദേശം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം?",
            "'{a}' പ്രധാനമായി പ്രവർത്തിച്ച സ്ഥലം?",
        ],
        [
            "'{b}'-യുടെ '{c}' പ്രതിനിധി?",
            "'{c}'-ലെ '{b}' പ്രസ്ഥാനത്തിന്റെ പ്രധാന വ്യക്തി?",
            "'{b}' '{c}'-യിൽ പ്രവർത്തിച്ച വ്യക്തി?",
        ],
        movements,
        regions,
        saints,
    )

    builders = list({b for _, b in MONUMENTS})
    monuments = list({a for a, _ in MONUMENTS})
    _pairs(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാതാവ്?",
            "'{a}'-ന്റെ നിർമ്മാണ കാലത്തെ ഭരണാധികാരി?",
            "'{a}'-യുടെ നിർമ്മാതാവ്?",
            "'{a}' നിർമ്മിച്ച ഭരണാധികാരി?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട രാജാവ്?",
        ],
        builders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണം?",
            "'{b}'-ന്റെ കാലത്തെ പ്രധാന സ്മാരകം?",
            "'{b}' നിർമ്മിച്ച സ്മാരകം?",
            "'{b}'-യുടെ പേരിലുള്ള നിർമ്മാണം?",
        ],
        monuments,
    )

    styles = list({b for _, b in TEMPLE_ARCH})
    temples = list({a for a, _ in TEMPLE_ARCH})
    _pairs(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{a}'-യുടെ വാസ്തുവിദ്യാ ശൈലി?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണശൈലി?",
            "'{a}' ഏത് ശില്പശൈലിയിൽ?",
            "'{a}'-ന്റെ ശില്പശൈലി?",
        ],
        styles,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണം?",
            "'{b}' ശൈലിയുടെ പ്രതിനിധി?",
            "'{b}'-യിൽ പണിത പ്രധാന നിർമ്മാണം?",
        ],
        temples,
    )

    periods = list({b for _, b in TRAVELLERS})
    travellers = list({a for a, _ in TRAVELLERS})
    _pairs(
        out,
        existing,
        rng,
        TRAVELLERS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട കാലഘട്ടം?",
            "'{a}'-ന്റെ ഇന്ത്യാ സന്ദർശന കാലം?",
            "'{a}' ഏത് കാലത്ത് ഇന്ത്യ സന്ദർശിച്ചു?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഭരണകാലം?",
        ],
        periods,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TRAVELLERS,
        [
            "'{b}'-യിൽ ഇന്ത്യ സന്ദർശിച്ചയാൾ?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സഞ്ചാരി?",
            "'{b}' കാലത്ത് ഇന്ത്യ സന്ദർശിച്ച വ്യക്തി?",
        ],
        travellers,
    )

    founders = list({b for _, b in NEWSPAPERS})
    papers = list({a for a, _ in NEWSPAPERS})
    _pairs(
        out,
        existing,
        rng,
        NEWSPAPERS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി?",
            "'{a}'-ന്റെ സ്ഥാപകൻ?",
            "'{a}' ആരുടെ പേരിലാണ്?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട സ്ഥാപകൻ?",
        ],
        founders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        NEWSPAPERS,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പത്രം?",
            "'{b}'-ന്റെ പേരിലുള്ള പത്രം?",
            "'{b}' ആരംഭിച്ച പത്രം?",
        ],
        papers,
    )

    years = list({y for _, y, _, _ in REVOLTS})
    rev_regions = list({r for _, _, r, _ in REVOLTS})
    leaders = list({l for _, _, _, l in REVOLTS})
    names = list({n for n, _, _, _ in REVOLTS})
    _quads(
        out,
        existing,
        rng,
        REVOLTS,
        [
            "'{n}'-യുടെ പ്രധാന വർഷം?",
            "'{n}'-യുമായി ബന്ധപ്പെട്ട വർഷം?",
            "'{n}' നടന്ന വർഷം?",
        ],
        [
            "'{n}'-യുടെ പ്രധാന പ്രദേശം?",
            "'{n}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം?",
            "'{n}' നടന്ന പ്രദേശം?",
        ],
        [
            "'{n}'-യുടെ നേതാവ്?",
            "'{n}'-യുമായി ബന്ധപ്പെട്ട നേതാവ്?",
            "'{n}'-യുടെ പ്രധാന വ്യക്തി?",
        ],
        [
            "'{l}'-യുമായി ബന്ധപ്പെട്ട സമരം?",
            "'{r}'-ൽ '{l}'-യുമായി ബന്ധപ്പെട്ട സംഘടന?",
            "'{l}' നേതൃത്വം നൽകിയ സംഘടന?",
        ],
        years,
        rev_regions,
        leaders,
        names,
    )

    for rows, pool_b, pool_a, ab_fwd, ab_rev in (
        (
            LAND_REVENUE,
            [b for _, b in LAND_REVENUE],
            [a for a, _ in LAND_REVENUE],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട നികുതി/വ്യവസ്ഥ?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നികുതി?",
        ),
        (
            MUGHAL_ADMIN,
            [b for _, b in MUGHAL_ADMIN],
            [a for a, _ in MUGHAL_ADMIN],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഭരണപദം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പദം?",
        ),
        (
            COINS,
            [b for _, b in COINS],
            [a for a, _ in COINS],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട നാണയ കാലം?",
            "'{b}'-ന്റെ കാലത്തെ നാണയം?",
        ),
        (
            EURO_FACTORIES,
            [b for _, b in EURO_FACTORIES],
            [a for a, _ in EURO_FACTORIES],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട കച്ചവട കേന്ദ്രം?",
            "'{b}'-യിലെ യൂറോപ്യൻ കമ്പനി?",
        ),
        (
            REFORMERS,
            [b for _, b in REFORMERS],
            [a for a, _ in REFORMERS],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രസ്ഥാനം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പരിഷ്കരണവാദി?",
        ),
        (
            INDUS,
            [b for _, b in INDUS],
            [a for a, _ in INDUS],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട സവിശേഷത?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സ്ഥലം?",
        ),
        (
            SANGAM,
            [b for _, b in SANGAM],
            [a for a, _ in SANGAM],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വിവരണം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട കൃതി?",
        ),
        (
            FOREIGN_POLICY,
            [b for _, b in FOREIGN_POLICY],
            [a for a, _ in FOREIGN_POLICY],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വിവരണം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നയം/സംഭവം?",
        ),
    ):
        _pairs(
            out,
            existing,
            rng,
            rows,
            [ab_fwd, "'{a}'-ന്റെ പ്രധാന വിവരണം?", "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?"],
            pool_b,
        )
        _pairs_rev(
            out,
            existing,
            rng,
            rows,
            [ab_rev, "'{b}'-യുമായി ബന്ധപ്പെട്ട വസ്തു?", "'{b}'-ന്റെ പേരിലുള്ള വസ്തു?"],
            pool_a,
        )

    _match_pairs(
        out,
        existing,
        rng,
        MATCH_ROWS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ശരിയായ ജോഡി?",
            "'{a}'-ന് അനുയോജ്യമായ വിവരണം?",
            "'{a}'-യുടെ ശരിയായ വിവരണം?",
            "താഴെ കൊടുത്തിരിക്കുന്നവയിൽ '{a}'-ന്റെ ശരിയായ ജോഡി?",
        ],
    )


if __name__ == "__main__":
    print(len(generate_wave15_candidates(set(), random.Random(0))))
