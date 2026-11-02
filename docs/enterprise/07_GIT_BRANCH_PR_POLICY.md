# Git/GitHub Governance — chưa cấu hình remote thì đây là policy, không phải enforcement

## Branching
- `main`: stable, protected when remote supports it; never develop directly.
- `feat/G3-02-group-split`, `fix/G1-04-quality-gate`, `docs/G0-02-srs`: one ticket/branch.
- Commit format: `feat(data): ...`, `fix(test): ...`, `docs(mlops): ...` + ticket ID in body/PR.
- Small PR, no magic notebook state; notebook outputs stripped if commit; freeze data/config hashes.

## PR sequence
1. `git switch -c fix/G1-04-quality-gate` (Git 2.25 supports `git checkout -b ...` if `switch` unavailable).
2. Check change with `git diff --check` and `git status`.
3. Run tests; capture private-safe evidence; submit PR body using `.github/pull_request_template.md`.
4. QA + Reviewer assess diff; no blanket approval based on green test alone.
5. After all checks pass and actual permissions approve, merge via GitHub UI/CLI; verify commit on main.

## Branch rules to configure AFTER remote created
Require PR for main; >=1 human approval when team available; require conversation resolution; require checks `unit-tests` **as it appears on Actions** and other validated checks; block force pushes/deletion; restrict bypass. On single-person account, true independent human approval may not be available. In that case use AI review as non-authoritative practice, but explicitly record `solo-simulation` and do not mislabel it as enforced.

## CI/GitHub Actions boundary
- Workflow currently `.github/workflows/ci.yml` checks pytest + Ruff CPU only. Do not change job name without updating branch rule.
- Runner should not download competition images or access student data.
- Keep secrets in approved secret store; never dump tokens into logs/PR.
- Do not activate shared server GPU or publish image artifacts from CI.
- Review `CODEOWNERS` only when real GitHub usernames/team names exist; do not invent them.

## Release vs code merge
Merged code does NOT automatically approve candidate model or deployment. Model registry aliases/production require separate model/release gate with accountable owner.

## Native GitHub manual settings
Repository → Settings → Branches/Rulesets → main → require pull request, reviews/status checks, no force-push. Depends on repository plan/permissions. Docs: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
