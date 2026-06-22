# QA / Acceptance / Release Gate

Use this gate after implementation and verification, before final review or launch summary.

## Purpose

Decide whether the MVP is actually ready for users, not only whether the code builds.

This gate checks product promise, core UX, technical verification, content, release readiness, known limitations, and final launch status.

## Required source inputs

- Idea Intake
- Launch Market Research
- Brand / Design System / UX Flow
- Standard Stack / Environment Preflight
- Product/Technical Brief
- Build / Deploy / Verification Plan
- OpenSpec
- Verification results
- Deployment or preview result, when applicable

## Required fields

```text
Product acceptance:
- MVP promise met:
- core user flow complete:
- must-have scope complete:
- no unapproved scope added:

UX acceptance:
- core scenarios pass:
- edge cases handled:
- empty states:
- error states:
- loading states:
- mobile check:
- desktop check:

Technical acceptance:
- primary verification command:
- verification result:
- tests/evals result:
- build result:
- deploy or preview result:
- rollback path known:

Content acceptance:
- no placeholders:
- product copy ready:
- CTAs clear:
- links work:
- legal/support notes present if needed:

Acceptance criteria coverage:
- criterion:
  evidence:
  command or check:
  status: PASS / FAIL / LIMITATION

Release readiness:
- release URL:
- analytics ready or explicitly deferred:
- support channel ready or explicitly deferred:
- known limitations documented:
- launch risks unchanged or escalated:

Final status:
PASS / BLOCKED / PASS WITH LIMITATIONS

If BLOCKED:
<blocking issues and required fix>

If PASS WITH LIMITATIONS:
<limitations, user impact, and whether human launch decision is required>
```

## Rules

- Passing build is not enough.
- Every must-have and acceptance criterion must have evidence.
- Do not ask the human to manually click through routine flows.
- Use automated checks, smoke checks, screenshots, logs, or review artifacts where possible.
- If a limitation changes product promise, risk, cost, trust, or launch quality, escalate with a Decision Card.
- If final status is BLOCKED, do not call the MVP ready.
- If final status is PASS WITH LIMITATIONS, list limitations clearly and say whether launch is still recommended.
