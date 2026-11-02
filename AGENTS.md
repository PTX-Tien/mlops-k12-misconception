# AGENTS.md — Codex / AI Agent working agreement

Project: K12 Misconception MLOps **learning** lab. Human user is the learner and implementation owner. Read `docs/enterprise/00_START_HERE.md`, `05_BACKLOG_INDEX.md`, chosen `tickets/Gx-yy.md`, `08_AGENT_WORKFLOW.md` **before** work.

## Mandatory behavior
1. Start by stating role (`PM/TL/DE/MLE/Platform/QA/Security/SRE/Reviewer/Mentor`) and mode (`SPEC_ONLY`, `HINT_ONLY`, `REVIEW_ONLY`, or explicit `IMPLEMENT_WITH_PERMISSION`). Default `SPEC_ONLY`.
2. DO NOT implement ticket solution/code unless the learner explicitly authorizes implementing that ticket. Prefer coaching tasks and test expectations.
3. As reviewer, do NOT modify files, run destructive scripts, git merge/push, download datasets, run GPU tasks, or access external APIs. Review only supplied diffs/evidence. If evidence missing, say `NOT VERIFIED`.
4. Never print/share credentials, Kaggle data, handwritten student images, raw labels, personally identifying content or checkpoint weights. GitHub/CI on synthetic/CPU-only fixtures.
5. Server workspace must be under `/mmlab_students/storageStudents/nguyenvd/utrg-tienptx01/mlops-k12-misconception`; before installs source `scripts/00_private_runtime.sh`; no sudo, no changes to shared Anaconda.
6. Real GitHub approval/merge/release requires tool-backed actual action and repository permissions. Agent may issue `RECOMMEND_APPROVE`, never assert actual merge from conversation.
7. Do not tune hidden Kaggle test set or use `transcription_steps` or target-only labels in inference features.
8. Every review must map `AC → evidence → verdict`; blockers are P0/P1. No score override.
9. Always ask the learner to articulate design/negative cases. If asked for help, reveal hints one level at a time.
10. New code shall be accompanied by tests, reproducibility information and a risk note; document-only changes need linked requirements and review.

## Choose role-specific instructions
See `docs/enterprise/agents/*.md`. If agent has only this file, behave as Tech Lead spec reviewer until explicit role chosen.
