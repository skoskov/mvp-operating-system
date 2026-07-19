#!/usr/bin/env python3
"""Validate and read the MVP OS Project Control v2 current-state bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_FILES = (
    "goal.json",
    "decisions.json",
    "scope.json",
    "architecture.json",
    "commands.json",
    "access.json",
    "runtime-requirements.json",
    "acceptance.json",
)
FORBIDDEN_SECRET_KEYS = {
    "authorization",
    "bearer",
    "cookie",
    "credential",
    "credential_value",
    "credentials",
    "password",
    "token",
    "api_key",
    "apikey",
    "secret",
    "secret_value",
    "client_secret",
    "private_key",
    "session_token",
}


class ControlError(ValueError):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ControlError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ControlError(f"invalid JSON: {path}: {exc}") from exc


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ControlError(f"timestamp needs timezone: {value}")
    return parsed.astimezone(timezone.utc)


SAFE_REFERENCE_KEYS = {
    "argv",
    "artifact_refs",
    "contract_version",
    "id",
    "source_commit",
    "source_events",
    "secret_ref",
}
KNOWN_SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?<![A-Za-z0-9])(?:gh[opusr]_|github_pat_|sk-|xox[baprs]-|AIza)[A-Za-z0-9_\-]{12,}"),
    re.compile(r"(?<![A-Za-z0-9])\d{6,12}:[A-Za-z0-9_-]{25,}"),
)
SECRET_REF_PATTERN = re.compile(r"^secret://[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)+$")


def string_entropy(value: str) -> float:
    if not value:
        return 0.0
    counts = {character: value.count(character) for character in set(value)}
    return -sum((count / len(value)) * math.log2(count / len(value)) for count in counts.values())


def looks_like_secret(value: str, key: str | None) -> bool:
    if key in SAFE_REFERENCE_KEYS or value.startswith(("context:", "working-tree:", "sha256:")):
        return False
    if any(pattern.search(value) for pattern in KNOWN_SECRET_PATTERNS):
        return True
    candidates = [
        candidate
        for candidate in re.findall(r"[A-Za-z0-9_+=/.-]{24,}", value)
        if not ("." in candidate and "/" in candidate)
    ]
    return any(string_entropy(candidate) >= 4.0 for candidate in candidates)


def walk_values(value: Any, location: str = "$", key: str | None = None) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_SECRET_KEYS:
                raise ControlError(f"secret value field forbidden at {location}.{key}")
            walk_values(child, f"{location}.{key}", lowered)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk_values(child, f"{location}[{index}]", key)
    elif isinstance(value, str) and looks_like_secret(value, key):
        raise ControlError(f"possible secret value forbidden at {location}")


def read_bundle(
    project_root: Path, current_override: dict | None = None
) -> tuple[dict, Path, dict[str, Any]]:
    control_root = project_root.resolve() / "project-control"
    current = current_override or load_json(control_root / "CURRENT.json")
    if not isinstance(current, dict) or current.get("schema_version") != 2:
        raise ControlError("CURRENT.json must use schema_version 2")
    release_id = current.get("release_id")
    if not isinstance(release_id, str) or not release_id or "/" in release_id or ".." in release_id:
        raise ControlError("CURRENT.json has unsafe release_id")
    release_root = control_root / "releases" / release_id
    manifest_path = release_root / "manifest.json"
    manifest = load_json(manifest_path)
    if current.get("manifest_sha256") != digest(manifest_path):
        raise ControlError("CURRENT.json manifest_sha256 mismatch")
    if manifest.get("schema_version") != 2 or manifest.get("release_id") != release_id:
        raise ControlError("manifest identity mismatch")
    files = manifest.get("files")
    if not isinstance(files, dict) or set(files) != set(REQUIRED_FILES):
        raise ControlError("manifest must list exactly the required current files")
    bundle: dict[str, Any] = {}
    for name in REQUIRED_FILES:
        expected = files.get(name)
        path = release_root / name
        if expected != digest(path):
            raise ControlError(f"release hash mismatch: {name}")
        payload = load_json(path)
        walk_values(payload)
        bundle[name] = payload
    return current, release_root, bundle


def evidence_state(item: dict, now: datetime) -> str:
    result = item.get("result")
    try:
        verified = parse_time(str(item["verified_at"]))
        ttl = int(item["ttl_seconds"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ControlError(f"invalid evidence for {item.get('id', '<unknown>')}") from exc
    if ttl < 0 or result not in {"proven", "failed", "blocked", "unverified", "not_needed"}:
        raise ControlError(f"invalid evidence state for {item.get('id', '<unknown>')}")
    if result != "proven":
        return str(result)
    age = (now - verified).total_seconds()
    return "fresh" if 0 <= age <= ttl else "stale"


def latest_evidence_state(item: dict, now: datetime) -> str:
    evidence = item.get("evidence", [])
    if not evidence:
        return "missing"
    dated = [(parse_time(str(entry["verified_at"])), entry) for entry in evidence]
    latest_time = max(timestamp for timestamp, _ in dated)
    latest = [entry for timestamp, entry in dated if timestamp == latest_time]
    states = {evidence_state(entry, now) for entry in latest}
    if len(states) != 1:
        return "conflict"
    return states.pop()


def validate_bundle(
    project_root: Path, current_override: dict | None = None
) -> tuple[dict, Path, dict[str, Any]]:
    current, release_root, bundle = read_bundle(project_root, current_override)
    goal = bundle["goal.json"]
    if not isinstance(goal, dict) or not goal.get("objective") or not goal.get("next_safe_step"):
        raise ControlError("goal.json needs objective and next_safe_step")

    decisions = bundle["decisions.json"].get("decisions", [])
    ids: set[str] = set()
    for item in decisions:
        if item.get("status") != "active":
            raise ControlError("current decisions may contain only active decisions")
        decision_id = item.get("id")
        if not decision_id or decision_id in ids:
            raise ControlError(f"missing or duplicate decision id: {decision_id}")
        ids.add(decision_id)
        if not item.get("source_events"):
            raise ControlError(f"decision lacks source_events: {decision_id}")

    commands = bundle["commands.json"].get("commands", [])
    for item in commands:
        argv = item.get("argv")
        if not isinstance(argv, list) or not argv or not all(isinstance(v, str) and v for v in argv):
            raise ControlError(f"command needs non-empty argv: {item.get('id')}")
        if "shell" in item or "command" in item:
            raise ControlError(f"shell command strings are forbidden: {item.get('id')}")

    access = bundle["access.json"].get("access", [])
    for item in access:
        reference = item.get("secret_ref")
        if reference is not None and not SECRET_REF_PATTERN.fullmatch(str(reference)):
            raise ControlError(f"invalid secret_ref: {item.get('id')}")
        if reference is not None:
            segments = str(reference).removeprefix("secret://").split("/")
            if any(looks_like_secret(segment, None) for segment in segments):
                raise ControlError(f"secret_ref contains a value, not a logical id: {item.get('id')}")

    requirements = bundle["runtime-requirements.json"].get("capabilities", [])
    for item in requirements:
        if item.get("required") and not item.get("evidence"):
            raise ControlError(f"required capability lacks evidence: {item.get('id')}")
        for evidence in item.get("evidence", []):
            evidence_state(evidence, datetime.now(timezone.utc))
    return current, release_root, bundle


def command_text(argv: list[str]) -> str:
    return " ".join(json.dumps(part) if any(ch.isspace() for ch in part) else part for part in argv)


def bootstrap(project_root: Path, as_json: bool = False) -> int:
    current, _, bundle = validate_bundle(project_root)
    now = datetime.now(timezone.utc)
    requirements = bundle["runtime-requirements.json"].get("capabilities", [])
    capabilities = [
        {
            "id": item["id"],
            "required": bool(item.get("required")),
            "states": [evidence_state(evidence, now) for evidence in item.get("evidence", [])],
            "current_state": latest_evidence_state(item, now),
        }
        for item in requirements
    ]
    output = {
        "project_id": bundle["goal.json"].get("project_id"),
        "project_version": bundle["goal.json"].get("project_version"),
        "release_id": current["release_id"],
        "objective": bundle["goal.json"]["objective"],
        "next_safe_step": bundle["goal.json"]["next_safe_step"],
        "decisions": [item["statement"] for item in bundle["decisions.json"].get("decisions", [])],
        "included": bundle["scope.json"].get("included", []),
        "excluded": bundle["scope.json"].get("excluded", []),
        "architecture": bundle["architecture.json"].get("components", []),
        "access": [
            {"id": item["id"], "status": item.get("status", "unknown"), "required": bool(item.get("required"))}
            for item in bundle["access.json"].get("access", [])
        ],
        "capabilities": capabilities,
        "commands": [
            {"id": item["id"], "argv": item["argv"], "side_effect": item.get("side_effect")}
            for item in bundle["commands.json"].get("commands", [])
        ],
        "gates": bundle["acceptance.json"].get("gates", []),
        "legacy_startup_reads": 0,
    }
    if as_json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    print(f"PROJECT {output['project_id']} {output['project_version']} / release {output['release_id']}")
    print(f"GOAL: {output['objective']}")
    print("ACTIVE DECISIONS:")
    for value in output["decisions"]:
        print(f"- {value}")
    print("INCLUDED:")
    for value in output["included"]:
        print(f"- {value}")
    print("EXCLUDED:")
    for value in output["excluded"]:
        print(f"- {value}")
    print("ARCHITECTURE:")
    for item in output["architecture"]:
        print(f"- {item.get('id')}: {item.get('role')}")
    print("ACCESS:")
    for item in output["access"]:
        print(f"- {item['id']}: {item['status']} ({'required' if item['required'] else 'optional'})")
    print("CAPABILITIES:")
    for item in capabilities:
        print(f"- {item['id']}: {item['current_state']} ({'required' if item['required'] else 'optional'})")
    print("COMMANDS:")
    for item in output["commands"]:
        print(f"- {item['id']}: {command_text(item['argv'])} [{item['side_effect']}]")
    print("GATES:")
    for value in output["gates"]:
        print(f"- {value}")
    print(f"NEXT: {output['next_safe_step']}")
    print("LEGACY_STARTUP_READS: 0")
    return 0


def doctor(project_root: Path) -> int:
    _, _, bundle = validate_bundle(project_root)
    now = datetime.now(timezone.utc)
    failures: list[str] = []
    for item in bundle["access.json"].get("access", []):
        if item.get("required") and item.get("status") != "available":
            failures.append(f"access {item.get('id')}: {item.get('status', 'unknown')}")
    for item in bundle["runtime-requirements.json"].get("capabilities", []):
        state = latest_evidence_state(item, now)
        if item.get("required") and state != "fresh":
            failures.append(f"capability {item.get('id')}: {state}")
    for item in bundle["commands.json"].get("commands", []):
        executable = item["argv"][0]
        if "/" in executable:
            working_directory = item.get("working_directory", ".")
            available = (project_root / working_directory / executable).is_file()
        else:
            available = shutil.which(executable) is not None
        if item.get("required") and not available:
            failures.append(f"command {item.get('id')}: executable missing: {executable}")
    if failures:
        print("PROJECT CONTROL DOCTOR: BLOCKED")
        for failure in failures:
            print(f"- {failure}")
        return 2
    print("PROJECT CONTROL DOCTOR: READY")
    return 0


def publish(project_root: Path, release_id: str, source_commit: str, activated_at: str) -> int:
    if not release_id or "/" in release_id or ".." in release_id:
        raise ControlError("unsafe release_id")
    control_root = project_root.resolve() / "project-control"
    release_root = control_root / "releases" / release_id
    manifest_path = release_root / "manifest.json"
    current_path = control_root / "CURRENT.json"
    if manifest_path.exists():
        raise ControlError("publish refuses to overwrite an existing release")
    parent_release = None
    if current_path.exists():
        previous, _, _ = validate_bundle(project_root)
        parent_release = previous["release_id"]
        if parent_release == release_id:
            raise ControlError("new release_id must differ from CURRENT")
    files: dict[str, str] = {}
    for name in REQUIRED_FILES:
        path = release_root / name
        payload = load_json(path)
        walk_values(payload)
        files[name] = digest(path)
    timestamp = parse_time(activated_at).isoformat()
    goal = load_json(release_root / "goal.json")
    manifest = {
        "schema_version": 2,
        "release_id": release_id,
        "project_id": goal.get("project_id"),
        "created_at": timestamp,
        "source_commit": source_commit,
        "parent_release": parent_release,
        "files": files,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    current = {
        "schema_version": 2,
        "release_id": release_id,
        "manifest_sha256": digest(manifest_path),
        "activated_at": timestamp,
    }
    try:
        validate_bundle(project_root, current_override=current)
    except Exception:
        manifest_path.unlink(missing_ok=True)
        raise
    current_path.parent.mkdir(parents=True, exist_ok=True)
    current_tmp = current_path.with_suffix(".json.tmp")
    current_tmp.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    current_tmp.replace(current_path)
    print(f"PROJECT CONTROL PUBLISHED: {release_id}")
    return 0


def initialize(project_root: Path, project_id: str) -> int:
    if not project_id or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for ch in project_id):
        raise ControlError("project_id may contain only letters, numbers, dot, underscore, and hyphen")
    current, release_root, bundle = validate_bundle(project_root)
    goal = bundle["goal.json"]
    if goal.get("project_id") != "replace-with-project-id":
        raise ControlError("initialize is allowed only on an untouched project template")
    lock_path = project_root.resolve() / "mvp-os.lock"
    lock = load_json(lock_path)
    if lock.get("project_id") != "replace-me":
        raise ControlError("template lock project_id was already initialized")

    goal["project_id"] = project_id
    goal_path = release_root / "goal.json"
    goal_path.write_text(json.dumps(goal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest_path = release_root / "manifest.json"
    manifest = load_json(manifest_path)
    manifest["project_id"] = project_id
    manifest["source_commit"] = "project-bootstrap"
    manifest["files"] = {name: digest(release_root / name) for name in REQUIRED_FILES}
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    current["manifest_sha256"] = digest(manifest_path)
    current_path = project_root.resolve() / "project-control" / "CURRENT.json"
    current_path.write_text(
        json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lock["project_id"] = project_id
    lock_path.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    validate_bundle(project_root)
    print(f"PROJECT CONTROL INITIALIZED: {project_id}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "bootstrap", "doctor", "publish", "initialize"))
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--release-id")
    parser.add_argument("--source-commit", default="uncommitted-migration")
    parser.add_argument("--activated-at")
    parser.add_argument("--project-id")
    args = parser.parse_args()
    try:
        if args.command == "validate":
            current, _, _ = validate_bundle(args.project_root)
            print(f"PROJECT CONTROL VALID: {current['release_id']}")
            return 0
        if args.command == "bootstrap":
            return bootstrap(args.project_root, args.as_json)
        if args.command == "publish":
            if not args.release_id or not args.activated_at:
                raise ControlError("publish needs --release-id and --activated-at")
            return publish(args.project_root, args.release_id, args.source_commit, args.activated_at)
        if args.command == "initialize":
            if not args.project_id:
                raise ControlError("initialize needs --project-id")
            return initialize(args.project_root, args.project_id)
        return doctor(args.project_root)
    except ControlError as exc:
        print(f"PROJECT CONTROL INVALID: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
