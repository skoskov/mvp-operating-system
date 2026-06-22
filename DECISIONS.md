# Decisions — mvp-os

## 2026-06-22 — Make Idea Intake mandatory

Decision: add Idea Intake as the first mandatory gate for every new MVP or project restart.

Reason: mvp-os should not move from a raw idea directly into Memory Preflight, Product/Technical Brief, OpenSpec, or implementation. The raw idea must first be normalized into a compact product input: idea, user, problem, main use case, MVP promise, first success moment, non-goals, constraints, and launch target.

Impact:

- The skill flow now starts with Idea Intake.
- Global and template AGENTS gates require Idea Intake before implementation.
- New projects include `product/idea-intake.md`.
- Bootstrap checks require the Idea Intake reference and template file.

## 2026-06-22 — Use public GitHub repository

Decision: manage `mvp-operating-system` as a Git repository and publish it as a public GitHub repository.

Reason: mvp-os is reusable infrastructure for idea-to-MVP projects and should have normal version history, remote backup, and shareable public access.

Impact:

- Initialize local Git repository.
- Add a minimal `.gitignore`.
- Create the first commit from the current approved project state.
- Create and push to a public GitHub repository named `mvp-operating-system` when GitHub CLI authentication allows it.

## 2026-06-22 — Replace separate Discovery gate with Launch Market Research

Decision: do not add Discovery as a separate mandatory gate. Keep user/problem/current workaround/problem urgency inside Idea Intake. Add Launch Market Research as the second mandatory gate after Idea Intake.

Reason: the project owner usually provides the core discovery answers with the idea. A separate Discovery gate would duplicate Idea Intake and add bureaucracy. The missing valuable step is practical market research for launch: competitors, alternatives, prices, user complaints, acquisition channels, visible ads, partner/referral mechanics, launch opportunities, and launch risks.

Impact:

- The skill flow now runs `Idea Intake → Launch Market Research → Memory Preflight`.
- New projects include `market/launch-market-research.md`.
- Bootstrap checks require the Launch Market Research reference and template file.
- Launch Market Research explicitly avoids TAM/SAM/SOM and focuses on practical launch reach through network, minimal budget, partnerships, communities, and manual outreach.
