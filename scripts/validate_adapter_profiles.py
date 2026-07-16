from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from validation_common import Finding, KEBAB_RE, load_yaml, main_guard, print_findings

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED_CAPABILITIES = {
    "text_to_image",
    "reference_conditioned_generation",
    "reference_image_editing",
    "multiple_references",
    "mask_or_inpainting",
    "exact_aspect_ratio",
    "exact_pixel_size",
    "transparent_background",
    "deterministic_seed",
    "returns_inspectable_image",
}
REQUIRED_FALLBACKS = {"semantic_lock", "identity_lock", "composition_lock", "delivery"}
TRUE_EVIDENCE_TYPES = {"public_contract", "successful_operation"}
ALL_EVIDENCE_TYPES = TRUE_EVIDENCE_TYPES | {"repository_contract"}


def _mapping(path: Path) -> tuple[dict[str, Any] | None, list[Finding]]:
    try:
        data = load_yaml(path)
    except ValueError as exc:
        return None, [Finding("ADAPTER-YAML-001", path.as_posix(), str(exc), "restore valid UTF-8 YAML")]
    if not isinstance(data, dict):
        return None, [Finding("ADAPTER-YAML-002", path.as_posix(), "top level must be a mapping", "use a YAML mapping")]
    return data, []


def validate(path: Path) -> list[Finding]:
    path = path.resolve()
    document, findings = _mapping(path)
    if findings:
        return findings
    assert document is not None

    profiles = document.get("profiles")
    unavailable = document.get("unavailable_profiles")
    if not isinstance(profiles, list):
        findings.append(Finding("ADAPTER-PROFILE-001", path.as_posix(), "profiles must be a list", "define a profiles list"))
        profiles = []
    if not isinstance(unavailable, list):
        findings.append(Finding("ADAPTER-UNAVAILABLE-001", path.as_posix(), "unavailable_profiles must be a list", "define unavailable profiles explicitly"))
        unavailable = []

    seen: set[str] = set()
    for index, profile in enumerate(profiles):
        item_path = f"{path.as_posix()}#profiles[{index}]"
        if not isinstance(profile, dict):
            findings.append(Finding("ADAPTER-PROFILE-002", item_path, "profile must be a mapping", "replace it with a profile mapping"))
            continue
        adapter_id = profile.get("adapter_id")
        if not isinstance(adapter_id, str) or not KEBAB_RE.fullmatch(adapter_id):
            findings.append(Finding("ADAPTER-ID-001", item_path, "adapter_id must be ASCII kebab-case", "set a stable adapter_id"))
            continue
        if adapter_id in seen:
            findings.append(Finding("ADAPTER-ID-002", item_path, f"duplicate adapter_id `{adapter_id}`", "keep one profile per adapter_id"))
        seen.add(adapter_id)

        for key in ("tool_name", "model_or_mode"):
            if not isinstance(profile.get(key), str) or not profile[key].strip():
                findings.append(Finding("ADAPTER-PROFILE-003", item_path, f"missing non-empty `{key}`", f"record {key}"))

        verification = profile.get("verification")
        if not isinstance(verification, dict):
            findings.append(Finding("ADAPTER-EVIDENCE-002", item_path, "profile lacks verification evidence", "add verification status, date, type, and source"))
            verification = {}
        evidence_type = verification.get("evidence_type")
        source = verification.get("source")
        if verification.get("status") != "verified":
            findings.append(Finding("ADAPTER-EVIDENCE-003", item_path, "profile verification status must be verified", "verify the profile or move it to unavailable_profiles"))
        if not isinstance(verification.get("verified_at"), str) or not DATE_RE.fullmatch(verification["verified_at"]):
            findings.append(Finding("ADAPTER-EVIDENCE-004", item_path, "verified_at must be YYYY-MM-DD", "record the verification date"))
        if evidence_type not in ALL_EVIDENCE_TYPES:
            findings.append(Finding("ADAPTER-EVIDENCE-005", item_path, f"invalid evidence_type `{evidence_type}`", f"use one of {sorted(ALL_EVIDENCE_TYPES)}"))
        if not isinstance(source, str) or not source.strip():
            findings.append(Finding("ADAPTER-EVIDENCE-006", item_path, "verification source is missing", "record a contract path, public URL, or operation record"))

        capabilities = profile.get("capabilities")
        if not isinstance(capabilities, dict):
            findings.append(Finding("ADAPTER-CAPABILITY-001", item_path, "capabilities must be a mapping", "define every required boolean capability"))
            capabilities = {}
        missing = sorted(REQUIRED_CAPABILITIES - set(capabilities))
        extra = sorted(set(capabilities) - REQUIRED_CAPABILITIES)
        if missing:
            findings.append(Finding("ADAPTER-CAPABILITY-002", item_path, f"missing capabilities: {', '.join(missing)}", "define every required capability"))
        if extra:
            findings.append(Finding("ADAPTER-CAPABILITY-003", item_path, f"unknown capabilities: {', '.join(extra)}", "remove or version new capability fields"))
        if any(not isinstance(value, bool) for value in capabilities.values()):
            findings.append(Finding("ADAPTER-CAPABILITY-004", item_path, "all capability values must be booleans", "replace inferred or unknown strings with false and document the limitation"))
        if any(value is True for value in capabilities.values()):
            if evidence_type not in TRUE_EVIDENCE_TYPES:
                findings.append(Finding("ADAPTER-EVIDENCE-001", item_path, "true capabilities require a public contract or successful-operation record", "add qualifying evidence or set unsupported capabilities to false"))
            if not isinstance(source, str) or not (source.startswith("https://") or source.startswith("operation_record:")):
                findings.append(Finding("ADAPTER-EVIDENCE-007", item_path, "true capabilities require a public URL or operation_record source", "record inspectable evidence"))

        fallbacks = profile.get("fallbacks")
        if not isinstance(fallbacks, dict):
            findings.append(Finding("ADAPTER-FALLBACK-001", item_path, "fallbacks must be a mapping", "define lock and delivery fallbacks"))
            fallbacks = {}
        missing_fallbacks = sorted(REQUIRED_FALLBACKS - set(fallbacks))
        if missing_fallbacks:
            findings.append(Finding("ADAPTER-FALLBACK-002", item_path, f"missing fallbacks: {', '.join(missing_fallbacks)}", "define every required fallback"))
        for key in REQUIRED_FALLBACKS & set(fallbacks):
            if not isinstance(fallbacks[key], str) or not fallbacks[key].strip():
                findings.append(Finding("ADAPTER-FALLBACK-003", item_path, f"fallback `{key}` must be non-empty", "record the explicit fallback effect"))

        if profile.get("false_delivery_claim_allowed") is not False:
            findings.append(Finding("ADAPTER-DELIVERY-001", item_path, "false delivery claims must never be allowed", "set false_delivery_claim_allowed to false"))

    for index, item in enumerate(unavailable):
        item_path = f"{path.as_posix()}#unavailable_profiles[{index}]"
        if not isinstance(item, dict):
            findings.append(Finding("ADAPTER-UNAVAILABLE-002", item_path, "unavailable profile must be a mapping", "replace it with an unavailable profile mapping"))
            continue
        adapter_id = item.get("adapter_id")
        if not isinstance(adapter_id, str) or not KEBAB_RE.fullmatch(adapter_id):
            findings.append(Finding("ADAPTER-ID-003", item_path, "adapter_id must be ASCII kebab-case", "set a stable adapter_id"))
            continue
        if adapter_id in seen:
            findings.append(Finding("ADAPTER-ID-004", item_path, f"adapter_id `{adapter_id}` exists in more than one state", "keep it verified or unavailable, not both"))
        seen.add(adapter_id)
        if not isinstance(item.get("reason"), str) or not item["reason"].strip():
            findings.append(Finding("ADAPTER-UNAVAILABLE-003", item_path, "unavailable profile lacks a reason", "add reason"))
        if not isinstance(item.get("unblock_condition"), str) or not item["unblock_condition"].strip():
            findings.append(Finding("ADAPTER-UNAVAILABLE-004", item_path, "unavailable profile lacks an unblock condition", "add unblock_condition"))

    return findings


def run() -> int:
    parser = argparse.ArgumentParser(description="Validate evidence-gated generator adapter profiles.")
    parser.add_argument("path", nargs="?", type=Path, default=Path("skills/modern-flat-image-pipeline/assets/adapters/capability-profiles.yaml"))
    args = parser.parse_args()
    return print_findings(validate(args.path))


if __name__ == "__main__":
    main_guard(run)
