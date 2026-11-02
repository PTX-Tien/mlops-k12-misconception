# Gate 0 — Problem framing & measurable requirements

## Business question
Input: student handwriting image, math question, answer key and permitted metadata.
Output: top-3 ranked taxonomy `root_code` recommendations or `NONE`.
User: teacher or annotation specialist (human remains final arbiter).
Decision: review potential root misconception, **not** automatic high-stakes student grading.

## ML objective
MAP@3 primary; top-1 accuracy, top-3 recall; quality on `NONE` cases; per-grade/topic metrics; label support and uncertainty. Capture latency per request, memory, data/inference failures. Separate technical KPI from stakeholder KPI (minutes saved per review, user trust, false feedback).

## Serving-time contract
Allowed: `trace_id`, `question_text`, `correct_answer`, `topic_name`, `grade`, `image_file`, `question_image_file`, and authorized image bytes. `root_code` is output not input.
Forbidden: `transcription_steps`, `misconceptions`, `clean`, `final_answer_correct`; these appear only in training annotations. If doing OCR, its output must be generated from image at inference using the same reproducible stage.

## Scope of learning lab
- Phase A: offline reproducible retraining and batch prediction on the local server.
- Phase B: staging-only REST service bound to localhost, or isolated container if allowed.
- Phase C: synthetic traffic, monitoring, manual approval for deployment/retraining.
- NO public educational service using contest artifacts without explicit written authorization.

## Threat model & failure modes
- Classification leakage via annotation-only columns.
- Image file not found or corrupted; blurry handwriting; math equations + Bahasa Indonesia.
- Domain shift to new topics or different handwriting quality.
- Wrong `NONE` causing false alarms on correct answers.
- Close/confusable taxonomy codes, long-tail labels and annotation disagreement.
- Shared GPU contention / OOM; credentials exposure; unapproved external uploads.

## Your own acceptance thresholds (fill after G4)
- Minimum validation MAP@3 for promotion: TODO (must be measured, not invented).
- Max p95 latency and memory budget: TODO after profiling.
- False-alarm ceiling on `NONE`: TODO with teacher acceptance.
- Rollback trigger and human approval owner: TODO.

## Reflection questions
1. Why is predicting the final answer wrong different from diagnosing the root reasoning error?
2. How can train/validation score look high if the production model cannot read handwriting?
3. What would convince a teacher to trust or reject the model's recommendation?
4. Is a public Kaggle score equal to a production SLA? Why not?
