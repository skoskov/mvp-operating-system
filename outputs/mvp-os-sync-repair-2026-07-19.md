# MVP OS sync repair — 2026-07-19

## Completed changes

- Prepared the versioned MVP OS release chain for canonical `main`:
  `v1.0.0` followed by the `v1.0.1` status-collection fix.
- Added `default_branch` to the active-project registry and set
  `crm-agent-mvp` to `master`.
- Updated central status collection to request each project's configured branch
  rather than assuming `main`.
- Recorded the verified `crm-agent-mvp` state: migrated, `v1.0.0`, and synced.
- Added the `v1.0.1` release manifest, release notes, and decision record.

## Verification

- `python3 scripts/mvp_os_sync.py validate --source-root .` passes for `v1.0.1`.
- Both MVP OS scripts compile when Python bytecode is directed to `/tmp`.
- Registry and release manifests parse as JSON.
- Git SSH confirms that the published `crm-agent-mvp` `master` branch contains
  its `mvp-os.lock` at `v1.0.0` with `sync_status: synced`.

## External blocker

The local GitHub CLI is unauthenticated and an unauthenticated GitHub Contents
API request returns `404` for private `skoskov/crm-agent-mvp`. The workflow is
already designed to use `MVP_OS_PROJECTS_READ_TOKEN`; that secret must be a
fine-grained token with read access to `skoskov/crm-agent-mvp`, configured in
the `skoskov/mvp-operating-system` repository. Its value was neither read nor
created during this repair.
