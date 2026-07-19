from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/mvp_os_sync.py"
SPEC = importlib.util.spec_from_file_location("mvp_os_sync", SCRIPT)
assert SPEC and SPEC.loader
mvp_os_sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mvp_os_sync)


class SyncV2Tests(unittest.TestCase):
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
            self.assertEqual(updated["mvp_os_version"], "2.0.0")
            self.assertEqual(updated["sync_status"], "project-control-migration-required")
            self.assertEqual(updated["project_control"]["status"], "pending")

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
