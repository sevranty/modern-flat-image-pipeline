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
| People, text, identity, and rights | `skills/modern-flat-image-pipeline/references/safety-and-rights.md` |
| Plugin package manifest | `.codex-plugin/plugin.json` |
| Package and contract versions | `docs/style-versioning.md` |
| Architecture | `docs/architecture.md` |
| Decisions | `docs/decision-log.md` |

Do not duplicate detailed rules across files. Link to the canonical file instead.

## Packaging rules

- Keep plugin, skill-folder, and frontmatter names equal to `modern-flat-image-pipeline`.
- Keep manifest paths relative and rooted with `./` where the manifest contract requires it.
- Keep plugin interface prompts short and aligned with real runtime capabilities.
- Do not claim a bundled image model, exact-size support, or private backend integration.
- Do not add marketplace entries unless the target personal or team marketplace is explicit.
- Update `CHANGELOG.md` when installation, metadata, compatibility, or public behavior changes.

## Change protocol

- Work in a task branch.
- Keep architecture and canonical runtime changes in a Draft pull request until explicit lifecycle approval.
- Update the decision log when changing a foundational contract.
- Update the changelog when changing externally observable behavior.
- Preserve compatibility between the runtime workflow, templates, references, packaging, tests, and metadata.
