import yaml
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from fetch_arxiv import fetch_entries
from utils import matches_filter
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"
STATIC_SRC = ROOT / "static"
STATIC_DST = SITE_DIR / "static"

env = Environment(loader=FileSystemLoader("templates"))

with open("config/filters.yaml") as f:
    config = yaml.safe_load(f)

filters = []
for fcfg in config["filters"]:
    entries = fetch_entries(fcfg["categories"])
    selected = []
    for e in entries:
        if matches_filter(e, fcfg):
            selected.append({
                "title": e.title,
                "authors": ", ".join(a.name for a in e.authors),
                "abstract": e.summary,
                "arxiv_url": e.link,
                "pdf_url": next(l.href for l in e.links if l.type == "application/pdf"),
            })
        if len(selected) >= fcfg["numberlimit"]:
            break

    with open(f"config/layouts/{fcfg['layout']}.yaml") as lf:
        layout = yaml.safe_load(lf)

    fcfg["entries"] = selected
    fcfg["layout"] = layout
    filters.append(fcfg)

html = env.get_template("base.html").render(
    page=config["page"],
    filters=filters,
    build_date=datetime.utcnow().strftime("%Y-%m-%d"),
)

os.makedirs("site", exist_ok=True)
with open("site/index.html", "w") as f:
    f.write(html)

# Copy static assets into site/
if STATIC_DST.exists():
    shutil.rmtree(STATIC_DST)

shutil.copytree(STATIC_SRC, STATIC_DST)
