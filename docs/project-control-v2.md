# Project Control v2

Project Control v2 separates current operating truth from preserved history. It
is mandatory from MVP OS v2.0.0.

## Startup contract

A new agent reads `AGENTS.md` and `mvp-os.lock`, then runs:

```bash
python3 .agents/skills/mvp-operating-system/bin/project_control.py bootstrap --project-root .
```

The command reads only `project-control/CURRENT.json`, its immutable release
manifest, and files named by that manifest. It does not read `DECISIONS.md`,
README files, `outputs/`, old OpenSpec changes, context repositories, chats, or
`project-control/history/`.

Legacy material is evidence, never startup authority. Read it only for an
explicit trace or conflict investigation linked from the current release.

## Layout

```text
project-control/
  CURRENT.json
  releases/<release-id>/
    manifest.json
    goal.json
    decisions.json
    scope.json
    architecture.json
    commands.json
    access.json
    runtime-requirements.json
    acceptance.json
  history/
```

`CURRENT.json` is the single atomic pointer. Releases are immutable after
publication. Every current decision cites at least one source event.

Backward-compatible v2.1 releases may include `source_event_catalog` in
`decisions.json`. When present, every decision source event must resolve to one
catalog entry containing a sanitized durable reference, capture timestamp, and
content SHA-256. Startup validates this metadata without reading the referenced
history or context store.

With `source_event_catalog_version: 1`, local references must remain under the
project root and hash-match their files. Version 2 embeds the captured source text
and binds it to its own content hash. Version 3 additionally requires embedded
local source text to occur in the referenced, hash-matched file. External
references must be immutable GitHub blob URLs pinned to a full commit and include
an explicit resolution method, timestamp, resolver, and referenced-object hash.
Older v2 bundles and catalog versions remain readable.

## Independent clocks

- `mvp_os_version`: tooling compatibility.
- `project_version`: current product/architecture state.
- `release_id`: immutable materialization of one project state.
- evidence TTL: whether runtime proof is usable now.

Never infer one from another.

## Secrets and commands

Store only logical references such as `secret://project/channel/credential`,
provider, status, and verification time. Secret values are forbidden. Do not
search old chats, outputs, or environment history for credentials.

Commands are argv arrays, not shell strings. They name exact startup,
verification, build, browser, deploy, diagnostics, and rollback entrypoints.

## Validation and readiness

```bash
python3 .agents/skills/mvp-operating-system/bin/project_control.py validate --project-root .
python3 .agents/skills/mvp-operating-system/bin/project_control.py doctor --project-root .
```

`validate` checks identities, hashes, decisions, commands, secret references,
and evidence format. `doctor` additionally fails on unavailable required access,
stale/failed/missing evidence, or missing executables. Structural validity does
not imply runtime readiness.

## Migration

1. Preserve legacy files; do not rewrite history.
2. Create a migration branch and reviewed release `000001` from current
   decisions only.
3. Keep rejected/superseded content outside the current release.
4. Publish once:

```bash
python3 .agents/skills/mvp-operating-system/bin/project_control.py publish \
  --project-root . --release-id 000001 --source-commit <commit> \
  --activated-at <ISO-8601-with-timezone>
```

5. Run `validate`, `bootstrap`, and `doctor`.
6. Independent clean-context reviewer reads only `AGENTS.md`, runs bootstrap,
   and proves legacy decisions did not enter startup.
7. Mark `mvp-os.lock.project_control.status` `active` only after review.

Automated sync installs tooling and marks unmigrated projects `pending`. It must
not infer project-specific truth from contradictory history.

New-project bootstrap scripts run `initialize --project-id <name>` before the
first commit. This replaces template identifiers and recomputes hashes exactly
once; `initialize` refuses an already initialized project.

## MVP OS self-hosting

The MVP OS source repository follows the same startup-authority contract. Its
root `AGENTS.md` points to the canonical source CLI under `skill/`, and its root
Project Control release describes current release-engineering truth.

The source repository does not consume itself through downstream sync. Root
`mvp-os.lock` therefore uses `repository_role: source` and `sync_mode: source`.
While `publication_status` is `candidate`, `release` must be `null`; local
`VERSION` must not be reported as an official release. Published state requires
the matching release tag after merge, verification, and push.
