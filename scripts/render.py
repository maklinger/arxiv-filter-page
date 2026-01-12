import yaml
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, UTC
from zoneinfo import ZoneInfo
from fetch_arxiv import fetch_entries
from utils import matches_filter
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
        label = dt.strftime("%d %b %Y")  # 12 Jan 2026
        grouped.setdefault(label, []).append(e)
    return grouped


env = Environment(loader=FileSystemLoader("templates"))

with open("config/filters.yaml") as f:
    config = yaml.safe_load(f)

filters = []
for fcfg in config["filters"]:
    entries = fetch_entries(fcfg["categories"], max_results=2000)
    selected = []
    for e in entries:
        if matches_filter(e, fcfg):
            selected.append({
                "title": e.title,
                "authors": ", ".join(a.name for a in e.authors),
                "abstract": e.summary,
                "arxiv_url": e.link,
                "pdf_url": next(l.href for l in e.links if l.type == "application/pdf"),
                "published": e.published
            })
        if len(selected) >= fcfg.get("numberlimit", 10000):
            break
    

    with open(f"config/layouts/{fcfg['layout']}.yaml") as lf:
        layout = yaml.safe_load(lf)

    fcfg["grouped_entries"] = group_by_date(selected)
    fcfg["layout"] = layout
    filters.append(fcfg)

html = env.get_template("base.html").render(
    page=config["page"],
    filters=filters,
    build_date=datetime.now(ZoneInfo("Europe/Amsterdam")).strftime("%d %b %Y"),
)

os.makedirs("site", exist_ok=True)
with open("site/index.html", "w") as f:
    f.write(html)

# Copy static assets into site/
if STATIC_DST.exists():
    shutil.rmtree(STATIC_DST)

shutil.copytree(STATIC_SRC, STATIC_DST)
