# Token and Time Budget Policy

Every expensive stage requires a budget estimate before execution.

## Required fields

```text
Stage:
<name>

Work included:
- ...

Expected tokens:
<range>

Expected agent time:
<range>

Expected human time:
<range>

Limit risk:
Low / Medium / High

Stop conditions:
- ...

Recommended budget:
A/B/C or explicit ceiling
```

## Default ceilings

- Small planning/review: 20k-80k tokens
- Small implementation slice: 80k-250k tokens
- Standard recovery slice: 300k-800k tokens
- Deep rebuild/import: 800k-1.5M+ tokens

## Stop conditions

Stop if:

- the same failure repeats 3 times;
- the stage exceeds the approved token ceiling;
- Codex asks the human to run terminal commands;
- implementation begins before required gates;
- verification cannot be reduced to a single command;
- a product/risk/cost trade-off appears.
