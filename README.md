# Modern Flat Image Pipeline

A generator-independent Agent Skill that turns visual references into new Modern Flat illustrations through structured analysis, explicit locks, scene contracts, visual QA, and targeted correction.

## Status

Package line `0.1.0` is available for review and local installation. The skill does not ship an image model; it routes work to image-generation or image-editing capabilities available in the host environment.

## Pipeline

```text
reference input
-> reference analysis
-> semantic / identity / composition locks
-> scene brief
-> Modern Flat style contract
-> generation specification
-> pre-generation gate
-> image generation or edit
-> visual QA
-> targeted correction
-> final user-visible delivery
```

## Install as a standalone skill

```bash
git clone https://github.com/sevranty/modern-flat-image-pipeline.git "$HOME/modern-flat-image-pipeline"
mkdir -p "$HOME/.codex/skills"
ln -sfn "$HOME/modern-flat-image-pipeline/skills/modern-flat-image-pipeline" "$HOME/.codex/skills/modern-flat-image-pipeline"
```

## Install as a Codex plugin package

Clone the repository into the personal plugin directory:

```bash
mkdir -p "$HOME/plugins"
git clone https://github.com/sevranty/modern-flat-image-pipeline.git "$HOME/plugins/modern-flat-image-pipeline"
```

The package manifest is stored at `.codex-plugin/plugin.json`. Add the local plugin to the selected personal or team marketplace using the current Codex plugin configuration. This repository does not modify a user or team marketplace automatically.

## Quick start

Attach one or more visual references and ask:

```text
Use $modern-flat-image-pipeline to preserve the required meaning and composition, create a new Modern Flat illustration, inspect the result, correct diagnosed defects, and show the accepted final image.
```

## Inputs and outputs

Inputs:

- one or more usable visual references;
- a transformation goal;
- output use, aspect ratio, crop, or safe-area requirements when relevant.

Outputs:

- reference analysis and explicit locks;
- Scene Brief and Generation Specification;
- generated or edited candidate when a compatible image tool is available;
- visual QA report and targeted correction decision;
- accepted final image delivered visibly to the user.

## Repository structure

```text
.codex-plugin/plugin.json
skills/modern-flat-image-pipeline/
  SKILL.md
  agents/openai.yaml
  references/
  assets/templates/
docs/
```

## Limitations

- No image model or private generation endpoint is bundled.
- Exact identity, masks, multiple references, transparency, seeds, and exact sizes depend on the active image tool.
- Static validation, regression fixtures, public examples, social preview, and the full benchmarked README are tracked separately.
- Visual QA of the actual returned image remains mandatory.

## Versioning

Runtime, style, prompt-pack, evaluation, and plugin-package versions are tracked independently. See `docs/style-versioning.md` and `CHANGELOG.md`.

## Contribution workflow

Work in a task branch, preserve the source-of-truth boundaries in `AGENTS.md`, update the decision log for foundational contract changes, and validate runtime, templates, packaging, and documentation together.

## License

MIT. See `LICENSE`.
