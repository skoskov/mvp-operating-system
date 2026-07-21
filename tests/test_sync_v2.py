from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/mvp_os_sync.py"
SPEC = importlib.util.spec_from_file_location("mvp_os_sync", SCRIPT)
assert SPEC and SPEC.loader
mvp_os_sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mvp_os_sync)


class SyncV2Tests(unittest.TestCase):
    def test_source_lock_candidate_does_not_claim_release_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            lock = {
                "schema_version": 2,
                "project_id": "mvp-operating-system",
                "mvp_os_version": "2.0.0",
                "release": None,
                "publication_status": "candidate",
                "repository_role": "source",
                "sync_mode": "source",
                "source_repository": "skoskov/mvp-operating-system",
                "project_control": {
                    "schema_version": 2,
                    "status": "pending-review",
                    "current_path": "project-control/CURRENT.json",
                },
            }
            (source / "mvp-os.lock").write_text(
                json.dumps(lock) + "\n", encoding="utf-8"
            )
            mvp_os_sync.validate_source_lock(source, "2.0.0")
            lock["release"] = "v2.0.0"
            (source / "mvp-os.lock").write_text(
                json.dumps(lock) + "\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(
                SystemExit, "Candidate source lock must not claim a release tag"
            ):
                mvp_os_sync.validate_source_lock(source, "2.0.0")

    def test_published_source_lock_requires_matching_release_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            lock = {
                "schema_version": 2,
                "project_id": "mvp-operating-system",
                "mvp_os_version": "2.0.0",
                "release": None,
                "publication_status": "published",
                "repository_role": "source",
                "sync_mode": "source",
                "source_repository": "skoskov/mvp-operating-system",
                "project_control": {
                    "schema_version": 2,
                    "status": "active",
                    "current_path": "project-control/CURRENT.json",
                },
            }
            (source / "mvp-os.lock").write_text(
                json.dumps(lock) + "\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(
                SystemExit, "Published source lock must claim the matching release tag"
            ):
                mvp_os_sync.validate_source_lock(source, "2.0.0")
            lock["release"] = "v2.0.0"
            (source / "mvp-os.lock").write_text(
                json.dumps(lock) + "\n", encoding="utf-8"
            )
            with patch.object(mvp_os_sync, "tag_points_to_head", return_value=True):
                mvp_os_sync.validate_source_lock(source, "2.0.0")
            with patch.object(mvp_os_sync, "tag_points_to_head", return_value=False):
                with self.assertRaisesRegex(
                    SystemExit, "Published source lock release tag must point to HEAD"
                ):
                    mvp_os_sync.validate_source_lock(source, "2.0.0")

    def test_v1_project_becomes_pending_project_control_migration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            lock = {
                "schema_version": 1,
                "project_id": "crm-agent-mvp",
                "mvp_os_version": "1.0.1",
                "release": "v1.0.1",
                "sync_status": "synced",
                "sync_mode": "pull-pr",
                "source_repository": "skoskov/mvp-operating-system",
                "managed_paths": [".agents/skills/mvp-operating-system"],
            }
            (project / "mvp-os.lock").write_text(
                json.dumps(lock) + "\n", encoding="utf-8"
            )
            with redirect_stdout(StringIO()):
                with patch.object(mvp_os_sync, "require_published_source"):
                    result = mvp_os_sync.sync(
                        ROOT,
                        project,
                        Path("mvp-os.lock"),
                        False,
                        "skoskov/crm-agent-mvp",
                        False,
                    )
            self.assertEqual(result, 0)
            updated = json.loads((project / "mvp-os.lock").read_text())
            self.assertEqual(updated["schema_version"], 2)
            self.assertEqual(updated["mvp_os_version"], "2.1.0")
            self.assertEqual(updated["sync_status"], "project-control-migration-required")
            self.assertEqual(updated["project_control"]["status"], "pending")

    def test_sync_refuses_candidate_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "mvp-os.lock").write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "project_id": "crm-agent-mvp",
                        "mvp_os_version": "2.0.0",
                    }
                ) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(SystemExit, "unpublished MVP OS candidate"):
                mvp_os_sync.sync(
                    ROOT,
                    project,
                    Path("mvp-os.lock"),
                    True,
                    "skoskov/crm-agent-mvp",
                    False,
                )

    def test_newest_release_wins_for_repeated_destination(self) -> None:
        releases = [
            {"managed_paths": [{"source": "old", "destination": "target"}]},
            {"managed_paths": [{"source": "new", "destination": "target"}]},
        ]
        self.assertEqual(
            mvp_os_sync.effective_managed_paths(releases),
            [{"source": "new", "destination": "target"}],
        )


if __name__ == "__main__":
    unittest.main()
