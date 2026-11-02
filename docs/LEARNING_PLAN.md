# Step-by-step learning plan with evidence gates

| Gate | Required tasks (in order) | Required evidence and tests |
|---|---|---|
| G0 Design | Read competition rules; define stakeholders and output contract; choose batch/online serving; threat-model privacy; document code/data/model versions | Problem spec, performance requirements, privacy checklist; distinguish MAP@3 from business outcome |
| G1 Foundation | Run preflight; verify disk quota; create conda; write `.gitignore`; Git init; run tests and lint | `preflight.json`, `pip freeze`, first commit; no image/credential tracked |
| G2 Data | Accept terms; fetch Kaggle; preserve immutable raw; audit schema/file linkage; classify missing/corruption; calculate class counts/grade/topic; stratify annotation error analysis; provenance hashes | `data_audit.json`, EDA notebook + data card, taxonomy histogram, missing-rate table; never upload child work |
| G3 Evaluation | Write MAP@3 from scratch; verify trivial cases; choose random stratified-like & group question validation; record difference; prevent using privileged columns; check train/val trace overlap | `pytest` pass, frozen split manifest; group question overlap = 0; known long-tail coverage |
| G4 Baseline | Begin with prior/metadata baseline; track seed/config/data hash; train only on training partition; measure MAP@3 and NONE FP; hold out official test; inspect 20 errors | Reproducible `baseline.joblib`, `baseline_metrics.json`, 20-item anonymized failure taxonomy |
| G5 Image model | Select supervised OCR / vision encoder or multimodal VLM; check GPU VRAM, fp16, compute budget; image preprocessing; generate **out-of-fold** OCR/transcription for training to avoid teacher-forcing mismatch; deploy complete OCR->ranker | Identical inference feature pipeline; OCR error audit, quality & latency comparison; no label-leaking text |
| G6 Scientific model evaluation | Fixed validation version; compare text-only, image-only, fusion; ablations of context and taxonomy; 3 seeds or grouped folds if feasible; confidence/calibration; unknown/long-tail labels | Reproducible comparison matrix including uncertainty, per-topic and NONE false alarm |
| G7 Lineage | Git SHA, DVC-tracked data metadata and output artifacts, MLflow params/metrics/artifacts, model signature; avoid pushing private data | Given run ID reconstruct model, data hash, code SHA, config |
| G8 Pipeline | Convert steps to idempotent functions/stages; DVC DAG first, then Prefect 3 orchestration for cache, retries, schedules, alerting | Run the DAG twice, confirm caching; inject missing-data failure, no model promotion |
| G9 Registry | Register candidate; compare with current champion; use validation and serving acceptance gates; human review; stage->champion, rollback test | Written model card; rejected candidate stays unpromoted; successful rollback |
| G10 Serve | Exact shared inference library for batch + API; contract validation; health endpoint; timing/logging; test with anonymized/synthetic request | Unit/integration tests; p50/p95 benchmark; no raw image payload in logs |
| G11 CI/CD | Git PR checks: lint + tests + synthetic contract cases; isolated packaging; staging deployment with approval | CI green; intentionally failing test blocks merge/release; no GPU training on CI runner |
| G12 Monitor/CT | Track traffic, latency, error, image quality, topic/grade distribution, prediction distribution and delayed labels; distinguish drift from real concept shift; define trigger and approval | Synthetic drift demo; alert; retraining candidate evaluated, accepted/rejected by gate; audit incident |

## Validation protocol — important
Official data splits by student; questions can recur in train/test. You do **not** have student IDs to reproduce original student-disjoint split inside `train.csv`. Therefore maintain **two offline views**: (1) a frozen row-level holdout for a competition-like check (not guaranteed student-disjoint), (2) a stricter GroupShuffleSplit by `question_id` testing new questions; report both instead of calling either the official split. Small classes with one example cannot be stratified. Report per-class supports; do not invent missing labels.

## Recommended architectural learning sequence
1. CPU-only metadata baseline (tests/lineage), NOT competitive vision model.
2. Add image reader OCR or VLM (whole production input available at inference).
3. Add model training and scientific comparison.
4. MLflow + DVC -> Prefect -> model registry -> FastAPI -> CI/CD -> monitoring.

## Change-management discipline
- Git version: code + config + documentation only.
- Dataset version: DVC pointer + immutable raw hash (secure remote only if permitted).
- Model version: MLflow run plus model registry alias; archive preprocessors & taxonomy version.
- Infrastructure version: environment lock, deployment config, container image digest (if Docker permitted).
- Workflow version: DVC DAG, orchestration code, tests and approvals.

## Typical pitfalls
- Official Kaggle test cannot serve as local hyperparameter tuning validation.
- `transcription_steps` is ONLY supplied with train labels, not test/inference.
- Simple row split may memorize a repeated `question_id`; stricter group split may be pessimistic relative to official contest (report both).
- Label distribution about one-third NONE, and 13 labels reportedly have only one training item; macro per-class conclusions are noisy.
- 2080 Ti 11GB has compute capability 7.5 and no native bf16; prefer FP16-compatible models after checking exact PyTorch/wheel support.
- Model deployment alone ≠ a tested end-to-end MLOps process.
