# Pre-launch Iteration Update loop — 2026-06-22

## Result

Added a mandatory pre-launch iteration loop.

## Purpose

Before users, MVP work cycles through layout, content, business logic, features, UX, bugs, analytics, support, and deploy/infra fixes.

After each non-final deploy/check/review cycle:

```text
QA / Acceptance / Release Gate
→ Pre-launch Iteration Update
→ update Build / Deploy / Verification Plan
→ next implementation slice
```

The loop continues until the owner explicitly says the MVP is ready to launch.

## Added

- `skill/mvp-operating-system/references/pre-launch-iteration-update.md`
- `template/mvp-project-template/.agents/skills/mvp-operating-system/references/pre-launch-iteration-update.md`
- `template/mvp-project-template/iteration/pre-launch-iteration-update.md`

## Updated

- skill workflow
- template skill workflow
- AGENTS post-implementation rules
- README
- how-to-start docs
- operating principles
- template README
- bootstrap check
- DECISIONS.md
