# Reference analysis contract

## 1. Purpose

Analyze each input reference as evidence for a new image. Separate observable content from inferred meaning and separate both from the reference's original rendering style.

Do not start generation during reference analysis.

## 2. Input gate

Before analysis, confirm:

- at least one usable image is available;
- the intended target is clear: reinterpretation, edit, or composition-guided generation;
- each image can be distinguished from the others;
- low-quality, cropped, ambiguous, or conflicting evidence is recorded;
- sensitive people, private data, exact text, or external identity assets are flagged for the policy pass.

If the image target is missing or inaccessible, stop. Do not invent its content.

## 3. Observation discipline

Record three levels separately:

1. **Observed** — directly visible evidence.
2. **Inferred** — likely interpretation supported by visible evidence.
3. **Unknown** — not reliably determinable.

Never present an inference as an observation.

## 4. Reference Analysis Card

Create one card for each reference with these fields:

### Identity

- `reference_id`;
- `source_type`: photo, illustration, sketch, screenshot, diagram, render, or mixed;
- `quality_notes`;
- `crop_notes`.

### Content

- `primary_subject`;
- `secondary_objects`;
- `action`;
- `environment`;
- `time_or_state`;
- `story_or_message`;
- `intended_emotion`.

### Composition

- `aspect_ratio`;
- `shot_scale`;
- `camera_angle`;
- `main_subject_position`;
- `main_subject_frame_share`;
- `movement_direction`;
- `gaze_direction`;
- `foreground`;
- `midground`;
- `background`;
- `negative_space`;
- `crop_risks`.

### Recognition

- `identity_defining_features`;
- `construction_defining_features`;
- `pose_defining_features`;
- `features_safe_to_simplify`.

### Transfer decision

- `preserve`;
- `change`;
- `exclude`;
- `unknowns`;
- `confidence`.

## 5. Confidence scale

Use a four-level scale:

| Level | Meaning | Required behavior |
|---|---|---|
| high | directly visible and unambiguous | may lock when relevant |
| medium | supported but not fully certain | preserve with caution |
| low | weak evidence or partial visibility | do not lock without user confirmation |
| unknown | cannot be determined | omit or request clarification when critical |

Confidence applies to individual claims, not only the whole reference.

## 6. Reference role assignment

Every reference must receive one or more explicit roles. Allowed roles:

- `content`;
- `identity`;
- `pose`;
- `construction`;
- `camera`;
- `composition`;
- `scale`;
- `environment`;
- `palette_direction`;
- `detail`.

`style` is not an allowed user-reference role. Style always comes from `style-spec.md`.

For each assigned role, record:

- `take` — which properties may transfer;
- `do_not_take` — which properties must not transfer;
- `priority` — how this reference resolves conflicts;
- `strictness` — advisory or locked.

## 7. Multiple-reference conflict rules

Resolve conflicts in this order:

1. explicit user instruction;
2. Semantic Lock;
3. Identity Lock;
4. higher-priority reference role;
5. higher-confidence observation;
6. Scene Brief coherence;
7. simplest interpretation that does not invent unsupported detail.

Do not average incompatible references silently.

Examples of conflicts to record:

- two different camera angles;
- incompatible object construction;
- contradictory poses;
- competing palettes;
- inconsistent environments;
- different subject identities.

## 8. Media-specific analysis

### Photo

Distinguish identity, pose, environment, lens-like composition, and incidental photographic effects. Do not transfer photographic rendering behavior.

### Illustration

Separate subject, composition, geometry, palette relationships, and narrative devices from the original authorial rendering language.

### Sketch or diagram

Treat it as structural evidence. Infer the intended real object cautiously and record uncertainty. Do not preserve impossible or accidental construction.

### Screenshot

Distinguish interface structure from private content, exact text, personal data, and third-party visual assets. Flag content that must be removed or recreated separately.

### Low-quality or partial image

Reduce lock strength. Record invisible areas and avoid inventing identity-defining features.

## 9. Output

Reference analysis is complete only when:

- every reference has a card;
- every reference has assigned roles;
- preserve, change, exclude, and unknown lists are explicit;
- confidence is recorded for ambiguous claims;
- conflicts are resolved or escalated;
- no generation prompt has been produced yet.
