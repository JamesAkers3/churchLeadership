from pathlib import Path


ROOT = Path("/Users/jamesakers/Desktop/PERSONAL/James New Endeavor")
VIZ = Path("/Users/jamesakers/.codex/visualizations/2026/09/08/01a08335-514b-78a0-b162-752a9af52e17")
OUT = ROOT / "tmp/pdfs/html"
OUT.mkdir(parents=True, exist_ok=True)


def wrap(fragment: str, title: str, extra_css: str = "") -> str:
    return f"""<!doctype html>
<html lang="en" style="color-scheme: dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    html, body {{ margin: 0; background: #181818; }}
    body {{ padding: 16px; overflow: visible; {extra_css} }}
  </style>
</head>
<body>
{fragment}
</body>
</html>
"""


tree = (VIZ / "tree-lifecycle-working-concept.html").read_text(encoding="utf-8")
(OUT / "tree-lifecycle-export.html").write_text(
    wrap(tree, "Rooted. Renewed. Multiplying Life.", "zoom: 0.30;"),
    encoding="utf-8",
)

passion = (VIZ / "from-passion-to-impact.html").read_text(encoding="utf-8")
(OUT / "from-passion-to-impact-export.html").write_text(
    wrap(passion, "From Passion to Impact"),
    encoding="utf-8",
)
