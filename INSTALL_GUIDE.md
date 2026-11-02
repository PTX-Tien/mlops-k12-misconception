# Hướng dẫn cài governance overlay an toàn vào server hiện có

**Không giải nén đè trực tiếp vào project root.** Bộ tài liệu có thể áp dụng vào project đã tồn tại mà không làm mất diff/edits của bạn.

## 1. Tải lên
```bash
# Run on local machine (replace SSH alias as configured)
scp mlops_enterprise_overlay.tar.gz \
  utrg-tienptx01@gpu154-4029GPTRT2:/mmlab_students/storageStudents/nguyenvd/utrg-tienptx01/
```

## 2. Trên server — extract to staging, non-destructive copy
```bash
BASE=/mmlab_students/storageStudents/nguyenvd/utrg-tienptx01
ROOT="$BASE/mlops-k12-misconception"
cd "$ROOT"
source scripts/00_private_runtime.sh

# Verify archive contents before extracting.
tar -tzf "$BASE/mlops_enterprise_overlay.tar.gz" | head -30

STAGE=$(mktemp -d "$ROOT/.runtime/tmp/mlops-overlay.XXXXXX")
tar -xzf "$BASE/mlops_enterprise_overlay.tar.gz" -C "$STAGE"

# Installer skips pre-existing paths; does not write src/tests/data/.conda/.runtime.
bash "$STAGE/mlops_enterprise_overlay/scripts/install_enterprise_overlay.sh" "$ROOT"

# Review files; no automatic commit/merge.
git status --short
sed -n '1,120p' docs/enterprise/00_START_HERE.md
```

## 3. What is installed
New governance docs in `docs/enterprise/`, role-specific agent prompts, 42 ticket specs, templates, `AGENTS.md`, issue/PR templates. The installer self-copy into `scripts/` is documentation support. **Existing paths are skipped**; if you update overlay later, review diff and merge manually. Existing `README.md`, CI, source code, tests, environments, dataset and experiments are not overwritten.

## 4. First work item
`docs/enterprise/tickets/G1-04.md` → `docs/enterprise/20_WALKTHROUGH_G1_04.md` → create branch → resolve Ruff → run tests and manifest → submit `templates/SUBMISSION.md` → independent agent review → GitHub PR/merge only if configured.
