# Quality gates

## 1. Principle

Quality control is split into four mandatory gates:

```text
input gate
-> pre-generation gate
-> visual QA gate
-> final delivery gate
```

Prompt quality does not prove image quality. The actual returned image must be inspected.

## 2. Gate 1: input

Pass only when:

- at least one usable reference is available;
- each reference has an ID;
- each reference has assigned roles;
- ambiguous claims are marked with confidence;
- conflicts are resolved or explicitly blocked;
- sensitive inputs and exact-text requirements have been routed through the policy rules.

Fail when:

- the target image is missing;
- the referenced image cannot be accessed;
- critical identity or construction details are unknowable;
- the task requires a capability that cannot be provided and no safe fallback exists.

## 3. Gate 2: pre-generation

Pass only when all of the following exist:

- Reference Analysis Cards;
- Reference Map;
- Semantic Lock;
- Identity Lock when required;
- Composition Lock with level and exact elements;
- mandatory Style Lock;
- Scene Brief;
- Composition Specification;
- Generation Specification;
- capability route.

### Semantic checks

- The primary subject is explicit.
- The action is observable and physically coherent.
- The message and emotional purpose are not contradictory.
- Supporting objects have defined roles.
- No unsupported story element has been added.

### Composition checks

- Camera angle and shot scale are explicit.
- Main-subject position and frame share are explicit.
- Foreground, midground, and background are defined when relevant.
- Negative space is intentional.
- Protected crop zones are explicit.
- Safe-area requirements are compatible with the output format.

### Style checks

The Generation Specification semantically includes:

- clean structured planar geometry;
- readable silhouette;
- vector-like surfaces;
- volumetric gradients;
- clean layered shadows;
- coherent directional light;
- controlled rim light where useful;
- depth-layer separation;
- explicit non-photorealistic intent;
- scene-relevant anti-drift exclusions.

### Tool checks

- Requested size or aspect ratio is supported or safely approximated.
- Reference editing support is known.
- Multiple-reference support is known.
- Mask, transparency, seed, and format support are not assumed.
- The tool can return an inspectable image.

If any required artifact is missing, do not generate.

## 4. Gate 3: visual QA

Inspect the actual candidate image in a fresh pass.

### 4.1 Meaning and action

Check:

- correct primary subject;
- correct object count;
- correct action;
- readable message or metaphor;
- correct emotional tone;
- no unrelated narrative additions.

### 4.2 Identity and construction

Check:

- identity-defining properties;
- product, machine, or architectural structure;
- clothing, equipment, and distinctive details under lock;
- no duplicated, detached, or impossible parts;
- no unrequested substitution of the main subject.

### 4.3 Anatomy

For people or creatures, check:

- correct limb count;
- plausible joints and posture;
- usable hands;
- coherent face;
- consistent age and body proportions;
- no merged bodies or accidental duplicates.

### 4.4 Composition and camera

Check:

- lock level compliance;
- camera and shot scale;
- subject position and frame share;
- visual center;
- movement and gaze direction;
- negative space;
- crop safety;
- balance of major masses.

### 4.5 Modern Flat style

Check:

- clean planar or vector-like geometry;
- readable silhouettes;
- dimensional gradient modeling;
- clean cast and contact shadows;
- coherent directional key light;
- controlled rim light;
- foreground, midground, and background separation;
- atmospheric depth;
- hierarchical detail;
- absence of dominant photographic, painterly, glossy-CGI, or generic-flat drift.

### 4.6 Palette

Check:

- role hierarchy;
- focal accent placement;
- thumbnail contrast;
- no equal-weight saturation across all objects;
- no accidental muddy or noisy color mixing.

### 4.7 Production quality

Check:

- no random text;
- no watermarks;
- no unrequested logos;
- no broken edges or obvious generation artifacts;
- sufficient resolution for the declared use;
- correct background behavior when supported;
- usable crop and safe area.

## 5. Diagnostic categories

Use exactly one primary category per correction request:

- `semantic_error`;
- `identity_error`;
- `composition_error`;
- `camera_error`;
- `silhouette_error`;
- `anatomy_error`;
- `geometry_error`;
- `layering_error`;
- `lighting_error`;
- `shadow_error`;
- `gradient_error`;
- `palette_error`;
- `style_drift`;
- `texture_error`;
- `detail_error`;
- `safe_area_error`;
- `crop_error`;
- `text_error`;
- `technical_error`;
- `delivery_missing`.

Secondary categories may be recorded, but one primary category controls the next action.

## 6. Severity

| Severity | Meaning | Required action |
|---|---|---|
| critical | blocks acceptance regardless of score | correct or regenerate |
| major | materially harms meaning, identity, composition, or style | targeted correction or regeneration |
| minor | local imperfection with no critical semantic impact | targeted correction or documented acceptance |
| note | non-blocking observation | record only |

## 7. Weighted scorecard

| Category | Weight |
|---|---:|
| Meaning and metaphor | 20 |
| Primary subject and identity | 15 |
| Composition and camera | 15 |
| Modern Flat compliance | 25 |
| Anatomy and construction | 10 |
| Light, shadows, and depth | 10 |
| Technical quality and delivery readiness | 5 |
| **Total** | **100** |

Quality bands:

- `90-100`: `accept` if no critical defect exists;
- `80-89`: `local_correction`;
- `65-79`: `required_iteration`;
- `0-64`: `reject`.

A quality band describes the candidate. It is not the runtime action.

Map the quality band and tool capability to exactly one runtime action:

| Quality band | Runtime action |
|---|---|
| `accept` | `accept` |
| `local_correction` | `targeted_correction` when accepted layers can be preserved; otherwise `regenerate` |
| `required_iteration` | `targeted_correction` for one bounded primary defect with reliable edit support; otherwise `regenerate` |
| `reject` | `regenerate` |

Use `fail` only when required source evidence, permission, or tool capability is unavailable and no valid fallback exists.

A high score never overrides a critical defect.

## 8. Critical rejection criteria

Reject regardless of score when any of the following is present:

- wrong primary subject;
- lost or inverted meaning;
- wrong required action;
- identity-defining structure is missing;
- broken face, extra limbs, or merged anatomy;
- constructively impossible main object;
- critical crop of the main subject;
- dominant photorealism;
- dominant glossy CGI;
- generic flat result without required depth;
- dirty texture noise dominating the scene;
- contradictory light directions;
- unreadable or accidental text where none is allowed;
- required final image is not visible to the user.

## 9. Correction order

Always correct from the highest-level failure downward:

1. meaning and subject;
2. identity and construction;
3. composition and camera;
4. silhouette and anatomy;
5. geometry and depth layers;
6. lighting and shadows;
7. gradients and palette;
8. detail and technical finish;
9. delivery.

Do not polish detail while a higher-level defect remains.

## 10. Fresh-pass rule

After every correction:

- inspect the new image again;
- do not assume previously accepted layers remained intact;
- compare against all locks and not only the corrected category;
- issue a new QA report, quality band, and runtime action.

## 11. Final decision record

Record:

- candidate ID;
- score by category;
- total score;
- quality band;
- critical defects;
- primary diagnostic category;
- runtime next action;
- accepted limitations;
- delivery readiness.
