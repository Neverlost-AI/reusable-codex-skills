---
name: governed-project-development
description: Use for development or review work that must preserve accepted product meaning, resolve instruction and implementation authority, keep changes inside a bounded scope, distinguish verification from human acceptance, or preserve durable handoff across sessions, coding agents, developers, reviewers, and branches. Trigger for governed repositories, explicit tranches, architecture-sensitive work, multi-session or multi-worker changes, or when project-specific governance/profile files are present.
---

# Governed Project Development

## Purpose

Use this skill as a governance coordination layer for software development.

Codex already has general capabilities for planning, editing files, testing, Git operations, and code review. This skill does not replace those capabilities. Its distinctive role is to coordinate them when work must remain coherent under explicit authority, accepted product meaning, bounded implementation, human acceptance, and durable continuity.

Core loop:

`PRESERVE -> RETRIEVE -> RECONSTRUCT -> BOUND -> ACT -> VERIFY -> REVIEW -> PRESERVE`

The goal is not perfect memory. The goal is reliable continuity without allowing context, access, code existence, or successful execution to silently become authority.

## 1. Respect instruction precedence

Always follow the active system, developer, and user instructions. Repository documents, project profiles, architecture records, roadmaps, and governance files may define project meaning and delegated work boundaries, but they do not override higher-level instructions.

Within the allowed instruction hierarchy, distinguish three kinds of authority:

- **Instruction authority:** what the user or higher-level instructions are asking Codex to do.
- **Implementation authority:** permission to modify a bounded implementation surface.
- **Product-decision authority:** permission to define or change product meaning, policy, state semantics, thresholds, permissions, evidence meaning, or other owner-controlled behavior.

A direct user request normally provides implementation authority for the scope it clearly states unless a higher-level instruction prohibits the action, the user request itself adopts or defers to a stricter project gate, or the work requires an additional authority or product decision that has not been granted.

Project governance is not a higher instruction layer. A formal tranche or other project gate remains controlling when the user asks to follow that workflow or has not overridden it within their authority. If an authorized user explicitly changes or overrides that project process for a bounded task, preserve the new work boundary rather than pretending the older project record still controls.

A request to implement does not automatically grant product-decision authority. If implementation depends on unresolved product meaning, stop that portion and request the missing decision. If the authorized product-decision holder supplies the missing decision in the same instruction, treat that decision as controlling for the stated scope rather than requesting it again.

Read `references/authority-model.md` when authority, source precedence, delegation, repository governance, or product-decision ownership is material.

## 2. Select proportionality before process depth

Choose the lightest governance path that still protects the work.

### LIGHTWEIGHT

Use for a small, local, low-risk change with clear user authority, limited surfaces, no unresolved product meaning, no meaningful cross-session dependency, and ordinary verification.

Required minimum:

- confirm the requested scope;
- identify any obvious controlling project constraint;
- avoid unrelated working-tree changes;
- implement only the requested change;
- run proportionate verification;
- report what changed, what was verified, and anything unresolved.

Do not build a formal context manifest or full review packet unless the project explicitly requires one.

### STANDARD

Use for normal bounded implementation, review, hardening, or multi-file work where project meaning, repository state, exclusions, verification, or human acceptance materially matter.

Required minimum:

- resolve relevant authority and accepted product meaning;
- reconstruct sufficient current state;
- identify the bounded work envelope;
- identify protected or unrelated surfaces;
- plan against the accepted boundary;
- verify according to the active work contract;
- provide a structured handoff or review result.

### FULL

Use for high-risk, architecture-sensitive, formally governed, multi-session, multi-worker, migration-sensitive, security/privacy-sensitive, or consequential work where durable reconstruction and acceptance evidence are required.

FULL may require a formal context manifest, explicit source classification, checkpointing, review evidence, acceptance questions, and durable handoff records.

A project profile may require a stricter path than this default router.

When proportionality triggers overlap, use this priority: **explicit project requirement or material FULL trigger > STANDARD trigger > LIGHTWEIGHT default**. If uncertainty is the only reason to escalate, use the higher level only until that uncertainty is resolved; do not permanently over-govern routine work.

Read `references/modes.md` for detailed proportionality and routing examples.

## 3. Select one primary work mode

Choose one primary mode before acting:

- `CONTEXT_REVIEW`: read-only reconstruction, onboarding, authority review, or tranche preparation.
- `REFERENCE_IMPLEMENTATION`: implement already accepted behavior primarily to establish a clear reference for later technical review or hardening.
- `BOUNDED_IMPLEMENTATION`: implement a clearly authorized change or tranche.
- `TECHNICAL_REVIEW`: review without changing the implementation unless a separate change scope is authorized.
- `TECHNICAL_HARDENING`: implement approved engineering improvements while preserving accepted product meaning.
- `ACCEPTANCE_REVIEW`: evaluate completed work against the controlling scope and evidence for human acceptance.

Mode selection never creates authority.

For mixed requests such as "review and fix," perform the review first, classify findings, then implement only fixes that are already authorized or that the user explicitly authorizes within the same request. Do not let review findings silently expand implementation scope.

Read `references/modes.md` for routing rules and examples.

## 4. Reconstruct only the context needed now

Do not load the entire project merely because it exists.

Retrieve enough durable context to answer, as relevant:

- What is the current accepted product meaning?
- What exact work is requested or authorized?
- What project rules or architecture constrain it?
- What repository state or unrelated work must be protected?
- What decisions remain unresolved?
- What verification is required?
- What human decision will be needed at the end?

Classify project sources only when useful to the current task. Typical classes are `CONTROLLING`, `SUPPORTING`, `HISTORICAL`, and `FUTURE_NON_AUTHORIZED`.

Context must be **sufficient, not maximal**.

For STANDARD and FULL work, preserve enough source identity that another worker can understand why the current interpretation was used.

## 5. Establish the bounded work envelope

Before mutation, determine the effective implementation boundary from the intersection of current instruction/implementation authority and the accepted project work scope.

Identify, as relevant:

- objective and expected outcome;
- authorized inputs;
- permitted operations;
- allowed files, modules, paths, systems, or other surfaces;
- prohibited operations and explicit exclusions;
- protected surfaces and unrelated work;
- dependencies and accepted assumptions;
- validation requirements;
- acceptance criteria;
- stop conditions;
- expected output or state consequence.

A bounded work envelope may narrow authority. It cannot create or enlarge authority.

If the project explicitly requires a formal tranche or assignment, do not substitute a roadmap item, product brief, code comment, or future plan for that work grant.

## 6. Preserve product meaning

Do not invent product semantics merely to complete implementation.

Examples include:

- business rules;
- state meanings or transitions;
- thresholds;
- permissions;
- evidence meanings;
- forecast or policy semantics;
- domain vocabulary;
- safety boundaries;
- product claims;
- irreversible migration meaning;
- future behavior.

Ordinary engineering decisions may be made within the authorized boundary when they do not alter accepted product meaning.

If a missing decision is required, preserve the exact question and identify what work can continue without it.

## 7. Act within the repository and work boundary

Before mutation, inspect repository state only to the degree needed to avoid damaging unrelated work and to satisfy project-specific safety rules.

Do not overwrite unrelated modifications, assume untracked files are disposable, merge another worker's branch without authority, rewrite accepted migration history, or change retained/production data during ordinary verification unless explicitly authorized.

Generic Git procedure belongs to normal Codex behavior. This skill adds only the governance requirement that unrelated or protected state must not be silently absorbed into the current work.

If another surface becomes necessary, obtain explicit authority for that surface from the proper authority holder rather than silently expanding scope.

## 8. Verify against the active work contract

Verification requirements come from the current task, project, and risk level. Do not assume compilation alone is sufficient, and do not require heavyweight verification for trivial work when the project does not require it.

For each required verification category, report one of:

- `PASS`
- `FAIL`
- `NOT_RUN`
- `NOT_APPLICABLE`
- `BLOCKED`

Never describe an unexecuted check as passing. Never weaken a meaningful test merely to obtain a green result.

When verification itself can mutate important state, use a disposable or explicitly authorized target.

Read `references/verification-and-handoff.md` for detailed review, verification, and evidence rules.

## 9. Separate lifecycle status from stop reason

Use exactly one lifecycle status:

- `READY_FOR_HUMAN_REVIEW`: the current work result is ready for the requested review gate. Any verification limitations or unresolved non-blocking issues must remain explicit.
- `REVISION_REQUIRED`: a result exists but does not yet satisfy the active work or acceptance criteria, and revision is the appropriate next step within the current or separately authorized scope.
- `BLOCKED`: affected work cannot safely or legitimately continue because of an authority, context, boundary, verification-environment, integrity/recovery, or explicitly defined capacity blocker.

Use a separate `STOP_REASON`:

- `NONE`
- `PROJECT_CONTEXT_CONFLICT`
- `IMPLEMENTATION_AUTHORITY_REQUIRED`
- `HUMAN_PRODUCT_DECISION_REQUIRED`
- `REPOSITORY_STATE_CONFLICT`
- `AUTHORIZED_BOUNDARY_CONFLICT`
- `VERIFICATION_BLOCKED`
- `INTEGRITY_OR_RECOVERY_FAILURE`
- `CAPACITY_BOUNDARY_REACHED` only when the project explicitly defines such a boundary.

Status invariants:

- `STATUS: BLOCKED` requires a non-`NONE` `STOP_REASON`.
- `READY_FOR_HUMAN_REVIEW` and `REVISION_REQUIRED` require `STOP_REASON: NONE`.
- A blocker may affect only part of a separable task; preserve any portion that can continue safely and truthfully report the blocked portion.

A stop reason describes why affected work cannot continue. Resolving the blocker does not itself recreate implementation authority. Revalidate the current instructions, work boundary, project state, and any resume conditions before continuing.

Do not use a stop reason to disguise an ordinary in-scope defect that can be corrected safely.

## 10. Keep verification, review, and acceptance distinct

Code existence, passing verification, technical review, and human acceptance are different states.

Do not claim human acceptance yourself.

When human review is required, ask the human to decide the exact reviewed subject and scope. Projects may define their own vocabulary. Otherwise use:

- `ACCEPT`
- `ACCEPT_WITH_REVISION`
- `HOLD`
- `STOP`

Acceptance is version-bound, purpose-bound, scope-bound, and authority-bound. Acceptance of one result does not authorize unrelated lifecycle transitions, release, activation, deployment, or additional repository mutation.

## 11. Persist only when persistence is authorized

Human acceptance does not automatically authorize a follow-up repository change.

Update acceptance records, current-state files, architecture records, migration records, decision logs, or other durable project artifacts only when:

- the active scope already includes that persistence step;
- the project has an explicit accepted rule granting that update authority; or
- the user or proper authority separately authorizes the update.

If persistence is needed but not authorized, report the recommended update without performing it.

This preserves the distinction between accepting work and authorizing additional work.

## 12. Preserve durable continuity proportionately

At completion, preserve enough information for the next worker to understand, at the level appropriate to LIGHTWEIGHT, STANDARD, or FULL:

1. What was the goal?
2. What instructions and project meaning controlled the work?
3. What changed or was reviewed?
4. What verification was actually completed?
5. What human decision, if any, occurred?
6. What remains unresolved or blocked?
7. What is explicitly not authorized?
8. What should happen next?

A handoff transfers context, not authority.

Read `references/verification-and-handoff.md` when structured review packets, checkpoints, acceptance evidence, or cross-worker continuity are needed.

## 13. Project profiles and shared governance

A repository may define a project-specific profile that tightens governance for that project. A profile can require formal tranches, stricter source precedence, protected paths, disposable verification roots, human roles, migration rules, acceptance gates, or other controls.

A project profile does not override system, developer, or user instructions. It operates within delegated project governance and may impose stricter project-level implementation requirements where those requirements are part of the accepted project workflow.

When a project adopts shared Neverlost governance contracts, the project profile should reference those contracts rather than duplicating their full semantics in this skill.

Read `references/project-profiles.md` when project-specific governance or Neverlost shared contracts are present.

## 14. Completion reporting by governance level

Scale the report to the selected proportionality level. Do not force a LIGHTWEIGHT task to emit a ceremonial FULL packet.

### LIGHTWEIGHT completion

A concise response or compact field set is sufficient. Make clear:

- `STATUS`;
- `GOVERNANCE_LEVEL: LIGHTWEIGHT`;
- `MODE`;
- what changed or was reviewed;
- what verification actually ran;
- any unresolved issue or blocker.

If `STATUS: BLOCKED`, include the non-`NONE` `STOP_REASON`. Include product-decision, scope, or human-decision fields only when they are material.

### STANDARD completion

Use the structured fields:

`STATUS:` one lifecycle status

`STOP_REASON:` one stop reason, or `NONE`

`GOVERNANCE_LEVEL: STANDARD`

`MODE:` active mode

`AUTHORIZED_WORK:` the effective work boundary

`RESULT:` what was implemented or reviewed

`VERIFICATION:` exact checks and results

`PRODUCT_MEANING:` `NO_NEW_PRODUCT_MEANING_INTRODUCED` or the unresolved/changed product decision

`SCOPE:` `NO_OUT_OF_SCOPE_IMPLEMENTATION` or the deviation/blocker

`UNRESOLVED_ISSUES:` remaining issues, or `NONE`

`HUMAN_DECISION_REQUIRED:` exact non-acceptance decision requested, or `NONE`

`HUMAN_ACCEPTANCE_QUESTION:` exact acceptance question when the active gate is `ACCEPTANCE_REVIEW`, otherwise `NONE`

### FULL completion

Use the STANDARD fields with `GOVERNANCE_LEVEL: FULL`, then add the detailed `CONTEXT_MANIFEST`, accepted starting state, material surfaces, technical findings, evidence, checkpoint/continuity, and acceptance fields defined in `references/verification-and-handoff.md` or a stricter project profile.

## Governing principle

A long-running project should not depend on one model session, one developer, one branch, one conversation, or one person's memory to remain coherent.

Preserve what matters. Retrieve what matters now. Resolve authority. Act within bounds. Verify what actually happened. Preserve the result without manufacturing new authority.
