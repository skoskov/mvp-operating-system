# Changelog

## [1.0.1] - 2026-07-19

### Fixed

- Read each active project lock from its configured default branch instead of
  assuming `main`.
- Record the verified MVP OS status for `crm-agent-mvp` in the central registry.

## [1.0.0] - 2026-07-12

### Added

- Versioned MVP OS release metadata.
- Active-project registry with `active`, `paused`, and `archived` statuses.
- Project `mvp-os.lock` contract for recording the applied MVP OS release.
- Safe pull-based sync for system-owned project skill files.
- Central status collection from active project lock files.
- Template GitHub Actions workflow that opens a project PR for an active project.

### Notes

- `AGENTS.md`, `DECISIONS.md`, and product files are review-only and are never overwritten automatically.
- Projects not present in the active registry do not receive automated updates.
