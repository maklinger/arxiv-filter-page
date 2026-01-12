# arXiv Filter Page

A static GitHub Pages site that tracks new arXiv submissions using
YAML-defined filters and layouts.

Daily updates via GitHub Actions.


# For local debugging:

```shell
micromamba create -n arxiv-env python feedparser jinja2 pyyaml
micromamba activate arxiv-env 
python ./scripts/render.py
``` 
