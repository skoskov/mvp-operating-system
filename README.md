# MVP Operating System

A reusable operating system for idea-to-MVP projects built with Codex, OpenSpec, independent review, Codex GitHub Review, automated verification, and an Obsidian-based LLM Knowledge Base.

## Repository

Public GitHub repository: https://github.com/skoskov/mvp-operating-system

## Purpose

This system keeps the human focused on high-value product, business, risk, cost, scope, and important technical trade-off decisions.

It must not use the human as a terminal operator, log copier, code reviewer, long-spec approver, QA engineer, or checklist validator.

## Core flow

Every project startup first resolves current truth through Project Control v2:

```bash
python3 .agents/skills/mvp-operating-system/bin/project_control.py bootstrap --project-root .
```

This prevents preserved but superseded decisions from silently becoming active
in a new chat. See `docs/project-control-v2.md`.

1. Start from a high-level idea.
2. Create a mandatory Idea Intake.
3. Create mandatory Launch Market Research.
4. Create mandatory Brand / Design System / UX Flow.
5. Run Standard Stack / Environment Preflight.
6. Run Memory Preflight from the Obsidian LLM Knowledge Base.
7. Create Analytics / Observability Plan.
8. Create Support / Feedback / User Operations.
9. Optionally create Limited Release / Launch Plan for closed beta, controlled test, or explicit GTM request.
10. Create Build / Deploy / Verification Plan.
11. Ask the human only short Decision Cards when needed.
12. Present Token/Time Budget before expensive work.
13. Create OpenSpec proposal/spec/tasks.
14. Run independent review for technical artifacts.
15. Give Codex small approved implementation slices.
16. Codex implements, runs commands, verifies, and repairs failures.
17. Run QA / Acceptance / Release Gate.
18. Run Pre-launch Iteration Update.
19. Update Build / Deploy / Verification Plan and continue with the next implementation slice until the owner explicitly says the MVP is ready to launch.
20. Run final PR review with Codex GitHub Review.
21. Update Obsidian memory with decisions, failures, defaults, token/time usage, and lessons learned.

## Repository contents

```text
/global/AGENTS.md
/global/standard-stack.md
/skill/mvp-operating-system/
/template/mvp-project-template/
/obsidian/vault-template/
/docs/how-to-start-new-mvp.md
/docs/operating-principles.md
/docs/codex-multiagent-protocol.md
/docs/project-control-v2.md
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

## Versioned project sync

MVP OS releases are tracked in `VERSION`, `CHANGELOG.md`, and
`compatibility/projects.json`. Active projects use `mvp-os.lock` and the
template `MVP OS Sync` workflow to receive reviewed pull requests for managed
operating-layer files. See `docs/mvp-os-sync.md` for the contract.
