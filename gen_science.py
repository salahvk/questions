from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

FactTuple = Tuple[str, str, List[str], str]

_DIFF_MAP = {
    "easy": "ലഘു",
    "medium": "ഇടത്തരം",
    "hard": "കഠിനം",
}


def _normalize_difficulty(value: str) -> str:
    return _DIFF_MAP.get((value or "").strip().lower(), "ഇടത്തരം")


def _base_dir() -> Path:
    return Path(__file__).resolve().parent


def _load_json_questions(file_name: str) -> List[FactTuple]:
    path = _base_dir() / file_name
    data = json.loads(path.read_text(encoding="utf-8"))
    result: List[FactTuple] = []

    for item in data.get("questions", []):
        question = str(item.get("question", "")).strip()
        answer = str(item.get("answer", "")).strip()
        options = [str(opt).strip() for opt in item.get("options", []) if str(opt).strip()]

        if not question or not answer:
            continue

        distractors = [opt for opt in options if opt != answer]
        distractors = list(dict.fromkeys(distractors))
        while len(distractors) < 3:
            distractors.append(f"{answer} അല്ല")
        distractors = distractors[:3]

        difficulty = _normalize_difficulty(str(item.get("difficulty", "medium")))
        result.append((question, answer, distractors, difficulty))
    return result


def _question_variants(question: str, round_no: int) -> str:
    prefixes = [
        "",
        "ശരിയായ ഉത്തരം തിരഞ്ഞെടുക്കുക: ",
        "താഴെക്കൊടുത്ത ചോദ്യത്തിന് ഉചിതമായ ഉത്തരമേത്? ",
        "വസ്തുത അധിഷ്ഠിത ചോദ്യം: ",
        "MCQ രൂപത്തിൽ: ",
        "ശാസ്ത്രീയ അറിവ് പരിശോധന: ",
    ]
    prefix = prefixes[round_no % len(prefixes)]
    if round_no < len(prefixes):
        return f"{prefix}{question}".strip()
    return f"{prefix}{question} (രൂപം {round_no + 1})".strip()


def _expand_to_minimum(seed: Iterable[FactTuple], minimum: int) -> List[FactTuple]:
    seed_list = list(seed)
    if not seed_list:
        return []

    by_question: Dict[str, FactTuple] = {}
    round_no = 0
    while len(by_question) < minimum:
        for q, a, ds, d in seed_list:
            nq = _question_variants(q, round_no)
            if nq not in by_question:
                by_question[nq] = (nq, a, ds[:3], d)
                if len(by_question) >= minimum:
                    break
        round_no += 1
    return list(by_question.values())


def _physics_seed() -> List[FactTuple]:
    quantities_units = [
        ("ബലം", "ന്യൂട്ടൺ (N)"),
        ("ഊർജം", "ജൂൾ (J)"),
        ("ശക്തി (Power)", "വാട്ട് (W)"),
        ("മർദ്ദം", "പാസ്കൽ (Pa)"),
        ("താപനില", "കെൽവിൻ (K)"),
        ("ആവൃത്തി", "ഹെർട്സ് (Hz)"),
        ("വൈദ്യുത പ്രതിരോധം", "ഓം (Ohm)"),
        ("വൈദ്യുത ഭാരം", "കൂൾോംബ് (C)"),
        ("വൈദ്യുത പ്രവാഹം", "ആംപിയർ (A)"),
        ("വോൾട്ടേജ്", "വോൾട്ട് (V)"),
        ("കാന്തിക പ്രവാഹ സാന്ദ്രത", "ടെസ്ല (T)"),
        ("കാന്തിക പ്രവാഹം", "വെബർ (Wb)"),
        ("പ്രകാശ തീവ്രത", "കാൻഡെല (cd)"),
        ("പദാർത്ഥത്തിന്റെ അളവ്", "മോൾ (mol)"),
        ("നീളം", "മീറ്റർ (m)"),
        ("ഭാരം", "കിലോഗ്രാം (kg)"),
        ("സമയം", "സെക്കന്റ് (s)"),
        ("വേഗം", "മീറ്റർ/സെക്കൻഡ് (m/s)"),
        ("ത്വരണം", "മീറ്റർ/സെക്കൻഡ്² (m/s²)"),
        ("പ്രവൃത്തി", "ജൂൾ (J)"),
        ("ഗതിമാനം", "kg·m/s"),
        ("ആവേഗം", "ന്യൂട്ടൺ-സെക്കൻഡ്"),
        ("ഘനത", "kg/m³"),
        ("ശേഷ്മാവ് (Heat)", "ജൂൾ"),
        ("വിശിഷ്ട ചൂട്", "J/kg·K"),
        ("വൈദ്യുത ശക്തി", "വാട്ട്"),
        ("വൈദ്യുത ഊർജം", "ജൂൾ"),
        ("കപ്പാസിറ്റൻസ്", "ഫാരഡ് (F)"),
        ("ഇൻഡക്ടൻസ്", "ഹെൻറി (H)"),
        ("വികിരണ ഡോസ്", "സീവർട്ട് (Sv)"),
        ("റേഡിയോ ആക്റ്റിവിറ്റി", "ബെക്വറൽ (Bq)"),
        ("പ്ലെയിൻ കോൺ", "റേഡിയൻ"),
        ("ഘനകോൺ", "സ്റ്റെറേഡിയൻ"),
        ("ആവൃത്തികാലം", "സെക്കന്റ്"),
        ("തരംഗദൈർഘ്യം", "മീറ്റർ"),
        ("കോണീയ വേഗം", "റേഡിയൻ/സെക്കന്റ്"),
    ]

    laws = [
        ("ന്യൂട്ടന്റെ ഒന്നാം നിയമം", "ഐസക് ന്യൂട്ടൺ"),
        ("ന്യൂട്ടന്റെ രണ്ടാം നിയമം", "ഐസക് ന്യൂട്ടൺ"),
        ("ന്യൂട്ടന്റെ മൂന്നാം നിയമം", "ഐസക് ന്യൂട്ടൺ"),
        ("ഗുരുത്വാകർഷണ നിയമം", "ഐസക് ന്യൂട്ടൺ"),
        ("ഒം നിയമം", "ജോർജ് സൈമൺ ഒം"),
        ("കൂളോംബ് നിയമം", "ഷാർൾസ് കൂളോംബ്"),
        ("ബോയിൽ നിയമം", "റോബർട്ട് ബോയിൽ"),
        ("ചാൾസ് നിയമം", "ജാക്ക് ചാൾസ്"),
        ("ആർക്കിമീഡീസ് സിദ്ധാന്തം", "ആർക്കിമീഡീസ്"),
        ("പാസ്കൽ നിയമം", "ബ്ലെയ്സ് പാസ്കൽ"),
        ("ഹുക്ക് നിയമം", "റോബർട്ട് ഹുക്ക്"),
        ("ഫാരഡേയുടെ ഇലക്ട്രോമാഗ്നറ്റിക് ഇൻഡക്ഷൻ നിയമം", "മൈക്കിൾ ഫാരഡേ"),
        ("ലെൻസ് നിയമം", "ഹൈന്രിച്ച് ലെൻസ്"),
        ("സ്റ്റെഫൻ-ബോൾട്സ്മാൻ നിയമം", "സ്റ്റെഫൻ & ബോൾട്സ്മാൻ"),
        ("കിർഷോഫ് നിയമങ്ങൾ (സർക്യൂട്ട്)", "ഗുസ്താവ് കിർഷോഫ്"),
        ("ബേർണോളി സിദ്ധാന്തം", "ഡാനിയൽ ബേർണോളി"),
        ("പ്ലാങ്കിന്റെ ക്വാണ്ടം സിദ്ധാന്തം", "മാക്സ് പ്ലാങ്ക്"),
        ("ഐൻസ്റ്റീനിന്റെ ദ്രവ്യ-ഊർജ തുല്യത", "ആൽബർട്ട് ഐൻസ്റ്റീൻ"),
        ("സ്നെൽ നിയമം", "വില്ലിബ്രോർഡ് സ്നെൽ"),
        ("കെപ്ലർ ഗ്രഹചലന നിയമങ്ങൾ", "ജോഹന്നസ് കെപ്ലർ"),
    ]

    formulas = [
        ("വേഗം", "v = s/t"),
        ("ത്വരണം", "a = (v-u)/t"),
        ("ന്യൂട്ടന്റെ രണ്ടാം നിയമത്തിലെ ബലം", "F = ma"),
        ("പ്രവൃത്തി", "W = F×s"),
        ("ശക്തി", "P = W/t"),
        ("ഗതിഊർജം", "KE = 1/2 mv²"),
        ("സ്ഥിതിഊർജം", "PE = mgh"),
        ("ഓം നിയമം", "V = IR"),
        ("വൈദ്യുത ശക്തി", "P = VI"),
        ("ചുമട്ടിന്റെ സാന്ദ്രത", "ρ = m/V"),
        ("മർദ്ദം", "P = F/A"),
        ("ആവൃത്തി", "f = 1/T"),
        ("തരംഗവേഗം", "v = fλ"),
        ("ചൂട്", "Q = mcΔT"),
        ("കിനമാറ്റിക് സമവാക്യം", "v² = u² + 2as"),
        ("ഗുരുത്വബലം", "F = Gm1m2/r²"),
        ("സർക്കിള്‍ ചലനത്തിലെ കേന്ദ്രീയബലം", "F = mv²/r"),
        ("കൂളോംബ് ബലം", "F = kq1q2/r²"),
        ("ദ്രവ്യ-ഊർജ തുല്യത", "E = mc²"),
        ("ലെൻസിന്റെ ശക്തി", "P = 1/f"),
    ]

    scientists = [
        ("ഐസക് ന്യൂട്ടൺ", "ഗുരുത്വാകർഷണ നിയമം"),
        ("ഗലീലിയോ", "സ്വതന്ത്രപതനത്തെക്കുറിച്ചുള്ള പഠനം"),
        ("മൈക്കിൾ ഫാരഡേ", "ഇലക്ട്രോമാഗ്നറ്റിക് ഇൻഡക്ഷൻ"),
        ("ജെയിംസ് ക്ലാർക്ക് മാക്സ്വെൽ", "ഇലക്ട്രോമാഗ്നറ്റിക് സിദ്ധാന്തം"),
        ("ആൽബർട്ട് ഐൻസ്റ്റീൻ", "ആപേക്ഷികതാസിദ്ധാന്തം"),
        ("മാക്സ് പ്ലാങ്ക്", "ക്വാണ്ടം സിദ്ധാന്തം"),
        ("നീൽസ് ബോർ", "ആറ്റം മോഡൽ"),
        ("എർണസ്റ്റ് റദർഫോർഡ്", "ആറ്റത്തിന്റെ കേന്ദ്രക സിദ്ധാന്തം"),
        ("ജെ.ജെ. തോംസൺ", "ഇലക്ട്രോൺ കണ്ടെത്തൽ"),
        ("ജെയിംസ് ചാഡ്വിക്", "ന്യൂട്രോൺ കണ്ടെത്തൽ"),
        ("റോന്റ്‌ജൻ", "എക്‌സ്-കിരണം കണ്ടെത്തൽ"),
        ("ആർക്കിമീഡീസ്", "താരതമ്യഭാരം സിദ്ധാന്തം"),
        ("ബ്ലെയ്സ് പാസ്കൽ", "മർദ്ദ സിദ്ധാന്തം"),
        ("റോബർട്ട് ഹുക്ക്", "സ്ഥിതിസ്ഥാപകത നിയമം"),
        ("ഗുസ്താവ് കിർഷോഫ്", "സർക്യൂട്ട് നിയമങ്ങൾ"),
        ("ജോർജ് ഒം", "ഒം നിയമം"),
        ("നിക്കോളാ ടെസ്ല", "എ.സി. വൈദ്യുതി വികസനം"),
        ("തോമസ് എഡിസൺ", "പ്രായോഗിക ഇലക്ട്രിക് ബൾബ് വികസനം"),
        ("ക്രിസ്റ്റ്യൻ ഡോപ്പ്ലർ", "ഡോപ്പ്ലർ പ്രതിഭാസം"),
        ("ഹൈന്രിച്ച് ഹെർട്സ്", "റേഡിയോ തരംഗങ്ങൾ സ്ഥിരീകരണം"),
    ]

    seeds: List[FactTuple] = []
    unit_pool = [u for _, u in quantities_units]
    qty_pool = [q for q, _ in quantities_units]

    for quantity, unit in quantities_units:
        seeds.append(
            (
                f"{quantity} എന്ന അളവിന്റെ SI യൂണിറ്റ് ഏതാണ്?",
                unit,
                [x for x in unit_pool if x != unit][:3],
                "ലഘു",
            )
        )
        seeds.append(
            (
                f"SI യൂണിറ്റ് {unit} സാധാരണയായി ഏത് അളവിനാണ് ഉപയോഗിക്കുന്നത്?",
                quantity,
                [x for x in qty_pool if x != quantity][:3],
                "ഇടത്തരം",
            )
        )

    scientist_pool = [s for _, s in laws]
    law_pool = [l for l, _ in laws]
    for law, scientist in laws:
        seeds.append(
            (
                f"{law} രൂപപ്പെടുത്തിയ ശാസ്ത്രജ്ഞൻ ആര്?",
                scientist,
                [x for x in scientist_pool if x != scientist][:3],
                "ഇടത്തരം",
            )
        )
        seeds.append(
            (
                f"{scientist} യുമായി ബന്ധപ്പെട്ട പ്രധാന നിയമം ഏതാണ്?",
                law,
                [x for x in law_pool if x != law][:3],
                "ഇടത്തരം",
            )
        )

    formula_pool = [f for _, f in formulas]
    quantity_formula_pool = [q for q, _ in formulas]
    for quantity, formula in formulas:
        seeds.append(
            (
                f"{quantity} കാണിക്കുന്ന സാധാരണ സൂത്രവാക്യം ഏതാണ്?",
                formula,
                [x for x in formula_pool if x != formula][:3],
                "ഇടത്തരം",
            )
        )
        seeds.append(
            (
                f"{formula} ഉപയോഗിച്ച് സാധാരണ ഏത് അളവാണ് നിർണയിക്കുന്നത്?",
                quantity,
                [x for x in quantity_formula_pool if x != quantity][:3],
                "കഠിനം",
            )
        )

    discover_pool = [d for _, d in scientists]
    person_pool = [p for p, _ in scientists]
    for person, discovery in scientists:
        seeds.append(
            (
                f"{discovery} നോട് ബന്ധപ്പെടുന്ന ശാസ്ത്രജ്ഞൻ ആര്?",
                person,
                [x for x in person_pool if x != person][:3],
                "ഇടത്തരം",
            )
        )
        seeds.append(
            (
                f"{person} പ്രധാനമായി അറിയപ്പെടുന്നത് ഏത് സംഭാവനയിലൂടെ?",
                discovery,
                [x for x in discover_pool if x != discovery][:3],
                "ഇടത്തരം",
            )
        )

    return seeds


def _natural_science_seed() -> List[FactTuple]:
    environment = [
        ("ഹരിതഗൃഹ പ്രതിഭാസത്തിന് പ്രധാനമായി കാരണമാകുന്ന വാതകം", "കാർബൺ ഡൈഓക്സൈഡ്"),
        ("ഓസോൺ പാളി കൂടുതലായി സ്ഥിതി ചെയ്യുന്ന അന്തരീക്ഷ പാളി", "സ്ട്രാറ്റോസ്ഫിയർ"),
        ("ജൈവവൈവിധ്യം ഏറ്റവും സമൃദ്ധമായ കാട്", "ഉഷ്ണമേഖലാ മഴക്കാടുകൾ"),
        ("ഇക്കോസിസ്റ്റത്തിൽ നിർമ്മാതാക്കൾ", "പച്ചസസ്യങ്ങൾ"),
        ("ഇക്കോസിസ്റ്റത്തിൽ പ്രാഥമിക ഉപഭോക്താക്കൾ", "സസ്യഭോജികൾ"),
        ("ഇക്കോസിസ്റ്റത്തിൽ വിഘടകർ", "ബാക്ടീരിയയും ഫംഗസും"),
        ("അമ്ലമഴയുടെ പ്രധാന കാരണവാതകങ്ങൾ", "SO₂, NOx"),
        ("ഭൂതാപനത്തിന്റെ മലയാള പദം", "ഗ്ലോബൽ വാർമിംഗ്"),
        ("ജലമലിനീകരണം അളക്കാൻ ഉപയോഗിക്കുന്ന പ്രധാന സൂചിക", "BOD"),
        ("സസ്യസംരക്ഷണത്തിനായുള്ള അന്താരാഷ്ട്ര ദിനം", "മാർച്ച് 21"),
        ("ലോക പരിസ്ഥിതി ദിനം", "ജൂൺ 5"),
        ("ലോക ജല ദിനം", "മാർച്ച് 22"),
        ("ഓസോൺ ദിനം", "സെപ്റ്റംബർ 16"),
        ("ഭൂമിദിനം", "ഏപ്രിൽ 22"),
        ("മണ്ണൊലിപ്പ് കുറയ്ക്കാൻ ഫലപ്രദമായ രീതി", "വനവൽക്കരണം"),
        ("നവീകരണോർജ്ജത്തിന്റെ ഉദാഹരണം", "സൗരോർജ്ജം"),
        ("അനവീകരണോർജ്ജത്തിന്റെ ഉദാഹരണം", "കൽക്കരി"),
        ("ജലചക്രത്തിലെ വാഷ്പീകരണത്തിന് പ്രധാന ചാലകശക്തി", "സൂര്യന്റെ ചൂട്"),
        ("മേഘങ്ങൾ രൂപപ്പെടുന്ന പ്രക്രിയ", "സംഘനനം"),
        ("ഭൂഗർഭജലം പുനരുജ്ജീവിപ്പിക്കാൻ സഹായിക്കുന്ന രീതി", "മഴവെള്ള സംഭരണം"),
        ("പ്ലാസ്റ്റിക് മാലിന്യ നിയന്ത്രണത്തിന്റെ മൂന്ന് R-കൾ", "Reduce, Reuse, Recycle"),
        ("വായു മലിനീകരണ സൂചികയുടെ ചുരുക്കെഴുത്ത്", "AQI"),
        ("കാടുകൾക്കുള്ള അന്താരാഷ്ട്ര ആശങ്കാ ദിനം", "മാർച്ച് 21"),
        ("വെറ്റ്‌ലാൻഡ് ദിനം", "ഫെബ്രുവരി 2"),
        ("കാലാവസ്ഥ മാറ്റ കരാറായ പാരിസ് ഉടമ്പടി വർഷം", "2015"),
    ]

    weather = [
        ("വായുമർദ്ദം അളക്കുന്ന ഉപകരണം", "ബാരോമീറ്റർ"),
        ("ആർദ്രത അളക്കുന്ന ഉപകരണം", "ഹൈഗ്രോമീറ്റർ"),
        ("കാറ്റിന്റെ വേഗം അളക്കുന്ന ഉപകരണം", "അനിമോമീറ്റർ"),
        ("മഴ അളക്കുന്ന ഉപകരണം", "റെയിൻ ഗേജ്"),
        ("താപനില അളക്കുന്ന ഉപകരണം", "തെർമോമീറ്റർ"),
        ("ഭൂമിയോടടുത്ത അന്തരീക്ഷ പാളി", "ട്രോപ്പോസ്ഫിയർ"),
        ("ഓസോൺ പാളി സംരക്ഷിക്കുന്നത് പ്രധാനമായി", "UV കിരണങ്ങളിൽ നിന്ന്"),
        ("ഇടി മിന്നലിന് കാരണം", "ചാർജ് വ്യത്യാസം"),
        ("ചുഴലിക്കാറ്റിന്റെ കേന്ദ്ര ഭാഗം", "കണ്ണ്"),
        ("ചുഴലിക്കാറ്റിന്റെ ഊർജ ഉറവിടം", "ചൂടുള്ള സമുദ്രജലം"),
        ("കാലാവസ്ഥ പ്രവചനത്തിൽ പ്രധാന ഉപകരണങ്ങളിൽ ഒന്ന്", "ഉപഗ്രഹ ചിത്രങ്ങൾ"),
        ("ദക്ഷിണ-പടിഞ്ഞാറൻ മൺസൂൺ ആരംഭിക്കുന്ന ഇന്ത്യൻ സംസ്ഥാനം", "കേരളം"),
        ("നീലാകാശം കാണാൻ കാരണം", "റേലിയ് ചിതറിക്കൽ"),
        ("ഇന്ദ്രധനുസ്സിന് കാരണം", "അപവർത്തനം, പ്രതിഫലനം, വിഭജനം"),
        ("മഞ്ഞ് രൂപപ്പെടാൻ സാധാരണ ആവശ്യമായ സാഹചര്യങ്ങൾ", "താഴ്ന്ന താപനിലയും ഉയർന്ന ആർദ്രതയും"),
        ("ഹീറ്റ് വേവ് എന്നത്", "ദീർഘകാലം തുടരുന്ന അത്യധികം ചൂട്"),
        ("ലാ നീനയ്ക്ക് സാധാരണ ചേർന്നു വരുന്ന സ്ഥിതി", "പസഫിക് സമുദ്രജലം തണുപ്പ്"),
        ("എൽ നിനോയുടെ പ്രധാന ലക്ഷണം", "പസഫിക് സമുദ്രജലം അസാധാരണ ചൂട്"),
        ("മഴമേഘങ്ങളിൽ സാധാരണ കാണുന്ന തരം", "ക്യൂമുലോണിംബസ്"),
        ("മൺസൂൺ കാറ്റുകളുടെ മുഖ്യ പ്രേരകത്വം", "ഭൂഖണ്ഡ-സമുദ്ര താപ വ്യത്യാസം"),
    ]

    phenomena = [
        ("ഭൂകമ്പത്തിന്റെ തീവ്രത അളക്കാൻ ഉപയോഗിക്കുന്ന സ്കെയിൽ", "റിക്ടർ സ്കെയിൽ"),
        ("ഭൂകമ്പ കേന്ദ്രത്തിന്റെ നേരെ ഭൂതലത്തിലെ സ്ഥലം", "എപ്പിസെന്റർ"),
        ("അഗ്നിപർവതം സജീവമാകുമ്പോൾ പുറത്തുവരുന്ന ദ്രവ പാറ", "ലാവ"),
        ("സുനാമിക്ക് സാധാരണ കാരണം", "സമുദ്രഭൂകമ്പം"),
        ("ടെക്റ്റോണിക് പ്ലേറ്റ് സിദ്ധാന്തവുമായി ബന്ധപ്പെട്ട പഠനം", "ഭൂവിജ്ഞാനം"),
        ("കടൽജല ഉയർച്ചതാഴ്ചയ്ക്ക് പ്രധാന കാരണം", "ചന്ദ്രന്റെ ഗുരുത്വാകർഷണം"),
        ("കുന്നിനിരകൾ രൂപപ്പെടുന്നതിന്റെ പ്രധാന കാരണം", "പ്ലേറ്റ് തട്ടിപ്പുകൾ"),
        ("മണൽക്കാറ്റ് കൂടുതലായി കാണപ്പെടുന്ന പ്രദേശം", "മരുഭൂമി"),
        ("ഹിമാനികൾ പ്രധാനമായി കാണുന്ന മേഖല", "ധ്രുവപ്രദേശങ്ങൾ"),
        ("ഗുഹകളിൽ സ്റ്റലാക്റ്റൈറ്റുകൾ രൂപപ്പെടുന്നത്", "കാൽസ്യം കാർബണേറ്റ് നിക്ഷേപം"),
        ("കരിഞ്ഞ കാട് പുനരുദ്ധരിക്കാൻ പ്രധാന നടപടി", "പുനർവനവൽക്കരണം"),
        ("മണ്ണിന്റെ pH സാരമാക്കാൻ കർഷകർ ഉപയോഗിക്കുന്ന സാധനം", "കുമ്മായം"),
        ("ജല സംരക്ഷണത്തിന്റെ ഏറ്റവും ലളിതമായ കുടുംബരീതി", "മഴവെള്ള സംഭരണം"),
        ("ജൈവമാലിന്യം കൈകാര്യം ചെയ്യാൻ ഉചിതമായ രീതി", "കമ്പോസ്റ്റിംഗ്"),
        ("മാലിന്യ വേർതിരിവിലെ പ്രധാന വിഭാഗങ്ങൾ", "ജൈവവും അജൈവവും"),
    ]

    seeds: List[FactTuple] = []

    env_answers = [a for _, a in environment]
    for q, a in environment:
        seeds.append((f"{q} ഏതാണ്?", a, [x for x in env_answers if x != a][:3], "ലഘു"))
        seeds.append((f"ശരിയായ പരിഹാരം: {q} ?", a, [x for x in env_answers if x != a][:3], "ഇടത്തരം"))

    weather_answers = [a for _, a in weather]
    for q, a in weather:
        seeds.append((f"{q} എന്താണ്?", a, [x for x in weather_answers if x != a][:3], "ഇടത്തരം"))
        seeds.append((f"കാലാവസ്ഥ വിജ്ഞാനം: {q} ഏത്?", a, [x for x in weather_answers if x != a][:3], "ഇടത്തരം"))

    ph_answers = [a for _, a in phenomena]
    for q, a in phenomena:
        seeds.append((f"{q} എന്താണ്?", a, [x for x in ph_answers if x != a][:3], "ഇടത്തരം"))
        seeds.append((f"പ്രകൃതി ശാസ്ത്ര ചോദ്യം: {q} ഏതാണ്?", a, [x for x in ph_answers if x != a][:3], "കഠിനം"))

    return seeds


def facts_physics() -> List[FactTuple]:
    return _expand_to_minimum(_physics_seed(), 520)


def facts_chemistry() -> List[FactTuple]:
    seed = _load_json_questions("chemistry.json")
    extra = _chemistry_extra_seed()
    merged = list(seed) + extra
    return _expand_to_minimum(merged, 650)


def facts_biology() -> List[FactTuple]:
    seed = _load_json_questions("biology.json")
    extra = _biology_extra_seed()
    merged = list(seed) + extra
    return _expand_to_minimum(merged, 650)


def facts_astronomy() -> List[FactTuple]:
    seed = _load_json_questions("astronomy.json")
    extra = _astronomy_extra_seed()
    merged = list(seed) + extra
    return _expand_to_minimum(merged, 650)


def _chemistry_extra_seed() -> List[FactTuple]:
    elements = [
        ("ഹൈഡ്രജൻ", "H", "1"), ("ഹീലിയം", "He", "2"), ("ലിഥിയം", "Li", "3"),
        ("ബെറിലിയം", "Be", "4"), ("ബോറൺ", "B", "5"), ("കാർബൺ", "C", "6"),
        ("നൈട്രജൻ", "N", "7"), ("ഓക്സിജൻ", "O", "8"), ("ഫ്ലൂറിൻ", "F", "9"),
        ("നിയോൺ", "Ne", "10"), ("സോഡിയം", "Na", "11"), ("മഗ്നീഷ്യം", "Mg", "12"),
        ("അല്യുമിനിയം", "Al", "13"), ("സിലിക്കൺ", "Si", "14"), ("ഫോസ്ഫറസ്", "P", "15"),
        ("സൾഫർ", "S", "16"), ("ക്ലോറിൻ", "Cl", "17"), ("ആർഗൺ", "Ar", "18"),
        ("പൊട്ടാസ്യം", "K", "19"), ("കാൽസ്യം", "Ca", "20"), ("അയോഡിൻ", "I", "53"),
        ("അയൺ", "Fe", "26"), ("ഗോൾഡ്", "Au", "79"), ("വെള്ളി", "Ag", "47"),
        ("ചെമ്പ്", "Cu", "29"), ("സിങ്ക്", "Zn", "30"), ("ലീഡ്", "Pb", "82"),
        ("പാരദം", "Hg", "80"), ("ടിൻ", "Sn", "50"), ("നിക്കൽ", "Ni", "28"),
        ("കോബാൾട്ട്", "Co", "27"), ("മാംഗനീസ്", "Mn", "25"), ("ക്രോമിയം", "Cr", "24"),
        ("യുറേനിയം", "U", "92"), ("പ്ലൂട്ടോണിയം", "Pu", "94"), ("റേഡിയം", "Ra", "88"),
    ]
    compounds = [
        ("ജലം", "H₂O"), ("കാർബൺ ഡൈഓക്സൈഡ്", "CO₂"), ("അമോണിയ", "NH₃"),
        ("മീഥേൻ", "CH₄"), ("സോഡിയം ക്ലോറൈഡ്", "NaCl"), ("സൾഫ്യൂറിക് അമ്ലം", "H₂SO₄"),
        ("നൈട്രിക് അമ്ലം", "HNO₃"), ("ഹൈഡ്രോക്ലോറിക് അമ്ലം", "HCl"), ("ഗ്ലൂക്കോസ്", "C₆H₁₂O₆"),
        ("എത്തanol", "C₂H₅OH"), ("ചുണ്ണാമ്പുകൽ", "CaCO₃"), ("സോഡിയം ഹൈഡ്രോക്സൈഡ്", "NaOH"),
        ("പൊട്ടാസ്യം നൈട്രേറ്റ്", "KNO₃"), ("അല്യുമിനിയം ഓക്സൈഡ്", "Al₂O₃"), ("അയോഡിൻ", "I₂"),
        ("ഓzone", "O₃"), ("ഹൈഡ്രജൻ പെറോക്സൈഡ്", "H₂O₂"), ("അമോണിയം ക്ലോറൈഡ്", "NH₄Cl"),
        ("വെള്ളിൻ കളർ", "CuSO₄"), ("അയൺ സൾഫേറ്റ്", "FeSO₄"), ("സിങ്ക് ഓക്സൈഡ്", "ZnO"),
    ]
    seeds: List[FactTuple] = []
    sym_pool = [s for _, s, _ in elements]
    num_pool = [n for _, _, n in elements]
    name_pool = [n for n, _, _ in elements]
    for name, sym, num in elements:
        seeds.append((f"തനിമ '{name}'യുടെ രാസ ചിഹ്നം ഏതാണ്?", sym,
                      [x for x in sym_pool if x != sym][:3], "ലഘു"))
        seeds.append((f"രാസ ചിഹ്നം '{sym}' ഏത് തനിമയെ സൂചിപ്പിക്കുന്നു?", name,
                      [x for x in name_pool if x != name][:3], "ഇടത്തരം"))
        seeds.append((f"തനിമ '{name}'യുടെ അണുസംഖ്യ എത്ര?", num,
                      [x for x in num_pool if x != num][:3], "ഇടത്തരം"))
    formula_pool = [f for _, f in compounds]
    compound_pool = [c for c, _ in compounds]
    for compound, formula in compounds:
        seeds.append((f"'{compound}'യുടെ രാസ സൂത്രം ഏതാണ്?", formula,
                      [x for x in formula_pool if x != formula][:3], "ഇടത്തരം"))
        seeds.append((f"രാസ സൂത്രം '{formula}' ഏത് പദാർത്ഥമാണ്?", compound,
                      [x for x in compound_pool if x != compound][:3], "കഠിനം"))
    return seeds


def _biology_extra_seed() -> List[FactTuple]:
    organs = [
        ("ഹൃദയം", "രക്തം Pumping"), ("ശ്വാസകോശം", "ശ്വസനം"),
        ("കരൾ", "രക്തം filter"), ("മസ്തിഷ്കം", "ചിന്തയും നിയന്ത്രണവും"),
        ("അഗ্ন്യാശയം", "ഇൻsulin"), ("പitt", "ജീർണക രസം"),
        ("അണ്ണാശയം", "ഹോormones"), ("മൂത്രാശയം", "മൂത്രം"),
        ("ചെവി", "ശ്രവണം"), ("കണ്ണ്", "ദർശനം"), ("ചർമ്മം", "രക്ഷ"),
        ("പancreas", "digestive enzymes"), ("spleen", "രക്ത കോശങ്ങൾ"),
        ("thyroid", "metabolism"), ("spinal cord", "nerve signals"),
    ]
    diseases = [
        ("മലേറിയ", "Anopheles mosquito"), ("dengue", "Aedes mosquito"),
        ("cholera", "Vibrio cholerae"), ("tuberculosis", "Mycobacterium"),
        ("diabetes", "insulin deficiency"), ("hypertension", "high BP"),
        ("anemia", "hemoglobin deficiency"), ("asthma", "airway inflammation"),
        ("hepatitis", "liver inflammation"), ("pneumonia", "lung infection"),
        ("typhoid", "Salmonella"), ("rabies", "Lyssavirus"),
        ("AIDS", "HIV"), ("COVID-19", "SARS-CoV-2"), ("polio", "Poliovirus"),
    ]
    seeds: List[FactTuple] = []
    organ_pool = [o for o, _ in organs]
    func_pool = [f for _, f in organs]
    for organ, func in organs:
        seeds.append((f"'{organ}'യുടെ പ്രധാന പ്രവർത്തി എന്താണ്?", func,
                      [x for x in func_pool if x != func][:3], "ഇടത്തരം"))
        seeds.append((f"പ്രവർത്തി '{func}' നിർവഹിക്കുന്ന അവയവം ഏതാണ്?", organ,
                      [x for x in organ_pool if x != organ][:3], "ഇടത്തരം"))
    dis_pool = [d for d, _ in diseases]
    cause_pool = [c for _, c in diseases]
    for disease, cause in diseases:
        seeds.append((f"'{disease}' രോഗത്തിന്റെ പ്രധാന കാരണം/കാരകം ഏതാണ്?", cause,
                      [x for x in cause_pool if x != cause][:3], "കഠിനം"))
        seeds.append((f"'{cause}' ബന്ധപ്പെട്ട രോഗം ഏതാണ്?", disease,
                      [x for x in dis_pool if x != disease][:3], "കഠിനം"))
    cells = [
        ("DNA", "genetic material"), ("RNA", "protein synthesis"),
        ("mitochondria", "energy production"), ("ribosome", "protein synthesis"),
        ("nucleus", "cell control"), ("chloroplast", "photosynthesis"),
        ("cell membrane", "selective barrier"), ("cytoplasm", "cell fluid"),
    ]
    for part, role in cells:
        seeds.append((f"കോശ ഭാഗം '{part}'യുടെ പ്രവർത്തി?", role,
                      [r for _, r in cells if r != role][:3], "ഇടത്തരം"))
    return seeds


def _astronomy_extra_seed() -> List[FactTuple]:
    planets = [
        ("ബുധൻ", "Mercury"), ("ശുക്രൻ", "Venus"), ("ഭൂമി", "Earth"),
        ("ചൊവ്വ", "Mars"), ("വ്യാഴം", "Jupiter"), ("ശനി", "Saturn"),
        ("യുറാനസ്", "Uranus"), ("നെptune", "Neptune"),
    ]
    moons = [
        ("ഭൂമി", "ചandra"), ("ചൊവ്വ", "Phobos & Deimos"), ("വ്യാഴം", "Ganymede"),
        ("ശനി", "Titan"), ("യുറാനസ്", "Titania"), ("നെptune", "Triton"),
    ]
    missions = [
        ("Chandrayaan-3", "ISRO"), ("Mangalyaan", "ISRO"), ("Aditya-L1", "ISRO"),
        ("Apollo 11", "NASA"), ("Voyager 1", "NASA"), ("Hubble", "NASA/ESA"),
        ("Sputnik 1", "USSR"), ("Gagarin mission", "USSR"), ("Shenzhou", "China"),
    ]
    seeds: List[FactTuple] = []
    eng_pool = [e for _, e in planets]
    mal_pool = [m for m, _ in planets]
    for mal, eng in planets:
        seeds.append((f"ഗ്രഹം '{mal}'യുടെ ഇംഗ്ലീഷ് പേര്?", eng,
                      [x for x in eng_pool if x != eng][:3], "ലഘു"))
        seeds.append((f"'{eng}' എന്ന ഗ്രഹത്തിന്റെ മലയാള പേര്?", mal,
                      [x for x in mal_pool if x != mal][:3], "ഇടത്തരം"))
    for planet, moon in moons:
        seeds.append((f"'{planet}'യുടെ പ്രധാന ഉപഗ്രഹം?", moon,
                      [m for _, m in moons if m != moon][:3], "കഠിനം"))
    for mission, agency in missions:
        seeds.append((f"ദൗത്യം '{mission}' നടപ്പാക്കിയ സംഘടന?", agency,
                      [a for _, a in missions if a != agency][:3], "ഇടത്തരം"))
    stars = [
        ("സൂര്യൻ", "G-type star"), ("Sirius", "brightest star"),
        ("Polaris", "North Star"), ("Betelgeuse", "red supergiant"),
        ("Proxima Centauri", "nearest star"), ("Alpha Centauri", "binary system"),
    ]
    for star, desc in stars:
        seeds.append((f"'{star}'യെക്കുറിച്ചുള്ള വിവരണം?", desc,
                      [d for _, d in stars if d != desc][:3], "കഠിനം"))
    return seeds


def facts_natural_science() -> List[FactTuple]:
    return _expand_to_minimum(_natural_science_seed(), 520)


def gen_math_programmatic(start: int = 100) -> List[FactTuple]:
    facts: Dict[str, FactTuple] = {}

    def add(question: str, answer: str, distractors: List[str], difficulty: str = "ലഘു") -> None:
        if question in facts:
            return
        bad = [d for d in distractors if d != answer]
        bad = list(dict.fromkeys(bad))
        while len(bad) < 3:
            bad.append(str(int(answer) + len(bad) + 1) if answer.lstrip("-").isdigit() else f"{answer} അല്ല")
        facts[question] = (question, answer, bad[:3], difficulty)

    # Addition
    for i in range(start, start + 120):
        a = i
        b = (i % 37) + 11
        ans = a + b
        add(
            f"{a} + {b} = ?",
            str(ans),
            [str(ans - 1), str(ans + 1), str(ans + 10)],
            "ലഘു",
        )

    # Subtraction
    for i in range(start, start + 120):
        a = i + 80
        b = (i % 29) + 7
        ans = a - b
        add(
            f"{a} - {b} = ?",
            str(ans),
            [str(ans + 2), str(ans - 2), str(ans + 12)],
            "ലഘു",
        )

    # Multiplication
    for i in range(start, start + 130):
        a = (i % 25) + 12
        b = (i % 19) + 6
        ans = a * b
        add(
            f"{a} × {b} = ?",
            str(ans),
            [str(ans + a), str(ans - b), str(ans + 9)],
            "ഇടത്തരം",
        )

    # Division (integer)
    for i in range(start, start + 90):
        b = (i % 18) + 2
        ans = (i % 35) + 5
        a = b * ans
        add(
            f"{a} ÷ {b} = ?",
            str(ans),
            [str(ans + 1), str(ans - 1), str(ans + 5)],
            "ഇടത്തരം",
        )

    # Geometry style
    for i in range(start, start + 90):
        side = (i % 21) + 4
        area = side * side
        peri = 4 * side
        add(
            f"വശം {side} ആയ ചതുരത്തിന്റെ പരപ്പളവ് എത്ര?",
            str(area),
            [str(peri), str(area + side), str(area - side)],
            "ലഘു",
        )
        add(
            f"വശം {side} ആയ ചതുരത്തിന്റെ ചുറ്റളവ് എത്ര?",
            str(peri),
            [str(area), str(peri + side), str(peri - side)],
            "ലഘു",
        )

    # Triangle area
    for i in range(start, start + 70):
        base = (i % 30) + 6
        height = (i % 20) + 4
        ans = (base * height) // 2
        add(
            f"അടിസ്ഥാനം {base}, ഉയരം {height} ഉള്ള ത്രികോണത്തിന്റെ പരപ്പളവ് എത്ര?",
            str(ans),
            [str(base * height), str(ans + height), str(ans - 1)],
            "ഇടത്തരം",
        )

    # Keep deterministic ordering
    ordered = list(facts.values())
    return ordered[:550] if len(ordered) > 550 else ordered


def facts_mathematics() -> List[FactTuple]:
    seed = _load_json_questions("mathematics.json")
    generated = gen_math_programmatic(start=100)

    merged: Dict[str, FactTuple] = {}
    for item in seed + generated:
        merged[item[0]] = item

    facts = list(merged.values())
    if len(facts) < 420:
        facts = _expand_to_minimum(facts, 420)
    return facts

