# Decisions — mvp-os

## 2026-07-19 — Self-host Project Control without self-sync

Decision: manage the MVP OS source repository through root `AGENTS.md`, a
source-role `mvp-os.lock`, and hash-verified root Project Control. Keep release
distribution as a separate downstream pull-request mechanism.

Reason: MVP OS cannot require Project Control from every project while leaving
its own current operating truth implicit. Reusing consumer self-sync would
create a circular and misleading release path.

Impact:

- Root startup uses the canonical CLI under `skill/`.
- `publication_status: candidate` cannot claim a release tag.
- Local `VERSION` alone is not official release evidence.
- Secret detection covers command arguments and source-event references.
- Existing decisions and historical artifacts remain preserved.

## 2026-07-19 — Track every project's default branch in the sync registry

Decision: store `default_branch` per project in `compatibility/projects.json`
and use it for central lock collection.

Reason: active repositories can use `master` or another default branch. A
hardcoded `main` makes a valid applied lock appear unavailable.

Impact:

- New registry entries should declare their default branch.
- Existing entries without the field remain compatible through the `main`
  fallback.
- `crm-agent-mvp` is recorded as `master`, migrated, and synced at `v1.0.0`.

## 2026-07-08 - Add Codex multiagent coordination layer

Decision: add a repository-based Codex multiagent coordination layer to the MVP project template.

Reason: multiple Codex chats or agents should not exchange project meaning through chat history. They should coordinate through one repository source of truth while MVP OS remains responsible for what to do.

Impact:

- New projects include `docs/agent-protocol.md` for role, handoff, evidence, and escalation rules.
- New projects include `docs/project-state.md` as a status index only, not a requirements source.
- New projects include project-scoped custom agents in `.codex/agents/`.
- Bootstrap validation now requires the agent protocol and custom agent files.
- `global/AGENTS.md` and template `AGENTS.md` now state that the multiagent protocol coordinates how agents work and does not replace MVP OS artifacts.
- Final launch still requires explicit owner approval.

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

## 2026-06-22 - Add Build / Deploy / Verification Plan gate

Decision: add Build / Deploy / Verification Plan after Product/Technical Brief and before OpenSpec.

Reason: Codex needs an explicit plan for slices, checks, deployment path, acceptance criteria mapping, repair loop, and stop conditions before implementation starts.

Impact:

- Added `build/build-deploy-verification-plan.md` to the project template.
- Added `references/build-deploy-verification-plan.md` to the skill and template skill.
- OpenSpec tasks now use the Build / Deploy / Verification Plan as the source for slices and checks.

## 2026-06-22 - Add QA / Acceptance / Release Gate

Decision: add QA / Acceptance / Release Gate after verification and before final review.

Reason: a passing build is not enough to call an MVP ready. The result must be checked against product promise, core UX, content readiness, acceptance criteria coverage, known limitations, and release readiness.

Impact:

- Added `qa/acceptance-release-gate.md` to the project template.
- Added `references/acceptance-release-gate.md` to the skill and template skill.
- Post-implementation rules now require the release gate before final review.

## 2026-06-22 - Add Analytics / Observability Plan

Decision: add Analytics / Observability Plan after Product/Technical Brief and before Build / Deploy / Verification Plan.

Reason: MVPs need minimal measurement without tracking every click. The default stack is Umami for product analytics and GlitchTip for issue and uptime monitoring.

Impact:

- Added `analytics/analytics-observability-plan.md` to the project template.
- Added `references/analytics-observability-plan.md` to the skill and template skill.
- Added Umami and GlitchTip defaults to `global/standard-stack.md`.
- Build / Deploy / Verification Plan now includes metrics input and smoke check.

## 2026-06-22 - Add Support / Feedback / User Operations

Decision: add Support / Feedback / User Operations after Analytics / Observability Plan and before Build / Deploy / Verification Plan.

Reason: MVP launch needs one support channel, an owner, FAQ, known issues, feedback categories, response templates, escalation rules, backlog rules, and daily support summary before implementation and launch.

Impact:

- Added `support/support-feedback-plan.md` to the project template.
- Added `references/support-feedback-ops.md` to the skill and template skill.
- Build / Deploy / Verification Plan now includes User Ops Plan as a source input.

## 2026-06-22 - Add optional test plan

Decision: add a limited user test plan as an optional gate, not a mandatory GTM gate.

Reason: before GTM, MVPs usually need a controlled test with a limited group of users. Full GTM requires a separate decision.

Impact:

- Added `launch/limited-release-plan.md` to the project template.
- Added `references/limited-release-plan.md` to the skill and template skill.
- Build / Deploy / Verification Plan can use it as an optional source input.
- Bootstrap check does not require this plan as a blocking file.

## 2026-06-22 - Keep security/access inside Build Plan

Decision: do not add a separate Security / Privacy / Access Review gate for MVP.

Reason: for MVP this is too heavy. Build / Deploy / Verification Plan only needs a compact access section.

Impact:

- Added `Secrets` to Build / Deploy / Verification Plan.
- Added `Access map` to Build / Deploy / Verification Plan.
- Added `Codex permissions` to Build / Deploy / Verification Plan.

## 2026-06-22 - Add mandatory Pre-launch Iteration Update loop

Decision: add Pre-launch Iteration Update as a mandatory loop after deploy/check/review cycles and before launch.

Reason: before users, MVP work is still about layout, content, business logic, features, UX, bugs, analytics, support, and deploy fixes. After each non-final check, the process must return to Build / Deploy / Verification Plan with updates and the next small implementation slice.

Impact:

- Added `iteration/pre-launch-iteration-update.md` to the project template.
- Added `references/pre-launch-iteration-update.md` to the skill and template skill.
- Post-implementation rules now loop through Pre-launch Iteration Update until the owner explicitly says the MVP is ready to launch.
- Bootstrap check requires the pre-launch iteration files.

## 2026-07-08 — Hard execution gate for MVP-OS work

Decision:
Require a hard execution gate before implementation, deployment, or public-demo work.

Reason:
Product work must not proceed on top of broken tools, broken infrastructure, unstable browser QA, or unverified public delivery. A broken required stack element must stop the task as a P0 blocker instead of being hidden by a degraded workaround.

Status:
Accepted by user `IMPLEMENT` request on 2026-07-08.

Consequences:
- Execution is allowed only with a fully verified working stack for the task.
- Broken, flaky, blocked, unavailable, or unverified required elements are immediate P0 blockers.
- Infrastructure failure is not permission to simplify UI, remove navigation, reduce interactivity, fake integrations, or narrow demo scope.
- Static shells, mock fallbacks, route bypasses, screenshots-as-proof, or narrower flows require explicit user approval through a Decision Card before implementation.
- Substantial user-visible work must compare baseline and final state.
- A task cannot be reported as `READY` if the final state is less functional, less clickable, less navigable, less visually faithful, or less product-complete than the baseline.

## 2026-07-12 — Versioned MVP OS propagation

Decision:
Use MVP OS releases, an active-project registry, project `mvp-os.lock` files,
and pull-based project PRs as the default propagation mechanism.

Reason:
MVP OS must remain the source of truth while project-specific rules remain
safe to review. Pull-based PRs limit write access, provide an audit trail, and
allow only active projects to receive automated rollout work.

Consequences:
- SemVer is used for MVP OS releases, starting with `1.0.0`.
- `compatibility/projects.json` controls `active`, `paused`, and `archived` projects.
- Only release-manifest `managed_paths` are copied automatically.
- `AGENTS.md`, `DECISIONS.md`, product docs, and OpenSpec remain review-only.
- Sync opens a project PR and never auto-merges it.
- The project lock is the actual applied-version record; the central registry stores desired state and last-known reporting data.

## 2026-07-21 — Backward-compatible executable gates in MVP OS v2.1.0

Decision:
Release the MaxCRM-derived improvements as conditional, dependency-free MVP OS
v2.1.0 gates while keeping Project Control schema v2 compatible.

Reason:
Build, HTTP, component, or connector success can exist without a verified product
outcome. Documentation-only rules did not prove inspected browser behavior, state
transitions, truthful external-result claims, reuse discovery, or optional runtime
boundaries.

Consequences:
- Every custom implementation starts with a validated Outcome-First / Reuse-First contract.
- Web acceptance requires inspected screenshots, DOM, clicks, transitions, exact environment, browser health, and public post-deploy evidence when applicable.
- Integration states distinguish intent, dispatch, platform acceptance, delivery, recipient observation, definitive failure, and uncertainty.
- Stateful work compares authoritative-row and authorization-ledger fingerprints.
- Hermes is an optional runtime for connectors, schedules, tasks, tools/files, and gateway; product state and semantics remain product-owned.
- New Project Control releases can make decision source events traceable through a hashed catalog without reading history at startup.
- Independent findings require repeat review; agents cannot concurrently write shared build outputs.
