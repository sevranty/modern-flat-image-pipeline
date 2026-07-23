# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.1.0] - unreleased

### Added

- Plugin-ready repository architecture.
- Canonical Modern Flat style contract.
- Reference analysis, locks, scene, and generation contracts.
- Pre-generation and post-generation quality gates.
- Generator capability and fallback rules.
- Safety, rights, text, and identity handling rules.
- Canonical runtime `SKILL.md`.
- Codex plugin manifest for package version `0.1.0`.
- Standalone skill and plugin installation documentation.
- MIT license and release compatibility contract.
- Evaluation contract version `0.1.0`.
- Twelve end-to-end positive and negative regression cases.
- Synthetic reference fixtures and expected decision map.
- Accepted and rejected golden anchor specifications.
- Offline repository, manifest, evaluation, scene, and prompt validators.
- Positive and negative validation fixtures with deterministic rule IDs.
- Repository social preview benchmark, concepts, editable source, and validated PNG exports.
- README benchmark and content-architecture analysis.
- Autonomous WebFactoryOS orchestration boundary with `grants_write_access: false`.
- One evidence-state record for every normative golden anchor.
- Evidence-gated adapter profile registry with explicit unavailable routes.
- Anchor evidence and adapter profile validators.
- Positive and negative adapter fixtures for evidence, fallback, and delivery failures.

### Changed

- Skill discovery metadata describes the complete reference-to-image and visual-QA workflow.
- Release compatibility records `eval_version: 0.1.0`.
- Contribution guidance requires one-command local validation before review.
- Public README documents orchestration ownership, evidence states, verified adapter boundaries, and conditional roadmap triggers.
- Golden anchor status is now `evidence_tracked`; no unavailable record is presented as visual proof.
- Repository Social preview installation and public-card verification are tracked separately in MFP#12 and do not block merges, tags, GitHub Releases, or release closure.

### Validation

- Clean-checkout validation passed on 2026-07-23 for exact `main` commit `03b29f605d92a4ecc412c2467ae59ad134133e1b`: 19 checks, 0 failures. `git diff --check` passed, the checkout remained clean, and remote `main` matched the validated commit before and after the run.

### Release gate

Version `0.1.0` remains unreleased until tag `v0.1.0` targets the validated commit `03b29f605d92a4ecc412c2467ae59ad134133e1b` and the GitHub Release is published and publicly verified. Repository Social preview installation is an independent owner-side follow-up and is not a release gate.
