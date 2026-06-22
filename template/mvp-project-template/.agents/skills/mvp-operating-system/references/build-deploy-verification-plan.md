# Build / Deploy / Verification Plan

Use this gate after Product/Technical Brief and before OpenSpec or implementation.

## Purpose

Give Codex everything needed to build, run, check, repair, deploy, and smoke-test the MVP without asking the human for terminal work.

Codex stops only when a real product, scope, budget, risk, or project-access decision is required.

## Required fields

```text
Build goal:
<what must be ready after implementation>

Source inputs:
- Idea Intake:
- Launch Market Research:
- Brand / Design System / UX Flow:
- Standard Stack / Environment Preflight:
- Memory Preflight:
- Product/Technical Brief:

Stack:
<approved stack from preflight>

Architecture:
<main modules, data model, integrations, content model, background jobs, if any>

Deployment plan:
- deploy target:
- deploy method:
- production URL:
- preview URL:
- rollback:
- required project settings:
- missing decisions:

Implementation slices:
1. Bootstrap / setup
2. Core data or content model
3. Main user flow
4. UI according to design system
5. Edge cases and states
6. Tests / evals
7. Deploy preparation
8. Deploy smoke check

Slice format:
- goal:
- scope:
- non-goals:
- files likely touched:
- expected checks:
- verification command:
- stop conditions:

Acceptance Criteria mapping:
- Criterion:
  Verification:
  Command:

Test strategy:
- static checks:
- type checks:
- unit tests:
- integration tests:
- e2e / smoke tests:
- content or schema validation:
- LLM evals, if AI behavior exists:
- visual / UX smoke check:
- deploy smoke check:
- regression tests:

Verification commands:
- primary:
- secondary, if needed:

Autonomous repair loop:
1. implement slice
2. run verification
3. inspect failures
4. repair inside approved scope
5. rerun verification
6. repeat until pass or stop condition
7. deploy preview when available
8. run deploy smoke check
9. summarize only final result and decisions needed

Stop conditions:
- missing project access or settings:
- paid service decision required:
- external service value required:
- deploy path blocked:
- tests contradict acceptance criteria:
- scope starts growing:
- same failure repeats 3 times:
- approved stack must change:
- shared resource would be affected:
```

## Rules

- Do not give Codex one large task to build the whole MVP.
- Turn implementation into small approved slices.
- Every acceptance criterion must map to a test, eval, smoke check, or explicit manual-free verification step.
- A passing build is not enough; deploy smoke checks are required when deployment is part of the MVP.
- If a blocker is about project access, budget, product promise, risk, or scope, create a Decision / Access Card.
- Do not ask the human to run commands, paste logs, inspect files, or manually confirm routine checks.
