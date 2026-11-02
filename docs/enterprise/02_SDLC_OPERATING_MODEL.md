# SDLC Operating Model — quy trình thực tế

## End-to-end state machine
`BACKLOG → REFINED → READY → IN_PROGRESS → SELF_TESTED → IN_REVIEW → {CHANGES_REQUESTED | APPROVED} → MERGED → VERIFIED → CLOSED`

- `BLOCKED`: state phụ có blocker và owner (không đánh đồng với DONE).
- `REOPENED`: khi regression/incident phá acceptance đã đóng.
- `APPROVED` nghĩa là người có quyền hoặc policy thực đã approve PR; Agent chỉ cho `RECOMMEND_APPROVE`.
- `MERGED` nghĩa là PR có merge commit/squash commit thực; không tự khai nhận qua hội thoại.
- `VERIFIED` nghĩa là post-merge/staging checks tương ứng đã đạt; `CLOSED` có nghiệm thu và cập nhật docs.

## Chu kỳ một ticket (tránh bàn giao suông)
1. PM phát hiện problem, viết user story, measurable outcome.
2. TL xem dependency, design questions, DoR, nhận `READY`.
3. Implementer tạo branch, viết ngắn `Implementation Plan` và rủi ro; tự code + tự test.
4. Submit PR kèm issue link, evidence, run config, screenshots **đã redact**, limitations.
5. CI thực chạy; QA đối chiếu test plan; Security nếu động đến dữ liệu/secrets/network.
6. Independent reviewer xem **diff + test evidence + artifacts + requirements**, phải tạo review có mức độ severity.
7. Nếu blocker: `CHANGES_REQUESTED`; cập nhật cùng branch, chạy lại tests, yêu cầu re-review.
8. Nếu pass: người có quyền approve rồi merge; verify post-merge; cập nhật backlog/decision log.

## Meetings/cadence (mô phỏng)
- Planning 30–45 phút/gate: scope, priority, dependencies, risks.
- Async daily update: Done / Next / Blocker / Evidence; chỉ 3–6 câu.
- Review trước merge: thay đổi, regression, data governance.
- Gate demo: mô phỏng happy path + negative test + giải thích vì sao đúng.
- Retro mỗi G3/G6/G9/G12: what changed, what failed, prevention.

## Definition of Ready (DoR)
- Problem & why rõ; input/output contract; dependencies pass; scope excluded; expected deliverables; kiểm thử độc lập; reviewer gán; có dữ liệu hợp lệ/an toàn.
- Không có test plan hoặc không có cách tái lập => chưa READY.

## Definition of Done (DoD) chung
- Acceptance được kiểm chứng với paths/commands, tests pass, lint clean.
- Không chứa dữ liệu riêng tư/secrets; code nhất quán project conventions.
- Có changelog hoặc docs nếu thay đổi API/schema/pipeline.
- Evidence và môi trường reproducible; error handling được kiểm thử.
- Reviewer khuyến nghị approve; authority thực tế approve/merge; post-merge verify.

## Khi làm một mình
Tách ba phiên rõ: **Builder (bạn)**, **Reviewer Agent (không được sửa code)**, **Release Owner (bạn với quyền Git)**. Không cho cùng một agent vừa implement vừa review. Khuyến nghị lưu review record trong `docs/enterprise/submissions/` (nếu chứa thông tin môi trường nhạy cảm, lưu local, không commit).
