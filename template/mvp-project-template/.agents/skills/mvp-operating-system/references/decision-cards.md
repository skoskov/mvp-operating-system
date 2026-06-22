# Decision Cards

Use Decision Cards only when the human is needed for an important decision.

## When to ask

Ask only if the choice affects product value, user-facing behavior, MVP scope, business model, risk, cost, quality mechanism, token/time budget, data handling, or important technical trade-offs.

## Do not ask for

- command execution;
- log copying;
- routine package choices;
- file naming;
- long spec approval;
- code review;
- manual QA;
- checklist validation.

## Format

```text
Decision: <short name>

Why it matters:
<1-3 lines>

Options:
A. <option> — <trade-off>
B. <option> — <trade-off>
C. <option> — <trade-off>

Recommendation:
<option + reason>

Token/time impact:
<short estimate>

Default if no answer:
<option>
```

## Rules

- One decision per card.
- Maximum three options.
- No long background.
- No raw logs.
- No technical dump.
