# Governor Intake

A recovered reusable Codex skill for capturing bounded work for later execution without silently turning intake into execution.

## Package

- `SKILL.md` — operating instructions for intake, defer, resume, and execution boundaries.
- `scripts/governor_intake.py` — deterministic Python implementation, schema version `governor-intake-v0.1.2`.
- `references/task-record.md` — durable task-record contract and lifecycle semantics.
- `tests/test_governor_intake_recovery.py` — fresh recovery acceptance suite.

## What it enforces

Governor Intake keeps task completeness, human approval, and capacity as separate gates. It preserves settled decisions and explicit `do_not_reopen` boundaries, blocks incomplete artifact edits for human clarification, keeps durable capacity at `NOT_OBSERVED`, and requires a fresh capacity check in the transition that begins substantive execution.

## Validation

The recovered package was exercised again on September 15, 2026 with the included synthetic recovery acceptance suite.

**Result: 13/13 checks passed.**

Covered behaviors include:

- Intake remains non-executing.
- Capacity remains `NOT_OBSERVED` during intake.
- Settled decisions and do-not-reopen boundaries are preserved.
- Human approval is enforced independently.
- Historical capacity observations do not create readiness.
- Resume preparation stays bounded and non-executing.
- Execution is rejected without a fresh capacity check.
- A supplied fresh capacity check permits the authorized execution transition.
- The lifecycle can advance through `EXECUTING -> VERIFIED -> COMPLETE`.
- Incomplete artifact tasks remain `WAITING_FOR_INPUT` with explicit missing requirements.
- Blocking input takes precedence over readiness.

Run the current recovery suite with:

```bash
python skills/governor-intake/tests/test_governor_intake_recovery.py
```

## Evidence boundary

This is a recovered package, not a claim that the original development directory was preserved byte-for-byte. Historical evidence also records an earlier unit-test run of 10/11 in which the remaining assertion was stale relative to a task record that had legitimately advanced to `COMPLETE`. The included 13-check suite is a fresh recovery acceptance test against the recovered implementation and contract, not a rewrite of that historical test suite.
