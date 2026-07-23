#!/usr/bin/env python3
"""Register existing schema v1 task contracts in a new Project Control release."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).with_name("project_control.py")
SPEC = importlib.util.spec_from_file_location("mvp_os_project_control", SCRIPT)
assert SPEC and SPEC.loader
project_control = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(project_control)


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def legacy_contracts(project_root: Path) -> list[Path]:
    outputs = project_root / "outputs"
    if not outputs.is_dir() or outputs.is_symlink():
        return []
    matches = []
    for path in outputs.rglob("*.json"):
        if path.is_symlink() or not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        if (
            isinstance(payload, dict)
            and payload.get("schema_version") == 1
            and all(key in payload for key in ("task_id", "scope", "outcome", "reuse"))
        ):
            matches.append(path)
    return sorted(matches)


def register(project_root: Path) -> int:
    current_path = project_root / "project-control/CURRENT.json"
    if not current_path.is_file():
        print("LEGACY CONTRACT REGISTRATION: SKIP (Project Control is not initialized)")
        return 0
    current, release_root, bundle = project_control.validate_bundle(project_root)
    hashes = sorted({digest(path) for path in legacy_contracts(project_root)})
    registered = bundle["acceptance.json"].get("legacy_task_contract_sha256", [])
    if not isinstance(registered, list):
        raise project_control.ControlError("legacy_task_contract_sha256 must be a list")
    merged = sorted(set(registered) | set(hashes))
    if merged == sorted(registered):
        print(f"LEGACY CONTRACT REGISTRATION: READY ({len(hashes)} contract(s))")
        return 0

    releases_root = project_root / "project-control/releases"
    release_number = int(current["release_id"]) + 1
    while (releases_root / f"{release_number:06d}").exists():
        release_number += 1
    release_id = f"{release_number:06d}"
    destination = releases_root / release_id
    destination.mkdir(parents=True)
    for name in project_control.REQUIRED_FILES:
        shutil.copy2(release_root / name, destination / name)
    acceptance_path = destination / "acceptance.json"
    acceptance = json.loads(acceptance_path.read_text(encoding="utf-8"))
    acceptance["legacy_task_contract_sha256"] = merged
    acceptance_path.write_text(
        json.dumps(acceptance, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    source_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=project_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    project_control.publish(
        project_root,
        release_id,
        source_commit,
        datetime.now(timezone.utc).isoformat(),
    )
    print(
        f"LEGACY CONTRACT REGISTRATION: REGISTERED {len(hashes)} contract(s) "
        f"in Project Control {release_id}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path("."))
    args = parser.parse_args()
    return register(args.project_root.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
