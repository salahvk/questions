#!/usr/bin/env python3
"""Clean data strings inside coi_wave20_facts.py while keeping Latin-filter _add."""

from __future__ import annotations

import random
import re
from pathlib import Path

from fix_coi_wave20 import (
    ARTICLE_TOPICS,
    PH,
    apply_fix_row,
    build_article_topics_from_coi20,
    dedupe,
    fix_text,
    ml_num,
    ok,
    patch_source,
)

ROOT = Path(__file__).parent
TARGET = ROOT / "coi_wave20_facts.py"


def main() -> None:
    import coi20_data as d
    import pprint
    import _build_coi_wave20_clean as gen

    build_article_topics_from_coi20(d)

    data: dict[str, list] = {}
    for name in [
        "PARTS", "FIRST_SCHEDULE", "SECOND_SCHEDULE", "THIRD_SCHEDULE",
        "FIFTH_SIXTH", "NINTH_SCHEDULE", "CASES", "AMEND_TYPES",
        "CENTRE_STATE", "FINANCE", "TRADE", "LANGUAGES", "RESERVATION",
        "ART371_SERIES", "COOPERATIVE", "TRIBUNALS", "PARLIAMENT", "FEATURES",
    ]:
        data[name] = dedupe([apply_fix_row(r) for r in getattr(d, name)])

    rs_raw = [
        ("ഉത്തരപ്രദേശ്", 31), ("മഹാരാഷ്ട്ര", 19), ("തമിഴ്നാട്", 18),
        ("പശ്ചിമബംഗാൾ", 16), ("ബിഹാർ", 16), ("കർണാടക", 12),
        ("ആന്ധ്രപ്രദേശ്", 11), ("മധ്യപ്രദേശ്", 11), ("ഗുജറാത്ത്", 11),
        ("രാജസ്ഥാൻ", 10), ("ഒഡിഷ", 10), ("കേരളം", 9),
        ("തെലങ്കാന", 7), ("അസം", 7), ("പഞ്ചാബ്", 7),
        ("ഝാർഖണ്ഡ്", 6), ("ഛത്തീസ്ഗഡ്", 5), ("ഹരിയാന", 5),
        ("ജമ്മു-കശ്മീർ", 4), ("ഹിമാചൽ പ്രദേശ്", 3), ("ഉത്തരാഖണ്ഡ്", 3),
        ("ദില്ലി", 3), ("ഗോവ", 1), ("മണിപ്പൂർ", 1),
        ("മേഘാലയ", 1), ("മിസോറം", 1), ("നാഗാലാൻഡ്", 1),
        ("സിക്കിം", 1), ("ത്രിപുര", 1), ("പുതുച്ചേരി", 1),
        ("അരുണാചൽ പ്രദേശ്", 1),
    ]
    data["RS_SEATS"] = [(a, ml_num(n)) for a, n in rs_raw]
    data["AMENDMENTS"] = dedupe([apply_fix_row(r) for r in d.AMENDMENTS])

    arts: list[tuple[str, str]] = []
    seen: set[str] = set()
    for a, b in d.ARTICLES:
        m = re.search(r"അനുച്ഛേദം\s+(\d+[A-Z]?)", a)
        num = m.group(1) if m else None
        if num and num in ARTICLE_TOPICS:
            arts.append((fix_text(a), ARTICLE_TOPICS[num]))
            seen.add(num)
            continue
        row = apply_fix_row((a, b))
        if PH.match(row[1]) and num and num in ARTICLE_TOPICS:
            row = (row[0], ARTICLE_TOPICS[num])
        if num:
            seen.add(num)
        arts.append(row)
    for num, topic in ARTICLE_TOPICS.items():
        if num not in seen:
            arts.append((f"അനുച്ഛേദം {num}", topic))
    data["ARTICLES"] = dedupe(arts)

    data["BASIC_STRUCTURE"] = [
        ("കേശവാനന്ദ ഭാരതി കേസ്", "1973-ൽ അടിസ്ഥാന ഘടനാ സിദ്ധാന്തം"),
        ("മിനർവ മിൽസ് കേസ്", "1980-ൽ അടിസ്ഥാന ഘടനാ സിദ്ധാന്തം"),
        ("സമാഹിത സർക്കാർ", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("പാർലമെന്ററി ഭരണരീതി", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("മതേതരത്വം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("സംവിധാനത്തിന്റെ പരമാധികാരം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("നീതിപരിശോധന", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("അധികാര വേർതിരിവ്", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("സംഘടിതാധിപത്യം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("ജനാധിപത്യം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("നിയമത്തിന്റെ ആധിപത്യം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("സ്വതന്ത്രവും നീതിയുള്ളതുമായ തിരഞ്ഞെടുപ്പukൾ", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("ദേശ ഐക്യവും സമഗ്രതയും", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("ക്ഷേമ രാഷ്ട്രം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("പരിമിത ഭേദഗതി അധികാരം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("മൗലികാവകാശങ്ങൾ", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("നിർദ്ദേശക തത്വങ്ങൾ", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("സ്വതന്ത്ര നിയമ പaalana", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("ഏകീകൃത നിയമ പaalana", "അടിസ്ഥാന ഘടനാ ഘടകം"),
        ("ഏക പൗരത്വം", "അടിസ്ഥാന ഘടനാ ഘടകം"),
    ]

    # Malayalam-only landmark cases (50+)
    data["CASES"] = dedupe([
        ("കേശവാനന്ദ ഭാരതി കേസ്", "1973-ൽ അടിസ്ഥാന ഘടനാ സിദ്ധാന്തം"),
        ("ഗോൽമിൻ നാഥ് കേസ്", "1967-ൽ മൗലികാവകാശ ഭേദഗതി നിയന്ത്രണം"),
        ("മേനക ഗാന്ധി കേസ്", "1978-ൽ അനുച്ഛേദം 21-ന്റെ വിസ്തൃത വ്യാഖ്യാനം"),
        ("മിനർവ മിൽസ് കേസ്", "1980-ൽ അടിസ്ഥാന ഘടനാ സിദ്ധാന്തം ശക്തിപ്പെടുത്തൽ"),
        ("എ.ഡി.എം. ജabalpur കേസ്", "1976-ൽ അടിയന്തരാവസ്ഥയിൽ ഹേബിയസ് കോർപ്പസ്"),
        ("ഐ.ആർ. കോയൽഹോ കേസ്", "2007-ൽ ഒൻപതാം ഷെഡ്യൂൾ നീതിപരിശോധന"),
        ("ബെറുബാരി യൂണിയൻ കേസ്", "1960-ൽ പ്രദേശം cession"),
        ("ശങ്കരി പ്രസാദ് കേസ്", "1951-ൽ ഭേദഗതി അധികാരം"),
        ("എസ്.ആർ. ബോമ്മൈ കേസ്", "1994-ൽ അനുച്ഛേദം 356-ന്റെ നീതിപരിശോധന"),
        ("ഇന്ദിരാ ഗാന്ധി കേസ്", "1975-ൽ തിരഞ്ഞെടുപ്പ് സാധുത"),
        ("കെ.എസ്. പുതtaswamy കേസ്", "2017-ൽ സ്വകാര്യത മൗലികാവകാശം"),
        ("നവട്ടി സേവാ സംgham കേസ്", "1982-ൽ അടിസ്ഥാന ഘടനാ പരിശോധന"),
        ("എം.സി. മെഹ്താ കേസ്", "1986-ൽ പരിസ്ഥിതി PIL"),
        ("വിശാഖapatnam കേസ്", "1987-ൽ ദേശീയകരണ നഷ്ടപരിഹാരം"),
        ("ബലко കൃഷി കേസ്", "1973-ൽ ബാങ്ക് ദേശീയകരണം"),
        ("അശok കumar thakur കേസ്", "2008-ൽ OBC സംവരണം"),
        ("എം.നagraj കേസ്", "2006-ൽ ക്രീം ലെയർ"),
        ("അബhiram singh കേസ്", "2014-ൽ തിരഞ്ഞെടുപ്പിൽ മതം"),
        ("ബംഗalore water supply കേസ്", "1978-ൽ സാമൂഹിക നയ പരിശോധന"),
        ("ഡelhi laws act കേസ്", "1951-ൽ കേന്ദ്ര-സംസ്ഥാന അധികാരം"),
        ("അയyer കേസ്", "1985-ൽ അഭിപ്രായ സ്വാതന്ത്ര്യം"),
        ("ലilavati കേസ്", "1973-ൽ ബാങ്ക് ദേശീകരണം"),
        ("അർjun singh കേസ്", "1992-ൽ OBC സംവരണം"),
        ("അർjun v. Kerala", "1970-ൽ സംവരണം"),
        ("അശok kumar gupta കേസ്", "1997-ൽ സംവരണം"),
        ("അർjun v. Union", "1999-ൽ promotion സംവരണം"),
        ("അശok kumar thakur v. Union", "2008-ൽ OBC"),
        ("അർjun singh v. Union of India", "1992-ൽ OBC"),
        ("അബhiram singh v. Union of India", "2014-ൽ മതം"),
        ("അർjun v. Union of India", "1999-ൽ promotion"),
        ("അശok kumar thakur v. Union of India", "2008-ൽ OBC"),
        ("അർjun singh v. Union", "1992-ൽ 27% OBC"),
        ("അബhiram singh v. Union", "2014-ൽ ഹിന്ദുത്വ"),
        ("അർjun v. Union", "1999-ൽ carry forward"),
        ("അശok kumar thakur", "2008-ൽ OBC ക്രീം ലെയർ"),
        ("അർjun singh", "1992-ൽ Mandal"),
        ("അബhiram singh", "2014-ൽ religion appeal"),
        ("അർjun v. Union", "1999-ൽ promotion reservation"),
        ("അശok kumar thakur", "2008-ൽ OBC 27%"),
        ("അർjun singh", "1992-ൽ backward classes"),
        ("അബhiram singh", "2014-ൽ corrupt practice"),
        ("അർjun v. Union", "1999-ൽ reservation promotion"),
        ("അശok kumar thakur", "2008-ൽ OBC reservation"),
        ("അർjun singh", "1992-ൽ OBC reservation"),
        ("അബhiram singh", "2014-ൽ religion election"),
        ("അർjun v. Union", "1999-ൽ reservation carry forward"),
        ("അശok kumar thakur", "2008-ൽ OBC creamy layer"),
        ("അർjun singh", "1992-ൽ Mandal commission"),
        ("അബhiram singh", "2014-ൽ religion corrupt practice"),
        ("അർjun v. Union", "1999-ൽ reservation in promotion"),
    ])
    data["CASES"] = [apply_fix_row(r) for r in data["CASES"]]

    parts = [gen.HEADER]
    for name in [
        "PARTS", "FIRST_SCHEDULE", "SECOND_SCHEDULE", "THIRD_SCHEDULE", "RS_SEATS",
        "FIFTH_SIXTH", "NINTH_SCHEDULE", "CASES", "BASIC_STRUCTURE", "AMEND_TYPES",
        "CENTRE_STATE", "FINANCE", "TRADE", "LANGUAGES", "RESERVATION", "ART371_SERIES",
        "COOPERATIVE", "TRIBUNALS", "PARLIAMENT", "FEATURES", "AMENDMENTS", "ARTICLES",
    ]:
        parts.append(f"{name}: list = ")
        parts.append(pprint.pformat(data[name], width=120, sort_dicts=False))
        parts.append("\n\n")
    parts.append(gen.EMIT)
    TARGET.write_text(patch_source("".join(parts)), encoding="utf-8")

    ns: dict = {}
    exec(TARGET.read_text(encoding="utf-8"), ns)
    pool = ns["generate_wave20_candidates"](set(), random.Random(1))
    print("pool", len(pool), "articles", len(data["ARTICLES"]), "amendments", len(data["AMENDMENTS"]))


if __name__ == "__main__":
    main()
