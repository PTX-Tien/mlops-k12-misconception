# Practice: end-to-end simulated PR review & merge

## Scenario A: G1-04 lint fix
1. Implementer receives issue G1-04 and fixes `I001`, runs `ruff` and `pytest` using isolated Python.
2. Captures diff + env path + test results, submits markdown using template.
3. Reviewer only reads ticket + diff + evidence; issues `RECOMMEND_APPROVE` or `CHANGES_REQUESTED` with severity.
4. If no remote, label `LOCAL_REVIEW_SIMULATION`; do not claim actual merge.
5. If remote configured, open PR, observe status checks, request human approval when policy allows, merge and verify main.

## Scenario B: model regression
An ML candidate increases MAP@3 but has unacceptable `NONE` false positives or breaks train–serve parity. Agent must mark `BLOCKED`/`CHANGES_REQUESTED` even if tests are superficially green. Define what failed and what additional evidence needed.

## Scenario C: deployment incident
Simulated corrupted model artifact or invalid input overwhelms worker. SRE responds via runbook; records detection, rollback, health validation, postmortem and prevention. No GPU/production service needed initially.

## Reviewer worksheet
- Which acceptance ID(s) are proven, unproven or violated?
- Which failing test is reproduced? Do evidence and code match?
- Did any protected/competition data escape?
- Is PR narrow and reviewer-independent?
- What blocks merge? Can it be independently fixed and re-tested?
- Is the status **recommendation** or verified real GitHub `approved/merged`?
