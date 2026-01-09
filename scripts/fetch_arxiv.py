import feedparser

ARXIV_API = "http://export.arxiv.org/api/query"

def fetch_entries(categories, max_results=500):
    query = " OR ".join(f"cat:{c}" for c in categories)
    url = f"{ARXIV_API}?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    return feedparser.parse(url).entries
