#!/usr/bin/env python3
"""Validate MVP OS v2.1 task contracts and acceptance evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import zlib
from pathlib import Path
from typing import Any


CHAIN = [
    "external_signal",
    "interpretation",
    "decision_policy",
    "action",
    "external_result",
    "product_display",
    "independent_verification",
]
REUSE_ORDER = [
    "existing_project",
    "official_api_sdk_connector",
    "supported_github_project",
    "mcp_server",
    "library",
    "service_api",
]
OUTCOME_MEANINGS = {
    "intent_created": "durable intent exists; no connector invocation claimed",
    "dispatched": "connector invocation started; no platform acceptance claimed",
    "platform_accepted": "platform accepted the request; recipient delivery, reading, or reply is not claimed",
    "delivery_confirmed": "channel-specific evidence confirms delivery",
    "recipient_read": "a separate observable event confirms recipient read",
    "recipient_replied": "a separate observable event confirms recipient reply",
    "failed_definitive": "a definitive failure was observed",
    "failed_uncertain": "the result is uncertain and must not be retried automatically",
}
OUTCOME_EVENT_TYPES = {
    "intent_created": "durable_intent_record",
    "dispatched": "connector_invocation_started",
    "platform_accepted": "platform_acceptance_response",
    "delivery_confirmed": "channel_delivery_confirmation",
    "recipient_read": "recipient_read_event",
    "recipient_replied": "recipient_reply_event",
    "failed_definitive": "definitive_failure_response",
    "failed_uncertain": "uncertain_connector_result",
}
PASS_OR_NA = {"PASS", "NOT_APPLICABLE"}
PLACEHOLDERS = {"replace", "placeholder", "todo", "tbd", "n/a", "none"}
SHA256_PATTERN = re.compile(r"sha256:[a-f0-9]{64}")


class GateError(ValueError):
    pass


def load_contract(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GateError(f"cannot read contract: {exc}") from exc
    if not isinstance(value, dict):
        raise GateError("contract root must be an object")
    return value


def nonempty(value: Any, location: str) -> str:
    if (
        not isinstance(value, str)
        or not value.strip()
        or value.strip().lower() in PLACEHOLDERS
        or "replace-with-" in value.strip().lower()
    ):
        raise GateError(f"{location} must be a non-empty string")
    return value


def nonempty_list(value: Any, location: str) -> list[Any]:
    if not isinstance(value, list) or not value:
        raise GateError(f"{location} must be a non-empty list")
    return value


def string_list(value: Any, location: str) -> list[str]:
    items = nonempty_list(value, location)
    for index, item in enumerate(items):
        nonempty(item, f"{location}[{index}]")
    return items


def mapping(value: Any, location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GateError(f"{location} must be an object")
    return value


def result(value: Any, location: str, *, allow_na: bool = True) -> None:
    allowed = PASS_OR_NA if allow_na else {"PASS"}
    if value not in allowed:
        raise GateError(f"{location} must be {' or '.join(sorted(allowed))}")


def artifact(
    value: Any,
    project_root: Path,
    location: str,
    expected_type: str,
    task_id: str,
    build_id: str | None = None,
    expected_details: dict[str, Any] | None = None,
) -> Path:
    item = mapping(value, location)
    relative = Path(nonempty(item.get("path"), f"{location}.path"))
    if relative.is_absolute() or ".." in relative.parts:
        raise GateError(f"{location}.path must stay under project root")
    root_resolved = project_root.resolve()
    candidate = project_root / relative
    current = project_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise GateError(f"{location}.path contains a symlink")
    try:
        path = candidate.resolve(strict=True)
        path.relative_to(root_resolved)
    except (FileNotFoundError, ValueError) as exc:
        raise GateError(f"{location}.path escapes project root or is missing") from exc
    if not path.is_file():
        raise GateError(f"{location}.path does not resolve to a regular file")
    expected = item.get("sha256")
    if not isinstance(expected, str) or not SHA256_PATTERN.fullmatch(expected):
        raise GateError(f"{location}.sha256 is invalid")
    actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise GateError(f"{location}.sha256 does not match file content")
    if expected_type == "screenshot":
        payload = path.read_bytes()
        if path.suffix.lower() != ".png" or not payload.startswith(b"\x89PNG\r\n\x1a\n"):
            raise GateError(f"{location} must be a structurally valid PNG")
        offset = 8
        seen_ihdr = False
        seen_idat = False
        seen_iend = False
        while offset + 12 <= len(payload):
            length = struct.unpack(">I", payload[offset : offset + 4])[0]
            chunk_type = payload[offset + 4 : offset + 8]
            chunk_end = offset + 12 + length
            if chunk_end > len(payload):
                raise GateError(f"{location} has a truncated PNG chunk")
            chunk_data = payload[offset + 8 : offset + 8 + length]
            expected_crc = struct.unpack(">I", payload[offset + 8 + length : chunk_end])[0]
            if zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF != expected_crc:
                raise GateError(f"{location} has an invalid PNG checksum")
            if chunk_type == b"IHDR":
                if seen_ihdr or length != 13:
                    raise GateError(f"{location} has an invalid PNG header")
                width, height = struct.unpack(">II", chunk_data[:8])
                if width < 1 or height < 1:
                    raise GateError(f"{location} has invalid PNG dimensions")
                seen_ihdr = True
            elif chunk_type == b"IDAT":
                seen_idat = True
            elif chunk_type == b"IEND":
                seen_iend = True
                if chunk_end != len(payload):
                    raise GateError(f"{location} has trailing PNG data")
                break
            offset = chunk_end
        if not (seen_ihdr and seen_idat and seen_iend):
            raise GateError(f"{location} is not a complete PNG")
        return path
    if path.suffix.lower() != ".json":
        raise GateError(f"{location} must be a typed JSON artifact")
    try:
        payload_json = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GateError(f"{location} is not valid JSON") from exc
    if not isinstance(payload_json, dict) or payload_json.get("schema_version") != 1:
        raise GateError(f"{location} must use evidence schema_version 1")
    if payload_json.get("evidence_type") != expected_type:
        raise GateError(f"{location} evidence_type must be {expected_type}")
    if payload_json.get("task_id") != task_id:
        raise GateError(f"{location} task_id mismatch")
    if payload_json.get("result") != "PASS":
        raise GateError(f"{location} artifact result must be PASS")
    details = payload_json.get("details")
    if isinstance(details, str):
        nonempty(details, f"{location}.details")
    elif not isinstance(details, (dict, list)) or not details:
        raise GateError(f"{location}.details must contain structured evidence")
    if build_id is not None and payload_json.get("release_build_id") != build_id:
        raise GateError(f"{location} release_build_id mismatch")
    if expected_details is not None and details != expected_details:
        raise GateError(f"{location}.details do not match the claimed evidence")
    return path


def evidence_result(
    value: Any,
    project_root: Path,
    location: str,
    expected_type: str,
    task_id: str,
    *,
    allow_na: bool = True,
    build_id: str | None = None,
    expected_details: dict[str, Any] | None = None,
) -> None:
    item = mapping(value, location)
    result(item.get("result"), f"{location}.result", allow_na=allow_na)
    if item.get("result") == "PASS":
        artifact(
            item.get("artifact"), project_root, f"{location}.artifact",
            expected_type, task_id, build_id, expected_details,
        )
    else:
        nonempty(item.get("rationale"), f"{location}.rationale")


def validate_outcome(contract: dict[str, Any]) -> None:
    outcome = mapping(contract.get("outcome"), "outcome")
    for key in (
        "observable_result",
        "realistic_data",
        "external_result",
        "cost_scale_contract",
        "time_budget",
        "stop_condition",
        "rollback",
    ):
        nonempty(outcome.get(key), f"outcome.{key}")
    string_list(outcome.get("acceptance_criteria"), "outcome.acceptance_criteria")
    string_list(outcome.get("forbidden_simplifications"), "outcome.forbidden_simplifications")
    chain = mapping(outcome.get("chain"), "outcome.chain")
    if list(chain) != CHAIN:
        raise GateError("outcome.chain must contain the canonical ordered end-to-end chain")
    for key in CHAIN:
        nonempty(chain[key], f"outcome.chain.{key}")


def validate_reuse(contract: dict[str, Any]) -> None:
    reuse = mapping(contract.get("reuse"), "reuse")
    discovery = nonempty_list(reuse.get("discovery"), "reuse.discovery")
    kinds = [mapping(item, "reuse.discovery item").get("kind") for item in discovery]
    if kinds != REUSE_ORDER:
        raise GateError("reuse.discovery must follow the canonical search order")
    for index, item in enumerate(discovery):
        item = mapping(item, f"reuse.discovery[{index}]")
        if item.get("status") not in {"reused", "rejected", "not_applicable"}:
            raise GateError(f"reuse.discovery[{index}].status is invalid")
        nonempty(item.get("rationale"), f"reuse.discovery[{index}].rationale")
        if item.get("status") == "reused" and reuse.get("custom_code") is True:
            nonempty(item.get("remaining_gap"), f"reuse.discovery[{index}].remaining_gap")
    if reuse.get("custom_code") is True:
        nonempty(reuse.get("custom_code_reason"), "reuse.custom_code_reason")


def validate_scope(contract: dict[str, Any]) -> dict[str, bool]:
    scope = mapping(contract.get("scope"), "scope")
    required = ("web", "public_deploy", "integration", "hermes", "stateful")
    rationale = mapping(contract.get("scope_rationale"), "scope_rationale")
    for key in required:
        if not isinstance(scope.get(key), bool):
            raise GateError(f"scope.{key} must be boolean")
        nonempty(rationale.get(key), f"scope_rationale.{key}")
    if scope["public_deploy"] and not scope["web"]:
        raise GateError("public_deploy requires web scope")
    if scope["hermes"] and not scope["integration"]:
        raise GateError("hermes requires integration scope")
    return {key: scope[key] for key in required}


def validate_structured_checks(
    values: Any,
    project_root: Path,
    location: str,
    required_fields: tuple[str, ...],
    expected_type: str,
    task_id: str,
    build_id: str,
) -> None:
    for index, raw in enumerate(nonempty_list(values, location)):
        item = mapping(raw, f"{location}[{index}]")
        for field in required_fields:
            nonempty(item.get(field), f"{location}[{index}].{field}")
        if "expected" in required_fields and item["expected"] != item["observed"]:
            raise GateError(f"{location}[{index}] expected and observed values differ")
        if "expected_after" in required_fields and item["expected_after"] != item["observed_after"]:
            raise GateError(f"{location}[{index}] expected and observed state differ")
        result(item.get("result"), f"{location}[{index}].result", allow_na=False)
        claimed_details = {field: item[field] for field in required_fields}
        artifact(
            item.get("artifact"), project_root, f"{location}[{index}].artifact",
            expected_type, task_id, build_id, claimed_details,
        )


def validate_web(
    evidence: dict[str, Any], public_deploy: bool, project_root: Path, task_id: str
) -> None:
    web = mapping(evidence.get("web"), "evidence.web")
    nonempty(web.get("target_url"), "evidence.web.target_url")
    if web.get("environment") not in {"local", "preview", "public"}:
        raise GateError("evidence.web.environment is invalid")

    build_id = nonempty(web.get("release_build_id"), "evidence.web.release_build_id")
    evidence_result(
        web.get("browser_preflight"), project_root, "evidence.web.browser_preflight",
        "browser_preflight", task_id, allow_na=False, build_id=build_id,
        expected_details={"target_url": web["target_url"], "environment": web["environment"]},
    )
    screenshots = nonempty_list(web.get("screenshots"), "evidence.web.screenshots")
    required_shots = {
        (phase, viewport)
        for phase in ("baseline", "final")
        for viewport in ("desktop", "mobile")
    }
    observed_shots: set[tuple[str, str]] = set()
    screenshot_paths: set[Path] = set()
    screenshot_hashes: set[str] = set()
    for index, shot in enumerate(screenshots):
        shot = mapping(shot, f"evidence.web.screenshots[{index}]")
        pair = (shot.get("phase"), shot.get("viewport"))
        if pair in required_shots:
            observed_shots.add(pair)
        nonempty(shot.get("path"), f"evidence.web.screenshots[{index}].path")
        if shot.get("inspected") is not True:
            raise GateError(f"evidence.web.screenshots[{index}] was not visually inspected")
        screenshot_path = artifact(
            {"path": shot.get("path"), "sha256": shot.get("sha256")},
            project_root, f"evidence.web.screenshots[{index}]",
            "screenshot", task_id, build_id,
        )
        if screenshot_path in screenshot_paths:
            raise GateError("baseline/final desktop/mobile screenshots must be distinct")
        screenshot_paths.add(screenshot_path)
        if shot["sha256"] in screenshot_hashes:
            raise GateError("baseline/final desktop/mobile screenshot content must be distinct")
        screenshot_hashes.add(shot["sha256"])
        capture_details = {
            "phase": shot["phase"],
            "viewport": shot["viewport"],
            "target_url": web["target_url"],
            "image_sha256": shot["sha256"],
        }
        artifact(
            shot.get("capture_artifact"), project_root,
            f"evidence.web.screenshots[{index}].capture_artifact",
            "screenshot_capture", task_id, build_id, capture_details,
        )
    if observed_shots != required_shots:
        raise GateError("web evidence needs inspected baseline/final desktop/mobile screenshots")

    validate_structured_checks(
        web.get("dom_assertions"), project_root, "evidence.web.dom_assertions",
        ("assertion", "expected", "observed"), "dom_assertion", task_id, build_id,
    )
    validate_structured_checks(
        web.get("click_navigation_matrix"), project_root, "evidence.web.click_navigation_matrix",
        ("control", "action", "expected", "observed"), "click_navigation", task_id, build_id,
    )
    validate_structured_checks(
        web.get("state_transitions"), project_root, "evidence.web.state_transitions",
        ("before", "action", "expected_after", "observed_after"),
        "state_transition", task_id, build_id,
    )
    for key in ("empty", "error", "loading"):
        state = mapping(mapping(web.get("ui_states"), "evidence.web.ui_states").get(key), f"evidence.web.ui_states.{key}")
        evidence_result(
            state, project_root, f"evidence.web.ui_states.{key}",
            f"ui_state_{key}", task_id, build_id=build_id,
            expected_details={"state": key, "target_url": web["target_url"]},
        )
    health = mapping(web.get("browser_health"), "evidence.web.browser_health")
    for key in ("console", "runtime", "network", "overflow", "assets", "mobile_navigation"):
        item = mapping(health.get(key), f"evidence.web.browser_health.{key}")
        evidence_result(
            item, project_root, f"evidence.web.browser_health.{key}",
            f"browser_health_{key}", task_id, build_id=build_id,
            expected_details={"check": key, "target_url": web["target_url"]},
        )
    evidence_result(
        web.get("baseline_final_verdict"), project_root, "evidence.web.baseline_final_verdict",
        "baseline_final_verdict", task_id, allow_na=False, build_id=build_id,
        expected_details={"target_url": web["target_url"], "verdict": "no_regression"},
    )
    artifact(
        web.get("build_artifact"), project_root, "evidence.web.build_artifact",
        "build_manifest", task_id, build_id,
        {"target_url": web["target_url"], "environment": web["environment"]},
    )
    nonempty(web.get("rollback_command"), "evidence.web.rollback_command")
    if public_deploy:
        nonempty(web.get("public_url"), "evidence.web.public_url")
        evidence_result(
            web.get("public_post_deploy"), project_root, "evidence.web.public_post_deploy",
            "public_post_deploy", task_id, allow_na=False, build_id=build_id,
            expected_details={"public_url": web["public_url"], "verified": True},
        )
        if web.get("environment") != "public":
            raise GateError("public deploy evidence must target the public environment")


def validate_integration(evidence: dict[str, Any], project_root: Path, task_id: str) -> None:
    integration = mapping(evidence.get("integration"), "evidence.integration")
    outcomes = nonempty_list(integration.get("outcomes"), "evidence.integration.outcomes")
    for index, item in enumerate(outcomes):
        item = mapping(item, f"evidence.integration.outcomes[{index}]")
        state = item.get("state")
        if state not in OUTCOME_MEANINGS:
            raise GateError(f"evidence.integration.outcomes[{index}].state is invalid")
        if item.get("meaning") != OUTCOME_MEANINGS[state]:
            raise GateError(f"evidence.integration.outcomes[{index}] overclaims or changes {state}")
        nonempty(item.get("observed_event"), f"evidence.integration.outcomes[{index}].observed_event")
        if item.get("event_type") != OUTCOME_EVENT_TYPES[state]:
            raise GateError(f"evidence.integration.outcomes[{index}].event_type is invalid")
        event_id = item.get("observed_event_id")
        if not isinstance(event_id, str) or not SHA256_PATTERN.fullmatch(event_id):
            raise GateError(f"evidence.integration.outcomes[{index}].observed_event_id is invalid")
        claimed_details = {
            "state": state,
            "meaning": item["meaning"],
            "event_type": item["event_type"],
            "observed_event": item["observed_event"],
            "observed_event_id": event_id,
        }
        artifact(
            item.get("artifact"), project_root,
            f"evidence.integration.outcomes[{index}].artifact",
            "integration_outcome", task_id, expected_details=claimed_details,
        )
    for index, item in enumerate(integration.get("non_real_modes", [])):
        item = mapping(item, f"evidence.integration.non_real_modes[{index}]")
        if item.get("mode") not in {"dry_run", "mock", "replay", "synthetic"}:
            raise GateError(f"evidence.integration.non_real_modes[{index}].mode is invalid")
        if item.get("new_external_result") is not False:
            raise GateError("dry_run, mock, replay, and synthetic modes cannot claim a new external result")


def validate_fingerprints(evidence: dict[str, Any], project_root: Path, task_id: str) -> None:
    fingerprints = mapping(evidence.get("fingerprints"), "evidence.fingerprints")
    for key in ("authoritative_rows", "authorization_ledger"):
        item = mapping(fingerprints.get(key), f"evidence.fingerprints.{key}")
        before = nonempty(item.get("before"), f"evidence.fingerprints.{key}.before")
        after = nonempty(item.get("after"), f"evidence.fingerprints.{key}.after")
        if before != after:
            raise GateError(f"evidence.fingerprints.{key} changed")
        claimed_details = {"before": before, "after": after}
        artifact(
            item.get("artifact"), project_root, f"evidence.fingerprints.{key}.artifact",
            f"fingerprint_{key}", task_id, expected_details=claimed_details,
        )


def validate_hermes(evidence: dict[str, Any], project_root: Path, task_id: str) -> None:
    hermes = mapping(evidence.get("hermes"), "evidence.hermes")
    if hermes.get("optional") is not True:
        raise GateError("Hermes must remain optional")
    if hermes.get("authoritative") is not False:
        raise GateError("Hermes cannot own authoritative product state")
    for key in ("version_config", "gateway_lifecycle", "channels", "cron_jobs", "tools_files"):
        evidence_result(
            hermes.get(key), project_root, f"evidence.hermes.{key}",
            f"hermes_{key}", task_id, allow_na=False,
            expected_details={"capability": key, "verified": True},
        )
    if hermes.get("llm_routing") not in {"direct_model", "hermes_with_runtime_benefit", "not_needed"}:
        raise GateError("evidence.hermes.llm_routing is invalid")
    restart = mapping(hermes.get("restart"), "evidence.hermes.restart")
    if restart.get("service_notifications") not in {"silent", "authorized", "none"}:
        raise GateError("Hermes restart side effects must be silent, authorized, or absent")
    send = mapping(hermes.get("send_capability"), "evidence.hermes.send_capability")
    if send.get("enabled") is True:
        nonempty_list(send.get("intent_ids"), "evidence.hermes.send_capability.intent_ids")
        nonempty_list(send.get("allowed_channels"), "evidence.hermes.send_capability.allowed_channels")
        if not isinstance(send.get("max_calls"), int) or send["max_calls"] < 1:
            raise GateError("evidence.hermes.send_capability.max_calls must be positive")
        nonempty(send.get("authorization_ledger"), "evidence.hermes.send_capability.authorization_ledger")
        if send.get("automatic_retry_after_uncertain") is not False:
            raise GateError("Hermes cannot automatically retry uncertain sends")


def validate_contract(contract: dict[str, Any], phase: str, project_root: Path) -> None:
    if contract.get("schema_version") != 1:
        raise GateError("schema_version must be 1")
    task_id = nonempty(contract.get("task_id"), "task_id")
    validate_outcome(contract)
    validate_reuse(contract)
    scope = validate_scope(contract)
    if phase == "preflight":
        return
    evidence = mapping(contract.get("evidence"), "evidence")
    if scope["web"]:
        validate_web(evidence, scope["public_deploy"], project_root, task_id)
    if scope["integration"]:
        validate_integration(evidence, project_root, task_id)
    if scope["stateful"]:
        validate_fingerprints(evidence, project_root, task_id)
    if scope["hermes"]:
        validate_hermes(evidence, project_root, task_id)
    review = mapping(evidence.get("review"), "evidence.review")
    for key, evidence_type in (
        ("implementation", "implementation_review"),
        ("clean_context", "clean_context_review"),
    ):
        item = mapping(review.get(key), f"evidence.review.{key}")
        details = {
            "reviewer": nonempty(item.get("reviewer"), f"evidence.review.{key}.reviewer"),
            "head": nonempty(item.get("head"), f"evidence.review.{key}.head"),
            "summary": nonempty(item.get("summary"), f"evidence.review.{key}.summary"),
            "findings": item.get("findings"),
        }
        if not isinstance(details["findings"], list):
            raise GateError(f"evidence.review.{key}.findings must be a list")
        evidence_result(
            item, project_root, f"evidence.review.{key}", evidence_type,
            task_id, allow_na=False, expected_details=details,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("preflight", "acceptance"))
    parser.add_argument("contract", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path("."))
    args = parser.parse_args()
    try:
        validate_contract(load_contract(args.contract), args.phase, args.project_root.resolve())
    except GateError as exc:
        print(f"MVP OS GATE: BLOCKED: {exc}")
        return 2
    print(f"MVP OS GATE: PASS ({args.phase})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
