# Decision log

## ADR-001: Internal style source

**Decision:** Modern Flat is defined by the internal style contract. User references cannot redefine the style.

**Reason:** Content and style must remain independently controllable. Reference-derived styling creates drift and makes outputs irreproducible.

## ADR-002: Generation Specification as source of truth

**Decision:** The Generation Specification is canonical. Natural-language prompts are compiled outputs.

**Reason:** A structured contract is easier to inspect, validate, adapt, and test than one long prompt.

## ADR-003: Generator-independent core

**Decision:** The runtime core cannot depend on one image model, private endpoint, CLI, seed format, or parameter vocabulary.

**Reason:** Host environments expose different image capabilities. Adapter logic must remain replaceable.

## ADR-004: Mandatory visual QA

**Decision:** The actual returned image must be inspected after every generation or edit.

**Reason:** Prompt correctness does not prove image correctness.

## ADR-005: Targeted correction

**Decision:** Correct one diagnosed error family at a time while preserving accepted layers whenever the tool supports local editing.

**Reason:** Full regeneration introduces uncontrolled regressions.

## ADR-006: User-visible delivery gate

**Decision:** Tool success is insufficient. The final image must be shown to the user.

**Reason:** An image left only in tool output or internal state is a failed deliverable.

## ADR-007: No embedded external identity system

**Decision:** The core skill contains no built-in third-party logos, corporate palettes, or unrelated domain-specific identity rules.

**Reason:** The project is a general Modern Flat pipeline. External identity can be supplied as an explicit task input and handled under the rights policy.

## ADR-008: Personal artist names are not style primitives

**Decision:** Describe formal visual characteristics instead of using a living artist's name as a shortcut.

**Reason:** Formal specifications are more precise, testable, portable, and respectful of authorship boundaries.

## ADR-009: WebFactoryOS is orchestration-only

**Decision:** MFP owns its runtime, contracts, assets, validators, tests, Issues, pull requests, tags, and releases. WebFactoryOS may own only external registry, routing, relations, naming, and orchestration status. `grants_write_access` is false.

**Reason:** External orchestration must not become a runtime dependency or override the repository source of truth.

## ADR-010: Evidence can be explicitly unavailable

**Decision:** Every normative visual anchor has one evidence record. A record may be published or unavailable. Unavailable records require a reason and unblock condition and never count as visual proof.

**Reason:** Complete evidence accounting is preferable to fabricated, unclear-rights, or provenance-free images.

## ADR-011: Adapter capabilities are evidence-gated

**Decision:** A profile capability may be true only when backed by a dated public contract or recorded successful operation. Unverified tools remain unavailable and the core skill keeps its no-image-tool fallback.

**Reason:** Generator claims drift quickly and unsupported capabilities can break locks or create false completion claims.

## ADR-012: Repository Social preview is non-blocking release metadata

**Decision:** Installation and public verification of the repository Social preview are tracked only in MFP#12 as an independent owner-side follow-up. They do not block repository changes, validation, merge, tag creation, GitHub Release publication, or closure of MFP#21.

**Reason:** Social preview is presentation metadata managed through repository Settings. It does not change package bytes, runtime behavior, validation semantics, compatibility, provenance, or release integrity. Coupling it to the critical release path delays verified data without improving the released artifact.
