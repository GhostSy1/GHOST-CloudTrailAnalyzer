# GHOST-CloudTrailAnalyzer Architecture Review

## Purpose of this document

This document records the repository structure observed during the portfolio review. It is intentionally factual: it describes paths that exist in the checkout and does not imply capabilities that are not implemented.

## Implementation inventory

| Property | Observed value |
|---|---|
| Repository | `GHOST-CloudTrailAnalyzer` |
| Languages | Python |
| Source-file count | 3 |
| Execution policy | Must be confirmed from the source before use |
| Release boundary | Authorized systems and operator-supplied data only |

## Source map

- `main.py`
- `tests/test_core.py`
- `tests/test_repository_contract.py`

## Review expectations

The command-line entry point, if present, should validate operator input, fail closed on invalid paths, and report observations with their source. Network access, external service calls, and privileged actions should be explicit in the README and should never be hidden behind a default command. A detection result must remain traceable to evidence rather than a hardcoded example.

## Change boundary

A change should update the relevant source module, tests, CLI reference, and changelog entry. A public release must not contain credentials, private keys, customer data, raw engagement artifacts, or undocumented access mechanisms.
