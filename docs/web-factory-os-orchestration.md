# WebFactoryOS orchestration boundary

This document is the only local source of truth for the MFP#20 WebFactoryOS orchestration boundary.

## Task identity

- Project: `MODERN_FLAT_IMAGE_PIPELINE`
- Short ID: `MFP`
- Task: `MFP-020`
- Exact base head: `c2347f2c63c1f34a30e019c4aefbbca72a7f1d94`
- Local onboarding branch: `onboarding/mfp-020-web-factory-os`
- Write access granted to WebFactoryOS: `grants_write_access=false`

## Ownership boundary

Modern Flat Image Pipeline remains the autonomous execution and source-of-truth repository.

MFP owns:

- skill and plugin source code;
- Modern Flat style, workflow, prompt, QA, delivery, adapter, and rights contracts;
- assets, templates, anchor specifications, tests, fixtures, and validators;
- package versions, changelog entries, tags, releases, and release readiness;
- local issues, pull requests, review decisions, and protected resource changes.

WebFactoryOS owns only external orchestration metadata:

- broker availability signals;
- registry entries;
- routing decisions;
- task relations and lookups;
- shared naming records;
- orchestration status.

WebFactoryOS metadata, including broker state, is not an authority over MFP runtime behavior, validation semantics, package contents, repository permissions, or release state.

## Dependency boundary

MFP must not gain a build, runtime, validation, or release dependency on WebFactoryOS.

MFP must not import, call, vendor, or require WebFactoryOS code, broker services, configuration, services, CLIs, schemas, registries, or generated files for normal repository operation.

MFP also must not gain a runtime dependency on `caveman`. Caveman principles may inform short operational output, but no Caveman package, hook, schema, import, or executable is part of this repository contract.

## Protected resources

MFP#20 does not authorize changes to:

- `skills/modern-flat-image-pipeline/**`;
- `.codex-plugin/plugin.json`;
- `tests/**`;
- `scripts/**`;
- `assets/**`;
- tags, releases, or repository settings;
- scopes owned by MFP#21, MFP#22, or MFP#23;
- the `sevranty/web-factory-os` repository.

## Broker boundary

- External WFO brokers may coordinate task readiness, but they do not approve, block, or replace local repository review.
- Missing broker signals must be treated as external orchestration latency, not as evidence that MFP contracts changed or validation passed.
- If a broker is unavailable, hold only the cross-repository handoff; continue local review, diff inspection, and offline validation.

## Handoff rules

- Keep one canonical file per detailed rule.
- Link to this document for WFO orchestration boundaries instead of copying registry facts or WFO schemas into MFP files.
- Cross-repository references are informational unless an MFP maintainer explicitly changes local repository contracts.
- Static validation remains local and offline: `python3 scripts/validate_repository.py .`.
- Full review must include the complete diff and a check that no secrets, local absolute paths, WFO runtime hooks, package-version changes, or cross-repository writes were introduced.
