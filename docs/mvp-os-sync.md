# MVP OS Sync Contract

MVP OS is the source of truth for reusable operating rules. Projects consume
released versions through a pull-based GitHub Actions workflow.

## Release source

- `VERSION` is the canonical SemVer version.
- `CHANGELOG.md` contains short release notes.
- `compatibility/releases/v<version>.json` declares managed and review-only paths.
- `compatibility/projects.json` is the active-project registry and desired-state control plane.

`VERSION` can describe a local release candidate. Official publication also
requires root `mvp-os.lock.publication_status` to be `published`, its `release`
to match `v<VERSION>`, successful verification, merge to `main`, and push of the
matching tag. Candidate source locks keep `release: null`.

Only projects with registry status `active` receive automated sync work. `paused`
and `archived` projects remain visible but are not updated.

## Project contract

Every project declares `mvp-os.lock`. It records the applied release and the
source repository. The template workflow checks weekly and can also be started
manually. It opens a PR in the project; it never auto-merges.

From v2.0.0 the lock also reports Project Control status. Sync installs the
validator/bootstrap tooling, but never auto-generates project-specific current
decisions. An unmigrated active project receives
`project-control-migration-required`; a reviewed project migration must create
and activate `project-control/CURRENT.json`.

The project lock is the actual applied-version source. The central registry's
`last_known_version` is a reporting field, not a live claim; it must be updated
from a project status report or review PR.

The central `MVP OS Project Status` workflow checks only `active` projects,
reads each lock through the GitHub Contents API from the project's configured
`default_branch` (falling back to `main` for older registry entries), and opens
a PR when the reported version or sync status changes. Paused and archived
projects are not queried. Private project repositories require the optional
`MVP_OS_PROJECTS_READ_TOKEN` repository secret.

The sync script manages only paths listed in the release manifest. Project
`AGENTS.md`, `DECISIONS.md`, product docs, and OpenSpec files are review-only so
project-specific rules cannot be overwritten silently.

Project Control releases are project-owned review paths. Their history and
current pointer are never overwritten by central sync.

## Candidate propagation

1. A project records a reusable improvement in its context improvement log.
2. The improvement is proposed in MVP OS and reviewed as a normal repository change.
3. A merged change increments `VERSION`, updates `CHANGELOG.md`, and adds a release manifest.
4. Active projects receive a PR through their sync workflow.
5. The project merges the PR after project-specific review and its lock records the new release.

Every published version must also have a matching Git tag, for example `v1.0.0`.
Projects resolve `VERSION` from `main` and then check out that tag before sync.
Each release manifest declares `previous_version`; projects apply the complete
chain and refuse to skip a migration.

The MVP OS repository itself uses `sync_mode: source`. It self-hosts Project
Control but never enters the downstream pull-request sync loop.

The sync command requires the repository identity from the registry. A local
run must pass `--repository owner/name`. Current-version drift is blocked by
default; the template workflow passes `--allow-overwrite` because its clean PR
branch makes the replacement reviewable.

## Status semantics

- `active`: eligible for automated sync PRs.
- `paused`: tracked, but no rollout.
- `archived`: historical only, no rollout.
