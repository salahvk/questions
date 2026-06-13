#!/usr/bin/env python3
"""Rebuild literature.json with proper Malayalam."""
import json
import random
from pathlib import Path

random.seed(42)
BASE = Path(__file__).parent

W = {
    # World literature — keep original English titles
    "Iliad": "Iliad",
    "Odyssey": "Odyssey",
    "Divine Comedy": "Divine Comedy",
    "Don Quixote": "Don Quixote",
    "War and Peace": "War and Peace",
    "Anna Karenina": "Anna Karenina",
    "Crime and Punishment": "Crime and Punishment",
    "The Brothers Karamazov": "The Brothers Karamazov",
    "Madame Bovary": "Madame Bovary",
    "Les Miserables": "Les Misérables",
    "The Stranger": "The Stranger",
    "The Trial": "The Trial",
    "One Hundred Years of Solitude": "One Hundred Years of Solitude",
    "Love in the Time of Cholera": "Love in the Time of Cholera",
    "Faust": "Faust",
    "The Metamorphosis": "The Metamorphosis",
    "The Little Prince": "The Little Prince",
    "The Alchemist": "The Alchemist",
    "A Tale of Two Cities": "A Tale of Two Cities",
    "Moby-Dick": "Moby-Dick",
    "The Great Gatsby": "The Great Gatsby",
    "To Kill a Mockingbird": "To Kill a Mockingbird",
    "The Catcher in the Rye": "The Catcher in the Rye",
    "Ulysses": "Ulysses",
    "Hamlet": "Hamlet",
    "Macbeth": "Macbeth",
    "Gitanjali": "Gitanjali",
    "Godan": "Godan",
    "Mrichchakatika": "Mrichchakatika",
    "Abhijnanasakuntalam": "Abhijnanasakuntalam",
    "Meghaduta": "Meghaduta",
    "Midnight's Children": "Midnight's Children",
    "God of Small Things": "The God of Small Things",
    "Animal Farm": "Animal Farm",
    "Brave New World": "Brave New World",
    "Lord of the Rings": "The Lord of the Rings",
    "Harry Potter": "Harry Potter",
    "Pride and Prejudice": "Pride and Prejudice",
    "Wuthering Heights": "Wuthering Heights",
    "Great Expectations": "Great Expectations",
    "Old Man and the Sea": "The Old Man and the Sea",
    "Alice in Wonderland": "Alice in Wonderland",
    "Iliad and Odyssey": "Iliad and Odyssey",
    "Malgudi": "Malgudi",
    "Ayemenem": "Ayemenem",
    "Wessex": "Wessex",
    # Malayalam / regional works
    "Chinthavishtayaya Sita": "ചിന്താവിഷ്ടയായ സീത",
    "Balyakalasakhi": "ബാല്യകാലസഖി",
    "Chemmeen": "ചെമ്മീൻ",
    "Naalukettu": "നാലുകെട്ട്",
    "Khasakkinte Ithihasam": "ഖസാക്കിന്റെ ഇതിഹാസം",
    "Odakkuzhal": "ഓടക്കുഴൽ",
    "Khasak": "ഖസാക്ക്",
}

A = {
    "Homer": "ഹോമർ",
    "Dante": "ഡാന്റെ",
    "Miguel de Cervantes": "മിഗ്വേൽ ഡി സർവാന്റസ്",
    "Cervantes": "മിഗ്വേൽ ഡി സർവാന്റസ്",
    "Leo Tolstoy": "ലിയോ ടോൾസ്റ്റോയ്",
    "Tolstoy": "ലിയോ ടോൾസ്റ്റോയ്",
    "Dostoevsky": "ദോസ്തോയെവ്സ്കി",
    "Gustave Flaubert": "ഗുസ്താവ് ഫ്ലോബെർ",
    "Victor Hugo": "വിക്ടർ ഹ്യൂഗോ",
    "Albert Camus": "ആൽബർ കാമ്യൂ",
    "Franz Kafka": "ഫ്രാൻസ് കാഫ്ക",
    "Gabriel Garcia Marquez": "ഗബ്രിയേൽ ഗാർസിയ മാർക്വസ്",
    "Goethe": "ഗ്യോതെ",
    "Paulo Coelho": "പൗലോ കോയ്ലോ",
    "Charles Dickens": "ചാൾസ് ഡിക്കൻസ്",
    "Dickens": "ചാൾസ് ഡിക്കൻസ്",
    "Herman Melville": "ഹെർമൻ മെൽവിൽ",
    "F. Scott Fitzgerald": "എഫ്. സ്കോട്ട് ഫിറ്റ്സ്ജെറാൾഡ്",
    "Harper Lee": "ഹാർപ്പർ ലീ",
    "J.D. Salinger": "ജെ.ഡി. സലിഞ്ജർ",
    "James Joyce": "ജെയിംസ് ജോയ്‌സ്",
    "Antoine de Saint-Exupery": "ആൻറ്വൺ ഡി സെയ്ന്റ്-എക്സ്യൂപറി",
    "Rabindranath Tagore": "രവീന്ദ്രനാഥ ടാഗോർ",
    "Tagore": "രവീന്ദ്രനാഥ ടാഗോർ",
    "Premchand": "മുൻഷി പ്രേംചന്ദ്",
    "Sudraka": "ശൂദ്രകൻ",
    "Kalidasa": "കാലിദാസൻ",
    "Tulsidas": "തുലസിദാസ്",
    "Valmiki": "വാല്മീകി",
    "Vyasa": "വ്യാസൻ",
    "William Shakespeare": "വില്ലിയം ഷേക്സ്പിയർ",
    "Shakespeare": "വില്ലിയം ഷേക്സ്പിയർ",
    "Salman Rushdie": "സൽമാൻ റുഷ്ദി",
    "Arundhati Roy": "അരുന്ധതി റോയ്",
    "R.K. Narayan": "ആർ.കെ. നാരായണൻ",
    "Ayyappa Paniker": "\u0D05\u0D2F\u0D4D\u0D2F\u0D2A\u0D4D\u0D2A \u0D2A\u0D3E\u0D23\u0D3F\u0D15\u0D30\u0D4D",
    "Thakazhi": "തകഴി ശിവശങ്കര പിള്ള",
    "Basheer": "വൈകം മുഹമ്മദ് ബഷീർ",
    "MT": "എം.ടി. വാസുദേവൻ നായർ",
    "OV Vijayan": "ഒ.വി. വിജയൻ",
    "G. Sankara Kurup": "ജി. ശങ്കര കുറുപ്പ്",
    "G. Sankara Kurup (Odakkuzhal)": "ജി. ശങ്കര കുറുപ്പ് (ഓടക്കുഴൽ)",
    "ONV": "ഒ.എൻ.വി. കുറുപ്പ്",
    "ONV Kurup": "ഒ.എൻ.വി. കുറുപ്പ്",
    "Sugathakumari": "സുഗതകുമാരി",
    "Kamala Surayya": "കമലാ സുരയ്യ",
    "Kamala Das": "കമലാ ദാസ്",
    "Kumaranasan": "കുമാരനാശാൻ",
    "Vallathol": "വള്ളത്തോൾ",
    "Ulloor": "ഉള്ളൂർ",
    "Jane Austen": "ജെയ്ൻ ഓസ്റ്റിൻ",
    "Austen": "ജെയ്ൻ ഓസ്റ്റിൻ",
    "Emily Bronte": "എമിലി ബ്രോണ്ടെ",
    "Bronte": "എമിലി ബ്രോണ്ടെ",
    "Ernest Hemingway": "എർണസ്റ്റ് ഹെമിംഗ്വേ",
    "George Orwell": "ജോർജ് ഓർവെൽ",
    "Orwell": "ജോർജ് ഓർവെൽ",
    "Aldous Huxley": "ഔൾഡസ് ഹക്സ്ലി",
    "Huxley": "ഔൾഡസ് ഹക്സ്ലി",
    "J.R.R. Tolkien": "ജെ.ആർ.ആർ. റ്റോൾകീൻ",
    "Tolkien": "ജെ.ആർ.ആർ. റ്റോൾകീൻ",
    "J.K. Rowling": "ജെ.കെ. റോലിംഗ്",
    "Rowling": "ജെ.കെ. റോലിംഗ്",
    "Lewis Carroll": "ലൂയിസ് കാരോൾ",
    "Chekhov": "ആന്റൺ ചെഖോവ്",
    "Pushkin": "പുഷ്കിൻ",
    "Schiller": "ഷില്ലർ",
    "Thomas Hardy": "തോമസ് ഹാർഡി",
    "Faulkner": "\u0D35\u0D3F\u0D32\u0D4D\u0D32\u0D4D\u0D2F\u0D02 \u0D2B\u0D4B\u0D7E\u0D15\u0D4D\u0D28\u0D7C",
    "Steinbeck": "\u0D1C\u0D4B\u0D23\u0D4D \u0D38\u0D4D\u0D1F\u0D48\u0D28\u0D4D\u0D2C\u0D46\u0D15\u0D4D",
    "Twain": "\u0D2E\u0D3E\u0D31\u0D4D\u0D15\u0D4D \u0D1F\u0D4D\u0D35\u0D47\u0D28\u0D4D",
    "Asimov": "\u0D10\u0D38\u0D15\u0D4D \u0D06\u0D38\u0D3F\u0D2E\u0D4B\u0D35\u0D4D",
    "Lewis": "സി.എസ്. ലൂയിസ്",
}

INDIAN_WORKS = {
    "Gitanjali", "Godan", "Mrichchakatika", "Abhijnanasakuntalam",
}

ALL_WORKS_ML = set(W.values())
ALL_AUTHORS_ML = set(A.values())

WORLD_PAIRS = [
    ("Iliad", "Homer", "medium"),
    ("Homer", "Iliad", "medium"),
    ("Odyssey", "Homer", "medium"),
    ("Divine Comedy", "Dante", "medium"),
    ("Dante", "Divine Comedy", "medium"),
    ("Don Quixote", "Miguel de Cervantes", "medium"),
    ("Miguel de Cervantes", "Don Quixote", "medium"),
    ("War and Peace", "Leo Tolstoy", "medium"),
    ("Leo Tolstoy", "War and Peace", "medium"),
    ("Anna Karenina", "Leo Tolstoy", "medium"),
    ("Crime and Punishment", "Dostoevsky", "medium"),
    ("Dostoevsky", "Crime and Punishment", "medium"),
    ("The Brothers Karamazov", "Dostoevsky", "medium"),
    ("Madame Bovary", "Gustave Flaubert", "medium"),
    ("Gustave Flaubert", "Madame Bovary", "medium"),
    ("Les Miserables", "Victor Hugo", "medium"),
    ("Victor Hugo", "Les Miserables", "medium"),
    ("The Stranger", "Albert Camus", "medium"),
    ("Albert Camus", "The Stranger", "medium"),
    ("The Trial", "Franz Kafka", "medium"),
    ("Franz Kafka", "The Trial", "medium"),
    ("One Hundred Years of Solitude", "Gabriel Garcia Marquez", "medium"),
    ("Gabriel Garcia Marquez", "One Hundred Years of Solitude", "medium"),
    ("Love in the Time of Cholera", "Gabriel Garcia Marquez", "medium"),
    ("Faust", "Goethe", "medium"),
    ("Goethe", "Faust", "medium"),
    ("The Metamorphosis", "Franz Kafka", "medium"),
    ("The Little Prince", "Antoine de Saint-Exupery", "medium"),
    ("Antoine de Saint-Exupery", "The Little Prince", "medium"),
    ("The Alchemist", "Paulo Coelho", "medium"),
    ("Paulo Coelho", "The Alchemist", "medium"),
    ("A Tale of Two Cities", "Charles Dickens", "medium"),
    ("Charles Dickens", "A Tale of Two Cities", "medium"),
    ("Moby-Dick", "Herman Melville", "medium"),
    ("Herman Melville", "Moby-Dick", "medium"),
    ("The Great Gatsby", "F. Scott Fitzgerald", "medium"),
    ("F. Scott Fitzgerald", "The Great Gatsby", "medium"),
    ("To Kill a Mockingbird", "Harper Lee", "medium"),
    ("Harper Lee", "To Kill a Mockingbird", "medium"),
    ("The Catcher in the Rye", "J.D. Salinger", "medium"),
    ("J.D. Salinger", "The Catcher in the Rye", "medium"),
    ("Ulysses", "James Joyce", "medium"),
    ("James Joyce", "Ulysses", "medium"),
    ("Gitanjali", "Rabindranath Tagore", "medium"),
    ("Rabindranath Tagore", "Gitanjali", "medium"),
    ("Godan", "Premchand", "medium"),
    ("Premchand", "Godan", "medium"),
    ("Mrichchakatika", "Sudraka", "medium"),
    ("Sudraka", "Mrichchakatika", "medium"),
    ("Abhijnanasakuntalam", "Kalidasa", "medium"),
]

LIT_001 = {
    "question": "'ഇരുപ്പ്' എന്ന പ്രസിദ്ധ കവിതയുടെ രചയിതാവ് ആരാണ്?",
    "options": ["കുമാരനാശാൻ", "വള്ളത്തോൾ", "ഉള്ളൂർ", "ചങ്ങമ്പുഴ"],
    "answer": "കുമാരനാശാൻ",
    "difficulty": "medium",
}


def mw(key: str) -> str:
    return W[key]


def ma(key: str) -> str:
    return A[key]


def pick(pool: set[str], correct: str, n: int = 3) -> list[str]:
    xs = [x for x in pool if x != correct]
    random.shuffle(xs)
    return xs[:n]


def q_work_author(work_key: str, author_key: str, difficulty: str) -> dict:
    work_ml, author_ml = mw(work_key), ma(author_key)
    if work_key in INDIAN_WORKS:
        q = f"'{work_ml}' എന്ന ഇന്ത്യൻ കൃതിയുടെ രചയിതാവ് ആരാണ്?"
    else:
        q = f"'{work_ml}' എന്ന കൃതിയുടെ രചയിതാവ് ആരാണ്?"
    opts = pick(ALL_AUTHORS_ML, author_ml) + [author_ml]
    random.shuffle(opts)
    return {"question": q, "options": opts, "answer": author_ml, "difficulty": difficulty}


def q_author_work(author_key: str, work_key: str, difficulty: str) -> dict:
    work_ml, author_ml = mw(work_key), ma(author_key)
    q = f"{author_ml} രചിച്ച പ്രസിദ്ധ കൃതി ഏത്?"
    opts = pick(ALL_WORKS_ML, work_ml) + [work_ml]
    random.shuffle(opts)
    return {"question": q, "options": opts, "answer": work_ml, "difficulty": difficulty}


def q_title_author(title: str, opts: list[str], ans: str, diff: str, *, indian: bool = False) -> dict:
    kind = "ഇന്ത്യൻ കൃതിയുടെ" if indian else "കൃതിയുടെ"
    return q(f"'{title}' എന്ന {kind} രചയിതാവ് ആരാണ്?", opts, ans, diff)


def q_title_author_key(work_key: str, opts: list[str], ans: str, diff: str, *, indian: bool = False) -> dict:
    return q_title_author(mw(work_key), opts, ans, diff, indian=indian)


def q(qtext: str, opts: list[str], ans: str, diff: str) -> dict:
    return {"question": qtext, "options": opts, "answer": ans, "difficulty": diff}


def malayalam_section() -> list[dict]:
    return [
        q("മലയാള ആധുനിക കവിതയുടെ പിതാവ് എന്നറിയപ്പെടുന്ന കവി ആരാണ്?",
          [ma("Ayyappa Paniker"), ma("ONV"), ma("Sugathakumari"), ma("Kamala Surayya")],
          ma("Ayyappa Paniker"), "medium"),
        q("വൈകം മുഹമ്മദ് ബഷീറിന്റെ ബാല്യകാല പ്രണയത്തെ ആസ്പദമാക്കി എഴുതിയ നോവൽ ഏത്?",
          [mw("Balyakalasakhi"), mw("Chemmeen"), mw("Naalukettu"), mw("Iliad")],
          mw("Balyakalasakhi"), "hard"),
        q("തകഴി ശിവശങ്കര പിള്ള രചിച്ച പ്രസിദ്ധ നോവൽ ഏത്?",
          [mw("Chemmeen"), mw("God of Small Things"), mw("Midnight's Children"), mw("Iliad")],
          mw("Chemmeen"), "easy"),
        q_title_author_key("Chemmeen",
          [ma("Thakazhi"), ma("Basheer"), ma("MT"), ma("OV Vijayan")],
          ma("Thakazhi"), "easy"),
        q("എം.ടി. വാസുദേവൻ നായർ രചിച്ച പ്രസിദ്ധ നോവൽ ഏത്?",
          [mw("Naalukettu"), mw("Chemmeen"), mw("Iliad"), mw("Odyssey")],
          mw("Naalukettu"), "medium"),
        q("ഒ.വി. വിജയൻ രചിച്ച പ്രസിദ്ധ നോവൽ ഏത്?",
          [mw("Khasakkinte Ithihasam"), mw("Chemmeen"), mw("Naalukettu"), mw("Iliad")],
          mw("Khasakkinte Ithihasam"), "medium"),
        q_title_author_key("God of Small Things",
          [ma("Arundhati Roy"), ma("R.K. Narayan"), ma("Tagore"), ma("Premchand")],
          ma("Arundhati Roy"), "medium"),
        q("മലയാളത്തിൽ ജ്ഞാനപീഠ പുരസ്കാരം നേടിയ ആദ്യ കവി ആരാണ്?",
          [ma("G. Sankara Kurup (Odakkuzhal)"), ma("Basheer"), ma("MT"), ma("ONV")],
          ma("G. Sankara Kurup (Odakkuzhal)"), "hard"),
        q("'ഓടക്കുഴൽ' എന്ന കവിതാസമാഹാരത്തിന്റെ രചയിതാവ് ആരാണ്?",
          [ma("G. Sankara Kurup"), ma("Kumaranasan"), ma("Ulloor"), ma("Vallathol")],
          ma("G. Sankara Kurup"), "hard"),
        q("കുമാരനാശാൻ രചിച്ച പ്രസിദ്ധ കൃതി ഏത്?",
          [mw("Chinthavishtayaya Sita"), mw("Chemmeen"), mw("Naalukettu"), mw("Iliad")],
          mw("Chinthavishtayaya Sita"), "medium"),
        q("വള്ളത്തോളുടെ 'ബന്ധനസ്ഥാനയ അനിരുദ്ധൻ' ഏത് തരം സാഹിത്യകൃതിയാണ്?",
          ["മഹാകാവ്യം", "നോവൽ", "ചെറുകഥ", "നാടകം"],
          "മഹാകാവ്യം", "hard"),
        q("ഉള്ളൂരിന്റെ 'ഉമാകേരളം' ഏത് തരം സാഹിത്യകൃതിയാണ്?",
          ["മഹാകാവ്യം", "നോവൽ", "അക്ഷരശേഖരം", "നിഘണ്ടു"],
          "മഹാകാവ്യം", "hard"),
        q("ഹോമർ രചിച്ച പ്രസിദ്ധ കൃതി ഏത്?",
          [mw("Iliad and Odyssey"), mw("Divine Comedy"), mw("Hamlet"), mw("Faust")],
          mw("Iliad and Odyssey"), "easy"),
        q_title_author_key("Divine Comedy",
          [ma("Dante"), ma("Homer"), ma("Shakespeare"), ma("Tolstoy")],
          ma("Dante"), "easy"),
        q("വില്ലിയം ഷേക്സ്പിയർ രചിച്ച പ്രസിദ്ധ നാടകം ഏത്?",
          [mw("Hamlet"), mw("Iliad"), mw("Odyssey"), mw("Faust")],
          mw("Hamlet"), "easy"),
        q_title_author_key("War and Peace",
          [ma("Leo Tolstoy"), ma("Dostoevsky"), ma("Chekhov"), ma("Pushkin")],
          ma("Leo Tolstoy"), "medium"),
        q_title_author_key("Crime and Punishment",
          [ma("Dostoevsky"), ma("Tolstoy"), ma("Homer"), ma("Dante")],
          ma("Dostoevsky"), "medium"),
        q_title_author_key("Faust",
          [ma("Goethe"), ma("Schiller"), ma("Homer"), ma("Dante")],
          ma("Goethe"), "hard"),
        q_title_author_key("Don Quixote",
          [ma("Cervantes"), ma("Homer"), ma("Dante"), ma("Shakespeare")],
          ma("Cervantes"), "medium"),
        q_title_author_key("One Hundred Years of Solitude",
          [ma("Gabriel Garcia Marquez"), ma("Tolstoy"), ma("Homer"), ma("Tagore")],
          ma("Gabriel Garcia Marquez"), "hard"),
        q("രവീന്ദ്രനാഥ ടാഗോർക്ക് നോബൽ സാഹിത്യ പുരസ്കാരം ലഭിച്ച കൃതി ഏത്?",
          [mw("Gitanjali"), mw("Chemmeen"), mw("Naalukettu"), mw("Iliad")],
          mw("Gitanjali"), "medium"),
        q("മുൻഷി പ്രേംചന്ദ് രചിച്ച പ്രസിദ്ധ ഹിന്ദി കൃതി ഏത്?",
          [mw("Godan"), mw("Chemmeen"), mw("Hamlet"), mw("Iliad")],
          mw("Godan"), "hard"),
        q("ആർ.കെ. നാരായണൻ സൃഷ്ടിച്ച കൽപിത നഗരം ഏത്?",
          [mw("Malgudi"), mw("Khasak"), mw("Ayemenem"), mw("Wessex")],
          mw("Malgudi"), "medium"),
        q_title_author_key("Midnight's Children",
          [ma("Salman Rushdie"), ma("Arundhati Roy"), ma("Tagore"), ma("Premchand")],
          ma("Salman Rushdie"), "hard"),
        q_title_author_key("Alice in Wonderland",
          [ma("Lewis Carroll"), ma("Dickens"), ma("Austen"), ma("Bronte")],
          ma("Lewis Carroll"), "medium"),
        q_title_author_key("Pride and Prejudice",
          [ma("Jane Austen"), ma("Bronte"), ma("Dickens"), ma("Thomas Hardy")],
          ma("Jane Austen"), "medium"),
        q_title_author_key("Wuthering Heights",
          [ma("Emily Bronte"), ma("Jane Austen"), ma("Dickens"), ma("Thomas Hardy")],
          ma("Emily Bronte"), "hard"),
        q_title_author_key("Great Expectations",
          [ma("Charles Dickens"), ma("Austen"), ma("Homer"), ma("Dante")],
          ma("Charles Dickens"), "medium"),
        q_title_author_key("Old Man and the Sea",
          [ma("Ernest Hemingway"), ma("Faulkner"), ma("Steinbeck"), ma("Twain")],
          ma("Ernest Hemingway"), "medium"),
        q_title_author_key("To Kill a Mockingbird",
          [ma("Harper Lee"), ma("Austen"), ma("Bronte"), ma("Dickens")],
          ma("Harper Lee"), "hard"),
        q("'1984' എന്ന കൃതിയുടെ രചയിതാവ് ആരാണ്?",
          [ma("George Orwell"), ma("Huxley"), ma("Asimov"), ma("Tolkien")],
          ma("George Orwell"), "medium"),
        q_title_author_key("Animal Farm",
          [ma("George Orwell"), ma("Huxley"), ma("Dickens"), ma("Asimov")],
          ma("George Orwell"), "medium"),
        q_title_author_key("Brave New World",
          [ma("Aldous Huxley"), ma("Orwell"), ma("Asimov"), ma("Tolkien")],
          ma("Aldous Huxley"), "hard"),
        q_title_author_key("Lord of the Rings",
          [ma("J.R.R. Tolkien"), ma("Rowling"), ma("Lewis"), ma("Orwell")],
          ma("J.R.R. Tolkien"), "medium"),
        q_title_author_key("Harry Potter",
          [ma("J.K. Rowling"), ma("Tolkien"), ma("Lewis"), ma("Dickens")],
          ma("J.K. Rowling"), "easy"),
        q("പാരമ്പര്യമായി രാമായണം രചിച്ചത് ആരാണ്?",
          ["വാല്മീകി", "വ്യാസൻ", "തുലസിദാസ്", "കാലിദാസൻ"],
          "വാല്മീകി", "easy"),
        q("പാരമ്പര്യമായി മഹാഭാരതം രചിച്ചത് ആരാണ്?",
          ["വ്യാസൻ", "വാല്മീകി", "തുലസിദാസ്", "കാലിദാസൻ"],
          "വ്യാസൻ", "easy"),
        q("കാലിദാസൻ രചിച്ച പ്രസിദ്ധ നാടകം ഏത്?",
          [mw("Abhijnanasakuntalam"), mw("Hamlet"), mw("Macbeth"), mw("Faust")],
          mw("Abhijnanasakuntalam"), "medium"),
        q_title_author_key("Meghaduta",
          [ma("Kalidasa"), ma("Valmiki"), ma("Vyasa"), ma("Tulsidas")],
          ma("Kalidasa"), "hard", indian=True),
        q("തുലസിദാസ് രചിച്ച 'രാമചരിതമാനസ്' ഏത് ഭാഷയിലാണ്?",
          ["അവധി/ഹിന്ദി", "സംസ്കൃതം മാത്രം", "മലയാളം", "തമിഴ്"],
          "അവധി/ഹിന്ദി", "hard"),
        q("കബീറിന്റെ ദോഹകൾ പ്രധാനമായും ഏത് ഭാഷയിലാണ് രചിച്ചത്?",
          ["ഖഡി ബോലി/ഹിന്ദി മിശ്രണം", "മലയാളം", "ഇംഗ്ലീഷ്", "ഫ്രെഞ്ച്"],
          "ഖഡി ബോലി/ഹിന്ദി മിശ്രണം", "hard"),
        q("സൂർദാസ് രചിച്ച ഭക്തികവിതകൾ ഏതിനെ കുറിച്ചുള്ളവയാണ്?",
          ["ശ്രീകൃഷ്ണനെ", "ശിവനെ മാത്രം", "ബുദ്ധനെ മാത്രം", "ജൈനതത്വത്തെ മാത്രം"],
          "ശ്രീകൃഷ്ണനെ", "hard"),
        q("മിര്സാ ഗാലിബിന്റെ ഭാഷ എത്?",
          ["ഉർദു/പേർഷ്യൻ", "മലയാളം", "തമിഴ്", "ഇംഗ്ലീഷ്"],
          "ഉർദു/പേർഷ്യൻ", "hard"),
        q("സാദത് ഹസൻ മാന്റോ ഏതിനാണ് പ്രശസ്തൻ?",
          ["വിഭജന കഥകൾ (ഉർദു)", "മലയാള നോവലുകൾ", "ഗ്രീക്ക് മഹാകാവ്യങ്ങൾ", "ഒന്നുമില്ല"],
          "വിഭജന കഥകൾ (ഉർദു)", "hard"),
        q("ഒ.എൻ.വി. കുരുപ്പിന് ജ്ഞാനപീഠ പുരസ്കാരം ലഭിച്ചത് എന്തിനാണ്?",
          ["മലയാള കവിതാ സംഭാവനകൾ", "ഇംഗ്ലീഷ് നോവലുകൾ", "ഹിന്ദി മാത്രം", "തമിഴ്"],
          "മലയാള കവിതാ സംഭാവനകൾ", "hard"),
        q("സുഗതകുമാരി ഏതിനാണ് പ്രശസ്ത?",
          ["കവിതയും പരിസ്ഥിതി പ്രവർത്തനവും", "നോവലുകൾ മാത്രം", "നാടകങ്ങൾ മാത്രം", "ചിത്രകല മാത്രം"],
          "കവിതയും പരിസ്ഥിതി പ്രവർത്തനവും", "medium"),
        q("കമലാ സുരയ്യ മുൻപ് ഏത് പേരിൽ അറിയപ്പെട്ടിരുന്നു?",
          ["കമലാ ദാസ്", "ഒന്നുമില്ല", "മാധവിക്കുട്ടി (വേറൊരാൾ)", "രണ്ട് പേരുകളും ഒരാളുടേതല്ല"],
          "കമലാ ദാസ്", "medium"),
        q("കേന്ദ്ര സാഹിത്യ അക്കാദമി സ്ഥാപിതമായ വർഷം ഏത്?",
          ["1954", "1947", "2000", "1990"],
          "1954", "hard"),
        q("യുനെസ്കോ ലോക സാഹിത്യ ദിനം ആചരിക്കുന്നത് എപ്പോഴാണ്?",
          ["ഏപ്രിൽ 23", "ജൂൺ 1", "ജനുവരി 1", "ഡിസംബർ 25"],
          "ഏപ്രിൽ 23", "hard"),
    ]


def build_questions() -> list[dict]:
    out = [LIT_001]
    for work_key, author_key, diff in WORLD_PAIRS:
        if WORLD_PAIRS.index((work_key, author_key, diff)) % 2 == 0:
            out.append(q_work_author(work_key, author_key, diff))
        else:
            out.append(q_author_work(author_key, work_key, diff))
    out.extend(malayalam_section())
    return out


if __name__ == "__main__":
    questions = []
    questions.append({**LIT_001, "id": "lit_001"})
    idx = 2
    for a, b, diff in WORLD_PAIRS:
        if a in W:
            body = q_work_author(a, b, diff)
        else:
            body = q_author_work(a, b, diff)
        questions.append({**body, "id": f"lit_{idx:03d}"})
        idx += 1
    for body in malayalam_section():
        questions.append({**body, "id": f"lit_{idx:03d}"})
        idx += 1
    path = BASE / "literature.json"
    path.write_text(json.dumps({"questions": questions}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {path}")
