# Global AGENTS.md — MVP Operating System

Use these rules for all idea-to-MVP projects.

## Core rule

Use the `mvp-operating-system` skill for every new MVP, major feature, or recovery slice.

The human is not a terminal operator, log copier, QA engineer, code reviewer, long-spec approver, or checklist validator.

## Agent coordination

For multiagent Codex work, use `docs/agent-protocol.md` and project-scoped agents from `.codex/agents/`.

The agent protocol defines how agents coordinate work. It does not replace MVP OS source files.

Do not use chat history as project memory. Coordinate through repository files, branches, worktrees, checks, and pull requests.

`docs/project-state.md` is a status index only. It must not introduce requirements that are absent from MVP OS artifacts.

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
11. Ask only required Decision Cards.
12. Present Token/Time Budget for expensive work.
13. Create or update OpenSpec artifacts.
14. Run independent review for technical artifacts.
15. Prepare an approved implementation slice.

After implementation:

1. Run the single verification command.
2. Repair failures without involving the human unless a real decision is required.
3. Run QA / Acceptance / Release Gate.
4. Run Pre-launch Iteration Update.
5. Update Build / Deploy / Verification Plan.
6. Continue with the next implementation slice until the owner explicitly says the MVP is ready to launch.
7. Run final PR review only after explicit launch readiness approval.
8. Produce a short summary.
9. Update the Obsidian LLM Knowledge Base.

## Escalation rule

If a decision can be resolved by standard practice, tests, evals, CI, logs, independent review, or CodeRabbit, do not escalate it to the human.

If the choice changes product value, user promise, business model, risk, cost, quality mechanism, data handling, or MVP scope, escalate via a short Decision Card.
