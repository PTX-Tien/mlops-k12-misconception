# Evaluation & Dataset Protocol — freeze before comparing ML models

## Primary metric
Single-label MAP@3 (for the label in top 3, reciprocal rank 1/r; else 0) **only if confirmed by current official competition metric**. Unit tests: correct at rank 1/2/3, outside top3, duplicate predicted codes, missing/extra label, null label, invalid class, all `NONE`. Check that output ordering is deterministic under ties.

## Splits and leakage
- Official hidden test NOT for local tuning. Dataset split is a local research validation surrogate.
- Default GroupShuffleSplit by `question_id` to prevent question leakage, with seed and hash; **does not guarantee class stratification**.
- Check label coverage (`val_labels_not_in_train`), `NONE` prevalence, rare classes. When significant unseen class gap, design alternative protocol with TL approval/ADR instead of silently changing split after observing performance.
- Never use `transcription_steps`, `root_code`, `clean`, `final_answer_correct`, `misconceptions` as deployed features; training-only annotations can supervise legitimate separate OCR modules if serving input can supply equivalent features.

## Evaluation suites
- Offline MAP@3, top1 accuracy, `NONE` sensitivity/precision and false-positive (define denominators), per-class samples and grouped errors.
- Human-readable sanitized error analysis: category counts, not raw student work; no repeated leaderboard optimizations.
- Train–serve parity: same transformations for train/eval/API; offline batch equals live inference for same allowed request.
- Robustness: missing question context, image corruption, rotated/large image, OCR empty output, OOD question with abstention.
- Resource: CPU memory, GPU peak VRAM, p50/p95 duration on allowed hardware; compare models on equivalent setup.

## Model comparison policy
Pre-register hypothesis, metric, seed, split, resource budget and stop condition before tuning. Don't claim statistical significance from a single short holdout; use uncertainty/CI or multiple controlled repeats when feasible and do not repeatedly peek at hidden test.
