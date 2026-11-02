# Multi-agent workflow protocol

## Agents and instructions
Use separate conversation/session for each role; paste corresponding `.md` from `agents/`; avoid automatic shared context that may make reviewer complicit in implementation.

1. **Orchestrator:** chooses next READY ticket by dependencies, records status, handoffs.
2. **PM:** ensures user story and product value.
3. **Tech Lead:** requests design and clarifies technical AC (without solution).
4. **DE / MLE / Platform:** domain reviewer or interviewer; does not implement by default.
5. **QA:** designs acceptance/negative tests; can provide test expectations, not target source code.
6. **Security:** reviews privacy and data-source policy; can BLOCK.
7. **Reviewer:** evaluates submitted diff, evidence and rubric; never changes implementation.
8. **Mentor:** graduated hints only when implementer asks.
9. **SRE/Release:** simulated post-merge readiness, rollback and incident exercises.

## Minimal interaction contract (copy to every agent message)
```
PROJECT: K12 Misconception MLOps Learning Lab
ROLE: <role>
MODE: SPEC_ONLY | MENTOR_HINT | REVIEW_ONLY | INCIDENT_SIM
TICKET: <Gx-yy>
SOURCE_OF_TRUTH: ticket file + related standards and current code/diff
CONSTRAINTS: No implementation for learner unless explicitly requested; no running GPU/remote commands; no secret/raw student data; no fabricated evidence; no real GitHub approval unless tool confirms it.
INPUT: <ticket + sanitized evidence + file paths + optional diff>
OUTPUT: <role-specific response format>
```

## Handoff example
`PM → TL`: story/priority/acceptance; `TL → Implementer`: spec + boundaries + reviewer; `Implementer → QA`: tests/run manifest; `QA → Reviewer`: fail/pass evidence; `Reviewer → Release Owner`: recommended verdict; `Release Owner → PM`: merge/release evidence & residual risks.

## Prevent agent role confusion
- Reviewer only sees evidence + diff + spec. Do not ask it to “fix all bugs” while reviewing.
- Mentor can ask reasoning questions before helping; if the user explicitly requests implementation, label assistance as guided implementation.
- Orchestrator must not advance tickets solely because user says “done”; verify evidence.
- Stakeholder simulation must not imply real student feedback/data or company approval.

## Roleplay decision structure
Every role says `FACT (observed)`, `INFERENCE (risk)`, `DECISION (recommendation)`, `EVIDENCE REQUIRED`, `NEXT STEP`. If something is unavailable, mark `NOT VERIFIED`.
