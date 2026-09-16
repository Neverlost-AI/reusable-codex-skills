# Governor Intake task record

## Required record fields

- `task_id`, `title`, `objective`, and `status`
- `inputs`: supplied artifact references only; Intake does not open them
- `supplied_context`: concise authoritative context from the user
- `authorized_work`: work a later execution process may perform
- `settled_decisions`: decisions already made
- `do_not_reopen`: explicit excluded scope and closed decisions
- `human_review_items`: issues that require a human decision rather than reinterpretation
- `human_approval_required` and `human_approval_granted`
- `capacity_state`: durable value `NOT_OBSERVED`
- `capacity_check_required_at_execution`: always `true` in Intake v0.1.x
- `capacity_observations`: timestamped historical observations with explicit source and optional supplied percentage
- `blockers` and `resume_instruction`
- `task_completeness`: task kind, explicit-supply attestations, expected output/completion condition, missing requirements, and human-clarification requirement
- `intake_measurement` and `resume_measurement`

## Artifact-task completeness

For `ARTIFACT_EDIT`, Intake requires all of the following before execution eligibility:

- exact target artifacts, filenames, or supplied identifiers in `inputs`, explicitly supplied by the human;
- an explicitly supplied exact requested change or bounded `objective`;
- non-empty `authorized_work`;
- at least one `do_not_reopen` or `settled_decisions` boundary;
- a non-empty expected output or completion condition.

Missing items are recorded in `task_completeness.missing_requirements`, with `human_clarification_required: true`. Intake must leave missing targets and changes blank or partial; it must not infer them or scan for likely substitutes.

## Lifecycle states

`CAPTURED` -> `INTAKE_COMPLETE` -> one of `HUMAN_APPROVAL_REQUIRED`, `WAITING_FOR_INPUT`, or `READY_TO_EXECUTE` -> `EXECUTING` -> `VERIFIED` -> `COMPLETE`. `WAITING_FOR_RESET` is retained only for legacy compatibility and is not assigned from a historical capacity observation.

Completeness and human approval remain durable independent gates. Capacity remains an independent but transient execution-time gate.

State-selection precedence for resume preparation is:

1. incomplete execution contract -> `WAITING_FOR_INPUT`
2. known blockers -> `WAITING_FOR_INPUT`
3. required approval not granted -> `HUMAN_APPROVAL_REQUIRED`
4. all durable conditions satisfied -> `READY_TO_EXECUTE`, with a fresh capacity check still required at execution

`READY_TO_EXECUTE` is durable-prerequisite readiness, not a capacity PASS or execution. Intake and resume preparation must always report `execution_performed: false` and `capacity_check_required_at_execution: true`.

## Capacity observations

Intake never persists a transient capacity PASS or FAIL. `capacity_state` remains `NOT_OBSERVED`. A human-supplied percentage may be appended to `capacity_observations` with its timestamp and source, but it cannot affect lifecycle selection or future execution eligibility. A fresh capacity check must accompany the transition to substantive execution; it becomes audit history only as part of that execution event.

## Lightweight measurements

Intake records elapsed milliseconds, supplied payload bytes, written record bytes, and any user-supplied before/after usage display. Resume preparation records load/envelope time, record bytes, envelope bytes, and explicitly supplied reconstruction actions. These observations do not demonstrate savings or efficiency.
