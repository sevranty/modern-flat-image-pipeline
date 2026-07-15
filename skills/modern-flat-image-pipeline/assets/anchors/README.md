# Golden anchor set

```text
eval_version: 0.1.0
anchor_status: specification_ready
```

The initial golden set contains twelve scene-level anchor specifications:

- six accepted targets;
- six rejected targets.

Each anchor records the related regression case, scene intent, palette or failure characteristics, acceptance or rejection reasons, diagnostic category, and expected runtime action.

## Why the first set is specification-based

The core repository does not bundle an image model. Committing arbitrary generated images before a verified generator run would create unverifiable provenance and misleading visual claims. The v0.1.0 anchors therefore define the exact contracts that future candidate images must satisfy.

A visual anchor may be added only when:

- its source and generation path are recorded;
- redistribution is permitted;
- the image is free from third-party logos, signatures, private data, and copied identity systems;
- the candidate has a completed QA scorecard;
- the file is linked to one existing `anchor_id`;
- accepted and rejected states remain clearly separated.

The specification anchors are normative for evaluation. Future image files are evidence attached to those contracts, not replacements for them.
