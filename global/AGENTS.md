# Global AGENTS.md — MVP Operating System

Use these rules for all idea-to-MVP projects.

## Core rule

Use the `mvp-operating-system` skill for every new MVP, major feature, or recovery slice.

The human is not a terminal operator, log copier, QA engineer, code reviewer, long-spec approver, or checklist validator.

## Current-state startup gate

Before reading project documentation, run:

```bash
python3 .agents/skills/mvp-operating-system/bin/project_control.py bootstrap --project-root .
```

Only the hash-verified release referenced by `project-control/CURRENT.json` is
current operating truth. Do not startup-read `DECISIONS.md`, README files,
`outputs/`, old OpenSpec changes, context repositories, chats, or history. Read
them only for an explicit trace linked from the current release.

If Project Control is missing or invalid, stop implementation and perform the v2
migration. Never infer current decisions from file order or age.

## Agent coordination

For multiagent Codex work, use `docs/agent-protocol.md` and project-scoped agents from `.codex/agents/`.

The agent protocol defines how agents coordinate work. It does not replace MVP OS source files.

Do not use chat history as project memory. Coordinate through repository files, branches, worktrees, checks, and pull requests.

`docs/project-state.md` is a status index only. It must not introduce requirements that are absent from MVP OS artifacts.

## Hard execution gate

Execution is allowed only when the full required stack is verified and working.

Before implementation, deployment, or public-demo work, the agent must prove the required technical path is operational:
- repository state and allowed write scope;
- dependency manager;
- build command;
- test or verification command;
- local runtime when the task needs a running app;
- browser QA tool when the task has UI or click requirements;
- VPS/runtime service when deployment is in scope;
- reverse proxy, CDN, DNS, and public URL path when public demo is in scope;
- screenshots, DOM inspection, and click/navigation checks when user-visible behavior is in scope;
- rollback path before any public route or deploy change.

If any required element is broken, flaky, unavailable, blocked, or unverified, work must stop immediately. Record the exact blocker and the exact next action. Do not continue the product task with a degraded workaround.

Infrastructure failure is a P0 blocker. It is not permission to simplify the product, replace the UI, remove navigation, reduce interactivity, fake integrations, or change demo scope.

Goal completion by non-optimal means is prohibited when it changes product behavior, UX fidelity, demo scope, data realism, architecture, or user-visible functionality. Static shells, mock fallbacks, route bypasses, screenshots-as-proof, or narrower flows are forbidden unless the human explicitly approves that exact tradeoff through a Decision Card.

Every substantial user-visible task must capture and compare baseline and final state:
- public URL availability;
- desktop and mobile screenshots;
- visible UI structure;
- clickable controls;
- page transitions;
- browser console/runtime errors where available;
- product-specific acceptance criteria.

If the final state is less functional, less clickable, less navigable, less visually faithful, or less product-complete than the baseline, the task is not complete and must not be reported as READY.

For web scope, final evidence must identify the exact environment and build,
include visually inspected baseline/final desktop/mobile screenshots, DOM, real
click/navigation/filter coverage, state transitions, browser health, rollback,
and public post-deploy verification when applicable.

## Outcome-First / Reuse-First gate

Before custom implementation, validate a task contract under `outputs/` that
defines the complete observable outcome, end-to-end chain, acceptance, realistic
data/external result, cost/scale, time budget, stop condition, forbidden
simplifications, rollback, and ordered reuse discovery.

Use short mode only for bounded local bugfix, refactor, maintenance, or test work
with every conditional scope disabled. Use full mode for features, integrations,
external actions, product experiments, and any conditional scope. Legacy v2.1
contracts without an explicit mode remain full contracts.

Hermes is opt-in and non-authoritative. Use it for connectors, schedules, local
tasks, files/tools, and gateway runtime when those capabilities add value. Do not
route direct LLM calls through Hermes by default.

## Ask the human only through Decision Cards

Ask only when a decision affects:

- product value;
- user-facing behavior;
- MVP scope;
- business logic;
- unit economics;
- cost, speed, quality, or risk;
- important technical trade-offs;
- token/time/budget approval;
- examples of good/bad outputs where taste or quality matters.

Do not ask the human to:

- run shell commands;
- paste logs;
- approve long technical specifications;
- review code;
- validate file completeness manually;
- decide routine implementation details;
- inspect raw test output unless explicitly requested.

## Required gates

Before implementation:

1. Create or update Idea Intake.
2. Create or update Launch Market Research.
3. Create or update Brand / Design System / UX Flow.
4. Run Standard Stack / Environment Preflight.
5. Run Memory Preflight.
6. Produce a short Product/Technical Brief.
7. Create or update Analytics / Observability Plan.
8. Create or update Support / Feedback / User Operations.
9. Optionally create Limited Release / Launch Plan for closed beta, controlled test, or explicit GTM request.
10. Create or update Build / Deploy / Verification Plan.
11. Validate the Outcome-First / Reuse-First preflight contract.
12. Ask only required Decision Cards.
13. Present Token/Time Budget for expensive work.
14. Create or update OpenSpec artifacts.
15. Run independent review for technical artifacts.
16. Prepare an approved implementation slice.

After implementation:

1. Run the single verification command.
2. Repair failures without involving the human unless a real decision is required.
3. Run QA / Acceptance / Release Gate.
4. Run Pre-launch Iteration Update.
5. Update Build / Deploy / Verification Plan.
6. Continue with the next implementation slice until the owner explicitly says the MVP is ready to launch.
7. Run final PR review only after explicit launch readiness approval.
8. Validate the final task evidence contract.
9. Produce a short summary.
10. Update the Obsidian LLM Knowledge Base.

## Escalation rule

If a decision can be resolved by standard practice, tests, evals, CI, logs, independent review, or CodeRabbit, do not escalate it to the human.

If the choice changes product value, user promise, business model, risk, cost, quality mechanism, data handling, or MVP scope, escalate via a short Decision Card.
