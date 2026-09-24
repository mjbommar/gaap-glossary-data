# FASB Master Glossary audit data

Data for the note *Circular, Superseded, and Borrowed: An Audit of the Definitions in the FASB Master Glossary*
by Michael J. Bommarito II (2026).

The note audits all 1,287 entries of the Master Glossary of the FASB Accounting Standards Codification. Deterministic
detectors and two independent language-model reviews (Claude Opus 5.5 and Claude Sonnet 5) screened every entry, and
every reported defect was verified against primary sources. This repository holds the screening results, the
verification records, and the glossary dependency graph.

## What is and is not here

The files contain identifiers (glossary slugs and headwords, Codification paragraph citations), defect codes, verdicts
and the authors' reasons. **They do not contain the text of the Codification.** Columns holding full definitions,
paragraph excerpts or model-quoted evidence were removed before publication (see `scripts/export_public_data.py`).
Reasons occasionally quote a short phrase, as the note does, for commentary. The Codification is published by the
Financial Accounting Foundation, and every claim here can be checked against its public viewer at
<https://asc.fasb.org/>, which requires accepting the Foundation's terms.

Snapshot: the public viewer as retrieved on September 9–10, 2026.

## Files

| File | Rows | What it is |
|---|---|---|
| `data/link_errors.csv` | 7 | Paragraphs whose glossary link leads to a definition that does not apply: the paragraph, the term, the definition linked, the definition that applies, and why. The note's lead finding. |
| `data/verified_cycles.csv` | 36 | Every cycle in the glossary dependency graph, classified as a genuine mutual definition, a harmless synonym pointer, or a phrase-matching artifact, with severity and rationale. |
| `data/verified_nonauth_homonym.csv` | 62 | Verification of entries that rely on nonauthoritative sources (NONAUTH) and of names carrying several definitions (HOMONYM, HOMONYM_HIDDEN), with the subtopics that link each definition. |
| `data/verified_dangling.csv` | 45 | Verification of every pointer to a paragraph or term that may not exist, with the resolved citation and a verdict (real defect or extraction artifact). |
| `data/audit_defects.csv` | 532 | Every (entry, defect code) pair flagged by a detector or by either model: which flagged it, tier, severity, and the model's explanation. Screening output, not findings. |
| `data/glossary_edges_multiword.csv` | 1,294 | The dependency graph: entry `term` uses glossary term `uses_term` in its definition (multiword terms). |
| `data/audit_stats.json` | | Per-code counts for each model, both models, and Cohen's kappa between them. |
| `data/detect_summary.json` | | Per-code counts from the deterministic detectors. |
| `data/TAXONOMY.md` | | Definitions of the defect codes used in every file. |

## How to read the counts

Only verified rows are findings. The model and detector flags in `audit_defects.csv` are a screen, and verification
checked flagged entries only, so the verified counts are lower bounds: they measure precision, not recall.

## Citation

Please cite the note and this dataset; see `CITATION.cff`. An archived, DOI-bearing copy of each release is deposited
on Zenodo.

## License

The data and code are released under the Creative Commons Attribution 4.0 International license (`LICENSE`). This
covers the authors' annotations, verdicts and code. It grants no rights in the Accounting Standards Codification,
which remains subject to the Financial Accounting Foundation's terms.
