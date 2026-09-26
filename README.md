# FASB Master Glossary audit data

Data for the note *Circular, Superseded, and Borrowed: An Audit of the Definitions in the FASB Master Glossary*
by Michael J. Bommarito II (2026).

The note audits all 1,287 entries of the Master Glossary of the FASB Accounting Standards Codification. Deterministic
detectors and two independent language-model reviews (Claude Opus 5.5 and Claude Sonnet 5) screened every entry, and
every reported defect was verified against primary sources. This repository holds the screening results, the
verification records, and the glossary dependency graph.

## What is and is not here

The files contain identifiers (glossary slugs and headwords, Codification paragraph citations), defect codes, verdicts,
the authors' reasons, and the glossary citation graph with a short snippet for every link. They do not contain any
full paragraph or any definition as such. Each snippet is at most six words either side of the linked term, quoted so
that a reader can see each link and each dependency in context. Because many glossary definitions are short, the
windows around a short entry's several terms can together cover most of that entry. The Codification is published by
the Financial Accounting Foundation, which retains all rights in its text. Every claim here can be checked against its
public viewer at <https://asc.fasb.org/>, which requires accepting the Foundation's terms, and `definitions.csv` gives a
SHA-256 fingerprint of each linked definition's whitespace-normalized text so a reader can confirm they are reading
the version audited.

Snapshot: the public viewer as retrieved between 22:50 UTC on September 9 and 04:02 UTC on September 10, 2026.

**Citation keys.** The crawl files an industry Subtopic under the general Topic first (for example `605-958-15-6`).
`paragraph_links.csv` gives both the crawl key and the standard Codification citation (`958-605-15-6`). Other files
use the crawl key. On nine viewer pages the crawl recorded no citation, so 72 paragraphs (107 links, mostly in
Subtopics 944-20, 958-605 and 958-810) carry the viewer's internal page and element ID instead.

**Link occurrences.** `paragraph_links.csv` has one row per link occurrence (8,476), numbered in order within each
paragraph by `occurrence`; a paragraph can link the same term more than once. The `links` column of `definitions.csv`
counts the same occurrences, so the two files reconcile.

## Files

| File | Rows | What it is |
|---|---|---|
| `data/link_errors.csv` | 7 | Paragraphs whose glossary link leads to a definition that does not apply: the paragraph, the term, the definition linked, the definition that applies, and why. The note's lead finding. |
| `data/subtopic_link_splits.csv` | 6 | Every Subtopic whose paragraphs link two different definitions of one term, found by comparing displayed text, with a verdict. Three are defects reported in the note; three are explained by scope, transition text or a status table. |
| `data/verified_cycles.csv` | 36 | Every cycle in the glossary dependency graph, classified as a genuine mutual definition, a harmless synonym pointer, or a phrase-matching artifact, with severity and rationale. For genuine cycles, `glossary_anchor` names any entry content that is independent of the loop (5 of 11); an empty value means nothing in the glossary breaks it. For those six, `operative_anchor` names the operative paragraph outside the glossary that supplies the missing meaning. |
| `data/verified_nonauth_homonym.csv` | 62 | Verification of entries that rely on nonauthoritative sources (NONAUTH) and of names carrying several definitions (HOMONYM, HOMONYM_HIDDEN), with the subtopics that link each definition. |
| `data/verified_dangling.csv` | 45 | Verification of every pointer to a paragraph or term that may not exist, with the resolved citation and a verdict: an extraction artifact, or a pointer whose target survives only as a superseded placeholder. |
| `data/entry_manifest.csv` | 1,287 | Every glossary entry with each model's sound or unsound decision, the codes each model flagged (empty if none) and the codes the detectors flagged. Reproduces every count and kappa in `audit_stats.json`. |
| `data/detector_flags.csv` | 271 | Every detector flag, one row per flag, with its cycle, target or source but without the matched Codification text. |
| `data/audit_defects.csv` | 532 | Every (entry, defect code) pair flagged by at least one model, with each model's flag, whether a detector also flagged it, tier, severity, and the model's explanation. Detector-only flags are in `detector_flags.csv`. Screening output, not findings. |
| `data/paragraph_links.csv` | 8,476 | The citation graph: every glossary link occurrence in a Codification paragraph, with the specific definition it targets (`definition_key`: the Subtopic and headword in the viewer's element ID) and a snippet with the linked words in brackets. |
| `data/definitions.csv` | 1,145 | Every distinct definition that some paragraph links, with the Subtopic in its viewer ID, the number of links to it, and a SHA-256 fingerprint of its text. The ID Subtopic is not always where the definition originates: the viewer's "customer" links carry a 985-605 ID but display the Topic 606 definition. Compare definitions by fingerprint, not by ID. |
| `data/definition_edges.csv` | 1,294 | The dependency graph: glossary entry `entry` uses glossary term `uses_term` in its definition, with a snippet showing the words that create the dependency (56 edges have no snippet because the term appears only in a variant form). |
| `data/glossary_edges_multiword.csv` | 1,294 | The same dependency edges without snippets, as used by the detectors. |
| `data/audit_stats.json` | | Per-code counts for each model, both models, and Cohen's kappa between them. |
| `data/detect_summary.json` | | Per-code counts from the deterministic detectors. |
| `data/TAXONOMY.md` | | Definitions of the defect codes used in every file. |

## Scripts

`scripts/export_public_data.py` produced the audit and verification files from the private audit data, removing
full-text columns. `scripts/export_screening.py` produced the entry manifest and detector flags from the raw model
outputs and detector files, and asserts that the manifest reproduces `audit_stats.json`. `scripts/build_link_graph.py` produced the citation-graph files from the private crawl. Both are
included to document the method; their inputs are not distributed.

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
