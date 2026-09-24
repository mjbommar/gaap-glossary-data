# Defect taxonomy for the FASB Master Glossary audit

Each glossary entry is checked for the following defects. Codes are used in every data file.

| Code | Defect | Test |
|---|---|---|
| CIRC | Circular definition | The entry belongs to a cycle of entries that define each other (strongly connected component of the dependency graph). Dependencies: every multiword glossary term appearing in the definition, plus single-word terms in the sensitivity variant. |
| SELF | Self-definition | The definition uses the term itself in a way that adds no content (tautology), as opposed to a restatement in a longer explanation. |
| NONAUTH | Nonauthoritative dependence | The definition relies on a source that is not authoritative GAAP: FASB Concepts Statements, AICPA guides or statements of position, pre-Codification standards, IFRS/IAS, or practice. |
| POINTER | Pointer-only entry | The entry defines nothing and only refers the reader elsewhere (another term or paragraphs). |
| DANGLING | Dangling pointer | A pointer whose target term or paragraph does not exist, or exists only as superseded text. |
| HOMONYM | Homonym entries | Two or more entries share a name with different definitions, without the entry saying where each applies. |
| SCOPECONF | Scope conflict | The entry itself says the word has a different meaning elsewhere in GAAP (one word, several meanings). |
| STALE | Stale or superseded | The entry, or what it depends on, is superseded or refers to superseded guidance. |
| PENDING | Embedded transition text | Two versions of a definition (current and pending) are concatenated in one entry. |
| UNDEF | Undefined dependency | The definition depends on a technical term that no glossary entry defines. |
| INCONS | Inconsistent with use | The definition conflicts with how the Codification's own paragraphs use the term. |
| MALFORMED | Malformed entry | The entry key, name or text is truncated, mislabeled or garbled. |
