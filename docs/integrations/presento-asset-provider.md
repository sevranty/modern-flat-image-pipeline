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

This document records contract adoption only; implementation adapter and tests remain required before terminal completion.