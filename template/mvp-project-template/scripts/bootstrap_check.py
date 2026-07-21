from pathlib import Path

REQUIRED = [
    "AGENTS.md",
    ".codex/config.toml",
    ".codex/agents/architect.toml",
    ".codex/agents/implementer.toml",
    ".codex/agents/devops_qa.toml",
    ".codex/agents/release_manager.toml",
    ".agents/skills/mvp-operating-system/SKILL.md",
    ".agents/skills/mvp-operating-system/bin/gate_check.py",
    ".agents/skills/mvp-operating-system/assets/task-contract-template.json",
    ".agents/skills/mvp-operating-system/references/outcome-reuse-gate.md",
    ".agents/skills/mvp-operating-system/references/hermes-runtime.md",
    ".agents/skills/mvp-operating-system/references/evidence-manifest.md",
    ".agents/skills/mvp-operating-system/references/idea-intake.md",
    ".agents/skills/mvp-operating-system/references/launch-market-research.md",
    ".agents/skills/mvp-operating-system/references/brand-design-ux.md",
    ".agents/skills/mvp-operating-system/references/environment-preflight.md",
    ".agents/skills/mvp-operating-system/references/analytics-observability-plan.md",
    ".agents/skills/mvp-operating-system/references/support-feedback-ops.md",
    ".agents/skills/mvp-operating-system/references/build-deploy-verification-plan.md",
    Path(".agents") / "skills" / "mvp-operating-system" / "references" / "acceptance-release-gate.md",
    Path(".agents") / "skills" / "mvp-operating-system" / "references" / "pre-launch-iteration-update.md",
    "product/idea-intake.md",
    "product/brand-design-ux.md",
    "market/launch-market-research.md",
    Path("ops") / "environment-preflight.md",
    Path("analytics") / "analytics-observability-plan.md",
    Path("support") / "support-feedback-plan.md",
    Path("build") / "build-deploy-verification-plan.md",
    Path("qa") / "acceptance-release-gate.md",
    Path("iteration") / "pre-launch-iteration-update.md",
    "openspec/README.md",
    "docs/agent-protocol.md",
    "docs/project-state.md",
    "docs/memory-policy.md",
    "docs/verification.md",
    "mvp-os.lock",
    ".github/workflows/mvp-os-sync.yml",
    "Makefile",
]

missing = [path for path in REQUIRED if not Path(path).exists()]

if missing:
    print("Missing required operating-layer files:")
    for path in missing:
        print(f"- {path}")
    raise SystemExit(1)

print("Operating layer bootstrap check passed.")
