# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas"]
# ///
"""Export the public dataset from the private audit files of gaap-glossary-note.

Drops every column that carries full Codification text (definitions, paragraph excerpts, model-quoted evidence).
Keeps identifiers, citations, defect codes, verdicts and the authors' own reasons, which quote at most a short phrase.
Usage: uv run scripts/export_public_data.py ../gaap-glossary-note/data
"""
import json
import shutil
import sys
from pathlib import Path

import pandas as pd

SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parents[1] / "data"
DROP = {
    "audit_defects": ["evidence"],
    "verified_cycles": ["verbatim_fragments"],
    "verified_dangling": ["resolved_text_excerpt"],
    "verified_nonauth_homonym": ["verbatim_current", "verbatim_pending"],
    "glossary_edges_multiword": [],
}
for name, cols in DROP.items():
    d = pd.read_csv(SRC / f"{name}.csv")
    d.drop(columns=cols).to_csv(OUT / f"{name}.csv", index=False)
    print(f"{name}: {len(d)} rows, dropped {cols}")
for name in ["audit_stats.json", "detect_summary.json"]:
    json.loads((SRC / name).read_text())  # validate
    shutil.copyfile(SRC / name, OUT / name)
