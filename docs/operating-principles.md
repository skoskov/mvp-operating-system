# Operating Principles

## One idea, one source of truth

Do not duplicate the same rule across AGENTS.md, SKILL.md, OpenSpec, and Obsidian.

- AGENTS.md: always-on guardrails.
- SKILL.md: workflow.
- references: detailed formats.
- OpenSpec: current project requirements.
- Obsidian: persistent memory.

## Human as decision maker, not operator

The human decides important product, business, risk, token/budget, scope, and technical trade-offs.

Agents handle terminal work, logs, specs, code, tests, reviews, and repairs.

## Hard execution gate

Execution is allowed only when the full required stack for the task is verified and working.

A broken required tool, runtime, dependency manager, browser QA path, deploy service, reverse proxy, CDN route, public URL, screenshot path, click/navigation check, or rollback path is a P0 blocker. Stop immediately and report the blocker instead of continuing with a degraded workaround.

Do not complete goals by non-optimal means that change product behavior, UX fidelity, architecture, demo scope, data realism, or user-visible functionality. Static shells, mock fallbacks, route bypasses, screenshots-as-proof, and narrower flows require explicit user approval through a Decision Card before implementation.

## No implementation without gates

Implementation starts only after Idea Intake, Launch Market Research, Brand / Design System / UX Flow, Standard Stack / Environment Preflight, Memory Preflight, Product/Technical Brief, Analytics / Observability Plan, Support Plan, Build / Deploy / Verification Plan, required Decision Cards, Token/Time Budget, OpenSpec, independent review, and approved implementation slice.

Every custom implementation slice also requires a validated Outcome-First /
Reuse-First contract. The contract defines the observable end-to-end result,
acceptance, realistic data/external result, cost and scale, time and stop limits,
forbidden simplifications, rollback, and ordered reuse discovery.

The gate is proportional. Short mode is limited to bounded local bugfix,
refactor, maintenance, or test work with internal/no behavior change, no public
API/data/dependency change, and no conditional scope. Features, integrations,
external actions, product experiments, and conditional scopes use full mode. New
schema v2 contracts require independent preflight classification review;
schema v1 is accepted only for an unchanged legacy contract whose exact SHA-256
is registered in the current hash-verified Project Control acceptance.

## Truthful external results

Keep intent creation, dispatch, platform acceptance, confirmed delivery, recipient
read/reply, definitive failure, and uncertain failure separate. Dry-run, mock,
replay, and synthetic activity never counts as a new external result.

Hermes is optional. When selected, it provides connector, schedule, local task,
file/tool, and gateway runtime. Product semantics, policy, durable state,
reconciliation, audit, and UI metrics remain product-owned.

## No launch without release gate

Do not call an MVP ready until the QA / Acceptance / Release Gate is complete.

## No final launch without owner approval

After every non-final deploy/check/review cycle, run Pre-launch Iteration Update, update Build / Deploy / Verification Plan, and continue with the next implementation slice. Stop only when the owner explicitly says the MVP is ready to launch.

## No launch without support path

Every MVP must have a Support Plan before implementation starts.

## Keep context small

Use indexes, summaries, review packets, and small implementation slices.

Do not paste full vaults, long specs, or raw logs into the main context.
