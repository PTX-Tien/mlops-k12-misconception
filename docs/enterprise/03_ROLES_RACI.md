# Role Charter & RACI

| Role | Trách nhiệm | Không được làm |
|---|---|---|
| Product Owner / PM | Requirement, user value, priority, sign-off business | Chỉ định thuật toán như một giả định bắt buộc khi chưa có evidence |
| Tech Lead / ML Architect | Architecture, ADR, dependencies, review technical, quality gates | Bỏ qua data leakage/security để đẩy score |
| Data Engineer (DE) | Ingestion, contract, validation, dataset lineage, split pipeline | Sửa raw data không ghi nguồn và transformation |
| ML Engineer (MLE) | Features, training, eval, calibration, inference compatibility | Sử dụng field train-only vào serving mà không tái tạo được |
| MLOps / Platform | Env, DVC, MLflow, orchestration, registry, CI/CD | Chạy workloads ngoài tài nguyên được phép |
| QA / Test Engineer | Test strategy, negatives, regression, test evidence | Chỉ dựa 4 unit tests mà tuyên bố end-to-end hoàn chỉnh |
| Security / Data Steward | Privacy, secret scanning, data rights, model/data export policy | Approve public raw data publication không có authorization |
| SRE / Release Owner | Serving SLO, telemetry, incident, rollback, change management | Auto-promote candidate không có gate |
| Independent Reviewer | Review diff, evidence, severity, independent verdict | Sửa bài thay người học, approve không có evidence |
| Learning Mentor | Explain concepts, hints stepwise, oral questions | Gửi full answer trước first submission nếu chưa được yêu cầu |

## RACI (A=Accountable; R=Responsible; C=Consulted; I=Informed)
| Activity | PM | TL | DE | MLE | Platform | QA | Security | SRE |
|---|---|---|---|---|---|---|---|---|
| Scope + business acceptance | A/R | C | I | C | I | C | C | I |
| Data license / privacy | C | C | R | I | I | C | A | I |
| Data contract + split | I | A | R | C | I | C | C | I |
| Baseline/model selection | C | A | C | R | I | C | I | I |
| CI/pipeline reproducibility | I | A | C | C | R | C | C | I |
| Acceptance tests | C | A | C | C | C | R | C | I |
| Model promotion | C | A | I | R | R | C | C | C |
| Deployment operations | I | C | I | C | R | C | C | A |
| Incident response | I | C | I | C | R | C | C | A |

Trong sandbox học, AI chỉ **mô phỏng** các role và phân công trong tài liệu. GitHub remote permissions, CI green và merge đều phải được thực thi/xác nhận thực tế.

## Handoff contract
Mọi chuyển giao có: `ticket_id`, revision, owner, changed paths, input/output, evidence links (private safe), blockers, risk, next action. Không chấp nhận “done” không kèm artifact.
