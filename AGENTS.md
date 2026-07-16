# Repository agent instructions

## Scope

This repository contains one canonical skill: `modern-flat-image-pipeline`.

The skill converts one or more visual references into a new Modern Flat illustration. It does not provide its own image model and must remain independent of any specific generator.

## Non-negotiable rules

1. Treat the internal Modern Flat style contract as the only style source.
2. Treat user references as sources of content, identity, pose, construction, camera, composition, scale, environment, palette direction, or individual details only when explicitly assigned.
3. Do not infer style from a user reference.
4. Do not generate before the Scene Brief, locks, and Generation Specification are complete.
5. Inspect the actual generated image before accepting it.
6. Correct diagnosed errors locally when the available tool supports editing.
7. Do not claim completion until the final image is visible to the user.
8. Keep all repository paths ASCII-only.
9. Do not add embedded third-party identity systems, fixed corporate palettes, or unrelated domain rules.
10. Do not use a living artist's name as a style shortcut.

## Source-of-truth map

| Concern | Canonical file |
|---|---|
| Runtime order and branching | `skills/modern-flat-image-pipeline/SKILL.md` |
| Style definition | `skills/modern-flat-image-pipeline/references/style-spec.md` |
| Reference analysis | `skills/modern-flat-image-pipeline/references/reference-analysis.md` |
| Locks and workflow contracts | `skills/modern-flat-image-pipeline/references/workflow-and-locks.md` |
| Prompt compilation | `skills/modern-flat-image-pipeline/references/prompt-patterns.md` |
| Quality gates | `skills/modern-flat-image-pipeline/references/quality-gates.md` |
| Final user delivery | `skills/modern-flat-image-pipeline/references/output-delivery.md` |
| Generator capabilities | `skills/modern-flat-image-pipeline/references/generator-adapters.md` |
| Verified adapter registry | `skills/modern-flat-image-pipeline/assets/adapters/capability-profiles.yaml` |
| People, text, identity, and rights | `skills/modern-flat-image-pipeline/references/safety-and-rights.md` |
| Plugin package manifest | `.codex-plugin/plugin.json` |
| Evaluation semantics | `docs/evaluation-contract.md` |
| Evaluation fixtures and expected decisions | `tests/` |
| Golden anchor specifications | `skills/modern-flat-image-pipeline/assets/anchors/` |
| Golden anchor evidence states | `skills/modern-flat-image-pipeline/assets/anchors/evidence.yaml` |
| Validation orchestration | `scripts/validate_repository.py` |
| Package and contract versions | `docs/style-versioning.md` |
| Architecture | `docs/architecture.md` |
| Orchestration boundary | `docs/web-factory-os-orchestration.md` |
| Decisions | `docs/decision-log.md` |

Do not duplicate detailed rules across files. Link to the canonical file instead.

## Orchestration boundary

- MFP owns the skill, contracts, assets, validators, tests, local Issues and pull requests, tags, and releases.
- WebFactoryOS owns only external registry, routing, relations, naming, and orchestration status.
- `grants_write_access` is false.
- MFP has no build, runtime, validation, packaging, or release dependency on WebFactoryOS.
- Caveman is a communication reference only. Do not install, import, vendor, or require it.

See [the orchestration contract](docs/web-factory-os-orchestration.md).

## Packaging rules

- Keep plugin, skill-folder, and frontmatter names equal to `modern-flat-image-pipeline`.
- Keep manifest paths relative and rooted with `./` where the manifest contract requires it.
- Keep plugin interface prompts short and aligned with real runtime capabilities.
- Do not claim a bundled image model, exact-size support, or private backend integration.
- Do not add marketplace entries unless the target personal or team marketplace is explicit.
- Update `CHANGELOG.md` when installation, metadata, compatibility, or public behavior changes.

## Evaluation rules

- Keep fixture IDs, case IDs, anchor IDs, and adapter IDs stable and ASCII-only.
- Test complete decisions, not exact prompt wording.
- Keep quality bands separate from runtime actions.
- Require one primary diagnostic category for every rejected case.
- Do not commit externally sourced visual references without clear redistribution rights.
- Treat golden anchor specifications as normative and visual candidates as evidence attached to them.
- Give every anchor one published or unavailable evidence record.
- An unavailable record requires a reason and unblock condition and is not visual proof.
- A true adapter capability requires dated public-contract or successful-operation evidence.
- Do not treat static evaluation as a substitute for inspecting an actual generated image.

## Validation rules

Run before review:

```bash
python3 scripts/validate_repository.py .
```

- Validators must remain deterministic and offline.
- Every error must include a stable rule ID, path, message, and fix.
- Positive fixtures must pass; negative fixtures must fail with their expected rule ID.
- Do not weaken a validator only to make a fixture pass; fix the contract or fixture.
- Static validation never declares an image visually correct.

## Change protocol

- Work in one task branch and one pull request per completion scope.
- Keep architecture and canonical runtime changes in Draft until exact-head review is complete.
- Update the decision log when changing a foundational contract.
- Update the changelog when changing externally observable behavior.
- Preserve compatibility between runtime workflow, templates, references, packaging, tests, validators, and metadata.
- Record exact base, exact validated HEAD, checks, review threads, and final merge SHA.
