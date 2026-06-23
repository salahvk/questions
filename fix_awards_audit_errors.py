#!/usr/bin/env python3
"""Fix confirmed factual errors in awards.json from audit (sections 15–30)."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AWARDS = ROOT / "awards.json"


def set_q(q: dict, **fields) -> None:
    for k, v in fields.items():
        q[k] = v


def replace_in_q(q: dict, old: str, new: str) -> None:
    q["question"] = q["question"].replace(old, new)
    q["options"] = [o.replace(old, new) for o in q["options"]]
    if q["answer"] == old:
        q["answer"] = new


def fix_by_id(questions: dict[str, dict]) -> None:
    """Apply per-id fixes. Missing ids are skipped silently."""

    # --- Kerala: Vallathol Puraskaram ---
    if "aca_0383" in questions:
        q = questions["aca_0383"]
        set_q(
            q,
            options=[
                "പണ്ഡിത് രവി ശങ്കർ",
                "പാലാ നാരായണൻ നായർ",
                "ഭാൽചന്ദ്ര നേമേഡെ",
                "വള്ളത്തോൾ നാരായണമേനോൻ",
            ],
            answer="പാലാ നാരായണൻ നായർ",
        )

    # --- Gallantry: Manoj Pandey PVC not Ashoka Chakra ---
    if "aca_2129" in questions:
        replace_in_q(questions["aca_2129"], "അശോക ചക്രം", "പരമവീര ചക്രം")

    # --- Turing Award: Alfred → Alan Perlis / namesake ---
    if "aca_0278" in questions:
        set_q(
            questions["aca_0278"],
            question="1966-ൽ ആദ്യ 'ട്യൂറിംഗ് അവാർഡ്' ലഭിച്ച കമ്പ്യൂട്ടർ ശാസ്ത്രജ്ഞൻ?",
            options=[
                "അലൻ പെർലിസ്",
                "ഹര്‍ഗോബിന്ദ് ഖോരാന",
                "സി.എൻ.ആർ. റാവു",
                "ഹരി ഗോവിന്ദ് ഖോരാന",
            ],
            answer="അലൻ പെർലിസ്",
        )

    if "aca_2167" in questions:
        set_q(
            questions["aca_2167"],
            question="1966-ൽ ആദ്യ 'ട്യൂറിംഗ് അവാർഡ്' ലഭിച്ച കമ്പ്യൂട്ടർ ശാസ്ത്രജ്ഞൻ?",
            options=[
                "രവീന്ദ്രനാഥ ടാഗോർ",
                "ടെറൻസ് ടാവോ",
                "അലൻ പെർലിസ്",
                "ഹരി ഗോവിന്ദ് ഖോരാന",
            ],
            answer="അലൻ പെർലിസ്",
        )

    if "aca_2624" in questions:
        set_q(
            questions["aca_2624"],
            question="'ട്യൂറിംഗ് അവാർഡ്' ആദ്യം ലഭിച്ച വർഷം?",
            options=["1966", "1954", "1971", "1983"],
            answer="1966",
        )

    if "aca_1858" in questions:
        set_q(
            questions["aca_1858"],
            question="'അലൻ പെർലിസ്' ലഭിച്ച 'ട്യൂറിംഗ് അവാർഡ്' ഏത് ശാസ്ത്ര ശാഖയുമായി ബന്ധപ്പെട്ടതാണ്?",
            options=[
                "കമ്പ്യൂട്ടർ സയൻസ്",
                "ഗണിതശാസ്ത്രം",
                "രസതന്ത്രം",
                "ഭൗതികശാസ്ത്രം",
            ],
            answer="കമ്പ്യൂട്ടർ സയൻസ്",
        )

    # --- Fields Medal: not fixed in Houston ---
    icm = "അന്താരാഷ്ട്ര ഗണിതശാസ്ത്ര കോൺഗ്രസ്"
    for qid in ("aca_1668", "aca_2994"):
        if qid not in questions:
            continue
        q = questions[qid]
        if qid == "aca_1668":
            set_q(
                q,
                question="പുരസ്കാര ചടങ്ങുകളിൽ 'ഫീൽഡ്സ് മെഡൽ' സാധാരണ നടക്കുന്നത്?",
                options=[icm, "തിരുവനന്തപുരം", "ഗോവ", "മനില"],
                answer=icm,
            )
        else:
            set_q(
                q,
                question="പുരസ്കാര ചടങ്ങുകളിൽ 'ഫീൽഡ്സ് മെഡൽ'-ന്റെ പ്രധാന ചടങ്ങ്/വിതരണം?",
                options=[icm, "കാന്സ്", "ഓസ്ലോ", "സാൻ ഫ്രാൻസിസ്കോ"],
                answer=icm,
            )

    # --- Sports awards ---
    if "aca_0640" in questions:
        set_q(
            questions["aca_0640"],
            question="2000-ൽ രാജീവ് ഗാന്ധി ഖേൽരത്ന അവാർഡ് നേടിയത് ആരാണ്?",
            options=[
                "വിരാട് കോഹ്‌ലി",
                "മേരി കോം",
                "പുൽളേള ഗോപിചന്ദ്",
                "മിറാൻബായി ചാനു",
            ],
            answer="പുൽളേള ഗോപിചന്ദ്",
        )

    if "aca_1229" in questions:
        set_q(
            questions["aca_1229"],
            question="1956-ൽ പത്മഭൂഷൺ നേടിയ 'ധ്യാൻചന്ദ്' ഏത് കായിക മേഖലയിൽ പ്രവർത്തിച്ചവർ ആണ്?",
            options=["ഫുട്ബോൾ", "കബഡി", "വെയ്റ്റ്‌ലിഫ്റ്റിംഗ്", "ഹോക്കി"],
            answer="ഹോക്കി",
        )

    if "aca_2311" in questions:
        replace_in_q(questions["aca_2311"], "1976", "1998")

    if "aca_2168" in questions:
        q = questions["aca_2168"]
        q["options"] = ["ബോക്സിംഗ്", "വെയ്റ്റ്‌ലിഫ്റ്റിംഗ്", "ചെസ്സ്", "ബാഡ്മിന്റൺ"]
        q["answer"] = "ബോക്സിംഗ്"

    if "aca_1904" in questions:
        replace_in_q(questions["aca_1904"], "1972", "2012")

    # --- Padma Awards ---
    padma_bhushan = "പത്മഭൂഷൺ"
    padma_vibhushan = "പത്മവിഭൂഷൺ"

    for qid in ("aca_0873",):
        if qid in questions:
            q = questions["aca_0873"]
            q["options"] = ["2024", "2020", "2005", "1974"]
            q["answer"] = "2024"

    if "aca_0488" in questions:
        q = questions["aca_0488"]
        replace_in_q(q, "2018", "2024")
        q["answer"] = padma_vibhushan

    if "aca_2657" in questions:
        replace_in_q(questions["aca_2657"], "2018", "2024")

    for qid in ("aca_1560", "aca_0911"):
        if qid in questions:
            q = questions[qid]
            if q["answer"] == padma_vibhushan:
                q["answer"] = padma_bhushan

    for qid in ("aca_1040", "aca_1691", "aca_1905", "aca_2254", "aca_2532"):
        if qid in questions:
            replace_in_q(questions[qid], padma_vibhushan, padma_bhushan)

    for qid in ("aca_1307", "aca_1458", "aca_0975", "aca_1756"):
        if qid in questions:
            replace_in_q(questions[qid], padma_vibhushan, padma_bhushan)

    if "aca_0276" in questions:
        replace_in_q(questions["aca_0276"], padma_vibhushan, padma_bhushan)

    if "aca_0964" in questions:
        q = questions["aca_0964"]
        replace_in_q(q, "2022", "2026")
        q["answer"] = padma_bhushan

    if "aca_2621" in questions:
        set_q(
            questions["aca_2621"],
            question="2026 പത്മഭൂഷൺ ചലച്ചിത്രം — ആരാണ്?",
            options=["മമ്മൂട്ടി", "കമൽഹാസൻ", "സി.എൻ.ആർ. റാവു", "ലതാ മങ്കേഷ്കർ"],
            answer="മമ്മൂട്ടി",
        )

    if "aca_2813" in questions:
        q = questions["aca_2813"]
        replace_in_q(q, padma_vibhushan, padma_bhushan)
        q["options"] = ["2007", "2026", "1999", "1979"]
        q["answer"] = "2026"

    for qid in ("aca_0291", "aca_1915"):
        if qid in questions:
            replace_in_q(questions[qid], "ടെന്നീസ്", "ബോക്സിംഗ്")

    if "aca_0590" in questions:
        q = questions["aca_0590"]
        q["options"] = ["ചെസ്സ്", "ശാസ്ത്രം", "ഷൂട്ടിംഗ്", "ബോക്സിംഗ്"]
        q["answer"] = "ബോക്സിംഗ്"

    if "aca_0418" in questions:
        set_q(
            questions["aca_0418"],
            question="2025 പത്മഭൂഷൺ നൃത്തം — ആരാണ്?",
            options=["മമ്മൂട്ടി", "ലവ്ലീന ബോർഗോഹൈൻ", "ശോഭനാ", "വിജയ്"],
            answer="ശോഭനാ",
        )

    if "aca_0502" in questions:
        set_q(
            questions["aca_0502"],
            question="പത്മഭൂഷൺ 2025-ൽ നൃത്തം മേഖലയിൽ ലഭിച്ചത്?",
            options=["അഭിനവ് ബിന്ദ്ര", "ശോഭനാ", "സൗരവ് ഗാംഗുലി", "കപിൽ ദേവ്"],
            answer="ശോഭനാ",
        )

    if "aca_2545" in questions:
        q = questions["aca_2545"]
        replace_in_q(q, "2024", "2025")
        q["answer"] = padma_bhushan

    if "aca_0543" in questions:
        set_q(
            questions["aca_0543"],
            options=["സൂര്യ", "ഉസ്താദ് ബിസ്മില്ലാ ഖാൻ", "ജയറാം", "ആമിർ ഖാൻ"],
            answer="ജയറാം",
        )

    if "aca_2485" in questions:
        set_q(
            questions["aca_2485"],
            question="'ജയറാം' പത്മശ്രീ ലഭിച്ച വർഷം?",
            options=["2011", "2002", "1979", "1992"],
            answer="2011",
        )

    for qid in ("aca_1456", "aca_2530", "aca_2649"):
        if qid in questions:
            replace_in_q(questions[qid], "1976", "2008")

    for qid in ("aca_1686", "aca_2063", "aca_2152", "aca_2201"):
        if qid in questions:
            replace_in_q(questions[qid], "1972", "2012")

    for qid in ("aca_1836", "aca_1988", "aca_2163"):
        if qid in questions:
            replace_in_q(questions[qid], "1990", "2004")

    if "aca_2283" in questions:
        replace_in_q(questions["aca_2283"], padma_vibhushan, padma_bhushan)

    if "aca_0258" in questions:
        replace_in_q(questions["aca_0258"], padma_vibhushan, padma_bhushan)

    # --- SNA classical music year/person fixes ---
    if "aca_0065" in questions:
        replace_in_q(questions["aca_0065"], "1976", "1975")

    for qid in ("aca_1279", "aca_2701"):
        if qid in questions:
            replace_in_q(questions[qid], "1976", "1975")

    bade = "ഉസ്താദ് ബഡെ ഗുലാം അലി ഖാൻ"
    for qid in ("aca_0577", "aca_0629", "aca_3052"):
        if qid in questions:
            q = questions[qid]
            q["answer"] = bade
            if bade not in q["options"]:
                q["options"] = [bade if o == "പണ്ഡിത് ജസ്റാജ്" else o for o in q["options"]]

    for qid in ("aca_1821", "aca_2183"):
        if qid in questions:
            replace_in_q(questions[qid], "1960", "1962")

    ginde = "കെ. ജി. ഗിൻദെ"
    for qid in ("aca_0981", "aca_1642", "aca_2821"):
        if qid in questions:
            q = questions[qid]
            q["answer"] = ginde
            if ginde not in q["options"]:
                q["options"] = [ginde if o == "സാക്കിർ ഹുസൈൻ" else o for o in q["options"]]

    # SNA Cinema → Theatre (no cinema category)
    for q in questions.values():
        if "SNA" in q.get("question", "") and "സിനിമ" in q.get("question", ""):
            replace_in_q(q, "സിനിമ", "നാടകം")

    # SNA Fellowship: year-only answers → real recipients
    fellowship_fixes = {
        "aca_0105": (
            "SNA ഫെലോഷിപ്പിൽ 1986 SNA ഫെലോഷിപ്പ് — ആരാണ്?",
            ["ലതാ മങ്കേഷ്കർ", "സത്യജിത് റേ", "പണ്ഡിത് ജസ്റാജ്", "ഗുൽസാർ"],
            "സത്യജിത് റേ",
        ),
        "aca_0192": (
            "SNA ഫെലോഷിപ്പിൽ 1986 SNA ഫെലോഷിപ്പ് — ആരാണ്?",
            ["ലതാ മങ്കേഷ്കർ", "സത്യജിത് റേ", "പണ്ഡിത് ജസ്റാജ്", "ഗുൽസാർ"],
            "സത്യജിത് റേ",
        ),
        "aca_0594": (
            "SNA ഫെലോഷിപ്പിൽ 1989 SNA ഫെലോഷിപ്പ് — ആരാണ്?",
            ["ലതാ മങ്കേഷ്കർ", "സത്യജിത് റേ", "പണ്ഡിത് ജസ്റാജ്", "ഗുൽസാർ"],
            "ലതാ മങ്കേഷ്കർ",
        ),
        "aca_1246": (
            "SNA ഫെലോഷിപ്പിൽ 2001 SNA ഫെലോഷിപ്പ് — ആരാണ്?",
            ["എം. ബാലമുരളികൃഷ്ണ", "ബി. വി. കാരന്ത്", "സത്യജിത് റേ", "ഗുൽസാർ"],
            "എം. ബാലമുരളികൃഷ്ണ",
        ),
        "aca_1286": (
            "SNA ഫെലോഷിപ്പിൽ 1990 SNA ഫെലോഷിപ്പ് — ആരാണ്?",
            ["ഉത്പൽ ദത്ത്", "റാം ഗോപാൽ", "ലതാ മങ്കേഷ്കർ", "ഗുൽസാർ"],
            "ഉത്പൽ ദത്ത്",
        ),
        "aca_2185": (
            "SNA ഫെലോഷിപ്പിൽ 1973 SNA ഫെലോഷിപ്പ് — ആരാണ്?",
            ["കെ. ശിവറാമ കാരന്ത", "സത്യജിത് റേ", "ലതാ മങ്കേഷ്കർ", "ഗുൽസാർ"],
            "കെ. ശിവറാമ കാരന്ത",
        ),
        "aca_2257": (
            "SNA ഫെലോഷിപ്പിൽ 2002 SNA ഫെലോഷിപ്പ് — ആരാണ്?",
            ["കാവലം നാരായണ പണിക്കർ", "സത്യജിത് റേ", "ലതാ മങ്കേഷ്കർ", "ഗുൽസാർ"],
            "കാവലം നാരായണ പണിക്കർ",
        ),
        "aca_0268": (
            "SNA ഫെലോഷിപ്പിൽ 2004 SNA ഫെലോഷിപ്പ് — ആരാണ്?",
            ["സോഹ്റാ സെഹ്ഗാൽ", "സത്യജിത് റേ", "ലതാ മങ്കേഷ്കർ", "ഗുൽസാർ"],
            "സോഹ്റാ സെഹ്ഗാൽ",
        ),
        "aca_3175": (
            "SNA ഫെലോഷിപ്പിൽ 2004 SNA ഫെലോഷിപ്പ് — ആരാണ്?",
            ["സോഹ്റാ സെഹ്ഗാൽ", "സത്യജിത് റേ", "ലതാ മങ്കേഷ്കർ", "ഗുൽസാർ"],
            "സോഹ്റാ സെഹ്ഗാൽ",
        ),
    }
    for qid, (question, options, answer) in fellowship_fixes.items():
        if qid in questions:
            set_q(questions[qid], question=question, options=options, answer=answer)

    # --- Dadasaheb Phalke ---
    phalke = {
        "aca_0055": ("വി. ശാന്താരാം", ["വി. ശാന്താരാം", "സത്യജിത് റേ", "മനോജ് കുമാർ", "പൃഥ്വിരാജ് കപൂർ"]),
        "aca_2788": ("വി. ശാന്താരാം", ["വി. ശാന്താരാം", "സത്യജിത് റേ", "യശ് ചോപ്ര", "ഹൃദയനാഥ് മംഗേഷ്കർ"]),
        "aca_0058": ("എൽ. വി. പ്രസാദ്", ["എൽ. വി. പ്രസാദ്", "മിഥുൻ ചക്രവർത്തി", "നർഗീസ്", "രാജ്കപൂർ"]),
        "aca_0103": ("അടൂർ ഗോപാലകൃഷ്ണൻ", ["അടൂർ ഗോപാലകൃഷ്ണൻ", "രാജ്കപൂർ", "വിനോദ് ഖന്ന", "നാഗരാജ്"]),
        "aca_2100": ("അടൂർ ഗോപാലകൃഷ്ണൻ", ["അടൂർ ഗോപാലകൃഷ്ണൻ", "ദിലീപ് കുമാർ", "നർഗീസ്", "ബി. ആർ. ചോപ്ര"]),
        "aca_0444": ("പി. ജയറാജ്", ["പി. ജയറാജ്", "സൊഹ്റാബ് മോദി", "വിനോദ് ഖന്ന", "അശോക് കുമാർ"]),
        "aca_2670": ("പി. ജയറാജ്", ["പി. ജയറാജ്", "ബി. നാഗേശ്വര റാവു", "ബി. ആർ. ചോപ്ര", "ഹൃദയനാഥ് മംഗേഷ്കർ"]),
        "aca_0764": ("ഗുൽസാർ", ["ഗുൽസാർ", "സത്യജിത് റേ", "ഹൃദയനാഥ് മംഗേഷ്കർ", "കെ. വിശ്വനാഥ്"]),
        "aca_1069": ("അമിതാഭ് ബച്ചൻ", ["അമിതാഭ് ബച്ചൻ", "ലതാ മങ്കേഷ്കർ", "മിഥുൻ ചക്രവർത്തി", "നർഗീസ്"]),
        "aca_1100": ("രജനീകാന്ത്", ["രജനീകാന്ത്", "അശോക് കുമാർ", "നർഗീസ്", "ദേവിക റാണി"]),
        "aca_3069": ("രജനീകാന്ത്", ["രജനീകാന്ത്", "അമിതാഭ് ബച്ചൻ", "ഹൃദയനാഥ് മംഗേഷ്കർ", "മനോജ് കുമാർ"]),
        "aca_1319": ("ബി. നാഗേശ്വര റാവു", ["ബി. നാഗേശ്വര റാവു", "ഭൂപൻ ഹസാരിക", "മനോജ് കുമാർ", "യശ് ചോപ്ര"]),
        "aca_1399": ("വഹീദ റഹ്മാൻ", ["വഹീദ റഹ്മാൻ", "സൊഹ്റാബ് മോദി", "ഹൃദയനാഥ് മംഗേഷ്കർ", "മിഥുൻ ചക്രവർത്തി"]),
        "aca_1853": ("സൗമിത്ര ചാറ്റർജി", ["സൗമിത്ര ചാറ്റർജി", "വഹീദ റഹ്മാൻ", "ഹൃദയനാഥ് മംഗേഷ്കർ", "വിനോദ് ഖന്ന"]),
        "aca_2395": ("സൗമിത്ര ചാറ്റർജി", ["സൗമിത്ര ചാറ്റർജി", "സത്യജിത് റേ", "ദിലീപ് കുമാർ", "പൃഥ്വിരാജ് കപൂർ"]),
        "aca_1966": ("മിഥുൻ ചക്രവർത്തി", ["മിഥുൻ ചക്രവർത്തി", "നാഗരാജ്", "ദേവിക റാണി", "ഭൂപൻ ഹസാരിക"]),
        "aca_2036": ("മിഥുൻ ചക്രവർത്തി", ["മിഥുൻ ചക്രവർത്തി", "വിനോദ് ഖന്ന", "ഷബാനാ ആസ്മി", "ബാലസാഹേബ് താക്കറേ"]),
        "aca_2074": ("ബി. എൻ. സർക്കാർ", ["ബി. എൻ. സർക്കാർ", "സൊഹ്റാബ് മോദി", "വഹീദ റഹ്മാൻ", "വിനോദ് ഖന്ന"]),
        "aca_2296": ("ബി. എൻ. സർക്കാർ", ["ബി. എൻ. സർക്കാർ", "സൊഹ്റാബ് മോദി", "വഹീദ റഹ്മാൻ", "ഹൃദയനാഥ് മംഗേഷ്കർ"]),
        "aca_2617": ("രാജ്കപൂർ", ["രാജ്കപൂർ", "വഹീദ റഹ്മാൻ", "മനോജ് കുമാർ", "ഭൂപൻ ഹസാരിക"]),
        "aca_2724": ("ഷാഹ് റുഖ് ഖാൻ", ["ഷാഹ് റുഖ് ഖാൻ", "രജനീകാന്ത്", "മനോജ് കുമാർ", "അശോക് കുമാർ"]),
    }
    for qid, (answer, options) in phalke.items():
        if qid in questions:
            set_q(questions[qid], answer=answer, options=options)


def main() -> None:
    data = json.loads(AWARDS.read_text(encoding="utf-8"))
    by_id = {q["id"]: q for q in data["questions"] if "id" in q}
    fix_by_id(by_id)
    AWARDS.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Patched awards.json ({len(by_id)} questions)")


if __name__ == "__main__":
    main()
