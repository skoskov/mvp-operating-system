#!/usr/bin/env python3
"""Validate and apply the MVP OS project sync contract.

The script deliberately manages only paths declared by a release manifest.
Project-specific AGENTS.md, DECISIONS.md, product files, and OpenSpec files
remain review-only.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def version_key(value: str) -> tuple[int, int, int]:
    raw = value.removeprefix("v")
    parts = raw.split(".")
    if len(parts) != 3 or any(not part.isdigit() for part in parts):
        raise ValueError(f"Expected SemVer x.y.z, got {value!r}")
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def safe_relative_path(value: str) -> None:
    path = Path(value)
    if not value or value == "." or path.is_absolute() or ".." in path.parts:
        raise SystemExit(f"Unsafe managed path: {value!r}")


def safe_path(root: Path, relative: str) -> Path:
    safe_relative_path(relative)
    root_resolved = root.resolve()
    candidate = root / relative
    if candidate.is_symlink():
        raise SystemExit(f"Symlink is not allowed in managed path: {candidate}")
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise SystemExit(f"Managed path escapes root: {candidate}") from exc
    return candidate


def ensure_tree_safe(path: Path) -> None:
    if path.is_symlink():
        raise SystemExit(f"Symlink is not allowed in managed tree: {path}")
    if not path.exists() or not path.is_dir():
        return
    for child in path.rglob("*"):
        if child.is_symlink():
            raise SystemExit(f"Symlink is not allowed in managed tree: {child}")


def release_manifests(source_root: Path, applied: str, current: str) -> list[dict]:
    current_key = version_key(current)
    manifests: dict[str, dict] = {}
    for path in (source_root / "compatibility" / "releases").glob("v*.json"):
        manifest = load_json(path)
        version = manifest.get("version")
        if not isinstance(version, str):
            raise SystemExit(f"Release manifest has invalid version: {path}")
        if version in manifests:
            raise SystemExit(f"Duplicate release manifest version: {version}")
        manifests[version] = manifest
    if applied == current:
        return []

    selected: list[dict] = []
    cursor = applied
    while cursor != current:
        candidates = [
            manifest
            for manifest in manifests.values()
            if manifest.get("previous_version") == cursor
            and version_key(manifest.get("version", "0.0.0")) <= current_key
        ]
        if len(candidates) != 1:
            raise SystemExit(
                f"No unique release migration from v{cursor} to v{current}; "
                "publish a manifest with matching previous_version"
            )
        next_manifest = candidates[0]
        next_version = next_manifest["version"]
        if version_key(next_version) <= version_key(cursor):
            raise SystemExit(f"Release chain does not advance from v{cursor}")
        selected.append(next_manifest)
        cursor = next_version
    return selected


def source_version(source_root: Path) -> str:
    path = source_root / "VERSION"
    if not path.exists():
        raise SystemExit(f"Missing MVP OS VERSION: {path}")
    return path.read_text(encoding="utf-8").strip()


def tag_points_to_head(source_root: Path, tag: str) -> bool:
    tag_result = subprocess.run(
        ["git", "-C", str(source_root), "rev-parse", f"{tag}^{{commit}}"],
        capture_output=True,
        text=True,
        check=False,
    )
    head_result = subprocess.run(
        ["git", "-C", str(source_root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return (
        tag_result.returncode == 0
        and head_result.returncode == 0
        and tag_result.stdout.strip() == head_result.stdout.strip()
    )


def validate_source_lock(source_root: Path, current: str) -> None:
    lock = load_json(source_root / "mvp-os.lock")
    expected = {
        "schema_version": 2,
        "project_id": "mvp-operating-system",
        "mvp_os_version": current,
        "repository_role": "source",
        "sync_mode": "source",
        "source_repository": "skoskov/mvp-operating-system",
    }
    for key, value in expected.items():
        if lock.get(key) != value:
            raise SystemExit(
                f"Source lock {key} mismatch: {lock.get(key)!r} != {value!r}"
            )
    publication_status = lock.get("publication_status")
    release = lock.get("release")
    if publication_status == "candidate":
        if release is not None:
            raise SystemExit("Candidate source lock must not claim a release tag")
    elif publication_status == "published":
        if release != f"v{current}":
            raise SystemExit("Published source lock must claim the matching release tag")
        if not tag_points_to_head(source_root, release):
            raise SystemExit("Published source lock release tag must point to HEAD")
    else:
        raise SystemExit(f"Invalid source publication_status: {publication_status!r}")
    project_control = lock.get("project_control")
    if not isinstance(project_control, dict):
        raise SystemExit("Source lock needs project_control metadata")
    if project_control.get("schema_version") != 2:
        raise SystemExit("Source lock project_control must use schema_version 2")
    if project_control.get("status") not in {"pending-review", "active"}:
        raise SystemExit("Source lock project_control status must be pending-review or active")
    if project_control.get("current_path") != "project-control/CURRENT.json":
        raise SystemExit("Source lock project_control current_path mismatch")


def path_differs(source: Path, destination: Path) -> bool:
    """Return whether managed source content is missing or different.

    The check intentionally does not delete destination-only files. A future
    release can explicitly add pruning after a separate migration decision.
    """
    if source.is_file():
        return not destination.is_file() or source.read_bytes() != destination.read_bytes()
    if not destination.is_dir():
        return True
    for source_child in source.iterdir():
        destination_child = destination / source_child.name
        if path_differs(source_child, destination_child):
            return True
    return False


def effective_managed_paths(releases: list[dict]) -> list[dict]:
    """Return each destination once, using the newest release declaration."""
    by_destination: dict[str, dict] = {}
    for release in releases:
        for item in release["managed_paths"]:
            by_destination[item["destination"]] = item
    return list(by_destination.values())


def validate(source_root: Path) -> None:
    current = source_version(source_root)
    version_key(current)
    validate_source_lock(source_root, current)
    registry = load_json(source_root / "compatibility" / "projects.json")
    if registry.get("current_version") != current:
        raise SystemExit(
            "Registry current_version does not match VERSION: "
            f"{registry.get('current_version')} != {current}"
        )

    statuses_value = registry.get("statuses", [])
    if not isinstance(statuses_value, list):
        raise SystemExit("Registry statuses must be a list")
    statuses = set(statuses_value)
    if statuses != {"active", "paused", "archived"}:
        raise SystemExit("Registry statuses must be active, paused, archived")

    ids: set[str] = set()
    projects = registry.get("projects", [])
    if not isinstance(projects, list):
        raise SystemExit("Registry projects must be a list")
    for project in projects:
        if not isinstance(project, dict):
            raise SystemExit("Every registry project must be an object")
        project_id = project.get("id")
        if not project_id or project_id in ids:
            raise SystemExit(f"Registry project id is missing or duplicated: {project_id!r}")
        ids.add(project_id)
        if project.get("status") not in statuses:
            raise SystemExit(f"Invalid status for {project_id}: {project.get('status')!r}")
        if project.get("sync_mode") != "pull-pr":
            raise SystemExit(f"Unsupported sync_mode for {project_id}")
        default_branch = project.get("default_branch", "main")
        if not isinstance(default_branch, str) or not default_branch.strip():
            raise SystemExit(f"Invalid default_branch for {project_id}: {default_branch!r}")

    releases = release_manifests(source_root, "0.0.0", current)
    if not releases or releases[-1].get("version") != current:
        raise SystemExit("Current VERSION has no matching release manifest")
    for release in releases:
        managed_paths = release.get("managed_paths", [])
        review_paths = release.get("review_paths", [])
        if not isinstance(managed_paths, list) or not isinstance(review_paths, list):
            raise SystemExit("Release paths must be lists")
        destinations: set[str] = set()
        for item in managed_paths:
            if not isinstance(item, dict) or not item.get("source") or not item.get("destination"):
                raise SystemExit("Every managed path needs source and destination")
            source = str(item["source"])
            destination = str(item["destination"])
            safe_path(source_root, source)
            safe_relative_path(destination)
            if destination in destinations:
                raise SystemExit(f"Duplicate managed destination: {destination}")
            destinations.add(destination)
            source_path = safe_path(source_root, source)
            if not source_path.exists():
                raise SystemExit(f"Managed source path does not exist: {source}")
            ensure_tree_safe(source_path)
        for review_path in review_paths:
            safe_relative_path(str(review_path))

    print(f"MVP OS compatibility metadata valid: v{current}")


def require_published_source(source_root: Path, current: str) -> None:
    lock = load_json(source_root / "mvp-os.lock")
    if lock.get("publication_status") != "published":
        raise SystemExit("Downstream sync refuses an unpublished MVP OS candidate")
    release = f"v{current}"
    if lock.get("release") != release or not tag_points_to_head(source_root, release):
        raise SystemExit("Downstream sync requires the published tag to point to HEAD")


def sync(
    source_root: Path,
    project_root: Path,
    lock_path: Path,
    dry_run: bool,
    repository: str,
    allow_overwrite: bool,
) -> int:
    validate(source_root)
    require_published_source(source_root, source_version(source_root))
    lock = load_json(project_root / lock_path)
    project_id = lock.get("project_id")
    registry = load_json(source_root / "compatibility" / "projects.json")
    project = next(
        (item for item in registry["projects"] if item.get("id") == project_id), None
    )
    if project is None:
        print(f"SKIP {project_id!r}: project is not registered")
        return 0
    if project["status"] != "active":
        print(f"SKIP {project_id}: status={project['status']}")
        return 0
    if project.get("repository") != repository:
        raise SystemExit(
            f"Registry repository mismatch for {project_id}: "
            f"{project.get('repository')} != {repository}"
        )

    current = source_version(source_root)
    applied = lock.get("mvp_os_version", "0.0.0")
    if version_key(applied) > version_key(current):
        raise SystemExit(f"Project lock is newer than MVP OS: {applied} > {current}")
    releases = release_manifests(source_root, applied, current)
    if not releases:
        releases = [
            load_json(
                source_root / "compatibility" / "releases" / f"v{current}.json"
            )
        ]
    managed_paths = effective_managed_paths(releases)
    if not dry_run and version_key(applied) < version_key("2.1.1"):
        registration = (
            source_root
            / "skill/mvp-operating-system/bin/register_legacy_contracts.py"
        )
        subprocess.run(
            [sys.executable, str(registration), "--project-root", str(project_root)],
            check=True,
        )
    drift = any(
        path_differs(
            safe_path(source_root, item["source"]),
            safe_path(project_root, item["destination"]),
        )
        for item in managed_paths
    )
    if applied == current and not drift:
        print(f"OK {project_id}: already on MVP OS v{current}")
        return 0

    if applied == current and drift:
        print(f"DRIFT {project_id}: managed files differ from MVP OS v{current}")
        if not allow_overwrite:
            raise SystemExit(
                "Managed files drifted at the current version; "
                "rerun with --allow-overwrite after review"
            )
    for item in managed_paths:
        source = safe_path(source_root, item["source"])
        destination = safe_path(project_root, item["destination"])
        ensure_tree_safe(source)
        if destination.exists():
            ensure_tree_safe(destination)
        if not source.exists():
            raise SystemExit(f"Managed source path does not exist: {source}")
        print(f"SYNC {item['source']} -> {item['destination']}")
        if not dry_run:
            if source.is_dir():
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)

    if not dry_run:
        control_current = project_root / "project-control" / "CURRENT.json"
        lock["mvp_os_version"] = current
        lock["release"] = f"v{current}"
        lock["schema_version"] = 2
        project_control = lock.setdefault("project_control", {})
        project_control["schema_version"] = 2
        project_control["current_path"] = "project-control/CURRENT.json"
        if not control_current.exists():
            project_control["status"] = "pending"
            lock["sync_status"] = "project-control-migration-required"
        else:
            project_control.setdefault("status", "pending-review")
            lock["sync_status"] = (
                "synced" if project_control["status"] == "active" else "project-control-review-required"
            )
        (project_root / lock_path).write_text(
            json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    print(f"READY {project_id}: MVP OS v{current} {'would be ' if dry_run else ''}synced")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--source-root", type=Path, default=Path("."))

    sync_parser = subparsers.add_parser("sync")
    sync_parser.add_argument("--source-root", type=Path, required=True)
    sync_parser.add_argument("--project-root", type=Path, default=Path("."))
    sync_parser.add_argument("--lock", type=Path, default=Path("mvp-os.lock"))
    sync_parser.add_argument("--repository", required=True)
    sync_parser.add_argument("--allow-overwrite", action="store_true")
    sync_parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()
    if args.command == "validate":
        validate(args.source_root)
        return 0
    return sync(
        args.source_root,
        args.project_root,
        args.lock,
        args.dry_run,
        args.repository,
        args.allow_overwrite,
    )


if __name__ == "__main__":
    sys.exit(main())
