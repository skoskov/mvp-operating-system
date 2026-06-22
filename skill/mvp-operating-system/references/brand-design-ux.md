# Brand / Design System / UX Flow

Use Brand / Design System / UX Flow as a mandatory gate after Launch Market Research and before Memory Preflight.

## Purpose

Turn the scoped MVP into implementation-ready brand, visual, and UX instructions so Codex or a developer builds a coherent product interface, not just a technically working screen.

## Required fields

```text
Product name:
<product name>

Logo:
<logo description, file path, or reference link>

Slogan:
<short memorable promise>

Short description:
<1-2 sentences explaining format and value>

Positioning:
<what this is, for whom, and why it matters>

Tone of voice:
<how the product speaks to users>

Design references:
<optional links, images, products, screenshots, or descriptions>

Design system:
- Grid:
- Layout:
- Colors:
- Typography:
- Spacing:
- Buttons:
- Cards:
- Forms:
- Icons:
- States:
- Mobile rules:
- Desktop rules:

UX flows:
<flow diagrams in text form using arrows, states, and conditions>

Core scenarios:
1. <scenario name and flow>
2. <scenario name and flow>
3. <scenario name and flow>

Edge cases:
- <empty state>
- <missing data>
- <duplicate data>
- <failed action>
- <permission denied>
- <user cancels or skips>
- <sensitive data>
- <overdue or conflicting state>

Acceptance criteria:
<how to know brand, design system, and UX are ready for implementation>
```

## Example

```text
Product name:
MaxCRM

Slogan:
Максимум пользы из вашей записной книжки!

Short description:
Личная CRM, которая пишет в вашем стиле. Поздравления и напоминания в нужный момент.

Core scenario:
User opens app
→ sees today's relationship tasks
→ opens contact
→ sees suggested message
→ edits or approves
→ copies/sends message
→ task is marked done
```

## Rules

- Keep this as implementation instruction, not a decorative brand essay.
- Include enough detail for Codex or a developer to build screens and states.
- UX flows must use clear text diagrams with arrows, states, branches, and edge cases.
- Use the scoped MVP from Idea Intake and practical launch findings from Launch Market Research.
- Design references are optional, but if provided they must be linked or described clearly.
- Escalate only if brand, UX, or design decisions change product promise, scope, risk, cost, or launch quality.
