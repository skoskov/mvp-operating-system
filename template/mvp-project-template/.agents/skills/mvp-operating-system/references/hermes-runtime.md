# Optional Hermes Runtime Profile

Hermes is an opt-in runtime for connectors, schedules, local tasks, files, tools,
gateway lifecycle, and incoming callbacks. It is not a mandatory LLM proxy.

## Ownership boundary

- Product owns semantics, policy, quality, durable intents, reconciliation, audit,
  UI state, idempotency, and authoritative metrics.
- Hermes owns connector execution, schedules, local tools/files, and gateway.
- LLM owns interpretation, scoring, tone, and draft generation when needed.
- Analytics is observational and non-authoritative.

Prefer `no-agent` local jobs for deterministic acquisition and schedule work. A
source adapter must not have send capability.

## Runtime gate

When Hermes is in scope, prove version/config compatibility, safe gateway lifecycle,
required inbound/outbound channels, cron contract and latest successful run,
required files/tools, and model selection only for LLM-dependent steps.

Gateway restart is an external action when it emits service notifications. Use
silent mode or obtain explicit authorization.

Send capability must be separately bounded by exact synthetic intent IDs, protected
test destinations, allowed channels, maximum calls, a one-time authorization ledger,
and no automatic retry after an uncertain result.

Hermes remains absent from required Project Control capabilities when a project did
not opt in.
