# Security, Data Governance & Ethics

## Default restriction
Input is handwriting of school-age students. Treat all images, CSVs, possible identifiers, transcriptions and model predictions as confidential; use only within authorized competition/education scope. Check current Kaggle competition rules and data terms before any external compute or redistribution. **Even model checkpoints may be restricted**.

## Data handling controls
- Raw data immutable, `data/raw` gitignored, checksums manifest; authorized user access only.
- Avoid direct PII and raw student imagery in PR, CI, ChatGPT prompts, public issue, model cards or MLflow screenshots.
- Do not log full image, raw handwriting/OCR text, raw CSV rows or identifying filenames in API/request logs.
- Config/credentials under `.runtime/` private (chmod 700) not `/home`/shared `anaconda3`; never commit Kaggle token or cloud secrets.
- Access by least privilege; single-person access on shared server means verify directory ACL/permission and collaborators, not assume folder name means private.
- No public deployment; any staging uses synthetic or explicitly authorized content.
- Privacy deletion/retention plan required before collecting real feedback. No arbitrary persistent raw inference logs.

## Threat model starter
Assets: student work, hidden labels, model parameters, Kaggle secrets, GitHub token. Threats: data exfiltration via agent APIs/cloud, path traversal in uploads, malicious pickle/joblib load, accidental Git commit, cross-user cache, artifact exposure, model memorization.

## Security acceptance checklist
- No secrets/data tracked by `git ls-files` or PR diff; explicit no-secrets test.
- Validate file type/size and path, permissions, safe serialization, and allowed external library downloads.
- Redact identifiers and logits tied to identifiable student; store aggregates by default.
- Threat model + risk owner + written signoff before external access.

## Legal/ethical boundary
We are building a learning prototype, **not** a substitute for a teacher. Model provides candidate diagnostics with confidence limitations; do not infer student identity or protected traits.
