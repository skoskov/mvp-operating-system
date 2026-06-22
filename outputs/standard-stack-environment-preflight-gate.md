# Standard Stack / Environment Preflight gate — 2026-06-22

## Result

Standard Stack / Environment Preflight was added as a mandatory mvp-os gate after Brand / Design System / UX Flow and before Memory Preflight.

## Purpose

New MVP projects must use the approved baseline instead of solving dependency, runtime, deploy, and configuration problems differently in each project.

## Added

- `global/standard-stack.md`
- `skill/mvp-operating-system/references/environment-preflight.md`
- `template/mvp-project-template/.agents/skills/mvp-operating-system/references/environment-preflight.md`
- `template/mvp-project-template/ops/environment-preflight.md`

## Enforced order

```text
Idea Intake → Launch Market Research → Brand / Design System / UX Flow → Standard Stack / Environment Preflight → Memory Preflight
```

## Rule

If the approved stack or environment is broken, Codex stops and reports the problem instead of adding project-local workarounds.
