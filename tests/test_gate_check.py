from __future__ import annotations

import importlib.util
import hashlib
import tempfile
import unittest
import json
import struct
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skill/mvp-operating-system/bin/gate_check.py"
SPEC = importlib.util.spec_from_file_location("gate_check", SCRIPT)
assert SPEC and SPEC.loader
gate_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate_check)


def json_artifact(
    project_root: Path,
    evidence_type: str,
    *,
    build_id: str | None = None,
    details: dict | None = None,
    name: str | None = None,
    task_id: str = "web-integration-proof",
) -> dict:
    relative = Path("outputs") / f"{name or evidence_type}.json"
    path = project_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "evidence_type": evidence_type,
        "task_id": task_id,
        "result": "PASS",
        "details": details or {"observed": f"verified {evidence_type}"},
    }
    if build_id is not None:
        payload["release_build_id"] = build_id
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "path": str(relative),
        "sha256": "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def screenshot_artifact(project_root: Path, name: str) -> dict:
    relative = Path("outputs") / f"{name}.png"
    path = project_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    def chunk(kind: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + kind
            + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        )

    color = hashlib.sha256(name.encode("utf-8")).digest()[:3] + b"\xff"
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(b"\x00" + color))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(png)
    return {
        "path": str(relative),
        "sha256": "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def valid_contract(project_root: Path) -> dict:
    build_id = "release-1"
    return {
        "schema_version": 1,
        "task_id": "web-integration-proof",
        "scope": {
            "web": True,
            "public_deploy": True,
            "integration": True,
            "hermes": True,
            "stateful": True,
        },
        "scope_rationale": {
            key: f"The test explicitly enables {key}."
            for key in ("web", "public_deploy", "integration", "hermes", "stateful")
        },
        "outcome": {
            "observable_result": "A user action produces a truthful public result.",
            "acceptance_criteria": ["The complete chain is independently verified."],
            "realistic_data": "Versioned synthetic input and observed platform evidence.",
            "external_result": "The platform accepts the bounded test action.",
            "cost_scale_contract": "One source fetch and at most two connector calls.",
            "time_budget": "Stop after four hours.",
            "stop_condition": "Stop on the first uncertain external result.",
            "forbidden_simplifications": ["No mock may replace the public flow."],
            "rollback": "Run the versioned rollback command.",
            "chain": {
                "external_signal": "A versioned input is observed.",
                "interpretation": "The input is normalized.",
                "decision_policy": "Policy accepts the bounded action.",
                "action": "A durable intent is dispatched.",
                "external_result": "The platform response is observed.",
                "product_display": "The UI shows the truthful state.",
                "independent_verification": "An independent browser review passes.",
            },
        },
        "reuse": {
            "discovery": [
                {"kind": kind, "status": "rejected", "rationale": f"Reviewed {kind}."}
                for kind in gate_check.REUSE_ORDER
            ],
            "custom_code": True,
            "custom_code_reason": "No reviewed option covers the bounded product contract.",
        },
        "evidence": {
            "web": {
                "browser_preflight": {
                    "result": "PASS",
                    "artifact": json_artifact(
                        project_root, "browser_preflight", build_id=build_id,
                        details={"target_url": "https://example.test/app", "environment": "public"},
                    ),
                },
                "target_url": "https://example.test/app",
                "public_url": "https://example.test/app",
                "environment": "public",
                "release_build_id": build_id,
                "build_artifact": json_artifact(
                    project_root, "build_manifest", build_id=build_id,
                    details={"target_url": "https://example.test/app", "environment": "public"},
                ),
                "screenshots": [
                    {
                        "phase": phase,
                        "viewport": viewport,
                        **screenshot_artifact(project_root, f"{phase}-{viewport}"),
                        "capture_artifact": json_artifact(
                            project_root, "screenshot_capture", build_id=build_id,
                            details={
                                "phase": phase,
                                "viewport": viewport,
                                "target_url": "https://example.test/app",
                                "image_sha256": screenshot_artifact(
                                    project_root, f"{phase}-{viewport}"
                                )["sha256"],
                            },
                            name=f"screenshot_capture_{phase}_{viewport}",
                        ),
                        "inspected": True,
                    }
                    for phase in ("baseline", "final")
                    for viewport in ("desktop", "mobile")
                ],
                "dom_assertions": [{
                    "assertion": "main heading exists", "expected": "one", "observed": "one",
                    "result": "PASS",
                    "artifact": json_artifact(
                        project_root, "dom_assertion", build_id=build_id,
                        details={"assertion": "main heading exists", "expected": "one", "observed": "one"},
                    ),
                }],
                "click_navigation_matrix": [{
                    "control": "approve", "action": "click", "expected": "history", "observed": "history",
                    "result": "PASS",
                    "artifact": json_artifact(
                        project_root, "click_navigation", build_id=build_id,
                        details={"control": "approve", "action": "click", "expected": "history", "observed": "history"},
                    ),
                }],
                "state_transitions": [{
                    "before": "pending 2", "action": "approve",
                    "expected_after": "pending 1", "observed_after": "pending 1",
                    "result": "PASS",
                    "artifact": json_artifact(
                        project_root, "state_transition", build_id=build_id,
                        details={
                            "before": "pending 2", "action": "approve",
                            "expected_after": "pending 1", "observed_after": "pending 1",
                        },
                    ),
                }],
                "ui_states": {
                    key: {
                        "result": "PASS",
                        "artifact": json_artifact(
                            project_root, f"ui_state_{key}", build_id=build_id,
                            details={"state": key, "target_url": "https://example.test/app"},
                        ),
                    }
                    for key in ("empty", "error", "loading")
                },
                "browser_health": {
                    key: {
                        "result": "PASS",
                        "artifact": json_artifact(
                            project_root, f"browser_health_{key}", build_id=build_id,
                            details={"check": key, "target_url": "https://example.test/app"},
                        ),
                    }
                    for key in ("console", "runtime", "network", "overflow", "assets", "mobile_navigation")
                },
                "baseline_final_verdict": {
                    "result": "PASS",
                    "artifact": json_artifact(
                        project_root, "baseline_final_verdict", build_id=build_id,
                        details={"target_url": "https://example.test/app", "verdict": "no_regression"},
                    ),
                },
                "public_post_deploy": {
                    "result": "PASS",
                    "artifact": json_artifact(
                        project_root, "public_post_deploy", build_id=build_id,
                        details={"public_url": "https://example.test/app", "verified": True},
                    ),
                },
                "rollback_command": "./scripts/rollback.sh",
            },
            "integration": {
                "outcomes": [
                    {
                        "state": "platform_accepted",
                        "meaning": gate_check.OUTCOME_MEANINGS["platform_accepted"],
                        "event_type": "platform_acceptance_response",
                        "observed_event": "provider returned an accepted response",
                        "observed_event_id": "sha256:" + "c" * 64,
                        "artifact": json_artifact(
                            project_root, "integration_outcome",
                            details={
                                "state": "platform_accepted",
                                "meaning": gate_check.OUTCOME_MEANINGS["platform_accepted"],
                                "event_type": "platform_acceptance_response",
                                "observed_event": "provider returned an accepted response",
                                "observed_event_id": "sha256:" + "c" * 64,
                            },
                        ),
                    }
                ],
                "non_real_modes": [
                    {"mode": "synthetic", "new_external_result": False}
                ],
            },
            "fingerprints": {
                "authoritative_rows": {
                    "before": "sha256:" + "a" * 64,
                    "after": "sha256:" + "a" * 64,
                    "artifact": json_artifact(
                        project_root, "fingerprint_authoritative_rows",
                        details={"before": "sha256:" + "a" * 64, "after": "sha256:" + "a" * 64},
                    ),
                },
                "authorization_ledger": {
                    "before": "sha256:" + "b" * 64,
                    "after": "sha256:" + "b" * 64,
                    "artifact": json_artifact(
                        project_root, "fingerprint_authorization_ledger",
                        details={"before": "sha256:" + "b" * 64, "after": "sha256:" + "b" * 64},
                    ),
                },
            },
            "hermes": {
                "optional": True,
                "authoritative": False,
                "version_config": {
                    "result": "PASS", "artifact": json_artifact(
                        project_root, "hermes_version_config",
                        details={"capability": "version_config", "verified": True},
                    )
                },
                "gateway_lifecycle": {
                    "result": "PASS", "artifact": json_artifact(
                        project_root, "hermes_gateway_lifecycle",
                        details={"capability": "gateway_lifecycle", "verified": True},
                    )
                },
                "channels": {
                    "result": "PASS", "artifact": json_artifact(
                        project_root, "hermes_channels",
                        details={"capability": "channels", "verified": True},
                    )
                },
                "cron_jobs": {
                    "result": "PASS", "artifact": json_artifact(
                        project_root, "hermes_cron_jobs",
                        details={"capability": "cron_jobs", "verified": True},
                    )
                },
                "tools_files": {
                    "result": "PASS", "artifact": json_artifact(
                        project_root, "hermes_tools_files",
                        details={"capability": "tools_files", "verified": True},
                    )
                },
                "llm_routing": "direct_model",
                "restart": {"service_notifications": "silent"},
                "send_capability": {
                    "enabled": True,
                    "intent_ids": ["intent-1"],
                    "allowed_channels": ["telegram"],
                    "max_calls": 1,
                    "authorization_ledger": "auth-ledger-v1",
                    "automatic_retry_after_uncertain": False,
                },
            },
            "review": {
                "implementation": {
                    "result": "PASS", "reviewer": "independent-reviewer",
                    "head": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "summary": "Implementation review passed.", "findings": [],
                    "artifact": json_artifact(
                        project_root, "implementation_review",
                        details={
                            "reviewer": "independent-reviewer", "head": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            "summary": "Implementation review passed.", "findings": [],
                        },
                    ),
                },
                "clean_context": {
                    "result": "PASS", "reviewer": "clean-context-reviewer",
                    "head": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "summary": "Clean-context review passed.", "findings": [],
                    "artifact": json_artifact(
                        project_root, "clean_context_review",
                        details={
                            "reviewer": "clean-context-reviewer", "head": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            "summary": "Clean-context review passed.", "findings": [],
                        },
                    ),
                },
            },
        },
    }


def short_contract(project_root: Path) -> dict:
    checks = {key: True for key in gate_check.REVIEW_CHECKS}
    review_details = {
        "reviewer": "independent-classification-reviewer",
        "summary": "Short mode and planned evidence are justified.",
        "findings": [],
        "checks": checks,
    }
    return {
        "schema_version": 2,
        "task_id": "local-bugfix",
        "gate_mode": "short",
        "work_type": "bugfix",
        "gate_mode_rationale": "A bounded local bugfix changes no external or user-facing flow.",
        "classification": {
            "planned_paths": ["validator.py", "tests/test_validator.py"],
            "behavior_change": "internal",
            "public_api_change": False,
            "data_contract_change": False,
            "dependency_change": False,
        },
        "scope": {
            "web": False,
            "public_deploy": False,
            "integration": False,
            "hermes": False,
            "stateful": False,
        },
        "scope_rationale": {
            key: f"The local bugfix does not use {key}."
            for key in ("web", "public_deploy", "integration", "hermes", "stateful")
        },
        "outcome": {
            "beneficiary": "Maintainers running the validator.",
            "result_owner": "The module owner.",
            "observable_result": "The regression test passes without changing public behavior.",
            "acceptance_criteria": ["The focused regression test passes."],
            "non_goals": ["No feature or integration behavior changes."],
            "minimum_proof": "One failing-before and passing-after regression test.",
            "time_budget": "One bounded implementation slice.",
            "stop_condition": "Stop if public behavior or conditional scope changes.",
            "rollback": "Revert the bounded patch.",
        },
        "reuse": {
            "discovery": [{
                "kind": "existing_project",
                "status": "reused",
                "rationale": "Reuse the existing module and test harness.",
                "remaining_gap": "The regression still requires a local code fix.",
            }],
            "custom_code": True,
            "custom_code_reason": "The defect is in the existing local implementation.",
        },
        "preflight_review": {
            "result": "PASS",
            **review_details,
            "artifact": json_artifact(
                project_root,
                "preflight_review",
                details=review_details,
                task_id="local-bugfix",
            ),
        },
        "evidence": {},
    }


def explicit_full_contract(project_root: Path) -> dict:
    contract = valid_contract(project_root)
    contract.update({
        "schema_version": 2,
        "gate_mode": "full",
        "work_type": "feature",
        "gate_mode_rationale": "The feature changes an observable end-to-end product flow.",
        "classification": {
            "planned_paths": ["app/flow.py", "tests/test_flow.py"],
            "behavior_change": "user_visible",
            "public_api_change": False,
            "data_contract_change": False,
            "dependency_change": False,
        },
    })
    contract["outcome"].update({
        "beneficiary": "A user completing the public flow.",
        "result_owner": "The product owner.",
        "non_goals": ["No unrelated channel or workflow expansion."],
        "minimum_proof": "Independent evidence verifies the complete public flow.",
    })
    contract["reuse"]["discovery"] = [
        {
            "kind": kind,
            "status": "rejected",
            "rationale": f"Reviewed {kind} against the required outcome.",
            "evaluation": {
                "maintenance": "Actively assessed.",
                "license": "Compatible or not applicable.",
                "security": "No unresolved blocker.",
                "lock_in": "Acceptable for the bounded scope.",
                "integration_cost": "Compared with the local extension.",
            },
        }
        for kind in gate_check.FULL_REUSE_ORDER
    ]
    checks = {key: True for key in gate_check.FULL_REVIEW_CHECKS}
    preflight_details = {
        "reviewer": "independent-classification-reviewer",
        "summary": "Full mode, product outcome, reuse, and evidence plan are justified.",
        "findings": [],
        "checks": checks.copy(),
    }
    contract["preflight_review"] = {
        "result": "PASS",
        **preflight_details,
        "artifact": json_artifact(
            project_root, "preflight_review", details=preflight_details,
        ),
    }
    for key, evidence_type in (
        ("implementation", "implementation_review"),
        ("clean_context", "clean_context_review"),
    ):
        review = contract["evidence"]["review"][key]
        review["checks"] = checks.copy()
        review["artifact"] = json_artifact(
            project_root,
            evidence_type,
            details={
                "reviewer": review["reviewer"],
                "head": review["head"],
                "summary": review["summary"],
                "findings": review["findings"],
                "checks": review["checks"],
            },
        )
    return contract


def short_acceptance_contract(project_root: Path) -> dict:
    contract = short_contract(project_root)
    checks = {key: True for key in gate_check.REVIEW_CHECKS}
    contract["evidence"]["review"] = {}
    for key, evidence_type in (
        ("implementation", "implementation_review"),
        ("clean_context", "clean_context_review"),
    ):
        details = {
            "reviewer": f"independent-{key}-reviewer",
            "head": "a" * 40,
            "summary": f"{key} review passed.",
            "findings": [],
            "checks": checks.copy(),
        }
        contract["evidence"]["review"][key] = {
            "result": "PASS",
            **details,
            "artifact": json_artifact(
                project_root, evidence_type, details=details,
                task_id="local-bugfix",
            ),
        }
    return contract


class GateCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        release = self.root / "project-control/releases/000001"
        release.mkdir(parents=True)
        (self.root / "project-control/CURRENT.json").write_text(
            json.dumps({"release_id": "000001"}) + "\n", encoding="utf-8"
        )
        (release / "manifest.json").write_text(
            json.dumps({"source_commit": "a" * 40}) + "\n", encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_valid_contract_passes_preflight_and_acceptance(self) -> None:
        contract = valid_contract(self.root)
        gate_check.validate_contract(contract, "preflight", self.root)
        gate_check.validate_contract(contract, "acceptance", self.root)

    def test_short_mode_passes_for_bounded_local_bugfix(self) -> None:
        gate_check.validate_contract(short_contract(self.root), "preflight", self.root)

    def test_short_mode_rejects_feature_work(self) -> None:
        contract = short_contract(self.root)
        contract["work_type"] = "feature"
        with self.assertRaisesRegex(gate_check.GateError, "short gate_mode"):
            gate_check.validate_contract(contract, "preflight", self.root)

    def test_short_mode_rejects_conditional_scope(self) -> None:
        contract = short_contract(self.root)
        contract["scope"]["web"] = True
        with self.assertRaisesRegex(gate_check.GateError, "every conditional scope"):
            gate_check.validate_contract(contract, "preflight", self.root)

    def test_schema_v2_cannot_omit_gate_mode(self) -> None:
        contract = short_contract(self.root)
        del contract["gate_mode"]
        with self.assertRaisesRegex(gate_check.GateError, "requires gate_mode"):
            gate_check.validate_contract(contract, "preflight", self.root)

    def test_schema_v1_remains_legacy_and_rejects_new_mode_fields(self) -> None:
        contract = valid_contract(self.root)
        contract["gate_mode"] = "full"
        with self.assertRaisesRegex(gate_check.GateError, "schema_version 1 is legacy"):
            gate_check.validate_contract(contract, "preflight", self.root)

    def test_short_mode_rejects_user_visible_behavior(self) -> None:
        contract = short_contract(self.root)
        contract["classification"]["behavior_change"] = "user_visible"
        with self.assertRaisesRegex(gate_check.GateError, "user-visible"):
            gate_check.validate_contract(contract, "preflight", self.root)

    def test_short_mode_rejects_public_api_change(self) -> None:
        contract = short_contract(self.root)
        contract["classification"]["public_api_change"] = True
        with self.assertRaisesRegex(gate_check.GateError, "public_api_change"):
            gate_check.validate_contract(contract, "preflight", self.root)

    def test_short_mode_acceptance_requires_and_passes_classification_review(self) -> None:
        contract = short_acceptance_contract(self.root)
        gate_check.validate_contract(contract, "acceptance", self.root)
        contract["evidence"]["review"]["implementation"]["checks"]["gate_classification"] = False
        with self.assertRaisesRegex(gate_check.GateError, "gate_classification"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_preflight_review_must_confirm_gate_classification(self) -> None:
        contract = short_contract(self.root)
        contract["preflight_review"]["checks"]["gate_classification"] = False
        with self.assertRaisesRegex(gate_check.GateError, "gate_classification"):
            gate_check.validate_contract(contract, "preflight", self.root)

    def test_custom_code_rejects_not_applicable_reuse_candidates(self) -> None:
        contract = explicit_full_contract(self.root)
        for candidate in contract["reuse"]["discovery"]:
            candidate["status"] = "not_applicable"
        with self.assertRaisesRegex(gate_check.GateError, "reused or rejected"):
            gate_check.validate_contract(contract, "preflight", self.root)

    def test_full_mode_passes_with_structured_outcome_reuse_and_review(self) -> None:
        contract = explicit_full_contract(self.root)
        gate_check.validate_contract(contract, "preflight", self.root)
        gate_check.validate_contract(contract, "acceptance", self.root)

    def test_full_mode_requires_reuse_risk_evaluation(self) -> None:
        contract = explicit_full_contract(self.root)
        del contract["reuse"]["discovery"][0]["evaluation"]["security"]
        with self.assertRaisesRegex(gate_check.GateError, "evaluation.security"):
            gate_check.validate_contract(contract, "preflight", self.root)

    def test_full_mode_acceptance_requires_explicit_review_checks(self) -> None:
        contract = explicit_full_contract(self.root)
        contract["evidence"]["review"]["implementation"]["checks"]["cost_scale"] = False
        with self.assertRaisesRegex(gate_check.GateError, "checks.cost_scale"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_preflight_requires_complete_outcome_chain(self) -> None:
        contract = valid_contract(self.root)
        del contract["outcome"]["chain"]["external_result"]
        with self.assertRaisesRegex(gate_check.GateError, "canonical ordered"):
            gate_check.validate_contract(contract, "preflight", self.root)

    def test_preflight_requires_reuse_search_order(self) -> None:
        contract = valid_contract(self.root)
        contract["reuse"]["discovery"].reverse()
        with self.assertRaisesRegex(gate_check.GateError, "canonical search order"):
            gate_check.validate_contract(contract, "preflight", self.root)

    def test_stock_template_placeholders_fail_preflight(self) -> None:
        template = gate_check.load_contract(
            ROOT / "skill/mvp-operating-system/assets/task-contract-template.json"
        )
        with self.assertRaisesRegex(gate_check.GateError, "task_id"):
            gate_check.validate_contract(template, "preflight", ROOT)

    def test_stock_short_template_placeholders_fail_preflight(self) -> None:
        template = gate_check.load_contract(
            ROOT / "skill/mvp-operating-system/assets/task-contract-short-template.json"
        )
        with self.assertRaisesRegex(gate_check.GateError, "task_id"):
            gate_check.validate_contract(template, "preflight", ROOT)

    def test_web_acceptance_requires_visual_inspection(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["web"]["screenshots"][0]["inspected"] = False
        with self.assertRaisesRegex(gate_check.GateError, "not visually inspected"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_web_acceptance_requires_resolvable_hashed_artifacts(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["web"]["screenshots"][0]["path"] = "outputs/missing.png"
        with self.assertRaisesRegex(gate_check.GateError, "missing"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_web_acceptance_rejects_wrong_artifact_type(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["web"]["browser_preflight"]["artifact"] = json_artifact(
            self.root, "integration_outcome", build_id="release-1"
        )
        with self.assertRaisesRegex(gate_check.GateError, "evidence_type"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_web_acceptance_rejects_contradictory_observation(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["web"]["dom_assertions"][0]["observed"] = "zero"
        with self.assertRaisesRegex(gate_check.GateError, "expected and observed"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_integration_artifact_must_match_observed_claim(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["integration"]["outcomes"][0]["observed_event"] = "different response"
        with self.assertRaisesRegex(gate_check.GateError, "do not match"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_screenshot_requires_complete_png_structure(self) -> None:
        contract = valid_contract(self.root)
        shot = contract["evidence"]["web"]["screenshots"][0]
        path = self.root / shot["path"]
        path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"not-an-image" * 4)
        shot["sha256"] = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        with self.assertRaisesRegex(gate_check.GateError, "PNG"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_artifact_rejects_intermediate_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as outside_tmp:
            outside = Path(outside_tmp)
            outside_file = outside / "evidence.json"
            outside_file.write_text("{}\n", encoding="utf-8")
            link = self.root / "linked"
            try:
                link.symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"symlink unavailable: {exc}")
            value = {
                "path": "linked/evidence.json",
                "sha256": "sha256:" + hashlib.sha256(outside_file.read_bytes()).hexdigest(),
            }
            with self.assertRaisesRegex(gate_check.GateError, "symlink"):
                gate_check.artifact(
                    value, self.root, "artifact", "implementation_review",
                    "web-integration-proof",
                )

    def test_public_acceptance_rejects_local_environment(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["web"]["environment"] = "local"
        with self.assertRaisesRegex(gate_check.GateError, "do not match|public environment"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_web_acceptance_requires_state_transitions(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["web"]["state_transitions"] = []
        with self.assertRaisesRegex(gate_check.GateError, "state_transitions"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_stateful_acceptance_rejects_changed_fingerprint(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["fingerprints"]["authorization_ledger"]["after"] = "sha256:changed"
        with self.assertRaisesRegex(gate_check.GateError, "authorization_ledger changed"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_platform_acceptance_cannot_overclaim_delivery(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["integration"]["outcomes"][0]["meaning"] = "recipient received and read it"
        with self.assertRaisesRegex(gate_check.GateError, "overclaims"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_non_real_mode_cannot_claim_external_result(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["integration"]["non_real_modes"][0]["new_external_result"] = True
        with self.assertRaisesRegex(gate_check.GateError, "cannot claim"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_hermes_must_remain_optional_and_non_authoritative(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["hermes"]["optional"] = False
        with self.assertRaisesRegex(gate_check.GateError, "remain optional"):
            gate_check.validate_contract(contract, "acceptance", self.root)
        contract = valid_contract(self.root)
        contract["evidence"]["hermes"]["authoritative"] = True
        with self.assertRaisesRegex(gate_check.GateError, "authoritative"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_hermes_uncertain_result_cannot_auto_retry(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["hermes"]["send_capability"]["automatic_retry_after_uncertain"] = True
        with self.assertRaisesRegex(gate_check.GateError, "automatically retry"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_acceptance_requires_independent_reviews(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["review"]["clean_context"] = {
            "result": "NOT_APPLICABLE", "rationale": "not reviewed"
        }
        with self.assertRaisesRegex(gate_check.GateError, "clean_context"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_acceptance_rejects_unresolved_review_findings(self) -> None:
        contract = valid_contract(self.root)
        review = contract["evidence"]["review"]["implementation"]
        review["findings"] = [{"priority": "P0", "status": "unresolved"}]
        review["artifact"] = json_artifact(
            self.root, "implementation_review",
            details={
                "reviewer": review["reviewer"], "head": review["head"],
                "summary": review["summary"], "findings": review["findings"],
            },
        )
        with self.assertRaisesRegex(gate_check.GateError, "findings must be empty"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_acceptance_binds_reviews_to_release_source_commit(self) -> None:
        contract = valid_contract(self.root)
        review = contract["evidence"]["review"]["implementation"]
        review["head"] = "b" * 40
        review["artifact"] = json_artifact(
            self.root, "implementation_review",
            details={
                "reviewer": review["reviewer"], "head": review["head"],
                "summary": review["summary"], "findings": [],
            },
        )
        with self.assertRaisesRegex(gate_check.GateError, "source_commit"):
            gate_check.validate_contract(contract, "acceptance", self.root)


class DistributionConsistencyTests(unittest.TestCase):
    def test_template_skill_matches_canonical_skill(self) -> None:
        source = ROOT / "skill/mvp-operating-system"
        template = ROOT / "template/mvp-project-template/.agents/skills/mvp-operating-system"
        source_files = {path.relative_to(source) for path in source.rglob("*") if path.is_file()}
        template_files = {path.relative_to(template) for path in template.rglob("*") if path.is_file()}
        self.assertEqual(source_files, template_files)
        for relative in source_files:
            self.assertEqual((source / relative).read_bytes(), (template / relative).read_bytes(), str(relative))


if __name__ == "__main__":
    unittest.main()
