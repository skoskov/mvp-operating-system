# Hard Execution Gate

Status: mandatory

Execution is allowed only when the full required stack is verified and working.

If any required stack element is broken, flaky, unavailable, blocked, or unverified, stop immediately. Record the blocker and the exact next action. Do not continue by changing the product, reducing the UX, narrowing the demo, or hiding the failure behind a workaround.

## Required Preflight

| Element | Required when | Stop condition |
| --- | --- | --- |
| Repository state | Always | Unknown branch, unsafe dirty state, or unclear write scope |
| Dependency manager | Build or code work | Install/build commands unavailable or unreliable |
| Build command | App or UI work | Build fails or cannot be reproduced |
| Test/verification command | Any implementation | Required tests/evals fail or cannot run |
| Local runtime | Running app required | App cannot start or route cannot be reached |
| Browser QA tool | UI/click/demo work | Browser cannot inspect, screenshot, click, or navigate reliably |
| VPS/runtime service | Deployment work | Service cannot start, restart, or report health |
| Reverse proxy/CDN/public URL | Public demo work | Public route differs from origin, hangs, closes, caches stale content, or cannot be verified |
| Screenshots and DOM | User-visible work | Baseline or final state cannot be captured |
| Click/navigation checks | Interactive demo work | Any visible action is inert, broken, ambiguous, or unverified |
| Rollback path | Public route/deploy changes | Rollback command or backup is missing |

## Forbidden Completion Patterns

These are forbidden unless the human explicitly approves the exact tradeoff before implementation:

- replacing a product UI with a static shell;
- reducing page count, navigation, actions, or state transitions;
- hiding a broken integration behind a fake success state;
- treating HTTP 200 as proof that a user flow works;
- reporting READY when browser QA failed or was skipped;
- changing architecture to bypass a tool failure;
- using screenshots as a substitute for clickable behavior;
- narrowing demo scope after implementation starts;
- presenting synthetic or dry-run behavior as a connected integration;
- calling a public demo ready when the public path behaves differently from local or origin checks.

## Baseline And Final Comparison

For every substantial user-visible task, capture baseline before edits and final state after implementation or deployment.

Final verification must prove:

- no baseline product capability was lost;
- all visible controls work or are removed;
- all promised pages/routes are reachable;
- browser-visible UI matches the intended product direction;
- no console/runtime blockers affect the demo;
- public route behavior matches the verified origin/local route.

If the final state regresses from baseline, the task is not complete.

## READY Definition

`READY` means the intended product behavior works through the intended user path with the intended stack.

`READY` never means a fallback page loads, a mock replaces the product, local works while public is broken, or the UI is less capable than before.
