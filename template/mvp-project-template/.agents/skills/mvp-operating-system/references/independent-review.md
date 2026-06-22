# Independent Review Policy

Every major technical artifact must be reviewed by an independent reviewer before implementation or shipping.

## Clean context rule

The reviewer should receive only a review packet, not the full conversation.

## Review packet

```text
Artifact:
<what is being reviewed>

Minimal context:
<short project context>

Checks:
- completeness
- contradictions
- missing risks
- testability
- security/privacy implications
- token/time risk
- whether human escalation is required

Output:
PASS / FAIL
Blocking issues:
Non-blocking suggestions:
Human decision required:
```

## Rule

Builder agents cannot approve their own work.

If the issue is technical, agents resolve it without the human.

If the issue changes product value, scope, risk, data, cost, or quality mechanism, escalate via Decision Card.
