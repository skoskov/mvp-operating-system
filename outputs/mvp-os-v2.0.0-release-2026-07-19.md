# MVP OS v2.0.0 release

Status: published release marker prepared.

Release contents:

- Project Control release `000002` is current and hash-verified;
- source lock records `publication_status: published` and `release: v2.0.0`;
- `000002` inherits the reviewed self-hosting model and records the published
  release state without mutating immutable release `000001`;
- final publication requires the `v2.0.0` tag to point to this release commit,
  then the single verification command and remote push verification.

Review and verification before release marker:

- independent review: PASS after three P1 fixes;
- `python3 scripts/verify.py`: 19/19 tests PASS before publication marker;
- root and template Project Control validate/doctor: PASS.

Preserved:

- `outputs/sync-duration-analysis-2026-07-19.md` remains unmodified and
  unstaged;
- no secret values were recorded.
