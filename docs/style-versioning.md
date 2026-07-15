# Versioning model

The project versions independent contracts separately.

| Component | Identifier | Change examples |
|---|---|---|
| Runtime skill | `skill_version` | workflow order, branching, completion rules |
| Modern Flat contract | `style_version` | invariants, boundaries, anti-drift rules |
| Prompt pack | `prompt_pack_version` | compilation blocks, correction patterns |
| Evaluation set | `eval_version` | fixtures, expected findings, anchors |
| Plugin package | `plugin_version` | manifest, distribution, metadata |

## Compatibility rules

- A patch version clarifies wording without changing observable behavior.
- A minor version adds backward-compatible fields, branches, or checks.
- A major version changes required inputs, removes fields, or changes acceptance semantics.
- Runtime and style versions must be recorded independently.
- A style-contract change requires prompt and QA impact review.
- A runtime change requires evaluation impact review.
- A package release must declare the included runtime, style, prompt, and evaluation versions.

## Initial development line

```text
skill_version: 0.1.0
style_version: 0.1.0
prompt_pack_version: 0.1.0
eval_version: not-yet-published
plugin_version: not-yet-published
```
