#!/usr/bin/env python3
"""Generate tail Malayalam categories from English _gen_build blocks + translation dicts."""
from __future__ import annotations

import ast
import pprint
import re
from pathlib import Path

ROOT = Path(__file__).parent
GEN = ROOT / "_gen_build_economics_wave20_data.py"
REST = ROOT / "_gen_economics_ml_rest.py"
ML_BUILD = ROOT / "build_economics_ml_data.py"
BUILD_OUT = ROOT / "build_economics_wave20_data.py"

ALLOWED = re.compile(
    r"\b(RBI|SEBI|GST|IMF|WTO|CPI|GDP|FDI|FII|HDI|MSP|NPS|UPI|NPCI|FRBM|SEZ|PLI|PMJDY|"
    r"NSDL|CDSL|IPO|FPO|ETF|QIP|ADR|GDR|LIC|IRDAI|ULIP|PFRDA|PMJJBY|PMSBY|PMJAY|GIC|"
    r"EPFO|ESIC|PMKVY|PLFS|FCI|NABARD|APMC|CACP|KCC|NPOP|ICAR|NAFED|CGST|SGST|IGST|GSTN|"
    r"CBDT|CBIC|GAAR|DTAA|UIDAI|DBT|OCEN|ONDC|PMJDY|CCI|STPI|EOU|PMKISAN|PMFBY)\b",
    re.I,
)


def tr_en(text: str, ans: dict[str, str], stem: dict[str, str]) -> str:
    if text in stem:
        return stem[text]
    if text in ans:
        return ans[text]
    for k, v in sorted(ans.items(), key=lambda x: -len(x[0])):
        if k in text:
            text = text.replace(k, v)
    return text


def load_dicts() -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    text = ML_BUILD.read_text(encoding="utf-8")
    text = text.split('print("This script')[0]
    text = re.sub(r"^GEN = .*$", "", text, flags=re.M)
    text = re.sub(r"^OUT = .*$", "", text, flags=re.M)
    ns: dict = {}
    exec(text, ns)
    return ns["ANS"], ns["STEM"], ns["PAIR_ML"]


def _load_block(name: str, kind: str) -> str:
    for src in (GEN, BUILD_OUT):
        code = src.read_text(encoding="utf-8")
        marker = f"{name}: list[{kind}] = ["
        if marker not in code:
            continue
        idx = code.index(marker)
        list_start = idx + len(marker) - 1
        depth = 0
        for i in range(list_start, len(code)):
            if code[i] == "[":
                depth += 1
            elif code[i] == "]":
                depth -= 1
                if depth == 0:
                    return code[idx : i + 1]
    raise SystemExit(f"missing {name}")


def load_en_facts(name: str) -> list:
    ns: dict = {"_f": lambda s, a, w, d="medium": (s, a, w, d)}
    exec(_load_block(name, "Fact"), ns)
    return ns[name]


def load_en_triples(name: str) -> list:
    ns: dict = {}
    exec(_load_block(name, "Triple"), ns)
    return ns[name]


def load_en_pairs(name: str) -> list:
    ns: dict = {}
    exec(_load_block(name, "Pair"), ns)
    return ns[name]


def translate_facts(facts: list, ans: dict, stem: dict) -> list[tuple]:
    out = []
    for s, a, w, d in facts:
        out.append((tr_en(s, ans, stem), tr_en(a, ans, stem), [tr_en(x, ans, stem) for x in w], d))
    return out


def translate_pairs(pairs: list, pair_ml: dict) -> list[tuple]:
    by_acr = {
        "LIC": "ജീവൻ ഇൻ shutil",
        "IRDAI": "ഇൻ shutil നിയന്ത്രണം",
        "EPFO": "തൊഴിലാളി ഭവിഷ്യ നിധി",
        "NPS": "ദേശീയ പെൻഷൻ",
        "PFRDA": "പെൻഷൻ നിയന്ത്രണം",
        "PMJJBY": "ജീവൻ ഇൻ shutil പദ്ധതി",
        "PMSBY": "അപകട ഇൻ shutil പദ്ധതി",
        "PMJAY": "ആരോഗ്യ ഇൻ shutil പദ്ധതി",
        "GIC": "പുനരിശ്വാസന",
        "ULIP": "യൂണിറ്റ് ലിങ്ക് ഇൻ shutil",
        "PMFBY": "വിള ഇൻ shutil",
        "APY": "അatal പENSION",
    }
    ins = "\u0d07\u0d7b\u0d37\u0d41\u0d31\u0d3e\u0d7b\u0d38\u0d4d"
    out = []
    for a, b in pairs:
        ml = by_acr.get(a, pair_ml.get(b, tr_en(b, {}, {})))
        out.append((a, ml.replace("ഇൻ shutil", ins).replace("അatal പENSION", "അatal പENSION")))
    return out


def scrub(s: str, bulk: dict[str, str]) -> str:
    for k, v in sorted(bulk.items(), key=lambda x: -len(x[0])):
        if k and k in s:
            s = s.replace(k, v)
    return s


def scrub_facts(facts: list, bulk: dict[str, str]) -> list[tuple]:
    return [(scrub(s, bulk), scrub(a, bulk), [scrub(x, bulk) for x in w], d) for s, a, w, d in facts]


EXTRA_ANS = {
    "special economic zone": "പ്രത്യേക സാമ്പത്തിക zone",
    "export promotion investment": "കയറ്റുമതി പ്രോത്സാഹനവും നിക്ഷേപവും",
    "manufacturing incentive": "നിർമ്മാണ പ്രോത്സാഹനം",
    "Kandla": "കന്ദ്‌ല",
    "central goods and services tax": "കേന്ദ്ര GST",
    "state goods and services tax": "സംസ്ഥാന GST",
    "inter state GST": "അന്തർസംസ്ഥാന GST",
    "National Payments Corporation of India": "ദേശീയ പേയ്മെന്റ് കോർപ്പറേഷൻ",
    "financial inclusion bank accounts": "സാമ്പത്തിക ഉൾപ്പെടുത്തൽ ബാങ്ക് അക്കൗണ്ടുകൾ",
    "direct benefit transfer": "നേരിട്ടുള്ള ആനുകൂല്യ കൈമാറ്റം",
    "Jan Dhan Aadhaar Mobile": "ജനധന-ആധാർ-മൊബൈൽ",
    "game theory concept": "ഗെയിം തിയറി ആശയം",
    "classical economics": "ശാസ്ത്രീയ സാമ്പത്തികശാസ്ത്രം",
    "demand management": "ചോദനാ നിയന്ത്രണം",
    "trade theory": "വ്യാപാര സിദ്ധാന്തം",
    "partial equilibrium": "ഭാഗിക സമതുല്യം",
    "capability approach": "സാമർത്ഥ്യ സമീപനം",
    "heavy industry": "ഭാരമേറിയ വ്യവസായം",
    "population theory": "ജനസംഖ്യാ സിദ്ധാന്തം",
    "creative destruction": "സർജനാവകാശ നശിപ്പ്",
    "innovation": "നവീകരണം",
    "interest inflation": "പലിശ-പണപ്പെരുപ്പം",
    "welfare economics": "ക്ഷേമ സാമ്പത്തികശാസ്ത്രം",
    "Wealth of Nations": "ദേശത്തിന്റെ സമ്പദ്‌വിത്തം",
    "Das Kapital": "മൂലധനം",
    "General Theory": "പൊതു സിദ്ധാന്തം",
    "comparative advantage": "താരതമ്യ മേന്മ",
    "Principles of Economics": "സാമ്പത്തികശാസ്ത്രത്തിന്റെ തത്വങ്ങൾ",
    "monetarism": "നാണയവാദം",
    "money supply": "നാണയ_supply",
    "Development as Freedom": "വികസനം സ്വാതന്ത്ര്യമായി",
    "Mahalanobis model": "മഹാലനോബിസ് മാതൃക",
    "self reliance village economy": "സ്വയംപര്യാപ്ത ഗ്രാമ ekonomi",
    "Indian industrialists plan": "ഇന്ത്യൻ实业家 പദ്ധതി",
    "Asian Drama": "ഏഷ്യൻ നാടകം",
    "dual sector surplus labour": "ദ്വി-മേഖല അധിക തൊഴിൽ",
    "growth savings capital output": "വളർച്ച-സമ്പാദ്യ-മൂലധന-ഉൽപ്പാ�adan",
    "long run growth technology": "ദീർഘകാല വളർച്ച-technology",
    "income inequality development": "വരുമാന അസമത്വ-വികസനം",
    "tax rate revenue relation": "നികുതി നിരക്ക്-വരുമാന ബന്ധം",
    "A W Phillips": "എ.ഡബ്ല്യു. ഫില്ലിപ്സ്",
    "Thomas Malthus": "തോമസ് മാൽത്തസ്",
    "Thorstein Veblen": "തോർസ്റ്റിൻ വെബ്ലൻ",
    "Joseph Schumpeter": "ജോസഫ് ഷംപീറ്റർ",
    "Irving Fisher": "ഇർവിംഗ് ഫിഷർ",
    "Vilfredo Pareto": "വിൽഫ്രെഡോ പരേറ്റോ",
    "Indian Nobel economics": "ഇന്ത്യയിലെ സാമ്പത്തികശാസ്ത്ര നൊബൽ",
}

EXTRA_STEM = {
    "SEZ-ന്റെ പൂർണ്ണ രൂപം?": "SEZ-ന്റെ പൂർണ്ണ രൂപം?",
    "comparative advantage theory?": "താരതമ്യ മേന്മ സിദ്ധാന്തം?",
    "invisible hand concept?": "അദൃശ്യ കൈ ആശയം?",
    "Indian Nobel economics?": "ഇന്ത്യയിലെ സാമ്പത്തികശാസ്ത്ര നൊബൽ?",
}


def main() -> None:
    ans, stem, pair_ml = load_dicts()
    ans.update(EXTRA_ANS)
    stem.update(EXTRA_STEM)

    triples_en = load_en_triples("ECONOMIC_THINKERS")
    triples = [
        (p if not p[0].isascii() else tr_en(p, ans, stem), tr_en(w, ans, stem), tr_en(f, {**ans, "surplus value": "അധികമൂല്യം", "food limits": "ഭക്ഷ്യ പരിമിതി", "Fisher equation": "ഫിഷർ സമവാക്യം", "Pareto efficiency": "പരേറ്റോ കാര്യക്ഷമത"}, stem))
        for p, w, f in triples_en
    ]
    # Malayalam person names for Latin-only entries
    name_fix = {
        "Thomas Malthus": "തോമസ് മാൽത്തസ്",
        "Joseph Schumpeter": "ജോസഫ് ഷംപീറ്റർ",
        "Irving Fisher": "ഇർവിംഗ് ഫിഷർ",
        "Vilfredo Pareto": "വിൽഫ്രെഡോ പരേറ്റോ",
    }
    triples = [(name_fix.get(p, p), w, f) for p, w, f in triples]

    thinker_extra = translate_facts(load_en_facts("THINKER_EXTRA"), ans, stem)
    try:
        thinker_more = translate_facts(load_en_facts("ECONOMIC_THINKERS"), ans, stem)
    except SystemExit:
        thinker_more = []
    seen = {s for s, _, _, _ in thinker_extra}
    for row in thinker_more:
        if row[0] not in seen:
            thinker_extra.append(row)
            seen.add(row[0])
    thinker_extra = thinker_extra[:25]

    ins = "\u0d07\u0d7b\u0d37\u0d41\u0d31\u0d3e\u0d7b\u0d38\u0d4d"
    pairs = [
        ("LIC", f"ജീവൻ {ins}"),
        ("IRDAI", f"{ins} നിയന്ത്രണം"),
        ("EPFO", "തൊഴിലാളി ഭവിഷ്യ നിധി"),
        ("NPS", "ദേശീയ പെൻഷൻ"),
        ("PFRDA", "പെൻഷൻ നിയന്ത്രണം"),
        ("PMJJBY", f"ജീവൻ {ins} പദ്ധതി"),
        ("PMSBY", f"അപകട {ins} പദ്ധതി"),
        ("PMJAY", f"ആരോഗ്യ {ins} പദ്ധതി"),
        ("GIC", "പുനരിശ്വാസന"),
        ("ULIP", f"യൂണിറ്റ് ലിങ്ക് {ins}"),
        ("PMFBY", f"വിള {ins}"),
        ("APY", "അatal പENSION"),
    ]

    cats = {
        "INDUSTRIAL_SEZ": translate_facts(load_en_facts("INDUSTRIAL_SEZ"), ans, stem),
        "PUBLIC_FINANCE_TAX": translate_facts(load_en_facts("PUBLIC_FINANCE_TAX"), ans, stem),
        "DIGITAL_CONSUMER": translate_facts(load_en_facts("DIGITAL_CONSUMER"), ans, stem),
        "THINKER_EXTRA": thinker_extra,
    }
    bulk = {**ans, **EXTRA_ANS}
    cats = {k: scrub_facts(v, bulk) for k, v in cats.items()}
    thinker_extra = cats["THINKER_EXTRA"]

    head = REST.read_text(encoding="utf-8").split("INSURANCE_PENSION")[0].rstrip() + "\n\n"
    ins = REST.read_text(encoding="utf-8")
    ins_block = ins[ins.index("INSURANCE_PENSION"):].split("\n\n")[0] + "\n"

    parts = [head, ins_block, "\n"]
    parts.append(f"INSURANCE_INST: list[Pair] = {pprint.pformat(pairs, width=120)}\n\n")
    parts.append(f"ECONOMIC_THINKERS: list[Triple] = {pprint.pformat(triples, width=120)}\n\n")
    for name, rows in cats.items():
        parts.append(f"{name}: list[Fact] = {pprint.pformat(rows, width=120)}\n\n")
    REST.write_text("".join(parts), encoding="utf-8")
    text = REST.read_text(encoding="utf-8")
    text = text.replace("'മധ്യം'", "'medium'").replace("'കഠിനം'", "'hard'").replace("'ലളിതം'", "'easy'")
    REST.write_text(text, encoding="utf-8")
    print("Wrote", REST)
    for k, v in cats.items():
        print(k, len(v))
    print("pairs", len(pairs), "triples", len(triples))

if __name__ == "__main__":
    main()
