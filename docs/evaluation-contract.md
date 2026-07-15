# Evaluation contract

```text
eval_version: 0.1.0
```

## Purpose

Validate the end-to-end decision pipeline independently from generator wording and without treating prompt-marker presence as proof of image quality.

## Evaluation layers

```text
fixture resolution
-> reference role assignment
-> lock validation
-> Scene Brief expectations
-> prompt semantic coverage
-> QA findings
-> quality band
-> runtime action
-> delivery state
```

## Canonical values

Quality bands:

```text
accept
local_correction
required_iteration
reject
```

Runtime actions:

```text
accept
targeted_correction
regenerate
fail
```

Composition Lock levels are integers from `0` through `4`.

Style Lock must always be:

```yaml
style_id: modern-flat
style_override_allowed: false
```

## Case completeness

Every case must include:

- stable ASCII `case_id`;
- one or more resolvable fixture IDs;
- a concrete user request;
- reference roles;
- expected locks;
- required prompt semantics;
- forbidden prompt semantics;
- expected quality band;
- expected runtime action.

Rejected cases must additionally include:

- expected QA findings;
- one primary diagnostic category;
- one or more critical rejection criteria.

## Golden anchors

The golden set is split into `accepted` and `rejected` catalogs. Anchor specifications are normative. Visual evidence can be attached later only with provenance and completed QA.

## Change control

Increment `eval_version` when:

- adding or removing required case fields;
- changing expected decisions;
- changing canonical enum values;
- changing anchor acceptance or rejection logic;
- adding a new mandatory regression family.

Adding a backward-compatible case or fixture increments the minor version. Correcting wording without changing expected behavior increments the patch version.
