#!/usr/bin/env python3
"""Collect reported MVP OS lock status from registered GitHub projects."""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_lock(repository: str, lock_path: str, token: str | None) -> dict:
    url = f"https://api.github.com/repos/{repository}/contents/{lock_path}?ref=main"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "mvp-os-status"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    content = base64.b64decode(payload["content"]).decode("utf-8")
    return json.loads(content)


def collect(registry_path: Path, output_path: Path, token: str | None) -> bool:
    registry = load_json(registry_path)
    report: list[dict] = []
    changed = False
    for project in registry.get("projects", []):
        if project.get("status") != "active":
            report.append({"id": project.get("id"), "status": "not-checked"})
            continue
        project_id = project["id"]
        lock_path = project.get("lock_path", "mvp-os.lock")
        try:
            lock = fetch_lock(project["repository"], lock_path, token)
            if lock.get("project_id") != project_id:
                raise ValueError(
                    f"lock project_id mismatch: {lock.get('project_id')!r}"
                )
            if lock.get("source_repository") != "skoskov/mvp-operating-system":
                raise ValueError("lock source_repository mismatch")
            reported_version = lock.get("mvp_os_version")
            reported_status = lock.get("sync_status", "unknown")
            report.append(
                {
                    "id": project_id,
                    "status": reported_status,
                    "mvp_os_version": reported_version,
                }
            )
        except (
            HTTPError,
            URLError,
            KeyError,
            ValueError,
            json.JSONDecodeError,
            TimeoutError,
        ) as exc:
            reported_version = None
            reported_status = "lock-unavailable"
            report.append(
                {"id": project_id, "status": reported_status, "error": str(exc)}
            )

        if project.get("last_known_version") != reported_version:
            project["last_known_version"] = reported_version
            changed = True
        if project.get("last_known_status") != reported_status:
            project["last_known_status"] = reported_status
            changed = True

    if changed:
        registry_path.write_text(
            json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps({"schema_version": 1, "projects": report}, indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--token", default=os.environ.get("GH_TOKEN"))
    args = parser.parse_args()
    changed = collect(args.registry, args.output, args.token)
    print("Registry status changed" if changed else "Registry status unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
