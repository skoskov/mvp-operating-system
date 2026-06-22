# Standard Stack

Use this as the approved baseline for new MVP projects unless a Decision Card explicitly changes it.

## Core rules

- Do not invent a new stack for each MVP.
- Do not switch package managers locally to bypass a broken setup.
- Do not install global tools, change shared services, stop shared containers, edit DNS, or modify shared deployment settings unless explicitly approved.
- If the standard stack does not work, stop and report an environment/configuration problem. Fix the shared configuration, not one project with local workarounds.

## Git and repository

- Use Git for every MVP project.
- Use GitHub as the remote.
- Use `main` as the default branch.
- Use Codex worktrees for implementation slices when available.
- Commit only verified, intentional changes.

## Windows/local environment

- Primary dev root: `C:\Users\skoskov\Documents\_DEV`.
- Supported shells: PowerShell, Git Bash, WSL2 when needed.
- Do not assume Linux-only tooling is available on Windows.
- Prefer commands that work in the active project environment.

## JavaScript / TypeScript web MVPs

- Default frontend stack: Next.js + React + TypeScript.
- Default package manager: npm.
- Use `package-lock.json` for npm projects.
- Do not introduce pnpm/yarn unless approved by Decision Card.
- Primary verification command should be `npm run verify` when available.

## Python MVPs

- Use local virtual environments.
- Do not install Python packages globally.
- Use project-local dependency files.
- Verification must be a single project command.

## Analytics and observability defaults

- Default product analytics: Umami.
- Default issue and uptime monitoring: GlitchTip.
- Do not use heavy product analytics by default.
- PostHog requires an explicit Decision Card for complex MVPs with heavier analytics needs.
- MVP event tracking must stay minimal: source, start, activation, core value, errors, and feedback.
- Do not track every click or sensitive user content.

## Deployment defaults

- Static/web MVP default: Vercel.
- Server/API/bot MVP default: project-specific decision required.
- Do not change shared deployment projects, shared domains, DNS, or existing services without approval.
- Preview deployments are preferred when supported.
- Production deployment requires deployment access and a deploy smoke check.

## Secrets and env

- Never commit `.env` or secrets.
- Keep `.env.example` when needed.
- Codex must list required env vars before implementation.
- Missing secrets are Access Cards, not implementation problems.

## Ports and services

- Do not kill unknown processes.
- Do not stop containers or services that may belong to another project.
- If a port is busy, report the conflict and stop unless the owner is clearly the current project.
- Shared databases, queues, servers, tunnels, and deploy projects are protected resources.

## Network and external services

- Do not reconfigure external services to make a local task pass.
- Do not rotate keys, change DNS, edit production settings, or modify shared Vercel/GitHub/server resources without approval.
- If a service is unavailable or access is missing, stop and report.

## Standard stop message

```text
Environment/configuration problem detected.
Do not patch this project locally.
Fix the standard stack or shared environment first.
```
