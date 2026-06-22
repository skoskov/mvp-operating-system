# Analytics / Observability Plan

Use this gate after Product/Technical Brief and before Build / Deploy / Verification Plan.

## Purpose

Define the minimum useful measurement for the MVP without tracking every click.

For MVPs, focus on:

- traffic source;
- start of use;
- activation;
- core value event;
- user-visible errors;
- system errors;
- feedback.

## Default stack

- Product analytics: Umami.
- Error and uptime monitoring: GlitchTip.
- PostHog is not the default. Use it only when a Decision Card approves heavier product analytics needs.

## Required fields

```text
Measurement goal:
<what decision this analytics must support>

Product analytics tool:
Umami / other approved tool

Issue monitoring tool:
GlitchTip / other approved tool

Activation event:
<the first action proving the user reached initial value>

Core value event:
<the action proving the main MVP promise worked>

Traffic source rules:
<referrer, UTM, invite/referral code, partner, campaign, manual source>

MVP events:
- traffic_source_detected
- app_started
- onboarding_started
- activation_completed
- core_action_completed
- user_error_seen
- system_error_happened
- feedback_sent

Event properties:
<only essential properties; avoid personal data>

Error taxonomy:
- user input error:
- integration error:
- generation/AI error:
- permission/access error:
- system error:

Where data is stored:
<Umami / GlitchTip / project DB / logs>

Where team views reports:
<dashboard URL or TBD>

Daily report:
<which numbers are checked daily>

What not to track:
<clicks, sensitive data, personal notes, private message contents, or other excluded data>

Privacy notes:
<what data is not collected and why>

Deferred analytics:
<what is intentionally not built in MVP>
```

## Rules

- Do not track every click in MVP.
- Use 5-8 product events unless the project requires more.
- Always include source, start, activation, core value, errors, and feedback.
- Do not capture sensitive content, private notes, message bodies, or unnecessary personal data.
- Codex must add only the events named in this plan unless a Decision Card approves more.
- Build / Deploy / Verification Plan must include analytics setup and smoke checks when analytics is in MVP scope.
