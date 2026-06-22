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

The first outputs should be mandatory Idea Intake, Launch Market Research, Brand / Design System / UX Flow, and Standard Stack / Environment Preflight. After that, produce a short Product/Technical Brief and, if needed, Decision Cards.

## 4. Approve budget only when needed

The human approves token/time budget and important decisions, not long specs.

## 5. OpenSpec before implementation

Create proposal/spec/tasks before implementation. Do not move to OpenSpec until Idea Intake, Launch Market Research, Brand / Design System / UX Flow, and Standard Stack / Environment Preflight exist.

## 6. Independent review

Technical artifacts are reviewed by independent agents before Codex implementation.

## 7. Implementation slices

Codex receives small approved slices.

## 8. Verification

Codex runs `make verify` or the project equivalent.

## 9. Final review

Use Codex GitHub Review or an independent reviewer.

## 10. Learning update

Save decisions, failed decisions, defaults, token/time actuals, and lessons learned to Obsidian.
