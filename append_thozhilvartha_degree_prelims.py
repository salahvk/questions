#!/usr/bin/env python3
"""Append Mathrubhumi Thozhilvartha / Kerala PSC Degree Prelims Stage III (071/2024) questions."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")


def rows() -> list[tuple[str, str, str, list[str], str, str]]:
    """file, prefix, question, options, answer, difficulty"""
    out: list[tuple[str, str, str, list[str], str, str]] = []

    def add(file: str, prefix: str, q: str, opts: list[str], ans: str, diff: str = "medium") -> None:
        out.append((file, prefix, q.strip(), opts, ans, diff))

    # --- Thozhilvartha solved paper: Q1–8 (images) ---
    add(
        "current_affairs_2026_06.json",
        "ca_2026_06_",
        "ഗ്ലാസ്ഗോയിൽ നടന്ന COP-26-ൽ ഇന്ത്യ പ്രഖ്യാപിച്ച കാലാവസ്ഥാ നടപടിയിൽ "
        "ഇനിപ്പറയുന്നവയിൽ ഏതാണ് ഉൾപ്പെടുത്തിയിട്ടില്ലാത്തത്?",
        [
            "2050-ഓടെ കാർബൺ neutrality കൈവരിക്കുക",
            "500 GW അജൈവ ഇന്ധന ഊർജ്ജം കൈവരിക്കുക",
            "2030-ഓടെ സമ്പദ്വ്യവസ്ഥയുടെ കാർബൺ തീവ്രത 45% കുറയ്ക്കുക",
            "2030-ഓടെ ഒരു ബില്യൺ ടൺ കാർബൺ ഉത്സർജനം കുറയ്ക്കുക",
        ],
        "2050-ഓടെ കാർബൺ neutrality കൈവരിക്കുക",
    )
    add(
        "important_institutions.json",
        "ii_",
        "ഡിആർഡിഒ രൂപീകരണത്തെക്കുറിച്ച് ഇനിപ്പറയുന്ന പ്രസ്താവനകളിൽ ഏതാണ് ശരി?\n"
        "(i) ഇന്ത്യൻ സൈന്യത്തിന്റെ സാങ്കേതിക വികസന സ്ഥാപനങ്ങളെ ലയിപ്പിച്ചാണ് "
        "ഡിആർഡിഒ രൂപീകരിച്ചത്.\n"
        "(ii) ഡിആർഡിഒയിൽ ലയിപ്പിച്ച സ്ഥാപനങ്ങളിലൊന്നാണ് ഡിഫൻസ് സയൻസ് ഓർഗനൈസേഷൻ.\n"
        "(iii) ഡിആർഡിഒ മിസൈൽ വികസന മേഖലയിൽ മാത്രമാണ് പ്രവർത്തിക്കുന്നത്",
        ["i ഉം ii ഉം മാത്രം", "ii ഉം iii ഉം മാത്രം", "i ഉം iii ഉം മാത്രം", "മുകളിലുള്ള എല്ലാം"],
        "i ഉം ii ഉം മാത്രം",
    )

    mat = [
        (
            "തുടർച്ചയായ രണ്ട് പോസിറ്റീവ് പൂർണ്ണസംഖ്യകളുടെ ഗുണനഫലം 132 ആണ്. "
            "വലിയ സംഖ്യയെ മാത്രം 3 കൊണ്ട് കൂട്ടിയാൽ പുതിയ ഗുണനഫലം എത്ര?",
            ["165", "140", "210", "186"],
            "165",
        ),
        (
            "ഒരു ക്ലാസിലെ ആൺകുട്ടികളുടെയും പെൺകുട്ടികളുടെയും അനുപാതം 5:4 ആണ്. "
            "18 ആൺകുട്ടികൾ കൂടി ചേർന്നാൽ അനുപാതം 7:4 ആയി മാറുന്നു. പെൺകുട്ടികളുടെ എണ്ണം?",
            ["36", "18", "24", "48"],
            "36",
        ),
        (
            "ഒരു കടയുടമ വസ്തുവിന്റെ വില 25% കൂടുതലായി അടയാളപ്പെടുത്തി 20% കിഴിവ് "
            "നൽകുന്നു. അയാളുടെ ലാഭം അല്ലെങ്കിൽ നഷ്ടം?",
            ["5% ലാഭം", "4% ലാഭം", "ലാഭമില്ല, നഷ്ടമില്ല", "5% നഷ്ടം"],
            "ലാഭമില്ല, നഷ്ടമില്ല",
        ),
        ("x = 1/0.2 + 3/0.4 ആണെങ്കിൽ, x/0.5 = ?", ["0.25", "25", "250", "2.5"], "25", "easy"),
        ("60 - 24 ÷ 3 × 2 + 4 = ?", ["36", "40", "44", "48"], "48", "easy"),
        (
            "ഒരേ ഉയരമുള്ള സിലിണ്ടറുകളുടെ വ്യാപ്തം 16:25 അനുപാതത്തിലാണ്. "
            "വളഞ്ഞ പ്രതലവിസ്തീർണ്ണത്തിന്റെ അനുപാതം?",
            ["16:25", "8:10", "4:5", "5:4"],
            "4:5",
        ),
        (
            "16-ന്റെ തുടർച്ചയായ മൂന്ന് ഗുണിതങ്ങളുടെ ശരാശരി 432. മധ്യ ഗുണിതം?",
            ["432", "414", "400", "416"],
            "432",
        ),
        (
            "ONE = 37, TWO = 61 എന്ന കോഡിൽ SIX = ?",
            ["55", "52", "58", "56"],
            "52",
            "hard",
        ),
        (
            "ശ്രേണി: 2, 8, 18, 32, 50, 72, ?",
            ["98", "95", "90", "102"],
            "98",
        ),
        ("9, 27, 81, 246, 729, 2187 — ഒറ്റയാൻ?", ["9", "81", "246", "729"], "246", "easy"),
        ("2026-ലെ കലണ്ടർ ഏത് വർഷം വരെ ഉപയോഗിക്കാം?", ["2037", "2031", "2052", "2036"], "2037"),
        ("61 × 14 × 127^38-ന്റെ യൂണിറ്റ് അക്കം?", ["4", "8", "2", "6"], "6", "hard"),
        (
            "അരുൺ 25 km 50 m ബസ്സിൽ, 7 km 265 m കാറിൽ, 1 km 30 m നടന്നു. ആകെ ദൂരം (കി.മീ.)?",
            ["33.345", "34.065", "34.345", "33.065"],
            "33.065",
        ),
        (
            "40% mark pass. 320 mark കിട്ടി; 80 mark കൊണ്ട് fail. maximum marks?",
            ["800", "1000", "1500", "1280"],
            "1000",
        ),
        (
            "10% profit-ൽ vend. ₹250 കൂടി കിട്ടിയിരുന്നാൽ profit 20%. cost price?",
            ["2,500", "2,000", "1,350", "1,500"],
            "2,500",
        ),
        ("6 men + 7 women → 12 days; 2 men + 5 women → 20 days. 10 men എത്ര days?", ["20", "22", "24", "26"], "20", "hard"),
        (
            "1 km track-ൽ 5, 4, 7, 11 km/hr speeds. ആരംഭ ബിന്ദുവിൽ വീണ്ടും കൂടാൻ?",
            ["3 മണി", "2 മണി", "1 മണി", "4 മണി"],
            "1 മണി",
        ),
        ("RIDE = 36, DESK = 39 → RISK = ?", ["60", "57", "58", "56"], "57"),
        ("2025 കലണ്ടർ = ഏത് വർഷം?", ["2031", "2030", "2036", "2033"], "2036"),
        (
            "72 ? 4 ? 10 ? 4 ? 2 = 72. ശരിയായ ചിഹ്നങ്ങൾ?",
            ["=, +, ×, ÷", "=, ×, +, ÷", "×, +, =, ÷", "+, =, ×, ÷"],
            "=, +, ×, ÷",
            "hard",
        ),
    ]
    for q, opts, ans, *rest in mat:
        add("mathematics.json", "mat_", q, opts, ans, rest[0] if rest else "medium")

    # --- Kerala PSC 071/2024 GK (Malayalam) ---
    add(
        "indian_history.json",
        "ih_",
        "പോർച്ചുഗീസുകാരെക്കുറിച്ച്:\n"
        "(i) 1510-ൽ Albuquerque Goa പിടിച്ചു\n"
        "(ii) Vasco da Gama King Emmanuel-ന്റെ inspiration-ൽ India route കണ്ടെത്തി\n"
        "(iii) Cochin Portuguese-കാലത്ത് Malabar-il രണ്ടാമത്തെ വലിയ നഗരം",
        ["I, II, III", "I, II മാത്രം", "II, III മാത്രം", "I, III മാത്രം"],
        "I, II, III",
    )
    add(
        "history_of_kerala.json",
        "hok_",
        "മാർത്താണ്ഡവർമ്മ:\n"
        "(i) 1741 കോളച്ചൽ യുദ്ധത്തിൽ Dutch-ine തോൽപ്പിച്ചു\n"
        "(ii) 1757 മാവേലിക്കര treaty-il Travancore-Cochin friendship\n"
        "(iii) Mandapathu Vattukal Army HQ-ക്ക് title",
        ["I, II മാത്രം", "I, II, III", "I, III മാത്രം", "II, III മാത്രം"],
        "I, II, III",
    )
    add(
        "kerala_renaissance.json",
        "kr_",
        "വൈക്കം സത്യാഗ്രഹം:\n"
        "(i) E.V. Ramaswami Naicker arrest\n"
        "(ii) 1924 flood-സമയം തുടർന്നു\n"
        "(iii) 1925 Feb 7-ന് legislature 22 support, 21 reject",
        ["I, III മാത്രം", "I, II മാത്രം", "II, III മാത്രം", "I, II, III"],
        "I, III മാത്രം",
    )
    add(
        "modern_india.json",
        "mi_",
        "സിവിൽ disobedience:\n"
        "(i) Gandhi Purna Swaraj non-violent struggle\n"
        "(ii) Dandi march Sabarmati to sea\n"
        "(iii) Nehru 1931-ൽ Gandhi-യോട് salt strategy praise",
        ["I, III മാത്രം", "II, III മാത്രം", "I, II മാത്രം", "I, II, III"],
        "I, II, III",
    )
    add(
        "world_history.json",
        "wh_",
        "UNO:\n"
        "(i) League of Nations resemble; 50 members San Francisco\n"
        "(ii) Charter: peace, security, cooperation; no internal intervention\n"
        "(iii) Teheran 1943: democratic nations family",
        ["I, II മാത്രം", "II, III മാത്രം", "I, III മാത്രം", "I, II, III"],
        "I, II, III",
    )
    add(
        "geography.json",
        "geo_",
        "National Waterway 3 (NW3) India-യിൽ?",
        ["Sadiya–Dhubri", "Kakinada–Puducherry", "Kottapuram–Kollam", "Allahabad–Haldia"],
        "Kottapuram–Kollam",
    )
    add(
        "geography.json",
        "geo_",
        "Silent Valley — lion-tailed macaque-ന്റെ largest population?",
        ["Anamudi Shola", "Mathikettan Shola", "Silent Valley", "Eravikulam"],
        "Silent Valley",
    )
    add(
        "economics.json",
        "eco_",
        "India-യുടെ 12th Five Year Plan (2012–17) theme?",
        [
            "Garibi Hatao",
            "Faster, Inclusive and Sustainable Growth",
            "Growth with Social Justice",
            "Poverty Alleviation and Industrial Development",
        ],
        "Faster, Inclusive and Sustainable Growth",
    )
    add(
        "economics.json",
        "eco_",
        "RBI:\n(i) IMF member\n(ii) Established 1 April 1935\n(iii) Usha Thorat first woman Governor",
        ["i, ii മാത്രം", "ii, iii മാത്രം", "i, iii മാത്രം", "i, ii, iii"],
        "i, ii മാത്രം",
    )
    add(
        "economics.json",
        "eco_",
        "GST-ൽ imports-ന് levy?",
        ["CGST മാത്രം", "IGST", "SGST മാത്രം", "മുകളിലുള്ള എല്ലാം"],
        "IGST",
    )
    add(
        "constitution_of_india.json",
        "coi_",
        "106th Amendment — SEBC recognition authority?",
        ["106", "101", "105", "100"],
        "106",
        "hard",
    )
    add(
        "constitution_of_india.json",
        "coi_",
        "Indian Constitution-ന്റെ official calligrapher?",
        ["Prem Behari Narain Raizada", "Ram Parshad", "N.V. Gadgil", "Nand Lal Bose"],
        "Prem Behari Narain Raizada",
    )
    add(
        "constitution_of_india.json",
        "coi_",
        "Article 248 — Union-ന്റെ residuary legislative power?",
        [
            "Executive power scope",
            "Concurrent/state list law",
            "PMO special powers",
            "Unenumerated matters-ൽ law making",
        ],
        "Unenumerated matters-ൽ law making",
    )
    add(
        "constitution_of_india.json",
        "coi_",
        "Local bodies-il 50% women reservation ആദ്യം?",
        ["Bihar", "Kerala", "Karnataka", "Himachal Pradesh"],
        "Bihar",
    )
    add(
        "constitution_of_india.json",
        "coi_",
        "S.R. Bommai v. Union of India — Article?",
        ["356", "360", "362", "352"],
        "356",
    )
    add(
        "arts.json",
        "art_",
        "Koodiyattam-നെ scientifically describe ചെയ്ത പുസ്തകം?",
        ["Hasta Lakshana Deepika", "Natyasastra", "Natyakalpa Drumam", "Thapathi Samvaranam"],
        "Natyakalpa Drumam",
    )
    add(
        "arts.json",
        "art_",
        "UNESCO heritage-il Kerala visual arts (2)?",
        ["Kathakali, Ottamthullal", "Theyyam, Koodiyattam", "Koodiyattam, Padayani", "Koodiyattam, Mudiyettu"],
        "Koodiyattam, Mudiyettu",
    )
    add(
        "sports.json",
        "sca_",
        "Olympics opening ceremony-il first march — country?",
        ["Greece", "France", "Switzerland", "Host country"],
        "Greece",
    )
    add(
        "sports.json",
        "sca_",
        "Davis Cup — sport?",
        ["Cricket", "Tennis", "Badminton", "Basketball"],
        "Tennis",
    )
    add(
        "malayalam.json",
        "mal_",
        "'Nandanar' — pen name?",
        ["P.C. Kuttikrishnan", "C. Govinda Pisharody", "P.C. Gopalan", "R. Ramachandran Nair"],
        "P.C. Kuttikrishnan",
    )
    add(
        "cinema.json",
        "cin_",
        "Malayalam-il first colour movie?",
        ["Chemmeen", "Kandam Becha Coat", "Balan", "Neelakuyil"],
        "Balan",
    )
    add(
        "literature.json",
        "lit_",
        "Sangam period — Onam reference?",
        ["Akananooru", "Chilappatikaram", "Madurai Kanchi", "Periyapuranam"],
        "Akananooru",
    )
    add(
        "kerala_renaissance.json",
        "kr_",
        "Malayali Memorial writer?",
        ["E.V. Krishna Pillai", "Kumaranasan", "Bodeswaran", "C.V. Raman Pillai"],
        "C.V. Raman Pillai",
    )
    add(
        "current_affairs_2026_06.json",
        "ca_2026_06_",
        "Israel-Hamas conflict-il Indians-നെ Operation Ajay?",
        ["Operation Ajay", "Operation Vijay", "Operation Bluestar", "Operation Hamas"],
        "Operation Ajay",
    )
    add(
        "arts.json",
        "art_",
        "Kerala Kalamandalam Vice Chancellor (recent)?",
        ["Mrinalini Sarabhai", "Dr. Mohan Kunnummel", "Dr. B. Anantha Krishnan", "Dr. S. Bijoy Nandan"],
        "Dr. Mohan Kunnummel",
    )
    add(
        "information_technology.json",
        "it_",
        "Boot program hold ചെയ്യുന്ന memory?",
        ["ROM", "RAM", "Cache", "Secondary memory"],
        "ROM",
    )
    add(
        "information_technology.json",
        "it_",
        "Line-by-line HLL → machine code?",
        ["Assembler", "Compiler", "Interpreter", "Operating system"],
        "Interpreter",
    )
    add(
        "information_technology.json",
        "it_",
        "Cyber crime helpline (National portal)?",
        ["1940", "1930", "1098", "1947"],
        "1930",
    )
    add(
        "information_technology.json",
        "it_",
        "ICANN full form?",
        [
            "Internet Corporation for Assigned Names and Numbers",
            "International Computer Association",
            "Indian Network Centre",
            "Integrated Circuit Analysis Network",
        ],
        "Internet Corporation for Assigned Names and Numbers",
    )
    add(
        "information_technology.json",
        "it_",
        "Omegle founder?",
        ["Sam Altman", "David R. Woolley", "Doug Brown", "Leif K. Brooks"],
        "Leif K. Brooks",
    )
    add(
        "awards.json",
        "aca_",
        "Bharat Ratna — scientists?\n(i) Vikram Sarabhai (ii) A.P.J. Abdul Kalam (iii) Homi Bhabha",
        ["i മാത്രം", "i, iii മാത്രം", "i, ii, iii", "ii മാത്രം"],
        "ii മാത്രം",
    )
    add(
        "natural_science.json",
        "nsc_",
        "Aditya-L1 science objectives?",
        [
            "iii മാത്രം",
            "i, iii മാത്രം",
            "i മാത്രം",
            "i, ii, iii",
        ],
        "i മാത്രം",
    )
    add(
        "natural_science.json",
        "nsc_",
        "National Green Hydrogen Mission?",
        ["ii മാത്രം", "i, iii മാത്രം", "ii, iii മാത്രം", "i, ii, iii"],
        "i, iii മാത്രം",
    )
    add(
        "natural_science.json",
        "nsc_",
        "Environment Protection Act enacted?",
        ["1986", "1980", "2020", "1972"],
        "1986",
        "easy",
    )

    # English section (071/2024 + Thozhilvartha images)
    eng = [
        ("Let us reconsider the proposal, ______?", ["will you", "shall we", "do we", "don't we"], "shall we"),
        (
            "Identify the correct sentence.",
            [
                "The director had the assistant prepare the summary.",
                "The director had the assistant prepared the summary.",
                "The director had the assistant preparing the summary.",
                "The director had the assistant to prepare the summary.",
            ],
            "The director had the assistant prepare the summary.",
        ),
        ("Ravi ______ tea every morning.", ["is drinking", "drinks", "drink", "has drank"], "drinks", "easy"),
        ("The plant shed its leaves. Possessive pronoun?", ["plant", "shed", "its", "leaves"], "its", "easy"),
        ("Keerthana won't be late, ______?", ["will she", "won't she", "would she", "wouldn't she"], "will she"),
        (
            "Now we shall discuss ______ our future prospects.",
            ["about", "of", "for", "no preposition"],
            "no preposition",
        ),
        (
            "We are going to bake the bread. (Passive)",
            [
                "The bread is going to be baked.",
                "The bread was going to be baked.",
                "The bread has been baked.",
                "The bread will be baked.",
            ],
            "The bread is going to be baked.",
        ),
        (
            "Antonym of 'strictly' (rules were strictly enforced).",
            ["leniently", "firmly", "rigidly", "severely"],
            "leniently",
        ),
        ("Something happened at the college, ______?", ["don't it", "hadn't it", "didn't it", "isn't it"], "didn't it"),
        ("The programme starts ______ 8:15 am.", ["at", "in", "on", "over"], "at", "easy"),
        ("The Principal ______ to speak to you.", ["wants", "wanting", "is wanting", "was wanting"], "wants"),
        (
            "Mary opened the door. (Passive)",
            [
                "Mary was opened the door.",
                "The door was opened by Mary.",
                "Opened the door by Mary.",
                "Mary has opened the door.",
            ],
            "The door was opened by Mary.",
        ),
        ("What a super show!", ["Declarative", "Interrogative", "Imperative", "Exclamatory"], "Exclamatory", "easy"),
        ("He didn't get ______ job he applied for.", ["an", "a", "the", "none of the above"], "the"),
        ("Michelle is ______ than Natasha.", ["old", "more old", "elder", "older"], "older"),
        ("I look forward ______ from you.", ["for hearing", "for hear", "to hearing", "by hearing"], "to hearing"),
        (
            "Joshua said to mom, \"I have been here\".",
            [
                "Joshua told mom that I had been there.",
                "Joshua told mom that he has been there.",
                "Joshua told mom that he had been here.",
                "Joshua told mom that he had been there.",
            ],
            "Joshua told mom that he had been there.",
        ),
        ("Phrasal verb: didn't ______ (meet as arranged).", ["fall off", "turn up", "move in", "clear up"], "turn up"),
        ("Synonym of 'amicable'.", ["cruel", "large", "friendly", "simple"], "friendly", "easy"),
        ("Opposite of 'cautious'.", ["reckless", "careful", "slim", "beautiful"], "reckless", "easy"),
        ("Correctly spelt?", ["catastrophy", "catastrophi", "catastrophe", "catestrophy"], "catastrophe", "easy"),
        ("One word: person with no money.", ["stale", "agile", "passerby", "pauper"], "pauper"),
        ("Idiom 'round the corner' means?", ["very near", "difficult", "spontaneous", "clear"], "very near"),
        ("Compound word?", ["table", "hallway", "ceiling", "computer"], "hallway", "easy"),
        ("Female tiger?", ["tigress", "ewe", "calf", "tiger cub"], "tigress", "easy"),
        ("Prefix comes at ______ of a word.", ["ending", "middle", "beginning", "top"], "beginning", "easy"),
        (
            "LASER stands for?",
            [
                "Light Amplification by Stimulated Emission of Radiation",
                "Light Applied System Energy Resource",
                "Linear Amplified Signal Energy Ray",
                "Low Amplitude Stimulated Energy Ray",
            ],
            "Light Amplification by Stimulated Emission of Radiation",
        ),
        ("One word: pleasure as chief good.", ["Stoic", "Hedonist", "Ascetic", "Cynic"], "Hedonist"),
        ("Collective noun: herd of ______.", ["cattle", "sheep", "fish", "birds"], "cattle", "easy"),
    ]
    for item in eng:
        q, opts, ans, *rest = item
        add("english_language.json", "eng_", q, opts, ans, rest[0] if rest else "medium")

    return out


def max_id_num(questions: list[dict], prefix: str) -> int:
    best = 0
    for q in questions:
        qid = q.get("id", "")
        if qid.startswith(prefix):
            m = re.search(r"\d+", qid[len(prefix) :])
            if m:
                best = max(best, int(m.group()))
    return best


def load_global_stems(exclude: Path) -> set[str]:
    stems: set[str] = set()
    for path in BASE.glob("*.json"):
        if path.name == "current_affairs_manifest.json" or path == exclude:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for q in data.get("questions", []):
            s = q.get("question", "").strip()
            if s:
                stems.add(s)
    return stems


def main() -> None:
    by_file: dict[str, list[tuple]] = {}
    prefixes: dict[str, str] = {}
    for file, prefix, q, opts, ans, diff in rows():
        by_file.setdefault(file, []).append((q, opts, ans, diff))
        prefixes[file] = prefix

    total = 0
    for file, batch in by_file.items():
        path = BASE / file
        data = json.loads(path.read_text(encoding="utf-8"))
        questions = data.setdefault("questions", [])
        prefix = prefixes[file]
        global_stems = load_global_stems(path)
        existing = {q["question"].strip() for q in questions}
        n = max_id_num(questions, prefix)
        added = 0
        is_eng = file == "english_language.json"
        for q, opts, ans, diff in batch:
            if q in existing or q in global_stems:
                continue
            if len(set(opts)) != 4 or ans not in opts:
                print(f"SKIP invalid [{file}]: {q[:50]}", file=sys.stderr)
                continue
            if not is_eng and MIXED.search(q + "".join(opts) + ans):
                print(f"SKIP mixed [{file}]: {q[:50]}", file=sys.stderr)
                continue
            n += 1
            questions.append({"id": f"{prefix}{n:03d}", "question": q, "options": opts, "answer": ans, "difficulty": diff})
            existing.add(q)
            global_stems.add(q)
            added += 1
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{file}: +{added}")
        total += added
    print(f"Total: +{total}")
    subprocess.run([sys.executable, "validate_questions.py"], cwd=BASE, check=False)


if __name__ == "__main__":
    main()
