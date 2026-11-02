# Acceptance, QA and Quality Gates

## Evidence precedence
1. Reproducible command + input version + output + exit status.
2. Machine-readable tests and checks.
3. Small sanitized log snippets/metrics & run ID, git commit.
4. Human explanation of failure cases and tradeoffs.

Screenshots/talk-only are insufficient. Never paste tokens, student images, raw CSV rows, identifiable work, private paths if unsafe.

## Severity taxonomy
- **P0 / BLOCKER:** data disclosure, training on train-only data, official test leakage, corrupt/potentially destructive script, false claim of approval; always block.
- **P1 / HIGH:** invalid metric, incorrect split, un-reproducible result, failing CI/test, broken serving contract; block.
- **P2 / MEDIUM:** missing negative cases/docs/logging, poor diagnostics, performance risks; normally request changes unless explicitly accepted as tracked debt.
- **P3 / LOW:** naming/style/readability; fix in PR if trivial or add followup with owner.

## Reviewer rubric (100 points; minimum >=85 AND all hard gates)
| Domain | Weight | How assess |
|---|---:|---|
| Meets acceptance criteria | 25 | each AC met, no untested assumptions |
| Correctness / robustness | 20 | positive + negative tests; no leakage |
| Reproducibility / evidence | 15 | run identifiers, commands, hashes, environment |
| Maintainability | 10 | lint, small modules, clear interfaces |
| Data/privacy/security | 15 | secrets, sensitivity, data rights, safe logging |
| Operational readiness | 10 | failure handling, resources, rollback if relevant |
| Explanation/learning | 5 | candidate can explain choice + alternative |

Rubric 85 không override P0/P1 hoặc failing CI. QA verdict: `PASS`, `FAIL`, `NEEDS_EVIDENCE`.
Reviewer verdict: `RECOMMEND_APPROVE`, `CHANGES_REQUESTED`, `BLOCKED`, `NEEDS_EVIDENCE`. **Not equal to GitHub approval**.

## Hard-gates per changeset
- **All:** `pytest` + `ruff` clean, appropriate package/contract tests, no secrets/raw data, issue link and impact statement.
- **Data:** validated raw/processed separation, schema test, lineage, no raw overwrite, leakage audit.
- **Model:** accepted split/metric protocol, legal input fields, seed/model hash, evaluation including `NONE` errors, inference parity.
- **API:** versioned schema, negative inputs, bounded resources, logging policy, staging smoke.
- **Release:** staged model, manual release decision, rollback target, post-deploy checks.

## Minimum test pyramid
- Unit: normalization, ranking, metrics, schema, deterministic transforms.
- Integration: ingest→validate→split (synthetic), train→predict, API→loader (synthetic model), MLflow save/load.
- End-to-end: staging request + output format + telemetry + rollback; NOT CI with real Kaggle images.
- Nonfunctional: latency measured on supported hardware, stress/corrupted image, resource starvation.

## Requirement traceability
Ticket AC ↔ test ID ↔ evidence record ↔ reviewer comment ↔ PR ↔ merge commit. See `14_TRACEABILITY_MATRIX.md`.
