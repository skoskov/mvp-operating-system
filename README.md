# MVP Operating System

A reusable operating system for idea-to-MVP projects built with Codex, OpenSpec, independent review, Codex GitHub Review, automated verification, and an Obsidian-based LLM Knowledge Base.

## Repository

Public GitHub repository: https://github.com/skoskov/mvp-operating-system

## Purpose

This system keeps the human focused on high-value product, business, risk, cost, scope, and important technical trade-off decisions.

It must not use the human as a terminal operator, log copier, code reviewer, long-spec approver, QA engineer, or checklist validator.

## Core flow

1. Start from a high-level idea.
2. Create a mandatory Idea Intake.
3. Create mandatory Launch Market Research.
4. Create mandatory Brand / Design System / UX Flow.
5. Run Standard Stack / Environment Preflight.
6. Run Memory Preflight from the Obsidian LLM Knowledge Base.
7. Create Analytics / Observability Plan.
8. Create Build / Deploy / Verification Plan.
9. Ask the human only short Decision Cards when needed.
10. Present Token/Time Budget before expensive work.
11. Create OpenSpec proposal/spec/tasks.
12. Run independent review for technical artifacts.
13. Give Codex small approved implementation slices.
14. Codex implements, runs commands, verifies, and repairs failures.
15. Run QA / Acceptance / Release Gate.
16. Run final PR review with Codex GitHub Review.
17. Update Obsidian memory with decisions, failures, defaults, token/time usage, and lessons learned.

## Repository contents

```text
/global/AGENTS.md
/global/standard-stack.md
/skill/mvp-operating-system/
/template/mvp-project-template/
/obsidian/vault-template/
/docs/how-to-start-new-mvp.md
/docs/operating-principles.md
```

## How to use

For every new MVP, do not manually run 10 setup commands. Give only the project name and run one bootstrap script from this repository.

Windows PowerShell:

```powershell
.\scripts\new-mvp.ps1 relationship-agent-mvp
```

WSL/bash:

```bash
./scripts/new-mvp.sh relationship-agent-mvp
```

The script creates the project under `C:\Users\skoskov\Documents\_DEV`, copies the MVP template, initializes Git, creates the first commit, and pushes to GitHub when `gh` is installed and authenticated.

Do not start from a blank chat or blank repository.
