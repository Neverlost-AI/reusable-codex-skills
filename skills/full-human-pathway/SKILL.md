---
name: full-human-pathway
description: Organize a person's desired life direction, current reality, responsible systems, dependencies, and bounded next actions into a whole-person pathway without replacing professional authority. Use for cross-system intake, pathway-stage statements, healthcare-to-vocational bridges, vocational-planning preparation, accessibility and resource mapping, recipient-specific handoffs, or any request to connect healthcare, daily living, training, vocational rehabilitation, benefits, research, and employment lanes.
---

# Full Human Pathway

Create a bounded bridge plan that keeps the person at the center while preserving the separate authority of each system.

## Establish the planning boundary

1. Define the person, purpose, intended audience, requested action, exclusions, and authorized source set.
2. Use synthetic or explicitly authorized information only.
3. Separate source records, external conclusions, user-reported experience, user guidance, and Neverlost synthesis.
4. Route consequential conclusions to the proper authority instead of filling gaps with inference.

Do not diagnose, determine work capacity, decide eligibility, approve services or funding, promise employment, or imply operational readiness.

## Map the pathway

Use only the lanes relevant to the current question:

- life direction;
- health and function;
- daily living and support;
- resources and capacity;
- healthcare;
- education and training;
- vocational rehabilitation and employment;
- environment and accessibility;
- system relationships.

For each active lane, record the current stage, what may proceed now, what remains premature, and the review trigger. Stages are planning descriptions, not judgments about worth, prognosis, eligibility, or permanent capacity.

## Create bridge records

Each active bridge must identify:

- need or opportunity;
- desired outcome;
- responsible lane;
- proper authority;
- existing evidence and source type;
- missing information;
- next bounded action;
- dependency or parallel work;
- owner, status, and review trigger.

## Minimum output contract

Return:

1. purpose, audience, scope, and exclusions;
2. client-defined direction;
3. relevant lane map;
4. pathway-stage statement;
5. active bridge records;
6. evidence gaps, conflicts, and uncertainty;
7. minimum-necessary sharing note;
8. exact next authorized step;
9. actions that remain unauthorized;
10. a machine-readable checkpoint status.

Default a completed draft to `READY_FOR_USER_REVIEW`, never `APPROVED`. Apply the `neverlost-review-workflow` before any external-facing packet or approval claim.

## Run the validated synthetic prototype

For an authorized synthetic demonstration, use the shared repository contracts:

- validate intake with `schemas/intake.schema.json`;
- validate pathway output with `schemas/pathway-plan.schema.json`;
- run `python3 scripts/run_demo_validation.py` with the exact case specification, fixture manifest, and output directory;
- inspect the generated validation report before reporting packet success;
- for `FHP-SYNTH-002`, also run `python3 scripts/score_stage3_retest.py` and preserve the locked baseline separately from any patched packet.

The validated synthetic fixtures are `FHP-SYNTH-001` and `FHP-SYNTH-002`. Stage 3 demonstrates bounded transfer across two fictional cases; it does not authorize real-client use, external distribution, marketplace release, acceptance-test claims, or operational use.
