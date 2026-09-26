# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "pyarrow", "scikit-learn"]
# ///
"""Export the complete screening record: every entry, every model decision (including negatives), every detector flag.

Outputs (data/):
  entry_manifest.csv  all 1,287 glossary entries with each model's sound/unsound decision and flagged codes,
                      and the detector codes
  detector_flags.csv  every detector flag (one row per flag), without the Codification text the detectors matched
Checks that the manifest reproduces data/audit_stats.json.
Usage: uv run scripts/export_screening.py <glossary-audit data dir>
"""
import json
import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score

SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parents[1] / "data"
TEXT = {"text", "quote"}
g = pd.read_parquet(SRC / "glossary_clean.parquet")[["slug", "term"]]
assert g.slug.is_unique and len(g) == 1287

flags = []
for f in sorted(SRC.glob("detect_*.csv")):
    d = pd.read_csv(f)
    d = d[[c for c in d.columns if c not in TEXT]]
    d.insert(0, "code", f.stem.split("_", 1)[1])
    flags.append(d)
F = pd.concat(flags, ignore_index=True)
for c in ["cycle_id", "cycle_size", "entries"]:
    F[c] = F[c].astype("Int64")
F.to_csv(OUT / "detector_flags.csv", index=False)

m = g.copy()
for model in ["claude-opus-5-5", "claude-sonnet-5"]:
    tag = "opus" if "opus" in model else "sonnet"
    rec = {}
    for b in sorted((SRC / f"swarm_{model}").glob("batch_*.json")):
        for a in json.loads(b.read_text())["audits"]:
            assert a["slug"] not in rec, a["slug"]
            rec[a["slug"]] = a
    assert set(rec) == set(g.slug), f"{tag}: {len(set(g.slug) - set(rec))} entries missing"
    m[f"{tag}_sound"] = m.slug.map(lambda s: bool(rec[s]["sound"]))
    m[f"{tag}_codes"] = m.slug.map(lambda s: ";".join(sorted({d["code"] for d in rec[s]["defects"]})))
dc = F.groupby("slug").code.apply(lambda s: ";".join(sorted(set(s))))
m["detector_codes"] = m.slug.map(dc).fillna("")
m.to_csv(OUT / "entry_manifest.csv", index=False)

# reproduce the reported statistics
st = json.loads((OUT / "audit_stats.json").read_text())
uo, us = ~m.opus_sound, ~m.sonnet_sound
got = dict(entries_audited=len(m), unsound_opus=int(uo.sum()), unsound_sonnet=int(us.sum()), unsound_both=int((uo & us).sum()))
for k, v in got.items():
    assert st[k] == v, (k, st[k], v)
k = cohen_kappa_score(m.opus_sound, m.sonnet_sound)
assert abs(k - st["kappa_sound"]) < 1e-9, (k, st["kappa_sound"])
for code, s in st["by_code"].items():
    o = m.opus_codes.str.split(";").map(lambda x: code in x)
    n = m.sonnet_codes.str.split(";").map(lambda x: code in x)
    assert (int(o.sum()), int(n.sum()), int((o & n).sum())) == (s["opus"], s["sonnet"], s["both"]), (code, s)
    if s.get("kappa") is not None:
        assert abs(cohen_kappa_score(o, n) - s["kappa"]) < 1e-9, (code, cohen_kappa_score(o, n), s["kappa"])
print(f"manifest {len(m)} entries; detector flags {len(F)}; all audit_stats.json values reproduced")
