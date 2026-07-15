# Workflow and locks

## 1. Default transformation mode

Unless the user explicitly requests a stricter edit, use semantic reinterpretation:

- preserve the main meaning and required identity;
- use the reference composition as an explicit lock or advisory constraint;
- rebuild the rendering language under the Modern Flat style contract;
- replace incidental details that do not support recognition or meaning.

## 2. Lock families

Locks define what a generation attempt is not allowed to change.

### 2.1 Semantic Lock

Use for:

- primary message;
- subject-action relationship;
- metaphor;
- causal relationship;
- emotional purpose;
- required narrative state.

A semantic error has the highest correction priority.

### 2.2 Identity Lock

Use only for observable, identity-defining properties:

- person or character identity when allowed and sufficiently referenced;
- product or device form;
- machine class and construction;
- architecture;
- distinctive clothing or equipment;
- required object count.

Do not lock uncertain or invisible properties.

### 2.3 Composition Lock

Use one explicit level:

| Level | Contract |
|---:|---|
| 0 | composition is free |
| 1 | preserve only overall balance and reading direction |
| 2 | preserve placement of major masses and negative space |
| 3 | preserve camera, scale, and major object placement closely |
| 4 | reconstruct composition as closely as the tool and policy allow |

Also record the exact locked elements. A numeric level without element-level explanation is incomplete.

### 2.4 Style Lock

Always set:

```yaml
style_lock:
  style_id: modern-flat
  source: references/style-spec.md
  override_allowed: false
```

User references cannot override this lock.

## 3. Scene Brief

The Scene Brief converts reference analysis into an intentional new-image decision.

Required fields:

- purpose;
- message;
- intended emotion;
- primary subject;
- primary action;
- supporting objects;
- environment;
- moment or state;
- visual center;
- movement and gaze direction;
- foreground, midground, background roles;
- negative-space requirement;
- output use;
- success criteria.

The Scene Brief must not contain generator syntax.

## 4. Composition Specification

Create before the Generation Specification.

Required fields:

- aspect ratio;
- shot scale;
- camera angle;
- subject position;
- subject frame share;
- movement direction;
- secondary-object placement;
- foreground;
- midground;
- background;
- overlaps;
- depth cues;
- negative space;
- safe area;
- allowed crop zones;
- protected crop zones.

Do not describe surface style or material realism in this artifact.

## 5. Generation Specification

The Generation Specification is the canonical contract for one generation attempt.

Required sections:

- metadata and versions;
- subject;
- action;
- environment;
- composition;
- camera;
- geometry;
- depth system;
- lighting;
- gradients and shadows;
- palette roles;
- detail hierarchy;
- preserve list;
- do-not-change list;
- exclude list;
- output requirements;
- adapter requirements.

The final natural-language prompt is compiled from this artifact.

## 6. Precedence

When two requirements conflict, apply this order:

1. safety and rights constraints;
2. explicit current user instruction;
3. Semantic Lock;
4. Identity Lock;
5. protected crop and delivery requirements;
6. Composition Lock;
7. Style Lock invariants;
8. Scene Brief;
9. assigned reference roles;
10. aesthetic preferences.

If a higher-priority requirement makes a lower-priority requirement impossible, record the deviation instead of hiding it.

## 7. Simple flow

Use when the scene has one clear subject, one environment, and no complex identity or edit constraints.

```text
analysis
-> locks
-> scene brief
-> composition spec
-> generation spec
-> preflight
-> generation
-> visual QA
-> accept or one targeted correction
-> delivery
```

## 8. Staged complex flow

Use when the scene has multiple people, precise construction, complex depth, strict composition, or repeated correction risk.

### Pass 1: structural frame

- primary subject;
- camera;
- scale;
- major masses;
- negative space.

### Pass 2: construction

- silhouette;
- anatomy;
- identity-defining structure;
- object count;
- overlaps.

### Pass 3: depth

- foreground;
- midground;
- background;
- atmospheric separation.

### Pass 4: light

- key-light direction;
- rim light;
- cast and contact shadows;
- focal contrast.

### Pass 5: color and volume

- palette roles;
- gradient modeling;
- accent placement;
- tonal hierarchy.

### Pass 6: finish

- edge cleanup;
- local detail;
- crop;
- safe area;
- output quality.

Do not advance to a later pass while an earlier critical defect remains.

## 9. Correction strategy

After visual QA, choose exactly one action:

- `accept` — all gates pass;
- `targeted_correction` — the tool supports local correction and accepted layers can be preserved;
- `regenerate` — the error is structural, the tool cannot edit reliably, or multiple critical layers failed;
- `fail` — the required capability or source evidence is unavailable.

A correction request must state:

- diagnosed error category;
- observed defect;
- target state;
- preserved layers;
- forbidden collateral changes.

## 10. Completion

The workflow is not complete until the output-delivery contract passes.
