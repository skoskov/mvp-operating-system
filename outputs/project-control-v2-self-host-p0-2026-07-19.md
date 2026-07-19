# Project Control v2 self-host P0

Status: implementation complete, independent review pending.

Implemented:

- root `AGENTS.md`, source-role `mvp-os.lock`, and Project Control release `000001`;
- candidate versus published source-release validation;
- published tag must resolve to `HEAD`;
- root validate/bootstrap/doctor in the single verification command;
- secret-value detection for command arguments and source events;
- canonical and template CLI kept identical;
- architecture decision and release documentation updated.

Verification:

- `python3 scripts/verify.py`: PASS;
- 16/16 unit tests: PASS;
- root Project Control validate/bootstrap/doctor: PASS;
- template Project Control validate/doctor: PASS;
- `LEGACY_STARTUP_READS: 0`;
- `git diff --check`: PASS.

Review:

- automated external review was not run because sandbox policy blocked transfer
  of uncommitted repository content;
- root lock remains `project_control.status: pending-review`;
- merge, tag, and publication remain blocked until independent PR review passes.

Preserved:

- previous decisions were not rewritten or deleted;
- `outputs/sync-duration-analysis-2026-07-19.md` was not modified or staged;
- no secret values were printed or stored.
