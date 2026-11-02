# System Design + NFR baseline

## Logical architecture
`Kaggle authorized local ingest → immutable raw → schema/PII audit → curated metadata/working images → frozen split → feature pipeline (metadata → later OCR/vision) → training → validation & artifacts → model candidate → QA/Security/ML gate → registry → offline batch + private API staging → telemetry → controlled feedback → retraining candidate`.

## Interfaces
- Ingestion: raw Kaggle zip with checksum; no writes to raw rows; auditable content version.
- Dataset: `trace_id` key, `question_id` group, `root_code` train-only label; exact schema determined at G2.
- Feature builder: works with **serving-available input only**, no label/transcriptions injected inadvertently.
- Prediction: 1–3 unique root codes ordered by confidence (or policy-defined fallback), stable identifiers; fail closed on invalid input.
- Tracking: manifest `git_sha, data_sha256, split_sha256, config_sha256, env, seed, run_id, artifact_hash`.
- API: contract version, request size limits, exception status mapping, internal auth/access control before any real deployment.

## NFR — measurable acceptance, avoid fabricated targets
| NFR ID | Quality | Minimum initial acceptance | Later target policy |
|---|---|---|---|
| NFR-01 | Reproducibility | Deterministic split, model/reports hashed; explain nondeterminism | Compare repeated runs with tolerance pre-registered |
| NFR-02 | Privacy | No secret, student image/identifier committed or public served | Threat model + reviewed retention windows |
| NFR-03 | Portability | CPU code tests on clean Python 3.11; no hard-coded hostname in library code | Container on controlled host |
| NFR-04 | Reliability | Bad input → controlled error, no corrupted output | SLO after measurement |
| NFR-05 | Observability | Run logs + request counts/errors/latency without PII | Alert thresholds after baseline |
| NFR-06 | Resource isolation | All writable package/model caches in own root | GPU scheduler/concurrency policy |
| NFR-07 | Maintainability | Ruff, pytest, typed/contracted interfaces, ADR | CI security/static checks |
| NFR-08 | Data integrity | Immutable `data/raw`, dataset hash + duplicate checks | DVC remote/access control |
| NFR-09 | Safe rollout | Candidate ≠ champion, staged tests, rollback documented | Canary/shadow only if allowed |

## Environment constraints
8x RTX 2080 Ti 11 GB on shared Linux host per user-provided snapshot; VRAM not guaranteed. CPU by default G0–G4. GPU workloads only when permission, fresh `nvidia-smi` and explicit `CUDA_VISIBLE_DEVICES`. Never use shared base Conda for writes; `source scripts/00_private_runtime.sh`.

## Design decisions pending ADR
- Validation split: group by `question_id` + alternative group/pseudo-group stress test, analyze coverage gaps; no fake equivalence to official heldout.
- OCR local vs VLM direct: compare accuracy, cost, privacy and capability 11GB VRAM.
- DVC vs other data lineage, orchestration selection, safe remote storage policies.
- API serving batch vs synchronous latency, model confidence/abstention.
