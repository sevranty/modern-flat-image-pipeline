# Repository social preview benchmark

Research date: 2026-07-15.

## Method

The benchmark covers fifteen public repositories across direct image-generation tools, Agent Skills/plugins, and adjacent design/developer products. It evaluates repository-level presentation, not product quality.

No competitor image is copied into this repository. Links and analytical notes are used only to identify recurring presentation patterns.

| Repository | Category | Presentation model | Text load | Thumbnail behavior | Useful pattern | Avoid |
|---|---|---|---|---|---|---|
| `openai/plugins` | Agent plugins | concise official identity, architecture-led README | low | strong name recognition | clear package purpose and restrained metadata | generic marketplace collage |
| `anthropics/skills` | Agent Skills | documentation-first repository | low | relies on title and publisher | immediate explanation of skill structure | visually empty first impression |
| `ningzimu/codex-gpt-image` | image skill | narrow capability and workflow framing | medium | technical title remains readable | show input, execution, and result as one flow | endpoint-specific UI imitation |
| `Comfy-Org/ComfyUI` | visual workflow | node/pipeline metaphor | medium | distinctive process silhouette | make transformation visible | dense node graph at thumbnail scale |
| `invoke-ai/InvokeAI` | image generation | polished product imagery and clear product name | medium | visual result carries recognition | one strong generated-output example | multi-screenshot collage |
| `AUTOMATIC1111/stable-diffusion-webui` | image generation | utility-first, community-led presentation | high | weak at small size | immediate category recognition | UI screenshot as social card |
| `lllyasviel/Fooocus` | image generation | simple value proposition and output examples | medium | one-image examples work well | reduce controls and emphasize outcome | too many sample tiles |
| `huggingface/diffusers` | image library | library identity with broad capabilities | medium | strong concise name | pair technical credibility with one visual idea | model-logo collection |
| `n8n-io/n8n` | workflow automation | process/network metaphor and strong wordmark | low | excellent silhouette | show controlled flow between states | literal complex workflow canvas |
| `langchain-ai/langchain` | agent framework | modular framework identity | low | title-first | communicate orchestration rather than one feature | abstract symbol without explanation |
| `storybookjs/storybook` | developer/design tool | interface/component metaphor | low | recognizable product shape | one focal object plus strong type | tiny component screenshots |
| `excalidraw/excalidraw` | design tool | product output as own identity | low | simple and memorable | use the artifact language of the tool | over-polished rendering that hides function |
| `penpot/penpot` | design tool | open design platform, collaborative visual | medium | strong color grouping | dimensional flat geometry with depth | crowded team illustration |
| `remotion-dev/remotion` | creative developer tool | code-to-media transformation | low | direct category cue | express input-to-output transformation | filmstrip clichés |
| `microsoft/semantic-kernel` | agent framework | architecture and orchestration framing | medium | technical recognition | show controlled layers and verification | generic AI glow or robot imagery |

## Repeated strengths

1. A short title remains the most reliable thumbnail element.
2. One transformation metaphor is stronger than a grid of features.
3. Product screenshots become unreadable below approximately 320 pixels wide.
4. Technical repositories benefit from a visible process, but the process must be reduced to three or four states.
5. A solid background is safer across social platforms than transparency.
6. The project should not borrow a competitor logo, signature color system, or exact composition.

## Project-specific conclusion

Use a split composition:

- title and one-sentence value proposition on the left;
- reference card, contract layers, and final Modern Flat illustration on the right;
- four compact process steps below the title;
- no badges, code, repository tree, or competitor marks;
- one dark neutral base with blue, violet, cyan, and warm focal accents.

This makes the project understandable without relying on a brand logo and keeps the core concept readable at thumbnail size.
