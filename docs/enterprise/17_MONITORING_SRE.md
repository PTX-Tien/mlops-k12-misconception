# SRE Monitoring, Drift, Feedback & Incident

## Monitoring taxonomy
- **Service:** request rate, error rate, latency p50/p95, memory, GPU pressure, loading failures.
- **Data:** schema failures, missing/OOD features, image size distribution, OCR parse failure (if authorized), label shift proxy.
- **Model:** prediction distribution, `NONE` rate, confidence/abstain rate; ground-truth metrics only when verified labels arrive (delayed evaluation).
- **Business:** teacher-reviewed usefulness, correction counts — synthetic/authorized only.

## Alert design
Define baseline with observation window, sample volume and false-positive policy. No arbitrary threshold presented as validated. Alerts categorized INFO/WARN/CRITICAL with owner/on-call and escalation.

## Incident lifecycle
`DETECT → TRIAGE → CONTAIN → RESTORE → VERIFY → POSTMORTEM → PREVENT`. Every incident captures timeline, impact (no sensitive payload), trigger, decision, model version, mitigation and tests preventing recurrence.

## Safe retraining flow
Alert is **not** a retrain command. Open dataset review/change ticket; approved labeled data + contract → frozen evaluation → candidate training → acceptance → manual promotion. If feedback data unavailable, demonstrate on synthetic drift data only.

## Mandatory tabletop exercises
1. `Input invalid`: contract handles gracefully.
2. `Model artifact checksum mismatch`: reject load, continue champion.
3. `Candidate regression`: model gate rejects despite green CI.
4. `Data drift false alarm`: analyze drift and decide **no retrain**.
5. `Latency spike/VRAM shared contention`: mitigation without killing other users' processes.
