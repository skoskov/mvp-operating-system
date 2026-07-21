# Changelog

## [2.1.1] - 2026-07-22

### Added

- Proportional short/full Outcome-First and Reuse-First contract modes.
- Work classification, beneficiary, result owner, non-goals, minimum proof, and
  explicit independent-review verdicts.
- Schema v2 planned-path and behavior/API/data/dependency classification with a
  typed independent preflight review.
- Full-mode reuse evaluation for maintenance, license, security, lock-in, and
  integration cost.

### Changed

- Short mode is limited to bounded local bugfix, refactor, maintenance, or test
  work with every conditional scope disabled.
- Features, integrations, external actions, product experiments, and conditional
  scopes require full mode.
- Unchanged schema v1 contracts remain valid as legacy full contracts.

## [2.1.0] - 2026-07-21

### Added

- Dependency-free `gate_check.py` preflight and acceptance enforcement.
- Outcome-First / Reuse-First contracts with ordered reuse discovery.
- Conditional web evidence for inspected screenshots, DOM, clicks, transitions,
  browser health, public post-deploy checks, and rollback.
- Truthful external-result taxonomy and authoritative-state fingerprints.
- Optional Hermes runtime profile for connectors, schedules, tasks, tools/files,
  gateway lifecycle, and bounded delivery execution.
- Traceable Project Control source-event catalogs with timestamps and content hashes.
- Positive and negative fixtures proving enforcement rather than documentation presence.

### Changed

- Canonical references and downstream templates now carry the same release gates.
- Multi-agent roles require outcome/reuse review, exact-environment QA, repeat
  independent review, isolated build outputs, and rollback on failed public QA.
- Hermes remains opt-in and is not a mandatory LLM proxy or authoritative store.

## [2.0.0] - 2026-07-19

### Added

- Immutable Project Control release bundles with one hash-verified `CURRENT.json`.
- Dependency-free `bootstrap`, `validate`, `doctor`, and one-time `publish` CLI.
- Separate MVP OS, project-state, release, and runtime-evidence clocks.
- Secret-reference-only access metadata and TTL-aware runtime evidence.
- Clean-context tests proving legacy decisions do not enter startup.
- Self-hosted root Project Control for the MVP OS source repository.
- Source-lock candidate versus published release semantics.
- Regression coverage for secret values hidden in command arguments or source events.

### Changed

- New chats use Project Control as the sole current-state authority.
- Automated sync marks unmigrated projects pending instead of inferring current
  truth from historical files.
- The MVP OS source repository uses a dedicated `source` role and never self-syncs.

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
