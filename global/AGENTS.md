# Global AGENTS.md — MVP Operating System

Use these rules for all idea-to-MVP projects.

## Core rule

Use the `mvp-operating-system` skill for every new MVP, major feature, or recovery slice.

The human is not a terminal operator, log copier, QA engineer, code reviewer, long-spec approver, or checklist validator.

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
4. Run Memory Preflight.
5. Produce a short Product/Technical Brief.
6. Ask only required Decision Cards.
7. Present Token/Time Budget for expensive work.
8. Create or update OpenSpec artifacts.
9. Run independent review for technical artifacts.
10. Prepare an approved implementation slice.

After implementation:

1. Run the single verification command.
2. Repair failures without involving the human unless a real decision is required.
3. Run final PR review.
4. Produce a short summary.
5. Update the Obsidian LLM Knowledge Base.

## Escalation rule

If a decision can be resolved by standard practice, tests, evals, CI, logs, independent review, or CodeRabbit, do not escalate it to the human.

If the choice changes product value, user promise, business model, risk, cost, quality mechanism, data handling, or MVP scope, escalate via a short Decision Card.
