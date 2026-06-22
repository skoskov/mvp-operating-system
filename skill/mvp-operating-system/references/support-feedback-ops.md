# Support / Feedback / User Operations

Use this gate after Analytics / Observability Plan and before Build / Deploy / Verification Plan.

## Purpose

Define the minimum support and feedback loop needed for an MVP launch.

The goal is not a full helpdesk. The goal is a simple operating loop:

```text
user has a question or problem
→ user has a clear support channel
→ team classifies the request
→ issue becomes FAQ, bugfix, backlog item, or product decision
→ user receives a clear answer
```

## Required fields

```text
Support channel:
<Telegram, email, form, chat, issue tracker, or other>

Support owner:
<person or role responsible for replies>

Expected response time:
<realistic MVP response time>

FAQ:
- question:
  answer:

Known issues:
- issue:
  user impact:
  workaround:
  planned fix:

Feedback categories:
- bug
- UX confusion
- missing feature
- pricing/payment question
- account/access issue
- data/import issue
- generation quality issue
- other

Bug report format:
- user/session identifier, if safe:
- source/channel:
- steps to reproduce:
- expected result:
- actual result:
- screenshot/log link, if available:
- severity:

User response templates:
- bug received:
- workaround:
- feature request received:
- known limitation:
- resolved:

Escalation rules:
- when to escalate to product:
- when to escalate to engineering:
- when to escalate to owner/founder:

Backlog rules:
- when feedback becomes a task:
- how duplicates are grouped:
- how severity is assigned:

Daily support summary:
- new issues:
- repeated questions:
- severe bugs:
- top UX confusion:
- feature requests:
- recommended actions:
```

## Rules

- Every MVP must have one clear support channel.
- Every MVP must have an owner for user replies.
- Known limitations must be written before launch.
- Repeated support questions must become FAQ items.
- Repeated bugs must become regression tests or eval cases.
- Feedback that changes product promise, scope, price, risk, or trust must become a Decision Card.
- Do not add a complex helpdesk system unless the MVP requires it.
