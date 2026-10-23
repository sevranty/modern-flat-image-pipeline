# Presento asset-provider contract fixtures

Issue: MFP#41

Repository-only contract cases for the optional Presento boundary. No paid provider calls, secrets, uploads, or runtime dependency are required.

## Successful result

Required provenance:

- exact provider revision;
- canonical configuration SHA-256 as 64 lowercase hexadecimal characters;
- materialized asset path owned by MFP;
- asset checksum as exactly 64 lowercase hexadecimal characters (no `sha256:` prefix), as implemented by Presento PRE#31.

Expected outcome: `accepted`.

## Missing provider revision

Expected outcome: `rejected` with stable reason `missing_provider_revision`.

## Invalid configuration digest

Expected outcome: `rejected` with stable reason `invalid_config` for non-canonicalizable request config; the adapter calculates `config_sha256` itself rather than accepting an untrusted digest.

## Missing materialized asset provenance

Asset path or checksum is absent.

Expected outcome: `rejected` with stable reason `missing_asset_provenance` for missing or empty files. Escaping the MFP output root is rejected with `invalid_asset_path`.

## Provider failure

Provider reports a failure before materialization.

Expected outcome: machine-readable failure with a stable error code and no fabricated asset path or checksum.

## Ownership invariant

MFP retains visual-generation and runtime ownership in every case. Presento is an optional caller-side integration boundary, not a runtime dependency of MFP.

Source contract: https://github.com/sevranty/presento/issues/31
Source merge: `3ce75515783cc6c956d43eaaa6dc0600a434a1e4`.

## Executable tests

The ten offline positive and negative cases live in `tests/test_presento_asset_provider.py` and run through `scripts/validate_repository.py`. These tests validate the result envelope, real file checksum, canonical config hash, missing revision/file, invalid config, path escape, fake file signatures, provider mismatch, kind mismatch and unsafe request ID. They do not claim visual acceptance of an image.
