GENERATE_BLOCK = '''

def _match_pairs(
    out: list[Candidate],
    existing: set[str],
    rng: random.Random,
    rows: list[tuple[str, str]],
    templates: list[str],
    diff: str = "medium",
) -> None:
    pool = [f"{a} — {b}" for a, b in rows]
    for a, b in rows:
        correct = f"{a} — {b}"
        for tmpl in templates:
            _add(
                out,
                existing,
                rng,
                tmpl.format(a=a, b=b, m=correct),
                correct,
                _pool(pool, correct)[:3],
                diff,
                pool,
            )


def generate_wave15_candidates(existing: set[str], rng: random.Random) -> list[Candidate]:
    out: list[Candidate] = []

    saints = list({a for a, _, _ in BHAKTI})
    movements = list({b for _, b, _ in BHAKTI})
    regions = list({c for _, _, c in BHAKTI})
    _triples(
        out,
        existing,
        rng,
        BHAKTI,
        [
            "'{a}' ഏത് ഭക്തി/സൂഫി പ്രസ്ഥാനവുമായി ബന്ധപ്പെട്ട സന്തനാണ്?",
            "'{a}'-ന്റെ പ്രസ്ഥാനം ഏത്?",
            "'{a}' ഏത് ആത്മീയ പരമ്പരയുമായി അറിയപ്പെടുന്നു?",
            "'{b}' പ്രസ്ഥാനവുമായി ബന്ധപ്പെട്ട പ്രധാന വ്യക്തി?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സന്തൻ?",
            "'{a}' ഏത് '{b}' പ്രസ്ഥാനവുമായി ബന്ധപ്പെട്ട്?",
            "'{b}'-യുടെ പ്രതിനിധി '{a}'?",
        ],
        [
            "'{a}' പ്രധാനമായി ഏത് പ്രദേശവുമായി ബന്ധപ്പെട്ട് പ്രവർത്തിച്ചു?",
            "'{a}'-ന്റെ പ്രവർത്തന കേന്ദ്രം?",
            "'{c}' പ്രദേശവുമായി ബന്ധപ്പെട്ട സന്തൻ?",
            "'{c}'-ൽ പ്രധാനമായി പ്രവർത്തിച്ച സന്തൻ?",
        ],
        [
            "'{b}' പ്രസ്ഥാനം '{c}'-ൽ പ്രവർത്തിച്ച പ്രധാന വ്യക്തി?",
            "'{c}'-ലെ '{b}' പ്രസ്ഥാനത്തിന്റെ പ്രതിനിധി?",
            "'{b}'-യുമായി '{c}'-ൽ ബന്ധപ്പെട്ട സന്തൻ?",
            "'{c}' പ്രദേശവുമായി '{b}'-യുമായി ബന്ധപ്പെട്ട സന്തൻ?",
        ],
        movements,
        regions,
        saints,
    )

    builders = list({b for _, b in MONUMENTS})
    monuments = list({a for a, _ in MONUMENTS})
    _pairs(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{a}' നിർമ്മിച്ചത് ആർ?",
            "'{a}'-ന്റെ നിർമ്മാതാവ്/രാജാവ്?",
            "'{a}' നിർമ്മാണവുമായി ബന്ധപ്പെട്ട വ്യക്തി?",
            "'{a}' സ്ഥാപിച്ച/നിർമ്മിച്ച ഭരണാധികാരി?",
            "'{a}'-ന്റെ പിൻബലത്തിൽ നിർമ്മിച്ചത്?",
            "'{a}' നിർമ്മിച്ച പ്രധാന വ്യക്തി?",
            "'{a}'-ന്റെ നിർമ്മാതാവ് ആർ?",
            "'{a}'-യുടെ രചയിതാവ്/നിർമ്മാതാവ്?",
            "'{a}' ആരുടെ കാലത്ത് നിർമ്മിച്ചത്?",
        ],
        builders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{b}' നിർമ്മിച്ച പ്രധാന നിർമ്മാണം?",
            "'{b}'-ന്റെ കാലത്ത് നിർമ്മിച്ച പ്രശസ്ത സ്മാരകം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണം?",
            "'{b}' നിർമ്മിച്ച/കമാൻഡ് ചെയ്ത സ്മാരകം?",
            "'{b}'-ന്റെ പേരിലുള്ള പ്രധാന നിർമ്മാണം?",
        ],
        monuments,
    )

    styles = list({b for _, b in TEMPLE_ARCH})
    temples = list({a for a, _ in TEMPLE_ARCH})
    _pairs(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{a}' ഏത് ശില്പശൈലിയിലാണ്?",
            "'{a}'-ന്റെ വാസ്തുവിദ്യാ ശൈലി?",
            "'{a}' ഏത് നിർമ്മാണശൈലിയിൽ പണിതം?",
            "'{a}'-ന്റെ ശില്പശൈലി?",
            "'{a}' ഏത് ശൈലിയുടെ ഉദാഹരണമാണ്?",
        ],
        styles,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{b}' ശൈലിയിലെ പ്രധാന ഉദാഹരണം?",
            "'{b}'-യുടെ പ്രതിനിധി നിർമ്മാണം?",
            "'{b}' ശൈലിയിൽ പണിത പ്രശസ്ത ക്ഷേത്രം/നിർമ്മാണം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണം?",
        ],
        temples,
    )

    periods = list({b for _, b in TRAVELLERS})
    travellers = list({a for a, _ in TRAVELLERS})
    _pairs(
        out,
        existing,
        rng,
        TRAVELLERS,
        [
            "'{a}' ഏത് കാലഘട്ടവുമായി ബന്ധപ്പെട്ട് ഇന്ത്യ സന്ദർശിച്ചു?",
            "'{a}'-ന്റെ സഞ്ചാര കാലഘട്ടം/ഭരണകാലം?",
            "'{a}' ഇന്ത്യയിൽ എപ്പോൾ/ഏത് കാലത്ത്?",
            "'{a}'-ന്റെ ഇന്ത്യാ സന്ദർശനവുമായി ബന്ധപ്പെട്ട കാലം?",
        ],
        periods,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TRAVELLERS,
        [
            "'{b}' കാലഘട്ടത്തിൽ ഇന്ത്യ സന്ദർശിച്ച പ്രശസ്ത സഞ്ചാരി?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട് ഇന്ത്യ സന്ദർശിച്ചയാൾ?",
            "'{b}'-ൽ സന്ദർശിച്ച പ്രശസ്ത വ്യക്തി?",
        ],
        travellers,
    )

    founders = list({b for _, b in NEWSPAPERS})
    papers = list({a for a, _ in NEWSPAPERS})
    _pairs(
        out,
        existing,
        rng,
        NEWSPAPERS,
        [
            "'{a}' ആരംഭിച്ചത്/പ്രസിദ്ധീകരിച്ചത് ആർ?",
            "'{a}'-ന്റെ സ്ഥാപകൻ/പ്രസിദ്ധീകരണ ഉത്തരവാദി?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി?",
            "'{a}' ആരുടെ പേരിലാണ്?",
        ],
        founders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        NEWSPAPERS,
        [
            "'{b}' ആരംഭിച്ച/പ്രസിദ്ധീകരിച്ച പത്രം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പത്രം?",
            "'{b}'-ന്റെ പേരിലുള്ള പ്രസിദ്ധ പത്രം?",
        ],
        papers,
    )

    years = list({y for _, y, _, _ in REVOLTS})
    rev_regions = list({r for _, _, r, _ in REVOLTS})
    leaders = list({l for _, _, _, l in REVOLTS})
    names = list({n for n, _, _, _ in REVOLTS})
    _quads(
        out,
        existing,
        rng,
        REVOLTS,
        [
            "'{n}' സംഭവിച്ച വർഷം?",
            "'{n}'-ന്റെ പ്രധാന വർഷം?",
            "'{n}'-യുമായി ബന്ധപ്പെട്ട വർഷം?",
        ],
        [
            "'{n}' പ്രധാനമായി ഏത് പ്രദേശത്ത്?",
            "'{n}'-ന്റെ പ്രധാന പ്രദേശം?",
            "'{n}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം?",
        ],
        [
            "'{n}'-ന്റെ നേതാവ്/പ്രധാന വ്യക്തി?",
            "'{n}'-യുമായി ബന്ധപ്പെട്ട നേതാവ്?",
            "'{n}' നയിച്ച/നേതൃത്വം നൽകിയ വ്യക്തി?",
        ],
        [
            "'{l}' നേതൃത്വം നൽകിയ/ബന്ധപ്പെട്ട സംഘടന/സമരം?",
            "'{l}'-യുമായി ബന്ധപ്പെട്ട പ്രധാന സമരം?",
            "'{r}'-ൽ '{l}'-യുമായി ബന്ധപ്പെട്ട സംഘടന?",
        ],
        years,
        rev_regions,
        leaders,
        names,
    )

    lr_terms = list({a for a, _ in LAND_REVENUE})
    lr_facts = list({b for _, b in LAND_REVENUE})
    _pairs(
        out,
        existing,
        rng,
        LAND_REVENUE,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി/കാലം?",
            "'{a}' ആരംഭിച്ച/നടപ്പാക്കിയത്?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
        ],
        lr_facts,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        LAND_REVENUE,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നികുതി/വ്യവസ്ഥ?",
            "'{b}'-ന്റെ പേരിലുള്ള നികുതി വ്യവസ്ഥ?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നികുതി/വ്യവസ്ഥ?",
        ],
        lr_terms,
    )

    ma_terms = list({a for a, _ in MUGHAL_ADMIN})
    ma_facts = list({b for _, b in MUGHAL_ADMIN})
    _pairs(
        out,
        existing,
        rng,
        MUGHAL_ADMIN,
        [
            "'{a}'-ന്റെ അർത്ഥം/വിവരണം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
            "'{a}' എന്തിനെ/ആരെ സൂചിപ്പിക്കുന്നു?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം?",
        ],
        ma_facts,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        MUGHAL_ADMIN,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ഭരണപദം?",
            "'{b}'-ന്റെ പേരിലുള്ള മുഗൾ ഭരണപദം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പദം?",
        ],
        ma_terms,
    )

    coin_names = list({a for a, _ in COINS})
    coin_facts = list({b for _, b in COINS})
    _pairs(
        out,
        existing,
        rng,
        COINS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട കാലം/ഭരണാധികാരി?",
            "'{a}' ഏത് കാലത്ത്/ആരുടെ കാലത്ത്?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം?",
        ],
        coin_facts,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        COINS,
        [
            "'{b}'-ന്റെ കാലത്ത്/പേരിലുള്ള നാണയം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നാണയം?",
        ],
        coin_names,
    )

    places = list({b for _, b in EURO_FACTORIES})
    companies = list({a for a, _ in EURO_FACTORIES})
    _pairs(
        out,
        existing,
        rng,
        EURO_FACTORIES,
        [
            "'{a}'-ന്റെ പ്രധാന ചരക്ക്/വ്യാപാര കേന്ദ്രം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട തുറമുഖ/നഗരം?",
            "'{a}'-ന്റെ പ്രധാന കച്ചവട കേന്ദ്രം?",
        ],
        places,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        EURO_FACTORIES,
        [
            "'{b}'-ൽ സ്ഥാപിച്ച/പ്രവർത്തിച്ച യൂറോപ്യൻ കമ്പനി?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട കച്ചവട കമ്പനി?",
        ],
        companies,
    )

    works = list({b for _, b in REFORMERS})
    reformers = list({a for a, _ in REFORMERS})
    _pairs(
        out,
        existing,
        rng,
        REFORMERS,
        [
            "'{a}'-ന്റെ പ്രധാന പ്രസ്ഥാനം/സംഘടന?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട സാമൂഹിക/മതപരിഷ്കരണ പ്രസ്ഥാനം?",
            "'{a}'-ന്റെ പ്രധാന സംഭാവന?",
        ],
        works,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        REFORMERS,
        [
            "'{b}'-ന്റെ സ്ഥാപകൻ/പ്രധാന വ്യക്തി?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പരിഷ്കരണവാദി?",
        ],
        reformers,
    )

    indus_sites = list({a for a, _ in INDUS})
    indus_facts = list({b for _, b in INDUS})
    _pairs(
        out,
        existing,
        rng,
        INDUS,
        [
            "'{a}'-ന്റെ പ്രധാന സവിശേഷത/വിവരണം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
            "'{a}' എന്തിനെ/എന്തിനെ സൂചിപ്പിക്കുന്നു?",
        ],
        indus_facts,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        INDUS,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സിന്ധു സംസ്കാര സ്ഥലം/കണ്ടെത്തൽ?",
            "'{b}'-ന്റെ പേരിലുള്ള സിന്ധു സംസ്കാര വസ്തു/സ്ഥലം?",
        ],
        indus_sites,
    )

    sangam_works = list({a for a, _ in SANGAM})
    sangam_facts = list({b for _, b in SANGAM})
    _pairs(
        out,
        existing,
        rng,
        SANGAM,
        [
            "'{a}'-ന്റെ പ്രധാന സവിശേഷത/രചയിതാവ്?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വിവരണം?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം?",
        ],
        sangam_facts,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        SANGAM,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സംഗം കൃതി?",
            "'{b}'-ന്റെ പേരിലുള്ള സാഹിത്യ കൃതി?",
        ],
        sangam_works,
    )

    fp_events = list({a for a, _ in FOREIGN_POLICY})
    fp_facts = list({b for _, b in FOREIGN_POLICY})
    _pairs(
        out,
        existing,
        rng,
        FOREIGN_POLICY,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി/രാജ്യം?",
            "'{a}'-ന്റെ പ്രധാന വിവരണം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?",
        ],
        fp_facts,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        FOREIGN_POLICY,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ഉടമ്പടി/നയം?",
            "'{b}'-ന്റെ പേരിലുള്ള നയം/സംഭവം?",
        ],
        fp_events,
    )

    _match_pairs(
        out,
        existing,
        rng,
        MATCH_ROWS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ശരിയായ ജോഡി?",
            "താഴെ കൊടുത്തിരിക്കുന്നവയിൽ '{a}'-ന്റെ ശരിയായ ജോഡി?",
            "'{a}' — ഏത്?",
            "ശരിയായ ജോഡി '{a}' — ?",
            "'{a}'-ന് അനുയോജ്യമായ വിവരണം?",
            "'{a}'-യുടെ ശരിയായ വിവരണം?",
        ],
    )

    _wave15_extra(out, existing, rng)
    _wave15_more(out, existing, rng)
    _wave15_wave4(out, existing, rng)

    return out


def _wave15_wave4(out: list[Candidate], existing: set[str], rng: random.Random) -> None:
    """Fourth template pass — distinct stems for pool depth."""
    saints = list({a for a, _, _ in BHAKTI})
    movements = list({b for _, b, _ in BHAKTI})
    regions = list({c for _, _, c in BHAKTI})
    _triples(
        out,
        existing,
        rng,
        BHAKTI,
        [
            "ഭക്തി/സൂഫി ചരിത്രത്തിൽ '{a}'-ന്റെ പ്രസ്ഥാനം?",
            "'{a}' ഏത് ആത്മീയ പരമ്പരയുമായി ബന്ധപ്പെട്ട്?",
            "'{b}' പ്രസ്ഥാനത്തിന്റെ പ്രധാന സന്ത് '{a}'?",
        ],
        [
            "'{a}' പ്രധാനമായി പ്രവർത്തിച്ച പ്രദേശം?",
            "സന്ത് '{a}'-ന്റെ പ്രവർത്തന കേന്ദ്രം?",
            "'{c}'-യുമായി '{a}'-യെ ബന്ധിപ്പിക്കാം?",
        ],
        [
            "'{c}' പ്രദേശത്ത് '{b}' പ്രസ്ഥാനവുമായി ബന്ധപ്പെട്ടവർ?",
            "'{b}' '{c}'-ൽ പ്രചരിച്ച പ്രധാന വ്യക്തി?",
        ],
        movements,
        regions,
        saints,
    )

    builders = list({b for _, b in MONUMENTS})
    monuments = list({a for a, _ in MONUMENTS})
    _pairs(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "പ്രസിദ്ധ നിർമ്മാണം '{a}' നിർമ്മിച്ചത്?",
            "'{a}' ആരുടെ/ഏത് ഭരണാധികാരിയുടെ കാലത്ത് പണിതം?",
            "ചരിത്ര സ്മാരകം '{a}'-ന്റെ നിർമ്മാതാവ്?",
        ],
        builders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{b}' നിർമ്മിച്ച/കമാൻഡ് ചെയ്ത പ്രസിദ്ധ സ്മാരകം?",
            "'{b}'-യുടെ പേരിൽ അറിയപ്പെടുന്ന നിർമ്മാണം?",
        ],
        monuments,
    )

    styles = list({b for _, b in TEMPLE_ARCH})
    temples = list({a for a, _ in TEMPLE_ARCH})
    _pairs(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{a}' ഏത് വാസ്തുവിദ്യാ/ശില്പശൈലിയിൽ പെടുന്നു?",
            "നിർമ്മാണം '{a}'-ന്റെ ശൈലി?",
        ],
        styles,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{b}' ശൈലിയുടെ ഉദാഹരണമായി '{a}'?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട ക്ഷേത്ര/ഗുഹ?",
        ],
        temples,
    )

    periods = list({b for _, b in TRAVELLERS})
    travellers = list({a for a, _ in TRAVELLERS})
    _pairs(
        out,
        existing,
        rng,
        TRAVELLERS,
        [
            "വിദേശ യാത്രികൻ '{a}' ഇന്ത്യ സന്ദർശിച്ച കാലം?",
            "'{a}'-ന്റെ ഇന്ത്യാ സന്ദർശനം ഏത് കാലഘട്ടവുമായി?",
        ],
        periods,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TRAVELLERS,
        [
            "'{b}' കാലത്ത് ഇന്ത്യ സന്ദർശിച്ച പ്രശസ്ത യാത്രികൻ?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട വിദേശ യാത്രികൻ?",
        ],
        travellers,
    )

    founders = list({b for _, b in NEWSPAPERS})
    papers = list({a for a, _ in NEWSPAPERS})
    _pairs(
        out,
        existing,
        rng,
        NEWSPAPERS,
        [
            "പത്രം '{a}' ആരാണ് ആരംഭിച്ചത്?",
            "'{a}'-യുടെ സ്ഥാപകൻ/പ്രസിദ്ധീകരണ ഉത്തരവാദി?",
        ],
        founders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        NEWSPAPERS,
        [
            "'{b}' ആരംഭിച്ച/പ്രസിദ്ധീകരിച്ച പത്രം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പത്രപ്രസിദ്ധീകരണം?",
        ],
        papers,
    )

    years = list({y for _, y, _, _ in REVOLTS})
    rev_regions = list({r for _, _, r, _ in REVOLTS})
    leaders = list({l for _, _, _, l in REVOLTS})
    names = list({n for n, _, _, _ in REVOLTS})
    _quads(
        out,
        existing,
        rng,
        REVOLTS,
        ["'{n}' നടന്ന/ആരംഭിച്ച വർഷം?", "'{n}'-യുമായി ബന്ധപ്പെട്ട വർഷം?"],
        ["'{n}' പ്രധാനമായി നടന്ന പ്രദേശം?", "'{n}'-യുടെ പ്രദേശം?"],
        ["'{n}'-യുടെ നേതാവ്/പ്രധാന വ്യക്തി?", "'{n}'-യുമായി ബന്ധപ്പെട്ട നേതാവ്?"],
        ["'{l}' നേതൃത്വം നൽകിയ സമരം/സംഘടന?", "'{l}'-യുമായി ബന്ധപ്പെട്ട വിദ്രോഹം?"],
        years,
        rev_regions,
        leaders,
        names,
    )

    for rows, pool_b, pool_a, fwd, rev in (
        (LAND_REVENUE, [b for _, b in LAND_REVENUE], [a for a, _ in LAND_REVENUE],
         "'{a}'-യുമായി ബന്ധപ്പെട്ട നികുതി/ഭൂമി വ്യവസ്ഥ?", "'{b}'-യുമായി ബന്ധപ്പെട്ട നികുതി പദം?"),
        (MUGHAL_ADMIN, [b for _, b in MUGHAL_ADMIN], [a for a, _ in MUGHAL_ADMIN],
         "മുഗൾ ഭരണപദം '{a}'-ന്റെ അർത്ഥം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട ഭരണപദം?"),
        (COINS, [b for _, b in COINS], [a for a, _ in COINS],
         "'{a}'-യുമായി ബന്ധപ്പെട്ട നാണയ/കാലം?", "'{b}'-ന്റെ കാലത്തെ നാണയം?"),
        (EURO_FACTORIES, [b for _, b in EURO_FACTORIES], [a for a, _ in EURO_FACTORIES],
         "'{a}'-ന്റെ പ്രധാന കച്ചവട/തുറമുഖ കേന്ദ്രം?", "'{b}'-യിലെ യൂറോപ്യൻ കച്ചവട കമ്പനി?"),
        (REFORMERS, [b for _, b in REFORMERS], [a for a, _ in REFORMERS],
         "സാമൂഹിക/മതപരിഷ്കരണവാദി '{a}'-ന്റെ പ്രസ്ഥാനം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട പരിഷ്കരണവാദി?"),
        (INDUS, [b for _, b in INDUS], [a for a, _ in INDUS],
         "സിന്ധു സംസ്കാരത്തിൽ '{a}'-ന്റെ പ്രധാന സവിശേഷത?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സിന്ധു സ്ഥലം?"),
        (SANGAM, [b for _, b in SANGAM], [a for a, _ in SANGAM],
         "സംഗം/പുരാതന സാഹിത്യത്തിൽ '{a}'-ന്റെ വിവരണം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട കൃതി?"),
        (FOREIGN_POLICY, [b for _, b in FOREIGN_POLICY], [a for a, _ in FOREIGN_POLICY],
         "'{a}'-യുമായി ബന്ധപ്പെട്ട രാജ്യം/വിവരണം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട നയം/ഉടമ്പടി?"),
    ):
        _pairs(out, existing, rng, rows, [fwd], pool_b)
        _pairs_rev(out, existing, rng, rows, [rev], pool_a)

    _match_pairs(
        out,
        existing,
        rng,
        MATCH_ROWS,
        [
            "താഴെപ്പറയുന്നവയിൽ '{a}'-യുമായി ശരിയായി ജോഡിച്ചത്?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ശരിയായ ജോഡി ഏത്?",
            "'{a}' — ശരിയായ വിവരണം?",
        ],
    )


def _wave15_extra(out: list[Candidate], existing: set[str], rng: random.Random) -> None:
    saints = list({a for a, _, _ in BHAKTI})
    movements = list({b for _, b, _ in BHAKTI})
    regions = list({c for _, _, c in BHAKTI})
    _triples(
        out,
        existing,
        rng,
        BHAKTI,
        ["'{a}'-ന്റെ ആത്മീയ പ്രസ്ഥാനം?", "'{a}' ഏത് പ്രസ്ഥാനവുമായി?"],
        ["'{a}' പ്രവർത്തിച്ച പ്രദേശം?", "'{a}'-ന്റെ പ്രവർത്തന കേന്ദ്രം?"],
        ["'{b}' പ്രസ്ഥാനത്തിന്റെ '{c}' പ്രതിനിധി?", "'{c}'-ൽ '{b}' പ്രസ്ഥാനം?"],
        movements,
        regions,
        saints,
    )

    builders = list({b for _, b in MONUMENTS})
    monuments = list({a for a, _ in MONUMENTS})
    _pairs(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{a}'-ന്റെ നിർമ്മാതാവ്?",
            "'{a}'-യുടെ നിർമ്മാണ ഉത്തരവാദി?",
        ],
        builders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{b}'-ന്റെ പേരിൽ അറിയപ്പെടുന്ന നിർമ്മാണം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണം?",
        ],
        monuments,
    )

    styles = list({b for _, b in TEMPLE_ARCH})
    temples = list({a for a, _ in TEMPLE_ARCH})
    _pairs(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{a}'-ന്റെ വാസ്തുവിദ്യാ ശൈലി?",
            "'{a}'-ന്റെ ശില്പശൈലി?",
        ],
        styles,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        ["'{b}' ശൈലിയിലെ പ്രധാന നിർമ്മാണം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട ക്ഷേത്രം?"],
        temples,
    )

    periods = list({b for _, b in TRAVELLERS})
    travellers = list({a for a, _ in TRAVELLERS})
    _pairs(
        out,
        existing,
        rng,
        TRAVELLERS,
        ["'{a}'-ന്റെ ഇന്ത്യാ സന്ദർശന കാലം?", "'{a}'-ന്റെ സഞ്ചാര കാലഘട്ടം?"],
        periods,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TRAVELLERS,
        ["'{b}'-യിൽ ഇന്ത്യ സന്ദർശിച്ചയാൾ?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സഞ്ചാരി?"],
        travellers,
    )

    founders = list({b for _, b in NEWSPAPERS})
    papers = list({a for a, _ in NEWSPAPERS})
    _pairs(
        out,
        existing,
        rng,
        NEWSPAPERS,
        ["'{a}'-ന്റെ സ്ഥാപകൻ?", "'{a}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി?"],
        founders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        NEWSPAPERS,
        ["'{b}'-ന്റെ പത്രം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട പത്രം?"],
        papers,
    )

    years = list({y for _, y, _, _ in REVOLTS})
    rev_regions = list({r for _, _, r, _ in REVOLTS})
    leaders = list({l for _, _, _, l in REVOLTS})
    names = list({n for n, _, _, _ in REVOLTS})
    _quads(
        out,
        existing,
        rng,
        REVOLTS,
        ["'{n}'-ന്റെ വർഷം?", "'{n}'-യുമായി ബന്ധപ്പെട്ട വർഷം?"],
        ["'{n}'-ന്റെ പ്രദേശം?", "'{n}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം?"],
        ["'{n}'-ന്റെ നേതാവ്?", "'{n}'-യുമായി ബന്ധപ്പെട്ട നേതാവ്?"],
        ["'{l}'-യുമായി ബന്ധപ്പെട്ട സംഘടന?", "'{l}'-ന്റെ സംഘടന/സമരം?"],
        years,
        rev_regions,
        leaders,
        names,
    )

    for rows, pool_b, pool_a, ab, ba in (
        (LAND_REVENUE, [b for _, b in LAND_REVENUE], [a for a, _ in LAND_REVENUE], "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?", "'{b}'-യുമായി ബന്ധപ്പെട്ട നികുതി/വ്യവസ്ഥ?"),
        (MUGHAL_ADMIN, [b for _, b in MUGHAL_ADMIN], [a for a, _ in MUGHAL_ADMIN], "'{a}'-ന്റെ അർത്ഥം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട പദം?"),
        (COINS, [b for _, b in COINS], [a for a, _ in COINS], "'{a}'-യുമായി ബന്ധപ്പെട്ട കാലം?", "'{b}'-ന്റെ കാലത്തെ നാണയം?"),
        (EURO_FACTORIES, [b for _, b in EURO_FACTORIES], [a for a, _ in EURO_FACTORIES], "'{a}'-ന്റെ കച്ചവട കേന്ദ്രം?", "'{b}'-യിലെ യൂറോപ്യൻ കമ്പനി?"),
        (REFORMERS, [b for _, b in REFORMERS], [a for a, _ in REFORMERS], "'{a}'-ന്റെ പ്രസ്ഥാനം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി?"),
        (INDUS, [b for _, b in INDUS], [a for a, _ in INDUS], "'{a}'-ന്റെ സവിശേഷത?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സ്ഥലം?"),
        (SANGAM, [b for _, b in SANGAM], [a for a, _ in SANGAM], "'{a}'-ന്റെ വിവരണം?", "'{b}'-യുമായി ബന്ധപ്പെട്ട കൃതി?"),
        (FOREIGN_POLICY, [b for _, b in FOREIGN_POLICY], [a for a, _ in FOREIGN_POLICY], "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?", "'{b}'-യുമായി ബന്ധപ്പെട്ട സംഭവം?"),
    ):
        _pairs(out, existing, rng, rows, [ab], pool_b)
        _pairs_rev(out, existing, rng, rows, [ba], pool_a)

    _match_pairs(
        out,
        existing,
        rng,
        MATCH_ROWS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ശരിയായ ജോഡി?",
            "'{a}'-ന്റെ ശരിയായ വിവരണം?",
            "'{a}'-യുടെ ശരിയായ ജോഡി?",
        ],
    )


def _wave15_more(out: list[Candidate], existing: set[str], rng: random.Random) -> None:
    saints = list({a for a, _, _ in BHAKTI})
    movements = list({b for _, b, _ in BHAKTI})
    regions = list({c for _, _, c in BHAKTI})
    _triples(
        out,
        existing,
        rng,
        BHAKTI,
        [
            "'{a}'-ന്റെ ആത്മീയ പരമ്പര?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രസ്ഥാനം?",
            "'{a}' ഏത് സൂഫി/ഭക്തി പരമ്പര?",
        ],
        [
            "'{a}'-ന്റെ പ്രവർത്തന പ്രദേശം?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം?",
            "'{a}' പ്രധാനമായി പ്രവർത്തിച്ച സ്ഥലം?",
        ],
        [
            "'{b}'-യുടെ '{c}' പ്രതിനിധി?",
            "'{c}'-ലെ '{b}' പ്രസ്ഥാനത്തിന്റെ പ്രധാന വ്യക്തി?",
            "'{b}' '{c}'-യിൽ പ്രവർത്തിച്ച വ്യക്തി?",
        ],
        movements,
        regions,
        saints,
    )

    builders = list({b for _, b in MONUMENTS})
    monuments = list({a for a, _ in MONUMENTS})
    _pairs(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാതാവ്?",
            "'{a}'-ന്റെ നിർമ്മാണ കാലത്തെ ഭരണാധികാരി?",
            "'{a}'-യുടെ നിർമ്മാതാവ്?",
            "'{a}' നിർമ്മിച്ച ഭരണാധികാരി?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട രാജാവ്?",
        ],
        builders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        MONUMENTS,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണം?",
            "'{b}'-ന്റെ കാലത്തെ പ്രധാന സ്മാരകം?",
            "'{b}' നിർമ്മിച്ച സ്മാരകം?",
            "'{b}'-യുടെ പേരിലുള്ള നിർമ്മാണം?",
        ],
        monuments,
    )

    styles = list({b for _, b in TEMPLE_ARCH})
    temples = list({a for a, _ in TEMPLE_ARCH})
    _pairs(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{a}'-യുടെ വാസ്തുവിദ്യാ ശൈലി?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണശൈലി?",
            "'{a}' ഏത് ശില്പശൈലിയിൽ?",
            "'{a}'-ന്റെ ശില്പശൈലി?",
        ],
        styles,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TEMPLE_ARCH,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നിർമ്മാണം?",
            "'{b}' ശൈലിയുടെ പ്രതിനിധി?",
            "'{b}'-യിൽ പണിത പ്രധാന നിർമ്മാണം?",
        ],
        temples,
    )

    periods = list({b for _, b in TRAVELLERS})
    travellers = list({a for a, _ in TRAVELLERS})
    _pairs(
        out,
        existing,
        rng,
        TRAVELLERS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട കാലഘട്ടം?",
            "'{a}'-ന്റെ ഇന്ത്യാ സന്ദർശന കാലം?",
            "'{a}' ഏത് കാലത്ത് ഇന്ത്യ സന്ദർശിച്ചു?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഭരണകാലം?",
        ],
        periods,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        TRAVELLERS,
        [
            "'{b}'-യിൽ ഇന്ത്യ സന്ദർശിച്ചയാൾ?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സഞ്ചാരി?",
            "'{b}' കാലത്ത് ഇന്ത്യ സന്ദർശിച്ച വ്യക്തി?",
        ],
        travellers,
    )

    founders = list({b for _, b in NEWSPAPERS})
    papers = list({a for a, _ in NEWSPAPERS})
    _pairs(
        out,
        existing,
        rng,
        NEWSPAPERS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വ്യക്തി?",
            "'{a}'-ന്റെ സ്ഥാപകൻ?",
            "'{a}' ആരുടെ പേരിലാണ്?",
            "'{a}'-യുമായി ബന്ധപ്പെട്ട സ്ഥാപകൻ?",
        ],
        founders,
    )
    _pairs_rev(
        out,
        existing,
        rng,
        NEWSPAPERS,
        [
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പത്രം?",
            "'{b}'-ന്റെ പേരിലുള്ള പത്രം?",
            "'{b}' ആരംഭിച്ച പത്രം?",
        ],
        papers,
    )

    years = list({y for _, y, _, _ in REVOLTS})
    rev_regions = list({r for _, _, r, _ in REVOLTS})
    leaders = list({l for _, _, _, l in REVOLTS})
    names = list({n for n, _, _, _ in REVOLTS})
    _quads(
        out,
        existing,
        rng,
        REVOLTS,
        [
            "'{n}'-യുടെ പ്രധാന വർഷം?",
            "'{n}'-യുമായി ബന്ധപ്പെട്ട വർഷം?",
            "'{n}' നടന്ന വർഷം?",
        ],
        [
            "'{n}'-യുടെ പ്രധാന പ്രദേശം?",
            "'{n}'-യുമായി ബന്ധപ്പെട്ട പ്രദേശം?",
            "'{n}' നടന്ന പ്രദേശം?",
        ],
        [
            "'{n}'-യുടെ നേതാവ്?",
            "'{n}'-യുമായി ബന്ധപ്പെട്ട നേതാവ്?",
            "'{n}'-യുടെ പ്രധാന വ്യക്തി?",
        ],
        [
            "'{l}'-യുമായി ബന്ധപ്പെട്ട സമരം?",
            "'{r}'-ൽ '{l}'-യുമായി ബന്ധപ്പെട്ട സംഘടന?",
            "'{l}' നേതൃത്വം നൽകിയ സംഘടന?",
        ],
        years,
        rev_regions,
        leaders,
        names,
    )

    for rows, pool_b, pool_a, ab_fwd, ab_rev in (
        (
            LAND_REVENUE,
            [b for _, b in LAND_REVENUE],
            [a for a, _ in LAND_REVENUE],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട നികുതി/വ്യവസ്ഥ?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നികുതി?",
        ),
        (
            MUGHAL_ADMIN,
            [b for _, b in MUGHAL_ADMIN],
            [a for a, _ in MUGHAL_ADMIN],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ഭരണപദം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പദം?",
        ),
        (
            COINS,
            [b for _, b in COINS],
            [a for a, _ in COINS],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട നാണയ കാലം?",
            "'{b}'-ന്റെ കാലത്തെ നാണയം?",
        ),
        (
            EURO_FACTORIES,
            [b for _, b in EURO_FACTORIES],
            [a for a, _ in EURO_FACTORIES],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട കച്ചവട കേന്ദ്രം?",
            "'{b}'-യിലെ യൂറോപ്യൻ കമ്പനി?",
        ),
        (
            REFORMERS,
            [b for _, b in REFORMERS],
            [a for a, _ in REFORMERS],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട പ്രസ്ഥാനം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട പരിഷ്കരണവാദി?",
        ),
        (
            INDUS,
            [b for _, b in INDUS],
            [a for a, _ in INDUS],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട സവിശേഷത?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട സ്ഥലം?",
        ),
        (
            SANGAM,
            [b for _, b in SANGAM],
            [a for a, _ in SANGAM],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വിവരണം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട കൃതി?",
        ),
        (
            FOREIGN_POLICY,
            [b for _, b in FOREIGN_POLICY],
            [a for a, _ in FOREIGN_POLICY],
            "'{a}'-യുമായി ബന്ധപ്പെട്ട വിവരണം?",
            "'{b}'-യുമായി ബന്ധപ്പെട്ട നയം/സംഭവം?",
        ),
    ):
        _pairs(
            out,
            existing,
            rng,
            rows,
            [ab_fwd, "'{a}'-ന്റെ പ്രധാന വിവരണം?", "'{a}'-യുമായി ബന്ധപ്പെട്ട വസ്തുത?"],
            pool_b,
        )
        _pairs_rev(
            out,
            existing,
            rng,
            rows,
            [ab_rev, "'{b}'-യുമായി ബന്ധപ്പെട്ട വസ്തു?", "'{b}'-ന്റെ പേരിലുള്ള വസ്തു?"],
            pool_a,
        )

    _match_pairs(
        out,
        existing,
        rng,
        MATCH_ROWS,
        [
            "'{a}'-യുമായി ബന്ധപ്പെട്ട ശരിയായ ജോഡി?",
            "'{a}'-ന് അനുയോജ്യമായ വിവരണം?",
            "'{a}'-യുടെ ശരിയായ വിവരണം?",
            "താഴെ കൊടുത്തിരിക്കുന്നവയിൽ '{a}'-ന്റെ ശരിയായ ജോഡി?",
        ],
    )


if __name__ == "__main__":
    print(len(generate_wave15_candidates(set(), random.Random(0))))
'''
