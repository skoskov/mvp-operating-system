#!/usr/bin/env python3
"""Validate MVP OS v2.1 task contracts and acceptance evidence."""

from __future__ import annotations

import argparse
import json
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
PASS_OR_NA = {"PASS", "NOT_APPLICABLE"}


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
    if not isinstance(value, str) or not value.strip():
        raise GateError(f"{location} must be a non-empty string")
    return value


def nonempty_list(value: Any, location: str) -> list[Any]:
    if not isinstance(value, list) or not value:
        raise GateError(f"{location} must be a non-empty list")
    return value


def mapping(value: Any, location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GateError(f"{location} must be an object")
    return value


def result(value: Any, location: str, *, allow_na: bool = True) -> None:
    allowed = PASS_OR_NA if allow_na else {"PASS"}
    if value not in allowed:
        raise GateError(f"{location} must be {' or '.join(sorted(allowed))}")


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
    nonempty_list(outcome.get("acceptance_criteria"), "outcome.acceptance_criteria")
    nonempty_list(outcome.get("forbidden_simplifications"), "outcome.forbidden_simplifications")
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
    if reuse.get("custom_code") is True:
        nonempty(reuse.get("custom_code_reason"), "reuse.custom_code_reason")


def validate_scope(contract: dict[str, Any]) -> dict[str, bool]:
    scope = mapping(contract.get("scope"), "scope")
    required = ("web", "public_deploy", "integration", "hermes", "stateful")
    for key in required:
        if not isinstance(scope.get(key), bool):
            raise GateError(f"scope.{key} must be boolean")
    if scope["public_deploy"] and not scope["web"]:
        raise GateError("public_deploy requires web scope")
    if scope["hermes"] and not scope["integration"]:
        raise GateError("hermes requires integration scope")
    return {key: scope[key] for key in required}


def validate_web(evidence: dict[str, Any], public_deploy: bool) -> None:
    web = mapping(evidence.get("web"), "evidence.web")
    result(web.get("browser_preflight"), "evidence.web.browser_preflight", allow_na=False)
    nonempty(web.get("target_url"), "evidence.web.target_url")
    if web.get("environment") not in {"local", "preview", "public"}:
        raise GateError("evidence.web.environment is invalid")

    screenshots = nonempty_list(web.get("screenshots"), "evidence.web.screenshots")
    required_shots = {
        (phase, viewport)
        for phase in ("baseline", "final")
        for viewport in ("desktop", "mobile")
    }
    observed_shots: set[tuple[str, str]] = set()
    for index, shot in enumerate(screenshots):
        shot = mapping(shot, f"evidence.web.screenshots[{index}]")
        pair = (shot.get("phase"), shot.get("viewport"))
        if pair in required_shots:
            observed_shots.add(pair)
        nonempty(shot.get("path"), f"evidence.web.screenshots[{index}].path")
        if shot.get("inspected") is not True:
            raise GateError(f"evidence.web.screenshots[{index}] was not visually inspected")
    if observed_shots != required_shots:
        raise GateError("web evidence needs inspected baseline/final desktop/mobile screenshots")

    nonempty_list(web.get("dom_assertions"), "evidence.web.dom_assertions")
    nonempty_list(web.get("click_navigation_matrix"), "evidence.web.click_navigation_matrix")
    nonempty_list(web.get("state_transitions"), "evidence.web.state_transitions")
    for key in ("empty", "error", "loading"):
        state = mapping(mapping(web.get("ui_states"), "evidence.web.ui_states").get(key), f"evidence.web.ui_states.{key}")
        result(state.get("result"), f"evidence.web.ui_states.{key}.result")
        if state.get("result") == "NOT_APPLICABLE":
            nonempty(state.get("rationale"), f"evidence.web.ui_states.{key}.rationale")
    health = mapping(web.get("browser_health"), "evidence.web.browser_health")
    for key in ("console", "runtime", "network", "overflow", "assets", "mobile_navigation"):
        item = mapping(health.get(key), f"evidence.web.browser_health.{key}")
        result(item.get("result"), f"evidence.web.browser_health.{key}.result")
        if item.get("result") == "NOT_APPLICABLE":
            nonempty(item.get("rationale"), f"evidence.web.browser_health.{key}.rationale")
    result(web.get("baseline_final_verdict"), "evidence.web.baseline_final_verdict", allow_na=False)
    nonempty(web.get("release_build_id"), "evidence.web.release_build_id")
    nonempty(web.get("rollback_command"), "evidence.web.rollback_command")
    if public_deploy:
        nonempty(web.get("public_url"), "evidence.web.public_url")
        result(web.get("public_post_deploy"), "evidence.web.public_post_deploy", allow_na=False)
        if web.get("environment") != "public":
            raise GateError("public deploy evidence must target the public environment")


def validate_integration(evidence: dict[str, Any]) -> None:
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
    for index, item in enumerate(integration.get("non_real_modes", [])):
        item = mapping(item, f"evidence.integration.non_real_modes[{index}]")
        if item.get("mode") not in {"dry_run", "mock", "replay", "synthetic"}:
            raise GateError(f"evidence.integration.non_real_modes[{index}].mode is invalid")
        if item.get("new_external_result") is not False:
            raise GateError("dry_run, mock, replay, and synthetic modes cannot claim a new external result")


def validate_fingerprints(evidence: dict[str, Any]) -> None:
    fingerprints = mapping(evidence.get("fingerprints"), "evidence.fingerprints")
    for key in ("authoritative_rows", "authorization_ledger"):
        item = mapping(fingerprints.get(key), f"evidence.fingerprints.{key}")
        before = nonempty(item.get("before"), f"evidence.fingerprints.{key}.before")
        after = nonempty(item.get("after"), f"evidence.fingerprints.{key}.after")
        if before != after:
            raise GateError(f"evidence.fingerprints.{key} changed")


def validate_hermes(evidence: dict[str, Any]) -> None:
    hermes = mapping(evidence.get("hermes"), "evidence.hermes")
    if hermes.get("optional") is not True:
        raise GateError("Hermes must remain optional")
    if hermes.get("authoritative") is not False:
        raise GateError("Hermes cannot own authoritative product state")
    for key in ("version_config", "gateway_lifecycle", "channels", "cron_jobs", "tools_files"):
        result(hermes.get(key), f"evidence.hermes.{key}", allow_na=False)
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


def validate_contract(contract: dict[str, Any], phase: str) -> None:
    if contract.get("schema_version") != 1:
        raise GateError("schema_version must be 1")
    nonempty(contract.get("task_id"), "task_id")
    validate_outcome(contract)
    validate_reuse(contract)
    scope = validate_scope(contract)
    if phase == "preflight":
        return
    evidence = mapping(contract.get("evidence"), "evidence")
    if scope["web"]:
        validate_web(evidence, scope["public_deploy"])
    if scope["integration"]:
        validate_integration(evidence)
    if scope["stateful"]:
        validate_fingerprints(evidence)
    if scope["hermes"]:
        validate_hermes(evidence)
    review = mapping(evidence.get("review"), "evidence.review")
    result(review.get("implementation"), "evidence.review.implementation", allow_na=False)
    result(review.get("clean_context"), "evidence.review.clean_context", allow_na=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("preflight", "acceptance"))
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    try:
        validate_contract(load_contract(args.contract), args.phase)
    except GateError as exc:
        print(f"MVP OS GATE: BLOCKED: {exc}")
        return 2
    print(f"MVP OS GATE: PASS ({args.phase})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

