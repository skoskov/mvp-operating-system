#!/usr/bin/env python3
"""Single non-destructive verification entrypoint for MVP OS."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV = os.environ.copy()
ENV.setdefault("PYTHONPYCACHEPREFIX", "/tmp/mvp-os-pyc")


def run(argv: list[str]) -> None:
    print("$", " ".join(argv))
    completed = subprocess.run(argv, cwd=ROOT, env=ENV)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def main() -> None:
    run([sys.executable, "scripts/mvp_os_sync.py", "validate", "--source-root", "."])
    run([
        sys.executable,
        "skill/mvp-operating-system/bin/project_control.py",
        "validate",
        "--project-root",
        ".",
    ])
    run([
        sys.executable,
        "skill/mvp-operating-system/bin/project_control.py",
        "bootstrap",
        "--project-root",
        ".",
    ])
    run([
        sys.executable,
        "skill/mvp-operating-system/bin/project_control.py",
        "doctor",
        "--project-root",
        ".",
    ])
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"])
    run([
        sys.executable,
        "template/mvp-project-template/.agents/skills/mvp-operating-system/bin/project_control.py",
        "validate",
        "--project-root",
        "template/mvp-project-template",
    ])
    run([
        sys.executable,
        "template/mvp-project-template/.agents/skills/mvp-operating-system/bin/project_control.py",
        "doctor",
        "--project-root",
        "template/mvp-project-template",
    ])
    print("MVP OS verification: PASS")


if __name__ == "__main__":
    main()
