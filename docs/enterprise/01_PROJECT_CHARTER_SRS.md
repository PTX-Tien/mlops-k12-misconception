# Project Charter / SRS v0.1 — ML Product Requirements

**Product:** K12 Misconception Insight (internal learning prototype). **Sponsor:** giả lập nhóm giáo viên/nhà nghiên cứu giáo dục. **Implementation owner:** người học. **Approval authority:** người quản lý repository thực tế.

## User problem / JTBD
Giáo viên cần gợi ý đến 3 mã hiểu sai tiềm năng từ ảnh bài giải toán viết tay + ngữ cảnh câu hỏi; dự đoán chỉ là **decision support**, không kết luận tự động về học sinh. Mỗi inference trả `top3_root_codes`, `model_version`, `prediction_time`, `status`; có cơ chế abstain/escalate khi không đủ tin cậy.

## In scope
- Nắm vững data/ML/code lifecycle, reproducibility, CI, staging serving, monitoring và rollback.
- Xây pipeline offline cho ảnh + metadata được phép; so sánh engineering baseline và model đọc nội dung bài làm.
- Kiểm toán phân phối nhãn và các lỗi None/rare-class, split leakage; batch và HTTP inference trên môi trường **nội bộ**.
- Human-in-the-loop và mô phỏng drift/retraining trên dữ liệu synthetic/authorized.

## Out of scope (chưa có phê duyệt)
- Public API / dịch vụ thương mại, chia sẻ ảnh/học sinh, external upload dữ liệu cá nhân.
- Tự động gắn nhãn/ra quyết định đánh giá học sinh không có người kiểm tra.
- Tự động fine-tune model/API không được phép theo rule cuộc thi.
- Tối ưu Kaggle LB bằng lặp đi lặp lại trên public test; không xem LB là validation.

## Functional Requirements (FR)
| ID | Requirement | Acceptance intent |
|---|---|---|
| FR-01 | Nhận input ảnh bài làm, question context, optional question image | Contract rejects malformed and forbidden fields |
| FR-02 | Trả rank top-3 root code (bao gồm `NONE` nếu hợp lệ) | Deterministic ranking, unique classes, official-compatible format |
| FR-03 | Cho phép CLI batch prediction và offline evaluation | Validation output and sample submission conformity |
| FR-04 | Trace run: Git SHA, data hash, config, seed, metrics, model hash | Một run có đầy đủ lineage |
| FR-05 | Candidate registry, champion version, rollback | Failure cannot promote automatically |
| FR-06 | Monitoring runtime/quality/feedback | Synthetic alert + incident + decision captured |
| FR-07 | CI lint/unit/synthetic integration; CD staging with approvals | Green checks + permission to promote |
| FR-08 | Human review and abstain path for uncertain predictions | Explicit escalation, no silent high-impact decision |

## ML success & measurement
- **Primary (competition):** local MAP@3 trên protocol freeze được mô tả; không đặt target số chưa có baseline.
- **Safety:** `NONE` false-positive diagnostics, macro/per-class coverage, label validity, corruption/missing input handling.
- **Engineering:** deterministic seeded split, reproducible pipeline, no privileged feature, cache isolation, code-quality.
- **Operational:** p50/p95 latency / error rate / peak VRAM phải đo thực tế trước khi thiết lập SLO; không ngụy tạo.
- **Promotion rule:** preset threshold sau khi có baseline, phi test leakage, provenance, checks pass, manual approval. Không tự nâng champion vì chỉ tăng MAP@3 rất nhỏ.

## Stakeholders & tradeoffs
Giáo viên: thích giải thích và hạn chế gán sai; ML Engineer: MAP@3; Infra: giá thành/latency; Data steward: privacy; QA: auditability. ADR khi tradeoff accuracy–latency–privacy.

## Assumption register
- Các trường CSV dự kiến: `trace_id`, `question_id`, `root_code`; context có thể gồm `question_text`, `correct_answer`, `grade`, `topic_name`, `question_image_file`. Xác minh schema thật ở G2.
- `transcription_steps` chỉ có ở train, không có ở test/serving: giả định lấy từ tài liệu challenge; xác minh với data thực tế.
- Phải kiểm tra các điều khoản Kaggle/HF, licensing model, external compute trước khi tải dữ liệu/training.
- Đối tượng là trẻ em: mặc định dữ liệu có độ nhạy cao, không lưu raw input/label trong public logs.

## Sign-off record (điền khi G0 hoàn thành)
| Owner | Version | Date | Decision | Evidence |
|---|---|---|---|---|
| PM | v0.1 | TBD | PENDING | |
| Tech Lead | v0.1 | TBD | PENDING | |
| Security | v0.1 | TBD | PENDING | |
