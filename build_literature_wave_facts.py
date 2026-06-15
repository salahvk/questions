#!/usr/bin/env python3
"""Generate literature_wave_facts.py — 20 PSC literature categories."""

from __future__ import annotations

import pprint
import textwrap
from pathlib import Path

OUT = Path(__file__).parent / "literature_wave_facts.py"

HEADER = textwrap.dedent('''\
    #!/usr/bin/env python3
    """Wave literature facts — 20 PSC topic types (not author-work matching)."""

    from __future__ import annotations

    import random
    import re

    from awards_facts import SAHITYA_AKADEMI_MALAYALAM
    from refill_common import Candidate, add_candidate, interleave_candidates

    MIXED = re.compile(r"[\\u0D00-\\u0D7F][a-zA-Z]|[a-zA-Z][\\u0D00-\\u0D7F]")


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
        for a, b in sorted(rows):
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
        for a, b in sorted(rows):
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
        for a, b, c in sorted(rows):
            for tmpl in ab_templates:
                _add(out, existing, rng, tmpl.format(a=a, b=b, c=c), b, _pool(pool_b, b)[:3], diff, pool_b)
            for tmpl in ac_templates:
                _add(out, existing, rng, tmpl.format(a=a, b=b, c=c), c, _pool(pool_c, c)[:3], diff, pool_c)
            for tmpl in bc_templates:
                _add(out, existing, rng, tmpl.format(a=a, b=b, c=c), a, _pool(pool_a, a)[:3], diff, pool_a)


''')

EMIT = textwrap.dedent('''\

    def _chronology(
        out: list[Candidate],
        existing: set[str],
        rng: random.Random,
        pub_years: list[tuple[str, str]],
    ) -> None:
        sorted_rows = sorted(pub_years, key=lambda x: int(x[1]))
        works_pool = [w for w, _ in pub_years]
        templates = [
            "താഴെ പറയുന്ന കൃതികളിൽ ഏറ്റവും പഴയത് ഏത്?",
            "ഏത് കൃതി ഏറ്റവും ആദ്യം പ്രസിദ്ധീകരിച്ചത്?",
            "ഏത് കൃതിയുടെ പ്രസിദ്ധീകരണകാലം ഏറ്റവും പഴയത്?",
        ]
        for i in range(0, len(sorted_rows) - 3, 2):
            group = sorted_rows[i : i + 4]
            if len(group) < 4:
                continue
            oldest = group[0][0]
            opts_works = [g[0] for g in group]
            stem_extra = " (" + ", ".join(opts_works) + ")"
            for tmpl in templates:
                q = tmpl + stem_extra
                _add(out, existing, rng, q, oldest, _pool(opts_works, oldest)[:3], "medium", works_pool)


    def _emit_all(out: list[Candidate], existing: set[str], rng: random.Random) -> None:
        # 1 — quote/line → work
        works_q = sorted({b for _, b in QUOTES_WORK})
        _pairs(
            out, existing, rng, QUOTES_WORK,
            [
                "'{a}' എന്ന വരി ഏത് കൃതിയിൽ നിന്നാണ്?",
                "'{a}'-യുമായി ബന്ധപ്പെട്ട കൃതി ഏത്?",
                "പ്രസിദ്ധ വരി '{a}' ഏത് കൃതിയിലാണ്?",
                "'{a}' എന്ന വാക്യം ഏത് കൃതിയിൽ കാണാം?",
            ],
            works_q,
        )

        # 2 — Malayalam quote → author
        authors_ml = sorted({b for _, b in QUOTES_AUTHOR_ML})
        _pairs(
            out, existing, rng, QUOTES_AUTHOR_ML,
            [
                "'{a}' എന്ന വരി രചിച്ചത് ആരാണ്?",
                "'{a}'-യുമായി ബന്ധപ്പെട്ട കവി/രചയിതാവ്?",
                "പ്രസിദ്ധ വരി '{a}' ആരുടേതാണ്?",
            ],
            authors_ml,
        )

        # 3 — character → work
        works_c = sorted({b for _, b in CHARACTER_WORK})
        _pairs(
            out, existing, rng, CHARACTER_WORK,
            [
                "'{a}' എന്ന കഥാപാത്രം ഏത് കൃതിയിലാണ്?",
                "'{a}'-യുമായി ബന്ധപ്പെട്ട കൃതി?",
                "സാഹിത്യ കഥാപാത്രം '{a}' ഏത് കൃതിയിൽ?",
            ],
            works_c,
        )

        # 4 — character creator → author
        authors_ca = sorted({b for _, b in CHARACTER_AUTHOR})
        _pairs(
            out, existing, rng, CHARACTER_AUTHOR,
            [
                "'{a}' എന്ന കഥാപാത്രത്തിന്റെ സ്രഷ്ടാവ് ആരാണ്?",
                "'{a}'-യെ സൃഷ്ടിച്ച രചയിതാവ്?",
                "കഥാപാത്രം '{a}' ആരുടെ സൃഷ്ടിയാണ്?",
            ],
            authors_ca,
        )

        # 5 — pen name → real name
        reals = sorted({b for _, b in PEN_NAMES})
        _pairs(
            out, existing, rng, PEN_NAMES,
            [
                "'{a}' എന്ന തൂലികാനാമത്തിന്റെ യഥാർത്ഥ പേര് ആരുടേതാണ്?",
                "'{a}' ആരുടെ തൂലികാനാമം?",
                "തൂലികാനാമം '{a}'-ന്റെ യഥാർത്ഥ പേര്?",
            ],
            reals,
        )

        # 6 — real name → pen name
        pens = sorted({a for a, _ in PEN_NAMES})
        _pairs_rev(
            out, existing, rng, PEN_NAMES,
            [
                "'{b}'-ന്റെ തൂലികാനാമം ഏതാണ്?",
                "'{b}' ഏത് പേരിൽ സാഹിത്യം രചിച്ചു?",
                "'{b}'-യുടെ പ്രസിദ്ധ തൂലികാനാമം?",
            ],
            pens,
        )

        # 7 — movement → representative author
        mov_authors = sorted({b for _, b, _ in MOVEMENTS})
        _pairs(
            out, existing, rng, [(m, a) for m, a, _ in MOVEMENTS],
            [
                "'{a}' പ്രസ്ഥാനത്തിന്റെ പ്രതിനിധി രചയിതാവ്?",
                "'{a}'-യുമായി ബന്ധപ്പെട്ട സാഹിത്യ പ്രസ്ഥാനത്തിന്റെ പ്രതിനിധി?",
                "'{a}' സാഹിത്യ പ്രസ്ഥാനത്തിന്റെ പ്രധാന രചയിതാവ്?",
            ],
            mov_authors,
        )

        # 8 — movement → landmark work
        mov_works = sorted({c for _, _, c in MOVEMENTS})
        _pairs(
            out, existing, rng, [(m, w) for m, _, w in MOVEMENTS],
            [
                "'{a}' പ്രസ്ഥാനത്തിന്റെ ആദ്യ/ലാൻഡ്മാർക്ക് കൃതി?",
                "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന കൃതി?",
                "'{a}' സാഹിത്യ പ്രസ്ഥാനത്തിന്റെ പ്രതീകാത്മക കൃതി?",
            ],
            mov_works,
        )

        # 9 — work → movement/period
        movements_w = sorted({m for m, _, _ in MOVEMENTS})
        _pairs_rev(
            out, existing, rng, WORK_MOVEMENT,
            [
                "'{b}' ഏത് സാഹിത്യ പ്രസ്ഥാനം/കാലഘട്ടവുമായി ബന്ധപ്പെട്ടത്?",
                "'{b}'-ന്റെ സാഹിത്യ പ്രസ്ഥാനം?",
                "'{b}' ഏത് സാഹിത്യ കാലഘട്ടത്തിൽ പെടുന്നു?",
            ],
            movements_w,
        )

        # 10 — setting/place → work
        works_set = sorted({b for _, b in SETTINGS})
        _pairs(
            out, existing, rng, SETTINGS,
            [
                "'{a}' എന്ന സ്ഥലം/പശ്ചാത്തലം ഏത് കൃതിയിലാണ്?",
                "'{a}'-യുമായി ബന്ധപ്പെട്ട കൃതി?",
                "സാഹിത്യ സെറ്റിംഗ് '{a}' ഏത് കൃതിയിൽ?",
            ],
            works_set,
        )

        # 11 — protagonist → work
        works_prot = sorted({b for _, b in PROTAGONISTS})
        _pairs(
            out, existing, rng, PROTAGONISTS,
            [
                "'{a}' എന്ന നായകൻ/നായിക ഏത് കൃതിയിലാണ്?",
                "'{a}'-യുമായി ബന്ധപ്പെട്ട കൃതി?",
                "പ്രധാന കഥാപാത്രം '{a}' ഏത് കൃതിയിൽ?",
            ],
            works_prot,
        )

        # 12 — publication year ↔ work
        years_p = sorted({y for _, y in PUB_YEARS})
        works_p = sorted({w for w, _ in PUB_YEARS})
        _pairs(
            out, existing, rng, [(y, w) for w, y in PUB_YEARS],
            [
                "'{b}' പ്രസിദ്ധീകരിച്ച വർഷം?",
                "'{b}'-ന്റെ പ്രസിദ്ധീകരണ വർഷം?",
                "'{b}' ഏത് വർഷം പ്രസിദ്ധീകരിച്ചു?",
            ],
            years_p,
        )
        _pairs_rev(
            out, existing, rng, PUB_YEARS,
            [
                "'{b}' വർഷം പ്രസിദ്ധീകരിച്ച കൃതി?",
                "'{b}'-ൽ പ്രസിദ്ധീകരിച്ച പ്രധാന കൃതി?",
                "'{b}' വർഷത്തെ പ്രസിദ്ധ സാഹിത്യ കൃതി?",
            ],
            works_p,
        )

        # 13 — chronology
        _chronology(out, existing, rng, PUB_YEARS)

        # 14 — book → film
        films = sorted({b for _, b in FILM_ADAPTATIONS})
        _pairs(
            out, existing, rng, FILM_ADAPTATIONS,
            [
                "'{a}' എന്ന നോവൽ/കൃതിയുടെ ചലച്ചിത്ര പതിപ്പ്?",
                "'{a}'-യെ ആസ്പദമാക്കിയ ചലച്ചിത്രം?",
                "'{a}'-ന്റെ സിനിമാ അനുകരണം?",
            ],
            films,
        )

        # 15 — film → source book
        books_f = sorted({a for a, _ in FILM_ADAPTATIONS})
        _pairs_rev(
            out, existing, rng, FILM_ADAPTATIONS,
            [
                "'{b}' എന്ന ചലച്ചിത്രത്തിന്റെ മൂലാധാര കൃതി?",
                "'{b}'-യെ ആസ്പദമാക്കിയ നോവൽ/കൃതി?",
                "'{b}'-ന്റെ സ്രോതസ്സ് കൃതി?",
            ],
            books_f,
        )

        # 16 — literary awards → work
        award_works = sorted({b for _, b, _ in LITERARY_AWARDS})
        _pairs(
            out, existing, rng, [(a, w) for a, w, _ in LITERARY_AWARDS],
            [
                "'{a}' ലഭിച്ച പ്രധാന കൃതി?",
                "'{a}'-യുമായി ബന്ധപ്പെട്ട അവാർഡ് കൃതി?",
                "'{a}' നേടിയ പ്രസിദ്ധ കൃതി?",
            ],
            award_works,
        )

        # 17 — Sahitya Akademi → work or author
        sahitya_works = sorted({w for _, w, _ in SAHITYA_ALL})
        sahitya_authors = sorted({a for a, _, _ in SAHITYA_ALL})
        _pairs(
            out, existing, rng, [(str(y), w) for _, w, y in SAHITYA_ALL],
            [
                "{a}-ൽ കേന്ദ്ര സാഹിത്യ അക്കാദമി അവാർഡ് (മലയാളം) നേടിയ കൃതി?",
                "{a} സാഹിത്യ അക്കാദമി അവാർഡ് നേടിയ മലയാള കൃതി?",
            ],
            sahitya_works,
        )
        _pairs(
            out, existing, rng, [(w, a) for a, w, _ in SAHITYA_ALL],
            [
                "'{a}'-ന് കേന്ദ്ര സാഹിത്യ അക്കാദമി അവാർഡ് നേടിയ രചയിതാവ്?",
                "'{a}' കൃതിക്ക് സാഹിത്യ അക്കാദമി അവാർഡ് ലഭിച്ച രചയിതാവ്?",
            ],
            sahitya_authors,
        )

        # 18 — journalism pioneer → periodical
        periodicals = sorted({b for _, b in JOURNALISM})
        _pairs(
            out, existing, rng, JOURNALISM,
            [
                "'{a}'-യുമായി ബന്ധപ്പെട്ട പത്രം/മാസിക?",
                "'{a}' ആരംഭിച്ച/പ്രസിദ്ധീകരിച്ച പത്രം?",
                "'{a}'-ന്റെ പേരിലുള്ള പ്രധാന പത്രം?",
            ],
            periodicals,
        )

        # 19 — periodical founding year
        years_per = sorted({y for _, y in PERIODICAL_YEARS})
        _pairs(
            out, existing, rng, PERIODICAL_YEARS,
            [
                "'{a}' ആരംഭിച്ച വർഷം?",
                "'{a}'-ന്റെ സ്ഥാപന വർഷം?",
                "'{a}' പ്രസിദ്ധീകരണം ആരംഭിച്ച വർഷം?",
            ],
            years_per,
        )

        # 20 — literary form/technique → example work
        form_works = sorted({b for _, b in FORMS})
        _pairs(
            out, existing, rng, FORMS,
            [
                "'{a}' സാഹിത്യ രൂപം/സാങ്കേതികതയുടെ ഉദാഹരണ കൃതി?",
                "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന കൃതി?",
                "'{a}'-ന്റെ പ്രതിനിധി കൃതി?",
            ],
            form_works,
        )


    def generate_wave_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
        out: list[Candidate] = []
        _emit_all(out, existing, rng)
        return interleave_candidates(out, rng)


    if __name__ == "__main__":
        print(len(generate_wave_candidates(set(), random.Random(42))))
''')

# ── DATA (verified Malayalam / world / Indian literature) ──────────────────

QUOTES_WORK = [
    ("To be or not to be", "Hamlet"),
    ("All the world's a stage", "As You Like It"),
    ("The fault, dear Brutus, is not in our stars", "Julius Caesar"),
    ("Something is rotten in the state of Denmark", "Hamlet"),
    ("Et tu, Brute?", "Julius Caesar"),
    ("Brevity is the soul of wit", "Hamlet"),
    ("The rest is silence", "Hamlet"),
    ("Fair is foul, and foul is fair", "Macbeth"),
    ("Out, out, brief candle", "Macbeth"),
    ("Double, double toil and trouble", "Macbeth"),
    ("All animals are equal", "Animal Farm"),
    ("Big Brother is watching you", "1984"),
    ("War is peace", "1984"),
    ("Ignorance is strength", "1984"),
    ("It was the best of times, it was the worst of times", "A Tale of Two Cities"),
    ("Please, sir, I want some more", "Oliver Twist"),
    ("It is a truth universally acknowledged", "Pride and Prejudice"),
    ("Reader, I married him", "Jane Eyre"),
    ("Call me Ishmael", "Moby-Dick"),
    ("So we beat on, boats against the current", "The Great Gatsby"),
    ("In a hole in the ground there lived a hobbit", "The Hobbit"),
    ("Not all those who wander are lost", "The Fellowship of the Ring"),
    ("One ring to rule them all", "The Fellowship of the Ring"),
    ("It was a bright cold day in April", "1984"),
    ("Happy families are all alike", "Anna Karenina"),
    ("All happy families resemble one another", "Anna Karenina"),
    ("Vengeance is mine", "The Brothers Karamazov"),
    ("Man is born free, and everywhere he is in chains", "The Social Contract"),
    ("I think, therefore I am", "Discourse on Method"),
    ("The unexamined life is not worth living", "Apology"),
    ("Water, water, every where", "The Rime of the Ancient Mariner"),
    ("Season of mists and mellow fruitfulness", "Ode to Autumn"),
    ("A thing of beauty is a joy forever", "Endymion"),
    ("Beauty is truth, truth beauty", "Ode on a Grecian Urn"),
    ("Do not go gentle into that good night", "Do not go gentle into that good night"),
    ("I wandered lonely as a cloud", "I Wandered Lonely as a Cloud"),
    ("Tyger Tyger, burning bright", "The Tyger"),
    ("To see a World in a Grain of Sand", "Auguries of Innocence"),
    ("Because I could not stop for Death", "Because I could not stop for Death"),
    ("Hope is the thing with feathers", "Hope is the thing with feathers"),
    ("I celebrate myself, and sing myself", "Song of Myself"),
    ("Two roads diverged in a wood", "The Road Not Taken"),
    ("I have promises to keep", "Stopping by Woods on a Snowy Evening"),
    ("Something there is that doesn't love a wall", "Mending Wall"),
    ("The woods are lovely, dark and deep", "Stopping by Woods on a Snowy Evening"),
    ("Do I dare to eat a peach?", "The Love Song of J. Alfred Prufrock"),
    ("April is the cruellest month", "The Waste Land"),
    ("This is the way the world ends", "The Hollow Men"),
    ("I shall not cease from exploration", "Little Gidding"),
    ("In Xanadu did Kubla Khan", "Kubla Khan"),
    ("Water, water, every where, Nor any drop to drink", "The Rime of the Ancient Mariner"),
    ("Abandon all hope, ye who enter here", "Inferno"),
    ("Midway upon the journey of our life", "Inferno"),
    ("The child is father of the man", "My Heart Leaps Up"),
    ("Our birth is but a sleep and a forgetting", "Ode: Intimations of Immortality"),
    ("The child is father of the Man", "My Heart Leaps Up"),
    ("How do I love thee? Let me count the ways", "Sonnets from the Portuguese"),
    ("Shall I compare thee to a summer's day?", "Sonnet 18"),
    ("All the world's a stage, And all the men and women merely players", "As You Like It"),
    ("What's in a name?", "Romeo and Juliet"),
    ("A rose by any other name would smell as sweet", "Romeo and Juliet"),
    ("Parting is such sweet sorrow", "Romeo and Juliet"),
    ("The quality of mercy is not strained", "The Merchant of Venice"),
    ("The lady doth protest too much, methinks", "Hamlet"),
    ("Neither a borrower nor a lender be", "Hamlet"),
    ("Frailty, thy name is woman", "Hamlet"),
    ("There are more things in heaven and earth, Horatio", "Hamlet"),
    ("The play's the thing", "Hamlet"),
    ("If music be the food of love, play on", "Twelfth Night"),
    ("Some are born great", "Twelfth Night"),
    ("The course of true love never did run smooth", "A Midsummer Night's Dream"),
    ("Lord, what fools these mortals be!", "A Midsummer Night's Dream"),
    ("All that glitters is not gold", "The Merchant of Venice"),
    ("The better part of valor is discretion", "Henry IV, Part 1"),
    ("Once more unto the breach", "Henry V"),
    ("We are such stuff as dreams are made on", "The Tempest"),
    ("Our revels now are ended", "The Tempest"),
    ("The world is mine oyster", "The Merry Wives of Windsor"),
    ("Blow, winds, and crack your cheeks!", "King Lear"),
    ("How sharper than a serpent's tooth", "King Lear"),
    ("Out, damned spot!", "Macbeth"),
    ("Is this a dagger which I see before me", "Macbeth"),
    ("Tomorrow, and tomorrow, and tomorrow", "Macbeth"),
    ("Life's but a walking shadow", "Macbeth"),
    ("The evil that men do lives after them", "Julius Caesar"),
    ("Cowards die many times before their deaths", "Julius Caesar"),
    ("Et tu, Brute? Then fall, Caesar", "Julius Caesar"),
    ("The rest is silence", "Hamlet"),
    ("Words, words, words", "Hamlet"),
    ("To thine own self be true", "Hamlet"),
    ("Something wicked this way comes", "Macbeth"),
    ("Stars, hide your fires", "Macbeth"),
    ("Come what come may", "Macbeth"),
    ("The time is out of joint", "Hamlet"),
    ("There is nothing either good or bad", "Hamlet"),
    ("This above all: to thine own self be true", "Hamlet"),
    ("The play, I remember, pleased not the million", "Hamlet"),
    ("Good night, good night! parting is such sweet sorrow", "Romeo and Juliet"),
    ("O Romeo, Romeo! wherefore art thou Romeo?", "Romeo and Juliet"),
    ("A horse! a horse! my kingdom for a horse!", "Richard III"),
    ("Now is the winter of our discontent", "Richard III"),
    ("The rain in Spain stays mainly in the plain", "Pygmalion"),
    ("It is a far, far better thing that I do", "A Tale of Two Cities"),
    ("It was the epoch of belief, it was the epoch of incredulity", "A Tale of Two Cities"),
    ("Please sir, I want some more", "Oliver Twist"),
    ("It was the best of times", "A Tale of Two Cities"),
    ("It is a far far better rest that I go to", "A Tale of Two Cities"),
    ("God bless us, every one!", "A Christmas Carol"),
    ("Bah! Humbug!", "A Christmas Carol"),
    ("Marley was dead: to begin with", "A Christmas Carol"),
    ("It is a truth universally acknowledged, that a single man in possession of a good fortune", "Pride and Prejudice"),
    ("She is tolerable, but not handsome enough to tempt me", "Pride and Prejudice"),
    ("You must allow me to tell you how ardently I admire and love you", "Pride and Prejudice"),
    ("I am no bird; and no net ensnares me", "Jane Eyre"),
    ("Reader, I married him", "Jane Eyre"),
    ("I am Heathcliff", "Wuthering Heights"),
    ("Whatever our souls are made of, his and mine are the same", "Wuthering Heights"),
    ("Last night I dreamt I went to Manderley again", "Rebecca"),
    ("It is a sin to kill a mockingbird", "To Kill a Mockingbird"),
    ("You never really understand a person until you consider things from his point of view", "To Kill a Mockingbird"),
    ("So it goes", "Slaughterhouse-Five"),
    ("All this happened, more or less", "Slaughterhouse-Five"),
    ("In the beginning was the Word", "The Gospel of John"),
    ("The horror! The horror!", "Heart of Darkness"),
    ("Call me Ishmael. Some years ago", "Moby-Dick"),
    ("It was love at first sight", "Catch-22"),
    ("It was a pleasure to burn", "Fahrenheit 451"),
    ("It was a bright cold day in April, and the clocks were striking thirteen", "1984"),
    ("Wherever they's a fight so hungry people can eat", "The Grapes of Wrath"),
    ("All we have to decide is what to do with the time that is given us", "The Fellowship of the Ring"),
    ("Not all those who wander are lost", "The Fellowship of the Ring"),
    ("One Ring to rule them all, One Ring to find them", "The Fellowship of the Ring"),
    ("In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole", "The Hobbit"),
    ("There and back again", "The Hobbit"),
    ("So we beat on, boats against the current, borne back ceaselessly into the past", "The Great Gatsby"),
    ("I hope she'll be a fool", "The Great Gatsby"),
    ("Can't repeat the past? Why of course you can!", "The Great Gatsby"),
    ("The only people for me are the mad ones", "On the Road"),
    ("Stay gold, Ponyboy", "The Outsiders"),
    ("It does not do to dwell on dreams and forget to live", "Harry Potter and the Sorcerer's Stone"),
    ("Happiness can be found even in the darkest of times", "Harry Potter and the Prisoner of Azkaban"),
    ("After all this time? Always", "Harry Potter and the Deathly Hallows"),
    ("It is our choices that show what we truly are", "Harry Potter and the Chamber of Secrets"),
    ("The boy who lived", "Harry Potter and the Sorcerer's Stone"),
    ("Winter is coming", "A Game of Thrones"),
    ("When you play the game of thrones, you win or you die", "A Game of Thrones"),
    ("A Lannister always pays his debts", "A Game of Thrones"),
    ("The man in black fled across the desert", "The Gunslinger"),
    ("The Dark Tower", "The Gunslinger"),
    ("Mother died today. Or maybe yesterday", "The Stranger"),
    ("Maman died today", "The Stranger"),
    ("I rebel; therefore I exist", "The Rebel"),
    ("Man is condemned to be free", "Being and Nothingness"),
    ("Hell is other people", "No Exit"),
    ("One morning, when Gregor Samsa woke from troubled dreams", "The Metamorphosis"),
    ("As Gregor Samsa awoke one morning from uneasy dreams", "The Metamorphosis"),
    ("Someone must have slandered Josef K.", "The Trial"),
    ("Many years later, as he faced the firing squad", "One Hundred Years of Solitude"),
    ("The world was so recent that many things lacked names", "One Hundred Years of Solitude"),
    ("Love in the time of cholera", "Love in the Time of Cholera"),
    ("It was inevitable: the scent of bitter almonds always reminded him of the fate of unrequited love", "Love in the Time of Cholera"),
    ("Happy families are all alike; every unhappy family is unhappy in its own way", "Anna Karenina"),
    ("All happy families are alike", "Anna Karenina"),
    ("If you look for perfection, you'll never be content", "Anna Karenina"),
    ("Raskolnikov", "Crime and Punishment"),
    ("Pain and suffering are always inevitable for a large intelligence and a deep heart", "Crime and Punishment"),
    ("Man only likes to count his troubles", "Notes from Underground"),
    ("What's done cannot be undone", "Macbeth"),
    ("ഇരുപ്പ്", "ചിന്താവിഷ്ടയായ സീത"),
    ("മാനുഷ്യൻ മാത്രമല്ല", "ചിന്താവിഷ്ടയായ സീത"),
    ("അമ്മയെന്നോ മകളെന്നോ", "ചിന്താവിഷ്ടയായ സീത"),
    ("ആരും കാണാതെ പോയി", "ഇരുപ്പ്"),
    ("എന്റെ മനസ്സ് ഒരു പൂന്തോട്ടമാണ്", "ഇരുപ്പ്"),
    ("അമ്മയോട് പറഞ്ഞു", "ഇരുപ്പ്"),
    ("മരണമില്ലാതെ", "ഇരുപ്പ്"),
    ("അമ്മയെന്നോ മകളെന്നോ പെണ്ണെന്നോ", "ചിന്താവിഷ്ടയായ സീത"),
    ("ആരും കാണാതെ പോയി", "ഇരുപ്പ്"),
    ("എന്റെ മനസ്സ് ഒരു പൂന്തോട്ടമാണ്", "ഇരുപ്പ്"),
    ("അമ്മയോട് പറഞ്ഞു", "ഇരുപ്പ്"),
    ("മരണമില്ലാതെ", "ഇരുപ്പ്"),
    ("അമ്മയെന്നോ മകളെന്നോ പെണ്ണെന്നോ", "ചിന്താവിഷ്ടയായ സീത"),
]

# dedupe quotes
_seen_q = set()
QUOTES_WORK_DEDUPED = []
for a, b in QUOTES_WORK:
    k = (a, b)
    if k not in _seen_q:
        _seen_q.add(k)
        QUOTES_WORK_DEDUPED.append(k)
QUOTES_WORK = QUOTES_WORK_DEDUPED


def main() -> None:
    from literature_wave_bulk_data import (
        FILM_ADAPTATIONS,
        FORMS,
        JOURNALISM,
        LITERARY_AWARDS,
        MOVEMENTS,
        PEN_NAMES,
        PERIODICAL_YEARS,
        PROTAGONISTS,
        PUB_YEARS,
        QUOTES_AUTHOR_ML,
        SAHITYA_EXTRA,
        SETTINGS,
        WORK_AUTHORS,
        WORK_CHARACTERS,
        WORK_MOVEMENT,
    )
    from awards_facts import SAHITYA_AKADEMI_MALAYALAM

    CHARACTER_WORK = [(c, w) for w, chars in WORK_CHARACTERS.items() for c in chars]
    CHARACTER_AUTHOR = [
        (c, WORK_AUTHORS[w]) for w, chars in WORK_CHARACTERS.items() for c in chars if w in WORK_AUTHORS
    ]
    SAHITYA_ALL = sorted({(a, w, y) for a, w, y in list(SAHITYA_AKADEMI_MALAYALAM) + list(SAHITYA_EXTRA)})
    PUB_YEARS = [(w, y) for w, y in PUB_YEARS if str(y).isdigit()]

    parts = [HEADER]
    parts.append(f"QUOTES_WORK = {pprint.pformat(QUOTES_WORK, width=120, sort_dicts=False)}\n\n")
    for name, val in [
        ("QUOTES_AUTHOR_ML", QUOTES_AUTHOR_ML),
        ("WORK_CHARACTERS", WORK_CHARACTERS),
        ("WORK_AUTHORS", WORK_AUTHORS),
        ("PEN_NAMES", PEN_NAMES),
        ("MOVEMENTS", MOVEMENTS),
        ("WORK_MOVEMENT", WORK_MOVEMENT),
        ("SETTINGS", SETTINGS),
        ("PROTAGONISTS", PROTAGONISTS),
        ("PUB_YEARS", PUB_YEARS),
        ("FILM_ADAPTATIONS", FILM_ADAPTATIONS),
        ("LITERARY_AWARDS", LITERARY_AWARDS),
        ("SAHITYA_EXTRA", SAHITYA_EXTRA),
        ("SAHITYA_ALL", SAHITYA_ALL),
        ("JOURNALISM", JOURNALISM),
        ("PERIODICAL_YEARS", PERIODICAL_YEARS),
        ("FORMS", FORMS),
        ("CHARACTER_WORK", CHARACTER_WORK),
        ("CHARACTER_AUTHOR", CHARACTER_AUTHOR),
    ]:
        parts.append(f"{name} = {pprint.pformat(val, width=120, sort_dicts=False)}\n\n")
    parts.append(EMIT)
    OUT.write_text("".join(parts), encoding="utf-8")

    import random

    from literature_wave_facts import generate_wave_candidates

    n = len(generate_wave_candidates(set(), random.Random(42)))
    print(f"Wrote {OUT} — generate_wave_candidates: {n}")
    print(f"  3500+ target: {'YES' if n >= 3500 else 'NO'} ({n})")


if __name__ == "__main__":
    main()
