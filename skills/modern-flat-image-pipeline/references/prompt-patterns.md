# Prompt patterns

```yaml
prompt_pack_version: 0.1.0
status: draft
```

## 1. Principle

Do not move directly from a reference to one long prompt.

Use prompts as controlled transformations between explicit artifacts:

```text
reference
-> analysis card
-> locks
-> scene brief
-> composition specification
-> generation specification
-> adapter prompt
-> QA report
-> correction request
```

The Generation Specification is canonical. Prompt wording is replaceable.

## 2. Analysis prompt contract

### Inputs

- available reference images;
- user request;
- intended output use when known.

### Required output

- one Reference Analysis Card per reference;
- observed, inferred, and unknown separation;
- preserve, change, exclude, and unknown lists;
- confidence per ambiguous claim;
- no generation prompt.

### Instruction pattern

1. Analyze the reference as a source of content and composition.
2. Do not inherit its rendering style.
3. Record observable evidence before interpretation.
4. Assign allowed roles.
5. State uncertainty.

## 3. Optional metaphor search

Run only when the task has a message but no defined visual concept.

Required output for each candidate:

- visual idea;
- main object;
- action;
- reason the metaphor communicates the message;
- primary misreading risk.

Reject metaphors that:

- require explanatory text;
- cannot read at thumbnail size;
- contain many equal-weight symbols;
- replace the requested subject without permission.

## 4. Optional metaphor strengthening

Run only when a concept exists but reads weakly.

Change the smallest possible set of:

- scale;
- hierarchy;
- direction;
- secondary-object placement;
- contrast;
- depth;
- supporting symbols.

Do not replace the main concept unless the user requests it.

## 5. Scene Brief prompt contract

### Inputs

- accepted Reference Analysis Cards;
- resolved conflicts;
- user instruction.

### Output

A generator-independent Scene Brief with no rendering syntax.

### Instruction pattern

- state the purpose and message;
- define the subject and action;
- define the environment and moment;
- define the visual center and depth roles;
- define negative space and output use;
- define measurable success criteria;
- add no unsupported story elements.

## 6. Lock prompt contract

Create:

- Semantic Lock;
- Identity Lock;
- Composition Lock level and exact elements;
- mandatory Style Lock.

For every lock, record:

- locked property;
- evidence or decision source;
- strictness;
- allowed simplification;
- failure condition.

## 7. Generation prompt compiler

Compile in this order:

1. asset type and intended result;
2. primary subject;
3. primary action;
4. identity-defining features;
5. environment;
6. composition and camera;
7. depth layers and overlaps;
8. Modern Flat geometry;
9. lighting and shadows;
10. gradient modeling;
11. palette roles;
12. detail hierarchy;
13. preserve and do-not-change constraints;
14. exclusions;
15. output requirements.

### Canonical semantic form

```text
Create a detailed dimensional Modern Flat illustration.

Subject and action:
Describe the primary subject, the exact action, and identity-defining features.

Environment and composition:
Describe the environment, camera, scale, position, depth layers, overlaps, movement, and negative space.

Style system:
Use clean structured planar geometry, readable silhouettes, vector-like surfaces, volumetric gradient modeling, clean layered shadows, one consistent directional key light, controlled rim light, and atmospheric depth. Keep the result polished and explicitly non-photorealistic.

Preserve:
State the approved semantic, identity, and composition constraints.

Do not change:
State accepted layers that must remain stable during an edit.

Exclude:
State scene-specific exclusions plus critical anti-drift exclusions from the style contract.

Output:
State aspect ratio, safe area, crop protection, background behavior, and required format when supported.
```

Adapters may change wording or parameters but not meaning.

## 8. Diagnostic QA prompt contract

Do not generate during diagnosis.

Compare the actual image against:

- Scene Brief;
- locks;
- Composition Specification;
- Generation Specification;
- style contract;
- output requirements.

For each finding, return:

- category;
- severity;
- observed defect;
- violated contract;
- correction target;
- layers to preserve;
- recommended action.

## 9. Targeted correction prompt contract

A correction request must be narrow.

```text
Correct only the diagnosed error category.

Observed defect:
State what is visibly wrong.

Target state:
State a verifiable result.

Preserve unchanged:
List all accepted semantic, identity, composition, geometry, lighting, palette, and detail layers that must not move.

Forbidden collateral changes:
Do not add objects, change camera, replace the subject, alter accepted colors, or regenerate the full scene unless explicitly required by the diagnosis.
```

Do not use vague instructions such as:

- make it better;
- make it more beautiful;
- improve quality;
- fix everything;
- make it more professional.

## 10. Full regeneration contract

Use full regeneration only when:

- the main subject is wrong;
- the action or message is wrong;
- camera and major masses fail together;
- the tool cannot preserve accepted layers;
- critical anatomy or construction defects are distributed across the scene;
- style drift affects the entire image.

Carry forward all accepted locks and explain why local correction is insufficient.

## 11. Final QA prompt contract

Perform a fresh pass on the final candidate. Do not reuse assumptions from the previous QA report.

Return:

- weighted score;
- critical defects;
- final decision;
- final candidate identifier;
- delivery readiness;
- known limitations.

## 12. Prompt quality rules

- Use explicit nouns and observable actions.
- Prefer one coherent instruction over contradictory adjective stacks.
- Express spatial relationships directly.
- Keep negative constraints focused on likely failure modes.
- Repeat invariants during edits when the tool may drift.
- Do not claim unsupported seed, mask, transparency, or exact-size capabilities.
- Do not include unrequested visible text, logos, or watermarks.
