---
name: mvp-operating-system
description: Run idea-to-MVP projects with idea intake, memory preflight, decision cards, token budgeting, OpenSpec, Codex implementation, independent review, final review, and Obsidian learning updates.
---

# MVP Operating System Skill

Use this skill for new MVPs, major features, recovery slices, and project restarts.

## Mission

Move from high-level idea to working MVP while keeping the human focused on important product, business, scope, risk, budget, and technical trade-off decisions.

Do not use the human for terminal work, log copying, manual QA, code review, long-spec approval, or routine technical validation.

## Flow

1. **Idea Intake**
   - Turn the raw idea into a compact starting point: idea, user, problem, main use case, MVP promise, first success moment, non-goals, constraints, and launch target.
   - Use `references/idea-intake.md`.
   - Do not move to OpenSpec until Idea Intake exists.

2. **Memory Preflight**
   - Read relevant Obsidian LLM Knowledge Base indexes and prior project notes.
   - Apply existing defaults without re-asking the human.
   - Surface only new or conflicting decisions.

3. **Product/Technical Brief**
   - Create a short brief: goal, user, core value, MVP success, non-goals, constraints, known defaults.
   - Do not produce long specs for human approval.

4. **Decision Cards**
   - Ask the human only for important trade-offs.
   - Use `references/decision-cards.md`.

5. **Token/Time Budget**
   - Before expensive work, estimate tokens, limit risk, agent time, human time, and stop conditions.
   - Use `references/token-budget.md`.

6. **OpenSpec Handoff**
   - Create or update OpenSpec proposal/spec/tasks.
   - Treat OpenSpec as agent-readable project contract, not human approval material.
   - Use `references/openspec-handoff.md`.

7. **Independent Review**
   - Send technical artifacts to an independent reviewer in a clean context.
   - Resolve blocking issues before implementation.
   - Use `references/independent-review.md`.

8. **Codex Implementation Slice**
   - Give Codex a small approved slice.
   - Codex runs commands, tests, and repair loops autonomously.
   - Do not ask the human to paste logs or run commands.

9. **Verification**
   - Run the repo's single verification command.
   - Repair failures within budget.
   - If repeated failures exceed stop conditions, escalate with a Decision Card.

10. **Final Review**
   - Use CodeRabbit or another independent final reviewer for PR-level review.
   - Codex fixes blocking issues.

11. **Learning Update**
   - Save important decisions, failed decisions, defaults, token/time actuals, and lessons learned to the Obsidian LLM Knowledge Base.
   - Use `references/learning-update.md`.

## Output style to human

Use short summaries and Decision Cards.

Never send raw logs, long code, long specs, huge YAML, or file checklists unless explicitly requested.
