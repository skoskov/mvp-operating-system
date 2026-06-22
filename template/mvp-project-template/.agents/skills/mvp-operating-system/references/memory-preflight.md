# Memory Preflight

Before starting a new MVP or major slice, consult the Obsidian LLM Knowledge Base.

## Purpose

Use prior decisions, failures, defaults, token budgets, and patterns so the human is not asked the same questions repeatedly.

## Read only what is relevant

Do not load the full vault into context. Read indexes first, then 5-15 relevant pages.

## Memory Brief format

```text
Memory Brief

Relevant projects:
- ...

Applicable defaults:
- ...

Relevant failures to avoid:
- ...

Expected token/time range from similar work:
- ...

Decisions already settled:
- ...

New decisions that may require the human:
- ...
```

## Rule

If memory contains a stable default, apply it without asking the human again.

Escalate only when the current project conflicts with memory or introduces a new important trade-off.
