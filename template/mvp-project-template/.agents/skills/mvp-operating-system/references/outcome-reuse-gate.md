# Outcome-First / Reuse-First Gate

Run this gate before custom implementation.

## Outcome contract

Define the observable end-to-end result, acceptance criteria, realistic data and
external result, cost/scale contract, time budget, stop condition, forbidden
simplifications, and rollback. Integration work must cover:

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

Document the search in this order:

1. existing project solution;
2. official API, SDK, or connector;
3. supported GitHub project;
4. MCP server;
5. library;
6. ready service/API;
7. custom code only with a recorded rejection reason for earlier options.

Record scale limits and the acceptable time to add another source. Stop and reopen
reuse discovery when the limit is exceeded.

Every scope flag includes a rationale. Template placeholders are invalid. When an
existing component is reused but custom code is still needed, record the remaining
gap; otherwise custom code is blocked.

## Enforcement

Store the task contract as JSON under `outputs/` and run:

```bash
python3 .agents/skills/mvp-operating-system/bin/gate_check.py preflight <contract.json>
```

Implementation requires `MVP OS GATE: PASS (preflight)`.
