# MVP OS Sync Implementation

Date: 2026-07-12
Branch: `codex/multiagent-protocol`

## Goal

Introduce a versioned MVP OS release and a safe, active-project-only pull flow
for propagating reusable operating-layer changes.

## Implemented

- Added SemVer release `1.0.0`.
- Added `compatibility/projects.json` with project lifecycle statuses.
- Added release manifest with managed and review-only paths.
- Added `scripts/mvp_os_sync.py` for metadata validation and project sync.
- Added `mvp-os.lock` and scheduled/manual sync workflow to the project template.
- Added bootstrap requirements and sync contract documentation.
- Added a central status collector and scheduled status PR workflow for active projects.
- Recorded the durable decision in `DECISIONS.md`.

## Safety boundaries

Only `.agents/skills/mvp-operating-system` is managed automatically in this
release. Project `AGENTS.md`, `DECISIONS.md`, product docs, and OpenSpec files
are not overwritten; the generated PR asks for review instead.

## Verification

- `python3 scripts/mvp_os_sync.py validate`
- template bootstrap check
- dry-run sync for an active project and an unregistered project
- active-project sync with a lower lock version and repeat no-op check
- repository identity mismatch rejection

## Review

Independent read-only review completed after the repair loop. No blockers
remained in the final release-chain, path-safety, drift, identity, workflow,
or status-collection checks.

## Not included

Existing external projects were not modified in this slice. They need their
lock/workflow bootstrap and registry confirmation before receiving updates.

The first release must be published with Git tag `v1.0.0` before project
workflows can consume it.
