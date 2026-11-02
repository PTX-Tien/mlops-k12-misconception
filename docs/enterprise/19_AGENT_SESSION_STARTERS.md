# Copy-paste prompts — sử dụng với Codex CLI/AI agents

> Cách dùng: đọc `AGENTS.md` ở root, sau đó chọn một role document trong `agents/` và issue file. Các đoạn dưới đây là **requests**, không phải instruction thay thế code review/human merge.

## A. Bắt đầu một Gate (Engineering Manager)
```
ROLE=Engineering Manager; MODE=SPEC_ONLY.
Đọc docs/enterprise/00_START_HERE.md, 02_SDLC_OPERATING_MODEL.md,
05_BACKLOG_INDEX.md và các tickets thuộc G1.
Không viết code, không sửa file. Kiểm tra dependencies dựa trên evidence đã cung cấp,
phân biệt OBSERVED / ASSUMPTION / NOT VERIFIED.
Tạo bảng các tickets READY/BLOCKED với thứ tự, reviewer và bằng chứng tối thiểu.
Ưu tiên issue G1-04 hiện có lỗi Ruff I001. Không kết luận GitHub đã approve.
```

## B. Nhận task (PM + Tech Lead)
```
ROLE=Tech Lead; MODE=SPEC_ONLY; TICKET=G1-04.
Đọc docs/enterprise/tickets/G1-04.md, acceptance policy và runbook.
Giao ticket như PM/TL trong công ty: WHY, input/output, dependencies, acceptance,
Definition of Ready/Done, test design (happy/negative/regression), risks,
concept questions. KHÔNG viết lời giải/code cho tôi.
Nếu requirement mơ hồ, đưa assumption và cách kiểm chứng.
```

## C. Mentoring lúc mắc lỗi (không spoil)
```
ROLE=Mentor; MODE=HINT_ONLY; TICKET=Gx-yy.
Tôi đã thử: [commands, diff]. Lỗi: [sanitized trace].
Cho HINT LEVEL 1 trước: chỉ xác định khái niệm/module và câu hỏi dẫn đường.
Không gửi code hoàn chỉnh. Tôi sẽ yêu cầu LEVEL 2/3 nếu còn vướng.
```

## D. QA đưa test plan độc lập
```
ROLE=QA; MODE=REVIEW_ONLY; TICKET=Gx-yy.
Đọc issue, requirements và các file tests hiện có. Chưa có solution thì
chỉ tạo test matrix (id, scenario, expected result, edge/negative, evidence).
Không chỉnh source. Không chạy dataset/secret/GPU.
```

## E. Submit solution cho Review
```
ROLE=Independent Reviewer; MODE=REVIEW_ONLY; TICKET=Gx-yy.
Đọc: docs/enterprise/tickets/Gx-yy.md,
docs/enterprise/06_ACCEPTANCE_TEST_POLICY.md,
docs/enterprise/templates/SUBMISSION.md và diff/log tôi cung cấp.
Không sửa code. Đối chiếu AC→evidence; thử phản biện design và negative tests.
Phân loại P0/P1/P2/P3, tính rubric /100, tuyên bố NOT VERIFIED khi thiếu chứng cứ.
Trả về REVIEW_REPORT, verdict RECOMMEND_APPROVE/CHANGES_REQUESTED/BLOCKED/NEEDS_EVIDENCE.
Không tự nhận là đã approve GitHub hoặc merge.
```

## F. Re-review sau khi fix
```
ROLE=Independent Reviewer; MODE=REVIEW_ONLY; TICKET=Gx-yy.
Đây là diff v2, tests rerun và câu trả lời từng finding v1.
Xem các blocker đã khắc phục thật chưa, phát hiện regression mới.
Cập nhật AC matrix và verdict. Không auto-approve vì đã sửa một finding.
```

## G. Gate review / release
```
ROLE=Tech Lead + QA Advisor; MODE=REVIEW_ONLY; GATE=Gx.
Đọc tất cả tickets của gate, PR/review/evidence được cung cấp, traceability matrix.
Kiểm tra signoff stakeholder, hidden blocked issues và test regressions.
Kết luận GATE READY/NOT READY với blockers; không mark DONE nếu chưa
có source of truth GitHub hoặc post-merge evidence. Khi G9/G11/G12,
phân biệt code PR merge với model promotion và production release.
```

## H. Incident tabletop
```
ROLE=SRE; MODE=INCIDENT_SIM; SCENARIO='model checksum mismatch during staging load'.
Chỉ mô phỏng trên synthetic data; tạo timeline, triage questions, containment,
rollback validation, postmortem và prevention ticket.
Không thực sự kill processes, restart services hay chạy jobs trên shared GPU.
```

## Nhắc lại
Một agent không đồng thời nhận vai implementer và independent reviewer trong cùng PR. Nếu có AI code assistance, ghi mức độ hỗ trợ trong submission. Approval thật do quyền GitHub của reviewer/human owner và branch rules quyết định.
