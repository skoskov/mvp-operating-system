# Standard Stack / Environment Preflight

Use this gate after Brand / Design System / UX Flow and before Memory Preflight.

## Purpose

Check that the approved stack and project environment are ready before implementation starts.

If the common environment is broken, stop and report it. Do not fix one project with one-off workarounds.

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

## Stop message

```text
Environment/configuration problem detected.
Do not patch this project locally.
Fix the standard stack or shared environment first.
```
