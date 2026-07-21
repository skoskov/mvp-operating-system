# Outcome-First / Reuse-First Gate

New contracts use schema v2. Before custom implementation, set `gate_mode`,
`work_type`, a specific `gate_mode_rationale`, planned paths, and behavior/API/
data/dependency classification. Schema v1 is accepted only as the unchanged
legacy full-contract format.

## Proportional modes

- `short`: only local `bugfix`, `refactor`, `maintenance`, or `test` work with
  internal/no behavior change, no public API/data/dependency change, and every
  conditional scope set to `false`.
- `full`: features, integrations, external actions, product experiments, and
  any web, public-deploy, integration, Hermes, or stateful scope.

When uncertain, use `full`. A technical spike is a `product_experiment`; its
minimum proof and stop condition must be explicit, and it must not be reported
as a finished product function.

## Outcome contract

Both modes define beneficiary, result owner, observable result, acceptance,
non-goals, minimum proof, time budget, stop condition, and rollback. Full mode
also defines realistic data and external result, cost/scale contract, forbidden
simplifications, and the complete chain. Integration work must cover:

```text
external signal
→ interpretation
→ decision/policy
→ action
→ external result
→ product display
→ independent verification
```

Do not implement the nearest understandable component when any required link is
missing. Resolve the outcome first.

## Reuse discovery

Full mode documents the search in this order:

1. existing project solution;
2. official API or SDK;
3. platform connector;
4. maintained open-source project or library;
5. ready service/API;
6. custom code only with a recorded rejection reason for earlier options.

For every full-mode candidate, record maintenance, license, security, lock-in,
and integration cost. Reuse is not automatically better: reject a candidate
when total integration or operating risk exceeds a small local extension.

Short mode checks the existing project solution only. If discovery exposes a
feature, external action, product experiment, or conditional scope, switch to
full mode before implementation.

Record scale limits and the acceptable time to add another source. Stop and reopen
reuse discovery when the limit is exceeded.

Every scope flag includes a rationale. Template placeholders are invalid. When an
existing component is reused but custom code is still needed, record the remaining
gap; otherwise custom code is blocked. Custom code requires every candidate to
be either reused with a remaining gap or rejected; `not_applicable` is not a
build-vs-reuse decision.

## Product review

Both independent reviews explicitly confirm outcome alignment, absence of
component substitution, reuse analysis, and evidence quality. Full mode also
confirms the complete end-to-end result and cost/scale contract. Any failed check
or unresolved finding blocks acceptance.

Schema v2 preflight also requires an independent typed review artifact confirming
gate classification and those checks before implementation starts. Post-
implementation reviews repeat them against the completed source commit.

## Enforcement

Store the task contract as JSON under `outputs/` and run:

```bash
python3 .agents/skills/mvp-operating-system/bin/gate_check.py preflight <contract.json>
```

Implementation requires `MVP OS GATE: PASS (preflight)`.
