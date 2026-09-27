# Presento asset-provider contract fixtures

Issue: MFP#41

Repository-only contract cases for the optional Presento boundary. No paid provider calls, secrets, uploads, or runtime dependency are required.

## Successful result

Required provenance:

- exact provider revision;
- canonical configuration SHA-256 as 64 lowercase hexadecimal characters;
- materialized asset path owned by MFP;
- asset checksum as `sha256:` plus 64 lowercase hexadecimal characters.

Expected outcome: `accepted`.

## Missing provider revision

Expected outcome: `rejected` with stable reason `missing_provider_revision`.

## Invalid configuration digest

Expected outcome: `rejected` with stable reason `invalid_config_sha256`.

## Missing materialized asset provenance

Asset path or checksum is absent.

Expected outcome: `rejected` with stable reason `missing_asset_provenance`.

## Provider failure

Provider reports a failure before materialization.

Expected outcome: machine-readable failure with a stable error code and no fabricated asset path or checksum.

## Ownership invariant

MFP retains visual-generation and runtime ownership in every case. Presento is an optional caller-side integration boundary, not a runtime dependency of MFP.

Source contract: https://github.com/sevranty/presento/issues/31
Source merge: `3ce75515783cc6c956d43eaaa6dc0600a434a1e4`.
