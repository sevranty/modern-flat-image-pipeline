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

The golden set is split into `accepted` and `rejected` catalogs. Anchor specifications are normative.

`skills/modern-flat-image-pipeline/assets/anchors/evidence.yaml` tracks one evidence state for every anchor. Published evidence must carry a repository-relative asset, matching SHA-256, dimensions, format, provenance, redistribution rights, tool or model record, prompt or Generation Specification, and completed QA. Unavailable evidence must carry an exact reason and unblock condition.

An unavailable record is valid evidence accounting, not visual proof. Static validation must never convert an unavailable record into an accepted image claim.

## Adapter evidence

`skills/modern-flat-image-pipeline/assets/adapters/capability-profiles.yaml` is the profile registry. A capability may be `true` only when backed by a dated public contract or a recorded successful operation. Host-dependent or unverified tools remain in `unavailable_profiles` with a reason and unblock condition.

Adapter profile evidence does not redefine the Scene Brief, locks, style contract, prompt semantics, QA rules, or delivery gate.

## Change control

Increment `eval_version` when:

- adding or removing required case fields;
- changing expected decisions;
- changing canonical enum values;
- changing anchor acceptance or rejection logic;
- adding a new mandatory regression family.

Adding evidence accounting or adapter validation without changing normative case decisions does not by itself change `eval_version`.

Adding a backward-compatible case or fixture increments the minor version. Correcting wording without changing expected behavior increments the patch version.
