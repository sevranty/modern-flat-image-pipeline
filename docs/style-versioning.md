# Versioning model

The project versions independent contracts separately.

| Component | Identifier | Current line | Change examples |
|---|---|---:|---|
| Runtime skill | `skill_version` | `0.1.0` | workflow order, branching, completion rules |
| Modern Flat contract | `style_version` | `0.1.0` | invariants, boundaries, anti-drift rules |
| Prompt pack | `prompt_pack_version` | `0.1.0` | compilation blocks, correction patterns |
| Evaluation set | `eval_version` | `0.1.0` | fixtures, expected findings, anchors |
| Plugin package | `plugin_version` | `0.1.0` | manifest, distribution, metadata |

## Compatibility rules

- A patch version clarifies wording or fixes behavior without changing required inputs.
- A minor version adds backward-compatible fields, branches, adapters, checks, fixtures, or cases.
- A major version changes required inputs, removes fields, or changes acceptance semantics.
- Runtime and style versions are recorded independently.
- A style-contract change requires prompt-pack, QA, and evaluation impact review.
- A runtime change requires evaluation impact review.
- A package release declares the included runtime, style, prompt, and evaluation versions.
- A plugin package may advance without changing the runtime when only metadata, installation, or presentation changes.

## Release manifest

Every tagged release must record:

```text
plugin_version
skill_version
style_version
prompt_pack_version
eval_version
```

The release is compatible only when the packaged skill and every referenced contract exist at the declared versions.

## Initial package line

```text
plugin_version: 0.1.0
skill_version: 0.1.0
style_version: 0.1.0
prompt_pack_version: 0.1.0
eval_version: 0.1.0
```

## Changelog requirements

Add a changelog entry when a change affects:

- installation or manifest discovery;
- runtime inputs, outputs, or completion criteria;
- style acceptance or rejection behavior;
- prompt compilation semantics;
- evaluation fixtures or expected decisions;
- supported adapter capabilities.
