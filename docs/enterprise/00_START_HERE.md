# START HERE — dùng như một công ty ML thu nhỏ

## 1. Hiện trạng đã chứng minh
- Conda env riêng đã cài các dependencies và project ở `.conda`.
- `pytest -q`: 4 passed. `ruff check`: thất bại vì `I001` tại `tests/test_metrics.py`.
- `pip freeze > reports/environment-installed.txt` bị ngắt bằng Ctrl+C, **không chứng minh pip hỏng**.
- Chưa có bằng chứng G1 hoàn chỉnh (cache configuration, Python path, lint clean, manifest hợp lệ, Git status).
- Chưa có bằng chứng dataset thật, mô hình thật, PR remote hay deployment; tuyệt đối không đánh dấu đã hoàn thành.

## 2. Quy tắc học
- **Một ticket, một feature branch, một PR** (có thể nhóm documentation tickets nhỏ theo approval của TL); mỗi ticket có acceptance và evidence.
- Tự viết implementation trước; agent mặc định ở chế độ `SPEC_ONLY` và `REVIEW_ONLY`; coaching dùng mức HINT 1/2/3, chỉ có sample solution khi bạn yêu cầu sau khi đã submit lần đầu.
- Reviewer độc lập với implementer; không tự approve code mình viết; reviewer nêu line/path/evidence.
- Tất cả dữ liệu Kaggle và ảnh bài làm chỉ ở workspace private; sample CI là synthetic, CPU-only.

## 3. Bắt đầu ngay
1. Đọc `11_G1_REPAIR_RUNBOOK.md` và hoàn thành ticket `G1-04`.
2. Ghi vào `docs/enterprise/submissions/G1-04.md` theo `templates/SUBMISSION.md` (tạo khi submit).
3. Gọi QA Agent với issue `G1-04`, bằng chứng không chứa secrets; sau đó Reviewer Agent cho verdict.
4. Nếu `CHANGES_REQUESTED`, sửa trên cùng branch và submit lại. Nếu `RECOMMEND_APPROVE` và CI xanh, chủ repo có quyền merge.
5. Mở ticket kế tiếp theo dependency index; không bỏ qua G2/G3 để chạy VLM.

## 4. Cấu trúc directory chuẩn
```
docs/enterprise/
  00_START_HERE.md ... 18_REVIEW_SIMULATION.md
  tickets/G0-01.md ... G12-03.md
  agents/{role}.md
  templates/{TICKET,REVIEW,SUBMISSION,ADR,...}.md
  submissions/           # tạo local khi làm bài; review nội dung không chứa dữ liệu nhạy cảm
```

## 5. Loại Gate khác nhau
- **Learning Gate:** bạn giải thích được *vì sao* và *đánh đổi* của giải pháp.
- **Engineering Gate:** code, tests, lint và acceptance evidence đạt yêu cầu.
- **Data/ML Gate:** schema, split, leakage, metric, reproducibility và train–serve parity.
- **Release Gate:** artifact được approve và staging/rollback/monitor có bằng chứng.

Không dùng điểm leaderboard thay cho các gate kỹ thuật.
