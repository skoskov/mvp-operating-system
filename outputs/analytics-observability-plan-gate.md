# Analytics / Observability Plan gate — 2026-06-22

## Result

Analytics / Observability Plan was added as a mandatory mvp-os gate after Product/Technical Brief and before Build / Deploy / Verification Plan.

## Decision

Use a minimal MVP analytics standard:

- Product analytics: Umami.
- Issue and uptime monitoring: GlitchTip.
- PostHog is not default; use only by explicit decision for heavier analytics.

## MVP event rule

Do not track every click. Track only source, start, activation, core value, errors, and feedback.

## Added

- `skill/mvp-operating-system/references/analytics-observability-plan.md`
- `template/mvp-project-template/.agents/skills/mvp-operating-system/references/analytics-observability-plan.md`
- `template/mvp-project-template/analytics/analytics-observability-plan.md`

## Updated

- skill workflow
- template skill workflow
- global and template AGENTS gates
- README and start docs
- standard stack defaults
- Build / Deploy / Verification Plan references
- bootstrap check
- DECISIONS.md
