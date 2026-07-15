# README content outline

## Reader jobs

The README must let a new reader:

1. understand the reference-to-image purpose without scrolling;
2. decide whether Modern Flat is the required output style;
3. install the standalone skill safely;
4. invoke the skill with one real prompt;
5. understand why the process uses locks, specifications, and visual QA;
6. inspect repository maturity through tests and validators;
7. find deeper contracts without reading the entire README.

## Final information architecture

```text
Hero image
Title + one-sentence proposition
Version/status line
Why this exists
Pipeline
Use / do not use
Quick start
Installation
Transformation modes
Runtime artifacts
Quality gates
Examples
Architecture
Validation and evaluation
Capability boundaries
Versioning
Roadmap
Contributing
License
```

## Above-the-fold contract

The first viewport should contain:

- project name;
- repository hero image;
- one sentence describing input, process, and output;
- package/runtime/style/evaluation version line;
- one short invocation example.

## Editorial rules

- Prefer concrete nouns and observable workflow steps.
- Keep paragraphs to three sentences or fewer.
- Use tables only for comparison or stable contracts.
- Avoid duplicate definitions from `SKILL.md` and reference files.
- Do not claim exact identity preservation, generator support, or delivery when the host lacks the capability.
- Do not use a logo, wordmark, or color system from another organization.
- Use relative repository links.
- Keep all code blocks executable or directly usable.
- Add alt text to every image.

## Visual rules

- Use one hero image: `assets/repository-social-preview.png`.
- Do not add a gallery until provenance-controlled candidate images exist.
- Keep badges to zero; show versions as plain text.
- Use compact ASCII diagrams that remain readable without image rendering.

## Evidence links

- architecture: `docs/architecture.md`;
- style: `skills/modern-flat-image-pipeline/references/style-spec.md`;
- locks: `skills/modern-flat-image-pipeline/references/workflow-and-locks.md`;
- quality: `skills/modern-flat-image-pipeline/references/quality-gates.md`;
- evaluation: `docs/evaluation-contract.md` and `tests/`;
- validation: `scripts/validate_repository.py`;
- packaging: `.codex-plugin/plugin.json`;
- versioning: `docs/style-versioning.md`.
