# Reusable Codex Skills

A curated employer-facing collection of reusable Codex skills and governed AI workflow methods developed through Neverlost Systems projects.

The goal of this repository is discoverability: the canonical project repositories preserve full lineage and implementation context, while this repository gives reviewers one place to inspect the reusable methods themselves.

## Skills

| Skill | Purpose | Evidence / source status |
| --- | --- | --- |
| [`governed-project-development`](skills/governed-project-development/SKILL.md) | Coordinates bounded software development across sessions and agents while preserving authority, accepted product meaning, verification, human acceptance, and durable handoff. | Current v0.3 method was human-accepted after structural and forward-validation review. |
| [`governor-intake`](skills/governor-intake/SKILL.md) | Captures bounded deferred work without executing it, preserving scope, settled decisions, do-not-reopen constraints, completeness, human approval, and execution-time capacity gates for later resume. | Recovered installed v0.1.2 package includes the skill instructions, Python implementation, and durable task-record contract. |
| [`neverlost-review-workflow`](skills/neverlost-review-workflow/SKILL.md) | Governs document and artifact review through source classification, evidence checks, versioning, QA, checkpoints, and explicit approval gates. | Mirrored from the public Full Human Pathway repository. |
| [`full-human-pathway`](skills/full-human-pathway/SKILL.md) | Organizes complex cross-system information into bounded pathways, responsible lanes, dependencies, evidence gaps, and next actions without replacing professional authority. | Mirrored from the public Full Human Pathway repository and exercised with synthetic validation fixtures. |
| [`capacity-output`](skills/capacity-output/SKILL.md) | Records completed work together with the conditions, constraints, accommodations, variability, and recovery cost required to produce it. | Mirrored from the public Full Human Pathway repository and exercised with synthetic validation fixtures. |
| [Governed Workspace Builder](skills/governed-workspace-builder/README.md) | Creates controlled, resumable project workspaces with source registration, SHA-256 custody, review states, checkpoints, promotion gates, and deterministic validation. | Verified portfolio brief and reproducibility evidence are preserved here; the original installable skill/tool source is not duplicated until its exact source package is recovered. |

## Design pattern

Across these skills, the recurring pattern is:

`PRESERVE → CLASSIFY → BOUND → ACT → VERIFY → REVIEW → PRESERVE`

The methods are designed to make AI-assisted work more inspectable without silently turning context, code existence, test success, or model output into human authority.

## Why this repository exists

These skills originated inside larger Neverlost projects. Leaving them only inside those repositories made the reusable work difficult to discover. This repository is intentionally a curated mirror/index, not a claim that each skill originated here.

Where an exact source is available, the source is mirrored without changing its substantive rules. Where only portfolio/test evidence is currently recoverable, that limitation is stated explicitly instead of reconstructing a supposedly canonical skill from memory.

## Related public project

The historical Build Week skills and their synthetic validation environment remain available in the public [`Neverlost-full-human-pathway`](https://github.com/Neverlost-AI/Neverlost-full-human-pathway) repository.

## Author

Jeff Summerhays — Neverlost Systems
