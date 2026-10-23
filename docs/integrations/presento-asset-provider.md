# Presento asset-provider boundary

Issue: MFP#41

MFP accepts the optional Presento request/result boundary as an integration adapter contract, not as runtime ownership transfer.

- Request: `presento.asset-provider.request.v1` / `1.0.0`
- Result: `presento.asset-provider.result.v1` / `1.0.0`
- Provider ownership remains in MFP.
- Result must expose provider revision, canonical configuration SHA-256, materialized asset path and checksum.
- Failures must be machine-readable and must not require paid calls or secrets in contract tests.
- No runtime dependency MFP -> Presento is introduced.
- Source: https://github.com/sevranty/presento/issues/31
- Source merge: `3ce75515783cc6c956d43eaaa6dc0600a434a1e4`.

## Offline local adapter

The local adapter is [scripts/presento_asset_provider.py](../../scripts/presento_asset_provider.py). It converts an **already generated and visually reviewed MFP-owned file** to the exact Presento v1 result envelope. It does not generate images, make paid calls, access credentials, import Presento code, or select a generator.

Run the adapter with a valid Presento v1 JSON request, an existing image under the declared MFP output root, and the exact 40-character provider commit revision:

`python3 scripts/presento_asset_provider.py --request request.json --asset assets/output/final.png --asset-root assets/output --provider-revision f6af684d8b1c58e59d5edd6075392376ad86e635`

The example revision is the recorded MFP#41 starting revision; actual calls must supply their own exact current provider revision. The command prints one JSON result to stdout. Failure prints one JSON object with a stable `error.code` and returns nonzero. The asset is never modified.

Successful results contain `provider_revision`, SHA-256 of canonically serialized `config`, exact local file path, and SHA-256 of actual file bytes. Both hashes are 64 lowercase hexadecimal characters **without** a `sha256:` prefix, matching the accepted Presento implementation. An MFP image is not visually accepted by this adapter: normal MFP visual QA and final delivery rules still apply.

Offline checks: `python3 -m unittest discover -s tests -p test_presento_asset_provider.py`, also included in `python3 scripts/validate_repository.py .`.

This is a materialized-asset bridge, not a live generator executor. Full automatic generation and an external runtime end-to-end acceptance remain separate from this repository-only adapter.