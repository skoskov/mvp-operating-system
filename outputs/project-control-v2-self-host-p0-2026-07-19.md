# Project Control v2 self-host P0

Status: implementation complete, independent review passed.

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
- 19/19 unit tests: PASS;
- root Project Control validate/bootstrap/doctor: PASS;
- template Project Control validate/doctor: PASS;
- `LEGACY_STARTUP_READS: 0`;
- `git diff --check`: PASS.

Review:

- first independent review found three P1 findings: manifest secret bypass,
  symlink escape, and cross-file project identity mismatch;
- all findings have regression coverage and passed repeat independent review;
- root lock is now `project_control.status: active`;
- merge, tag, and publication remain gated by this PR's final merge step.

Preserved:

- previous decisions were not rewritten or deleted;
- `outputs/sync-duration-analysis-2026-07-19.md` was not modified or staged;
- no secret values were printed or stored.
