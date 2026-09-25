# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "pyarrow"]
# ///
"""Build the glossary citation graph with short snippets from the private crawl of the FASB public viewer.

Outputs (data/):
  paragraph_links.csv   every glossary link in a Codification paragraph, with the definition it targets
  definition_edges.csv  every dependency edge between glossary entries, with the triggering words
  definitions.csv       every distinct definition linked from a paragraph, with a SHA-256 of its text

Snippets are WINDOW words either side of the linked term, never more. No full definition or paragraph is written.
Usage: uv run scripts/build_link_graph.py <fasb.sqlite3> <glossary_clean.parquet> <glossary_edges_multiword.csv>
"""
import hashlib
import html as H
import re
import sqlite3
import sys
from pathlib import Path

import pandas as pd

WINDOW = 6
DB, GLOSS, EDGES = sys.argv[1], sys.argv[2], sys.argv[3]
OUT = Path(__file__).resolve().parents[1] / "data"
LINK = re.compile(r'<a href="/\d+/\d+/fasb-asc-publication/([^"]+)" title="([^"]*)">\s*<div class="term" '
                  r'id="term-([0-9]+-[0-9]+)-20-([^"]*?)-\d+"[^>]*>(.*?)</div>', re.S)


def words(fragment_html: str) -> list[str]:
    return H.unescape(re.sub(r"<[^>]+>", " ", fragment_html)).split()


def asc_citation(crawl_key: str) -> str:
    """The crawl files an industry Subtopic (9xx) under the general Topic first: 605-958-15-6 is ASC 958-605-15-6."""
    p = crawl_key.split("-")
    if len(p) > 2 and len(p[1]) == 3 and p[1].startswith("9"):
        p[0], p[1] = p[1], p[0]
    return "-".join(p)


def norm(s: str) -> str:
    return " ".join(H.unescape(s).split())


def sha(s: str) -> str:
    return hashlib.sha256(norm(s).encode()).hexdigest()


con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
links, defs = [], {}
for cit, h in con.execute("select citation, html from paragraph"):
    h = h or ""
    for m in LINK.finditer(h):
        slug, title, defsub, cname, anchor = m.groups()
        before, after = words(h[:m.start()])[-WINDOW:], words(h[m.end():])[:WINDOW]
        anchor = " ".join(words(anchor))
        key = f"{defsub} {cname}"
        defs.setdefault(key, dict(definition_key=key, defining_subtopic=defsub, slug=slug, sha256=sha(title), links=0))
        defs[key]["links"] += 1
        links.append(dict(paragraph=asc_citation(cit), crawl_key=cit, slug=slug, anchor=anchor, definition_key=key, defining_subtopic=defsub,
                          snippet=" ".join(before + [f"[{anchor}]"] + after)))
L = pd.DataFrame(links).drop_duplicates()
L.to_csv(OUT / "paragraph_links.csv", index=False)
pd.DataFrame(defs.values()).sort_values("definition_key").to_csv(OUT / "definitions.csv", index=False)

g = pd.read_parquet(GLOSS)
text = dict(zip(g.term.str.lower(), g.definition))
slug = dict(zip(g.term.str.lower(), g.slug))
rows = []
for r in pd.read_csv(EDGES).itertuples():
    d = text.get(str(r.term).lower(), "") or ""
    t = r"[\s-]+".join(re.escape(x) for x in str(r.uses_term).split())
    m = re.search(rf"(?<![A-Za-z]){t}(?:s|es)?(?![A-Za-z])", d, re.I)
    if m is None:  # allow singular use of a plural headword
        m = re.search(rf"(?<![A-Za-z]){t.rstrip('s')}(?![A-Za-z])", d, re.I)
    snip = "" if m is None else " ".join(d[:m.start()].split()[-WINDOW:] + [f"[{' '.join(m.group(0).split())}]"]
                                             + d[m.end():].split()[:WINDOW])
    rows.append(dict(entry=r.term, entry_slug=slug.get(str(r.term).lower(), ""), uses_term=r.uses_term,
                     uses_slug=slug.get(str(r.uses_term).lower(), ""), snippet=snip,
                     entry_sha256=sha(d) if d else ""))
E = pd.DataFrame(rows)
E.to_csv(OUT / "definition_edges.csv", index=False)
print(f"paragraph_links {len(L)}  definitions {len(defs)}  definition_edges {len(E)}  "
      f"edges without snippet {(E.snippet == '').sum()}")
