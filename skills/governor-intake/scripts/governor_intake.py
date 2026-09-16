#!/usr/bin/env python3
"""Minimal, intake-only deferred-task recorder for Capacity Governor."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATES = (
    "CAPTURED",
    "INTAKE_COMPLETE",
    "WAITING_FOR_RESET",
    "HUMAN_APPROVAL_REQUIRED",
    "WAITING_FOR_INPUT",
    "READY_TO_EXECUTE",
    "EXECUTING",
    "VERIFIED",
    "COMPLETE",
)
CAPACITY_STATES = ("NOT_OBSERVED",)
TASK_KINDS = ("ARTIFACT_EDIT", "OTHER")
ALLOWED_TRANSITIONS = {
    "CAPTURED": {"INTAKE_COMPLETE"},
    "INTAKE_COMPLETE": {"WAITING_FOR_RESET", "HUMAN_APPROVAL_REQUIRED", "WAITING_FOR_INPUT", "READY_TO_EXECUTE"},
    "WAITING_FOR_RESET": {"HUMAN_APPROVAL_REQUIRED", "WAITING_FOR_INPUT", "READY_TO_EXECUTE"},
    "HUMAN_APPROVAL_REQUIRED": {"WAITING_FOR_RESET", "WAITING_FOR_INPUT", "READY_TO_EXECUTE"},
    "WAITING_FOR_INPUT": {"WAITING_FOR_RESET", "HUMAN_APPROVAL_REQUIRED", "READY_TO_EXECUTE"},
    "READY_TO_EXECUTE": {"WAITING_FOR_RESET", "HUMAN_APPROVAL_REQUIRED", "WAITING_FOR_INPUT", "EXECUTING"},
    "EXECUTING": {"VERIFIED"},
    "VERIFIED": {"COMPLETE"},
    "COMPLETE": set(),
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def parse_percentage(value: str) -> float:
    try:
        percentage = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a number from 0 to 100") from exc
    if not 0 <= percentage <= 100:
        raise argparse.ArgumentTypeError("expected a number from 0 to 100")
    return percentage


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:48] or "task"


def payload_size(value: Any) -> int:
    return len(json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8"))


def atomic_write(path: Path, record: dict[str, Any]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(record, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=path.parent, suffix=".tmp") as handle:
        handle.write(rendered)
        temp_name = handle.name
    os.replace(temp_name, path)
    return len(rendered.encode("utf-8"))


def load_record(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        record = json.load(handle)
    validate_record(record)
    return record


def validate_record(record: dict[str, Any]) -> None:
    required = {
        "task_id", "title", "objective", "status", "inputs", "supplied_context",
        "authorized_work", "settled_decisions", "do_not_reopen", "human_review_items",
        "human_approval_required", "human_approval_granted", "capacity_state",
        "capacity_check_required_at_execution", "capacity_observations",
        "blockers", "resume_instruction", "intake_measurement",
        "resume_measurement", "execution_performed",
        "task_completeness",
    }
    missing = sorted(required - set(record))
    if missing:
        raise ValueError(f"missing record fields: {missing}")
    if record["status"] not in STATES:
        raise ValueError(f"invalid status: {record['status']}")
    if record["capacity_state"] not in CAPACITY_STATES:
        raise ValueError(f"invalid capacity_state: {record['capacity_state']}")
    if record["capacity_check_required_at_execution"] is not True:
        raise ValueError("capacity_check_required_at_execution must be true")
    if not isinstance(record["capacity_observations"], list):
        raise ValueError("capacity_observations must be a list")
    for observation in record["capacity_observations"]:
        if not isinstance(observation, dict) or not all(
            nonblank(observation.get(name)) for name in ("observed_at", "source")
        ):
            raise ValueError("each capacity observation requires observed_at and source")
        percent = observation.get("available_percent")
        if percent is not None and (not isinstance(percent, (int, float)) or not 0 <= percent <= 100):
            raise ValueError("available_percent must be between 0 and 100 when supplied")
    if record["execution_performed"] is not False and record["status"] not in {"EXECUTING", "VERIFIED", "COMPLETE"}:
        raise ValueError("Intake records cannot claim execution")
    for name in ("inputs", "authorized_work", "settled_decisions", "do_not_reopen", "human_review_items", "blockers"):
        if not isinstance(record[name], list) or not all(isinstance(item, str) for item in record[name]):
            raise ValueError(f"{name} must be a list of strings")
    completeness = record["task_completeness"]
    required_completeness = {
        "task_kind", "targets_explicitly_supplied", "change_explicitly_supplied",
        "expected_output_or_completion_condition", "missing_requirements",
        "human_clarification_required",
    }
    if not isinstance(completeness, dict) or required_completeness - set(completeness):
        raise ValueError("task_completeness is missing required fields")
    if completeness["task_kind"] not in TASK_KINDS:
        raise ValueError(f"invalid task_kind: {completeness['task_kind']}")
    if not isinstance(completeness["targets_explicitly_supplied"], bool):
        raise ValueError("targets_explicitly_supplied must be boolean")
    if not isinstance(completeness["change_explicitly_supplied"], bool):
        raise ValueError("change_explicitly_supplied must be boolean")
    if not isinstance(completeness["expected_output_or_completion_condition"], str):
        raise ValueError("expected_output_or_completion_condition must be a string")
    if not isinstance(completeness["missing_requirements"], list) or not all(
        isinstance(item, str) for item in completeness["missing_requirements"]
    ):
        raise ValueError("missing_requirements must be a list of strings")
    if not isinstance(completeness["human_clarification_required"], bool):
        raise ValueError("human_clarification_required must be boolean")


def nonblank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonblank_items(values: Any) -> bool:
    return isinstance(values, list) and bool(values) and all(nonblank(value) for value in values)


def completeness_result(record: dict[str, Any]) -> dict[str, Any]:
    stored = record["task_completeness"]
    task_kind = stored["task_kind"]
    missing: list[str] = []
    if task_kind == "ARTIFACT_EDIT":
        if not stored["targets_explicitly_supplied"] or not nonblank_items(record["inputs"]):
            missing.append("exact_target_artifacts_or_supplied_identifiers")
        if not stored["change_explicitly_supplied"] or not nonblank(record["objective"]):
            missing.append("exact_requested_change_or_bounded_objective")
        if not nonblank_items(record["authorized_work"]):
            missing.append("authorized_scope")
        if not (nonblank_items(record["do_not_reopen"]) or nonblank_items(record["settled_decisions"])):
            missing.append("do_not_reopen_or_settled_decision_boundaries")
        if not nonblank(stored["expected_output_or_completion_condition"]):
            missing.append("expected_output_or_completion_condition")
    return {
        "task_kind": task_kind,
        "targets_explicitly_supplied": bool(stored["targets_explicitly_supplied"]),
        "change_explicitly_supplied": bool(stored["change_explicitly_supplied"]),
        "expected_output_or_completion_condition": stored["expected_output_or_completion_condition"],
        "missing_requirements": missing,
        "human_clarification_required": bool(missing),
    }


def refresh_completeness(record: dict[str, Any]) -> dict[str, Any]:
    result = completeness_result(record)
    record["task_completeness"] = result
    return result


def recommended_state(record: dict[str, Any]) -> str:
    if completeness_result(record)["human_clarification_required"]:
        return "WAITING_FOR_INPUT"
    if record["blockers"]:
        return "WAITING_FOR_INPUT"
    if record["human_approval_required"] and not record["human_approval_granted"]:
        return "HUMAN_APPROVAL_REQUIRED"
    return "READY_TO_EXECUTE"


def eligibility(record: dict[str, Any]) -> dict[str, Any]:
    completeness = completeness_result(record)
    state = recommended_state(record)
    return {
        "eligible": False,
        "durable_prerequisites_satisfied": state == "READY_TO_EXECUTE",
        "recommended_state": state,
        "human_approval_required": record["human_approval_required"],
        "human_approval_granted": record["human_approval_granted"],
        "capacity_state": record["capacity_state"],
        "capacity_check_required_at_execution": record["capacity_check_required_at_execution"],
        "historical_capacity_observation_count": len(record["capacity_observations"]),
        "blockers": list(record["blockers"]),
        "task_completeness": completeness,
        "execution_performed": False,
    }


def create_record(args: argparse.Namespace) -> tuple[Path, dict[str, Any]]:
    started = time.perf_counter_ns()
    task_id = args.task_id or f"GI-{datetime.now(timezone.utc):%Y%m%d}-{uuid.uuid4().hex[:8]}"
    record = {
        "schema_version": "governor-intake-v0.1.2",
        "task_id": task_id,
        "title": args.title,
        "objective": args.objective,
        "status": "INTAKE_COMPLETE",
        "priority": args.priority,
        "inputs": list(args.input or []),
        "supplied_context": args.context,
        "authorized_work": list(args.authorized_work or []),
        "settled_decisions": list(args.settled_decision or []),
        "do_not_reopen": list(args.do_not_reopen or []),
        "human_review_items": list(args.human_review_item or []),
        "human_approval_required": args.human_approval_required,
        "human_approval_granted": args.human_approval_granted,
        "capacity_state": "NOT_OBSERVED",
        "capacity_check_required_at_execution": True,
        "capacity_observations": [],
        "blockers": list(args.blocker or []),
        "resume_instruction": args.resume_instruction,
        "task_completeness": {
            "task_kind": args.task_kind,
            "targets_explicitly_supplied": args.targets_explicitly_supplied,
            "change_explicitly_supplied": args.change_explicitly_supplied,
            "expected_output_or_completion_condition": args.completion_condition or "",
            "missing_requirements": [],
            "human_clarification_required": False,
        },
        "created_at": now_utc(),
        "updated_at": now_utc(),
        "execution_performed": False,
        "intake_measurement": {
            "usage_before": args.usage_before,
            "usage_after": args.usage_after,
            "displayed_delta": args.displayed_delta,
            "supplied_payload_bytes": 0,
            "record_bytes": 0,
            "elapsed_ms": 0.0,
            "measurement_note": "Observed values only; NOT_OBSERVED does not mean zero usage.",
        },
        "resume_measurement": None,
        "history": [{"at": now_utc(), "event": "INTAKE_CREATED", "status": "INTAKE_COMPLETE"}],
    }
    completeness = refresh_completeness(record)
    if completeness["human_clarification_required"]:
        record["status"] = "WAITING_FOR_INPUT"
        record["history"].append(
            {
                "at": now_utc(),
                "event": "COMPLETENESS_VALIDATED",
                "status": "WAITING_FOR_INPUT",
                "missing_requirements": list(completeness["missing_requirements"]),
            }
        )
    record["intake_measurement"]["supplied_payload_bytes"] = payload_size(record)
    record["intake_measurement"]["elapsed_ms"] = round((time.perf_counter_ns() - started) / 1_000_000, 3)
    path = Path(args.queue_dir) / f"{task_id}_{slugify(args.title)}.json"
    record["intake_measurement"]["record_bytes"] = payload_size(record)
    written = atomic_write(path, record)
    record["intake_measurement"]["record_bytes"] = written
    atomic_write(path, record)
    return path, record


def apply_recommended_state(record: dict[str, Any]) -> None:
    target = recommended_state(record)
    current = record["status"]
    if current == target:
        return
    if target not in ALLOWED_TRANSITIONS.get(current, set()):
        raise ValueError(f"transition {current} -> {target} is not allowed")
    record["status"] = target
    record["updated_at"] = now_utc()
    record["history"].append({"at": now_utc(), "event": "GATES_EVALUATED", "status": target})


def set_gates(args: argparse.Namespace) -> dict[str, Any]:
    path = Path(args.record)
    record = load_record(path)
    if args.human_approved is not None:
        record["human_approval_granted"] = args.human_approved
    refresh_completeness(record)
    apply_recommended_state(record)
    atomic_write(path, record)
    return record


def record_capacity_observation(args: argparse.Namespace) -> dict[str, Any]:
    path = Path(args.record)
    record = load_record(path)
    observation = {
        "observed_at": now_utc(),
        "source": args.source,
        "note": "Historical observation only; it does not determine future execution readiness.",
    }
    if args.available_percent is not None:
        observation["available_percent"] = args.available_percent
    record["capacity_observations"].append(observation)
    record["capacity_state"] = "NOT_OBSERVED"
    record["capacity_check_required_at_execution"] = True
    record["updated_at"] = now_utc()
    record["history"].append(
        {
            "at": now_utc(),
            "event": "CAPACITY_OBSERVATION_RECORDED",
            "source": args.source,
            "status": record["status"],
        }
    )
    apply_recommended_state(record)
    atomic_write(path, record)
    return record


def prepare_resume(args: argparse.Namespace) -> dict[str, Any]:
    started = time.perf_counter_ns()
    path = Path(args.record)
    record = load_record(path)
    refresh_completeness(record)
    apply_recommended_state(record)
    gate_result = eligibility(record)
    envelope = {
        "task_id": record["task_id"],
        "title": record["title"],
        "objective": record["objective"],
        "inputs": record["inputs"],
        "authorized_work": record["authorized_work"],
        "settled_decisions": record["settled_decisions"],
        "do_not_reopen": record["do_not_reopen"],
        "human_review_items": record["human_review_items"],
        "task_completeness": record["task_completeness"],
        "capacity_state": record["capacity_state"],
        "capacity_check_required_at_execution": record["capacity_check_required_at_execution"],
        "capacity_observations": record["capacity_observations"],
        "resume_instruction": record["resume_instruction"],
        "gates": gate_result,
        "execution_performed": False,
    }
    measurement = {
        "measured_at": now_utc(),
        "record_bytes": path.stat().st_size,
        "resume_envelope_bytes": payload_size(envelope),
        "context_reconstruction_actions": list(args.reconstruction_action or []),
        "reconstruction_action_count": len(args.reconstruction_action or []),
        "elapsed_ms": round((time.perf_counter_ns() - started) / 1_000_000, 3),
        "substantive_execution_cost": "NOT_MEASURED",
        "claim_boundary": "Observation from this record only; no efficiency claim established.",
    }
    record["resume_measurement"] = measurement
    record["updated_at"] = now_utc()
    record["history"].append({"at": now_utc(), "event": "RESUME_PREPARED", "status": record["status"]})
    atomic_write(path, record)
    return {"record": str(path), "resume_envelope": envelope, "resume_measurement": measurement}


def validate_completeness(args: argparse.Namespace) -> dict[str, Any]:
    path = Path(args.record)
    record = load_record(path)
    result = refresh_completeness(record)
    apply_recommended_state(record)
    record["updated_at"] = now_utc()
    record["history"].append(
        {
            "at": now_utc(),
            "event": "COMPLETENESS_VALIDATED",
            "status": record["status"],
            "missing_requirements": list(result["missing_requirements"]),
        }
    )
    record["execution_performed"] = False
    atomic_write(path, record)
    return record


def transition(args: argparse.Namespace) -> dict[str, Any]:
    path = Path(args.record)
    record = load_record(path)
    target = args.to
    current = record["status"]
    if target not in ALLOWED_TRANSITIONS.get(current, set()):
        raise ValueError(f"transition {current} -> {target} is not allowed")
    if target in {"READY_TO_EXECUTE", "EXECUTING"} and recommended_state(record) != "READY_TO_EXECUTE":
        raise ValueError("readiness requires a complete execution contract and satisfied human approval gate")
    capacity_check = None
    if target == "EXECUTING":
        if getattr(args, "fresh_capacity_confirmed", None) is not True or not nonblank(
            getattr(args, "fresh_capacity_source", None)
        ):
            raise ValueError("execution requires a fresh capacity check supplied with the execution transition")
        capacity_check = {
            "checked_at": now_utc(),
            "source": args.fresh_capacity_source,
            "available": True,
        }
        if getattr(args, "fresh_capacity_percent", None) is not None:
            capacity_check["available_percent"] = args.fresh_capacity_percent
    record["status"] = target
    record["execution_performed"] = target in {"EXECUTING", "VERIFIED", "COMPLETE"}
    record["updated_at"] = now_utc()
    history_event = {"at": now_utc(), "event": args.event, "status": target}
    if capacity_check is not None:
        history_event["fresh_capacity_check"] = capacity_check
    record["history"].append(history_event)
    atomic_write(path, record)
    return record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="Create an intake-only deferred task record")
    create.add_argument("--queue-dir", required=True)
    create.add_argument("--task-id")
    create.add_argument("--title", required=True)
    create.add_argument("--objective", required=True)
    create.add_argument("--priority")
    create.add_argument("--input", action="append")
    create.add_argument("--context", required=True)
    create.add_argument("--task-kind", choices=TASK_KINDS, required=True)
    create.add_argument("--targets-explicitly-supplied", type=parse_bool, default=False)
    create.add_argument("--change-explicitly-supplied", type=parse_bool, default=False)
    create.add_argument("--completion-condition")
    create.add_argument("--authorized-work", action="append")
    create.add_argument("--settled-decision", action="append")
    create.add_argument("--do-not-reopen", action="append")
    create.add_argument("--human-review-item", action="append")
    create.add_argument("--human-approval-required", type=parse_bool, default=True)
    create.add_argument("--human-approval-granted", type=parse_bool, default=False)
    create.add_argument("--blocker", action="append")
    create.add_argument("--resume-instruction", required=True)
    create.add_argument("--usage-before", default="NOT_OBSERVED")
    create.add_argument("--usage-after", default="NOT_OBSERVED")
    create.add_argument("--displayed-delta", default="NOT_OBSERVED")

    evaluate = sub.add_parser("evaluate", help="Report independent gate eligibility without executing")
    evaluate.add_argument("record")

    completeness = sub.add_parser(
        "validate-completeness",
        help="Persist task-completeness findings and block incomplete artifact tasks without executing",
    )
    completeness.add_argument("record")

    gates = sub.add_parser("set-gates", help="Update the durable human approval gate")
    gates.add_argument("record")
    gates.add_argument("--human-approved", type=parse_bool)

    capacity = sub.add_parser(
        "record-capacity-observation",
        help="Append a timestamped historical capacity observation without changing readiness",
    )
    capacity.add_argument("record")
    capacity.add_argument("--source", required=True)
    capacity.add_argument("--available-percent", type=parse_percentage)

    resume = sub.add_parser("prepare-resume", help="Build a bounded resume envelope without executing")
    resume.add_argument("record")
    resume.add_argument("--reconstruction-action", action="append")

    lifecycle = sub.add_parser("transition", help="Record an external lifecycle event")
    lifecycle.add_argument("record")
    lifecycle.add_argument("--to", choices=STATES, required=True)
    lifecycle.add_argument("--event", required=True)
    lifecycle.add_argument("--fresh-capacity-confirmed", type=parse_bool)
    lifecycle.add_argument("--fresh-capacity-source")
    lifecycle.add_argument("--fresh-capacity-percent", type=parse_percentage)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "create":
        path, record = create_record(args)
        output = {"record": str(path), "status": record["status"], "gates": eligibility(record), "execution_performed": False}
    elif args.command == "evaluate":
        output = eligibility(load_record(Path(args.record)))
    elif args.command == "validate-completeness":
        record = validate_completeness(args)
        output = {
            "record": args.record,
            "status": record["status"],
            "task_completeness": record["task_completeness"],
            "execution_performed": False,
        }
    elif args.command == "set-gates":
        record = set_gates(args)
        output = {"record": args.record, "status": record["status"], "gates": eligibility(record), "execution_performed": False}
    elif args.command == "record-capacity-observation":
        record = record_capacity_observation(args)
        output = {
            "record": args.record,
            "status": record["status"],
            "capacity_state": record["capacity_state"],
            "capacity_check_required_at_execution": record["capacity_check_required_at_execution"],
            "historical_capacity_observation_count": len(record["capacity_observations"]),
            "execution_performed": False,
        }
    elif args.command == "prepare-resume":
        output = prepare_resume(args)
    else:
        record = transition(args)
        output = {"record": args.record, "status": record["status"], "execution_performed": record["execution_performed"]}
    print(json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
