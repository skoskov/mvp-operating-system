# Codex Multiagent Protocol

MVP OS defines what to do.

The Codex multiagent protocol defines how agents coordinate the work.

## Purpose

Avoid chat-to-chat context transfer. Agents should work around one repository source of truth.

The protocol is included in every new MVP project template:

- `docs/agent-protocol.md`
- `docs/project-state.md`
- `.codex/config.toml`
- `.codex/agents/architect.toml`
- `.codex/agents/implementer.toml`
- `.codex/agents/devops_qa.toml`
- `.codex/agents/release_manager.toml`

## Non-goal

Do not replace MVP OS gates with a second set of project-control files.

The following remain canonical:

- scope: `product/idea-intake.md`
- market facts: `market/launch-market-research.md`
- product and UX: `product/brand-design-ux.md`
- stack and environment: `ops/environment-preflight.md`
- architecture, slices, checks: `build/build-deploy-verification-plan.md`
- requirements and tasks: `openspec/`
- release evidence: `qa/acceptance-release-gate.md`
- iteration loop: `iteration/pre-launch-iteration-update.md`
- durable decisions: `DECISIONS.md`

## Roles

- `release_manager`: coordinates agents, prioritizes blockers, consolidates evidence, reports readiness for owner review.
- `architect`: checks gate-mode classification, outcome, component substitution,
  reuse, scope, architecture consistency, acceptance coverage, cost/scale in full
  mode, and task decomposition.
- `implementer`: implements approved slices with small changes and verification.
- `devops_qa`: verifies the exact environment, deployment path, browser evidence,
  state transitions, fingerprints, logs, rollback, and release evidence.

## Rule

Final launch still requires explicit owner approval.

Passing checks, a completed release gate, or a release manager report can make the project ready for owner review, but they do not replace the owner launch decision.

Independent findings require a separate repeat review after fixes. The implementer
cannot replace that review with its own tests. Agents must not concurrently run
builds that write to the same `.next`, `dist`, `build`, or equivalent mutable
output. Public deploy requires a rollback path and post-deploy browser QA; failure
triggers rollback rather than READY.
