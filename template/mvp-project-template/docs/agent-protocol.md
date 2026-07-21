# Codex Agent Protocol

This file defines how Codex agents coordinate work in this repository.

MVP OS remains the source for what to do. This protocol defines how agents work around that source.

## Source of truth

Do not rely on prior chat history.

Use these files as the project control plane:

- `product/idea-intake.md`: scoped idea, user, MVP promise, scope, non-goals.
- `market/launch-market-research.md`: launch market facts and risks.
- `product/brand-design-ux.md`: product, brand, UX, user-facing acceptance.
- `ops/environment-preflight.md`: stack and environment readiness.
- `build/build-deploy-verification-plan.md`: architecture, slices, checks, permissions, stop conditions.
- `openspec/`: agent-readable requirements, proposal, and tasks.
- `qa/acceptance-release-gate.md`: launch readiness evidence.
- `iteration/pre-launch-iteration-update.md`: next loop after non-final checks.
- `DECISIONS.md`: durable product, technical, and process decisions.

`docs/project-state.md` is only a status index. It must not introduce requirements that are not present in the source files above.

## Roles

### release_manager

Owns coordination and readiness.

- Reads all control-plane files before assigning work.
- Chooses the next P0/P1 blocker or implementation slice.
- Uses specialist agents only when their role is needed.
- Consolidates evidence from diffs, commands, checks, logs, review findings, and docs.
- Updates `docs/project-state.md`.
- Reports `ready for owner review`, not final launch approval.

### architect

Owns scope and consistency.

- Checks that scope, acceptance criteria, architecture, and tasks do not contradict each other.
- Checks the observable outcome, full end-to-end chain, and ordered reuse discovery before implementation.
- Updates planning docs only when needed.
- Does not implement product code.
- Does not expand scope without a Decision Card.

### implementer

Owns approved implementation slices.

- Implements only slices from `build/build-deploy-verification-plan.md` or `openspec/tasks.md`.
- Makes the smallest safe code change.
- Runs relevant checks.
- Updates `docs/project-state.md` and the relevant task status.
- Records blockers instead of silently stopping.

### devops_qa

Owns setup, deployment, smoke checks, logs, and release evidence.

- Verifies commands, env vars, migrations, seed data, deploy path, and smoke tests.
- Uses browser checks for web UI flows when applicable.
- Verifies the exact target environment, inspected desktop/mobile screenshots,
  DOM, real clicks, state transitions, console/network/overflow, public
  post-deploy behavior, fingerprints, and rollback when applicable.
- Updates `qa/acceptance-release-gate.md`, `docs/project-state.md`, and release notes/runbook docs when present.
- Does not add product features.

## Coordination rules

- Use one repository as the coordination surface.
- Prefer separate branches or Codex worktrees for parallel work.
- Do not work directly in `main`.
- Do not make unrelated refactors.
- Do not create requirements in chat; write durable requirements to the proper source file.
- Do not mark work done without checks or a documented reason checks could not run.
- Do not let an agent approve its own major technical artifact.
- Close reviewer findings with a separate repeat review after fixes.
- Do not run concurrent builds that write to the same mutable output directory.
- Roll back a public deploy when required post-deploy browser QA fails.

## Human escalation

Use a short Decision Card only when the choice changes:

- product value;
- user-facing behavior;
- MVP scope;
- business logic;
- cost, speed, quality, or risk;
- important technical trade-offs;
- data handling;
- access, secrets, paid services, or irreversible production actions.

For all other ambiguity, choose the smallest demo-safe option, document the assumption in `DECISIONS.md`, and continue.

## Done means

A task is done only when:

- the approved scope is implemented or explicitly blocked;
- relevant checks ran, or the reason they could not run is documented;
- changed files are listed;
- `docs/project-state.md` is updated;
- any durable decision is recorded in `DECISIONS.md`;
- remaining risks or blockers are visible in the relevant MVP OS file.
