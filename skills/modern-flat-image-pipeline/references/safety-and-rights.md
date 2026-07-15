# Safety, rights, identity, text, and private-data rules

## 1. Purpose

Provide a policy layer for references that contain people, external identity assets, exact text, private information, screenshots, or recognizable authorial styling.

Apply the current host platform's safety policy first. This document adds workflow rules; it does not replace platform policy.

## 2. People

Classify the depicted person when relevant:

- fictional or synthetic person;
- the user;
- private third party;
- public person;
- child.

Do not identify an unknown real person from an image.

### Identity preservation

- Preserve identity only when the user requests it, sufficient reference evidence exists, and the host capability and policy allow it.
- Do not promise exact likeness.
- Record uncertain or occluded facial features as unknown.
- Do not infer sensitive attributes from appearance.
- Do not add health, religion, ethnicity, politics, sexuality, disability, criminality, or other sensitive claims not explicitly and appropriately provided.

### User likeness

When the requested output depicts the user, require a usable current-conversation image before attempting a likeness-preserving transformation, following host requirements.

### Children

- Keep depiction age-appropriate.
- Avoid adult styling, sexualization, dangerous context, or unverified identity claims.
- Use stricter anatomy and context review.

### Human QA

Always inspect:

- face integrity;
- hands and fingers;
- limb count;
- joints and posture;
- age consistency;
- body merging or duplication;
- unintended emotional expression changes.

## 3. Authorial style

When a reference is an illustration or artwork:

- extract formal principles such as geometry, composition, palette relationships, edge behavior, light, and depth;
- do not use a living artist's name as a style shortcut;
- do not recreate a recognizable personal signature style as the governing output style;
- keep the output under the canonical Modern Flat contract;
- preserve content or composition only through explicit reference roles.

If a user asks for a named style, translate the request into high-level visual characteristics compatible with Modern Flat and the host policy.

## 4. External identity assets

External identity assets include:

- logos;
- wordmarks;
- seals;
- trademarks;
- badges;
- product marks;
- proprietary interface graphics;
- recognizable campaign assets.

Rules:

- Do not transfer them automatically from a reference.
- Do not generate an approximate replacement when exactness matters.
- Prefer a separate, authorized asset and a post-processing step.
- Keep the core generation free of unrequested logos and watermarks.
- Record whether the user supplied the asset and whether its use is required.
- Do not embed any external identity system as a default of this repository.

## 5. Exact text

Image generators may distort text. When exact text matters:

1. generate the illustration without text;
2. reserve negative space and safe area;
3. add text in a separate editable layer or tool;
4. verify spelling, punctuation, language, contrast, and crop;
5. inspect the final composite.

Treat accidental pseudo-text as a defect.

Do not quote or reproduce private text from a reference unless necessary and explicitly requested.

## 6. Screenshots and interfaces

Before using a screenshot:

- identify private names, messages, account details, balances, IDs, addresses, tokens, QR codes, card numbers, document numbers, and internal URLs;
- remove, replace, blur, or abstract private data;
- distinguish interface layout from real user data;
- avoid copying proprietary interface artwork when only structure is needed;
- do not invent credible-looking sensitive values.

## 7. Documents and private information

Do not transfer:

- personal identifiers;
- financial account information;
- credentials or secrets;
- private correspondence;
- medical information;
- internal company information;
- confidential document content;

unless the request requires it, the user is authorized, and the host policy allows it. Prefer abstraction and anonymization.

## 8. Reference rights record

For externally sourced references, record when practical:

```yaml
reference_id: reference-01
source: ""
provided_by_user: true
intended_roles: []
rights_or_permission_note: ""
redistribution_allowed: unknown
public_golden_set_allowed: false
```

Unknown redistribution rights block committing the source image to a public anchor or example set.

## 9. Generated output rights hygiene

- Do not add watermarks that imply a third-party source.
- Do not preserve an original signature.
- Do not present a derivative as an official asset of an external entity.
- Keep research references out of public repository assets unless permission is clear.
- Maintain source notes for assets used in public examples.

## 10. Policy conflict behavior

When the requested transformation conflicts with safety, privacy, or rights constraints:

- preserve the valid part of the request;
- explain the blocked element briefly;
- offer a safer abstraction when appropriate;
- do not bypass the constraint through a different generator adapter;
- record the restriction before generation.

## 11. QA additions

Add these checks when relevant:

- identity evidence sufficient;
- no unsupported sensitive attributes;
- no unknown-person identification;
- no private data leakage;
- exact text handled separately;
- external identity assets authorized and correctly sourced;
- no accidental pseudo-text;
- no signature or watermark transfer;
- no protected reference committed to public assets without clear permission.
