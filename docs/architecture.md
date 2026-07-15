# Architecture

## 1. Purpose

`modern-flat-image-pipeline` is a single-purpose Agent Skill for converting visual references into new Modern Flat illustrations through a repeatable, inspectable workflow.

The repository separates:

- runtime orchestration;
- style definition;
- semantic and composition contracts;
- generator adaptation;
- quality assurance;
- user-visible delivery;
- evaluation and packaging.

## 2. Core boundary

The skill owns decisions and orchestration. It does not own an image model.

```text
skill-owned
  reference analysis
  locks
  scene brief
  style contract
  prompt compilation
  quality gates
  correction strategy
  delivery verification

tool-owned
  image generation
  reference-conditioned editing
  masking or inpainting
  resizing or export capabilities
```

A successful tool call is not a successful skill run. Completion requires inspection of the returned image and visible delivery to the user.

## 3. Canonical runtime flow

```text
INPUT
-> INPUT_GATE
-> REFERENCE_ANALYSIS
-> REFERENCE_MAP
-> LOCKS
-> SCENE_BRIEF
-> STYLE_CONTRACT
-> COMPOSITION_SPEC
-> GENERATION_SPEC
-> PREFLIGHT_GATE
-> CAPABILITY_ROUTING
-> GENERATE_OR_EDIT
-> VISUAL_QA
-> ACCEPT | TARGETED_CORRECTION | REGENERATE | FAIL
-> FINAL_GATE
-> USER_VISIBLE_DELIVERY
```

## 4. Layer model

### Layer A: runtime orchestration

`skills/modern-flat-image-pipeline/SKILL.md`

Contains only required order, branching, reference-loading instructions, failure handling, and completion criteria.

### Layer B: canonical references

`skills/modern-flat-image-pipeline/references/`

Contains detailed contracts. Each rule has exactly one canonical owner.

### Layer C: machine-readable templates

`skills/modern-flat-image-pipeline/assets/templates/`

Contains stable field structures for intermediate artifacts. Templates are contracts, not example answers.

### Layer D: adapters

`references/generator-adapters.md`

Maps the canonical Generation Specification to available tool capabilities. Adapter rules cannot redefine the style or semantic contract.

### Layer E: evaluation

`tests/` and `assets/anchors/` are deferred to the evaluation task. They validate the end-to-end behavior without becoming runtime dependencies.

### Layer F: packaging

Plugin manifest, release metadata, installation, and distribution remain separate from the runtime behavior.

## 5. Source-of-truth matrix

| Rule family | Canonical owner | May reference | Must not redefine |
|---|---|---|---|
| Runtime sequence | `SKILL.md` | all references | detailed style or QA rules |
| Style | `style-spec.md` | prompt and QA files | runtime order |
| Reference interpretation | `reference-analysis.md` | locks | style definition |
| Locks and intermediate contracts | `workflow-and-locks.md` | templates | generator syntax |
| Prompt compilation | `prompt-patterns.md` | style and locks | semantic decisions |
| Quality | `quality-gates.md` | style and delivery | generator capabilities |
| Delivery | `output-delivery.md` | quality gates | image-generation behavior |
| Tool routing | `generator-adapters.md` | generation spec | style or meaning |
| Rights and sensitive inputs | `safety-and-rights.md` | reference analysis and QA | runtime sequence |

## 6. Dependency direction

```text
SKILL.md
  -> reference-analysis.md
  -> workflow-and-locks.md
  -> style-spec.md
  -> prompt-patterns.md
  -> generator-adapters.md
  -> quality-gates.md
  -> output-delivery.md
  -> safety-and-rights.md
```

Reference files must not form circular normative dependencies. Cross-links may explain context but cannot create competing sources of truth.

## 7. Runtime state

The runtime workflow uses explicit intermediate artifacts:

- Reference Analysis Card;
- Reference Map;
- Locks;
- Scene Brief;
- Composition Specification;
- Generation Specification;
- QA Report;
- Delivery Record.

The Generation Specification is the source of truth for a generation attempt. The final natural-language prompt is a compiled representation and may vary by generator adapter.

## 8. Error model

Errors are classified before correction. The runtime never uses a generic instruction such as "make it better".

Correction priority:

1. semantics;
2. identity;
3. composition and camera;
4. silhouette, anatomy, and construction;
5. geometry and depth layers;
6. lighting and shadows;
7. gradients and palette;
8. detail, crop, and technical finish.

## 9. Completion contract

A run is complete only when:

- the final candidate passes all critical gates;
- the actual image has been inspected;
- the final candidate is distinguishable from intermediate attempts;
- the image is visible to the user;
- the response does not falsely claim unavailable capabilities.

## 10. Deferred modules

The following are intentionally outside this implementation slice:

- plugin manifest and distribution release;
- automated visual similarity scoring;
- a production golden set;
- repository social preview;
- full public README;
- generator-specific executable integrations.
