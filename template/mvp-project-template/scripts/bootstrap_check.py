from pathlib import Path

REQUIRED = [
    "AGENTS.md",
    ".agents/skills/mvp-operating-system/SKILL.md",
    ".agents/skills/mvp-operating-system/references/idea-intake.md",
    ".agents/skills/mvp-operating-system/references/launch-market-research.md",
    ".agents/skills/mvp-operating-system/references/brand-design-ux.md",
    ".agents/skills/mvp-operating-system/references/environment-preflight.md",
    ".agents/skills/mvp-operating-system/references/analytics-observability-plan.md",
    ".agents/skills/mvp-operating-system/references/support-feedback-ops.md",
    ".agents/skills/mvp-operating-system/references/build-deploy-verification-plan.md",
    Path(".agents") / "skills" / "mvp-operating-system" / "references" / "acceptance-release-gate.md",
    "product/idea-intake.md",
    "product/brand-design-ux.md",
    "market/launch-market-research.md",
    Path("ops") / "environment-preflight.md",
    Path("analytics") / "analytics-observability-plan.md",
    Path("support") / "support-feedback-plan.md",
    Path("build") / "build-deploy-verification-plan.md",
    Path("qa") / "acceptance-release-gate.md",
    "openspec/README.md",
    "docs/memory-policy.md",
    "docs/verification.md",
    "Makefile",
]

missing = [path for path in REQUIRED if not Path(path).exists()]

if missing:
    print("Missing required operating-layer files:")
    for path in missing:
        print(f"- {path}")
    raise SystemExit(1)

print("Operating layer bootstrap check passed.")
