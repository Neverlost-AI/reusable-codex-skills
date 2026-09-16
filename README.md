# Reusable Codex Skills

A curated employer-facing collection of reusable Codex skills and governed AI workflow methods developed through Neverlost Systems projects.

The goal of this repository is discoverability: canonical project repositories preserve full lineage and implementation context, while this repository gives reviewers one place to inspect reusable methods, executable tooling, and validation evidence.

## Packaged skills

| Skill | Purpose | Evidence / source status |
| --- | --- | --- |
| [`governed-project-development`](skills/governed-project-development/SKILL.md) | Coordinates bounded software development across sessions and agents while preserving authority, accepted product meaning, verification, human acceptance, and durable handoff. | Current v0.3 core skill was human-accepted after 31/31 structural checks and 20/20 static forward-validation cases. The five progressive-disclosure reference modules are not mirrored here; see the directory source note. |
| [`governor-intake`](skills/governor-intake/README.md) | Captures bounded deferred work without executing it, preserving scope, settled decisions, do-not-reopen constraints, completeness, human approval, and execution-time capacity gates for later resume. | Recovered v0.1.2 package includes the skill, Python implementation, task-record contract, and a fresh recovery acceptance suite that passes 13/13 checks. |
| [`neverlost-review-workflow`](skills/neverlost-review-workflow/SKILL.md) | Governs document and artifact review through source classification, evidence checks, versioning, QA, checkpoints, and explicit approval gates. | Mirrored from the public Full Human Pathway repository. |
| [`full-human-pathway`](skills/full-human-pathway/SKILL.md) | Organizes complex cross-system information into bounded pathways, responsible lanes, dependencies, evidence gaps, and next actions without replacing professional authority. | Mirrored from the public Full Human Pathway repository and exercised with synthetic validation fixtures. |
| [`capacity-output`](skills/capacity-output/SKILL.md) | Records completed work together with the conditions, constraints, accommodations, variability, and recovery cost required to produce it. | Mirrored from the public Full Human Pathway repository and exercised with synthetic validation fixtures. |

## Evidence-only recovery note

[`Governed Workspace Builder`](skills/governed-workspace-builder/README.md) is preserved here as an evidence/source note rather than presented as a recovered installable skill. Its portfolio evidence describes controlled workspace creation, source registration and SHA-256 custody, review states, checkpoints, promotion gates, and deterministic validation. The original skill/tool source package has not been recovered, so this repository does not reconstruct or publish a substitute as though it were the original.

## Design pattern

Across these skills, the recurring pattern is:

`PRESERVE -> CLASSIFY -> BOUND -> ACT -> VERIFY -> REVIEW -> PRESERVE`

The methods are designed to make AI-assisted work more inspectable without silently turning context, code existence, test success, or model output into human authority.

## Validation philosophy

Validation claims in this repository are intentionally bounded. Historical acceptance evidence remains historical; fresh recovery checks are labeled as recovery checks; and successful tests do not imply deployment, production use, or authority to act inside another project.

For the recovered Governor Intake implementation, the included test can be run directly:

```bash
python skills/governor-intake/tests/test_governor_intake_recovery.py
```

## Why this repository exists

These skills originated inside larger Neverlost projects. Leaving them only inside those repositories made the reusable work difficult to discover. This repository is intentionally a curated mirror/index, not a claim that each skill originated here.

Where an exact source is available, it is mirrored without changing its substantive rules. Where only portfolio or test evidence is recoverable, that limitation is stated explicitly instead of reconstructing a supposedly canonical skill from memory.

## Related public project

The historical Build Week skills and their synthetic validation environment remain available in the public [`Neverlost-full-human-pathway`](https://github.com/Neverlost-AI/Neverlost-full-human-pathway) repository.

## Author

Jeff Summerhays — Neverlost Systems
