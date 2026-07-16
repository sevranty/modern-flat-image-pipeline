# Adapter capability profiles

`capability-profiles.yaml` is the evidence-gated registry for generator and editor routes.

A verified profile records:

- stable `adapter_id`;
- tool and model or mode;
- verification status, date, evidence type, and source;
- every required capability as an explicit boolean;
- limitations;
- Semantic, Identity, Composition, and delivery fallbacks;
- `false_delivery_claim_allowed: false`.

A capability may be `true` only when supported by a dated public contract or a recorded successful operation. Repository prose alone cannot prove a tool capability.

Host-dependent or unverified tools stay in `unavailable_profiles` with a reason and unblock condition. The canonical v0.1.0 verified route is the no-image-tool fallback, which produces contracts and a capability-gap report without claiming image creation.

Validate the registry and fixtures with:

```bash
python3 scripts/validate_repository.py .
```
