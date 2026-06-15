#!/usr/bin/env python3
"""English-only grammar, vocabulary, and spelling questions."""

from __future__ import annotations

import random

from refill_common import add_candidate, Candidate

SYNONYMS: list[tuple[str, str, list[str], str]] = [
    ("Abundant", "Plentiful", ["Scarce", "Rare", "Limited"], "easy"),
    ("Brave", "Courageous", ["Cowardly", "Timid", "Weak"], "easy"),
    ("Begin", "Start", ["End", "Finish", "Close"], "easy"),
    ("Clever", "Intelligent", ["Foolish", "Dull", "Slow"], "easy"),
    ("Difficult", "Hard", ["Easy", "Simple", "Light"], "easy"),
    ("Enormous", "Huge", ["Tiny", "Small", "Little"], "easy"),
    ("Fast", "Quick", ["Slow", "Late", "Lazy"], "easy"),
    ("Generous", "Kind", ["Stingy", "Selfish", "Cruel"], "easy"),
    ("Happy", "Joyful", ["Sad", "Angry", "Tired"], "easy"),
    ("Honest", "Truthful", ["Dishonest", "Cunning", "False"], "easy"),
    ("Rapid", "Swift", ["Slow", "Weak", "Lazy"], "easy"),
    ("Silent", "Quiet", ["Loud", "Noisy", "Harsh"], "easy"),
    ("Strong", "Powerful", ["Weak", "Frail", "Soft"], "easy"),
    ("Tiny", "Small", ["Huge", "Large", "Wide"], "easy"),
    ("Ancient", "Old", ["Modern", "New", "Fresh"], "easy"),
    ("Dangerous", "Risky", ["Safe", "Secure", "Calm"], "medium"),
    ("Diligent", "Hardworking", ["Lazy", "Idle", "Slow"], "easy"),
    ("Fragile", "Delicate", ["Strong", "Hard", "Tough"], "easy"),
    ("Obsolete", "Outdated", ["Modern", "New", "Current"], "medium"),
    ("Benevolent", "Kind", ["Mean", "Cruel", "Harsh"], "medium"),
    ("Candid", "Honest", ["Deceptive", "Secretive", "Vague"], "medium"),
    ("Eloquent", "Fluent", ["Inarticulate", "Mute", "Hesitant"], "medium"),
    ("Genuine", "Authentic", ["Fake", "False", "Counterfeit"], "medium"),
    ("Meticulous", "Careful", ["Careless", "Sloppy", "Hasty"], "medium"),
    ("Pragmatic", "Practical", ["Idealistic", "Impractical", "Theoretical"], "medium"),
    ("Resilient", "Tough", ["Fragile", "Weak", "Brittle"], "medium"),
    ("Tranquil", "Calm", ["Noisy", "Chaotic", "Restless"], "medium"),
    ("Vivid", "Bright", ["Dull", "Faint", "Pale"], "medium"),
    ("Ample", "Plentiful", ["Scarce", "Meagre", "Limited"], "easy"),
    ("Brief", "Short", ["Long", "Extended", "Lengthy"], "easy"),
    ("Cease", "Stop", ["Start", "Begin", "Continue"], "easy"),
    ("Diverse", "Varied", ["Uniform", "Identical", "Same"], "medium"),
    ("Eager", "Keen", ["Reluctant", "Unwilling", "Indifferent"], "easy"),
    ("Frequent", "Often", ["Rare", "Seldom", "Never"], "easy"),
    ("Genuine", "Real", ["Fake", "Sham", "Counterfeit"], "easy"),
    ("Humble", "Modest", ["Arrogant", "Proud", "Boastful"], "medium"),
    ("Immense", "Huge", ["Tiny", "Minute", "Small"], "easy"),
    ("Jovial", "Cheerful", ["Gloomy", "Sullen", "Morose"], "medium"),
    ("Keen", "Eager", ["Apathetic", "Indifferent", "Reluctant"], "easy"),
    ("Loyal", "Faithful", ["Disloyal", "Treacherous", "False"], "easy"),
    ("Mature", "Adult", ["Immature", "Childish", "Juvenile"], "easy"),
    ("Noble", "Honourable", ["Ignoble", "Base", "Vile"], "medium"),
    ("Oblige", "Compel", ["Free", "Release", "Excuse"], "hard"),
    ("Polite", "Courteous", ["Rude", "Impolite", "Abrupt"], "easy"),
    ("Quaint", "Old-fashioned", ["Modern", "Contemporary", "New"], "medium"),
    ("Rigid", "Stiff", ["Flexible", "Soft", "Pliable"], "medium"),
    ("Sincere", "Genuine", ["Insincere", "False", "Hypocritical"], "medium"),
    ("Timid", "Shy", ["Bold", "Brave", "Confident"], "easy"),
    ("Unique", "Distinct", ["Common", "Ordinary", "Usual"], "easy"),
    ("Vital", "Essential", ["Optional", "Minor", "Trivial"], "medium"),
    ("Wary", "Cautious", ["Careless", "Reckless", "Rash"], "medium"),
    ("Zealous", "Enthusiastic", ["Apathetic", "Indifferent", "Lukewarm"], "hard"),
]

ANTONYMS: list[tuple[str, str, list[str], str]] = [
    ("Ancient", "Modern", ["Old", "Historic", "Aged"], "easy"),
    ("Artificial", "Natural", ["Fake", "Synthetic", "False"], "medium"),
    ("Accept", "Reject", ["Receive", "Allow", "Take"], "medium"),
    ("Brave", "Cowardly", ["Bold", "Fearless", "Heroic"], "easy"),
    ("Expand", "Contract", ["Grow", "Increase", "Extend"], "medium"),
    ("Generous", "Stingy", ["Kind", "Noble", "Liberal"], "easy"),
    ("Happy", "Sad", ["Joyful", "Glad", "Cheerful"], "easy"),
    ("Hot", "Cold", ["Warm", "Mild", "Boiling"], "easy"),
    ("Optimist", "Pessimist", ["Hopeful", "Cheerful", "Positive"], "easy"),
    ("Scarce", "Abundant", ["Few", "Limited", "Rare"], "easy"),
    ("Strong", "Weak", ["Powerful", "Brave", "Bold"], "easy"),
    ("Temporary", "Permanent", ["Fleeting", "Short", "Brief"], "easy"),
    ("Victory", "Defeat", ["Success", "Triumph", "Win"], "easy"),
    ("Early", "Late", ["Soon", "Fast", "Quick"], "easy"),
    ("Increase", "Decrease", ["Grow", "Expand", "Rise"], "easy"),
    ("Profit", "Loss", ["Gain", "Benefit", "Earning"], "easy"),
    ("Superior", "Inferior", ["Better", "Higher", "Greater"], "medium"),
    ("Transparent", "Opaque", ["Clear", "Lucid", "Obvious"], "medium"),
    ("Vertical", "Horizontal", ["Upright", "Erect", "Standing"], "medium"),
    ("Wealthy", "Poor", ["Rich", "Affluent", "Prosperous"], "easy"),
]

SPELLING: list[tuple[str, list[str], str]] = [
    ("Accommodation", ["Accomodation", "Acommodation", "Accomadation"], "medium"),
    ("Occurrence", ["Occurence", "Ocurrence", "Occurrance"], "medium"),
    ("Receive", ["Recieve", "Receeve", "Receve"], "medium"),
    ("Separate", ["Seperate", "Sepparate", "Seperete"], "medium"),
    ("Necessary", ["Neccessary", "Necesary", "Neccesary"], "medium"),
    ("Embarrass", ["Embarass", "Embarras", "Embaras"], "medium"),
    ("Maintenance", ["Maintainance", "Maintenence", "Maintenaince"], "hard"),
    ("Privilege", ["Priviledge", "Privilage", "Privelege"], "hard"),
    ("Rhythm", ["Rythm", "Rhytm", "Rhythem"], "hard"),
    ("Committee", ["Comittee", "Commitee", "Comitee"], "medium"),
    ("Definite", ["Definate", "Definately", "Definete"], "easy"),
    ("Environment", ["Enviroment", "Environmant", "Enviornment"], "medium"),
    ("Government", ["Goverment", "Governmant", "Govermnent"], "easy"),
    ("Independent", ["Independant", "Indipendent", "Independante"], "medium"),
    ("Knowledge", ["Knowlege", "Knowlede", "Knowladge"], "easy"),
    ("Parallel", ["Paralel", "Parrallel", "Paralell"], "hard"),
    ("Recommend", ["Reccomend", "Recomend", "Reccommend"], "medium"),
    ("Successful", ["Succesful", "Successfull", "Sucessful"], "easy"),
    ("Tomorrow", ["Tommorrow", "Tommorow", "Tomorow"], "easy"),
    ("Written", ["Writen", "Writtin", "Wriiten"], "easy"),
]

PLURALS: list[tuple[str, str, list[str], str]] = [
    ("child", "children", ["childs", "childes", "childrens"], "easy"),
    ("mouse", "mice", ["mouses", "mouse", "mices"], "easy"),
    ("leaf", "leaves", ["leafs", "leafes", "leavs"], "easy"),
    ("woman", "women", ["womans", "womens", "womanes"], "easy"),
    ("foot", "feet", ["foots", "feets", "foot"], "easy"),
    ("tooth", "teeth", ["tooths", "teeths", "tooth"], "easy"),
    ("goose", "geese", ["gooses", "geeses", "goose"], "medium"),
    ("man", "men", ["mans", "mens", "manes"], "easy"),
    ("person", "people", ["persons", "peoples", "persones"], "medium"),
    ("datum", "data", ["datums", "datas", "datum"], "hard"),
    ("criterion", "criteria", ["criterions", "criterias", "criterion"], "hard"),
    ("analysis", "analyses", ["analysises", "analysis", "analysises"], "hard"),
    ("thesis", "theses", ["thesises", "thesis", "thesies"], "hard"),
    ("ox", "oxen", ["oxes", "oxs", "oxens"], "medium"),
    ("knife", "knives", ["knifes", "knifves", "knive"], "medium"),
]

PAST_TENSE: list[tuple[str, str, list[str], str]] = [
    ("go", "went", ["goed", "gone", "going"], "easy"),
    ("eat", "ate", ["eat", "eaten", "eating"], "easy"),
    ("see", "saw", ["seen", "see", "seeing"], "easy"),
    ("write", "wrote", ["write", "written", "writing"], "easy"),
    ("break", "broke", ["breaked", "broken", "breaking"], "easy"),
    ("choose", "chose", ["choosed", "chosen", "choosing"], "medium"),
    ("drive", "drove", ["drived", "driven", "driving"], "easy"),
    ("fly", "flew", ["flied", "flown", "flying"], "medium"),
    ("give", "gave", ["gived", "given", "giving"], "easy"),
    ("know", "knew", ["knowed", "known", "knowing"], "easy"),
    ("speak", "spoke", ["speaked", "spoken", "speaking"], "easy"),
    ("take", "took", ["taked", "taken", "taking"], "easy"),
    ("think", "thought", ["thinked", "thinking", "thinks"], "easy"),
    ("bring", "brought", ["bringed", "bringing", "brings"], "medium"),
    ("catch", "caught", ["catched", "catching", "catches"], "medium"),
]

HOMOPHONES: list[tuple[str, str, list[str], str]] = [
    ("I can ___ the bell.", "hear", ["here", "hair", "hare"], "easy"),
    ("We ___ going to the park.", "are", ["our", "hour", "or"], "easy"),
    ("The ___ is shining brightly.", "sun", ["son", "soon", "sin"], "easy"),
    ("She ___ a letter yesterday.", "wrote", ["right", "rote", "wright"], "easy"),
    ("They ___ their homework.", "did", ["deed", "dead", "dad"], "easy"),
    ("He ___ the ball over the fence.", "threw", ["through", "thru", "true"], "medium"),
    ("The ship set ___ at dawn.", "sail", ["sale", "seal", "sole"], "medium"),
    ("Please be ___ to animals.", "kind", ["mined", "kinned", "caned"], "hard"),
]

GRAMMAR_FILL: list[tuple[str, str, list[str], str]] = [
    ("She ___ to school every day.", "goes", ["go", "going", "gone"], "easy"),
    ("They ___ playing cricket now.", "are", ["is", "was", "has"], "easy"),
    ("I have lived here ___ 2010.", "since", ["for", "from", "by"], "easy"),
    ("He is taller ___ his brother.", "than", ["then", "that", "from"], "easy"),
    ("Neither of the boys ___ present.", "is", ["are", "were", "have"], "medium"),
    ("The news ___ shocking.", "is", ["are", "were", "have"], "medium"),
    ("I look forward ___ meeting you.", "to", ["for", "at", "in"], "medium"),
    ("She is good ___ mathematics.", "at", ["on", "for", "in"], "easy"),
    ("He speaks English ___ fluently.", "very", ["much", "many", "more"], "easy"),
    ("If it rains, we ___ stay home.", "will", ["had", "would", "have"], "medium"),
    ("She has ___ finished her homework.", "already", ["yet", "since", "for"], "easy"),
    ("He is allergic ___ dust.", "to", ["of", "with", "from"], "medium"),
    ("Neither the students nor the teacher ___ present.", "was", ["have", "are", "were"], "medium"),
    ("Choose the correct form: Neither of them ___ ready.", "is", ["have", "are", "were"], "medium"),
]

PARTS_OF_SPEECH: list[tuple[str, str, list[str], str]] = [
    ("Which word is a noun?", "Happiness", ["Quickly", "Run", "Beautiful"], "medium"),
    ("Which is an adjective?", "Beautiful", ["Quickly", "Run", "Happiness"], "easy"),
    ("Which is an adverb?", "Quickly", ["Quick", "Speed", "Runner"], "easy"),
    ("Which is a pronoun?", "He", ["Book", "Run", "Blue"], "easy"),
    ("Which word is a verb?", "Run", ["Table", "Beauty", "Kindness"], "easy"),
    ("Which is a conjunction?", "And", ["Run", "Beautiful", "Quickly"], "easy"),
    ("Which is a preposition?", "Under", ["Jump", "Happy", "Swiftly"], "medium"),
    ("Which is an interjection?", "Alas", ["Table", "Quickly", "Running"], "hard"),
]

SENTENCES: list[tuple[str, str, list[str], str]] = [
    ("Which is a correct sentence?", "He doesn't like tea", ["He don't like tea", "He not like tea", "He doesn't likes tea"], "easy"),
    ("Choose the correct sentence?", "She goes to school", ["She go to school", "She going to school", "She gone to school"], "easy"),
    ("Which sentence is in passive voice?", "Rice is eaten by Ram", ["Ram eats rice", "Ram is eating", "Ram ate rice"], "medium"),
    ("Which sentence uses the correct article?", "An honest man", ["The honest man", "A honest man", "Honest a man"], "medium"),
    ("Choose the correct indirect speech: He said, 'I am tired.'", "He said that he was tired.", ["He said he is tired.", "He says he was tired.", "He said that I am tired."], "hard"),
]


def generate_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []

    for word, ans, wrong, diff in SYNONYMS:
        add_candidate(out, existing, rng, f"Choose the correct synonym of '{word}'.", ans, wrong, diff)
        add_candidate(out, existing, rng, f"Synonym of '{word}' is?", ans, wrong, diff)

    for word, ans, wrong, diff in ANTONYMS:
        add_candidate(out, existing, rng, f"The antonym of '{word}' is?", ans, wrong, diff)
        add_candidate(out, existing, rng, f"Choose the antonym of '{word}'.", ans, wrong, diff)

    for correct, wrong, diff in SPELLING:
        add_candidate(out, existing, rng, "Choose the correctly spelled word.", correct, wrong, diff)
        add_candidate(out, existing, rng, f"Which spelling is correct for the word meaning '{correct.lower()}'?", correct, wrong, diff)

    for sing, ans, wrong, diff in PLURALS:
        add_candidate(out, existing, rng, f"The plural of '{sing}' is?", ans, wrong, diff)
        add_candidate(out, existing, rng, f"Choose the correct plural of '{sing}'.", ans, wrong, diff)

    for verb, ans, wrong, diff in PAST_TENSE:
        add_candidate(out, existing, rng, f"Past tense of '{verb}' is?", ans, wrong, diff)
        add_candidate(out, existing, rng, f"What is the past tense of '{verb}'?", ans, wrong, diff)

    for stem, ans, wrong, diff in HOMOPHONES:
        add_candidate(out, existing, rng, f"Fill in: {stem}", ans, wrong, diff)

    for stem, ans, wrong, diff in GRAMMAR_FILL:
        add_candidate(out, existing, rng, f"Fill in: {stem}", ans, wrong, diff)

    for q, ans, wrong, diff in PARTS_OF_SPEECH + SENTENCES:
        add_candidate(out, existing, rng, q, ans, wrong, diff)

    # One-word meaning (PSC style)
    meanings = [
        ("Benevolent", "kind", ["cruel", "lazy", "harsh"], "medium"),
        ("Candid", "honest", ["secretive", "vague", "deceptive"], "medium"),
        ("Diligent", "hardworking", ["lazy", "idle", "slow"], "medium"),
        ("Fragile", "easily broken", ["strong", "hard", "tough"], "medium"),
        ("Hinder", "obstruct", ["help", "assist", "aid"], "medium"),
        ("Immaculate", "perfectly clean", ["dirty", "stained", "messy"], "medium"),
        ("Jubilant", "very joyful", ["sad", "gloomy", "angry"], "medium"),
        ("Lethargic", "sluggish", ["active", "energetic", "lively"], "medium"),
        ("Nostalgia", "longing for the past", ["fear", "anger", "hunger"], "hard"),
        ("Scrutinize", "examine closely", ["ignore", "overlook", "neglect"], "hard"),
    ]
    for word, ans, wrong, diff in meanings:
        add_candidate(out, existing, rng, f"Meaning of '{word}' is?", ans, wrong, diff)

    return out
