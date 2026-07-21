# Evidence Manifest

The JSON task contract under `outputs/` is both the pre-implementation gate record
and the final evidence manifest. Validate final evidence with:

```bash
python3 .agents/skills/mvp-operating-system/bin/gate_check.py acceptance <contract.json>
```

For web scope, final evidence includes the exact URL/environment and build ID,
visually inspected baseline/final desktop/mobile screenshots, DOM assertions,
click/navigation coverage, state transitions, empty/error/loading states,
console/runtime/network/assets/overflow/mobile results, rollback, and public
post-deploy proof when public deployment is in scope.

Every PASS links a project-relative regular evidence file and its SHA-256. Browser
assertions, clicks, and transitions are structured records containing expected and
observed values. Missing files, hash mismatches, placeholders, and unlinked PASS
claims block acceptance.

For stateful work, preserve and compare authoritative-row and authorization-ledger
fingerprints across export, build, browser QA, and deployment.

Integration outcomes use distinct claims: intent created, dispatched, platform
accepted, delivery confirmed, recipient read, recipient replied, definitive failure,
and uncertain failure. Dry-run, mock, replay, and synthetic modes never count as a
new external result.
