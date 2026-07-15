# Repository social preview concepts

## Technical contract

GitHub recommends PNG, JPG, or GIF under 1 MB, at least `640x320`, and `1280x640` for best display. The selected deliverable uses a solid background, `1280x640`, 2:1 ratio, and a minimum 40-pixel internal safe area.

## Concept A: Pipeline transformation

**Metaphor:** a reference card passes through translucent analysis and contract layers and becomes a polished Modern Flat scene.

**Composition:** title and value proposition on the left; transformation sequence on the right; four compact process steps below.

**Strengths:** explains the product in one glance; works without a logo; maps directly to runtime behavior.

**Risks:** translucent layers can become visually noisy if too numerous.

**Decision:** selected. Limit layers to three and keep the final image dominant.

## Concept B: Style compiler

**Metaphor:** a structured scene specification is compiled into a final illustration.

**Composition:** specification card, compiler core, output image.

**Strengths:** accurately communicates the Generation Specification as source of truth.

**Risks:** looks too technical and may read as a code-generation tool rather than an image pipeline.

**Decision:** retain as a future documentation diagram, not the social preview.

## Concept C: Layered scene construction

**Metaphor:** geometry, gradients, light, shadows, and depth are assembled into one scene.

**Composition:** exploded visual layers converging into the output.

**Strengths:** strongly demonstrates the Modern Flat style contract.

**Risks:** under-explains reference analysis and semantic preservation.

**Decision:** use as supporting visual language inside the selected concept.

## Final concept specification

```text
canvas: 1280x640
ratio: 2:1
background: solid dark neutral gradient
safe area: 40 px minimum; actual critical content starts at 64 px
left block: project title + one-line proposition
right block: reference card -> three contract layers -> final illustration
process row: Analyze -> Specify -> Generate -> Inspect
footer: Reference analysis · Locks · Modern Flat contract · Visual QA
```

## Text

```text
Modern Flat
Image Pipeline

Reference in. Structured control. Checked image out.
```

## Palette roles

- neutral base: dark navy;
- dominant group: blue;
- supporting groups: violet and cyan;
- focal accent: warm yellow-orange;
- primary text: white;
- secondary text: desaturated light blue.

## QA result

- title readable at `320x160`;
- one obvious visual center: final illustrated output;
- input and process remain identifiable at thumbnail size;
- no third-party logo, wordmark, signature palette, watermark, or pseudo-text;
- safe area respected;
- image remains under GitHub's 1 MB limit;
- solid background is reliable across light and dark platform surfaces.
