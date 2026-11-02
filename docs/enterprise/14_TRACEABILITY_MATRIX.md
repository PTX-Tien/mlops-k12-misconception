# Requirement → Ticket → Verification Traceability Matrix (starter)

| Requirement | Primary ticket(s) | Evidence/test identifiers | Owner |
|---|---|---|---|
| FR-01 valid input | G2-03, G5-01, G10-02 | T-CONTRACT-01, T-SERVE-01 | DE/MLE |
| FR-02 top3 ranking | G3-02, G4-02 | T-METRIC-01, T-SUB-01 | MLE/QA |
| FR-03 batch predict | G4-03, G10-01 | T-BATCH-01 | MLE |
| FR-04 lineage | G4-03, G7-02 | T-LINEAGE-01 | MLOps |
| FR-05 registry/champion | G9-01, G9-02 | T-REG-01, T-PROMOTE-01 | MLOps/TL |
| FR-06 monitoring | G12-01, G12-02 | T-MON-01, T-DRIFT-01 | SRE |
| FR-07 CI/release | G1-04, G11-01, G11-02 | T-CI-01, T-CD-01 | QA/Platform |
| FR-08 human escalation | G6-03, G10-03 | T-ABSTAIN-01 | PM/MLE |
| NFR-01 reproducibility | G1-02, G3-01, G7-02 | T-REPRO-01 | TL/Platform |
| NFR-02 privacy | G0-03, G2-02, G11-03 | T-PRIV-01 | Security |
| NFR-03 portability | G1-01, G10-02 | T-PORT-01 | Platform |
| NFR-04 reliability | G10-03, G12-03 | T-RELIABILITY-01 | QA/SRE |
| NFR-05 observability | G12-01 | T-OBS-01 | SRE |
| NFR-06 isolation | G1-02, G5-03 | T-CACHE-01 | Platform |
| NFR-07 maintainability | G1-04, G11-01 | T-CODE-01 | QA |
| NFR-08 data integrity | G2-01, G7-01 | T-DATA-01 | DE |
| NFR-09 safe rollout | G9-02, G11-02, G12-03 | T-ROLLOUT-01 | SRE |

**Rule:** Không được đánh dấu requirement `SATISFIED` cho đến khi test cụ thể đã chạy và evidence có đường dẫn/run ID/commit. Bảng này là đề xuất traceability, không phải trạng thái kết quả.
