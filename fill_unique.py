#!/usr/bin/env python3
"""Add unique Kerala PSC-style Malayalam quiz questions to underfilled JSON files."""

import json
import random
import re
from pathlib import Path

from malayalamize_questions import malayalamize_text

BASE = Path(__file__).parent
Question = tuple[str, list[str], str, str]


def load_all_existing() -> set[str]:
    existing: set[str] = set()
    for path in BASE.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for q in data.get("questions", []):
            text = q.get("question", "").strip()
            if text:
                existing.add(text)
    return existing


def max_id_num(questions: list[dict], prefix: str) -> int:
    pat = re.compile(rf"^{re.escape(prefix)}(\d+)$")
    mx = 0
    for q in questions:
        m = pat.match(q.get("id", ""))
        if m:
            mx = max(mx, int(m.group(1)))
    return mx


def make_entry(prefix: str, num: int, q: str, opts: list[str], ans: str, diff: str) -> dict:
    shuffled = list(opts)
    random.shuffle(shuffled)
    return {
        "id": f"{prefix}{num:03d}",
        "question": q,
        "options": shuffled,
        "answer": ans,
        "difficulty": diff,
    }


def fill_file(
    filename: str,
    prefix: str,
    candidates: list[Question],
    target_total: int,
    existing: set[str],
) -> int:
    path = BASE / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.get("questions", [])
    start = max_id_num(questions, prefix) + 1
    needed = max(0, target_total - len(questions))
    added = 0

    for q_text, opts, ans, diff in candidates:
        if added >= needed:
            break
        q_text = q_text.strip()
        if q_text in existing:
            continue
        if ans not in opts:
            raise ValueError(f"Answer not in options: {q_text!r}")
        entry = make_entry(prefix, start + added, q_text, opts, ans, diff)
        questions.append(entry)
        existing.add(q_text)
        added += 1

    data["questions"] = questions
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return added


def qb(q: str, o: list[str], a: str, d: str) -> Question:
    q = malayalamize_text(q)
    o = [malayalamize_text(x) for x in o]
    a = malayalamize_text(a)
    if a not in o or len(o) != 4:
        raise ValueError((q, o, a))
    return (q, o, a, d)


def build_indian_history() -> list[Question]:
    return [
        qb("പിറ്റിന്റെ ഇന്ത്യാ നിയമം പ്രാബല്യത്തിൽ വന്ന വർഷം ഏത്?", ["1784", "1773", "1793", "1813"], "1784", "medium"),
        qb("1773-ലെ റെഗുലേറ്റിംഗ് ആക്ട് പ്രകാരം ആദ്യ ഗവർണർ ജനറൽ ആരായിരുന്നു?", ["വാറൻ ഹേസ്റ്റിംഗ്സ്", "ലോർഡ് കോർൺവാലിസ്", "ലോർഡ് വെൽസלי", "ലോർഡ് ഡാല്ഹൗസി"], "വാറൻ ഹേസ്റ്റിംഗ്സ്", "medium"),
        qb("1793-ലെ പെർമനന്റ് സെറ്റിൽമെന്റ് ആക്ട് ആദ്യം പ്രയോഗിച്ച പ്രവിശ്യ ഏത്?", ["ബംഗാൾ", "മദ്രാസ്", "ബോംബെ", "പഞ്ചാബ്"], "ബംഗാൾ", "medium"),
        qb("പെർമനന്റ് സെറ്റിൽമെന്റ് ആക്ട് നടപ്പാക്കിയ വൈസ്രോയി ആര്?", ["ലോർഡ് കോർൺവാലിസ്", "വാറൻ ഹേസ്റ്റിംഗ്സ്", "ലോർഡ് ഡാല്ഹൗസി", "ലോർഡ് റിപ്പൺ"], "ലോർഡ് കോർൺവാലിസ്", "medium"),
        qb("റയത്ത്വാരി ഭൂമി-നികുതി സംവിധാനം ആദ്യം പ്രയോഗിച്ച ഉദ്യോഗസ്ഥൻ ആര്?", ["തോമസ് മൺറോ", "ലോർഡ് കോർൺവാലിസ്", "വാറൻ ഹേസ്റ്റിംഗ്സ്", "ലോർഡ് ഡാല്ഹൗസി"], "തോമസ് മൺറോ", "medium"),
        qb("മഹല്വാരി ഭൂമി-നികുതി സംവിധാനം ആദ്യം പ്രയോഗിച്ച പ്രദേശം ഏത്?", ["വടക്കൻ-പശ്ചിമ പ്രവിശ്യകൾ", "മദ്രാസ്", "ബംഗാൾ", "ബോംബെ"], "വടക്കൻ-പശ്ചിമ പ്രവിശ്യകൾ", "hard"),
        qb("ആദ്യ കർണാടക യുദ്ധം നടന്ന വർഷം ഏത്?", ["1746", "1767", "1780", "1799"], "1746", "hard"),
        qb("നാലാമത് കർണാടക യുദ്ധത്തിൽ ടിപ്പു സുൽത്താൻ വീഴ്ച സംഭവിച്ച വർഷം?", ["1799", "1784", "1767", "1746"], "1799", "medium"),
        qb("ബഹ്മനി സുൽത്താനത്തിന്റെ സ്ഥാപകൻ ആര്?", ["അലാവുദ്ദിൻ ബഹ്മനി ഷാ", "കൃഷ്ണദേവരായർ", "ഇബ്രാഹിം ആദിൽ ഷാ", "ഖുലി ഖുത്ബ് ഷാ"], "അലാവുദ്ദിൻ ബഹ്മനി ഷാ", "medium"),
        qb("ഗോൾക്കൊണ്ട സുൽത്താനത്തിന്റെ പ്രധാന കോട്ട നഗരം ഏത്?", ["ഗോൾക്കൊണ്ട", "ഹൈദരാബാദ്", "ബീദർ", "Bijapur"], "ഗോൾക്കൊണ്ട", "medium"),
        qb("ലോദി രാജവംശത്തിന്റെ അവസാന രാജാവ് ആര്?", ["ഇബ്രാഹിം ലോദി", "ബഹ്‌ലുൽ ലോദി", "സികന്ദർ ലോദി", "ദാബുൾ ഖാൻ"], "ഇബ്രാഹിം ലോദി", "medium"),
        qb("സൂർ സാമ്രാജ്യത്തിന്റെ സ്ഥാപകൻ ആര്?", ["ഷെർ ഷാ സൂരി", "ഹുമയൂൻ", "ബാബർ", "അക്ബർ"], "ഷെർ ഷാ സൂരി", "easy"),
        qb("ഗ്രാൻഡ് ട്രങ്ക് റോഡ് പുനർനിർമ്മിച്ചത് ആര്?", ["ഷെർ ഷാ സൂരി", "അക്ബർ", "ഷാ ജഹാൻ", "ഔറംഗസേബ്"], "ഷെർ ഷാ സൂരി", "medium"),
        qb("ബാദാമി ചാലുക്ക്യരുടെ തലസ്ഥാനം ഏത്?", ["ബാദാമി", "മാണ്യകേട", "Kalyani", "വാതാപി"], "ബാദാമി", "medium"),
        qb("രാഷ്ട്രകൂടരുടെ പ്രശസ്ത ചക്രവർത്തി ആര്?", ["അമോഘവർഷ", "പുലകേശിൻ II", "ഗോവിന്ദ III", "കൃഷ്ണ I"], "അമോഘവർഷ", "medium"),
        qb("രാഷ്ട്രകൂടരുടെ തലസ്ഥാനമായ മാണ്യകേട ഏത് സംസ്ഥാനത്താണ്?", ["കർണാടക", "മഹാരാഷ്ട്ര", "തെലുങ്കാനം", "ഗുജറാത്ത്"], "കർണാടക", "medium"),
        qb("ബംഗാളിലെ സേന രാജവംശത്തിന്റെ പ്രശസ്ത രാജാവ് ആര്?", ["വിജയ സേൻ", "സാമന്ത സേൻ", "ബല്ലാൽ സേൻ", "ലക്ഷ്മൺ സേൻ"], "വിജയ സേൻ", "hard"),
        qb("1907-ലെ സൂറത്ത് സമ്മേളനത്തിൽ മിതവാദികളുടെ നേതാവ് ആര്?", ["ഗോപാൽകൃഷ്ണ ഗോഖലെ", "Bal Gangadhar Tilak", "ലാലാ ലജപത് റായ്", "ബിപിൻ ചന്ദ്ര പാൽ"], "ഗോപാൽകൃഷ്ണ ഗോഖലെ", "medium"),
        qb("1907-ലെ സൂറത്ത് സമ്മേളനത്തിൽ കടുപ്പക്കാർക്ക് (extremists) നേതൃത്വം നൽകിയത് ആര്?", ["Bal Gangadhar Tilak", "ദാദാഭായി നൗറോജി", "ഫിറോസ്ഷാ മേത്ത", "സുരേന്ദ്രനാഥ ബാനർജി"], "Bal Gangadhar Tilak", "medium"),
        qb("ഖിലാഫത്ത് പ്രസ്ഥാനം ആരംഭിച്ച വർഷം ഏത്?", ["1919", "1920", "1915", "1922"], "1919", "easy"),
        qb("ഖിലാഫത്ത് പ്രസ്ഥാനത്തിൽ മഹാത്മാ ഗാന്ധിയോടൊപ്പം allied ആയ നേതാക്കൾ?", ["അലി സഹോദരanmar", "മുഹമ്മദ് അലി ജിന്ന", "മൗലാനാ ആസാദ്", "അബുൽ കലാം ആസാദ്"], "അലി സഹോദരanmar", "medium"),
        qb("1928-ലെ ബർദോലി സത്യാഗ്രഹത്തിന്റെ നേതൃത്വം?", ["സർദാർ വല്ലഭhai പatel", "ജawaharlal നehru", "Rajendra പ്രasad", "C. Rajagopalachari"], "സർദാർ വല്ലഭhai പatel", "medium"),
        qb("1925-ലെ കാക്കോരി train robbery-യുമായി ബന്ധപ്പെട്ട revolutionary?", ["Ram പ്രasad ബismil", "Bhagat സingh", "Chandra Shekhar അzad", "Sukhdev"], "Ram പ്രasad ബismil", "medium"),
        qb("INA (ഇന്ത്യൻ നാഷണൽ ആർമി) reorganize ചെയ്ത നേതാവ്?", ["Subhas ചandra ബose", "Rash Behari ബose", "Mohan സingh", "Lakshmi സahgal"], "Subhas ചandra ബose", "easy"),
        qb("INA-യുടെ 'Delhi Chalo' മുദ്രാവാക്യം പ്രഖ്യാപിച്ചത്?", ["Subhas ചandra ബose", "Jawaharlal നehru", "Mahatma ഗandhi", "Bhagat സingh"], "Subhas ചandra ബose", "easy"),
        qb("1946-ലെ Royal Indian Navy mutiny ആരംഭിച്ച നഗരം?", ["Mumbai", "Kolkata", "Chennai", "Karachi"], "Mumbai", "medium"),
        qb("Round Table Conferences-ൽ Indian National Congress പങ്കെടുത്തത്?", ["രണ്ടാം മാത്രം", "ഒന്നാം മാത്രം", "മൂന്നാം മാത്രം", "ഒന്നും പങ്കെടുത്തില്ല"], "രണ്ടാം മാത്രം", "hard"),
        qb("1932-ലെ Poona Pact-ൽ agreement ഉണ്ടായത് ആരുമായി?", ["B.R. Ambedkar", "Muhammad Ali ജinnah", "Lord Irwin", "Subhas ചandra ബose"], "B.R. Ambedkar", "medium"),
        qb("Poona Pact-ൽ depressed classes-ന് reserved seats എത്ര?", ["148", "121", "193", "75"], "148", "hard"),
        qb("1935-ലെ Government of India Act-ന് basis ആയത്?", ["Simon Commission Report", "Cripps Mission", "Cabinet Mission", "Wavell Plan"], "Simon Commission Report", "medium"),
        qb("1942-ലെ Cripps Mission-ന്റെ chairman?", ["Sir Stafford Cripps", "Lord Wavell", "Clement Attlee", "Lord Mountbatten"], "Sir Stafford Cripps", "medium"),
        qb("1946-ലെ Cabinet Mission-ൽ British delegation-ന്റെ leader?", ["Pethick-Lawrence", "Stafford Cripps", "A.V. Alexander", "Mountbatten"], "Pethick-Lawrence", "hard"),
        qb("Mountbatten Plan പ്രകാരം partition date?", ["1947 August 15", "1947 June 3", "1947 July 18", "1948 January 26"], "1947 August 15", "medium"),
        qb("Indian Independence Act passed in British Parliament?", ["1947 July", "1947 August", "1946 December", "1948 January"], "1947 July", "medium"),
        qb("Kalyani ചാലുക്ക്യരുടെ പ്രശസ്ത ruler?", ["Vikramaditya VI", "Pulakeshin II", "Krishna III", "Someshvara I"], "Vikramaditya VI", "hard"),
        qb("Hoysala architecture-ന്റെ star-shaped temples?", ["Belur and Halebidu", "Khajuraho", "Konark", "Modhera"], "Belur and Halebidu", "medium"),
        qb("Vijayanagara Empire-യുടെ സ്ഥാപകർ?", ["Harihara and Bukka", "Krishna Deva Raya", "Deva Raya II", "Rama Raya"], "Harihara and Bukka", "medium"),
        qb("Krishna Deva Raya-യുടെ court poet?", ["Allasani Peddana", "Tenali Ramakrishna", "Kalidasa", "Bana"], "Allasani Peddana", "medium"),
        qb("First Anglo-Mysore War ended with which treaty?", ["Treaty of Madras", "Treaty of Mangalore", "Treaty of Seringapatam", "Treaty of Purandar"], "Treaty of Madras", "hard"),
        qb("Doctrine of Lapse introduced by?", ["Lord Dalhousie", "Lord Wellesley", "Lord Hastings", "Lord Curzon"], "Lord Dalhousie", "easy"),
        qb("1857-ലെ സ്വാതന്ത്ര്യ സമരത്തിൽ ജansi-യിലെ രാജ്ഞി ആരായിരുന്നു?", ["Rani Lakshmibai", "Begum Hazrat Mahal", "Rani Chennamma", "Kittur Chennamma"], "Rani Lakshmibai", "easy"),
        qb("1857-ലെ സ്വാതന്ത്ര്യ സമരത്തിൽ ലucknow-ൽ നേതൃത്വം നൽകിയത് ആര്?", ["Begum Hazrat Mahal", "Rani Lakshmibai", "Nana Saheb", "Tantia Tope"], "Begum Hazrat Mahal", "medium"),
        qb("1857-ലെ സ്വാതന്ത്ര്യ സമരത്തിൽ കanpur-ൽ നേതൃത്വം നൽകിയത് ആര്?", ["Nana Saheb", "Bahadur Shah II", "Mangal Pandey", "Kunwar Singh"], "Nana Saheb", "medium"),
        qb("1857-ലെ സ്വാതന്ത്ര്യ സമരത്തിൽ ബihar-ൽ നേതൃത്വം നൽകിയത് ആര്?", ["Kunwar Singh", "Tantia Tope", "Mangal Pandey", "Rani Lakshmibai"], "Kunwar Singh", "medium"),
        qb("1909-ലെ ഇന്ത്യൻ കൗൺസിൽസ് ആക്ട് ഏത് reforms-ന്റെ പേരിലാണ് അറിയപ്പെടുന്നത്?", ["Morley-Minto Reforms", "Montagu-Chelmsford Reforms", "Government of India Act 1935", "Regulating Act"], "Morley-Minto Reforms", "medium"),
        qb("Montagu-Chelmsford Reforms enacted in?", ["1919", "1909", "1935", "1947"], "1919", "medium"),
        qb("Rowlatt Act passed in?", ["1919", "1920", "1915", "1930"], "1919", "easy"),
        qb("Chauri Chaura incident-ൽ police killed in?", ["1922", "1920", "1930", "1942"], "1922", "medium"),
        qb("Simon Commission arrived in India in?", ["1928", "1930", "1925", "1932"], "1928", "easy"),
        qb("Quit India Resolution passed in?", ["1942", "1940", "1945", "1930"], "1942", "easy"),
        qb("Indian National Army trial (Red Fort trials) in?", ["1945", "1946", "1942", "1947"], "1945", "medium"),
    ]


def build_modern_india() -> list[Question]:
    schemes = [
        ("NITI Aayog", "2015", ["2014", "2016", "2018"], "easy"),
        ("GST", "2017 ജൂലൈ 1", ["2016 ജൂലൈ 1", "2018 ജൂലൈ 1", "2017 ജനുവരി 1"], "easy"),
        ("Make in India", "2014", ["2015", "2016", "2013"], "easy"),
        ("Digital India", "2015", ["2014", "2016", "2017"], "easy"),
        ("Swachh Bharat Mission", "2014 ഓക്ടോബർ 2", ["2015 ജൂൺ 5", "2014 ജൂൺ 5", "2016 ഓക്ടോബർ 2"], "easy"),
        ("Ayushman Bharat PM-JAY", "2018", ["2017", "2019", "2016"], "medium"),
        ("PM-KISAN", "2019", ["2018", "2020", "2017"], "medium"),
        ("Startup India", "2016", ["2015", "2017", "2014"], "medium"),
        ("Smart Cities Mission", "2015", ["2014", "2016", "2017"], "medium"),
        ("Jan Dhan Yojana", "2014", ["2015", "2016", "2013"], "easy"),
        ("MUDRA Yojana", "2015", ["2014", "2016", "2017"], "medium"),
    ]
    qs: list[Question] = []
    for name, ans, wrong, diff in schemes:
        qs.append(qb(f"{name} പദ്ധതി/സംവിധാനം ആരംഭിച്ച വർഷം/തീയതി ഏത്?", wrong + [ans], ans, diff))
    qs.extend([
        qb("2016 നവംബർ 8-ന് പ്രഖ്യാപിച്ച നോട്ട് അസാധുവാക്കൽ ഏത് നോട്ടുകളായിരുന്നു?", ["₹500, ₹1000", "₹200, ₹500", "₹1000, ₹2000", "₹100, ₹500"], "₹500, ₹1000", "easy"),
        qb("Chandrayaan-3 ചന്ദ്രനിൽ soft landing നടത്തിയ വർഷം?", ["2023", "2019", "2024", "2022"], "2023", "easy"),
        qb("Mangalyaan (Mars Orbiter Mission) launch year?", ["2013", "2014", "2012", "2015"], "2013", "medium"),
        qb("Aditya-L1 സൗര്യ ദൗത്യം launch year?", ["2023", "2022", "2024", "2021"], "2023", "medium"),
        qb("ഇന്ത്യയുടെ ആദ്യ വനITa President?", ["Pratibha Patil", "Draupadi Murmu", "Indira Gandhi", "Meira Kumar"], "Pratibha Patil", "easy"),
        qb("ഇന്ത്യയുടെ ആദ്യ tribal woman President?", ["Draupadi Murmu", "Pratibha Patil", "Meira Kumar", "Sarojini Naidu"], "Draupadi Murmu", "easy"),
        qb("ഇന്ത്യയുടെ ആദ്യ Sikh Prime Minister?", ["Manmohan Singh", "Charan Singh", "I.K. Gujral", "Morarji Desai"], "Manmohan Singh", "easy"),
        qb("1991 സാമ്പത്തിക reforms Finance Minister?", ["Manmohan Singh", "P. Chidambaram", "Yashwant Sinha", "Pranab Mukherjee"], "Manmohan Singh", "medium"),
        qb("1991 reforms-ന്റെ Prime Minister?", ["P.V. Narasimha Rao", "Rajiv Gandhi", "V.P. Singh", "Atal Bihari Vajpayee"], "P.V. Narasimha Rao", "medium"),
        qb("Kargil War year?", ["1999", "1971", "1965", "2001"], "1999", "easy"),
        qb("India-China war year?", ["1962", "1965", "1971", "1984"], "1962", "easy"),
        qb("Emergency declared by Indira Gandhi in?", ["1975", "1977", "1974", "1976"], "1975", "easy"),
        qb("Operation Blue Star year?", ["1984", "1985", "1983", "1975"], "1984", "medium"),
        qb("Pokhran-II nuclear tests year?", ["1998", "1974", "2000", "1996"], "1998", "medium"),
        qb("Right to Information Act enacted in?", ["2005", "2002", "2008", "2010"], "2005", "medium"),
        qb("Right to Education Act enacted in?", ["2009", "2005", "2010", "2012"], "2009", "medium"),
        qb("India G20 presidency year?", ["2023", "2022", "2024", "2021"], "2023", "easy"),
        qb("G20 Summit 2023 venue?", ["New Delhi", "Mumbai", "Bengaluru", "Jaipur"], "New Delhi", "easy"),
        qb("Article 370 abrogation date?", ["2019 August 5", "2019 October 31", "2020 January 1", "2018 August 5"], "2019 August 5", "medium"),
        qb("ISRO founded in?", ["1969", "1972", "1962", "1980"], "1969", "medium"),
        qb("India's first satellite Aryabhata launched in?", ["1975", "1980", "1973", "1978"], "1975", "medium"),
        qb("Chandrayaan-1 launched in?", ["2008", "2010", "2012", "2006"], "2008", "medium"),
        qb("Green Revolution in India associated with?", ["M.S. Swaminathan", "Verghese Kurien", "Norman Borlaug", "C. Subramaniam"], "M.S. Swaminathan", "medium"),
        qb("White Revolution associated with?", ["Verghese Kurien", "M.S. Swaminathan", "Norman Borlaug", "C. Subramaniam"], "Verghese Kurien", "medium"),
        qb("Blue Revolution relates to?", ["Fisheries", "Dairy", "Water conservation", "Space"], "Fisheries", "medium"),
        qb("PM Gati Shakti launched in?", ["2021", "2020", "2022", "2019"], "2021", "hard"),
        qb("Production Linked Incentive (PLI) scheme announced in?", ["2020", "2019", "2021", "2018"], "2020", "hard"),
        qb("New Parliament building inaugurated in?", ["2023", "2022", "2024", "2021"], "2023", "medium"),
        qb("Citizenship Amendment Act passed in?", ["2019", "2018", "2020", "2017"], "2019", "medium"),
        qb("One Nation One Ration Card launched in?", ["2020", "2019", "2021", "2018"], "2020", "hard"),
        qb("Gaganyaan is India's?", ["Human spaceflight programme", "Mars mission", "Sun mission", "Navigation satellite"], "Human spaceflight programme", "medium"),
        qb("India's first nuclear reactor?", ["Apsara", "Dhruva", "Cirus", "Kamini"], "Apsara", "hard"),
        qb("Siachen conflict began in?", ["1984", "1971", "1999", "1962"], "1984", "hard"),
        qb("Shimla Agreement signed after?", ["1971 war", "1965 war", "Kargil war", "1962 war"], "1971 war", "medium"),
        qb("Tashkent Agreement after?", ["1965 war", "1971 war", "Kargil war", "1962 war"], "1965 war", "medium"),
        qb("First Pokhran nuclear test (Smiling Buddha)?", ["1974", "1998", "1962", "1980"], "1974", "medium"),
        qb("Rajiv Gandhi assassination year?", ["1991", "1990", "1992", "1989"], "1991", "medium"),
        qb("India's first PM from BJP?", ["Atal Bihari Vajpayee", "Narendra Modi", "L.K. Advani", "Morarji Desai"], "Atal Bihari Vajpayee", "medium"),
        qb("India's longest serving PM?", ["Jawaharlal Nehru", "Indira Gandhi", "Manmohan Singh", "Narendra Modi"], "Jawaharlal Nehru", "medium"),
        qb("Aadhaar project launched in?", ["2009", "2010", "2014", "2016"], "2009", "medium"),
        qb("UDAN regional connectivity scheme launched in?", ["2016", "2015", "2017", "2018"], "2016", "hard"),
        qb("Stand Up India launched in?", ["2016", "2015", "2017", "2018"], "2016", "hard"),
        qb("Atal Tunnel (Rohtang) inaugurated in?", ["2020", "2019", "2021", "2018"], "2020", "hard"),
        qb("Delhi Metro started operations in?", ["2002", "2000", "2005", "1998"], "2002", "hard"),
        qb("Golden Revolution relates to?", ["Horticulture", "Oilseeds", "Eggs", "Wheat"], "Horticulture", "hard"),
        qb("PM-KISAN-ൽ annual benefit per farmer?", ["₹6000", "₹8000", "₹5000", "₹10000"], "₹6000", "medium"),
        qb("Planning Commission replaced by NITI Aayog on?", ["2015 ജനുവരി 1", "2014 ഓഗസ്റ്റ് 15", "2016 ഏപ്രിൽ 1", "2017 മാർച്ച് 31"], "2015 ജനുവരി 1", "medium"),
        qb("Lahore Declaration signed in?", ["1999", "2000", "1998", "2001"], "1999", "hard"),
        qb("Jammu and Kashmir bifurcated into UTs in?", ["2019", "2020", "2018", "2021"], "2019", "medium"),
    ])
    return qs


def build_sports() -> list[Question]:
    return [
        qb("2024 പാരീസ് ഒളിമ്പിക്സ് നടന്ന വേദി?", ["പാരീസ്", "ടോക്കിയോ", "ലണ്ടൻ", "ലോസ് ആഞ്ചൽസ്"], "പാരീസ്", "easy"),
        qb("2028 ഒളിമ്പിക്സ് നടക്കാൻ നിശ്ചയിച്ച നഗരം?", ["ലോസ് ആഞ്ചൽസ്", "പാരീസ്", "ബ്രിസ്ബേൻ", "ടോക്കിയോ"], "ലോസ് ആഞ്ചൽസ്", "medium"),
        qb("2032 ഒളിമ്പിക്സ് ആതിഥ്യ നഗരം?", ["ബ്രിസ്ബേൻ", "പാരീസ്", "ലോസ് ആഞ്ചൽസ്", "ടോക്കിയോ"], "ബ്രിസ്ബേൻ", "medium"),
        qb("2023 ICC Cricket World Cup-ന്റെ വിജയി?", ["ഓസ്ട്രേലിയ", "ഇന്ത്യ", "ഇംഗ്ലണ്ട്", "ന്യൂസിലൻഡ്"], "ഓസ്ട്രേലിയ", "medium"),
        qb("2023 ICC Cricket World Cup അന്തിമ മത്സര വേദി?", ["അഹമദാബാദ്", "മുംബൈ", "കൊൽക്കത്ത", "ചെന്നൈ"], "അഹമദാബാദ്", "medium"),
        qb("ഏറ്റവും കൂടുതൽ ടെസ്റ്റ് സെഞ്ചuries നേടിയത് സച്ചിൻ ടെൻഡുൽക്കർ?", ["51", "49", "45", "55"], "51", "hard"),
        qb("ഏറ്റവും കൂടുതൽ ODI റൺസ് നേടിയ താരം?", ["സച്ചിൻ ടെൻഡുൽക്കർ", "വിരാട് കോഹ്ലി", "റിക്കി പോണ്ടിംഗ്", "കുമാർ സംഗക്കാര"], "സച്ചിൻ ടെൻഡുൽക്കർ", "medium"),
        qb("2024 IPL-ന്റെ വിജയി?", ["കൊൽക്കത്ത നൈറ്റ് റൈഡേഴ്സ്", "ചെന്നൈ സൂപ്പർ കിംഗ്സ്", "മുംബൈ ഇന്ത്യൻസ്", "സൺറൈസേഴ്സ് ഹൈദരാബാദ്"], "കൊൽക്കത്ത നൈറ്റ് റൈഡേഴ്സ്", "medium"),
        qb("2022 FIFA World Cup-ന്റെ വിജയി?", ["അർജന്റീന", "ഫ്രാൻസ്", "ബ്രാസീൽ", "ജർമ്മനി"], "അർജന്റീന", "easy"),
        qb("2022 FIFA World Cup-ന്റെ ആതിഥ്യ രാജ്യം?", ["ഖത്തർ", "റഷ്യ", "ബ്രാസീൽ", "ദക്ഷിണാഫ്രിക്ക"], "ഖത്തർ", "easy"),
        qb("P.V. സിന്ധു 2020 ഒളിമ്പിക് മെഡൽ നിറം?", ["വെങ്കലം", "സ്വർണ്ണം", "വെള്ളി", "ഒന്നുമില്ല"], "വെങ്കലം", "hard"),
        qb("നീരജ് ചോപ്രയുടെ ഒളിമ്പിക് സ്വർണ്ണ മെഡൽ ഇവന്റ്?", ["അമ്പെറിങ്ങ്", "ഡിസ്കസ് തൂക്കൽ", "ഷോട്ട് പുട്ട്", "നീണ്ട ചാട്ടം"], "അമ്പെറിങ്ങ്", "medium"),
        qb("നീരജ് ചോപ്രയുടെ ഒളിമ്പിക് സ്വർണ്ണം ഏത് വർഷം?", ["2021 ടോക്കിയോ", "2016 റിയോ", "2024 പാരീസ്", "2012 ലണ്ടൻ"], "2021 ടോക്കിയോ", "medium"),
        qb("കേരള ബ്ലാസ്റ്റേഴ്സ് FC ഏത് ലീഗിൽ കളിക്കുന്നു?", ["ISL", "I-League", "EPL", "La Liga"], "ISL", "easy"),
        qb("ജവഹർലാൽ നെഹ്റു സ്റ്റേഡിയം (കൊച്ചി) പ്രധാനമായും എന്തിനാണ്?", ["ഫുട്ബോളും ക്രിക്കറ്റും", "ഹോക്കി മാത്രം", "നീന്തൽ", "ട്രാക്ക്-ഫീൽഡ് മാത്രം"], "ഫുട്ബോളും ക്രിക്കറ്റും", "medium"),
        qb("ഗ്രീൻഫീൽഡ് അന്താരാഷ്ട്ര സ്റ്റേഡിയം എവിടെയാണ്?", ["കരിയാവട്ടം, തിരുവനന്തപുരം", "കലൂർ, കൊച്ചി", "കണ്ണൂർ", "കോഴിക്കോട്"], "കരിയാവട്ടം, തിരുവനന്തപുരം", "hard"),
        qb("അർജുന അവാർഡ് എന്തിനാണ് നൽകുന്നത്?", ["മികച്ച കായിക താരങ്ങൾ", "ചലച്ചിത്ര കലാകാരന്മാർ", "ശാസ്ത്രജ്ഞർ", "എഴുത്തുകാർ"], "മികച്ച കായിക താരങ്ങൾ", "easy"),
        qb("ദ്രോണാചാര്യ അവാർഡ് ആർക്കാണ് നൽകുന്നത്?", ["പരിശീലകർ", "കളിക്കാർ", "അംപയർമാർ", "ഭരണാധികാരികൾ"], "പരിശീലകർ", "medium"),
        qb("രാജീവ് ഗാന്ധി ഖേൽ രത്നത്തിന്റെ പുതിയ പേര്?", ["മേജർ ധ്യാൻ ചന്ദ് ഖേൽ രത്ന", "ദ്രോണാചാര്യ അവാർഡ്", "അർജുന അവാർഡ്", "പദ്മശ്രീ"], "മേജർ ധ്യാൻ ചന്ദ് ഖേൽ രത്ന", "hard"),
        qb("ഒളിമ്പിക് മുദ്രാവാക്യം 'Citius, Altius, Fortius'-ന്റെ അർത്ഥം?", ["വേഗം, ഉയരം, ശക്തി", "ഐക്യം, വിശ്വാസം, അച്ചടക്കം", "നീതിയുപയോഗിച്ച് കളിക്കുക", "സിറ്റിയസ് മാത്രം"], "വേഗം, ഉയരം, ശക്തി", "hard"),
        qb("T20-യിൽ ഒരു പക്ഷത്തിന് പരമാവധി ഓവറുകൾ എത്ര?", ["20", "50", "10", "15"], "20", "easy"),
        qb("ടെസ്റ്റ് ക്രിക്കറ്റിൽ പരമാവധി ദിവസങ്ങൾ?", ["5", "4", "3", "6"], "5", "easy"),
        qb("FIFA World Cup എത്ര വർഷത്തിലൊരിക്കൽ നടക്കുന്നു?", ["4 വർഷത്തിലൊരിക്കൽ", "2 വർഷത്തിലൊരിക്കൽ", "3 വർഷത്തിലൊരിക്കൽ", "5 വർഷത്തിലൊരിക്കൽ"], "4 വർഷത്തിലൊരിക്കൽ", "easy"),
        qb("ഇന്ത്യയുടെ ആദ്യ ഒളിമ്പിക് ഹോക്കി സ്വർണ്ണം ഏത് വർഷം?", ["1928", "1932", "1948", "1952"], "1928", "hard"),
        qb("വിശ്വനാഥൻ ആനന്ദ് ആദ്യം ലോക ചാമ്പ്യൻ ആയ വർഷം?", ["2000", "2007", "1995", "2010"], "2000", "hard"),
        qb("പി.ടി. ഉഷ ഏത് കായിക ഇവന്റുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?", ["ട്രാക്ക്-ഫീൽഡ്", "നീന്തൽ", "ഭാരോദ്വഹനം", "ബോക്സിംഗ്"], "ട്രാക്ക്-ഫീൽഡ്", "easy"),
        qb("മിൽഖാ സിംഗിന്റെ വിളിപ്പേര്?", ["ഫ്ലൈയിംഗ് സിഖ്", "ഹരിയാന ഹറിക്കേൻ", "ലിറ്റിൽ മാസ്റ്റർ", "ക്യാപ്റ്റൻ കൂൾ"], "ഫ്ലൈയിംഗ് സിഖ്", "medium"),
        qb("കപിൽ ദേവ് ഇന്ത്യയെ World Cup-ിൽ നയിച്ച വർഷം?", ["1983", "1987", "1992", "1975"], "1983", "easy"),
        qb("എം.എസ്. ധോണി ക്യാപ്റ്റനായി നേടിയ ICC ട്രോഫികൾ?", ["എല്ലാ പ്രധാന ICC ട്രോഫികളും", "T20 മാത്രം", "ODI മാത്രം", "ടെസ്റ്റ് മാത്രം"], "എല്ലാ പ്രധാന ICC ട്രോഫികളും", "hard"),
        qb("വിംബിൾഡൺ ഏത് കോർട്ടിൽ നടക്കുന്നു?", ["പുലു", "കളിമൺ", "ഹാർഡ് കോർട്ട്", "സിന്തറ്റിക്"], "പുലു", "medium"),
        qb("ഫ്രഞ്ച് ഓപ്പൺ ഏത് കോർട്ടിൽ?", ["കളിമൺ", "പുലു", "ഹാർഡ് കോർട്ട്", "പരിപ്പ്"], "കളിമൺ", "medium"),
        qb("യുഎസ് ഓപ്പൺ ഏത് കോർട്ടിൽ?", ["ഹാർഡ് കോർട്ട്", "പുലു", "കളിമൺ", "മണൽ"], "ഹാർഡ് കോർട്ട്", "medium"),
        qb("ഓസ്ട്രേലിയൻ ഓപ്പൺ ഏത് കോർട്ടിൽ?", ["ഹാർഡ് കോർട്ട്", "പുലു", "കളിമൺ", "മരം"], "ഹാർഡ് കോർട്ട്", "medium"),
        qb("ഒളിമ്പിക് ജ്വാലാ പാരമ്പര്യം ആരംഭിച്ച വേദി?", ["1936 ബെർലിൻ", "1896 ഏതൻസ്", "1924 പാരീസ്", "1900 പാരീസ്"], "1936 ബെർലിൻ", "hard"),
        qb("കേരള കായിക കൗൺസിൽ ആസ്ഥാനം?", ["തിരുവനന്തപുരം", "കൊച്ചി", "കോഴിക്കോട്", "തൃശ്ശൂർ"], "തിരുവനന്തപുരം", "medium"),
        qb("2025 നാഷണൽ ഗെയിംസ് ആതിഥ്യ സംസ്ഥാനം?", ["ഉത്തരാഖണ്ഡ്", "കേരളം", "ഗുജറാത്ത്", "അസം"], "ഉത്തരാഖണ്ഡ്", "hard"),
        qb("തോമസ് കപ്പ് ഏത് കായികവുമായി ബന്ധപ്പെട്ടത്?", ["ബാഡ്മിന്റൺ", "ടെന്നീസ്", "ടേബിൾ ടെന്നീസ്", "ക്രിക്കറ്റ്"], "ബാഡ്മിന്റൺ", "medium"),
        qb("ഡേവിസ് കപ്പ് ഏത് കായികവുമായി ബന്ധപ്പെട്ടത്?", ["ടെന്നീസ്", "ബാഡ്മിന്റൺ", "ഹോക്കി", "ഫുട്ബോൾ"], "ടെന്നീസ്", "medium"),
        qb("റഞ്ജി ട്രോഫി ഏത് കായികവുമായി ബന്ധപ്പെട്ടത്?", ["ക്രിക്കറ്റ്", "ഫുട്ബോൾ", "ഹോക്കി", "കബഡി"], "ക്രിക്കറ്റ്", "easy"),
        qb("സന്തോഷ് ട്രോഫി ഏത് കായികവുമായി ബന്ധപ്പെട്ടത്?", ["ഫുട്ബോൾ", "ക്രിക്കറ്റ്", "ഹോക്കി", "വോളിബോൾ"], "ഫുട്ബോൾ", "medium"),
        qb("പ്രോ കബഡി ലീഗ് ആരംഭിച്ച വർഷം?", ["2014", "2010", "2018", "2016"], "2014", "hard"),
        qb("2022 കോമൺവെൽത്ത് ഗെയിംസ് നടന്ന വേദി?", ["ബർമിംഗ്ഹാം", "ഗോൾഡ് കോസ്റ്റ്", "ഡൽഹി", "ഗ്ലാസ്ഗോ"], "ബർമിംഗ്ഹാം", "medium"),
        qb("2023 ഏഷ്യൻ ഗെയിംസ് നടന്ന വേദി?", ["ഹാങ്ചൺ", "ജക്കാർത്ത", "ഗുവാങ്ചൗ", "ഇഞ്ചിയോൺ"], "ഹാങ്ചൺ", "medium"),
        qb("ഒളിമ്പിക് വളയങ്ങളുടെ നിറങ്ങളുടെ എണ്ണം?", ["5", "4", "6", "7"], "5", "easy"),
        qb("ക്രിക്കറ്റ് പിച്ചിന്റെ നീളം (യാർഡ്)?", ["22", "20", "24", "18"], "22", "hard"),
        qb("ഫുട്ബോൾ ഗോൾ വീതി (മീറ്റർ, ഏകദേശം)?", ["7.32", "5", "10", "8"], "7.32", "hard"),
        qb("ഫുട്ബോൾ മൈതാനത്ത് ഒരു ടീമിലെ പരമാവധി കളിക്കാർ?", ["11", "10", "12", "9"], "11", "easy"),
        qb("ബാഡ്മിന്റൺ ഷട്ടിൽകോക്ക് പരമ്പരാഗത പദാർത്ഥം?", ["തൂവൽ", "റബ്ബർ", "പ്ലാസ്റ്റിക് മാത്രം", "മരം"], "തൂവൽ", "medium"),
        qb("ക്രിക്കറ്റ് പന്തിന്റെ ഭാരം (ഏകദേശം)?", ["155-163 ഗ്രാം", "100 g", "200 g", "250 g"], "155-163 ഗ്രാം", "hard"),
        qb("ബാസ്ക്കറ്റ്ബോൾ ഹൂപ്പിന്റെ ഉയരം (തറയിൽ നിന്ന്)?", ["10 അടി", "8 അടി", "12 അടി", "9 അടി"], "10 അടി", "medium"),
        qb("കേരള കായികതാരി ജെസ്ന ജേക്കബ് ഏത് ഇവന്റുമായി ബന്ധപ്പെട്ടിരിക്കുന്നു?", ["നീണ്ട ചാട്ടം/ട്രാക്ക്-ഫീൽഡ്", "നീന്തൽ", "മല്ലയുദ്ധം", "വില്ലുവെട്ട്"], "നീണ്ട ചാട്ടം/ട്രാക്ക്-ഫീൽഡ്", "hard"),
    ]


def build_national_schemes() -> list[Question]:
    data = [
        ("PM Vishwakarma", "2023", ["2021", "2022", "2024"], "medium"),
        ("PM SVANidhi", "2020", ["2018", "2019", "2021"], "medium"),
        ("PM FME (Formalisation of Micro Food Processing)", "2020", ["2018", "2019", "2022"], "hard"),
        ("PM Matsya Sampada Yojana", "2020", ["2018", "2019", "2022"], "hard"),
        ("PM Garib Kalyan Anna Yojana", "2020", ["2018", "2019", "2022"], "medium"),
        ("PM CARES Fund", "2020", ["2018", "2019", "2022"], "medium"),
        ("Har Ghar Jal (Jal Jeevan Mission)", "2019", ["2017", "2018", "2020"], "medium"),
        ("BharatNet", "2011", ["2009", "2010", "2012"], "hard"),
        ("Skill India Mission", "2015", ["2013", "2014", "2016"], "medium"),
        ("Beti Bachao Beti Padhao", "2015", ["2013", "2014", "2016"], "easy"),
        ("Sukanya Samriddhi Yojana", "2015", ["2013", "2014", "2016"], "medium"),
        ("Atal Pension Yojana", "2015", ["2013", "2014", "2016"], "medium"),
        ("PM Suraksha Bima Yojana", "2015", ["2013", "2014", "2016"], "medium"),
        ("PM Jeevan Jyoti Bima Yojana", "2015", ["2013", "2014", "2016"], "medium"),
        ("HRIDAY scheme (heritage cities)", "2015", ["2013", "2014", "2016"], "hard"),
        ("AMRUT scheme", "2015", ["2013", "2014", "2016"], "hard"),
        ("SAUBHAGYA (electricity for all)", "2017", ["2015", "2016", "2018"], "medium"),
        ("Ujjwala 2.0", "2021", ["2019", "2020", "2022"], "hard"),
        ("PM-KUSUM (solar for farmers)", "2019", ["2017", "2018", "2020"], "hard"),
        ("National Nutrition Mission (POSHAN Abhiyaan)", "2018", ["2016", "2017", "2019"], "medium"),
    ]
    qs = [qb(f"{n} പദ്ധതി ആരംഭിച്ച വർഷം ഏത്?", w + [a], a, d) for n, a, w, d in data]
    qs.extend([
        qb("PM-JAY-ൽ ഒരു കുടുംബത്തിന് വാർഷിക ആരോഗ്യ പരിരക്ഷ എത്ര?", ["₹5 ലക്ഷം", "₹1 ലക്ഷം", "₹2 ലക്ഷം", "₹10 ലക്ഷം"], "₹5 ലക്ഷം", "easy"),
        qb("MGNREGA-യിൽ guaranteed days of employment?", ["100 days", "150 days", "200 days", "50 days"], "100 days", "medium"),
        qb("PM Awas Yojana-Urban target year originally?", ["2022", "2020", "2025", "2018"], "2022", "hard"),
        qb("Deen Dayal Upadhyaya Gram Jyoti Yojana launched?", ["2015", "2014", "2016", "2013"], "2015", "hard"),
        qb("Kisan Credit Card scheme primarily for?", ["Farmers' credit needs", "Students", "MSME", "Exporters"], "Farmers' credit needs", "easy"),
        qb("PM Fasal Bima Yojana launched?", ["2016", "2014", "2018", "2015"], "2016", "medium"),
        qb("Soil Health Card scheme launched?", ["2015", "2014", "2016", "2013"], "2015", "medium"),
        qb("National Health Mission subsumed which missions?", ["NRHM and NUHM", "Only NRHM", "Only NUHM", "Ayushman only"], "NRHM and NUHM", "hard"),
        qb("PM eVIDYA for?", ["Digital education during COVID", "Agriculture", "Defence", "Railways"], "Digital education during COVID", "medium"),
        qb("One Nation One Ration Card under which ministry?", ["Consumer Affairs/Food & PD", "Home", "Defence", "External Affairs"], "Consumer Affairs/Food & PD", "hard"),
        qb("PM POSHAN Shakti Nirman related to?", ["Anganwadi/nutrition infrastructure", "Roads", "Ports", "Airports"], "Anganwadi/nutrition infrastructure", "hard"),
        qb("PM Daksh Yojana for?", ["Skill development of youth", "Farmers", "Senior citizens", "Artisans only"], "Skill development of youth", "hard"),
        qb("National Infrastructure Pipeline announced?", ["2019", "2017", "2021", "2015"], "2019", "hard"),
        qb("PM Gati Shakti master plan related to?", ["Integrated infrastructure planning", "Health", "Education", "Defence"], "Integrated infrastructure planning", "medium"),
        qb("Production Linked Incentive maximum sectors covered approx?", ["14+ sectors", "5 sectors", "3 sectors", "20 sectors only"], "14+ sectors", "hard"),
        qb("PM SHRI schools scheme for?", ["Upgrading schools to exemplary status", "Only IITs", "Only medical colleges", "Private schools only"], "Upgrading schools to exemplary status", "hard"),
        qb("National Edible Oil Mission-Oil Palm (NMEO-OP) launched?", ["2021", "2019", "2020", "2022"], "2021", "hard"),
        qb("PM DevINE for?", ["North-East development", "Western Ghats", "Desert areas", "Islands only"], "North-East development", "hard"),
        qb("Rashtriya Krishi Vikas Yojana is?", ["Agriculture development scheme", "Health scheme", "Defence scheme", "Space scheme"], "Agriculture development scheme", "medium"),
        qb("PM-KMY (Kisan Maan Dhan) for?", ["Pension for small farmers", "Crop insurance", "Irrigation", "Seeds subsidy"], "Pension for small farmers", "hard"),
        qb("SVAMITVA scheme for?", ["Rural property ownership records", "Urban housing", "Coastal fishing", "Mining"], "Rural property ownership records", "hard"),
        qb("PM MITRA textile parks announced?", ["2021", "2019", "2020", "2022"], "2021", "hard"),
        qb("National Mission on Edible Oils-Oil Palm ministry?", ["Agriculture", "Defence", "Railways", "External Affairs"], "Agriculture", "hard"),
        qb("PM Vishwakarma scheme for?", ["Traditional artisans/craftspeople", "IT professionals", "Doctors", "Lawyers"], "Traditional artisans/craftspeople", "medium"),
        qb("PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi) for?", ["Street vendors", "Large corporates", "Farmers only", "Students only"], "Street vendors", "medium"),
        qb("Jal Shakti Ministry formed in?", ["2019", "2017", "2021", "2014"], "2019", "hard"),
        qb("Ayushman Bharat Health Infrastructure Mission launched?", ["2020", "2018", "2019", "2021"], "2020", "hard"),
        qb("PM CARES Fund tax exemption status?", ["Trust donations eligible for 80G", "Not eligible", "Only companies", "Only foreign"], "Trust donations eligible for 80G", "hard"),
        qb("PM Garib Kalyan package during COVID first announced?", ["2020", "2019", "2021", "2018"], "2020", "medium"),
        qb("National Digital Health Mission (ABDM) launched?", ["2020", "2018", "2019", "2021"], "2020", "hard"),
        qb("PM WANI for?", ["Public Wi-Fi access", "Water supply", "Roads", "Railways"], "Public Wi-Fi access", "hard"),
        qb("Mission Karmayogi for?", ["Civil services capacity building", "Defence", "Police only", "Judiciary only"], "Civil services capacity building", "hard"),
        qb("PM eBus Sewa for?", ["Electric buses in cities", "Rural roads", "Airports", "Ports"], "Electric buses in cities", "hard"),
        qb("National Green Hydrogen Mission launched?", ["2023", "2021", "2022", "2024"], "2023", "hard"),
        qb("PM JANMAN for?", ["PVTG welfare", "Urban poor", "Large farmers", "Exporters"], "PVTG welfare", "hard"),
        qb("PM Surya Ghar Muft Bijli Yojana for?", ["Rooftop solar for households", "Coal mining", "Nuclear plants", "Wind only"], "Rooftop solar for households", "hard"),
        qb("PM Internship Scheme announced budget year?", ["2024", "2022", "2023", "2020"], "2024", "hard"),
        qb("Vibrant Villages Programme for?", ["Border villages development", "Metro cities", "Coastal only", "Desert only"], "Border villages development", "hard"),
        qb("PM Vishwakarma minimum loan amount (approx)?", ["₹1 lakh (without collateral)", "₹10 lakh", "₹50,000", "₹5 lakh"], "₹1 lakh (without collateral)", "hard"),
        qb("PM FME unit cost ceiling (approx)?", ["₹10 lakh", "₹1 crore", "₹50 lakh", "₹25 lakh"], "₹10 lakh", "hard"),
        qb("PM Matsya Sampada investment target period?", ["2020-25", "2015-20", "2025-30", "2010-15"], "2020-25", "hard"),
    ])
    return qs


def build_social_welfare() -> list[Question]:
    data = [
        ("കരുണ്യ ആരോഗ്യ സുരക്ഷാ പദ്ധതിയുടെ പ്രധാന ലക്ഷ്യം?", ["ആരോഗ്യ ഇൻഷുറൻസ്", "വIDIയാഭ്യാസം", "കാർഷിക വായ്പ", "റോഡ്"], "ആരോഗ്യ ഇൻഷുറൻസ്", "medium"),
        ("കുടുംബശ്രീ പദ്ധതി ആരംഭിച്ച വർഷം?", ["1998", "1995", "2005", "2001"], "1998", "easy"),
        ("ലൈഫ് മിഷൻ പദ്ധതിയുടെ പ്രധാന ലക്ഷ്യം?", ["ഭവനരഹിതർക്ക് വീട്", "കാർഷിക subsidies", "വിദ്യാഭ്യാസം", "യാത്ര"], "ഭവനരഹിതർക്ക് വീട്", "easy"),
        ("ഹരിത കേരളം മിഷൻ ആരംഭിച്ച വർഷം?", ["2017", "2015", "2019", "2020"], "2017", "medium"),
        ("അമ്മത്തൊഴിൽ പദ്ധതി ആരംഭിച്ച വർഷം?", ["2010", "2008", "2012", "2015"], "2010", "medium"),
        ("കുടുംബശ്രീയുടെ മുഖ്യ ലക്ഷ്യം?", ["സ്ത്രീശാക്തീകരണവും ദാരിദ്ര്യനിവാരണവും", "വIDIയാഭ്യാസം മാത്രം", "യാത്ര", "വ്യവസായം മാത്രം"], "സ്ത്രീശാക്തീകരണവും ദാരിദ്ര്യനിവാരണവും", "easy"),
        ("കerala Social Security Mission established?", ["2008", "2005", "2010", "2012"], "2008", "hard"),
        ("Karunya Benevolent Fund for?", ["Medical treatment assistance", "Education only", "Travel", "Sports"], "Medical treatment assistance", "medium"),
        ("Kerala Women's Commission established?", ["1996", "1990", "2000", "2005"], "1996", "hard"),
    ]
    qs = list(data)
    qs.extend([
        qb("Mid-Day Meal scheme national launch year?", ["1995", "2000", "2010", "1980"], "1995", "medium"),
        qb("National Social Assistance Programme (NSAP) includes?", ["Old age, widow, disability pensions", "Only crop insurance", "Only housing", "Only travel"], "Old age, widow, disability pensions", "hard"),
        qb("PMMVY (Maternity Benefit) provides?", ["₹5000 in instalments", "₹50000 lump sum", "₹1000 only", "₹500 only"], "₹5000 in instalments", "hard"),
        qb("Anganwadi services under which scheme?", ["ICDS", "MGNREGA", "PM-JAY", "GST"], "ICDS", "medium"),
        qb("National Food Security Act enacted?", ["2013", "2010", "2015", "2005"], "2013", "medium"),
        qb("Antyodaya Anna Yojana for?", ["Poorest families", "All citizens", "Only farmers", "Only students"], "Poorest families", "medium"),
        qb("PM Garib Kalyan Anna Yojana provides?", ["Free food grains during crisis", "Free laptops", "Free cars", "Free land"], "Free food grains during crisis", "easy"),
        qb("National Rural Livelihood Mission (NRLM) renamed?", ["DAY-NRLM", "PM-KISAN", "PM-JAY", "UDAN"], "DAY-NRLM", "hard"),
        qb("Kerala Kudumbashree is?", ["Community organisation of women", "Men's club", "Political party", "Trade union only"], "Community organisation of women", "easy"),
        qb("Kerala EMS housing scheme known as?", ["Life Mission/LIFE", "PMAY only", "MGNREGA", "UDAN"], "Life Mission/LIFE", "medium"),
        qb("Kerala's Karunya Plus under?", ["Health assistance", "Education", "Transport", "Defence"], "Health assistance", "medium"),
        qb("National Health Mission launched?", ["2013", "2010", "2015", "2005"], "2013", "hard"),
        qb("Rashtriya Swasthya Bima Yojana replaced by?", ["PM-JAY", "PM-KISAN", "GST", "UDAN"], "PM-JAY", "hard"),
        qb("Stand Up India for?", ["SC/ST and women entrepreneurs", "Only farmers", "Only students", "Only defence"], "SC/ST and women entrepreneurs", "medium"),
        qb("National Handicapped Finance Corporation for?", ["PwD welfare", "Farmers", "Exporters", "Railways"], "PwD welfare", "hard"),
        qb("Kerala SC/ST Development Department schemes include?", ["Educational concessions", "Only sports", "Only cinema", "Only ports"], "Educational concessions", "hard"),
        qb("Old Age Pension Kerala age criterion (approx)?", ["60 years", "50 years", "70 years only", "40 years"], "60 years", "hard"),
        qb("Widow Pension scheme in Kerala administered by?", ["Social Justice Department", "Sports Council", "Film Academy", "Port Authority"], "Social Justice Department", "hard"),
        qb("Disability pension requires minimum disability?", ["40%", "10%", "20%", "80% only"], "40%", "hard"),
        qb("National Programme for Health Care of Elderly launched?", ["2010", "2000", "2015", "2005"], "2010", "hard"),
        qb("Kerala Palliative Care policy focus?", ["End-of-life care", "Sports training", "Mining", "Ports"], "End-of-life care", "hard"),
        qb("She-Box portal for?", ["Women workplace harassment complaints", "Tax filing", "Passport", "GST"], "Women workplace harassment complaints", "hard"),
        qb("One Stop Centre scheme (Sakhi) for?", ["Women affected by violence", "Men only", "Children sports", "Farmers only"], "Women affected by violence", "hard"),
        qb("Ujjawala scheme for?", ["Trafficking victims rehabilitation", "LPG only", "Crop insurance", "Roads"], "Trafficking victims rehabilitation", "hard"),
        qb("PM Matru Vandana Yojana is?", ["Maternity benefit scheme", "Crop insurance", "Housing only", "Travel only"], "Maternity benefit scheme", "medium"),
        qb("National Creche Scheme for?", ["Working women's children", "Elderly only", "Farmers only", "Defence only"], "Working women's children", "hard"),
        qb("Kerala's Subhiksha Keralam during COVID related to?", ["Food security", "Space mission", "Defence", "Film festival"], "Food security", "medium"),
        qb("Ayushman Bharat covers how many beneficiaries (approx target)?", ["50 crore", "10 crore", "100 crore", "1 crore"], "50 crore", "hard"),
        qb("PM-JAY empaneled hospitals provide?", ["Cashless treatment", "Only diagnostics", "Only medicines outside", "Only consultation"], "Cashless treatment", "medium"),
        qb("National Ayush Mission for?", ["AYUSH systems promotion", "Allopathy only", "Defence", "Railways"], "AYUSH systems promotion", "hard"),
        qb("Kerala Mental Health Policy focus?", ["Community mental health", "Only sports", "Only mining", "Only cinema"], "Community mental health", "hard"),
        qb("Integrated Child Development Services (ICDS) components include?", ["Supplementary nutrition, immunization", "Only roads", "Only defence", "Only GST"], "Supplementary nutrition, immunization", "medium"),
        qb("National Nutrition Strategy launched?", ["2017", "2015", "2019", "2010"], "2017", "hard"),
        qb("POSHAN Abhiyaan target to reduce?", ["Stunting and malnutrition", "Road accidents only", "Air pollution only", "Tax evasion"], "Stunting and malnutrition", "medium"),
        qb("Kerala's Haritha Karma Sena associated with?", ["Waste management", "Defence", "Space", "Ports only"], "Waste management", "medium"),
        qb("National Social Assistance Programme old age pension amount (central share approx)?", ["₹200-500 varies by state", "₹5000", "₹50000", "₹50"], "₹200-500 varies by state", "hard"),
        qb("PM SVANidhi collateral free loan up to?", ["₹10,000 first tranche", "₹10 lakh", "₹1 crore", "₹1000"], "₹10,000 first tranche", "hard"),
        qb("National Rural Drinking Water Programme now part of?", ["Jal Jeevan Mission", "PM-KISAN", "GST", "UDAN"], "Jal Jeevan Mission", "hard"),
        qb("Kerala's Vayomithram for?", ["Elderly care services", "Youth sports", "Infants only", "Defence"], "Elderly care services", "hard"),
        qb("National Action Plan for Children under?", ["Ministry of Women and Child Development", "Defence", "Railways", "External Affairs"], "Ministry of Women and Child Development", "hard"),
        qb("PM CARES for Children scheme for?", ["COVID orphaned children", "All students", "All farmers", "All soldiers"], "COVID orphaned children", "hard"),
        qb("Kerala Building and Other Construction Workers Welfare Board for?", ["Construction workers welfare", "IT workers", "Doctors only", "Lawyers only"], "Construction workers welfare", "hard"),
        qb("National Family Benefit Scheme provides on death of primary breadwinner?", ["₹20000 lump sum", "₹5000 monthly", "₹1 lakh monthly", "₹100"], "₹20000 lump sum", "hard"),
        qb("Kerala's Sneha Purvam for?", ["Orphaned children education support", "Sports only", "Mining", "Ports"], "Orphaned children education support", "hard"),
        qb("National Livelihood Mission urban component?", ["DAY-NULM", "DAY-NRLM", "PM-JAY", "GST"], "DAY-NULM", "hard"),
        qb("PM Formalisation of Micro Food Processing scheme for?", ["Micro food enterprises", "Large steel plants", "Defence", "Space"], "Micro food enterprises", "hard"),
        qb("Kerala's Karunya health scheme initial year?", ["2012", "2000", "2020", "1990"], "2012", "hard"),
        qb("National Social Assistance Programme launched?", ["1999", "2010", "2015", "2005"], "1999", "hard"),
        qb("PM Jan Dhan minimum balance requirement (rural)?", ["Zero balance allowed", "₹10000", "₹50000", "₹1 lakh"], "Zero balance allowed", "medium"),
        qb("Kerala's Aswasakiranam for?", ["Caregivers of bedridden patients", "Sports coaches", "Film directors", "Port workers"], "Caregivers of bedridden patients", "hard"),
        qb("കerala സാമൂഹിക സുരക്ഷാ മിഷൻ ആരംഭിച്ച വർഷം?", ["2008", "2005", "2010", "2012"], "2008", "hard"),
    ])
    return qs


def build_indian_industries() -> list[Question]:
    psus = [
        ("BHEL", "Power equipment", ["Defence only", "Space only", "Banking"]),
        ("HAL", "Aerospace/Defence", ["Textiles", "Fisheries", "Tourism"]),
        ("SAIL", "Steel", ["Software", "Pharma only", "Tourism"]),
        ("ONGC", "Oil and gas exploration", ["Railways", "Post office", "Tourism"]),
        ("NTPC", "Power generation", ["Textiles", "Fisheries", "Film"]),
        ("IOCL", "Oil refining/marketing", ["Space", "Defence only", "Tourism"]),
        ("Coal India", "Coal mining", ["Software", "Pharma", "Film"]),
        ("GAIL", "Natural gas", ["Coal mining", "Shipbuilding", "Film"]),
        ("NHPC", "Hydro power", ["Coal", "Textiles", "Film"]),
        ("BEL", "Defence electronics", ["Textiles", "Fisheries", "Tourism"]),
        ("BEML", "Heavy equipment", ["Pharma", "Film", "Tourism only"]),
        ("HMT", "Machine tools (legacy)", ["Space launch", "Banking", "Insurance only"]),
        ("MIDHANI", "Special metals/alloys", ["Textiles", "Fisheries", "Tourism"]),
        ("NLC India", "Lignite mining/power", ["Software", "Film", "Tourism"]),
        ("SCI", "Shipping", ["Coal mining", "Textiles", "Film"]),
    ]
    qs = [qb(f"{n} PSU പ്രധാന മേഖല?", [s] + others, s, "medium") for n, s, others in psus]
    qs.extend([
        qb("Make in India logo animal?", ["Lion", "Tiger", "Elephant", "Peacock"], "Lion", "easy"),
        qb("Delhi-Mumbai Industrial Corridor (DMIC) length approx?", ["1500 km", "500 km", "3000 km", "200 km"], "1500 km", "hard"),
        qb("Chennai-Bengaluru Industrial Corridor part of?", ["East Coast Economic Corridor", "DMIC only", "None", "Himalayan corridor"], "East Coast Economic Corridor", "hard"),
        qb("Amritsar-Kolkata Industrial Corridor aligned along?", ["Eastern Dedicated Freight Corridor", "Western DFC only", "Coastal road only", "None"], "Eastern Dedicated Freight Corridor", "hard"),
        qb("Visakhapatnam-Chennai Industrial Corridor in which state mostly?", ["Andhra Pradesh", "Punjab", "Rajasthan", "Kerala"], "Andhra Pradesh", "hard"),
        qb("Bengaluru-Mumbai Industrial Corridor states include?", ["Karnataka and Maharashtra", "Kerala only", "Assam only", "Punjab only"], "Karnataka and Maharashtra", "hard"),
        qb("National Manufacturing Policy target share of GDP?", ["25%", "10%", "50%", "5%"], "25%", "hard"),
        qb("Pharma sector 'Pharmacy of the World' refers to?", ["India", "USA", "Japan", "Brazil"], "India", "medium"),
        qb("IT industry hub Bengaluru nickname?", ["Silicon Valley of India", "Detroit of India", "Steel City", "Pink City"], "Silicon Valley of India", "easy"),
        qb("Detroit of India often refers to?", ["Chennai (automobile)", "Jaipur", "Shimla", "Panaji"], "Chennai (automobile)", "medium"),
        qb("Largest refinery in India (Jamnagar) owned by?", ["Reliance", "ONGC only", "SAIL", "HAL"], "Reliance", "medium"),
        qb("Steel Authority of India headquarters?", ["New Delhi", "Mumbai", "Kolkata", "Chennai"], "New Delhi", "hard"),
        qb("Indian Space Research Organisation (ISRO) HQ?", ["Bengaluru", "Hyderabad", "Chennai", "Mumbai"], "Bengaluru", "easy"),
        qb("Defence Research and Development Organisation (DRDO) HQ?", ["New Delhi", "Pune only", "Kochi", "Guwahati"], "New Delhi", "medium"),
        qb("Hindustan Aeronautics Limited (HAL) HQ?", ["Bengaluru", "Mumbai", "Delhi", "Kolkata"], "Bengaluru", "medium"),
        qb("Bharat Electronics Limited (BEL) HQ?", ["Bengaluru", "Mumbai", "Chennai", "Kolkata"], "Bengaluru", "hard"),
        qb("National Aluminium Company (NALCO) HQ?", ["Bhubaneswar", "Delhi", "Mumbai", "Chennai"], "Bhubaneswar", "hard"),
        qb("Hindustan Petroleum HQ city?", ["Mumbai", "Delhi", "Chennai", "Kolkata"], "Mumbai", "hard"),
        qb("Maruti Suzuki manufacturing primarily in?", ["Haryana/Gujarat", "Kerala", "Assam only", "Goa only"], "Haryana/Gujarat", "medium"),
        qb("Tata Steel major plant at?", ["Jamshedpur", "Jaipur", "Shimla", "Panaji"], "Jamshedpur", "medium"),
        qb("Indian Oil refineries count (approx)?", ["10+", "2", "50", "100"], "10+", "hard"),
        qb("Textile industry major cluster Tiruppur known for?", ["Knitwear exports", "Coal", "Oil refining", "Space"], "Knitwear exports", "hard"),
        qb("Diamond cutting hub in India?", ["Surat", "Jaipur only", "Shimla", "Panaji"], "Surat", "hard"),
        qb("Leather industry hub?", ["Kanpur/Chennai", "Shimla", "Gangtok", "Panaji"], "Kanpur/Chennai", "hard"),
        qb("Software Technology Parks of India (STPI) established?", ["1991", "1980", "2005", "2015"], "1991", "hard"),
        qb("SEZ policy in India announced?", ["2000", "1990", "2010", "1985"], "2000", "hard"),
        qb("Production Linked Incentive first sector?", ["Mobile manufacturing", "Coal", "Fisheries", "Film"], "Mobile manufacturing", "hard"),
        qb("National Industrial Corridor Development Programme nodal?", ["DPIIT", "Defence Ministry", "External Affairs", "Home"], "DPIIT", "hard"),
        qb("MSME definition micro enterprise investment limit (manufacturing approx)?", ["₹2.5 crore", "₹100 crore", "₹500 crore", "₹1000 crore"], "₹2.5 crore", "hard"),
        qb("Khadi and Village Industries Commission (KVIC) for?", ["Rural industries", "Defence", "Space", "Film only"], "Rural industries", "medium"),
        qb("Coir industry major state?", ["Kerala", "Punjab", "Rajasthan", "Himachal"], "Kerala", "easy"),
        qb("Spices Board HQ?", ["Kochi", "Delhi", "Mumbai", "Chennai"], "Kochi", "hard"),
        qb("Rubber Board HQ?", ["Kottayam", "Delhi", "Mumbai", "Chennai"], "Kottayam", "hard"),
        qb("Tea Board HQ?", ["Kolkata", "Kochi", "Delhi", "Chennai"], "Kolkata", "hard"),
        qb("Coffee Board HQ?", ["Bengaluru", "Kochi", "Delhi", "Mumbai"], "Bengaluru", "hard"),
        qb("Handicrafts sector major export item?", ["Handmade carpets/textiles", "Coal", "Oil only", "Iron ore only"], "Handmade carpets/textiles", "hard"),
        qb("Shipbuilding major PSU?", ["Cochin Shipyard", "SAIL", "Coal India", "NTPC"], "Cochin Shipyard", "hard"),
        qb("Bharat Heavy Electricals major product?", ["Power plant equipment", "Aircraft carriers only", "Mobile phones only", "Cars only"], "Power plant equipment", "medium"),
        qb("National Investment and Manufacturing Zones (NIMZ) policy year?", ["2011", "2000", "2015", "1990"], "2011", "hard"),
        qb("Industrial Development Bank of India now known as?", ["IDBI Bank", "SBI", "PNB", "HDFC"], "IDBI Bank", "hard"),
        qb("Small Industries Development Bank of India (SIDBI) for?", ["MSME finance", "Defence only", "Space only", "Film only"], "MSME finance", "medium"),
        qb("Export Processing Zone first in India?", ["Kandla", "Kochi", "Delhi", "Chennai"], "Kandla", "hard"),
        qb("Petrochemical hub Panipat in?", ["Haryana", "Kerala", "Tamil Nadu", "Goa"], "Haryana", "hard"),
        qb("Automobile cluster Pune/Chennai associated industry?", ["Automobile manufacturing", "Coir", "Tea only", "Spices only"], "Automobile manufacturing", "easy"),
        qb("Pharma cluster Hyderabad nicknamed?", ["Bulk drug capital", "Steel city", "Pink city", "Blue city"], "Bulk drug capital", "hard"),
        qb("Indian Railways manufacturing unit Chittaranjan makes?", ["Locomotives", "Aircraft", "Ships only", "Mobile phones"], "Locomotives", "hard"),
        qb("Hindustan Shipyard located in?", ["Visakhapatnam", "Kochi", "Mumbai", "Chennai"], "Visakhapatnam", "hard"),
        qb("Mazagon Dock Shipbuilders in?", ["Mumbai", "Kochi", "Delhi", "Chennai"], "Mumbai", "hard"),
        qb("Garden Reach Shipbuilders in?", ["Kolkata", "Mumbai", "Kochi", "Chennai"], "Kolkata", "hard"),
        qb("Goa Shipyard in?", ["Vasco da Gama", "Panaji only", "Delhi", "Chennai"], "Vasco da Gama", "hard"),
    ])
    return qs


def build_international_orgs() -> list[Question]:
    orgs = [
        ("United Nations", "1945", "New York", ["1944", "1946", "1950"], ["Geneva", "Paris", "Rome"]),
        ("UNESCO", "1945", "Paris", ["1944", "1950", "1960"], ["New York", "Geneva", "Vienna"]),
        ("WHO", "1948", "Geneva", ["1945", "1950", "1960"], ["New York", "Paris", "Rome"]),
        ("IMF", "1944", "Washington D.C.", ["1945", "1950", "1960"], ["New York", "London", "Paris"]),
        ("World Bank", "1944", "Washington D.C.", ["1945", "1950", "1960"], ["Geneva", "Paris", "Rome"]),
        ("WTO", "1995", "Geneva", ["1945", "1980", "2000"], ["New York", "Paris", "Rome"]),
        ("ILO", "1919", "Geneva", ["1945", "1950", "2000"], ["New York", "Paris", "Rome"]),
        ("FAO", "1945", "Rome", ["1944", "1950", "1960"], ["New York", "Geneva", "Paris"]),
        ("IAEA", "1957", "Vienna", ["1945", "1960", "1970"], ["New York", "Geneva", "Paris"]),
        ("UNICEF", "1946", "New York", ["1945", "1950", "1960"], ["Geneva", "Paris", "Rome"]),
        ("UNHCR", "1950", "Geneva", ["1945", "1960", "1970"], ["New York", "Paris", "Rome"]),
        ("ASEAN", "1967", "Jakarta", ["1950", "1970", "1980"], ["Bangkok", "Singapore", "Manila"]),
        ("SAARC", "1985", "Kathmandu", ["1975", "1990", "2000"], ["Delhi", "Colombo", "Dhaka"]),
        ("EU", "1993", "Brussels", ["1950", "2000", "2010"], ["Paris", "London", "Rome"]),
        ("NATO", "1949", "Brussels", ["1945", "1960", "1970"], ["Washington", "Paris", "London"]),
        ("OPEC", "1960", "Vienna", ["1950", "1970", "1980"], ["Riyadh", "Dubai", "Tehran"]),
        ("BRICS", "2009", "— (summit host varies)", ["2000", "2015", "2020"], ["New York", "Paris", "London"]),
        ("G7", "1975", "— (rotating host)", ["1960", "1990", "2000"], ["New York only", "Geneva only", "Delhi only"]),
        ("G20", "1999", "— (rotating host)", ["1980", "2010", "2025"], ["New York only", "Paris only", "Rome only"]),
        ("Commonwealth", "1931", "London", ["1945", "1950", "2000"], ["New York", "Geneva", "Paris"]),
        ("African Union", "2002", "Addis Ababa", ["1990", "2010", "2020"], ["Nairobi", "Cairo", "Lagos"]),
        ("OIC", "1969", "Jeddah", ["1950", "1980", "2000"], ["Riyadh", "Cairo", "Istanbul"]),
        ("Interpol", "1923", "Lyon", ["1945", "1950", "2000"], ["Paris", "Geneva", "London"]),
    ]
    qs: list[Question] = []
    for name, year, hq, wy, wh in orgs:
        qs.append(qb(f"{name} സ്ഥാപിതമായ വർഷം ഏത്?", wy + [year], year, "medium"))
        if hq != "— (summit host varies)" and hq != "— (rotating host)":
            qs.append(qb(f"{name} ആസ്ഥാനം ഏത്?", wh + [hq], hq, "medium"))
    qs.append(qb("Red Cross (ICRC) headquarters?", ["Geneva", "New York", "Paris", "Rome"], "Geneva", "medium"))
    qs.extend([
        qb("UN Security Council permanent members count?", ["5", "10", "15", "7"], "5", "easy"),
        qb("UN General Assembly President elected for?", ["One year", "Five years", "Ten years", "Life"], "One year", "hard"),
        qb("International Court of Justice seat?", ["The Hague", "New York", "Geneva", "Paris"], "The Hague", "medium"),
        qb("World Trade Organization replaced?", ["GATT", "UNESCO", "NATO", "WHO"], "GATT", "hard"),
        qb("International Monetary Fund members count (approx)?", ["190+", "50", "100", "300"], "190+", "hard"),
        qb("World Health Organization regional office for South-East Asia in?", ["New Delhi", "Geneva", "Manila", "Cairo"], "New Delhi", "hard"),
        qb("UNDP headquarters?", ["New York", "Geneva", "Paris", "Rome"], "New York", "hard"),
        qb("UNEP headquarters?", ["Nairobi", "New York", "Geneva", "Paris"], "Nairobi", "hard"),
        qb("International Labour Organization Nobel Peace Prize year?", ["1969", "1945", "2000", "1980"], "1969", "hard"),
        qb("SAARC members count?", ["8", "10", "5", "12"], "8", "medium"),
        qb("ASEAN members count?", ["10", "8", "12", "15"], "10", "medium"),
        qb("BRICS original members before expansion?", ["Brazil, Russia, India, China, South Africa", "India only", "G7 members", "ASEAN members"], "Brazil, Russia, India, China, South Africa", "medium"),
        qb("BRICS 2024 expanded new members include?", ["Egypt, Ethiopia, Iran, UAE, Saudi Arabia", "USA, UK", "Japan, Germany", "Australia only"], "Egypt, Ethiopia, Iran, UAE, Saudi Arabia", "hard"),
        qb("Shanghai Cooperation Organisation HQ?", ["Beijing", "Moscow", "Delhi", "Islamabad"], "Beijing", "hard"),
        qb("Asian Development Bank HQ?", ["Manila", "Tokyo", "Delhi", "Bangkok"], "Manila", "hard"),
        qb("New Development Bank (BRICS bank) HQ?", ["Shanghai", "Delhi", "Moscow", "Brasilia"], "Shanghai", "hard"),
        qb("International Atomic Energy Agency monitors?", ["Peaceful nuclear use", "Only weapons", "Only space", "Only medical"], "Peaceful nuclear use", "medium"),
    ])
    return qs


def build_philosophy() -> list[Question]:
    return [
        qb("ശങ്കരാചാര്യൻ പ്രതിപാദിച്ച ദർശനം?", ["അദ്വൈത വേദാന്തം", "വിശിഷ്ടാദ്വൈതം", "ദ്വൈതം", "ബുദ്ധമതം"], "അദ്വൈത വേദാന്തം", "easy"),
        qb("രാമാനുജர் പ്രതിപാദിച്ച ദർശനം?", ["വിശിഷ്ടാദ്വൈതം", "അദ്വൈതം", "ദ്വൈതം", "ചാരvaka"], "വിശിഷ്ടാദ്വൈതം", "medium"),
        qb("മധ്വാചാര്യൻ പ്രതിപാദിച്ച ദർശനം?", ["ദ്വൈതം", "അദ്വൈതം", "വിശിഷ്ടാദ്വൈതം", "ബുദ്ധമതം"], "ദ്വൈതം", "medium"),
        qb("ഗൗതമ ബുദ്ധൻ പ്രതിപാദിച്ച നാല് ആര്യസത്യങ്ങൾ എത്ര?", ["നാല്", "അഞ്ച്", "മൂന്ന്", "ആറ്"], "നാല്", "easy"),
        qb("ബുദ്ധമതത്തിലെ എട്ട് നേർമാർഗം അറിയപ്പെടുന്നത്?", ["അഷ്ടാംഗ മാർഗം", "നവരasa", "യോഗ", "കർമ"], "അഷ്ടാംഗ മാർഗം", "medium"),
        qb("മഹാവീരൻ പ്രതിപാദിച്ച മതം?", ["ജൈനമതം", "ബുദ്ധമതം", "സിഖ് മതം", "ഹിന്ദുമതം"], "ജൈനമതം", "medium"),
        qb("ജൈനമതത്തിലെ അഹിംസാ സിദ്ധാന്തം?", ["സകല ജീവികളോടും അഹിംസ", "ഹിംസ അനിവാര്യം", "കർമ്മം മാത്രം", "യജ്ഞം മാത്രം"], "സകല ജീവികളോടും അഹിംസ", "easy"),
        qb("പതഞ്ജലി ബന്ധപ്പെട്ട ദർശനം?", ["യോഗദർശനം", "ന്യായം", "വൈശേഷികം", "സാംഖ്യം"], "യോഗദർശനം", "medium"),
        qb("കപില മഹർഷി ബന്ധപ്പെട്ട ദർശനം?", ["സാംഖ്യം", "യോഗം", "ന്യായം", "മീമാംസ"], "സാംഖ്യം", "medium"),
        qb("ഗൗതമ (ന്യായ) ബന്ധപ്പെട്ട ദർശനം?", ["ന്യായദർശനം", "വൈശേഷികം", "വേദാന്തം", "ചാരvaka"], "ന്യായദർശനം", "hard"),
        qb("കണാദ ബന്ധപ്പെട്ട ദർശനം?", ["വൈശേഷികം", "ന്യായം", "യോഗം", "സാംഖ്യം"], "വൈശേഷികം", "hard"),
        qb("ചാരvaka ദർശനം പ്രധാനമായി?", ["ഭൗതികവാദം/സുഖവാദം", "അദ്വൈതം", "കർമ്മം", "യോഗം"], "ഭൗതികവാദം/സുഖവാദം", "hard"),
        qb("സോക്രATES-ന്റെ ശിഷ്യൻ?", ["പ്ലേറ്റോ", "അറിസ്റ്റോട്ടിൽ", "ഡemocritus", "Heraclitus"], "പ്ലേറ്റോ", "easy"),
        qb("പ്ലato-യുടെ ശിഷ്യൻ?", ["അറിസ്റ്റോട്ടിൽ", "സോക്രATES", "Socrates", "Kant"], "അറിസ്റ്റോട്ടിൽ", "easy"),
        qb("അറിസ്റ്റോട്ടil-ന്റെ teacher?", ["പ്ലato", "Socrates directly only", "Kant", "Descartes"], "പ്ലato", "medium"),
        qb("Descartes-ന്റെ പ്രശസ്ത statement?", ["Cogito ergo sum", "Forms exist", "Tabula rasa", "Will to power"], "Cogito ergo sum", "medium"),
        qb("John Locke പ്രതിപാദിച്ച ആശയം?", ["Tabula rasa / social contract", "Categorical imperative", "Will to power", "Forms"], "Tabula rasa / social contract", "hard"),
        qb("Immanuel Kant-ന്റെ ethics concept?", ["Categorical Imperative", "Utilitarianism", "Eudaimonia", "Dharma only"], "Categorical Imperative", "medium"),
        qb("Utilitarianism associated with?", ["Bentham and Mill", "Plato only", "Shankaracharya", "Buddha only"], "Bentham and Mill", "hard"),
        qb("Nietzsche concept?", ["Will to power", "Forms", "Cogito", "Tabula rasa"], "Will to power", "hard"),
        qb("Karl Marx philosophy branch?", ["Dialectical materialism", "Idealism only", "Vedanta", "Yoga"], "Dialectical materialism", "medium"),
        qb("Sartre associated with?", ["Existentialism", "Stoicism", "Vedanta", "Nyaya"], "Existentialism", "hard"),
        qb("Stoicism associated with?", ["Zeno of Citium", "Plato", "Shankara", "Buddha"], "Zeno of Citium", "hard"),
        qb("Upanishads primarily discuss?", ["Brahman and Atman", "Only rituals", "Only politics", "Only grammar"], "Brahman and Atman", "medium"),
        qb("Bhagavad Gita part of?", ["Mahabharata", "Ramayana", "Vedas", "Upanishads only"], "Mahabharata", "easy"),
        qb("Purva Mimamsa focuses on?", ["Vedic rituals/karma", "Metaphysics only", "Logic only", "Art only"], "Vedic rituals/karma", "hard"),
        qb("Uttara Mimamsa is another name for?", ["Vedanta", "Nyaya", "Yoga", "Charvaka"], "Vedanta", "medium"),
        qb("Sri Narayana Guru Kerala philosophy emphasized?", ["One caste, one religion, one god for man", "Caste hierarchy", "Colonial rule", "None"], "One caste, one religion, one god for man", "medium"),
        qb("Vaikom Satyagraha leader association with Narayana Guru ideals?", ["Social equality", "Colonial expansion", "War", "None"], "Social equality", "hard"),
        qb("Chattampi Swamikal contributed to?", ["Kerala renaissance/spiritual reform", "Colonial army", "Film", "Sports only"], "Kerala renaissance/spiritual reform", "hard"),
        qb("Vagbhatananda Kerala philosopher associated with?", ["Atmavidya Sangham", "Congress only", "Muslim League only", "None"], "Atmavidya Sangham", "hard"),
        qb("Plato's famous work?", ["Republic", "Nicomachean Ethics", "Critique of Pure Reason", "Leviathan"], "Republic", "medium"),
        qb("Aristotle's ethics work?", ["Nicomachean Ethics", "Republic", "Meditations", "Thus Spoke Zarathustra"], "Nicomachean Ethics", "hard"),
        qb("Kant's major work?", ["Critique of Pure Reason", "Republic", "Ethics", "Das Kapital"], "Critique of Pure Reason", "hard"),
        qb("Confucius origin country?", ["China", "India", "Greece", "Egypt"], "China", "easy"),
        qb("Taoism associated with?", ["Lao Tzu", "Confucius only", "Buddha", "Shankara"], "Lao Tzu", "hard"),
        qb("Zen Buddhism origin linked to?", ["Mahayana/China-Japan", "Theravada Sri Lanka only", "Greece", "Egypt"], "Mahayana/China-Japan", "hard"),
        qb("Four Noble Truths belong to?", ["Buddhism", "Jainism", "Hinduism only", "Sikhism only"], "Buddhism", "easy"),
        qb("Middle Way (Madhyamaka) associated with?", ["Nagarjuna", "Shankara", "Plato", "Kant"], "Nagarjuna", "hard"),
        qb("Advaita means?", ["Non-duality", "Dualism", "Pluralism", "Materialism"], "Non-duality", "easy"),
        qb("Dvaita means?", ["Dualism", "Non-duality", "Monism", "Nihilism"], "Dualism", "easy"),
        qb("Maya concept in Advaita refers to?", ["Illusory appearance of world", "Absolute truth only", "Physical matter only", "None"], "Illusory appearance of world", "hard"),
        qb("Moksha in Indian philosophy means?", ["Liberation", "Wealth", "Power", "Fame"], "Liberation", "easy"),
        qb("Karma theory implies?", ["Action and consequence", "No causality", "Random events only", "Predestination only"], "Action and consequence", "easy"),
        qb("Socratic method is?", ["Dialectical questioning", "Meditation only", "Ritual only", "War strategy"], "Dialectical questioning", "medium"),
        qb("Empiricism emphasizes?", ["Experience as knowledge source", "Reason only", "Revelation only", "Authority only"], "Experience as knowledge source", "medium"),
        qb("Rationalism emphasizes?", ["Reason as primary knowledge source", "Senses only", "Tradition only", "Luck"], "Reason as primary knowledge source", "medium"),
        qb("Hegel associated with?", ["Dialectical idealism", "Charvaka", "Nyaya", "Yoga"], "Dialectical idealism", "hard"),
        qb("Schopenhauer known for?", ["Philosophy of will/pessimism", "Utilitarianism", "Vedanta", "Mimamsa"], "Philosophy of will/pessimism", "hard"),
        qb("Bertrand Russell contributed to?", ["Analytic philosophy/logic", "Yoga", "Vedanta", "Mimamsa"], "Analytic philosophy/logic", "hard"),
        qb("Wittgenstein known for?", ["Language philosophy", "Yoga", "Rituals", "Caste system"], "Language philosophy", "hard"),
    ]


def build_basic_gk() -> list[Question]:
    rivers = [
        ("Ganga", "Gangotri", ["Yamunotri", "Kedarnath", "Badrinath"]),
        ("Yamuna", "Yamunotri", ["Gangotri", "Kedarnath", "Badrinath"]),
        ("Narmada", "Amarkantak", ["Himalayas", "Western Ghats only Kerala", "Deccan only"]),
        ("Tapti", "Multai", ["Gangotri", "Yamunotri", "Kedarnath"]),
        ("കാവേരി", "തലakaveri", ["Nilgiris only", "Himalaya", "Aravalli"]),
        ("ഗodavari", "ത്രyambakeshwar", ["Gangotri", "Yamunotri", "Kedarnath"]),
        ("നarmada flows mainly?", ["West to Arabian Sea", "East to Bay only", "North to Ganga", "South to Indian Ocean direct"], "West to Arabian Sea", "medium"),
    ]
    qs: list[Question] = []
    for r, o, w in rivers[:4]:
        r_m = malayalamize_text(r)
        o_m = malayalamize_text(o)
        w_m = [malayalamize_text(x) for x in w]
        qs.append(qb(f"{r_m} നദിയുടെ ഉത്ഭവസ്ഥലം?", w_m + [o_m], o_m, "medium"))
    qs.extend([
        qb("India's longest dam Hirakud on river?", ["Mahanadi", "Godavari", "Krishna", "Kaveri"], "Mahanadi", "hard"),
        qb("Bhakra Nangal dam on river?", ["Sutlej", "Ganga", "Yamuna", "Narmada"], "Sutlej", "hard"),
        qb("Tehri dam on river?", ["Bhagirathi", "Yamuna", "Ganga main", "Narmada"], "Bhagirathi", "hard"),
        qb("Sardar Sarovar dam on river?", ["Narmada", "Tapi", "Mahi", "Sabarmati"], "Narmada", "medium"),
        qb("Idukki arch dam on river?", ["Periyar", "Bharathapuzha", "Pamba", "Chaliyar"], "Periyar", "medium"),
        qb("Mullaperiyar dam primarily on river?", ["Periyar", "Pamba", "Chaliyar", "Meenachil"], "Periyar", "medium"),
        qb("World's highest rail bridge Chenab on?", ["Chenab river", "Ganga", "Yamuna", "Narmada"], "Chenab river", "hard"),
        qb("India's smallest state by area?", ["Goa", "Sikkim", "Tripura", "Nagaland"], "Goa", "easy"),
        qb("India's largest state by area?", ["Rajasthan", "Madhya Pradesh", "Maharashtra", "Uttar Pradesh"], "Rajasthan", "easy"),
        qb("India's most populous state?", ["Uttar Pradesh", "Maharashtra", "Bihar", "West Bengal"], "Uttar Pradesh", "medium"),
        qb("Kerala formed as state on?", ["1956 November 1", "1947 August 15", "1950 January 26", "1960"], "1956 November 1", "easy"),
        qb("First President of India?", ["Rajendra Prasad", "Nehru", "Patel", "Azad"], "Rajendra Prasad", "easy"),
        qb("First woman Governor of an Indian state?", ["Sarojini Naidu (UP)", "Indira Gandhi", "Pratibha Patil", "Mother Teresa"], "Sarojini Naidu (UP)", "hard"),
        qb("First Indian in space?", ["Rakesh Sharma", "Kalpana Chawla", "Gaganyaan crew", "Nehru"], "Rakesh Sharma", "medium"),
        qb("First Indian woman in space?", ["Kalpana Chawla (NASA)", "Sunita Williams only Indian-born?", "None Indian citizen yet", "Indira Gandhi"], "Kalpana Chawla (NASA)", "hard"),
        qb("Longest river in India (within India length)?", ["Ganga", "Godavari", "Yamuna", "Narmada"], "Ganga", "medium"),
        qb("Longest river in Kerala?", ["Periyar", "Bharathapuzha", "Pamba", "Chaliyar"], "Periyar", "medium"),
        qb("Highest peak in India (disputed K2 excluded)?", ["Kanchenjunga", "Nanda Devi", "K2", "Mount Everest in India"], "Kanchenjunga", "hard"),
        qb("Highest peak in Kerala?", ["Anamudi", "Agasthyarkoodam", "Meesapulimala", "Chembra"], "Anamudi", "easy"),
        qb("Capital of Australia?", ["Canberra", "Sydney", "Melbourne", "Perth"], "Canberra", "easy"),
        qb("Capital of Canada?", ["Ottawa", "Toronto", "Vancouver", "Montreal"], "Ottawa", "medium"),
        qb("Capital of Brazil?", ["Brasilia", "Rio de Janeiro", "Sao Paulo", "Salvador"], "Brasilia", "medium"),
        qb("Capital of Japan?", ["Tokyo", "Kyoto", "Osaka", "Hiroshima"], "Tokyo", "easy"),
        qb("Capital of Germany?", ["Berlin", "Munich", "Frankfurt", "Hamburg"], "Berlin", "easy"),
        qb("Capital of France?", ["Paris", "Lyon", "Marseille", "Nice"], "Paris", "easy"),
        qb("Capital of Russia?", ["Moscow", "St Petersburg", "Kazan", "Sochi"], "Moscow", "easy"),
        qb("Capital of China?", ["Beijing", "Shanghai", "Hong Kong", "Guangzhou"], "Beijing", "easy"),
        qb("Capital of South Africa (legislative)?", ["Cape Town", "Pretoria only", "Johannesburg", "Durban"], "Cape Town", "hard"),
        qb("Capital of Sri Lanka?", ["Sri Jayawardenepura Kotte", "Colombo commercial", "Kandy", "Galle"], "Sri Jayawardenepura Kotte", "hard"),
        qb("Capital of Maldives?", ["Male", "Addu", "Fuvahmulah", "Colombo"], "Male", "easy"),
        qb("Capital of Nepal?", ["Kathmandu", "Pokhara", "Lalitpur", "Delhi"], "Kathmandu", "easy"),
        qb("Capital of Bhutan?", ["Thimphu", "Paro", "Punakha", "Kathmandu"], "Thimphu", "medium"),
        qb("Capital of Bangladesh?", ["Dhaka", "Chittagong", "Khulna", "Kolkata"], "Dhaka", "easy"),
        qb("Capital of Pakistan?", ["Islamabad", "Karachi", "Lahore", "Rawalpindi"], "Islamabad", "medium"),
        qb("Capital of Afghanistan?", ["Kabul", "Kandahar", "Herat", "Islamabad"], "Kabul", "medium"),
        qb("Capital of Myanmar?", ["Naypyidaw", "Yangon", "Mandalay", "Bangkok"], "Naypyidaw", "hard"),
        qb("Capital of Thailand?", ["Bangkok", "Chiang Mai", "Phuket", "Hanoi"], "Bangkok", "easy"),
        qb("Capital of Vietnam?", ["Hanoi", "Ho Chi Minh City", "Da Nang", "Bangkok"], "Hanoi", "medium"),
        qb("Capital of Malaysia?", ["Kuala Lumpur", "Putrajaya admin", "Penang", "Jakarta"], "Kuala Lumpur", "medium"),
        qb("Capital of Indonesia?", ["Jakarta", "Bali", "Surabaya", "Bangkok"], "Jakarta", "easy"),
        qb("Capital of Singapore?", ["Singapore", "Malaysia", "Bangkok", "Jakarta"], "Singapore", "easy"),
        qb("Capital of UAE?", ["Abu Dhabi", "Dubai", "Sharjah", "Doha"], "Abu Dhabi", "medium"),
        qb("Capital of Saudi Arabia?", ["Riyadh", "Jeddah", "Mecca", "Dubai"], "Riyadh", "medium"),
        qb("Capital of Iran?", ["Tehran", "Isfahan", "Shiraz", "Baghdad"], "Tehran", "medium"),
        qb("Capital of Iraq?", ["Baghdad", "Basra", "Mosul", "Tehran"], "Baghdad", "medium"),
        qb("Capital of Israel?", ["Jerusalem", "Tel Aviv", "Haifa", "Cairo"], "Jerusalem", "hard"),
        qb("Capital of Egypt?", ["Cairo", "Alexandria", "Giza", "Riyadh"], "Cairo", "easy"),
        qb("Capital of Kenya?", ["Nairobi", "Mombasa", "Kisumu", "Addis Ababa"], "Nairobi", "hard"),
        qb("Capital of Nigeria?", ["Abuja", "Lagos", "Kano", "Accra"], "Abuja", "hard"),
        qb("Capital of South Korea?", ["Seoul", "Busan", "Incheon", "Tokyo"], "Seoul", "easy"),
        qb("Capital of North Korea?", ["Pyongyang", "Seoul", "Busan", "Tokyo"], "Pyongyang", "hard"),
        qb("Capital of Italy?", ["Rome", "Milan", "Venice", "Florence"], "Rome", "easy"),
        qb("Capital of Spain?", ["Madrid", "Barcelona", "Seville", "Lisbon"], "Madrid", "easy"),
        qb("Capital of Portugal?", ["Lisbon", "Porto", "Madrid", "Paris"], "Lisbon", "medium"),
        qb("Capital of Switzerland?", ["Bern", "Zurich", "Geneva", "Vienna"], "Bern", "hard"),
        qb("Capital of Austria?", ["Vienna", "Salzburg", "Bern", "Prague"], "Vienna", "medium"),
        qb("Capital of Poland?", ["Warsaw", "Krakow", "Prague", "Budapest"], "Warsaw", "hard"),
        qb("Capital of Sweden?", ["Stockholm", "Oslo", "Copenhagen", "Helsinki"], "Stockholm", "medium"),
        qb("Capital of Norway?", ["Oslo", "Stockholm", "Copenhagen", "Helsinki"], "Oslo", "medium"),
        qb("Capital of Denmark?", ["Copenhagen", "Oslo", "Stockholm", "Helsinki"], "Copenhagen", "medium"),
        qb("Capital of Finland?", ["Helsinki", "Oslo", "Stockholm", "Tallinn"], "Helsinki", "medium"),
        qb("Capital of Greece?", ["Athens", "Thessaloniki", "Rome", "Istanbul"], "Athens", "easy"),
        qb("Capital of Turkey?", ["Ankara", "Istanbul", "Izmir", "Athens"], "Ankara", "medium"),
        qb("Capital of New Zealand?", ["Wellington", "Auckland", "Christchurch", "Sydney"], "Wellington", "hard"),
        qb("Capital of Argentina?", ["Buenos Aires", "Brasilia", "Santiago", "Lima"], "Buenos Aires", "medium"),
        qb("Capital of Mexico?", ["Mexico City", "Guadalajara", "Cancun", "Havana"], "Mexico City", "medium"),
    ])
    return qs


def build_politics_kerala() -> list[Question]:
    return [
        qb("കേരളത്തിലെ ആദ്യ elected CPI ministry 1957 led by?", ["E.M.S. Namboodiripad", "Achutha Menon", "K. Karunakaran", "A.K. Antony"], "E.M.S. Namboodiripad", "easy"),
        qb("Vimochana Samaram (1959) resulted in?", ["Dismissal of first EMS ministry", "Formation of Kerala", "President's rule forever", "None"], "Dismissal of first EMS ministry", "hard"),
        qb("Kerala's second EMS ministry year?", ["1967", "1957", "1980", "1996"], "1967", "hard"),
        qb("K. Karunakaran first became CM in?", ["1977", "1980", "1991", "1967"], "1977", "hard"),
        qb("A.K. Antony first became CM in?", ["1977", "1980", "1995", "2001"], "1977", "hard"),
        qb("C. Achutha Menon ministry known for?", ["Land reforms implementation", "Only cinema", "Only sports", "Only space"], "Land reforms implementation", "hard"),
        qb("Kerala Pradesh Congress Committee president 2024 approx?", ["K. Sudhakaran", "Pinarayi Vijayan", "V.D. Satheesan", "Oommen Chandy"], "K. Sudhakaran", "hard"),
        qb("Kerala Opposition Leader (UDF) 2024?", ["V.D. Satheesan", "Pinarayi Vijayan", "M.B. Rajesh", "K. Sudhakaran"], "V.D. Satheesan", "medium"),
        qb("Kerala Assembly Speaker 2024?", ["A.N. Shamseer", "M.B. Rajesh", "Thiruvanchoor Radhakrishnan", "Pinarayi Vijayan"], "A.N. Shamseer", "medium"),
        qb("Kerala Governor 2024?", ["Arif Mohammed Khan", "P. Sathasivam", "R.L. Bhatia", "Sikander Bakht"], "Arif Mohammed Khan", "medium"),
        qb("BJP first MLA in Kerala Assembly elected from?", ["Kazhakkoottam (O. Rajagopal 2016)", "Thiruvananthapuram", "Kasaragod", "Pathanamthitta"], "Kazhakkoottam (O. Rajagopal 2016)", "hard"),
        qb("Indian Union Muslim League stronghold district traditionally?", ["Malappuram", "Wayanad only", "Idukki only", "Kasaragod only"], "Malappuram", "medium"),
        qb("Kerala Congress (M) founder?", ["K.M. Mani", "K. Karunakaran", "Oommen Chandy", "A.K. Antony"], "K.M. Mani", "hard"),
        qb("Kerala Congress (Joseph faction) leader?", ["P.J. Joseph", "K.M. Mani", "Mani C. Kappan", "Ramesh Chennithala"], "P.J. Joseph", "hard"),
        qb("CPM Kerala state secretary 2024?", ["M.V. Govindan", "Pinarayi Vijayan", "Kodiyeri Balakrishnan", "E.K. Nayanar"], "M.V. Govindan", "hard"),
        qb("CPI Kerala state secretary (approx recent)?", ["P. Panneerselvam", "Pinarayi Vijayan", "Achuthanandan", "Namboodiripad"], "P. Panneerselvam", "hard"),
        qb("RSP in Kerala allied mainly with?", ["LDF historically often", "BJP always", "NDA always", "None"], "LDF historically often", "hard"),
        qb("Janata Dal(S) in Kerala linked to?", ["Vishwanathan / smaller fronts", "Congress only", "BJP only", "None"], "Vishwanathan / smaller fronts", "hard"),
        qb("BDJS party in Kerala associated with?", ["NDA alliance", "LDF only", "UDF only", "None"], "NDA alliance", "hard"),
        qb("Twenty20th Keralam party strong in?", ["Kizhakkambalam (Sabari Dasan)", "Kasaragod only", "Wayanad only", "None"], "Kizhakkambalam (Sabari Dasan)", "hard"),
        qb("Kerala local self-government three-tier includes?", ["Grama Panchayat, Block, District", "Only Parliament", "Only Rajya Sabha", "Only Governor"], "Grama Panchayat, Block, District", "medium"),
        qb("Kerala Panchayat Raj Act enacted?", ["1994", "1956", "2010", "1980"], "1994", "hard"),
        qb("First Kerala Legislative Assembly election year?", ["1957", "1956", "1960", "1950"], "1957", "hard"),
        qb("Kerala has how many Lok Sabha seats?", ["20", "14", "140", "9"], "20", "easy"),
        qb("Kerala has how many Rajya Sabha seats?", ["9", "20", "140", "5"], "9", "easy"),
        qb("Kerala Assembly seats?", ["140", "20", "9", "100"], "140", "easy"),
        qb("Malappuram district Lok Sabha seats count?", ["2", "1", "3", "4"], "2", "hard"),
        qb("Thiruvananthapuram Lok Sabha constituency MP 2019 winner?", ["Shashi Tharoor", "Pinarayi Vijayan", "Oommen Chandy", "K. Sudhakaran"], "Shashi Tharoor", "medium"),
        qb("Wayanad LS constituency notable MP?", ["Rahul Gandhi (2019)", "Modi", "Shashi Tharoor", "Mani"], "Rahul Gandhi (2019)", "medium"),
        qb("Kerala women's reservation in local bodies approx?", ["50%", "33%", "25%", "10%"], "50%", "hard"),
        qb("Kerala first coalition government?", ["1957 CPI-led", "1947", "2010", "1990 only UDF"], "1957 CPI-led", "hard"),
        qb("UDF acronym stands for?", ["United Democratic Front", "Unified Development Force", "Union Democratic Forum", "United Defence Front"], "United Democratic Front", "easy"),
        qb("LDF acronym stands for?", ["Left Democratic Front", "Liberal Democratic Front", "Local Development Front", "Left Defence Front"], "Left Democratic Front", "easy"),
        qb("NDA in Kerala includes?", ["BJP and allies like BDJS", "CPM only", "Congress only", "IUML only"], "BJP and allies like BDJS", "medium"),
        qb("Kerala Legislative Assembly term length?", ["5 വർഷം", "4 വർഷം", "6 years", "3 വർഷം"], "5 വർഷം", "easy"),
        qb("Minimum age to vote in India?", ["18", "21", "25", "16"], "18", "easy"),
        qb("Minimum age to become MLA in Kerala?", ["25", "18", "21", "30"], "25", "medium"),
        qb("Kerala High Court bench cities include?", ["Kochi, Thiruvananthapuram, Kozhikode", "Mumbai only", "Delhi only", "Chennai only"], "Kochi, Thiruvananthapuram, Kozhikode", "hard"),
    ]


def build_kerala_districts() -> list[Question]:
    kadalundi = "കാദലുന്ദി പുഴ"
    dist = [
        ("കാസർഗോഡ്", "കാസർഗോഡ്", "ബേവളി", "തെയ്യം"),
        ("കണ്ണൂർ", "കണ്ണൂർ", "വളപട്ടണം പുഴ", "തെയ്യം"),
        ("വയനാട്", "കൽപ്പറ്റ", "കബനി", "തെയ്യം/നേമമ"),
        ("കോഴിക്കോട്", "കോഴിക്കോട്", "ചാലിയാർ", "തിരുവാതിര"),
        ("മലപ്പുറം", "മലപ്പുറം", kadalundi, "പൂരം"),
        ("പാലക്കാട്", "പാലക്കാട്", "ഭാരതപ്പുഴ", "തൃശ്ശിവിലാമല പൂരം"),
        ("തൃശ്ശൂർ", "തൃശ്ശൂർ", "ചാലക്കുടിയാർ", "തൃശ്ശൂർ പൂരം"),
        ("ഇടുക്കി", "പൈനാവ്", "പെരിയാർ", "അറ്റുക്കൽ പൊങ്കല"),
        ("എറണാകുളം", "കാക്കനാട്", "പെരിയാർ", "ആലുവ ശിവരാത്രി"),
        ("ആലപ്പുഴ", "ആലപ്പുഴ", "പമ്പയാർ", "നെഹ്റു ട്രോഫി വള്ളംകളി"),
        ("കോട്ടയം", "കോട്ടയം", "മീനച്ചിലാർ", "അറ്റുക്കൽ പൊങ്കല"),
        ("പത്തനംതിട്ട", "പത്തനംതിട്ട", "പമ്പയാർ", "ശബരിമല തീർത്ഥാടന കാലം"),
        ("കൊല്ലം", "കൊല്ലം", "അഷ്ടമുടി കായൽ", "കൊല്ലം പൂരം"),
        ("തിരുവനന്തപുരം", "തിരുവനന്തപുരം", "കരമനയാർ", "അറ്റുക്കൽ പൊങ്കല"),
    ]
    qs: list[Question] = []
    for name, hq, river, fest in dist:
        qs.append(qb(f"{name} ജില്ലയുടെ ആസ്ഥാനം ഏത്?", [hq, "കൊച്ചി", "കോഴിക്കോട്", "തൃശ്ശൂർ"], hq, "medium"))
        qs.append(qb(f"{name} ജില്ലയിലെ പ്രധാന നദി/ജലാശയം?", [river, "ഗംഗ", "യമുന", "നർമ്മദ"], river, "hard"))
        qs.append(qb(f"{name} ജില്ലയുമായി ബന്ധപ്പെട്ട ഉത്സവം/സംഭവം?", [fest, "ദീപാവലി മാത്രം", "ഹോളി മാത്രം", "ഒന്നുമില്ല"], fest, "hard"))
    qs.extend([
        qb('കേരള-യിൽ വിസ്തീർണ്ണത്തിൽ ഏറ്റവും വലിയ ജില്ല?', ['ഇടുക്കി', 'പാലക്കാട്', 'കാസർഗോഡ്', 'തിരുവനന്തപുരം'], 'പാലക്കാട്', 'hard'),
        qb('കേരള-യിൽ വിസ്തീർണ്ണത്തിൽ ഏറ്റവും ചെറിയ ജില്ല?', ['ആലപ്പുഴ', 'കാസർഗോഡ്', 'പാലക്കാട്', 'ഇടുക്കി'], 'ആലപ്പുഴ', 'hard'),
        qb('കേരള-യിൽ ജനസംഖ്യയിൽ ഏറ്റവും മുന്നിൽ?', ['കോഴിക്കോട്', 'മലപ്പുറം', 'എറണാകുളം', 'തിരുവനന്തപുരം'], 'മലപ്പുറം', 'medium'),
        qb('വയനാട് ജില്ലയിലെ പ്രധാന വന്യജീവി അഭയാര്ഥനം ഏത്?', ['ഒന്നുമില്ല', 'സൈലന്റ് വാലി', 'പെരിയാർ', 'മുത്തങ്ങ'], 'മുത്തങ്ങ', 'hard'),
        qb('ഇടുക്കി ജില്ലയിലെ പ്രശിദ്ധ അണക്കെട്ട് ഏത്?', ['നെയ്യാർ ഡാം', 'ബാനാസുര സാഗർ', 'മലമ്പുഴ അണക്കെട്ട്', 'ഇടുക്കി അണക്കെട്ട്'], 'ഇടുക്കി അണക്കെട്ട്', 'medium'),
    ])
    return qs


def build_current_affairs() -> list[Question]:
    return [
        qb("2026 ജൂണിൽ കേരള സർക്കാർ പ്രഖ്യാപിച്ച 'ഹരിത കേരളം' പദ്ധതിയുടെ പ്രധാന ലക്ഷ്യം എന്ത്?", ["ചലച്ചിത്ര നിർമ്മാണം", "സംരക്ഷണ പ്രവർത്തനം", "നഗരങ്ങളിൽ വൃക്ഷത്തൈകൾ നട്ടുപിടിപ്പിക്കൽ", "ആണവ ഗവേഷണം"], "നഗരങ്ങളിൽ വൃക്ഷത്തൈകൾ നട്ടുപിടിപ്പിക്കൽ", "medium"),
        qb("2026 ജൂണിൽ ISRO-യുടെ വാണിജ്യ ശാഖ IN-SPACe-ന്റെ പ്രധാന ലക്ഷ്യം എന്ത്?", ["NASA-യുമായി ലയിപ്പിക്കൽ", "സ്വകാര്യ ബഹിരാകാശ മേഖലയെ സഹായിക്കൽ", "ചലച്ചിത്ര ഉത്സവം", "കരിമ്പ് കയറ്റുമതി"], "സ്വകാര്യ ബഹിരാകാശ മേഖലയെ സഹായിക്കൽ", "hard"),
        qb("2026 ജൂണിൽ കേരള ബജറ്റ് സെഷൻ നടന്ന സ്ഥലം ഏത്?", ["കൊച്ചി", "തിരുവനന്തപുരം നിയമസഭ", "ന്യൂഡൽഹി", "മുംബൈ"], "തിരുവനന്തപുരം നിയമസഭ", "easy"),
        qb("2026 ജൂണിൽ GST Council യോഗത്തിന്റെ പ്രധാന ചർച്ചാവിഷയം എന്ത്?", ["ചലച്ചിത്ര പുരസ്കാരം", "നിരക്ക് പരിഷ്ക്കരണവും അനുസരണവും", "ആണവ പരീക്ഷണം", "ബഹിരാകാശ ദൗത്യം"], "നിരക്ക് പരിഷ്ക്കരണവും അനുസരണവും", "hard"),
        qb("2026 ജൂണിൽ കേരളത്തിലെ മഴക്കാലം ആരംഭം പ്രഖ്യാപിക്കുന്ന സ്ഥാപനം ഏത്?", ["ECI", "IMD", "ISRO", "DRDO"], "IMD", "medium"),
        qb("2026 ജൂൺ അവധിക്ക് ശേഷം കേരളത്തിലെ വിദ്യാലയങ്ങൾ വീണ്ടും തുറക്കുന്നത് സാധാരണയായി എപ്പോൾ?", ["ഡിസംബർ", "ജൂൺ ആദ്യ ആഴ്ച", "മാർച്ച് മാത്രം", "ജനുവരി"], "ജൂൺ ആദ്യ ആഴ്ച", "medium"),
        qb("2026 ജൂണിൽ FIFA Club World Cup-ന്റെ ആതിഥ്യ രാജ്യം ഏത്?", ["ഖത്തർ", "ഇന്ത്യ", "ബ്രാസീൽ", "യുഎസ്എ"], "യുഎസ്എ", "hard"),
        qb("പാരീസ് കാലാവസ്ഥാ ഉടമ്പടിയുടെ ആഗോള വിലയിരുത്തൽ തുടരുന്ന UN സംഘടന ഏത്?", ["IMF", "UNFCCC", "WHO", "WTO"], "UNFCCC", "hard"),
        qb("2026 ജൂണിൽ കേരള Responsible Tourism Mission-ന്റെ പ്രധാന ലക്ഷ്യം എന്ത്?", ["പരിസ്ഥിതി സൗഹൃദ ടൂറിസം", "കൽക്കരി ഖനനം", "ചലച്ചിത്രം മാത്രം", "പ്രതിരോധം"], "പരിസ്ഥിതി സൗഹൃദ ടൂറിസം", "medium"),
        qb("2026 ജൂണിൽ ഇന്ത്യയുടെ UPI അന്താരാഷ്ട്ര വിപുലീകരണ പങ്കാളി പ്രദേശം ഏത്?", ["അന്റാർട്ടിക്ക", "മദ്ധ്യേഷ്യ/ഏഷ്യ", "ചന്ദ്രന", "ഒന്നുമില്ല"], "മദ്ധ്യേഷ്യ/ഏഷ്യ", "hard"),
        qb("KFON (Kerala Fibre Optic Network) പദ്ധതിയുടെ ലക്ഷ്യം എന്ത്?", ["പ്രതിരോധം മാത്രം", "കൽക്കരി കയിക്കയം", "ചലച്ചിത്രം മാത്രം", "എല്ലാവർക്കും ഇന്റർനെറ്റ് കണക്റ്റിവിറ്റി"], "എല്ലാവർക്കും ഇന്റർനെറ്റ് കണക്റ്റിവിറ്റി", "medium"),
        qb("NEP നടപ്പാക്കൽ പരിശോധന നടത്തുന്നത് ആര്?", ["കേന്ദ്രവും സംസ്ഥാനങ്ങളും", "കേരളം മാത്രം", "സ്വകാര്യ സ്കൂളുകൾ മാത്രം", "ഒന്നുമില്ല"], "കേന്ദ്രവും സംസ്ഥാനങ്ങളും", "hard"),
        qb("2026 ജൂണിൽ കേരള ആനക്കൂട്ടം എണ്ണം നടത്തുന്ന വകുപ്പ് ഏത്?", ["തുറമുഖ അധികൃതർ", "വന വകുപ്പ്", "പോലീസ് മാത്രം", "ചലച്ചിത്ര ബോർഡ്"], "വന വകുപ്പ്", "hard"),
        qb("India-Middle East-Europe Economic Corridor (IMEC) ചർച്ച ചെയ്ത ഫോറം ഏത്?", ["സ്കൂൾ PTA", "G20 ബന്ധപ്പെട്ട ഫോറങ്ങൾ", "ഒന്നുമില്ല", "പഞ്ചായത്ത്"], "G20 ബന്ധപ്പെട്ട ഫോറങ്ങൾ", "hard"),
        qb("Kerala Startup Mission-ന്റെ പ്രധാന പരിപാടി ഏത്?", ["Huddle Global/IGS", "ഓസ്കാർ അവാർഡുകൾ", "വിംബിൾഡൺ", "ഒന്നുമില്ല"], "Huddle Global/IGS", "hard"),
        qb("ECI സംസ്ഥാന തിരഞ്ഞെടുപ്പ് കാലക്രമം തയ്യാറാക്കുന്നത് എങ്ങനെ?", ["പഞ്ചായത്ത് ഒരിക്കലും", "കലണ്ടർ പ്രകാരം വിവിധ സംസ്ഥാനങ്ങൾ", "ഒന്നുമില്ല", "കേരളം എപ്പോഴും ജൂണിൽ"], "കലണ്ടർ പ്രകാരം വിവിധ സംസ്ഥാനങ്ങൾ", "hard"),
        qb("2026 ജൂണിൽ കേരള തീരദേശ കരിമ്പ് നിയന്ത്രണം നടത്തുന്നത് ആര്?", ["DRDO", "PWDയും തീരദേശ അധികൃതരും", "ചലച്ചിത്ര ബോർഡ്", "ISRO മാത്രം"], "PWDയും തീരദേശ അധികൃതരും", "hard"),
        qb("National Green Tribunal-ന്റെ കേസുകൾ പ്രധാനമായും എന്തിനെ സംബന്ധിച്ച്?", ["ചലച്ചിത്ര പുരസ്കാരം", "ഒന്നുമില്ല", "കായികം", "പരിസ്ഥിതി ലംഘനങ്ങൾ"], "പരിസ്ഥിതി ലംഘനങ്ങൾ", "medium"),
        qb("India semiconductor mission fabs-ന്റെ പുരോഗതി എവിടെ?", ["കേരളം മാത്രം", "ഒന്നുമില്ല", "ഗുജറാത്ത്/ഇന്ത്യൻ സൈറ്റുകൾ", "അന്റാർട്ടിക്ക"], "ഗുജറാത്ത്/ഇന്ത്യൻ സൈറ്റുകൾ", "hard"),
        qb("2026 ജൂണിൽ കേരള കൃഷി വകുപ്പ് മഴക്കാല വിള തയ്യാറെടുപ്പ് എന്തിനാണ്?", ["ശീതകാല കായികം", "മഴക്കാല വിള തയ്യാറെടുപ്പ്", "ഒന്നുമില്ല", "ചലച്ചിത്രോത്സവം"], "മഴക്കാല വിള തയ്യാറെടുപ്പ്", "medium"),
        qb("Ayushman Bharat coverage expansion എന്തുമായി ബന്ധപ്പെട്ടതാണ്?", ["ആരോഗ്യ ഇൻഷുറൻസ് ലാഭാർഥികൾ", "റോഡുകൾ", "ചലച്ചിത്രം", "പ്രതിരോധം"], "ആരോഗ്യ ഇൻഷുറൻസ് ലാഭാർഥികൾ", "medium"),
        qb("Kerala Police Cyber Dome-ന്റെ പ്രധാന ലക്ഷ്യം എന്ത്?", ["കൽക്കരി ഖനനം", "ചലച്ചിത്രം", "ആനക്കൂട്ടം എണ്ണം", "സൈബർ ക്രൈം തടയൽ"], "സൈബർ ക്രൈം തടയൽ", "hard"),
        qb("ഇന്ത്യയുടെ നവീകരണ ഊർജ്ജ സ്ഥാപിത ശേഷിയുടെ ആഗോള റാങ്ക്?", ["100-ാം മാത്രം", "അവസാനം", "മുൻനിരയിലെ 4-ാം", "പട്ടികയിൽ ഇല്ല"], "മുൻനിരയിലെ 4-ാം", "hard"),
        qb("Kochi Metro-യുടെ വിപുലീകരണ വാർത്തകൾ പ്രധാനമായും എന്തിനെ സംബന്ധിച്ച്?", ["ദില്ലി മെട്രോ", "ഒന്നുമില്ല", "ലണ്ടൻ ട്യൂബ്", "ആലുവ-തൃപ്പൂണിത്തുറ കോറിഡോർ ഘട്ടങ്ങൾ"], "ആലുവ-തൃപ്പൂണിത്തുറ കോറിഡോർ ഘട്ടങ്ങൾ", "hard"),
        qb("കേരള സ്ത്രീകൾക്കുള്ള കായിക ലീഗ് പദ്ധതി?", ["ഒന്നുമില്ല", "ഗോൽഫ് മാത്രം", "ഫുട്ബോൾ/ക്രിക്കറ്റ് ലീഗുകൾ", "വിദേശത്ത് ചെസ് മാത്രം"], "ഫുട്ബോൾ/ക്രിക്കറ്റ് ലീഗുകൾ", "hard"),
    ]


def build_malayalam() -> list[Question]:
    return [
        qb('മലയാള അക്ഷരമാലയിലെ സ്വരങ്ങളുടെ എണ്ണം (പാരമ്പര്യം)?', ['15', '12', '20', '8'], '15', 'medium'),
        qb("'അക്ഷരമാല' എന്നതിന്റെ അർത്ഥം?", ['അക്ഷരമാല/വർണമാല', 'വാക്യം', 'വ്യാകരണ പുസ്തകം മാത്രം', 'നിഘണ്ടു മാത്രം'], 'അക്ഷരമാല/വർണമാല', 'easy'),
        qb('മലയാളം ഏത് ഭാഷാ കുടുംബത്തിലാണ് പെടുന്നത്?', ['Dravidian', 'Indo-Aryan', 'Sino-Tibetan', 'Austronesian'], 'Dravidian', 'easy'),
        qb('തുഞ്ചത്ത് എഴുത്തച്ഛന്റെ ബിരുദം?', ['മലയാള ഭാഷയുടെ പിതാവ്', 'ആദ്യ മുഖ്യമന്ത്രി', 'ആദ്യ ഗവർണർ', 'ആദ്യ പ്രധാനമന്ത്രി'], 'മലയാള ഭാഷയുടെ പിതാവ്', 'easy'),
        qb('അദ്ധ്യാത്മരാമായണം രചയിതാവ്?', ['Thunchath Ezhuthachan', 'Kumaranasan', 'Ulloor', 'Vallathol'], 'Thunchath Ezhuthachan', 'easy'),
        qb('കിലിപ്പാട്ട് സാഹിത്യ രൂപത്തിന്റെ അർത്ഥം?', ['തത്തയുടെ പാട്ട്/ആഖ്യാന കവിത', 'നോവൽ', 'നാടകം മാത്രം', 'അക്ഷരം'], 'തത്തയുടെ പാട്ട്/ആഖ്യാന കവിത', 'medium'),
        qb('മണിപ്രവാളം സംയോജിപ്പിക്കുന്നത്?', ['Malayalam and Sanskrit', 'English and Hindi', 'Tamil and Telugu only', 'അറബി മാത്രം'], 'Malayalam and Sanskrit', 'medium'),
        qb('കേരള പാണിനി എന്തിനെ സൂചിപ്പിക്കുന്നു?', ['Kerala Varma Valiya Koil Thampuran', 'Ezhuthachan', 'Kumaranasan', 'MT Vasudevan Nair'], 'Kerala Varma Valiya Koil Thampuran', 'hard'),
        qb('ഭാഷാ സംസ്ഥാനമായ കേരളം പ്രധാനമായും ആർക്ക് വേണ്ടി രൂപീകരിച്ചത്?', ['മലയാളം സംസാരിക്കുന്നവർ', 'തമിഴ് മാത്രം', 'കന്നഡ മാത്രം', 'ഇംഗ്ലീഷ് മാത്രം'], 'മലയാളം സംസാരിക്കുന്നവർ', 'easy'),
        qb('മലയാള ലിപി എവിടെ നിന്ന് ഉത്ഭവിച്ചത്?', ['ഗ്രന്ഥ/ദക്ഷിണ ബ്രാഹ്മി പാരമ്പര്യം', 'Arabic', 'Latin', 'Cyrillic'], 'ഗ്രന്ഥ/ദക്ഷിണ ബ്രാഹ്മി പാരമ്പര്യം', 'hard'),
        qb('മലയാള വ്യാകരണത്തിലെ സന്ധി എന്താണ്?', ['ശബ്ദ/പദ ചേർക്കൽ നിയമങ്ങൾ', 'കവിത മാത്രം', 'നാടകം മാത്രം', 'നോവൽ മാത്രം'], 'ശബ്ദ/പദ ചേർക്കൽ നിയമങ്ങൾ', 'hard'),
        qb('മലയാളത്തിലെ സമാസം എന്താണ്?', ['സമാസ പദ നിർമ്മാണം', 'ക്രിയ മാത്രം', 'Letter only', 'വിരാമചിഹ്നം മാത്രം'], 'സമാസ പദ നിർമ്മാണം', 'hard'),
        qb('സാഹിത്യത്തിലെ അലങ്കാരം എന്താണ്?', ['അലങ്കാരങ്ങൾ', 'വ്യാകരണം മാത്രം', 'നിഘണ്ടു', 'മുദ്രണം'], 'അലങ്കാരങ്ങൾ', 'medium'),
        qb('മലയാള കവിതയിലെ വൃത്തം എന്താണ്?', ['ചന്ദസ്', 'നോവൽ വിഭാഗം', 'അക്ഷരം', 'ഗദ്യം മാത്രം'], 'ചന്ദസ്', 'medium'),
        qb('മലയാളത്തിലെ അക്ഷരത്തിന്റെ അർത്ഥം?', ['അക്ഷര/അക്ഷര യൂണിറ്റ്', 'പദം മാത്രം', 'Sentence only', 'പുസ്തകം'], 'അക്ഷര/അക്ഷര യൂണിറ്റ്', 'easy'),
        qb('പ്രതിപദത്തിന്റെ അർത്ഥം?', ['നാമം/വിഷയ പദം', 'Verb', 'വിശേഷണം മാത്രം', 'ക്രിയാവിശേഷണം മാത്രം'], 'നാമം/വിഷയ പദം', 'medium'),
        qb('മലയാള വ്യാകരണത്തിലെ ക്രിയ?', ['Verb', 'Noun', 'Adjective', 'Conjunction'], 'Verb', 'easy'),
        qb('വിശേഷണത്തിന്റെ അർത്ഥം?', ['Adjective', 'Verb', 'Noun', 'Adverb'], 'Adjective', 'easy'),
        qb('അവ്യയത്തിന്റെ അർത്ഥം?', ['അവ്യയം', 'Verb', 'Noun', 'Adjective'], 'അവ്യയം', 'hard'),
        qb('ഛന്ദസ്ശാസ്ത്ര പഠനം എന്താണ്?', ['Prosody/metre', 'നോവൽ എഴുത്ത്', 'മുദ്രണം', 'നടനം'], 'Prosody/metre', 'hard'),
        qb('പഴയ മലയാള കാലഘട്ടം (ഏകദേശം)?', ['9-13 നൂറ്റാണ്ട് (ക്രി.ശ.)', '1-ാം നൂറ്റാണ്ട് (ക്രി.പൂ.) മാത്രം', '20-ാം നൂറ്റാണ്ട് മാത്രം', 'ഭാവി'], '9-13 നൂറ്റാണ്ട് (ക്രി.ശ.)', 'hard'),
        qb('മധ്യ മലയാള കാലഘട്ടം (ഏകദേശം)?', ['13-15 നൂറ്റാണ്ട് (ക്രി.ശ.)', '9-ാം നൂറ്റാണ്ട് (ക്രി.പൂ.)', '21-ാം നൂറ്റാണ്ട് മാത്രം', 'ഒന്നുമില്ല'], '13-15 നൂറ്റാണ്ട് (ക്രി.ശ.)', 'hard'),
        qb('ആധുനിക മലയാള കാലഘട്ടം ഏതിൽ നിന്ന് (ഏകദേശം)?', ['16-ാം നൂറ്റാണ്ട് മുതൽ', '1-ാം നൂറ്റാണ്ട് (ക്രി.ശ.)', '30-ാം നൂറ്റാണ്ട്', 'ഒന്നുമില്ല'], '16-ാം നൂറ്റാണ്ട് മുതൽ', 'hard'),
        qb('ഭാഷാഭൂഷണം രചയിതാവ്?', ['A.R. Rajaraja Varma', 'Kumaranasan', 'Ulloor', 'Vallathol'], 'A.R. Rajaraja Varma', 'hard'),
        qb('കേരള സാഹിത്യ അക്കാദമി സ്ഥാപിച്ച വർഷം?', ['1956', '1947', '2000', '1990'], '1956', 'hard'),
        qb('മലയാളം ആദ്യം ശിലാലിഖിതങ്ങളിൽ കാണുന്നത്?', ['9-10 നൂറ്റാണ്ട്', '1st century BCE', '2020', 'ഒന്നുമില്ല'], '9-10 നൂറ്റാണ്ട്', 'hard'),
        qb('ചമ്പു ശൈലി സംയോജിപ്പിക്കുന്നത്?', ['ഗദ്യവും പദ്യവും', 'ഗദ്യം മാത്രം', 'ഇംഗ്ലീഷ് മാത്രം', 'അറബി മാത്രം'], 'ഗദ്യവും പദ്യവും', 'hard'),
        qb('പാട്ടിന്റെ സാഹിത്യ അർത്ഥം?', ['പാട്ട്/പദ്യ രൂപം', 'അക്ഷരം', 'നിഘണ്ടു', 'നോവൽ'], 'പാട്ട്/പദ്യ രൂപം', 'medium'),
        qb('കേരളത്തിലെ മലയാള ഔദ്യോഗിക ഭാഷാ നില ഏതിന് മുതൽ?', ['സംസ്ഥാന രൂപീകരണം 1956', '1947 മാത്രം', '2010', 'ഒരിക്കലും ഇല്ല'], 'സംസ്ഥാന രൂപീകരണം 1956', 'medium'),
        qb('ലലിതകാവ്യം എന്തിനെ സൂചിപ്പിക്കുന്നു?', ['ലളിത/സുന്ദര കവിത', 'മഹാകാവ്യം മാത്രം', 'നിഘണ്ടു', 'വ്യാകരണം മാത്രം'], 'ലളിത/സുന്ദര കവിത', 'hard'),
        qb('മലയാളത്തിലെ മഹാകാവ്യത്തിന്റെ ഉദാഹരണം?', ['കൃഷ്ണഗാഥാ പാരമ്പര്യം', 'രസീത് മാത്രം', 'നികുതി ഫോം', 'ഒന്നുമില്ല'], 'കൃഷ്ണഗാഥാ പാരമ്പര്യം', 'hard'),
        qb('മലയാള നോവൽ പയോണിയർ ആരെന്ന് പരാമർശിക്കപ്പെടുന്നു?', ['O. Chandu Menon (Indulekha)', 'Ezhuthachan only', 'ഒന്നുമില്ല', 'Shakespeare'], 'O. Chandu Menon (Indulekha)', 'hard'),
        qb('ഇന്ദുലേഖ നോവലിന്റെ പ്രാധാന്യം?', ['ആദ്യ പ്രധാന മലയാള നോവൽ', 'ആദ്യ മഹാകാവ്യം', 'ആദ്യ നിഘണ്ടു', 'ആദ്യ വ്യാകരണം'], 'ആദ്യ പ്രധാന മലയാള നോവൽ', 'hard'),
        qb('മലയാള നാടക പയോണിയർ?', ['Ayyampuzha Ramakrishnan / early playwrights', 'Shakespeare', 'Homer', 'ഒന്നുമില്ല'], 'Ayyampuzha Ramakrishnan / early playwrights', 'hard'),
        qb('വട്ടെഴുത്ത് ലിപി എന്തുമായി ബന്ധപ്പെട്ടത്?', ['പുരാതന കേരള-തമിഴ് പ്രദേശ ലിപികൾ', 'Arabic', 'Latin', 'Cyrillic'], 'പുരാതന കേരള-തമിഴ് പ്രദേശ ലിപികൾ', 'hard'),
        qb('കോലെഴുത്ത് ലിപി എന്തിനാണ് ഉപയോഗിച്ചത്?', ['മലയാള-തമിഴ് അതിർത്തി കൈയ്യെഴുത്തുകൾ', 'ചൈനീസ്', 'അറബി മാത്രം', 'ഒന്നുമില്ല'], 'മലയാള-തമിഴ് അതിർത്തി കൈയ്യെഴുത്തുകൾ', 'hard'),
        qb('മലയാള വർഷ കലണ്ടർ സാധാരണയായി പിന്തുടരുന്നത്?', ['Kollavarsham', 'Gregorian only', 'Islamic only', 'ഒന്നുമില്ല'], 'Kollavarsham', 'hard'),
        qb('ചിങ്ങം മാസം മലയാള കലണ്ടറിൽ?', ['ആദ്യ മാസം (ഏകദേശം ആഗസ്റ്റ് മധ്യം)', 'അവസാന മാസം', 'മധ്യ മാസം മാത്രം', 'ഒന്നുമില്ല'], 'ആദ്യ മാസം (ഏകദേശം ആഗസ്റ്റ് മധ്യം)', 'hard'),
        qb('മലയാള ലിപി പരിഷ്കരണ പ്രസ്ഥാനം നയിച്ചവർ?', ['സാമൂഹിക പരിഷ്കർത്താക്കൾ/വിദ്യാഭ്യാസവിദഗ്ധർ', 'ബ്രിട്ടീഷ് മാത്രം', 'ഒന്നുമില്ല', 'ചലച്ചിത്ര സംവിധായകർ'], 'സാമൂഹിക പരിഷ്കർത്താക്കൾ/വിദ്യാഭ്യാസവിദഗ്ധർ', 'hard'),
        qb('യൂണികോഡ് മലയാള ബ്ലോക്ക് ഉൾപ്പെടുത്തിയത്?', ['യൂണികോഡ് 1.0 കാലം/1990-കൾ', '2025 മാത്രം', 'ഒരിക്കലും ഇല്ല', '1850'], 'യൂണികോഡ് 1.0 കാലം/1990-കൾ', 'hard'),
        qb('മലയാള ടൈപ്പ് റൈറ്റിംഗ് പ്രചാരിപ്പിച്ചത്?', ['20-ാം നൂറ്റാണ്ട് മുദ്രണം/എസ്.പി പ്രസ്', 'പുരാതന ഗുഹകൾ', 'ഒന്നുമില്ല', 'ചന്ദ്രൻ'], '20-ാം നൂറ്റാണ്ട് മുദ്രണം/എസ്.പി പ്രസ്', 'hard'),
        qb('പച്ച മലയാളത്തിന്റെ അർത്ഥം?', ['ശുദ്ധ മലയാള ഉപയോഗം', 'ഇംഗ്ലീഷ് മിശ്രിതം മാത്രം', 'അറബി മാത്രം', 'ഒന്നുമില്ല'], 'ശുദ്ധ മലയാള ഉപയോഗം', 'medium'),
        qb('മാങ്ലിഷ് എന്തിനെ സൂചിപ്പിക്കുന്നു?', ['മലയാളം-ഇംഗ്ലീഷ് മിശ്രിത സംഭാഷണം', 'ശുദ്ധ സംസ്കൃതം', 'ശുദ്ധ തമിഴ്', 'ഒന്നുമില്ല'], 'മലയാളം-ഇംഗ്ലീഷ് മിശ്രിത സംഭാഷണം', 'easy'),
        qb('എൻ.വി. കൃഷ്ണ വാരിയർ എന്തിന് പ്രസിദ്ധൻ?', ['ലെക്സിക്കോഗ്രഫി/വ്യാകരണ പഠനം', 'ബഹിരാകാശം', 'പ്രതിരോധം', 'ചലച്ചിത്രം'], 'ലെക്സിക്കോഗ്രഫി/വ്യാകരണ പഠനം', 'hard'),
        qb('കുമാരനാശാൻ്റെ യഥാർത്ഥ പേര്?', ['Narayanan Nair', 'Chandu Menon', 'Ulloor', 'Vallathol'], 'Narayanan Nair', 'hard'),
        qb('വല്ലത്തോൾ നാരായണ മേനോൻ സ്ഥാപിച്ചത്?', ['Kerala Kalamandalam', 'ISRO', 'DRDO', 'ECI'], 'Kerala Kalamandalam', 'hard'),
        qb('ഉള്ളൂർ എസ്. പരമേശ്വരയ്യർ പ്രസിദ്ധ രചനാ രീതി?', ['മഹാകാവ്യ കവിത', 'നോവൽ മാത്രം', 'നിഘണ്ടു മാത്രം', 'ചലച്ചിത്ര സ്ക്രിപ്റ്റ് മാത്രം'], 'മഹാകാവ്യ കവിത', 'hard'),
        qb('മലയാള സാഹിത്യ ചരിത്രം രചയിതാവ് (ക്ലാസിക്)?', ['ഉള്ളൂർ (ചരിത്ര കൃതി)', 'Shakespeare', 'Homer', 'ഒന്നുമില്ല'], 'ഉള്ളൂർ (ചരിത്ര കൃതി)', 'hard'),
        qb('1930-കളിലെ മലയാള ചെറുകഥാ വളർച്ച ആരുമായി?', ['ബഷീർ, തകഴി മുതലായവർ', 'ഒന്നുമില്ല', 'ബ്രിട്ടീഷ് മാത്രം', 'ഹിന്ദി മാത്രം'], 'ബഷീർ, തകഴി മുതലായവർ', 'hard'),
    ]

def build_literature() -> list[Question]:
    from rebuild_literature import malayalam_section

    return [
        (item["question"], item["options"], item["answer"], item["difficulty"])
        for item in malayalam_section()
    ]


TARGETS = [
    ("indian_history.json", "ih_", build_indian_history(), 100),
    ("modern_india.json", "mi_", build_modern_india(), 100),
    ("sports.json", "sca_", build_sports(), 100),
    ("national_schemes.json", "ns_", build_national_schemes(), 100),
    ("social_welfare_schemes.json", "sws_", build_social_welfare(), 100),
    ("indian_industries.json", "ii_", build_indian_industries(), 100),
    ("international_organizations.json", "io_", build_international_orgs(), 100),
    ("philosophy.json", "phi_", build_philosophy(), 100),
    ("basic_general_knowledge.json", "bgk_", build_basic_gk(), 200),
    ("politics_of_kerala.json", "pok_", build_politics_kerala(), 100),
    ("kerala_through_districts.json", "ktd_", build_kerala_districts(), 100),
    ("current_affairs_2026_06.json", "ca_2026_06_", build_current_affairs(), 40),
    ("malayalam.json", "mal_", build_malayalam(), 100),
    ("literature.json", "lit_", build_literature(), 100),
]


def main() -> None:
    random.seed(42)
    existing = load_all_existing()
    print(f"Loaded {len(existing)} existing questions from all JSON files.\n")

    total_added = 0
    for filename, prefix, candidates, target_total in TARGETS:
        added = fill_file(filename, prefix, candidates, target_total, existing)
        total_added += added
        print(f"  {filename}: +{added} (target {target_total})")

    print(f"\nTotal added: {total_added}")


if __name__ == "__main__":
    main()

