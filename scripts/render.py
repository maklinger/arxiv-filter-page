import yaml
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from fetch_arxiv import fetch_entries
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"
STATIC_SRC = ROOT / "static"
STATIC_DST = SITE_DIR / "static"


def group_by_date(entries):
    grouped = OrderedDict()
    for e in entries:
        raw_day = e["published"][:10]  # YYYY-MM-DD
        dt = datetime.strptime(raw_day, "%Y-%m-%d")
        label = dt.strftime("%d %b %Y")
        grouped.setdefault(label, []).append(e)
    return grouped


def is_recent_enough(entry, days):
    """Return False if entry is older than `days` days."""
    if days is None:
        return True
    published_dt = datetime.fromisoformat(entry["published"].replace("Z", "+00:00"))
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return published_dt >= cutoff


# Use ROOT-relative paths so the script works regardless of CWD
env = Environment(loader=FileSystemLoader(str(ROOT / "templates")))

with open(ROOT / "config" / "filters.yaml") as f:
    config = yaml.safe_load(f)

filters = []
for fcfg in config["filters"]:
    selected = []

    try:
        # Pass keywords to fetch_entries so filtering happens server-side.
        # The API returns only papers matching category AND keyword,
        # so max_results can be much smaller (e.g. 100 instead of 2000).
        entries = fetch_entries(
            fcfg["categories"],
            keywords=fcfg.get("keywords"),
            max_results=fcfg.get("max_results", 100),
        )

        days = fcfg.get("days")
        for e in entries:
            entry = {
                "title": e.title,
                "authors": ", ".join(a.name for a in e.authors),
                "abstract": e.summary,
                "arxiv_url": e.link,
                "pdf_url": next(
                    (l.href for l in e.links if l.type == "application/pdf"),
                    e.link,
                ),
                "published": e.published,
            }
            # Only local filter still needed: date cutoff
            if not is_recent_enough(entry, days):
                break  # entries are sorted newest-first, so we can stop early
            selected.append(entry)
            if len(selected) >= fcfg.get("numberlimit", 10000):
                break

    except Exception as exc:
        print(f"WARNING: failed to fetch '{fcfg.get('title', '?')}': {exc}")

    with open(ROOT / "config" / "layouts" / f"{fcfg['layout']}.yaml") as lf:
        layout = yaml.safe_load(lf)

    fcfg["grouped_entries"] = group_by_date(selected)
    fcfg["layout"] = layout
    filters.append(fcfg)

html = env.get_template("base.html").render(
    page=config["page"],
    filters=filters,
    build_date=datetime.now(ZoneInfo("Europe/Amsterdam")).strftime("%d %b %Y"),
)

os.makedirs(SITE_DIR, exist_ok=True)
with open(SITE_DIR / "index.html", "w") as f:
    f.write(html)

if STATIC_DST.exists():
    shutil.rmtree(STATIC_DST)
shutil.copytree(STATIC_SRC, STATIC_DST)

print(f"Built site with {len(filters)} filter(s).")
for fcfg in filters:
    total = sum(len(v) for v in fcfg["grouped_entries"].values())
    print(f"  {fcfg.get('title', '?')}: {total} entries")
