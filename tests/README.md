# Evaluation suite

```text
eval_version: 0.1.0
```

The suite checks the complete contract flow rather than a fixed prompt string.

## Layout

```text
tests/
|-- cases/e2e-cases.yaml
|-- fixtures/reference-descriptors.yaml
`-- expected/decisions.yaml
```

All fixtures are synthetic textual descriptors. They contain no copied images, logos, private data, or external identity assets.

## Required coverage

The twelve cases cover:

- photo reference reinterpretation;
- illustration content transfer without authorial-style copying;
- multi-reference role mapping;
- sketch-driven composition;
- complex person and environment checks;
- machine Identity Lock;
- safe area for separately editable text;
- vertical 9:16 adaptation;
- photorealistic drift;
- glossy CGI drift;
- generic-flat drift;
- missing user-visible delivery.

## Assertion model

A runner must validate:

1. fixture IDs resolve;
2. every case declares expected reference roles and locks;
3. Style Lock is `modern-flat` and non-overridable;
4. required and forbidden semantic markers are present;
5. expected quality band and runtime action use canonical values;
6. every rejected case has a primary diagnostic category and critical defect;
7. the delivery regression fails when `visible_to_user` is false.

The suite does not replace visual QA. When real candidate images are added, they must be inspected against the same case and anchor contracts.
