# Data / Code / Model Versioning & Lineage

## Run manifest schema (proposed)
```yaml
run_id: TODO
ticket_id: G4-03
git_sha: TODO
python_version: TODO
env_lock_hash: TODO
raw_dataset_hash: TODO
split_hash: TODO
config_hash: TODO
seed: 42
model_artifact_hash: TODO
metric_definition_version: map_at_3_v1
metrics: {}
resource_profile: {}
limitations: []
```

## Reproducibility ladder
R0: same input/seed yields identical split hashes. R1: fresh environment installs dependencies reliably. R2: same fixed code/data/config produces predictions within declared deterministic/numeric tolerance. R3: DVC pipeline reproduces stages and artifacts. R4: registry version immutable and deployment loads exactly that version.

## DVC data policy
- Raw data checksum tracked; DVC metadata in Git only if license allows; DVC cache/remote private.
- Never commit large data or artifacts to public Git; evaluate metadata leakage through filenames.
- DVC `repro` must NOT overwrite frozen split/outputs silently without explicit version/run path policy.

## MLflow requirements
- Run links to Git, data, split, config, seed and metrics; artifact content checked for privacy.
- Registry `candidate`/`champion` managed with alias/versions; SQLite local suitable for educational lab, security and backup configured before multiuser server.
- Never serve MLflow server on public interface without access restrictions; default localhost.

## Dependency/lockfile policy
Pip freeze in ignored `reports/` is a snapshot, not necessarily portable lockfile. Later create intentional lock for Python 3.11 target environment, pin packages/constraints and document GPU compatibility and platform-specific wheels.
