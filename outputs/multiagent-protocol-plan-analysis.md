# Multiagent Protocol Plan Analysis — 2026-07-08

## Scope

Analyze whether the proposed Codex multiagent protocol can sit next to MVP Operating System without conflicting with it.

## Assumptions

- MVP OS remains responsible for what to do: idea intake, market research, design/UX, stack preflight, memory preflight, planning, OpenSpec, implementation slices, verification, release gate, and learning update.
- The new protocol should define how Codex agents coordinate work: roles, ownership, worktrees, evidence, status updates, and handoff rules.
- No implementation was requested yet.

## Verdict

The plan is directionally correct, but it should not be copied into MVP OS as-is.

The strong part is the shift from chat-to-chat memory transfer to repository-based coordination. This fits MVP OS.

The weak part is that the plan introduces a parallel set of project-control documents that overlaps with existing MVP OS artifacts.

## Main Conflict

Do not add a second requirements/control plane such as:

- `docs/DEMO_SCOPE.md`
- `docs/ACCEPTANCE_CRITERIA.md`
- `docs/ARCHITECTURE.md`
- `docs/TASKS.md`

as independent sources of truth.

MVP OS already has canonical equivalents:

- Demo scope: `product/idea-intake.md` plus `product/brand-design-ux.md`
- Architecture and slices: `build/build-deploy-verification-plan.md`
- Requirements/tasks: `openspec/`
- Acceptance and launch status: `qa/acceptance-release-gate.md`
- Iteration loop: `iteration/pre-launch-iteration-update.md`
- Decisions: root `DECISIONS.md`

## Safe Additions

The protocol should add only agent-work instructions:

- project-scoped custom agents under `.codex/agents/`
- an agent coordination document, for example `docs/agent-protocol.md`
- a small status index, for example `docs/project-state.md`, if kept explicitly non-authoritative
- optional `docs/risk-log.md` and `docs/release-runbook.md` only if they reference MVP OS source artifacts instead of replacing them

## Role Model

Recommended roles:

- `release_manager`: orchestrates, checks readiness, assigns work, consolidates evidence.
- `architect`: planning-only by default; checks scope, contradictions, and MVP OS artifact consistency.
- `implementer`: implements approved slices from OpenSpec / Build Plan only.
- `devops_qa`: verifies setup, env, deployment, browser/smoke checks, logs, and release runbook.

## Required Corrections To The Proposed Plan

1. Replace independent control docs with a mapping to existing MVP OS artifacts.
2. Make `release_manager` report `ready for owner review`, not final launch approval.
3. Keep owner approval mandatory before final launch.
4. Keep Decision Cards as the only human escalation path for scope, value, risk, cost, access, and irreversible actions.
5. Fix the `architect` custom agent contradiction: read-only sandbox cannot update docs.
6. Keep custom agents narrow and prevent recursive delegation by default.
7. Treat `docs/project-state.md` as an index/status digest, not a source of requirements.
8. Add browser checks only for web UI projects and unauthenticated/local/public routes.

## Recommendation

Implement the multiagent protocol as a coordination layer in MVP OS, not as a replacement for existing gates.

Minimal implementation target:

- update `global/AGENTS.md`
- update `template/mvp-project-template/AGENTS.md`
- add `template/mvp-project-template/docs/agent-protocol.md`
- add `.codex/agents/*.toml` templates to the project template
- update `scripts/new-mvp.ps1` and `scripts/new-mvp.sh` only if needed to copy the new files
- record the accepted decision in `DECISIONS.md`

## Limitation

`skoskov/context` could not be pulled before reading because SSH host key verification failed in the sandbox. The local copy was read instead.
