# MLOps Enterprise Learning — Governance Overlay (VI)

**Mục tiêu:** Học toàn diện Data → Model → Code → Production → Monitoring qua một dự án K12 Misconception Detection, với mô hình **ticket → self-implementation → submission → independent review → approval → merge → controlled release**.

Đây là **bộ tài liệu bổ sung**, KHÔNG thay thế source code, dữ liệu, environment hoặc lịch sử Git có sẵn. Tránh làm sẵn bài tập: người học chịu trách nhiệm code và evidence. AI agents hỗ trợ theo vai trò, không tự động có quyền approve GitHub/merge/release.

## Đọc theo thứ tự
1. `INSTALL_GUIDE.md` và `docs/enterprise/00_START_HERE.md`: cách dùng bộ này + Gate 1 hiện tại.
2. `docs/enterprise/01_PROJECT_CHARTER_SRS.md`: requirements, scope, success metrics.
3. `docs/enterprise/02_SDLC_OPERATING_MODEL.md`: lifecycle, workflow, state machine, reviews.
4. `docs/enterprise/03_ROLES_RACI.md`: PM, TL, DE, ML, MLOps, QA, SRE, Security.
5. `docs/enterprise/04_ARCHITECTURE_NFR.md`: architecture & non-functional requirements.
6. `docs/enterprise/05_BACKLOG_INDEX.md`: 42 tickets + dependencies, assign theo gate.
7. `docs/enterprise/06_ACCEPTANCE_TEST_POLICY.md`: DoR/DoD, severity, rubric, evidence.
8. `docs/enterprise/07_GIT_BRANCH_PR_POLICY.md`: GitHub workflow, branch protection.
9. `docs/enterprise/08_AGENT_WORKFLOW.md`: prompt cho nhiều agent, handoffs.
10. `docs/enterprise/09_RELEASE_MODEL_GOVERNANCE.md`: model acceptance, deployment.
11. `docs/enterprise/10_SECURITY_DATA_POLICY.md`: policy data trẻ em/Kaggle.
12. `docs/enterprise/11_G1_REPAIR_RUNBOOK.md`: lỗi Ruff/ pip freeze & closure G1.
13. `docs/enterprise/12_SELF_STUDY_CONTRACT.md`: tự giải bài theo hạn mức gợi ý.
14. `docs/enterprise/13_STANDARDS_AND_SOURCES.md`: đối chiếu chuẩn & nguồn.
15. `docs/enterprise/14_TRACEABILITY_MATRIX.md`: requirements → tickets → tests.
16. `docs/enterprise/15_EVALUATION_PROTOCOL.md`: train–serve parity, leakage, MAP@3.
17. `docs/enterprise/16_LINEAGE_AND_REPRODUCIBILITY.md`: run manifest/versioning.
18. `docs/enterprise/17_MONITORING_SRE.md`: monitoring, alert, incident, drift.
19. `docs/enterprise/18_REVIEW_SIMULATION.md`: dry-run reviewer, mock PR approval.

Tài liệu `docs/enterprise/tickets/` chứa từng issue độc lập, ghi mục tiêu, input, ràng buộc, deliverable, acceptance, evidence, reviewer, failure cases. `docs/enterprise/agents/` chứa prompt role-specific. `docs/enterprise/templates/` chứa khuôn mẫu để copy khi tạo PR/ADR/report.

## Cài vào project hiện có (an toàn)
Trên server: **giải nén vào thư mục staging** rồi chạy `scripts/install_enterprise_overlay.sh` để bỏ qua file đã tồn tại; bộ chỉ tạo file mới trong `docs/enterprise/` và `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`; **không chứa `src/`, `tests/`, `.conda/`, `.runtime/`, `.github/workflows/ci.yml` hay `README.md` gốc**. Xem `INSTALL_GUIDE.md` với hướng dẫn chi tiết. Trước khi giải nén, kiểm tra `tar -tzf` và các file đã có nếu từng áp dụng overlay. Không giải nén bằng sudo.

## Quan trọng
- `4 passed` là test pass, nhưng lint `I001` vẫn fail. Xem G1 runbook.
- Không thể tuyên bố GitHub PR merged nếu chưa có remote, permissions, CI thật. Local reviewer verdict chỉ là mô phỏng.
- Mọi action cài đặt/đào tạo/serve thật đều do người học thực thi; agent không chạy GPU hay publish private data.
- Chương trình sử dụng server Linux nhiều người dùng: luôn source `scripts/00_private_runtime.sh` trước Conda/pip.
