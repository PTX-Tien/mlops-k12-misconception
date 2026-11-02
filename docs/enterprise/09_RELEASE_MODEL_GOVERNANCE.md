# Model Registry, Acceptance & Release Governance

## Distinct lifecycle states
`EXPERIMENT → CANDIDATE → VALIDATED → APPROVED_FOR_STAGING → STAGING_VERIFIED → CHAMPION`.

Candidate model may be rejected. No automatic champion promotion on one metric. Champion is an **alias** to an immutable version, not an overwritten file (MLflow registry supports aliases). Rationale: rollback.

## Before model candidate registration
- Metadata model card including training data rights, license, sensitive limitations, code/config/data hashes.
- Evaluation protocol frozen before comparing; MAP@3, class/`NONE` errors, uncertainty, coverage, latency/memory on permitted hardware.
- No `transcription_steps` unless OCR provided in serving; no official test selection.
- Detect out-of-distribution/corrupt inputs and define abstention path.
- Artifact loader must work offline in staging (no undocumented downloads).

## Promotion decision record
Input: candidate version, champion version, predeclared thresholds, validation report, robustness, resource test, security signoff. Decision: APPROVE, REJECT, HOLD. Include reason, approver, time, rollback ID. Unfilled means NOT APPROVED.

## Staging rollout
1. Load pinned immutable model; verify checksums and compatible schema.
2. Smoke 5–20 sanitized synthetic test requests, valid and invalid.
3. Verify p50/p95 latency, error rates and telemetry without PII; actual thresholds documented after profiling.
4. Run parity test batch vs API outputs on synthetic inputs.
5. Perform rollback dry-run; record before production-like serving.
6. Approve rollout only if governance and license allow it (lab stays private).

## Failure injection
- Regressing MAP@3 / excessive NONE false positives → reject candidate.
- Corrupt model checksum → loader blocks, last champion still available.
- Invalid request/oversized image → controlled 4xx or error response, no crash.
- Simulated drift trigger → open retrain ticket, do not mutate champion automatically.
