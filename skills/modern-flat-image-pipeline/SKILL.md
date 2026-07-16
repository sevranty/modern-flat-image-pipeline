---
name: modern-flat-image-pipeline
description: Transform one or more visual references into a new Modern Flat illustration through structured reference analysis, semantic and composition locks, scene specification, controlled image generation or editing, visual QA, targeted correction, and final user-visible delivery. Use for reference-to-image reinterpretation, composition-guided generation, or correction of an existing Modern Flat candidate. Do not use for photorealistic, painterly, anime-led, generic flat-minimal, or glossy 3D CGI outputs.
---

# Modern Flat Image Pipeline

## Runtime metadata

```yaml
skill_version: 0.1.0
style_id: modern-flat
style_version: 0.1.0
prompt_pack_version: 0.1.0
status: draft
```

## Scope

Use this skill when the user provides one or more visual references and expects a new image rendered under the canonical Modern Flat style contract.

Supported task families:

- reference-to-image reinterpretation;
- composition-guided generation;
- identity- or construction-preserving restyling;
- multi-reference synthesis with explicit roles;
- targeted correction of an existing Modern Flat candidate;
- staged construction of a complex scene.

Do not use this skill when the requested final style is:

- photorealistic or hyperrealistic;
- painterly or watercolor-led;
- anime-led;
- generic flat minimalism without dimensional depth;
- glossy 3D CGI;
- direct imitation of a named living artist.

## Required references

Read these files before the corresponding stage:

| Stage | Read |
|---|---|
| Reference intake and analysis | `references/reference-analysis.md` |
| Locks, Scene Brief, and specifications | `references/workflow-and-locks.md` |
| Style decisions | `references/style-spec.md` |
| Prompt compilation and correction | `references/prompt-patterns.md` |
| Tool routing | `references/generator-adapters.md` |
| People, text, identity, and rights | `references/safety-and-rights.md` |
| Preflight and visual QA | `references/quality-gates.md` |
| Final delivery | `references/output-delivery.md` |

Do not restate detailed rules from those files. Apply them.

## Input contract

Require:

- at least one usable reference image or an existing candidate image;
- a requested outcome or a clear transformation goal;
- the intended output use when crop, safe area, or exact dimensions matter.

Resolve or explicitly record:

- which properties must be preserved;
- which properties may change;
- which properties must be excluded;
- whether person identity, exact text, or external identity assets are involved;
- whether the user expects a new generation or a targeted edit.

If the image target is missing or inaccessible, stop and request a usable image. Do not invent its content.

## Mandatory procedure

Follow every stage in order. Do not skip directly to generation.

### 1. Run the input gate

- Confirm the reference images are available and distinguishable.
- Assign stable reference IDs.
- Flag low quality, crop, ambiguity, conflicts, people, private data, exact text, and external identity assets.
- Apply `references/safety-and-rights.md` where relevant.

Stop if a critical source or permission boundary is unresolved.

### 2. Analyze every reference

Use `references/reference-analysis.md`.

Create one Reference Analysis Card per reference. Separate:

- observed evidence;
- inferred meaning;
- unknowns.

Record:

- subject and action;
- environment;
- composition and camera;
- depth layers;
- identity- and construction-defining features;
- preserve, change, exclude, and unknown lists;
- confidence per ambiguous claim.

Do not create a generation prompt yet.

### 3. Build the Reference Map

Assign only explicit roles:

- content;
- identity;
- pose;
- construction;
- camera;
- composition;
- scale;
- environment;
- palette direction;
- detail.

For every role, state `take`, `do_not_take`, priority, and strictness.

Never assign user references the `style` role. Style always comes from `references/style-spec.md`.

### 4. Resolve conflicts

Apply the precedence rules from `references/reference-analysis.md` and `references/workflow-and-locks.md`.

Do not silently average incompatible references. Escalate a conflict only when it blocks a critical lock or changes the user's intended subject or meaning.

### 5. Create locks

Create:

- Semantic Lock;
- Identity Lock when required;
- Composition Lock level `0-4` plus exact locked elements;
- mandatory Style Lock with `style_id: modern-flat` and `override_allowed: false`.

Do not lock uncertain properties.

### 6. Create the Scene Brief

Use `references/workflow-and-locks.md`.

Define:

- purpose and message;
- intended emotion;
- primary subject and action;
- supporting objects;
- environment and moment;
- visual center;
- movement and gaze;
- foreground, midground, and background roles;
- negative space;
- output use;
- success criteria.

Do not include generator syntax.

### 7. Create the Composition Specification

Fix:

- aspect ratio;
- shot scale and camera angle;
- subject position and frame share;
- movement direction;
- secondary-object placement;
- depth layers and overlaps;
- negative space;
- safe area;
- allowed and protected crop zones.

Do not add rendering-style prose here.

### 8. Apply the Modern Flat style contract

Read `references/style-spec.md`.

Use its canonical definition, invariants, role-based palette, anti-drift boundaries, and forbidden markers.

Do not inherit photographic, painterly, glossy-CGI, generic-flat, or author-signature rendering behavior from the input reference.

### 9. Create the Generation Specification

Use `assets/templates/generation-spec.yaml` as the field contract.

Complete:

- versions;
- subject and action;
- environment;
- locks;
- composition;
- geometry and depth;
- lighting;
- gradients and shadows;
- palette roles;
- detail hierarchy;
- preserve, do-not-change, and exclude lists;
- output requirements;
- adapter requirements;
- known unknowns.

The Generation Specification is the source of truth for the attempt.

### 10. Run the pre-generation gate

Use Gate 2 in `references/quality-gates.md`.

Do not generate if:

- a required artifact is missing;
- subject, action, camera, or composition is ambiguous;
- style invariants are absent;
- contradictory requirements remain;
- crop and safe area are unresolved;
- a required tool capability is unavailable and no valid fallback exists.

### 11. Route to an available image capability

Use `references/generator-adapters.md`.

Select the highest-fidelity compatible path:

- native generation or edit;
- generic reference edit;
- generic text-to-image;
- no-image-tool fallback.

Do not invent support for masks, multiple references, seeds, transparency, exact sizes, or output formats.

If no image tool is available, return the completed generation package and state that no image was generated. Do not claim completion.

### 12. Compile and execute the generation request

Use `references/prompt-patterns.md`.

Compile in the canonical block order. Preserve the meaning of the Generation Specification even when adapter syntax changes.

For a complex scene, use the staged flow from `references/workflow-and-locks.md` instead of attempting every detail in one pass.

### 13. Inspect the actual result

Do not accept tool success as proof of correctness.

Run the visual QA gate from `references/quality-gates.md` against the returned image.

Check:

- meaning and action;
- identity and construction;
- anatomy;
- composition and camera;
- Modern Flat geometry, gradients, light, shadows, and depth;
- palette hierarchy;
- crop and production quality;
- accidental text, watermarks, and unrequested logos.

Produce a QA report with category scores, critical defects, diagnostic categories, and a decision.

### 14. Choose one next action

Choose exactly one:

- `accept`;
- `targeted_correction`;
- `regenerate`;
- `fail`.

Use targeted correction only when accepted layers can be preserved. Correct one primary diagnostic category at a time.

Never issue a vague instruction such as "make it better".

### 15. Re-inspect after every correction

Perform a fresh full-image QA pass. Verify that previously accepted layers did not drift.

Repeat only as needed to resolve blocking defects. Do not polish local detail while higher-level semantic, identity, composition, or anatomy defects remain.

### 16. Run final QA

Select one final candidate explicitly.

Run a fresh final pass. A score of `90-100` is acceptable only when no critical defect exists.

Record known limitations honestly.

### 17. Deliver the final image

Apply `references/output-delivery.md`.

The run is complete only when:

- the delivered candidate is the one that passed final QA;
- the image is visible to the user;
- the final response is not empty;
- no inaccessible internal path is presented as the only result;
- no unsupported capability is claimed;
- delivery state is `delivered`.

## Conditional branches

### No visual concept

Run metaphor search from `references/prompt-patterns.md`, select a concept, then continue from Scene Brief.

### Weak existing metaphor

Run metaphor strengthening. Change the smallest set of hierarchy, scale, direction, contrast, or supporting symbols.

### Multiple references

Create one card per reference and an explicit role map. Stop when a critical conflict cannot be resolved without changing user intent.

### Sketch, diagram, toy, or unclear object

Infer the intended real class cautiously. Preserve purpose and high-confidence structural evidence. Do not reproduce impossible accidental construction.

### Person identity

Apply `references/safety-and-rights.md`. Do not identify unknown people or promise exact likeness.

### Exact text

Generate the illustration without exact text when possible, reserve safe area, and use a separate editable text step.

### External identity asset

Do not generate an approximate asset when exactness matters. Use an authorized separate asset and post-processing step.

### Existing candidate correction

Analyze the candidate, identify accepted layers, diagnose one primary error category, and prefer targeted edit when supported.

## Failure handling

- Missing image: stop and request the image.
- Critical ambiguity: request clarification only when it changes a required lock.
- Missing capability: use an explicit compatible fallback or stop.
- Tool error: retry once only when safe and likely transient.
- Empty result: mark not generated or delivery failed.
- Rejected result: do not present it as final.
- No visible delivery: mark `delivery_missing` and do not claim completion.

## Completion criteria

All of the following must be true:

- [ ] References analyzed.
- [ ] Reference roles assigned.
- [ ] Locks created.
- [ ] Scene Brief completed.
- [ ] Composition Specification completed.
- [ ] Generation Specification completed.
- [ ] Pre-generation gate passed.
- [ ] Actual image generated or edited.
- [ ] Actual image visually inspected.
- [ ] Critical defects resolved.
- [ ] Final candidate selected.
- [ ] Final candidate passed fresh QA.
- [ ] Final image is visible to the user.
- [ ] Delivery state is `delivered`.
