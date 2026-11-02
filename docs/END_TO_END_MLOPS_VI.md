# End-to-End Machine Learning / MLOps — Tài liệu thiết kế và học thực hành

*Ngày thiết kế: 02/11/2026 · use case CoLearn K-12 handwritten mathematics misconception detection*

## I. Tư duy hệ thống: dự đoán là một phần nhỏ

Một mô hình tốt trả lời *nhãn nào?*; hệ thống ML vận hành tốt phải trả lời thêm *dữ liệu ở đâu, mô hình nào, phiên bản nào, có thể tái lập hay không, ai phê duyệt, khi lỗi thì làm gì?* Bài viết **Three Levels of ML Software** mô tả ba tài sản cần quản lý (Data, Model, Code), trong khi khung trưởng thành tự động hóa của Google Cloud chia Level 0 (thủ công), Level 1 (ML pipeline automation / CT), Level 2 (CI/CD cho ML pipeline). Hai hệ phân loại không đồng nghĩa.

Kiến trúc logic:
```
Problem framing + requirements + cost/risk/privacy gates
                        |
                      DATA
source -> ingestion -> schema, integrity -> EDA -> splits -> immutable dataset snapshots
                        |
                      MODEL
baselines -> supervised training -> validation -> error analysis -> registry candidates
                        |
                      CODE
Git -> tests -> build -> release -> serving -> instrumentation -> operations
                        |
                     FEEDBACK
traffic + data quality + delayed true labels -> alerts -> investigate -> controlled retrain
```

Data, Code, and Model have independent version identities, but every accepted deployment must link all three (plus environment, transformation, and taxonomy versions).

## II. Problem specification, data and restrictions

Competition: https://www.kaggle.com/competitions/misconception-detection-in-k-12-student-math-workings/overview
Official organizer information: https://colearnlab.com/colearn-lab-launches-global-kaggle-competition-teach-ai-misconception/
Gated dataset info / conditions: https://huggingface.co/datasets/colearnlab/misconception-detection

Input is a photographed handwritten mathematical solution, question text / mathematical notation, question diagram if supplied, correct answer and metadata. Target is `root_code`, one of ~75 misconception categories, or `NONE` when no major misconception. Train: ~1,500 annotated rows; test: ~3,498 rows without label; unlabelled: ~50,000 rows. Score is MAP@3; only the first 3 distinct ranked codes matter and only one code is correct per row. These numbers are publisher-reported and must be audited on the actual downloaded version.

### Crucial train-serve asymmetry

`transcription_steps`, `final_answer_correct`, `clean`, `misconceptions`, and `root_code` are training-only labels/annotations. They **do not** exist as test-time input. If a text classifier is trained directly on ground-truth transcriptions, its local score does not validate a deployable solution unless OCR at inference can generate equivalent text. Never use transcriptions from validation images as an input to the **deployed** ranker. Use generated OCR text for both training-validation of a ranker and inference; if OCR is trained on labelled transcripts, cross-fit/OoF when creating text for training and do not feed target labels into prompts.

### Data protection

CoLearn mirror restricts use to participation/discussion under competition rules; don't redistribute data or trained models, don't attempt student identification, don't publicly serve real student images and don't send them to third-party APIs unless permitted. The project therefore uses an internal-only staging simulator for deployment/monitoring exercises. A real education product would require separate authorization, privacy assessment, access controls, retention controls and stakeholder review.

## III. Full plan per gate

### G0 — Problem framing
**Why**: without acceptance criteria and a serving contract, ML scores can optimize the wrong thing.

Tasks: write a problem statement; identify a teacher/annotator as decision maker, and model as recommendation aid; define top3 rank output, `NONE`, uncertainty, safe fallback; specify image/metadata-only contract; list costs and privacy obligations; choose initial batch serving, later local REST; define measurable acceptance criteria but leave thresholds unfilled until first runs; document serving budget and escalation.

Artifacts: `docs/01_problem_framing.md`, initial model/risk card, interface contract.

Exit: can explain what failure on correct student work looks like and why MAP@3 alone is insufficient.

### G1 — Engineering environment and source management
**Why**: unrepeatable environments and shared hardware contention invalidate experiments.

Tasks: identify server OS, Python, free storage, GPU processes, driver; choose isolated Python 3.11 conda at project path; do not modify base env, driver or neighbors' GPUs; create Git repository + ignore raw images/models/logs/credentials; verify unit tests; capture dependency snapshot; record seed/hardware; create branching and commit conventions.

Artifacts: `reports/preflight.json`, isolated environment, `git log`, tests, dependency snapshot.

Exit: tests run on CPU without access to data or GPU. A code clone can install the environment and run the same tests.

### G2 — Data engineering
**Why**: data contracts, integrity and provenance must be trusted before training.

Tasks: read and accept Kaggle restrictions; download privately, inspect archive structure before unzipping; preserve raw source immutable; store byte hashes + metadata; ensure unique `trace_id`, consistent taxonomy IDs, valid image paths, noncorrupt JPEGs and diagrams, train-only fields not present on test; investigate missing values, duplicate images (hash/perceptual hash if permitted), train/test question overlap; make class counts, topic/grade distributions, image sizes/blur analysis with anonymized aggregates.

Artifacts: `reports/data_audit.json`, `docs/data_card.md`, EDA notebook, incident log for unusable rows.

Exit: dataset contract passes, raw fingerprints logged and all known limitations written down.

### G3 — Evaluation design
**Why**: overly optimistic validation is one of the most common ML development failures.

Tasks: implement MAP@3 from scratch with toy examples; register top1 accuracy, top3 recall, NONE precision/recall/FAR, per-topic/grade/class metrics; define frozen validation manifest. Official split is by student; question IDs overlap across train/test. You lack student IDs in train; distinguish row-level (competition-like but potentially student leakage) from grouped-question (out-of-question generalization). Do not select models on official hidden test or repeatedly optimize public LB.

Artifacts: `tests/test_metrics.py`, `data/processed/split.csv` and manifest, validation protocol.

Exit: train/val `trace_id` disjoint, grouped-question IDs disjoint for group split, metrics unit tests pass; unseen labels in validation reported rather than silently dropped.

### G4 — CPU baseline
**Why**: first prove the ML system wiring works and quantify how much question metadata alone explains.

Tasks: run class-prior baseline (as a TODO exercise) then TF-IDF character n-gram + logistic regression from `question_text`, `correct_answer`, `topic_name`, `grade`, with no handwriting or privileged annotations. Record fixed seed/split/code/dataset hash, metrics and val predictions; inspect confusions, especially NONE. Produce submission from sample format without training on test labels.

Artifacts: `models/baseline.joblib`, `reports/baseline_metrics.json`, `reports/baseline_val_predictions.csv`, baseline submission.

Exit: repeated run under same env gives same metrics; baseline test serving only accesses declared allowed fields. This is **not** a serious visual misconception solution.

### G5 — Working-aware modeling
**Why**: real target is the handwritten reasoning, not the question topic.

Candidate 1: image -> OCR (Bahasa Indonesia + math notation) -> text from a consistent inference-time generator -> rank 75 misconception descriptions + NONE via embedding/classifier/reranker.

Candidate 2: image + question + taxonomy -> compact multimodal vision-language model -> constrained top-3 class ranks. Test model permissibility, latency and wrong-language math OCR before investing.

Candidate 3: fused image embedding, question metadata and OCR representation -> supervised classifier/ranker, with correct handling of missing/incorrect OCR.

Tasks: measure image loading, rotations, blurs, damaged files; compare OCR/manual transcription only as **upper bound diagnostic**, never as deployable test feature; choose GPU after checking current owner and VRAM. Favor fp16 on 2080 Ti/Turing; do not assume bf16/flash-attention-2 works. Small model + adapter tuning or frozen features are easier than full VLM fine-tuning on 11GB.

Artifacts: reusable image preprocess module, OCR/model config, outputs aligned by trace_id, per-sample timing, failed-image handling.

Exit: a new test image can produce top3 recommendations without any training-only columns.

### G6 — Evaluation & scientific iteration
**Why**: optimization without controlled comparisons and uncertainty estimates encourages leaderboard overfit.

Tasks: fixed group split and optionally a frozen row-level second split; compare metadata-only, image-only, OCR-only, multimodal fusion; ablate question text, correct answer, OCR, taxonomy descriptions, image resolution; quantify data efficiency with 10/25/50/100% label subsets; report minority classes and NONE FAR; repeat seeds or grouped folds, show confidence intervals when feasible; write error taxonomy and model card.

Exit: accepted candidate beats baseline on chosen honest validation while staying within memory, latency and privacy budgets.

### G7 — Lineage / tracking / versioning
**Why**: a model is not reproducible from a filename alone.

Tasks: initialize DVC only after raw audit; version data pointers, not image bytes in Git; use private remote only when competition terms permit; put code, config, seed, dataset checksum, transform version, feature version, taxonomy version, dependencies, model artifact and run ID into metadata. Add MLflow experiments/runs, stage metrics, images or model artifacts only in private storage.

Important: DVC is strong for data/pipeline dependencies; MLflow is strong for experiment runs, model registration and aliases. They complement; neither replaces Git.

Exit: can recover exactly which code/data/config produced a model and explain failure to reproduce if dependency version changes.

### G8 — Orchestration
**Why**: a list of commands is not yet an observable, retryable production pipeline.

DAG: `ingest -> validate -> split -> preprocess -> train -> evaluate -> model-gate -> register -> staging-smoke -> deploy-approved`. Start with DVC dependencies/caching, then explore Prefect 3 tasks, retries, state/flow runs, schedules, and notifications. DAG task outputs need deterministic IDs and atomic file writes; retries must not duplicate or corrupt artifacts.

Inject failure: wrong schema, missing image, no free disk, OOM, validation metric regression. Ensure downstream promotion cannot happen.

Exit: idempotent successful rerun, visible failure state, clear manual recovery.

### G9 — Registry and safe promotion
**Why**: a new model artifact should not automatically replace the one serving users.

Tasks: candidate artifact + model card -> acceptance checks (metric threshold; quality on NONE; runtime; signature; security; reproducibility) -> approval -> champion alias. Distinguish model artifact registration from deployment. Practice shadow testing (synthetic traffic), rollback and versioned signatures. Store hashes, class taxonomy version, image transformation version and release notes.

Exit: deliberately bad candidate is rejected, champion remains unchanged; rollback to known-good works.

### G10 — Serving patterns
**Why**: Kaggle prediction is batch serving but learning production requires online API and train/serve parity.

1. Batch: score all rows in test.csv with images and context, output top3; deterministic order, resumable, failed-row audit.
2. REST: `POST /predict` accepts image or private local file reference, approved question context; schema validation; returns ranked codes, `model_version`, confidence/proxy score and processing time; `/health` gives no private details. Use `127.0.0.1` only on shared server.
3. Load test: synthetic input only; measure p50/p95, throughput, memory, cold-start time; avoid raw image logging.

Exit: same pipeline produces equivalent batch vs API results under controlled inputs.

### G11 — CI/CD / reproducible release
**Why**: automated training is not equivalent to safe delivery.

CI: lint, formatting, unit tests, synthetic contract checks, security scanning, build artifact. CD: deploy to staging with an approved environment, smoke test, explicit promotion and rollback. CT: conditionally retrain when approved new labelled data arrives; evaluate candidate before deployment. Use CPU-only GitHub Actions for code checks. GPU experiments should run on an authorized isolated runner/scheduler, not fire on each PR.

Exit: failing metric/contract test blocks deployment; no real student data or tokens leak into CI logs.

### G12 — Monitoring, feedback and controlled retraining
**Why**: a good model at validation time can degrade after launch.

Observe system: request volume, error count, p50/p95 latency, VRAM, crash/OOM, image load failure.
Observe data: grade/topic distributions, image dimensions/quality, text length, missingness, embedding drift where privacy permits.
Observe model: predicted `NONE` rate, entropy/top3 margin, class distribution, out-of-distribution percentage, delayed accuracy/MAP@3 when verified teacher labels arrive. **Data drift is not sufficient evidence of performance degradation**, and performance is not measurable on unlabeled traffic until reliable labels return.

Set alert thresholds using reference baselines; triage alert; human review; candidate training on authorized and versioned new labels; evaluate in an honest holdout; promote or reject; rollback; record incident review.

Exit: a simulated drift triggers an investigation and a controlled re-evaluation, **not** automatic promotion based only on drift.

## IV. Shared-server resource planning

The snapshot sent (2026-11-02 10:29:57 GMT+7): 8 x RTX 2080 Ti, each 11,264 MiB. GPUs 3 and 7 are low utilization but have ~527/595 MiB already used, while others have workloads. Never assume these cards are available later, and get permission before GPU use. Start CPU-first. 2080 Ti is Turing (compute capability 7.5) and lacks native BF16. Consider FP16, microbatch=1, frozen encoders or LoRA if supported by actual model/driver. Enable explicit CUDA_VISIBLE_DEVICES only after checking and authorization; not a device scheduler.

Disk: expected raw dataset has a several-GB image footprint, and model/cache/checkpoints need additional space. Use a local private conda env in project root and keep caches controlled. `reports/preflight.json` records free disk on actual server.

## V. Deployment realism and governance

The competition data may be restricted to competition participation. A publicly available prediction web service using images or weights from the competition could violate those terms. For full MLOps learning, simulate deployment with synthetic input or a separately licensed teaching dataset; keep CoLearn competition evaluation private and compliant. Explain to a reviewer the boundary between *MLOps lab*, *competition submission*, and *authorized production application*.

## VI. Tool selection and alternatives

Chosen minimal path: Git + Conda/pip + Pandas/Pillow/pytest + scikit-learn/PyTorch + DVC + MLflow + Prefect 3 + FastAPI + Docker (if allowed) + CI service + Evidently or custom monitors. Reason: focused and deployable on one shared Linux server. Alternatives: TFX for TensorFlow-centric pipelines, Metaflow/Kubeflow for enterprise orchestration, Airflow for broader data pipelines, and managed Vertex AI/SageMaker/Azure ML for cloud deployment. These are alternatives, not prerequisites to understand MLOps. A feature store (e.g. Feast) is usually unnecessary for a 1,500-row image competition without real-time cross-service features.

## VII. Reading list

- https://ml-ops.org/content/three-levels-of-ml-software
- https://ml-ops.org/content/mlops-principles
- https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
- https://www.mlflow.org/docs/latest/ml/tracking/
- https://www.mlflow.org/docs/latest/model-registry/
- https://doc.dvc.org/start
- https://www.prefect.io/docs/v3/get-started/index
- https://docs.evidentlyai.com/introduction
- https://github.com/Kaggle/kaggle-cli/blob/main/docs/README.md
