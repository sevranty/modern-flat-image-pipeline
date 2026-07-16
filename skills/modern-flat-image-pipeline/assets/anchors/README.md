# Golden anchor set

```text
eval_version: 0.1.0
anchor_status: evidence_tracked
```

The initial golden set contains twelve scene-level anchor specifications:

- six accepted targets;
- six rejected targets.

Each anchor records the related regression case, scene intent, palette or failure characteristics, acceptance or rejection reasons, diagnostic category, and expected runtime action.

## Evidence registry

`evidence.yaml` contains exactly one machine-readable record for every normative anchor.

A record is either:

- `published`, with repository-relative asset path, SHA-256, dimensions, format, provenance, redistribution rights, tool or model record, prompt or Generation Specification, and completed QA; or
- `unavailable`, with an exact reason and unblock condition.

The v0.1.0 registry marks all twelve visual candidates unavailable because no provenance-controlled, rights-cleared generator run has been published. This is an explicit evidence state, not a claim that image evidence exists.

## Publication gate

A visual anchor may be published only when:

- its source and generation path are recorded;
- redistribution is permitted;
- the image is free from third-party logos, signatures, private data, and copied identity systems;
- the candidate has a completed QA scorecard;
- the file is linked to one existing `anchor_id`;
- accepted and rejected states remain clearly separated;
- the recorded SHA-256 matches the committed bytes.

The specification anchors remain normative. Visual files are evidence attached to those contracts, never replacements for them.
