---
name: capacity-output
description: Record useful output together with the conditions, accommodations, constraints, variability, and recovery cost that made it possible. Use when documenting capacity-aware work sessions, accessibility effects, pacing, episodic productivity, recovery needs, portfolio activity, vocational evidence, or when a successful task could be misread as proof of full-time capacity, work readiness, disability status, or sustainable employment.
---

# Capacity & Output

Make work visible without separating the output from the human cost and conditions required to produce it.

## Establish the observation boundary

1. Define the activity, observation window, source, and intended use.
2. Distinguish observed output, user-reported effects, external records, and derived interpretation.
3. Treat one session or short period as an observation, not a durable capacity conclusion.

Do not infer full-time capacity, work readiness, disability status, sustainable employment, or medical conclusions.

## Record the capacity context

Capture when available:

- date, duration, and available working window;
- task type and concrete output;
- position, device, workspace, assistance, and accommodations;
- pain, fatigue, cognitive, sensory, autonomic, or other constraints;
- breaks, interruptions, task switching, and abandoned work;
- immediate effect and delayed recovery cost;
- repeatability status: `OBSERVED_ONCE`, `VARIABLE`, `REPEATABLE_WITHIN_CURRENT_EVIDENCE`, or `NOT_YET_KNOWN`;
- source type and confidence for each material statement.

## Interpret conservatively

- Describe demonstrated skill separately from sustainable capacity.
- State what the accommodation changed without claiming it removed the underlying limitation.
- Count recovery time and delayed effects as part of the work context.
- Preserve uncertainty when repeatability has not been tested.
- Route medical, benefits, disability, vocational, funding, or employer conclusions to the proper authority.

## Minimum output contract

Return:

1. observation purpose and window;
2. output achieved;
3. conditions and accommodations;
4. limiting factors and interruptions;
5. immediate and delayed recovery cost;
6. repeatability status;
7. source labels and uncertainty;
8. bounded interpretation;
9. prohibited conclusions explicitly withheld;
10. exact next observation or review trigger.

Apply the `neverlost-review-workflow` when the record will support an external document, vocational packet, accessibility request, disability discussion, or public portfolio claim.

## Run the validated synthetic prototype

For an authorized synthetic demonstration, validate the record with `schemas/capacity-record.schema.json` and run `python3 scripts/run_demo_validation.py` with the exact case specification, fixture manifest, and output directory. Treat any failed recovery-cost, repeatability, source, privacy, or prohibited-claim check as gate-blocking.

Keep the primary capacity observation tied to the source that actually reports the activity. Do not silently merge a separate occupational-therapy simulation, provider statement, or vocational record into the client observation count; carry those sources through their proper lanes and bridges instead.

The validated synthetic fixtures are `FHP-SYNTH-001` and `FHP-SYNTH-002`. Automated tracking, trend analysis, work-capacity prediction, real-client use, external distribution, acceptance-test claims, and operational use remain unauthorized.
