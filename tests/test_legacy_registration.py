from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "skill/mvp-operating-system/bin/register_legacy_contracts.py"
)
SPEC = importlib.util.spec_from_file_location("register_legacy_contracts", SCRIPT)
assert SPEC and SPEC.loader
registration = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(registration)


class LegacyRegistrationTests(unittest.TestCase):
    def test_existing_schema_v1_contract_is_registered_before_upgrade(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            shutil.copytree(
                ROOT / "template/mvp-project-template/project-control",
                project / "project-control",
            )
            shutil.copy2(
                ROOT / "template/mvp-project-template/mvp-os.lock",
                project / "mvp-os.lock",
            )
            outputs = project / "outputs"
            outputs.mkdir()
            contract_path = outputs / "legacy-task.json"
            contract_path.write_text(
                json.dumps({
                    "schema_version": 1,
                    "task_id": "legacy-task",
                    "scope": {},
                    "outcome": {},
                    "reuse": {},
                }) + "\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "init", "-q"], cwd=project, check=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=project,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test"],
                cwd=project,
                check=True,
            )
            subprocess.run(["git", "add", "."], cwd=project, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "fixture"], cwd=project, check=True,
            )

            registration.register(project)

            current = json.loads(
                (project / "project-control/CURRENT.json").read_text(encoding="utf-8")
            )
            self.assertEqual(current["release_id"], "000002")
            acceptance = json.loads(
                (
                    project
                    / "project-control/releases/000002/acceptance.json"
                ).read_text(encoding="utf-8")
            )
            expected = "sha256:" + hashlib.sha256(contract_path.read_bytes()).hexdigest()
            self.assertEqual(acceptance["legacy_task_contract_sha256"], [expected])


if __name__ == "__main__":
    unittest.main()
