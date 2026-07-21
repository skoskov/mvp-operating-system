# How to Start a New MVP

## 1. Create project automatically

Do not copy templates or run Git setup manually. Give only the project name.

Windows PowerShell:

```powershell
.\scripts\new-mvp.ps1 relationship-agent-mvp
```

WSL/bash:

```bash
./scripts/new-mvp.sh relationship-agent-mvp
```

The script creates the project under `C:\Users\skoskov\Documents\_DEV`, copies `/template/mvp-project-template`, initializes Git, creates the first commit, and pushes to GitHub when `gh` is installed and authenticated.

## 2. Connect memory

Use the Obsidian vault template in `/obsidian/vault-template` or connect an existing Obsidian vault.

Before project work, create Idea Intake, Launch Market Research, and Brand / Design System / UX Flow, then run Standard Stack / Environment Preflight and Memory Preflight.

## 3. Start through the skill

Use `mvp-operating-system` for the first planning step.

The first outputs should be mandatory Idea Intake, Launch Market Research, Brand / Design System / UX Flow, Standard Stack / Environment Preflight, Product/Technical Brief, Analytics / Observability Plan, Support Plan, and Build / Deploy / Verification Plan. Limited release planning is optional. After that, ask only needed Decision Cards.

## 4. Approve budget only when needed

The human approves token/time budget and important decisions, not long specs.

## 5. OpenSpec before implementation

Create proposal/spec/tasks before implementation. Do not move to OpenSpec until Idea Intake, Launch Market Research, Brand / Design System / UX Flow, Standard Stack / Environment Preflight, Product/Technical Brief, Analytics / Observability Plan, Support Plan, and Build / Deploy / Verification Plan exist. Optional limited release planning does not block implementation.

Before custom implementation, create the Outcome-First / Reuse-First JSON task
contract under `outputs/` and run `gate_check.py preflight`. If web, integration,
Hermes, public-deploy, or stateful scope applies, declare it explicitly so the
final acceptance validator activates the matching evidence requirements.

Use the short template only for bounded local bugfix, refactor, maintenance, or
test work with internal/no behavior change, no public API/data/dependency change,
and every scope disabled. Features, integrations, external actions, product
experiments, and any conditional scope require the full template. An independent
reviewer validates classification and the evidence plan before preflight passes.

## 6. Independent review

Technical artifacts are reviewed by independent agents before Codex implementation.

## 7. Implementation slices

Codex receives small approved slices.

For parallel Codex work, use the project agent protocol in `docs/agent-protocol.md` and project-scoped agents in `.codex/agents/`.

## 8. Verification

Codex runs `make verify` or the project equivalent.

## 9. Release gate

Check whether the MVP is ready for users.

## 10. Pre-launch iteration loop

After every non-final deploy/check/review cycle, update `iteration/pre-launch-iteration-update.md`, update Build / Deploy / Verification Plan, and continue with the next implementation slice until the owner explicitly says the MVP is ready to launch.

## 11. Final review

Use Codex GitHub Review or an independent reviewer.

After fixing findings, run a separate repeat review. Validate final task evidence
with `gate_check.py acceptance`; public deploy failure triggers rollback.

## 12. Learning update

Save decisions, failed decisions, defaults, token/time actuals, and lessons learned to Obsidian.
