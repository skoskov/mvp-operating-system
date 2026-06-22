# Standard Stack / Environment Preflight

Use this gate after Brand / Design System / UX Flow and before Memory Preflight.

## Purpose

Check that the approved project stack and local environment are ready before implementation starts.

If the common environment is broken, stop and report it. Do not fix one project with one-off workarounds.

## Inputs

- `global/standard-stack.md`
- `ops/environment-preflight.md`
- Idea Intake
- Launch Market Research
- Brand / Design System / UX Flow

## Required checks

```text
Standard stack version:
Project type:
Git status:
Runtime versions:
Package manager:
Install command:
Dependency status:
Single verification command:
Expected tests/evals:
Build command:
Deploy target:
Deploy method:
Preview deploy:
Rollback path:
Required project settings:
Missing project settings:
Required ports:
Port conflicts:
Shared resources touched:
Protected resources at risk:
Result: PASS / BLOCKED
Blocking reason:
Required fix or Access Card:
```

## Rules

- Use the approved package manager.
- Do not switch tools to bypass install problems.
- Do not add one-off local dependencies to hide a broken baseline.
- Do not change shared resources unless approved.
- If a port is busy and ownership is unclear, stop.
- If required project settings are missing, create a Human Decision / Access Card.
- If a problem affects the baseline, fix the standard stack or shared environment before implementation continues.

## Stop conditions

Stop when:

- approved package manager is missing;
- runtime version is wrong;
- dependencies fail with the approved package manager;
- required library is unavailable under the approved stack;
- deploy path is not ready;
- required project setting is missing;
- port conflict ownership is unclear;
- task would change a shared resource;
- task would affect another project;
- verification cannot be reduced to a single command.

## Required stop message

```text
Environment/configuration problem detected.
Do not patch this project locally.
Fix the standard stack or shared environment first.
```
