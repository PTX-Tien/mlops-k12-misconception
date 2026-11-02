# G1 Runbook — current setup failures and closure

## Known state (provided by implementer)
- Installed editable package + dependencies successfully into `.../mlops-k12-misconception/.conda`.
- `python -m pytest -q` → `4 passed`.
- `python -m ruff check src tests` → `I001` at `tests/test_metrics.py` (import sorting; trivial quality gate).
- `python -m pip freeze > reports/environment-installed.txt` was interrupted using Ctrl+C; this is **not a pip exception**.

## Safe remediation: implementer executes
```bash
ROOT=/mmlab_students/storageStudents/nguyenvd/utrg-tienptx01/mlops-k12-misconception
cd "$ROOT"
source scripts/00_private_runtime.sh
conda activate "$ROOT/.conda"

# Observe the import rule; only fix that file.
python -m ruff check tests/test_metrics.py --fix
python -m ruff check src tests
python -m pytest -q

# Save manifest atomically; avoid retaining a partial file on failed command.
python -m pip freeze > reports/environment-installed.txt.tmp &&   mv reports/environment-installed.txt.tmp reports/environment-installed.txt

test -s reports/environment-installed.txt && echo 'manifest nonempty'
which python
python --version
python -m pip --version
conda config --show pkgs_dirs envs_dirs
printf 'HF_HOME=%s\nPIP_CACHE_DIR=%s\nTMPDIR=%s\n' "$HF_HOME" "$PIP_CACHE_DIR" "$TMPDIR"
git diff --check
git status --short
```

## Review requirements for G1
- Python resolves to `$ROOT/.conda/bin/python` (not `anaconda3/bin/python`).
- Conda `pkgs_dirs` and write targets under `$ROOT/.runtime` / allowed workspace; **source before conda/pip**.
- Ruff and Pytest both successful; tests run on isolated Python.
- `environment-installed.txt` nonempty and `pip check` succeeds (add `python -m pip check`).
- No shared cache cleanup, chmod or overwrites; no `sudo`.
- `git status` / review contains only intended changes; never commit environment manifest if it exposes private internals without reviewing it.
- If freeze is still slow: inspect process/disk; do not assume failure, and don't bypass the manifest requirement.

## Submission evidence
Ticket `G1-04`: command outputs + `which python` + `conda config --show` redacted if necessary + diff of import fix + proof `test -s` + reason why lint is a merge gate.

## Server-specific caution
`python -m pip freeze` may expose editable local paths, so keep it within ignored `reports/` and redact when sharing. If user needs lock reproducibility later, create reviewed platform-specific lockfile as separate ticket.
