import feedparser
from urllib.parse import urlencode

ARXIV_API = "http://export.arxiv.org/api/query"

# Maps filter config field names to arXiv API field prefixes
FIELD_MAP = {
    "title": "ti",
    "abstract": "abs",
    "authors": "au",
}


def build_query(categories, keywords):
    """
    Build an arXiv search_query string that combines:
      - category filter: (cat:A OR cat:B OR ...)
      - keyword filter:  (ti:kw1 OR ti:kw2 OR abs:kw3 OR ...)

    Both parts are ANDed together so only papers in the right
    categories AND matching at least one keyword are returned.
    """
    cat_part = " OR ".join(f"cat:{c}" for c in categories)

    kw_terms = []
    for field, kws in keywords.items():
        api_field = FIELD_MAP.get(field)
        if api_field is None:
            continue
        for kw in kws:
            # Quote multi-word keywords
            if " " in kw:
                kw_terms.append(f'{api_field}:"{kw}"')
            else:
                kw_terms.append(f"{api_field}:{kw}")

    if kw_terms:
        kw_part = " OR ".join(kw_terms)
        return f"({cat_part}) AND ({kw_part})"
    else:
        # No keywords defined — fall back to category-only query
        return cat_part


def fetch_entries(categories, keywords=None, max_results=500):
    """
    Fetch arXiv entries matching the given categories and (optionally)
    keywords, sorted by submission date descending.

    Parameters
    ----------
    categories : list[str]
        arXiv category identifiers, e.g. ["astro-ph.HE", "gr-qc"].
    keywords : dict or None
        Keyword dict from the filter config, e.g.
        {"title": ["GRB", "gamma-ray burst"], "abstract": ["GRB"]}.
        If None or empty, only the category filter is applied.
    max_results : int
        Maximum number of results to request from the API.
    """
    if not keywords:
        query = " OR ".join(f"cat:{c}" for c in categories)
    else:
        query = build_query(categories, keywords)

    params = {
        "search_query": query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results,
    }
    url = f"{ARXIV_API}?{urlencode(params)}"
    return feedparser.parse(url).entries
