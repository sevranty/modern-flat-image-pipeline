# WebFactoryOS orchestration boundary

```text
PROJECT_ID: MODERN_FLAT_IMAGE_PIPELINE
SHORT_ID: MFP
grants_write_access: false
```

## Ownership

MFP is the execution and source-of-truth repository for the skill runtime, Modern Flat contracts, prompt and QA rules, assets, tests, validators, local Issues and pull requests, tags, and releases.

WebFactoryOS owns only external registry, routing, relations, naming, and orchestration status. It cannot override MFP files, move MFP release state, or write to this repository.

## Dependency boundary

MFP has no build, runtime, validation, packaging, or release dependency on WebFactoryOS. The repository must remain installable, testable, and releasable when WebFactoryOS is unavailable.

Caveman is a communication reference only. It is not installed, imported, vendored, or required at runtime.

## Handoff

External orchestration may link to an MFP Issue or pull request. Execution still follows the local `TASK_CONTEXT`, `AGENTS.md`, repository validators, branch policy, and protected resources.

A handoff is valid only when it identifies the exact MFP task, repository, branch or base SHA, WRITE_SCOPE, protected resources, and DONE_WHEN. External metadata never grants write access.

## Verification

```bash
python3 scripts/validate_repository.py .
```

Review must confirm no WebFactoryOS import, workflow call, copied registry, credential, absolute local path, or cross-repository write was added.
