## Linked issue/ticket
`Gx-yy`: [link to ticket](docs/enterprise/tickets/)

## What/Why / Out of scope
- Motivation:
- Scope:
- ADR (if needed):

## Acceptance evidence
| AC | Evidence (safe summary or CI link) | PASS? |
|---|---|---|
| | | |

## Tests and governance
- [ ] `python -m pytest -q` passed (attach CI link)
- [ ] `python -m ruff check src tests` passed
- [ ] `git diff --check` passed
- [ ] Synthetic negative path tested
- [ ] No secret, Kaggle data, student image, private model artifacts or raw OCR text
- [ ] Only serving-available model features
- [ ] Dataset/run/config/hash and release gate documented where applicable

## Risk/rollback
Reviewer required roles, failure/recovery path, remaining limitations.

## Implementation note
I solved this myself / Guided by AI: ____ (disclose extent).

**PR approval/merge only occurs after actual required reviewers/checks, not AI recommendation.**
