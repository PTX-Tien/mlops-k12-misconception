# Gate-level Exit Criteria — signoff checklist

Mỗi ticket có AC chi tiết riêng. Bảng này là **gate acceptance** tổng quan; gate không đóng chỉ vì một command pass.

| Gate | Required demonstration | Blocking red flag | Signoff role |
|---|---|---|---|
| G0 | SRS + actual accepted scope + rights signoff | License or stakeholder unknown | PM + Security |
| G1 | isolated env + Git + Ruff+Pytest+manifest | Shared conda cache write, lint fail | TL + QA |
| G2 | documented provenance, audit, data contract | mutable raw, missing records unhandled | DE + Security |
| G3 | frozen split, tests metric, leakage audit | question overlap, train-only feature | QA + TL |
| G4 | validated baseline & output format + independent replay | unsupported ML score / test tuning | MLE + QA |
| G5 | lawful image/OCR model, measured resource budget | training image models without authorization, unmeasured OOM | TL + Platform |
| G6 | controlled comparison, errors & model card | cherry-picked test run | TL + QA |
| G7 | versioned private data/artifacts, queryable runs | public leak, missing lineage | DE + Platform + Security |
| G8 | DAG and orchestration, failure injection | hidden downstream job after fail | Platform + QA |
| G9 | candidate can be rejected, versioned champion rollback | automatic promotion without acceptance | TL + QA |
| G10 | private staging batch/API, schema/parity/reliability | public API/PII logs | Platform + SRE + Security |
| G11 | protected PR (if remote), CI, staging controlled release | bypass reviews, deploy on green lint only | TL + SRE |
| G12 | telemetry/drift/incident/controlled CT capstone | drift blindly replacing champion | SRE + TL + QA |

Gate has status `PASS` only with all dependent tickets PASS **and** signed gate record. In solo mode, agent recommendation is labeled SIMULATION, human owner verifies any real Git operations.
