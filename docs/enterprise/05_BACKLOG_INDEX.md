# Backlog Index — 42 atomic tickets, 13 gates

**Status:** all `BACKLOG` by default except any ticket you actually complete and can prove. Start at G1-04 given current logs; G0 documents still require explicit review.

| ID | Title | Owner | Dependencies | Status |
|---|---|---|---|---|
| [G0-01](tickets/G0-01.md) | Problem discovery & user journey | PM | — | BACKLOG |
| [G0-02](tickets/G0-02.md) | SRS, measurable success & signoff | PM+TL | G0-01 | BACKLOG |
| [G0-03](tickets/G0-03.md) | Data rights, privacy & ethics assessment | Security | G0-01 | BACKLOG |
| [G1-01](tickets/G1-01.md) | Server preflight and reproducible inventory | Platform | G0-02 | BACKLOG |
| [G1-02](tickets/G1-02.md) | Isolated Conda, private caches & environment | Platform | G1-01 | BACKLOG |
| [G1-03](tickets/G1-03.md) | Git repository and safe .gitignore | Platform | G1-01 | BACKLOG |
| [G1-04](tickets/G1-04.md) | Fix Ruff import gate and freeze env manifest | QA | G1-02; G1-03 | BACKLOG |
| [G2-01](tickets/G2-01.md) | Authorized data ingestion & immutable provenance | DE | G0-03; G1-04 | BACKLOG |
| [G2-02](tickets/G2-02.md) | Dataset inventory & data quality EDA | DE | G2-01 | BACKLOG |
| [G2-03](tickets/G2-03.md) | Input/label schema contract & validation | DE+QA | G2-02 | BACKLOG |
| [G2-04](tickets/G2-04.md) | Data processing & lineage policy | DE | G2-03 | BACKLOG |
| [G3-01](tickets/G3-01.md) | Frozen group-aware validation split | MLE+DE | G2-03 | BACKLOG |
| [G3-02](tickets/G3-02.md) | Implement and test MAP@3 & diagnostics | QA+MLE | G3-01 | BACKLOG |
| [G3-03](tickets/G3-03.md) | Leakage and train–serve parity audit | QA | G2-03; G3-02 | BACKLOG |
| [G4-01](tickets/G4-01.md) | B0 constant/rule baseline & artifact contract | MLE | G3-03 | BACKLOG |
| [G4-02](tickets/G4-02.md) | B1 metadata-only sklearn pipeline | MLE | G4-01 | BACKLOG |
| [G4-03](tickets/G4-03.md) | Reproduce baseline, predict & evidence report | MLE+QA | G4-02 | BACKLOG |
| [G5-01](tickets/G5-01.md) | OCR subsystem design and image I/O contract | MLE | G4-03 | BACKLOG |
| [G5-02](tickets/G5-02.md) | Vision/OCR model feasibility experiment | MLE | G5-01 | BACKLOG |
| [G5-03](tickets/G5-03.md) | Shared-GPU budget and safe scheduler | Platform | G1-02; G5-01 | BACKLOG |
| [G6-01](tickets/G6-01.md) | Controlled ablation & comparative report | MLE | G5-02; G3-03 | BACKLOG |
| [G6-02](tickets/G6-02.md) | Error analysis: NONE, rare class & robustness | QA+MLE | G6-01 | BACKLOG |
| [G6-03](tickets/G6-03.md) | Champion selection proposal & model card | TL+MLE | G6-02 | BACKLOG |
| [G7-01](tickets/G7-01.md) | DVC data & artifact versioning | Platform | G2-04; G4-03 | BACKLOG |
| [G7-02](tickets/G7-02.md) | MLflow run tracking & lineage | Platform | G4-03; G7-01 | BACKLOG |
| [G7-03](tickets/G7-03.md) | Reproducibility challenge: cold-run | QA+Platform | G7-02 | BACKLOG |
| [G8-01](tickets/G8-01.md) | DVC DAG for offline ML stages | Platform | G7-03 | BACKLOG |
| [G8-02](tickets/G8-02.md) | Prefect flow orchestration & retries | Platform | G8-01 | BACKLOG |
| [G8-03](tickets/G8-03.md) | Automated validation gates & failure drills | QA+Platform | G8-02 | BACKLOG |
| [G9-01](tickets/G9-01.md) | Model registry and immutable versions | Platform | G7-02; G6-03 | BACKLOG |
| [G9-02](tickets/G9-02.md) | Model acceptance & human approval policy | TL+QA | G9-01; G8-03 | BACKLOG |
| [G9-03](tickets/G9-03.md) | Champion alias, promotion/rollback rehearsal | Platform+SRE | G9-02 | BACKLOG |
| [G10-01](tickets/G10-01.md) | Batch inference packaging & contract | MLE | G9-03 | BACKLOG |
| [G10-02](tickets/G10-02.md) | Private FastAPI staging endpoint | MLE+Platform | G10-01 | BACKLOG |
| [G10-03](tickets/G10-03.md) | Latency, parity and reliability testing | QA+SRE | G10-02 | BACKLOG |
| [G11-01](tickets/G11-01.md) | GitHub CI required checks and PR template | Platform+QA | G1-04; G10-03 | BACKLOG |
| [G11-02](tickets/G11-02.md) | Staging CD, manual release & rollback | SRE+Platform | G11-01; G9-03 | BACKLOG |
| [G11-03](tickets/G11-03.md) | Secrets, dependency & artifact security review | Security+QA | G11-01; G10-02 | BACKLOG |
| [G12-01](tickets/G12-01.md) | Runtime monitoring and alert baseline | SRE | G10-03; G11-02 | BACKLOG |
| [G12-02](tickets/G12-02.md) | Drift monitoring & feedback contract | MLE+DE | G12-01 | BACKLOG |
| [G12-03](tickets/G12-03.md) | Incident response, rollback & postmortem | SRE+QA | G12-01; G9-03 | BACKLOG |
| [G12-04](tickets/G12-04.md) | Controlled retraining and final capstone audit | TL+Platform | G12-02; G12-03; G11-03 | BACKLOG |

## Gate completion

- **G0 — Product discovery, requirements, privacy signoff**: 3 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.
- **G1 — Infrastructure & developer experience**: 4 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.
- **G2 — Data engineering & quality**: 4 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.
- **G3 — Evaluation & leakage guardrails**: 3 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.
- **G4 — Baseline model engineering**: 3 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.
- **G5 — Image/OCR & shared GPU**: 3 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.
- **G6 — Experiments & model evaluation**: 3 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.
- **G7 — Data/model lineage**: 3 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.
- **G8 — ML pipeline automation**: 3 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.
- **G9 — Model registry & governance**: 3 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.
- **G10 — Model serving**: 3 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.
- **G11 — CI/CD, security & release**: 3 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.
- **G12 — SRE, drift & continuous training simulation**: 4 tickets. Gate closes only after all required tickets individually pass + Tech Lead signs checklist + PM/Security signoff where relevant.

## Dependency discipline

Dependencies must be PASS before the issue moves to READY. A well-defined ticket can be blocked (e.g., dataset license or GPU allocation), and alternative task orders need TL ADR. Do not mark all tickets complete merely because a notebook ran.

## Scheduling hints

Suggested task order: G0/G1 foundation → G2 → G3 → G4 → G5 → G6 → G7 → G8 → G9 → G10 → G11 → G12. G1-04 current unblocker can be fixed immediately; G0 signoff must still happen before handling real data.

## Epics mapped to MLOps

Data = G2–G3 + G7. Model = G4–G6 + G9. Code / release = G1 + G8 + G10–G12. Cross-cutting = G0, privacy, reproducibility and approval.
