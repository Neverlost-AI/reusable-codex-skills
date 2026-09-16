---
name: neverlost-review-workflow
description: Apply the established Neverlost governed review process to documents, reports, PDFs, packets, presentations, manuscripts, context exports, templates, and workflow outputs. Use when reviewing, revising, cleaning, versioning, checkpointing, approving, formatting, visually QA-ing, or preparing a Neverlost artifact; when the user asks for a boundary review, evidence review, substantive review, review-only draft, production lock, acceptance test, operational approval, Governance Mode, or Execution Mode; or when a non-Neverlost artifact should be handled through the user's Neverlost review method.
---

# Neverlost Review Workflow

Apply the operating principle: preserve source truth, make the functional reality visible, and promote only reviewed work into repeatable patterns.

## Establish the task

1. Identify the artifact, lane, audience, real question, requested action, and current authority status.
2. Default to **Governance Mode** for review, revision planning, controlled patches, checkpoints, and approval gates.
3. Enter **Execution Mode** only when the user clearly requests a finished artifact under that mode. Execution Mode changes the output bundle, not the quality standard.
4. Do not infer permission to revise merely from a request to review. Diagnose and report unless revision or creation is authorized.
5. Load only the minimum source set needed for the current gate. Summarize, reference, and route; do not reproduce the archive.
6. In Governance Mode, resolve standards-answered defects autonomously for up to three review/patch/checkpoint cycles. Stop for a real user decision, missing authority, or an issue outside the active scope.

## Protect authority and custody

- Preserve original records unchanged. Create a new version or working copy for authorized edits.
- Classify every input before using it: original evidence, user guidance, governing standard, approved output, draft/candidate, template, checkpoint, or derived synthesis.
- Keep evidence and guidance separate. Records support factual claims; user guidance controls purpose, emphasis, and personal intent.
- Treat explicit user instructions as task authority, not as authority to change source facts or imply third-party approval.
- Prefer current controlling sources and explicitly approved versions. Do not assume the newest draft is the best or authoritative version.
- Record stale, conflicting, missing, and unverified material. Do not silently harmonize conflicts.
- Preserve useful alternatives and rejected candidates when their status matters. Do not overwrite source-lane originals with portfolio copies.

## Choose review lanes

Use only the lanes required by the artifact, but keep their findings and gates separate. Read [references/review-model.md](references/review-model.md) for the lane definitions, sequencing rules, status language, and checkpoint schema.

Use this usual order when multiple lanes apply:

1. authority and source-set review;
2. role/boundary review;
3. current-facts and evidence review;
4. substantive alignment review;
5. authorized revision and clean versioning;
6. formatting and visual QA;
7. checkpoint and human review;
8. acceptance testing, if separately authorized;
9. operational approval, if separately authorized.

Do not collapse these gates. A clean draft is not substantively approved. A visually polished report is not factually approved. An acceptance-test pass is not operational approval.

## Conduct the review

1. State the bounded review question and exclusions before analyzing.
2. Build a claim/source map when factual or evidentiary statements matter. Label claims as provider/source-supported, user-reported, derived, conflicting, stale, or unverified.
3. Check role boundaries before prose polish when the artifact addresses providers, counselors, agencies, evaluators, legal actors, or other external decision-makers.
4. Review alignment among the evidence, the artifact's purpose, its audience, and the action it requests.
5. Classify findings as:
   - **revision required** — inaccurate, unsupported, boundary-crossing, materially misleading, or gate-blocking;
   - **softening/revision recommended** — defensible but overstated, ambiguous, poorly framed, or less effective than it could be;
   - **acceptable as written** — supported, bounded, and fit for purpose.
6. Preserve acceptable language during an authorized patch. Change only what the active review authorizes.
7. Create a change log for substantive or formatting changes. Record what changed, why, what remained untouched, and which source or standard controlled the decision.

## Handle domain boundaries

- For medical, functional, disability, legal, benefits, or vocational claims, distinguish records, provider conclusions, user reports, and Neverlost synthesis. Do not create diagnoses, eligibility conclusions, work-capacity conclusions, funding approvals, counselor approval, or other third-party decisions.
- For Modern Paradox work, preserve the literary/philosophical voice and the manuscript's own authority. Do not turn it into a Neverlost pitch, medical report, or disability argument.
- For review-only vocational materials, do not imply that a job is secured, full-time capacity exists, VR has approved services, funding is approved, an IPE is final, or production is locked.
- For context exports and clean-chat tests, enforce the exact authorized input set and bounded task. Treat extra files as deviations when appropriate; do not use them merely because they are present.

## Apply report and visual standards

For a covered Neverlost report, PDF, clinical support memo, provider-facing summary, VR document, care-coordination output, or report-style portfolio artifact:

1. Locate and load the current controlling Neverlost report standards before building or revising. Use the filenames in [references/review-model.md](references/review-model.md) as discovery anchors and honor any explicit superseding version.
2. Use only approved or explicitly candidate-approved logo assets. Do not invent, redraw, simplify, or substitute marks.
3. Render and inspect every page or slide at a useful reading size. Check typography, readability, spacing, alignment, overflow, clipping, page breaks, tables, visual hierarchy, logo use, and print behavior.
4. In normal workflow, require the finished artifact, visual proof, QA scorecard, and change log before marking it ready for user review.
5. If a visual failure is answered by the standards, patch and rerender automatically. Repeat for up to three failed QA cycles.
6. Ask the user only when the remaining issue requires real judgment, an exception, a new visual direction, missing authority, or content changes outside the authorized scope.
7. After three failed cycles, stop, identify the blocker precisely, preserve the best valid artifact, and set a blocked or needs-user-review status. Never lower the quality bar to declare success.

If a required controlling standard or approved logo asset cannot be located, do not improvise or declare the artifact ready. Name the exact missing source; for a missing logo, create `APPROVED_LOGO_ASSET_MISSING_NOTE.md` when the active task authorizes workflow files.

## Checkpoint every controlled stage

End a bounded stage with a checkpoint that records:

- artifact and version;
- as-of date and operating timezone when date-sensitive;
- current machine-readable status;
- authorized source set and controlling standards;
- reviews completed and findings disposition;
- changes made and files left untouched;
- human-review and third-party-authority boundaries;
- known gaps, conflicts, and unverified areas;
- exact next authorized step;
- actions that remain unauthorized.

Use `READY_FOR_USER_REVIEW` only after the applicable content and visual gates pass. Use `APPROVED` only after explicit human approval. Promote to a template only after a reviewed artifact proves the pattern, then retest the template on a distinct use case.

## Deliver proportionately

- For review-only requests, lead with the verdict, blocking findings, preserved strengths, boundaries, and exact next step.
- For authorized revisions, provide the revised version plus change log and checkpoint.
- For finished report builds, include the required deliverable set unless valid Execution Mode instructions narrow the bundle.
- Keep abandoned drafts, failed attempts, and source-only material out of curated portfolio lanes. Include only finished or explicitly approved work there.
