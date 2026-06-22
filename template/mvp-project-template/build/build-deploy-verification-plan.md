# Build / Deploy / Verification Plan

Build goal:

Source inputs:
- Idea Intake:
- Launch Market Research:
- Brand / Design System / UX Flow:
- Standard Stack / Environment Preflight:
- Memory Preflight:
- Product/Technical Brief:

Stack:

Architecture:

Deployment plan:
- Deploy target:
- Deploy method:
- Production URL:
- Preview URL:
- Rollback:
- Required project settings:
- Missing decisions:

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
- Goal:
- Scope:
- Non-goals:
- Files likely touched:
- Expected checks:
- Verification command:
- Stop conditions:

Acceptance Criteria mapping:
- Criterion:
  Verification:
  Command:

Test strategy:
- Static checks:
- Type checks:
- Unit tests:
- Integration tests:
- E2E / smoke tests:
- Content or schema validation:
- LLM evals, if AI behavior exists:
- Visual / UX smoke check:
- Deploy smoke check:
- Regression tests:

Verification commands:
- Primary:
- Secondary, if needed:

Autonomous repair loop:
1. Implement slice.
2. Run verification.
3. Inspect failures.
4. Repair inside approved scope.
5. Rerun verification.
6. Repeat until pass or stop condition.
7. Deploy preview when available.
8. Run deploy smoke check.
9. Summarize final result and decisions needed.

Stop conditions:
- Missing project access or settings:
- Paid service decision required:
- External service value required:
- Deploy path blocked:
- Tests contradict acceptance criteria:
- Scope starts growing:
- Same failure repeats 3 times:
- Approved stack must change:
- Shared resource would be affected:
