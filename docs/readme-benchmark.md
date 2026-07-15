# README benchmark

Research date: 2026-07-15.

## Method

The benchmark examines twelve public repositories in three groups:

1. official or widely used Agent Skills and plugin repositories;
2. image-generation and visual-workflow tools;
3. mature design and developer tools with strong onboarding.

The analysis focuses on information architecture and onboarding. It does not copy wording, screenshots, badges, visual identity, or repository assets.

| Repository | Audience | First screen | Value proposition | Install / quick start | Examples | Architecture | Limitations | Applied lesson |
|---|---|---|---|---|---|---|---|---|
| `openai/plugins` | plugin developers and users | concise official description | package structure and distribution | repository-oriented | plugin catalog | explicit plugin anatomy | platform contract implied | separate package metadata from runtime skill logic |
| `anthropics/skills` | skill authors and users | direct definition of skills | self-contained reusable capability | clear folder model | representative skills | strong skill-directory pattern | runtime-specific caveats | explain the repository as one focused skill, not a framework |
| `ningzimu/codex-gpt-image` | Codex image users | narrow image capability | immediate image-generation outcome | prominent setup and invocation | command examples | scripts and references visible | unofficial integration caveat | show exact usage early and state integration boundaries |
| `Comfy-Org/ComfyUI` | visual AI practitioners | recognizable product and workflow | graph-based image workflows | installation variants | rich visual output | workflow model is central | hardware and node complexity | visualize the pipeline without reproducing dense node UI |
| `invoke-ai/InvokeAI` | creators and teams | polished product framing | professional generative-media workflow | structured setup | visual proof | product modules | environment requirements | pair strong visual proof with restrained technical copy |
| `huggingface/diffusers` | ML developers | library identity and scope | reusable diffusion pipelines | package-first quick start | code examples | broad pipeline taxonomy | model and hardware variability | keep capability wording generic and adapter-aware |
| `lllyasviel/Fooocus` | non-technical and technical creators | simple outcome-led framing | reduced complexity for image generation | direct start path | output gallery | minimal conceptual overhead | model-specific behavior | avoid making the README read like an internal specification |
| `n8n-io/n8n` | automation builders | strong product statement | connect inputs, logic, and outputs | immediate self-host/cloud paths | workflow examples | process metaphor | deployment choices | show input → control → output as the central mental model |
| `storybookjs/storybook` | UI developers and designers | one-line product purpose | build and test components in isolation | short start command | visual component proof | ecosystem linked later | framework matrix | explain quality gates after the quick start, not before it |
| `excalidraw/excalidraw` | collaborative visual thinkers | product output is the identity | simple collaborative drawing | fast run path | immediate visual proof | implementation secondary | deployment caveats | let the hero image demonstrate the product language |
| `penpot/penpot` | design and development teams | platform-level proposition | open design and code collaboration | clear install options | product screenshots | system scope explained | infrastructure requirements | use strong hierarchy and avoid badge-heavy presentation |
| `remotion-dev/remotion` | creative developers | code-to-media statement | generate media programmatically | concise package start | short code and media proof | mental model before details | rendering environment | describe transformation in one sentence and one diagram |

## Cross-repository findings

### Strong patterns

- The first screen answers three questions: what it is, what goes in, and what comes out.
- A reliable quick start appears before architecture details.
- The strongest READMEs use one primary example rather than many equal-weight examples.
- Installation paths are separated by environment instead of mixed into one block.
- Limitations increase trust when they are concrete and placed before contribution guidance.
- Architecture is most useful after the user understands the primary workflow.

### Weak patterns

- Badge walls and long feature grids make narrow tools look generic.
- Large screenshots without explanatory captions fail on mobile.
- Claims such as “production ready,” “perfect fidelity,” or “guaranteed consistency” are weak without evidence.
- Internal schemas at the top of the README delay understanding.
- Multiple overlapping installation methods create uncertainty.
- Product marketing language can obscure capability boundaries.

## Decisions for this repository

- Use the repository social preview as the hero visual.
- State `reference in → structured control → checked image out` above the fold.
- Put standalone skill installation before plugin packaging details.
- Keep one canonical invocation in the quick start.
- Explain transformation modes, locks, and quality gates with compact tables.
- Link to detailed contracts instead of reproducing them.
- State clearly that no image model is bundled.
- Use no external logo, copied visual identity, fake metric, or unsupported compatibility claim.
- Keep the README useful without the hero image and readable on a narrow viewport.
