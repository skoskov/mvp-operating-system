# Build / Deploy / Verification Plan gate — 2026-06-22

## Result

Build / Deploy / Verification Plan was added as a mandatory mvp-os gate after Product/Technical Brief and before OpenSpec.

## Purpose

Codex must receive an explicit plan for implementation slices, deployment path, tests/evals, acceptance criteria mapping, verification commands, autonomous repair loop, and stop conditions before implementation starts.

## Added

- `skill/mvp-operating-system/references/build-deploy-verification-plan.md`
- `template/mvp-project-template/.agents/skills/mvp-operating-system/references/build-deploy-verification-plan.md`
- `template/mvp-project-template/build/build-deploy-verification-plan.md`

## Updated

- skill workflow
- template skill workflow
- global and template AGENTS gates
- README and start docs
- OpenSpec handoff reference
- OpenSpec tasks template
- bootstrap check
- DECISIONS.md

## Enforced order

```text
Idea Intake → Launch Market Research → Brand / Design System / UX Flow → Standard Stack / Environment Preflight → Memory Preflight → Product/Technical Brief → Build / Deploy / Verification Plan → OpenSpec
```

## Key rule

Every acceptance criterion must map to a test, eval, smoke check, or verification command.
