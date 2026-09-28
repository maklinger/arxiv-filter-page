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


# For manual, local update:

Go to root path and run
```
micromamba activate arxiv-env 
python ./scripts/render.py
ghp-import -n -p -f site/
```
`-n` adds a `.nojekyll` file, `-p` pushes automatically, `-f` forces.