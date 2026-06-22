---
name: mvp-operating-system
description: Run idea-to-MVP projects with idea intake, launch market research, brand/design/UX flow, standard stack preflight, memory preflight, analytics/observability planning, build/deploy/verification planning, decision cards, token budgeting, OpenSpec, Codex implementation, independent review, final review, and Obsidian learning updates.
---

# MVP Operating System Skill

Use this skill for new MVPs, major features, recovery slices, and project restarts.

## Mission

Move from high-level idea to working MVP while keeping the human focused on important product, business, scope, risk, budget, and technical trade-off decisions.

Do not use the human for terminal work, log copying, manual QA, code review, long-spec approval, or routine technical validation.

## Flow

1. **Idea Intake**
   - Turn the raw idea into a compact starting point: idea, user, problem, current workaround, problem urgency, trigger to try, main use case, MVP promise, first success moment, MVP scope, must-have items, explicit non-goals, backlog, constraints, and launch target.
   - Use `references/idea-intake.md`.
   - Do not move to OpenSpec until Idea Intake exists.

2. **Launch Market Research**
   - Assess the scoped MVP from Idea Intake against competitors, alternatives, pricing, user complaints, acquisition channels, visible ads, partner/referral mechanics, launch opportunities, and launch risks.
   - Focus on practical launch reach through network, minimal budget, partnerships, communities, and manual outreach.
   - Use `references/launch-market-research.md`.
   - Do not produce TAM/SAM/SOM analysis.

3. **Brand / Design System / UX Flow**
   - Define product name, logo, slogan, short description, positioning, tone of voice, design references, design system, UX flows, core scenarios, edge cases, and acceptance criteria.
   - Use `references/brand-design-ux.md`.
   - Keep this as implementation-ready instruction for Codex or developers.

4. **Standard Stack / Environment Preflight**
   - Apply `global/standard-stack.md` and check runtime, package manager, dependencies, deploy path, verification command, project settings, ports, and shared-resource boundaries.
   - Use `references/environment-preflight.md` and project `ops/environment-preflight.md`.
   - If the common environment is broken, stop and report instead of patching the project locally.

5. **Memory Preflight**
   - Read relevant Obsidian LLM Knowledge Base indexes and prior project notes.
   - Apply existing defaults without re-asking the human.
   - Surface only new or conflicting decisions.

6. **Product/Technical Brief**
   - Create a short brief: goal, user, core value, MVP success, non-goals, constraints, known defaults.
   - Do not produce long specs for human approval.

7. **Analytics / Observability Plan**
   - Define measurement goal, product analytics tool, issue monitoring tool, activation event, core value event, traffic source rules, MVP events, event properties, error taxonomy, reports, privacy notes, and deferred analytics.
   - Use `references/analytics-observability-plan.md`.
   - Do not track every click in MVP.

8. **Support / Feedback / User Operations**
   - Define support channel, owner, response time, FAQ, known issues, feedback categories, report format, response templates, escalation rules, backlog rules, and daily support summary.
   - Use `references/support-feedback-ops.md`.
   - Keep support lightweight for MVP.

9. **Optional Limited Release / Launch Plan**
   - Use only for closed beta, controlled test, or explicit GTM request.
   - Use `references/limited-release-plan.md`.
   - Do not require GTM before MVP implementation by default.

10. **Build / Deploy / Verification Plan**
   - Define build goal, source inputs, approved stack, architecture, deployment plan, implementation slices, acceptance criteria mapping, test strategy, verification commands, autonomous repair loop, and stop conditions.
   - Use `references/build-deploy-verification-plan.md`.
   - Every acceptance criterion must map to a test, eval, smoke check, or verification command.

11. **Decision Cards**
   - Ask the human only for important trade-offs.
   - Use `references/decision-cards.md`.

12. **Token/Time Budget**
   - Before expensive work, estimate tokens, limit risk, agent time, human time, and stop conditions.
   - Use `references/token-budget.md`.

13. **OpenSpec Handoff**
   - Create or update OpenSpec proposal/spec/tasks.
   - Treat OpenSpec as agent-readable project contract, not human approval material.
   - Use `references/openspec-handoff.md`.

14. **Independent Review**
   - Send technical artifacts to an independent reviewer in a clean context.
   - Resolve blocking issues before implementation.
   - Use `references/independent-review.md`.

15. **Codex Implementation Slice**
   - Give Codex a small approved slice.
   - Codex runs commands, tests, and repair loops autonomously.
   - Do not ask the human to paste logs or run commands.

16. **Verification**
   - Run the repo's single verification command.
   - Repair failures within budget.
   - If repeated failures exceed stop conditions, escalate with a Decision Card.

17. **Final Check**
   - Check product promise, core UX, verification results, content readiness, known limitations, and final status.
   - Use `references/acceptance-release-gate.md`.

18. **Pre-launch Iteration Update**
   - Use after each non-final deploy/check/review cycle.
   - Capture layout, content, business logic, feature, UX, bug, analytics, support, deploy, or infra changes.
   - Update Build / Deploy / Verification Plan and create the next small implementation slice.
   - Continue this loop until the owner explicitly says the MVP is ready to launch.
   - Use `references/pre-launch-iteration-update.md`.

19. **Final Review**
   - Use CodeRabbit or another independent final reviewer for PR-level review.
   - Codex fixes blocking issues.

20. **Learning Update**
   - Save important decisions, failed decisions, defaults, token/time actuals, and lessons learned to the Obsidian LLM Knowledge Base.
   - Use `references/learning-update.md`.

## Output style to human

Use short summaries and Decision Cards.

Never send raw logs, long code, long specs, huge YAML, or file checklists unless explicitly requested.
