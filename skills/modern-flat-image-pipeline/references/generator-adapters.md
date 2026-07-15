# Generator adapters and capability routing

## 1. Purpose

Keep the canonical Modern Flat workflow independent of any specific image model or tool syntax.

The adapter layer translates a completed Generation Specification into the capabilities and parameters exposed by the current host environment. It cannot redefine meaning, locks, style, or quality rules.

## 2. Capability profile

Before generation, identify the available capability profile.

```yaml
adapter_id: ""
tool_name: ""
model_or_mode: ""
capabilities:
  text_to_image: false
  reference_conditioned_generation: false
  reference_image_editing: false
  multiple_references: false
  mask_or_inpainting: false
  exact_aspect_ratio: false
  exact_pixel_size: false
  transparent_background: false
  deterministic_seed: false
  output_formats: []
  returns_inspectable_image: false
limitations: []
```

Do not set a capability to true without evidence from the current tool contract or an actual successful operation.

## 3. Required profiles

### 3.1 Native host image generation or editing

Use when the environment provides a first-class image tool.

Required behavior:

- pass the actual reference images through the supported image input mechanism;
- preserve reference roles in the instruction;
- use edit mode for targeted changes when available;
- inspect the returned image;
- follow the host tool's user-facing response contract.

### 3.2 Generic text-to-image

Use only when reference-conditioned generation or editing is unavailable and the task can be represented sufficiently in the Generation Specification.

Limitations:

- weaker identity preservation;
- weaker composition preservation;
- no guaranteed local correction;
- likely need for full regeneration.

If these limitations violate a required lock, do not downgrade silently.

### 3.3 Generic reference-edit tool

Use when the tool accepts a source image and change instructions.

Required behavior:

- state all do-not-change constraints explicitly;
- keep correction scope narrow;
- prefer the smallest edit region supported by the tool;
- inspect the full image for collateral drift after the edit.

### 3.4 No-image-tool fallback

Use when no generation or edit capability exists.

Produce only:

- Reference Analysis Cards;
- Reference Map;
- locks;
- Scene Brief;
- Composition Specification;
- Generation Specification;
- compiled prompt package;
- capability gap report.

Do not claim image creation or delivery.

## 4. Routing algorithm

Apply this order:

1. Determine whether the request is generation, reference-conditioned reinterpretation, or targeted edit.
2. Read the Generation Specification adapter requirements.
3. Compare required and available capabilities.
4. Choose the highest-fidelity compatible route.
5. Record every unsupported capability and fallback effect.
6. Stop if a fallback would violate a critical lock.
7. Generate or edit.
8. Inspect the actual result.
9. Route to accept, targeted correction, full regeneration, or fail.

## 5. Reference routing

For each reference, preserve its assigned role:

```yaml
references:
  - reference_id: reference-01
    roles:
      - identity
      - composition
    take:
      - main object silhouette
      - camera angle
    do_not_take:
      - original rendering style
      - incidental background texture
```

If the tool accepts only one image:

- choose the highest-priority reference;
- translate lower-priority references into explicit textual constraints where reliable;
- report the reduction in fidelity;
- stop when a discarded reference carries a critical Identity Lock that cannot be represented safely.

## 6. Text-to-image adaptation

Compile the canonical prompt into the tool's supported text format.

Do not:

- invent model-specific flags;
- assume exact size support;
- assume transparent background support;
- assume seed reproducibility;
- include private endpoints or local authentication instructions;
- replace unsupported reference input with a false claim of identity preservation.

## 7. Edit adaptation

Choose targeted edit when:

- the existing candidate has accepted semantic and composition layers;
- one or two local error categories remain;
- the tool can preserve unedited areas with reasonable fidelity;
- the correction can be described as a bounded change.

The edit instruction must include:

- exact defect;
- exact target state;
- preserved layers;
- forbidden collateral changes;
- Modern Flat invariants that are at risk of drift.

## 8. Full regeneration routing

Choose full regeneration when:

- the primary subject or action is wrong;
- camera and composition both fail;
- identity is unrecoverable through local edit;
- style drift affects the entire scene;
- the tool lacks reliable editing;
- multiple local edits would create more uncertainty than rebuilding from the locked contract.

Carry forward the complete Scene Brief and locks.

## 9. Size and aspect ratio

- Treat aspect ratio as more important than exact pixel size unless the user explicitly requires exact dimensions.
- Use the closest supported size when exact output is unavailable.
- Preserve protected crop zones.
- Record any post-generation crop or resize step.
- Do not stretch the image to force a ratio.

## 10. Background behavior

- Request transparency only when supported.
- If transparency is unavailable, choose an intentional opaque background compatible with the scene.
- Do not falsely report a transparent result.
- Inspect edge halos and cutout artifacts when a background-removal step is used.

## 11. Reproducibility

If the tool supports seeds or stable identifiers:

- record them;
- do not imply exact reproducibility unless verified.

If the tool does not support seeds:

- preserve the Generation Specification and prompt package;
- record tool, mode, date, candidate ID, and known limitations;
- treat reproducibility as semantic and procedural, not pixel-identical.

## 12. Failure handling

### Missing capability

Stop or degrade explicitly. Never hide the capability gap.

### Tool error

Retry once only when:

- the operation is safe to repeat;
- duplicate generation is acceptable;
- the failure appears transient.

### Empty or inaccessible result

Mark `delivery_failed` or `not_generated`. Do not perform visual QA on a nonexistent image.

### Returned image differs from request

Perform QA normally. Tool success does not reduce severity.

## 13. Adapter record

Record:

```yaml
adapter_id: ""
tool_name: ""
model_or_mode: ""
required_capabilities: []
available_capabilities: []
unsupported_capabilities: []
fallbacks: []
generation_or_edit: ""
reference_ids_used: []
result_candidate_id: ""
inspectable_result_returned: false
known_limitations: []
```
