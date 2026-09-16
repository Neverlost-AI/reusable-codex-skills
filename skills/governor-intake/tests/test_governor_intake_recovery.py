#!/usr/bin/env python3
"""Recovery acceptance checks for the recovered Governor Intake v0.1.2 package."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "governor_intake.py"


def jrun(args: list[str]) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"command failed {args}: {proc.stderr}\n{proc.stdout}")
    return json.loads(proc.stdout)


def main() -> int:
    results: list[tuple[str, bool]] = []

    with tempfile.TemporaryDirectory() as temp_dir:
        queue_dir = Path(temp_dir) / "queue"

        out = jrun(
            [
                "create",
                "--queue-dir",
                str(queue_dir),
                "--task-id",
                "GI-TEST-COMPLETE",
                "--title",
                "Polish packet",
                "--objective",
                "Apply bounded final polish",
                "--context",
                "Strategy is settled",
                "--task-kind",
                "ARTIFACT_EDIT",
                "--targets-explicitly-supplied",
                "true",
                "--change-explicitly-supplied",
                "true",
                "--completion-condition",
                "Revised packet saved for review",
                "--input",
                "packet.docx",
                "--authorized-work",
                "Polish wording only",
                "--settled-decision",
                "Strategy remains unchanged",
                "--do-not-reopen",
                "Do not reopen positioning",
                "--human-approval-required",
                "true",
                "--human-approval-granted",
                "false",
                "--resume-instruction",
                "Polish only within supplied bounds",
            ]
        )
        record_path = Path(out["record"])
        record = json.loads(record_path.read_text(encoding="utf-8"))
        results.append(("intake_nonexecuting", out["execution_performed"] is False and record["execution_performed"] is False))
        results.append(("capacity_not_observed", record["capacity_state"] == "NOT_OBSERVED" and record["capacity_check_required_at_execution"] is True))
        results.append(("bounds_preserved", record["do_not_reopen"] == ["Do not reopen positioning"] and record["settled_decisions"] == ["Strategy remains unchanged"]))

        out = jrun(["validate-completeness", str(record_path)])
        results.append(("approval_gate", out["status"] == "HUMAN_APPROVAL_REQUIRED"))

        out = jrun(
            [
                "record-capacity-observation",
                str(record_path),
                "--source",
                "human displayed meter",
                "--available-percent",
                "80",
            ]
        )
        results.append(("historical_capacity_not_readiness", out["status"] == "HUMAN_APPROVAL_REQUIRED" and out["capacity_state"] == "NOT_OBSERVED" and out["capacity_check_required_at_execution"] is True))

        out = jrun(["set-gates", str(record_path), "--human-approved", "true"])
        results.append(("approval_to_ready", out["status"] == "READY_TO_EXECUTE" and out["execution_performed"] is False))

        out = jrun(
            [
                "prepare-resume",
                str(record_path),
                "--reconstruction-action",
                "loaded task record only",
            ]
        )
        envelope = out["resume_envelope"]
        results.append(("resume_nonexecuting", envelope["execution_performed"] is False and envelope["capacity_state"] == "NOT_OBSERVED" and envelope["do_not_reopen"] == ["Do not reopen positioning"]))
        results.append(("resume_measurement_bounded", out["resume_measurement"]["reconstruction_action_count"] == 1 and out["resume_measurement"]["substantive_execution_cost"] == "NOT_MEASURED"))

        proc = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "transition",
                str(record_path),
                "--to",
                "EXECUTING",
                "--event",
                "START",
            ],
            capture_output=True,
            text=True,
        )
        results.append(("execution_requires_fresh_capacity", proc.returncode != 0 and "fresh capacity check" in proc.stderr.lower()))

        out = jrun(
            [
                "transition",
                str(record_path),
                "--to",
                "EXECUTING",
                "--event",
                "START",
                "--fresh-capacity-confirmed",
                "true",
                "--fresh-capacity-source",
                "human meter",
                "--fresh-capacity-percent",
                "80",
            ]
        )
        results.append(("fresh_capacity_allows_execution", out["status"] == "EXECUTING" and out["execution_performed"] is True))
        jrun(["transition", str(record_path), "--to", "VERIFIED", "--event", "VERIFY"])
        out = jrun(["transition", str(record_path), "--to", "COMPLETE", "--event", "CLOSE"])
        results.append(("lifecycle_to_complete", out["status"] == "COMPLETE" and out["execution_performed"] is True))

        out = jrun(
            [
                "create",
                "--queue-dir",
                str(queue_dir),
                "--task-id",
                "GI-TEST-INCOMPLETE",
                "--title",
                "Unknown edit",
                "--objective",
                "",
                "--context",
                "Need to edit something later",
                "--task-kind",
                "ARTIFACT_EDIT",
                "--targets-explicitly-supplied",
                "false",
                "--change-explicitly-supplied",
                "false",
                "--human-approval-required",
                "false",
                "--human-approval-granted",
                "false",
                "--resume-instruction",
                "Wait for clarification",
            ]
        )
        incomplete = json.loads(Path(out["record"]).read_text(encoding="utf-8"))
        expected_missing = {
            "exact_target_artifacts_or_supplied_identifiers",
            "exact_requested_change_or_bounded_objective",
            "authorized_scope",
            "do_not_reopen_or_settled_decision_boundaries",
            "expected_output_or_completion_condition",
        }
        results.append(("incomplete_waits_for_input", incomplete["status"] == "WAITING_FOR_INPUT" and incomplete["task_completeness"]["human_clarification_required"] is True and set(incomplete["task_completeness"]["missing_requirements"]) == expected_missing))

        out = jrun(
            [
                "create",
                "--queue-dir",
                str(queue_dir),
                "--task-id",
                "GI-TEST-BLOCKER",
                "--title",
                "Blocked edit",
                "--objective",
                "Apply exact update",
                "--context",
                "Bounded task",
                "--task-kind",
                "ARTIFACT_EDIT",
                "--targets-explicitly-supplied",
                "true",
                "--change-explicitly-supplied",
                "true",
                "--completion-condition",
                "Updated file reviewed",
                "--input",
                "target.md",
                "--authorized-work",
                "Change heading only",
                "--do-not-reopen",
                "Body text",
                "--human-approval-required",
                "false",
                "--human-approval-granted",
                "false",
                "--blocker",
                "Need source file",
                "--resume-instruction",
                "Resume after source file arrives",
            ]
        )
        out = jrun(["validate-completeness", out["record"]])
        results.append(("blocker_precedence", out["status"] == "WAITING_FOR_INPUT"))

    report = {
        "passed": sum(1 for _, passed in results if passed),
        "total": len(results),
        "results": [{"name": name, "pass": passed} for name, passed in results],
    }
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
