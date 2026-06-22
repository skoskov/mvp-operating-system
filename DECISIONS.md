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

## 2026-06-22 — Keep MVP scope inside Idea Intake

Decision: do not add a separate MVP Scope gate. Discuss and record MVP scope inside Idea Intake before Launch Market Research.

Reason: market research must know what is actually included in the first MVP version. A separate MVP Scope gate after research would make research evaluate an abstract idea instead of the intended launch version.

Impact:

- Idea Intake now includes current workaround, why it is bad, problem frequency/urgency, trigger to try MVP, MVP scope, must-have items, explicit non-goals, and post-launch backlog.
- Launch Market Research now explicitly researches the scoped MVP from Idea Intake.
- New project templates include the expanded `product/idea-intake.md` fields.

## 2026-06-22 — Add Brand / Design System / UX Flow gate

Decision: add Brand / Design System / UX Flow as a mandatory gate after Launch Market Research and before Memory Preflight.

Reason: mvp-os should produce implementation-ready product instructions, not only technical specs. Codex or developers need product name, logo direction, slogan, short description, positioning, tone of voice, design system, UX flows, core scenarios, edge cases, and acceptance criteria before OpenSpec and implementation.

Impact:

- The skill flow now runs `Idea Intake → Launch Market Research → Brand / Design System / UX Flow → Memory Preflight`.
- New projects include `product/brand-design-ux.md`.
- Bootstrap checks require the Brand / Design System / UX reference and template file.
- Product/Technical Brief now references Idea Intake, Launch Market Research, and Brand / Design System / UX Flow as source inputs.

## 2026-06-22 - Add Standard Stack / Environment Preflight gate

Decision: add Standard Stack / Environment Preflight before Memory Preflight.

Reason: new MVP projects must start from one approved working stack. If the stack check fails, implementation does not start.

Impact:

- Added `global/standard-stack.md`.
- Added `ops/environment-preflight.md` to the project template.
- Added `references/environment-preflight.md` to the skill and template skill.
- Product/Technical Brief now references the environment preflight result.
