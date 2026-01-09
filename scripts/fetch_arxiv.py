import feedparser
from urllib.parse import urlencode

ARXIV_API = "http://export.arxiv.org/api/query"

def fetch_entries(categories, max_results=500):
    query = " OR ".join(f"cat:{c}" for c in categories)

    params = {
        "search_query": query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results,
    }

    url = f"{ARXIV_API}?{urlencode(params)}"
    return feedparser.parse(url).entries
