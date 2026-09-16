# Neverlost Review Model

Use this reference to select review lanes, preserve gate distinctions, and produce consistent checkpoints.

## Core process

1. **Intake and Preserve** — bring material in without changing the original record.
2. **Classify** — assign each item a role before using it.
3. **Synthesize** — create an applied output that answers a real question.
4. **Index Evidence** — expose the source backbone so it can be checked.
5. **Review Alignment** — compare the output with evidence, audience, and intended purpose.
6. **Clean and Version** — improve the output without erasing useful alternatives or source history.
7. **Checkpoint** — document status, boundaries, known gaps, and the exact next step.
8. **Approve, Template, Retest** — promote only reviewed work, extract structure after proof, and test it again.

Stable core, flexible application: applied work may use the Neverlost framework without silently rewriting its governing principles.

## Authority order

Apply this hierarchy without allowing a lower layer to silently override a higher one:

1. safety, privacy, legal/medical scope, and explicit third-party-authority boundaries;
2. the user's current task authorization and explicit exclusions;
3. current controlling governance, design, lane, and approval-gate documents;
4. original source records and authoritative external documents;
5. explicitly approved Neverlost outputs;
6. review-ready or candidate outputs;
7. working drafts, derived summaries, examples, and templates.

Task authorization controls what Codex may do. It does not turn user guidance, a draft, or a Neverlost synthesis into external factual authority.

## Review lanes

| Lane | Question | Typical output | Does not establish |
| --- | --- | --- | --- |
| Authority/source set | What is authorized, controlling, current, missing, or conflicting? | source manifest, authority map, staleness/conflict note | factual correctness of the final prose |
| Role/boundary | Does the artifact stay within the speaker's and recipient's proper role? | boundary findings, required/soften/acceptable classifications | provider, counselor, agency, legal, or funding approval |
| Current facts/evidence | Is each material claim supported and correctly attributed? | claim ledger, evidence map, gaps/unverified list | broader substantive quality or operational approval |
| Substantive alignment | Does the content answer the real question accurately and effectively? | substantive review, revision plan, approved candidate | visual readiness or production lock |
| Clean/version | Were authorized changes applied without erasing history or alternatives? | new version, focused change log | human approval merely because edits succeeded |
| Formatting/visual QA | Is the artifact usable, readable, consistent, correctly branded, and print-safe? | render proof, scorecard, patched artifact | source accuracy or substantive approval |
| Human review/approval | Has the authorized human accepted this bounded artifact or decision? | explicit approval record and new status | operational use beyond the approved scope |
| Acceptance test | Does an approved component behave correctly on a bounded test? | acceptance record with deviations and result | operational approval or generalized reliability |
| Operational approval | May the tested component enter real use under stated controls? | explicit operational-use decision | unrestricted automation or future scope expansion |

## Sequencing rules

- Start with authority and source custody whenever inputs or versions are uncertain.
- Start substantive work with role/boundary review when an external actor's authority could be implied.
- Complete evidence classification before formalizing medical, functional, work-history, disability, legal, benefits, or portfolio claims.
- Keep current technical skill separate from developing skill in vocational materials.
- Perform formatting/visual QA after substantive text stabilizes, but do not treat polish as approval.
- Run acceptance testing only after the input set, task, evaluator criteria, and pre-build gate are approved.
- Require a separate explicit decision for operational use after an acceptance-test pass.

## Status model

Prefer descriptive, machine-readable uppercase statuses. Include the artifact, stage, disposition, and boundary when helpful.

Common visual statuses:

- `NEEDS_VISUAL_QA_PATCH`
- `VISUAL_QA_PATCH_APPLIED_RERENDERED`
- `READY_FOR_USER_REVIEW`
- `NEEDS_USER_REVIEW_FOR_LAYOUT_EXCEPTION`

Common semantic distinctions:

- `DRAFT_READY_FOR_REVIEW` — review has not yet occurred.
- `REVIEW_COMPLETED_REVISION_REQUIRED` — review occurred; blocking changes remain.
- `REVISIONS_COMPLETED_FOR_REVIEW` — authorized revisions were applied; human review remains.
- `APPROVED` — an authorized human explicitly approved the bounded artifact.
- `ACCEPTANCE_TEST_PASSED_PENDING_OPERATIONAL_APPROVAL_REVIEW` — the test passed; operational use remains unauthorized.
- `OPERATIONAL_USE_APPROVED` — use is authorized only within the recorded scope and controls.
- `PARKED` — no automatic next action is authorized.

Never convert `READY_FOR_USER_REVIEW`, `REVIEWED`, or `ACCEPTANCE_TEST_PASSED` into `APPROVED` by implication.

## Checkpoint schema

Use a compact checkpoint with these fields:

```markdown
# <Artifact> Checkpoint

As-of date: YYYY-MM-DD
Operating timezone: America/Denver
Status: `<MACHINE_READABLE_STATUS>`

## Scope completed
- ...

## Authorized sources and controlling standards
- ...

## Findings disposition
- Revision required: ...
- Revision recommended: ...
- Acceptable/preserved: ...

## Changes made
- ...

## Boundaries preserved
- No third-party approval implied.
- No conclusion beyond the authorized sources.
- No operational use or production lock unless explicitly approved.

## Known gaps / conflicts / unverified areas
- ...

## Exact next authorized step
- ...

## Still unauthorized
- ...
```

## Change-log minimum

Record:

- prior and new artifact versions;
- each material change or grouped mechanical change;
- reason for the change;
- controlling source, review finding, or standard;
- accepted content intentionally preserved;
- scope not touched;
- resulting status.

## Report-standard discovery anchors

Locate the current versions of these sources before creating or revising a covered Neverlost report. An explicitly superseding source controls over these version anchors.

- `NEVERLOST_REPORT_STYLE_GUIDE_v0_1.md`
- `NEVERLOST_REPORT_DESIGN_TOKENS_v0_1.json`
- `NEVERLOST_REPORT_COMPONENTS_v0_1.md`
- `NEVERLOST_REPORT_RENDERING_RULES_v0_1.md`
- `NEVERLOST_REPORT_PREFLIGHT_CHECKLIST_v0_1.md`
- `NEVERLOST_REPORT_TEMPLATE_USAGE_NOTES_v0_1.md`
- `Visual_QA/NEVERLOST_REPORT_VISUAL_QA_PROTOCOL_v0_1.md`
- `Visual_QA/NEVERLOST_REPORT_VISUAL_REFERENCE_SET_v0_1.md`
- `Visual_QA/NEVERLOST_REPORT_PREFLIGHT_SCORECARD_v0_1.md`
- `Visual_QA/NEVERLOST_REPORT_THUMBNAIL_PROOFING_WORKFLOW_v0_1.md`
- `Visual_QA/NEVERLOST_REPORT_STYLE_REGRESSION_RULES_v0_1.md`
- `NEVERLOST_REPORT_VISUAL_QA_FAILURE_HANDLING_PROTOCOL_v0_1.md`
- `NEVERLOST_REPORT_STANDARD_ENFORCEMENT_PATCH_v0_2_EXECUTION_MODE_RECONCILIATION.md`
- `00_Workspace_Architecture/Codex_Operating_Rules/CODEX_EXECUTION_MODE_PROTOCOL_v0_1.md`

Normal covered report builds require a style check, design-token check, approved-logo check, readability/font-size check, spacing/layout check, visual proof, QA scorecard, and change log.

## Governing maxims

- Preserve before you understand.
- Drafts are not gold standards.
- Templates come after proof.
- The newest version is not automatically the best version.
- Summarize, reference, and route. Do not reproduce the archive.
- Execution Mode changes the output bundle, not the quality standard.
- If standards answer a QA failure, patch and rerender. If judgment is required, stop and ask.
