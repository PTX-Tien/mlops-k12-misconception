# Learning Contract: solve before being shown the answer

## Difficulty bands
- L0: Understand theory + terminology, paraphrase acceptance.
- L1: Implement standalone script/test from specification.
- L2: Build integration, prove edge cases, reason about leakages.
- L3: Design tradeoff with ADR, failures, measurable evidence.
- L4: Lead review/release, incident and root-cause analysis.

## Mentor hint policy
- HINT 0: ask probing questions only.
- HINT 1: point to affected module/concept, no code.
- HINT 2: give algorithm outline/test cases, no full implementation.
- HINT 3: pinpoint root cause with minimal pseudo code.
- SOLUTION: only after self-attempt and explicit request; mark as guided, require student to explain tradeoffs.

## Learning checkpoint after each ticket
1. Requirement in your own words.
2. Chosen design and at least 1 rejected alternative.
3. What could break? At least 1 negative test.
4. What did we measure? How reproducible?
5. Why can't we mark finished from 1 green check?
6. Can another engineer reproduce from README and hash manifest?

## Evidence requirement
Every self-study PR must include a concise decision narrative (`context → hypothesis → implementation → test → result → limitations`). A code-only submission receives `NEEDS_EVIDENCE`.
