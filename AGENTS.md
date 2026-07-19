# MVP Operating System Maintainer Rules

This repository is the source of MVP OS releases. It self-hosts Project Control,
but it does not consume itself through the downstream sync workflow.

## Startup gate

Before reading project documentation, read `mvp-os.lock`, then run:

```bash
python3 skill/mvp-operating-system/bin/project_control.py bootstrap --project-root .
```

Only the hash-verified release referenced by `project-control/CURRENT.json` is
current operating truth. Read preserved decisions, outputs, chats, or history
only for an explicit trace or conflict investigation linked from that release.

## Source repository role

- `mvp-os.lock.repository_role` must be `source`.
- `mvp-os.lock.sync_mode` must be `source`; never run self-sync.
- `publication_status: candidate` is not an official MVP OS release.
- A release becomes official only after merge to `main`, matching tag creation,
  successful verification, and push of both branch and tag.
- Never infer publication from local `VERSION` alone.

## Verification

Use the single non-destructive command:

```bash
python3 scripts/verify.py
```

Do not modify immutable Project Control releases after publication. Create a new
release and atomically advance `project-control/CURRENT.json`.
