# Pre-launch Iteration Update

Use this mandatory loop after deploy/check/review cycles and before launch.

This is not a user-results review. There are no external users yet.

## Purpose

Keep improving the MVP until the owner explicitly says it is ready to launch.

The loop is:

```text
Build / Deploy / Verification Plan
→ implementation slice
→ verification
→ deploy or preview check
→ QA / Acceptance / Release Gate
→ Pre-launch Iteration Update
→ update Build / Deploy / Verification Plan
→ next implementation slice
```

This loop continues until the owner explicitly says:

```text
ready for launch
```

or an equivalent explicit approval.

## What this update covers

Use this update for pre-launch changes in:

- layout;
- content;
- business logic;
- features;
- UX;
- bugs;
- analytics;
- support;
- deploy or infra.

## Required fields

```text
Iteration date:

Source:
- QA / Acceptance result:
- Review result:
- Founder/product feedback:
- Design/content review:
- Failed verification:
- New constraint:

Change category:
layout / content / business logic / feature / UX / bug / analytics / support / deploy / infra

Problem:
<what is wrong or incomplete>

Decision:
<what will change>

Build Plan update:
<which section of Build / Deploy / Verification Plan must be changed>

Acceptance Criteria update:
<which criterion changes or which new criterion is added>

Next implementation slice:
<what Codex does next>

What not to change:
<what must remain unchanged>

Status:
continue loop / blocked / ready-for-owner-review
```

## Rules

- This is mandatory after every non-final QA / Acceptance / Release Gate.
- This is mandatory after every deploy/preview check until the owner says the MVP is ready to launch.
- Do not treat a passing build or deploy as launch approval.
- Do not move to GTM because this loop passed.
- Do not expand scope without a Decision Card.
- Every update must return to Build / Deploy / Verification Plan.
- Every next slice must be small and verifiable.
- The loop stops only when the owner explicitly approves launch readiness.
