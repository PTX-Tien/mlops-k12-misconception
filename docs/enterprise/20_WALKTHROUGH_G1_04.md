# G1-04 — Guided enterprise workflow cho lỗi hiện tại (không giải thay)

## Step 0: Tạo issue và nhận requirements
- Issue: `G1-04 Fix Ruff import gate and freeze env manifest`.
- Given: `pytest 4 passed`, `ruff I001`, `pip freeze Ctrl+C`, isolated Conda installed.
- Goal: cho chạy quality checks sạch, capture bằng chứng môi trường riêng, không chạm shared Anaconda.
- Merge-blocking acceptance: lint passed + tests passed + manifest nonempty + pip check + evidence of isolation + Git diff reviewed.

## Step 1: Tạo branch nhỏ
```bash
ROOT=/mmlab_students/storageStudents/nguyenvd/utrg-tienptx01/mlops-k12-misconception
cd "$ROOT"
source scripts/00_private_runtime.sh
conda activate "$ROOT/.conda"
git status --short
# Nếu worktree clean và Git đã init:
git checkout -b fix/G1-04-quality-gate
```

Nếu workspace có uncommitted edits, **đừng chạy git reset/clean**. Đánh giá trạng thái trước, có thể lưu patch/stash với quyết định của bạn. `git init` đã có? Chạy `git rev-parse --is-inside-work-tree` để kiểm tra.

## Step 2: Tự sửa `I001`
- Tool cho `I001` đã gợi ý: nhóm import bên ngoài và project import bằng blank line.
- Có thể chạy scoped auto-fix: `python -m ruff check tests/test_metrics.py --fix`.
- Xem `git diff -- tests/test_metrics.py`; chỉ thay đổi import formatting, không chỉnh thuật toán.

## Step 3: Test & proof
```bash
python -m ruff check src tests
python -m pytest -q
python -m pip check
python -m pip freeze > reports/environment-installed.txt.tmp && \
  mv reports/environment-installed.txt.tmp reports/environment-installed.txt
test -s reports/environment-installed.txt
which python
conda config --show pkgs_dirs envs_dirs
git diff --check
```

Không đưa toàn bộ pip freeze chứa paths private lên issue public. Chỉ báo hash/phiên bản/manifest tồn tại và trích log đã redact nếu cần.

## Step 4: Submit PR
Copy `templates/SUBMISSION.md`, ghi test matrix và one-line interpretation: `I001` là style quality gate, `4 passed` là correctness (chưa đủ để merge).

## Step 5: Independent Review (roles)
1. QA kiểm tra script/test outputs, no missing evidence.
2. Reviewer đối chiếu AC-G1-04-01…04, nhất là real Python path.
3. Nếu đề xuất approve, phải quan sát CI GitHub thực tế và reviewer người có quyền khi repository có remote.
4. Merge rồi `git checkout main && git pull` khi remote hợp lệ, xác minh `git log`/CI. Trên server một mình có thể ghi `LOCAL_REVIEW_SIMULATION`, không gọi là GitHub approved.

## Step 6: Gate closure quiz
- Tại sao shared Anaconda của bạn có lỗi PermissionError mặc dù `conda create -p` đặt env riêng?
- Tại sao `pip freeze` bị `Ctrl+C` không tự động là dependency incompatibility?
- Tại sao không thể đóng G1 dựa trên bốn unit tests pass?
- Một lệnh `git status` có thể tiết lộ file credential mới được tạo chưa được ignore thế nào?
