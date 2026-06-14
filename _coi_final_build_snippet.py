# Helper snippet merged into make_coi_wave20_final.py

def _dedupe(rows: list) -> list:
    seen: set = set()
    out = []
    for r in rows:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def _apply_fix_row(row: tuple) -> tuple:
    if len(row) == 2:
        a, b = fix_text(row[0]), fix_text(row[1])
        m = re.search(r"അനുച്ഛേദം\s+(\d+[A-Z]?)", a)
        if m and (PH.match(b) or b.startswith("അനുച്ഛേദം")):
            num = m.group(1)
            if num in ARTICLE_TOPICS:
                b = ARTICLE_TOPICS[num]
        return a, b
    a, b, c = fix_text(row[0]), fix_text(row[1]), fix_text(row[2])
    return a, b, c


def _filter_pairs(rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    out = []
    for a, b in rows:
        a2, b2 = fix_text(a), fix_text(b)
        if ok(a2) and ok(b2):
            out.append((a2, b2))
    return _dedupe(out)


def _filter_triples(rows: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    out = []
    for a, b, c in rows:
        a2, b2, c2 = fix_text(a), fix_text(b), fix_text(c)
        if ok(a2) and ok(b2) and ok(c2):
            out.append((a2, b2, c2))
    return _dedupe(out)


def _build_article_topics_from_coi20(d) -> None:
    for a, b in d.ARTICLES:
        m = re.search(r"അനുച്ഛേദം\s+(\d+[A-Z]?)", a)
        if not m:
            continue
        num = m.group(1)
        b2 = fix_text(b)
        if not PH.match(b2) and ok(b2):
            ARTICLE_TOPICS[num] = b2
