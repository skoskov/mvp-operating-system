# MVP OS current-state audit — 2026-07-18

## Scope

Read-only verification of the local checkout, GitHub SSH remotes, and the only
registered active project (`skoskov/crm-agent-mvp`). No product or sync files
were changed.

## Verified state

- Local MVP OS working tree: clean.
- Checked-out branch: `codex/multiagent-protocol`; it is in sync with its
  upstream (`0 ahead / 0 behind`).
- Local release: `VERSION=1.0.0`, tag `v1.0.0` at the current branch head.
- GitHub SSH access: available for MVP OS, `crm-agent-mvp`, and `context`.
- Active project: `crm-agent-mvp` has `mvp-os.lock` for `v1.0.0`, with
  `sync_status: synced`; its project sync workflow is present.
- `crm-agent-mvp` is locally one commit ahead of `origin/master`; the published
  remote still contains the verified lock file.
- Python scripts compile successfully when their bytecode cache is redirected
  to a writable temporary location; release and registry JSON parse correctly.

## Currentness risks

1. **Release is absent from default branch `main` (critical).** GitHub `main`
   is the default branch and does not contain `VERSION`, the compatibility
   registry, or the sync contract. The `v1.0.0` tag and implementation are on
   `codex/multiagent-protocol`, four commits ahead of `main`. Projects resolve
   releases from `main`, so the intended control plane is not usable from the
   canonical branch.
2. **Central registry is stale (high).** It lists `crm-agent-mvp` as active,
   but leaves `last_known_version`, `last_known_status` as `null` and
   `migration` as `pending`, despite the project lock reporting `v1.0.0` and
   `synced`.
3. **Status collector targets the wrong project branch (high).**
   `scripts/mvp_os_status.py` requests every lock with `ref=main`, while the
   registered project default branch is `master`. It will report the lock as
   unavailable even though it exists remotely on `master`.
4. **Durable context coverage is missing (medium).** The context repository is
   reachable and clean, but has no `mvp-operating-system-context/INDEX.md`.

## Recommendation

First merge the MVP OS release branch into `main` and confirm the tag points
to the merged release. Then make the project branch explicit in the registry
or collector, run the collector, and commit its reporting update. Push the
pending `crm-agent-mvp` commit separately after reviewing its scope.

## Assumptions

- `main` is canonical because GitHub advertises it as the MVP OS default branch
  and the sync contract explicitly resolves releases from it.
- `master` is canonical for `crm-agent-mvp` because GitHub advertises it as
  that repository's default branch.
