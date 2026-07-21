from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skill/mvp-operating-system/bin/project_control.py"
SPEC = importlib.util.spec_from_file_location("project_control", SCRIPT)
assert SPEC and SPEC.loader
project_control = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(project_control)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def make_project(
    root: Path,
    *,
    evidence_age_hours: int = 0,
    secret: bool = False,
    secret_in_purpose: bool = False,
    secret_in_ref: bool = False,
    extra_evidence: list[dict] | None = None,
) -> None:
    release = root / "project-control/releases/000001"
    now = datetime.now(timezone.utc) - timedelta(hours=evidence_age_hours)
    files = {
        "goal.json": {"project_id": "demo", "project_version": "1", "objective": "Current goal", "next_safe_step": "Run verify"},
        "decisions.json": {"decisions": [{"id": "ADR-2", "status": "active", "statement": "Hermes active", "source_events": ["event:2"]}]},
        "scope.json": {"included": ["Hermes"], "excluded": ["Twenty"]},
        "architecture.json": {"components": [{"id": "Hermes", "role": "runtime"}]},
        "commands.json": {"commands": [{"id": "verify", "argv": ["python3", "-V"], "side_effect": "read_only", "required": True}]},
        "access.json": {"access": [{"id": "repo", "purpose": "repository access", "required": True, "status": "available", "secret_ref": "secret://demo/repo"}]},
        "runtime-requirements.json": {"capabilities": [{"id": "verify", "required": True, "evidence": [{"id": "ev-1", "result": "proven", "verified_at": now.isoformat(), "ttl_seconds": 3600, "source_commit": "abc", "contract_version": "1"}] + (extra_evidence or [])}]},
        "acceptance.json": {"gates": ["verify passes"]},
    }
    if secret:
        files["access.json"]["access"][0]["token"] = "actual-secret"
    if secret_in_purpose:
        files["access.json"]["access"][0]["purpose"] = "A9f3Kp7Lm2Nx8Qr4Ts6Uv1Wx5Yz0BcDe"
    if secret_in_ref:
        files["access.json"]["access"][0]["secret_ref"] = "secret://demo/ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"
    hashes = {}
    for name, payload in files.items():
        write_json(release / name, payload)
        hashes[name] = sha(release / name)
    manifest = {"schema_version": 2, "release_id": "000001", "project_id": "demo", "created_at": now.isoformat(), "source_commit": "abc", "files": hashes}
    write_json(release / "manifest.json", manifest)
    write_json(root / "project-control/CURRENT.json", {"schema_version": 2, "release_id": "000001", "manifest_sha256": sha(release / "manifest.json"), "activated_at": now.isoformat()})
    write_json(root / "mvp-os.lock", {"project_id": "demo"})
    (root / "DECISIONS.md").write_text("Twenty is active and mandatory.\n", encoding="utf-8")


class ProjectControlTests(unittest.TestCase):
    def test_bootstrap_ignores_legacy_decisions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(project_control.bootstrap(root), 0)
            text = output.getvalue()
            self.assertIn("Hermes active", text)
            self.assertIn("LEGACY_STARTUP_READS: 0", text)
            self.assertNotIn("Twenty is active and mandatory", text)

    def test_stale_evidence_blocks_doctor_not_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root, evidence_age_hours=2)
            project_control.validate_bundle(root)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(project_control.doctor(root), 2)

    def test_secret_value_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root, secret=True)
            with self.assertRaises(project_control.ControlError):
                project_control.validate_bundle(root)

    def test_token_like_value_in_free_text_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root, secret_in_purpose=True)
            with self.assertRaises(project_control.ControlError):
                project_control.validate_bundle(root)

    def test_secret_ref_must_be_logical_identifier(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root, secret_in_ref=True)
            with self.assertRaises(project_control.ControlError):
                project_control.validate_bundle(root)

    def test_secret_value_in_command_argv_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            commands_path = root / "project-control/releases/000001/commands.json"
            commands = json.loads(commands_path.read_text())
            commands["commands"][0]["argv"].append("A9f3Kp7Lm2Nx8Qr4Ts6Uv1Wx5Yz0BcDe")
            write_json(commands_path, commands)
            manifest_path = root / "project-control/releases/000001/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["files"]["commands.json"] = sha(commands_path)
            write_json(manifest_path, manifest)
            current_path = root / "project-control/CURRENT.json"
            current = json.loads(current_path.read_text())
            current["manifest_sha256"] = sha(manifest_path)
            write_json(current_path, current)
            with self.assertRaises(project_control.ControlError):
                project_control.validate_bundle(root)

    def test_secret_value_in_source_events_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            decisions_path = root / "project-control/releases/000001/decisions.json"
            decisions = json.loads(decisions_path.read_text())
            decisions["decisions"][0]["source_events"] = [
                "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"
            ]
            write_json(decisions_path, decisions)
            manifest_path = root / "project-control/releases/000001/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["files"]["decisions.json"] = sha(decisions_path)
            write_json(manifest_path, manifest)
            current_path = root / "project-control/CURRENT.json"
            current = json.loads(current_path.read_text())
            current["manifest_sha256"] = sha(manifest_path)
            write_json(current_path, current)
            with self.assertRaises(project_control.ControlError):
                project_control.validate_bundle(root)

    def test_source_event_catalog_makes_decisions_traceable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            trace_path = root / "trace/event-2.md"
            trace_path.parent.mkdir(parents=True)
            trace_path.write_text("source event two\n", encoding="utf-8")
            decisions_path = root / "project-control/releases/000001/decisions.json"
            decisions = json.loads(decisions_path.read_text())
            captured_content = "source event two"
            decisions["source_event_catalog_version"] = 3
            decisions["source_event_catalog"] = {
                "event:2": {
                    "reference": "trace/event-2.md",
                    "reference_type": "local_file",
                    "captured_at": datetime.now(timezone.utc).isoformat(),
                    "captured_content": captured_content,
                    "content_sha256": "sha256:" + hashlib.sha256(captured_content.encode()).hexdigest(),
                    "reference_content_sha256": sha(trace_path),
                }
            }
            write_json(decisions_path, decisions)
            manifest_path = root / "project-control/releases/000001/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["files"]["decisions.json"] = sha(decisions_path)
            write_json(manifest_path, manifest)
            current_path = root / "project-control/CURRENT.json"
            current = json.loads(current_path.read_text())
            current["manifest_sha256"] = sha(manifest_path)
            write_json(current_path, current)
            project_control.validate_bundle(root)

            decisions["source_event_catalog"]["event:2"]["captured_content"] = "tampered"
            write_json(decisions_path, decisions)
            manifest["files"]["decisions.json"] = sha(decisions_path)
            write_json(manifest_path, manifest)
            current["manifest_sha256"] = sha(manifest_path)
            write_json(current_path, current)
            with self.assertRaisesRegex(project_control.ControlError, "captured content hash mismatch"):
                project_control.validate_bundle(root)

            decisions["source_event_catalog"]["event:2"]["captured_content"] = captured_content
            decisions["source_event_catalog"]["event:2"]["reference_content_sha256"] = "sha256:" + "1" * 64
            write_json(decisions_path, decisions)
            manifest["files"]["decisions.json"] = sha(decisions_path)
            write_json(manifest_path, manifest)
            current["manifest_sha256"] = sha(manifest_path)
            write_json(current_path, current)
            with self.assertRaisesRegex(project_control.ControlError, "content hash mismatch"):
                project_control.validate_bundle(root)

            decisions["source_event_catalog"]["event:2"]["reference_content_sha256"] = sha(trace_path)
            decisions["decisions"][0]["source_events"] = ["event:missing"]
            write_json(decisions_path, decisions)
            manifest["files"]["decisions.json"] = sha(decisions_path)
            write_json(manifest_path, manifest)
            current["manifest_sha256"] = sha(manifest_path)
            write_json(current_path, current)
            with self.assertRaisesRegex(project_control.ControlError, "not traceable"):
                project_control.validate_bundle(root)

    def test_external_source_event_requires_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            decisions_path = root / "project-control/releases/000001/decisions.json"
            decisions = json.loads(decisions_path.read_text())
            decisions["source_event_catalog_version"] = 1
            decisions["source_event_catalog"] = {
                "event:2": {
                    "reference": "https://github.com/example/context/blob/" + "a" * 40 + "/event.md",
                    "reference_type": "immutable_external",
                    "captured_at": datetime.now(timezone.utc).isoformat(),
                    "content_sha256": "sha256:" + "2" * 64,
                }
            }
            write_json(decisions_path, decisions)
            manifest_path = root / "project-control/releases/000001/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["files"]["decisions.json"] = sha(decisions_path)
            write_json(manifest_path, manifest)
            current_path = root / "project-control/CURRENT.json"
            current = json.loads(current_path.read_text())
            current["manifest_sha256"] = sha(manifest_path)
            write_json(current_path, current)
            with self.assertRaisesRegex(project_control.ControlError, "lacks external resolution"):
                project_control.validate_bundle(root)

    def test_secret_value_in_manifest_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            manifest_path = root / "project-control/releases/000001/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["source_commit"] = "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"
            write_json(manifest_path, manifest)
            current_path = root / "project-control/CURRENT.json"
            current = json.loads(current_path.read_text())
            current["manifest_sha256"] = sha(manifest_path)
            write_json(current_path, current)
            with self.assertRaises(project_control.ControlError):
                project_control.validate_bundle(root)

    def test_symlinked_release_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            goal_path = root / "project-control/releases/000001/goal.json"
            outside = root / "outside-goal.json"
            outside.write_bytes(goal_path.read_bytes())
            goal_path.unlink()
            try:
                goal_path.symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"symlink unavailable: {exc}")
            with self.assertRaises(project_control.ControlError):
                project_control.validate_bundle(root)

    def test_manifest_and_lock_project_ids_must_match_goal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            manifest_path = root / "project-control/releases/000001/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["project_id"] = "other-project"
            write_json(manifest_path, manifest)
            current_path = root / "project-control/CURRENT.json"
            current = json.loads(current_path.read_text())
            current["manifest_sha256"] = sha(manifest_path)
            write_json(current_path, current)
            with self.assertRaisesRegex(
                project_control.ControlError, "manifest project_id"
            ):
                project_control.validate_bundle(root)

            make_project(root)
            write_json(root / "mvp-os.lock", {"project_id": "other-project"})
            with self.assertRaisesRegex(
                project_control.ControlError, "mvp-os.lock project_id"
            ):
                project_control.validate_bundle(root)

    def test_current_hash_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            current = json.loads((root / "project-control/CURRENT.json").read_text())
            current["manifest_sha256"] = "sha256:" + "0" * 64
            write_json(root / "project-control/CURRENT.json", current)
            with self.assertRaises(project_control.ControlError):
                project_control.validate_bundle(root)

    def test_publish_advances_current_without_changing_old_release(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            old_manifest = (root / "project-control/releases/000001/manifest.json").read_bytes()
            new_release = root / "project-control/releases/000002"
            new_release.mkdir(parents=True)
            for name in project_control.REQUIRED_FILES:
                (new_release / name).write_bytes(
                    (root / "project-control/releases/000001" / name).read_bytes()
                )
            timestamp = datetime.now(timezone.utc).isoformat()
            with redirect_stdout(io.StringIO()):
                self.assertEqual(project_control.publish(root, "000002", "def", timestamp), 0)
            current = json.loads((root / "project-control/CURRENT.json").read_text())
            manifest = json.loads((new_release / "manifest.json").read_text())
            self.assertEqual(current["release_id"], "000002")
            self.assertEqual(manifest["parent_release"], "000001")
            self.assertEqual(
                old_manifest,
                (root / "project-control/releases/000001/manifest.json").read_bytes(),
            )

    def test_failed_publish_preserves_current_and_removes_candidate_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_project(root)
            old_current = (root / "project-control/CURRENT.json").read_bytes()
            new_release = root / "project-control/releases/000002"
            new_release.mkdir(parents=True)
            for name in project_control.REQUIRED_FILES:
                (new_release / name).write_bytes(
                    (root / "project-control/releases/000001" / name).read_bytes()
                )
            decisions = json.loads((new_release / "decisions.json").read_text())
            decisions["decisions"][0]["status"] = "superseded"
            write_json(new_release / "decisions.json", decisions)
            with self.assertRaises(project_control.ControlError):
                project_control.publish(
                    root, "000002", "def", datetime.now(timezone.utc).isoformat()
                )
            self.assertEqual(old_current, (root / "project-control/CURRENT.json").read_bytes())
            self.assertFalse((new_release / "manifest.json").exists())

    def test_newer_failed_evidence_blocks_doctor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            failed_at = (datetime.now(timezone.utc) + timedelta(seconds=1)).isoformat()
            make_project(
                root,
                extra_evidence=[
                    {"id": "ev-2", "result": "failed", "verified_at": failed_at, "ttl_seconds": 3600, "source_commit": "def", "contract_version": "1"}
                ],
            )
            with redirect_stdout(io.StringIO()):
                self.assertEqual(project_control.doctor(root), 2)

    def test_initialize_rekeys_untouched_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "new-project"
            shutil.copytree(ROOT / "template/mvp-project-template", root)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(project_control.initialize(root, "new-project"), 0)
            _, _, bundle = project_control.validate_bundle(root)
            lock = json.loads((root / "mvp-os.lock").read_text())
            self.assertEqual(bundle["goal.json"]["project_id"], "new-project")
            self.assertEqual(lock["project_id"], "new-project")
            self.assertEqual(lock["project_control"]["status"], "pending-review")


if __name__ == "__main__":
    unittest.main()
