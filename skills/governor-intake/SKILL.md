---
name: governor-intake
description: Capture and completeness-check a supplied, bounded task for deferred execution while preserving scope, settled decisions, do-not-reopen constraints, inputs, blockers, and independent human-approval and capacity gates. Use when the user says to intake, queue, log, or save work for later without executing it. Do not use to perform the deferred task.
---

# Governor Intake

Use Intake as a low-cost state-registration operation. The user supplies the relevant context; record it without rediscovering the project, then stop.

## Intake invariants

- Do not open, review, summarize, edit, test, build, deploy, or call external systems for the referenced task.
- Do not scan a repository or reconstruct broader strategy when the supplied context is sufficient.
- Do not improve or reinterpret settled decisions, do-not-reopen boundaries, or requested scope.
- Treat task completeness, human authorization, and capacity as independent gates. Neither implies another.
- Store durable capacity as `NOT_OBSERVED`. A timestamped human observation is audit evidence only and must not become a durable PASS, FAIL, AVAILABLE, or `WAITING_FOR_RESET` determination.
- Intake never performs substantive execution. A resume preparation may establish eligibility, but a separate authorized execution process must perform the task.
- Never infer, guess, or discover a missing artifact identity or requested change. Preserve the partial task and require human clarification.

## Capture flow

1. Use only the task context and artifact references supplied by the user.
2. Record the minimum resumable state: title, objective, inputs, supplied context, authorized work, settled decisions, do-not-reopen boundaries, expected completion condition, human-review items, blockers, approval requirement/state, `capacity_state: NOT_OBSERVED`, the execution-time capacity-check requirement, and a short resume instruction.
3. For an artifact edit, mark `ARTIFACT_EDIT` and set the explicit-supply flags true only when the human actually supplied the exact artifact reference and bounded change. Pass those references as opaque strings; the script never opens them.
4. Create the record with `scripts/governor_intake.py create`. The script persists `task_completeness`; incomplete artifact tasks remain preserved in `WAITING_FOR_INPUT` with visible missing requirements.
5. Preserve any observable usage indicator exactly as displayed. If none is available, record `NOT_OBSERVED`; never infer zero usage.
6. Return only the record path, current lifecycle state, missing requirements if any, durable capacity state/check requirement, and approval state. Stop.

The durable record schema and state meanings are in [references/task-record.md](references/task-record.md). Read that reference when creating, updating, or resuming a record.

## Defer and resume

- Use `evaluate` to inspect whether the independent gates are satisfied.
- Use `validate-completeness` to persist the current completeness result on an existing record. It does not fill missing information.
- Use `set-gates` only for explicit human approval; approval is durable.
- Use `record-capacity-observation` to retain a human-supplied capacity observation for audit analysis. It must not change readiness.
- Use `prepare-resume` to emit a bounded resume envelope and measure reconstruction overhead. It must not execute the task.
- `READY_TO_EXECUTE` means only that durable completeness, input, blocker, and approval conditions are satisfied. It does not mean capacity has passed and it does not start execution.
- A transition to `EXECUTING` must receive a fresh capacity check in that same execution transition. The check may be human-supplied until Governor can observe capacity independently; omit percentage when none was supplied.
- An incomplete artifact task takes precedence over approval and capacity and remains `WAITING_FOR_INPUT` until the human supplies the missing execution contract.
- Lifecycle transitions beyond readiness are recorded only from an external execution or verification event.

## Exit condition

After Intake, reply compactly with: task captured, saved record path, lifecycle state, missing requirements if any, human-approval state, `capacity_state`, and whether an execution-time capacity check is required. Do not continue into planning or execution.
