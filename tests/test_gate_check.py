from __future__ import annotations

import importlib.util
import hashlib
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skill/mvp-operating-system/bin/gate_check.py"
SPEC = importlib.util.spec_from_file_location("gate_check", SCRIPT)
assert SPEC and SPEC.loader
gate_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate_check)


def valid_contract(project_root: Path) -> dict:
    evidence_path = project_root / "outputs/evidence.txt"
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text("verified evidence\n", encoding="utf-8")
    evidence_hash = "sha256:" + hashlib.sha256(evidence_path.read_bytes()).hexdigest()
    evidence_artifact = {"path": "outputs/evidence.txt", "sha256": evidence_hash}
    passed = {"result": "PASS", "artifact": evidence_artifact}
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
                "browser_preflight": passed,
                "target_url": "https://example.test/app",
                "public_url": "https://example.test/app",
                "environment": "public",
                "release_build_id": "release-1",
                "build_artifact": evidence_artifact,
                "screenshots": [
                    {
                        "phase": phase,
                        "viewport": viewport,
                        "path": "outputs/evidence.txt",
                        "sha256": evidence_hash,
                        "inspected": True,
                    }
                    for phase in ("baseline", "final")
                    for viewport in ("desktop", "mobile")
                ],
                "dom_assertions": [{
                    "assertion": "main heading exists", "expected": "one", "observed": "one",
                    "result": "PASS", "artifact": evidence_artifact,
                }],
                "click_navigation_matrix": [{
                    "control": "approve", "action": "click", "expected": "history", "observed": "history",
                    "result": "PASS", "artifact": evidence_artifact,
                }],
                "state_transitions": [{
                    "before": "pending 2", "action": "approve", "after": "pending 1",
                    "result": "PASS", "artifact": evidence_artifact,
                }],
                "ui_states": {
                    key: passed for key in ("empty", "error", "loading")
                },
                "browser_health": {
                    key: passed
                    for key in ("console", "runtime", "network", "overflow", "assets", "mobile_navigation")
                },
                "baseline_final_verdict": passed,
                "public_post_deploy": passed,
                "rollback_command": "./scripts/rollback.sh",
            },
            "integration": {
                "outcomes": [
                    {
                        "state": "platform_accepted",
                        "meaning": gate_check.OUTCOME_MEANINGS["platform_accepted"],
                        "observed_event": "provider returned an accepted response",
                        "artifact": evidence_artifact,
                    }
                ],
                "non_real_modes": [
                    {"mode": "synthetic", "new_external_result": False}
                ],
            },
            "fingerprints": {
                "authoritative_rows": {"before": evidence_hash, "after": evidence_hash, "artifact": evidence_artifact},
                "authorization_ledger": {"before": evidence_hash, "after": evidence_hash, "artifact": evidence_artifact},
            },
            "hermes": {
                "optional": True,
                "authoritative": False,
                "version_config": passed,
                "gateway_lifecycle": passed,
                "channels": passed,
                "cron_jobs": passed,
                "tools_files": passed,
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
            "review": {"implementation": passed, "clean_context": passed},
        },
    }


class GateCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_valid_contract_passes_preflight_and_acceptance(self) -> None:
        contract = valid_contract(self.root)
        gate_check.validate_contract(contract, "preflight", self.root)
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

    def test_web_acceptance_requires_visual_inspection(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["web"]["screenshots"][0]["inspected"] = False
        with self.assertRaisesRegex(gate_check.GateError, "not visually inspected"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_web_acceptance_requires_resolvable_hashed_artifacts(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["web"]["screenshots"][0]["path"] = "outputs/missing.png"
        with self.assertRaisesRegex(gate_check.GateError, "regular file"):
            gate_check.validate_contract(contract, "acceptance", self.root)

    def test_public_acceptance_rejects_local_environment(self) -> None:
        contract = valid_contract(self.root)
        contract["evidence"]["web"]["environment"] = "local"
        with self.assertRaisesRegex(gate_check.GateError, "public environment"):
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
