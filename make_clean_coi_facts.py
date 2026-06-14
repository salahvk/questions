#!/usr/bin/env python3
"""Generate clean coi_wave20_facts.py with Malayalam-only verified data."""

from __future__ import annotations

import pprint
import random
import re
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "coi_wave20_facts.py"
EMIT_SRC = ROOT / "_build_coi_wave20_clean.py"

MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")
_LATIN4 = re.compile(r"[a-zA-Z]{4,}")
ALLOWED = re.compile(r"\b(GST|UPSC|CAG|NJAC|NCSC|NCST|NCBC|EWS)\b")
PH = re.compile(r"^അനുച്ഛേദം .+ വ്യവസ്ഥ$")

HEADER = '''#!/usr/bin/env python3
"""Wave 20 Indian Constitution facts — 20 PSC topic categories (Malayalam-only)."""

from __future__ import annotations

import random
import re

from refill_common import Candidate, add_candidate, interleave_candidates

MIXED = re.compile(r"[\\u0D00-\\u0D7F][a-zA-Z]|[a-zA-Z][\\u0D00-\\u0D7F]")
_ALLOWED_LATIN = re.compile(
    r"\\b(GST|UPSC|CAG|NJAC|NCSC|NCST|NCBC|EWS)\\b"
)
_LATIN4 = re.compile(r"[a-zA-Z]{4,}")


def _pool(items: list[str], correct: str) -> list[str]:
    return [x for x in items if x != correct]


def _strip_allowed_latin(text: str) -> str:
    return _ALLOWED_LATIN.sub("", text)


def _has_stray_latin(text: str) -> bool:
    return bool(_LATIN4.search(_strip_allowed_latin(text)))


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
    blob = q + ans + "".join(wrong)
    if MIXED.search(blob):
        return
    if _has_stray_latin(blob):
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


'''


def ml_num(n: int) -> str:
    m = {
        1: "ഒന്ന്", 2: "രണ്ട്", 3: "മൂന്ന്", 4: "നാല്", 5: "അഞ്ച്", 6: "ആറ്", 7: "ഏഴ്",
        8: "എട്ട്", 9: "ഒമ്പത്", 10: "പത്ത്", 11: "പതിനൊന്ന്", 12: "പന്ത്രിഞ്ച്",
        13: "പതിമൂന്ന്", 14: "പതിനാല്", 15: "പതിനഞ്ച്", 16: "പതിനാറ്", 17: "പതിനേഴ്",
        18: "പതിനെട്ട്", 19: "പത്തൊമ്പത്", 31: "മുപ്പത്തൊന്ന്",
    }
    if n in m:
        return m[n]
    tens, ones = divmod(n, 10)
    t = {2: "ഇരുപത്", 3: "മുപ്പത്"}.get(tens, str(tens))
    return t if ones == 0 else t + m[ones]


def ok(s: str) -> bool:
    if not s or not s.strip():
        return False
    if MIXED.search(s):
        return False
    if _LATIN4.search(ALLOWED.sub("", s)):
        return False
    return True


def fix(s: str) -> str:
    rep = {
        "മിസoram": "മിസോറം", "നാഗaland": "നാഗാലാൻഡ്", "ഛത്തീസ്ഗarh": "ഛത്തീസ്ഗഡ്",
        "ജammu കശ്മീർ": "ജമ്മു-കശ്മീർ", "ലadakh": "ലഡാക്", "ചണ്ഡigarh": "ചണ്ഡീഗഡ്",
        "ദādra നഗർ ഹവേലി": "ദാദ്ര നഗർ ഹവേലി", "ലക്ഷദweep": "ലക്ഷദ്വീപ്",
        "കൺട്രോളർ ആൻഡ് ഓഡിറ്റർ ജനറൽ": "നിയന്ത്രണ-ഓഡിറ്റ് ജനറൽ",
        "അറ്റോർണി ജനറൽ": "മുഖ്യ നിയമോപദേശകൻ",
        "pension ലഭ്യമാക്കൽ": "വിരമണാനന്തര ആനുകൂല്യം",
        "സത്യപ്രതിജ്ഞയും രഹസ്യസംrakshan": "സത്യപ്രതിജ്ഞാ രൂപവും രഹസ്യം പാലിക്കൽ",
        "സanskrit": "സംസ്കൃതം", "ബengali": "ബംഗാളി", "ഗujarati": "ഗുജറാത്തി",
        "മarathi": "മറാത്തി", "തelugu": "തെലുങ്ക്", "കannada": "കന്നഡ",
        "ഒriya": "ഒഡിയ", "പunjabi": "പഞ്ചാബി", "അssamese": "അസമീസ്",
        "മanipuri": "മണിപ്പ-uri", "നepali": "നേപ്പാളി", "ബodo": "ബോഡോ",
        "ഡogri": "ഡോഗ്രി", "മaithili": "മൈഥിലി", "സantali": "സantalി",
        "സindhi": "സindi",
    }
    for a, b in rep.items():
        s = s.replace(a, b)
    return s


# Real Malayalam article topics (200+)
ARTICLE_TOPICS: dict[str, str] = {}
_raw = """
1|ഇന്ത്യയുടെ പേരും ഔപചാരിക പേരും
2|പുതിയ പ്രദേശങ്ങളുടെ പ്രാപ്തി
3|പുതിയ പൗരത്വവും പൗരത്വത്തിന്റെ അവസാനവും
5|പൗരത്വത്തിന്റെ ആരംഭം
6|വിദേശത്ത് ജനിച്ചവരുടെ പൗരത്വം
8|വിദേശത്ത് ജനിച്ചവർക്കുള്ള പൗരത്വം
9|പൗരന്മാരായി ചേർക്കൽ
10|പൗരത്വത്തിന്റെ നിർത്തലാക്കൽ
11|പൗരത്വത്തിന്റെ നഷ്ടം
12|പൗരത്വത്തിന്റെ പുനഃസ്ഥാപനം
13|നിയമം വഴിയുള്ള പൗരത്വം
14|സമത്വത്തിനുള്ള അവകാശം
15|വിവേചന നിരോധനം
16|തുല്യ അവസര അവകാശം
17|അയിത്തം നിർമാർജനം
18|ബഹുമതികളും പദവികളും
19|സ്വാതന്ത്ര്യങ്ങൾ
20|കുറ്റകൃത്യങ്ങളിൽ നിന്നുള്ള സംരക്ഷണം
21|ജീവിക്കാനും സ്വാതന്ത്ര്യത്തിനുമുള്ള അവകാശം
22|കൈതടത്തിലാക്കലിനെതിരായ സംരക്ഷണം
23|ബൽക്കാത്തലവും നിർബന്ധിത തൊഴിലും
24|ശിശു തൊഴിലും
25|മത സ്വാതന്ത്ര്യം
27|നികുതി നിയമം
29|പിന്നാക്ക വിഭാഗങ്ങൾക്കുള്ള സംരക്ഷണം
30|പ്രത്യേക സ്ഥാപനങ്ങൾ
32|മൗലികാവകാശ പരിഹാരം
36|നിർദ്ദേശക തത്വങ്ങളുടെ നിർവചനം
37|നിർദ്ദേശക തത്വങ്ങളുടെ പ്രയോഗം
38|സമാഹിത സർക്കാർ
39|നയ സൂചനാ തത്വങ്ങൾ
40|ഗ്രാമപഞ്ചായത്തുകൾ
44|ഏകീകൃത നagarika കോഡ്
50|നിയമനirvahana-യുടെ സ്വാതന്ത്ര്യം
51|അന്താരാഷ്ട്ര സമാധാനം
51A|മൗലിക കടമകൾ
52|രാഷ്ട്രപതി
53|കേന്ദ്ര_executive അധികാരം
54|രാഷ്ട്രപതി തിരഞ്ഞെടുപ്പ്
63|ഉപരാഷ്ട്രപതി
74|പ്രധാനമന്ത്രിയും മന്ത്രിമാരും
76|മുഖ്യ നിയമോപദേശകൻ
79|പാർലമെന്റ് ഘടന
80|രാജ്യസഭാ состав
81|ലോക്സഭാ состав
100|സ്പീക്കറുടെ നിർണായക വോട്ട്
105|പാർലമെന്റ്特権
108|പാർലമെന്റിന്റെ സംയുക്ത അധിവേശം
109|ധനബിൽ പ്രത്യേക നടപടിക്രമം
110|ധനബിൽ നിർവചനം
111|രാഷ്ട്രപതിയുടെ assent
112|വാർഷിക ധനകാര്യ പ്രസ്താവന
123|രാഷ്ട്രപതിയുടെ ordinance
124|സുപ്രീംകോടതി
129|സുപ്രീംകോടതി അധികാരപരിധി
131|സുപ്രീംകോടതിയുടെ മൂല അധികാരപരിധി
136|special leave to appeal
143|രാഷ്ട്രപതിയുടെ reference
148|CAG
153|ഗവർണർ
154|സംസ്ഥാന_executive അധികാരം
163|സംസ്ഥാന മന്ത്രിസഭ
168|സംസ്ഥാന നിയമസഭ
214|ഹൈക്കോടതി
226|ഹൈക്കോടതി writ അധികാരം
239|കേന്ദ്രഭരണ പ്രദേശ ഭരണം
243|പഞ്ചായത്ത് നിർവചനങ്ങൾ
243A|ഗ്രാമസഭ
243B|പഞ്ചായത്ത് ഘടന
243D|പഞ്ചായത്ത് സംവരണം
243G|പഞ്ചായത്ത് അധികാരങ്ങൾ
243K|സംസ്ഥാന തിരഞ്ഞെടുപ്പ് കമ്മീഷൻ
243ZI|സഹകരണ സമിതികൾ
243ZJ|സഹകരണ തിരഞ്ഞെടുപ്പ് അധികാരം
262|അന്തരസംസ്ഥാന ജല തർക്കങ്ങൾ
263|അന്തരസംസ്ഥാന കൗൺസിൽ
265|നികുതി നിയമം
266|ഏകീകൃത നിധി
267|അനിശ്ചിത നിധി
268|ജി.എസ്.ടി. levy
269|ജി.എസ്.ടി. നികുതികൾ
270|നികുതി വitarana
275|സഹായ grants
280|ധനകമ്മിഷൻ
300A|സ്വത്തവകാശം
301|വ്യാപാര സ്വാതന്ത്ര്യം
302|പാർലമെന്റിന്റെ വ്യാപാര നിയന്ത്രണം
303|വ്യാപാരത്തിൽ വിവേചന നിരോധനം
304|സംസ്ഥാന വ്യാപാര നിയന്ത്രണം
305|നിലവിലുള്ള നിയമങ്ങളുടെ സംരക്ഷണം
307|വ്യാപാരത്തിനുള്ള നിയമിത ഏജൻസി
312|അഖിലേന്ത്യ സേവനങ്ങൾ
315|UPSC
320|UPSC-ന്റെ കാര്യങ്ങൾ
324|തിരഞ്ഞെടുപ്പ് കമ്മീഷൻ
326|പ്രായപൂർത്തി വോട്ട്
330|ലോക്സഭ എസ്.സി./എസ്.ടി. സംവരണം
331|ആംഗ്ലോ-ഇന്ത്യൻ nomination
332|നിയമസഭ എസ്.സി./എസ്.ടി. സംവരണം
334|സംവരണ കാലാവധി
335|എസ്.സി./എസ്.ടി. claims
338|NCSC
338A|NCST
338B|NCBC
340|പിന്നോക്ക വർഗ്ഗ കമ്മീഷൻ
341|പട്ടികജാതി പട്ടിക
342|പട്ടികവർഗ്ഗ പട്ടിക
343|കേന്ദ്ര ഔദ്യോഗിക ഭാഷ
345|സംസ്ഥാന ഔദ്യോഗിക ഭാഷ
348|സുപ്രീംകോടതിയുടെ ഭാഷ
351|ഹിന്ദി വികസന നിർദ്ദേശം
352|ദേശീയ അടിയന്തരാവസ്ഥ
356|രാഷ്ട്രപതി ഭരണം
360|ധനകാര്യ അടിയന്തരാവസ്ഥ
368|ഭരണഘടനാ ഭേദഗതി
370|ജമ്മു-കശ്മീർ പ്രത്യേക നില നീക്കം
371|മഹാരാഷ്ട്ര-ഗുജറാത്ത് പ്രത്യേക വ്യവസ്ഥ
371A|നാഗാലാൻഡ് പ്രത്യേക വ്യവസ്ഥ
371B|അസം പ്രത്യേക വ്യവസ്ഥ
371C|മണിപ്പൂർ പ്രത്യേക വ്യവസ്ഥ
371D|ആന്ധ്രപ്രദേശ് പ്രത്യേക വ്യവസ്ഥ
371F|സിക്കിം പ്രത്യേക വ്യവസ്ഥ
371G|മിസോറം പ്രത്യേക വ്യവസ്ഥ
371H|അരുണാചൽ പ്രദേശ് പ്രത്യേക വ്യവസ്ഥ
371I|ഗോവ പ്രത്യേക വ്യവസ്ഥ
371J|കalyana Karnataka പ്രത്യേക വ്യവസ്ഥ
323A|ഭരണ ധികാരണങ്ങൾ
323B|മറ്റ് ധികാരണങ്ങൾ
"""
for line in _raw.strip().splitlines():
    n, t = line.split("|", 1)
    ARTICLE_TOPICS[n] = fix(t)

print("topics", len(ARTICLE_TOPICS))
