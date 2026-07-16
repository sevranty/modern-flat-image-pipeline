from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from validation_common import Finding, KEBAB_RE, load_yaml, main_guard, print_findings

CAPABILITY_KEYS = {
    "text_to_image",
    "reference_conditioned_generation",
    "reference_image_editing",
    "multiple_references",
    "mask_or_inpainting",
    "exact_aspect_ratio",
    "exact_pixel_size",
    "transparent_background",
    "deterministic_seed",
    "output_formats",
    "returns_inspectable_image",
}


def validate_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        doc = load_yaml(path)
    except ValueError as exc:
        return [Finding("ADAPTER-YAML-001", path.as_posix(), str(exc), "restore valid adapter YAML")]
    if not isinstance(doc, dict):
        return [Finding("ADAPTER-SCHEMA-001", path.as_posix(), "top level must be a mapping", "use a YAML mapping")]
    profiles = doc.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        return [Finding("ADAPTER-SCHEMA-002", path.as_posix(), "`profiles` must be a non-empty list", "add at least one adapter profile")]
    seen: set[str] = set()
    for index, profile in enumerate(profiles):
        item_path = f"{path.as_posix()}#profiles[{index}]"
        if not isinstance(profile, dict):
            findings.append(Finding("ADAPTER-SCHEMA-003", item_path, "profile must be a mapping", "replace it with a mapping"))
            continue
        adapter_id = profile.get("adapter_id")
        if not isinstance(adapter_id, str) or not KEBAB_RE.fullmatch(adapter_id):
            findings.append(Finding("ADAPTER-ID-001", item_path, "adapter ID must be stable ASCII kebab-case", "set a unique kebab-case adapter_id"))
        elif adapter_id in seen:
            findings.append(Finding("ADAPTER-ID-002", item_path, f"duplicate adapter ID `{adapter_id}`", "use one unique adapter ID"))
        else:
            seen.add(adapter_id)
        caps = profile.get("capabilities")
        if not isinstance(caps, dict):
            findings.append(Finding("ADAPTER-CAP-001", item_path, "missing capabilities mapping", "add all capability keys"))
            continue
        missing = sorted(CAPABILITY_KEYS - set(caps))
        if missing:
            findings.append(Finding("ADAPTER-CAP-002", item_path, f"missing capability keys: {', '.join(missing)}", "declare every supported capability explicitly"))
        invented = sorted(set(caps) - CAPABILITY_KEYS)
        if invented:
            findings.append(Finding("ADAPTER-CAP-003", item_path, f"invented capability keys: {', '.join(invented)}", "remove unsupported capability keys"))
        true_caps = [key for key, value in caps.items() if key != "output_formats" and value is True]
        if caps.get("output_formats"):
            true_caps.append("output_formats")
        evidence = profile.get("evidence")
        if true_caps:
            if not isinstance(evidence, dict) or not evidence.get("date") or not evidence.get("source"):
                findings.append(Finding("ADAPTER-EVIDENCE-001", item_path, "true capabilities require dated source evidence", "add evidence.date and evidence.source or set unverified capabilities to false"))
        if not profile.get("fallback_impact"):
            findings.append(Finding("ADAPTER-FALLBACK-001", item_path, "profile lacks fallback impact", "record unsupported capability fallback effects"))
        if caps.get("returns_inspectable_image") is False and "delivery" in " ".join(str(v).lower() for v in profile.values()) and "do not claim generated-image delivery" not in " ".join(str(v).lower() for v in profile.values()):
            findings.append(Finding("ADAPTER-DELIVERY-001", item_path, "non-inspectable profile must not imply image delivery", "state that generated-image delivery is not claimed"))
    return findings


def run() -> int:
    parser = argparse.ArgumentParser(description="Validate generator adapter capability evidence.")
    parser.add_argument("path", nargs="?", type=Path, default=Path("skills/modern-flat-image-pipeline/assets/adapters/profiles.yaml"))
    args = parser.parse_args()
    return print_findings(validate_file(args.path))


if __name__ == "__main__":
    main_guard(run)
