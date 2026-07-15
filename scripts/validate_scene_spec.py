from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from validation_common import Finding, load_yaml, main_guard, nested_get, normalize_text, print_findings

REQUIRED_PATHS = {
    "subject.primary": "SCENE-REQ-001",
    "action": "SCENE-REQ-002",
    "composition.aspect_ratio": "SCENE-REQ-003",
    "composition.camera_angle": "SCENE-REQ-004",
    "style_system.geometry": "SCENE-REQ-005",
    "style_system.lighting": "SCENE-REQ-006",
    "style_system.palette_roles.neutral_base": "SCENE-REQ-007",
    "style_system.palette_roles.dominant_group": "SCENE-REQ-008",
    "style_system.palette_roles.supporting_group": "SCENE-REQ-009",
    "style_system.palette_roles.focal_accent": "SCENE-REQ-010",
    "preserve": "SCENE-REQ-011",
    "exclude": "SCENE-REQ-012",
    "output_requirements.format": "SCENE-REQ-013",
}

CONFLICT_PAIRS = (
    ("photorealistic", "non-photorealistic"),
    ("transparent background", "opaque background"),
    ("no shadows", "layered shadows"),
    ("flat fills only", "volumetric gradients"),
)


def is_missing(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def validate(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        data = load_yaml(path)
    except ValueError as exc:
        return [Finding("SCENE-PARSE-001", path.as_posix(), str(exc), "fix the YAML syntax and encoding")]
    if not isinstance(data, dict):
        return [Finding("SCENE-TYPE-001", path.as_posix(), "top-level value must be a mapping", "use a YAML mapping with the generation-spec fields")]

    for dotted_path, rule_id in REQUIRED_PATHS.items():
        if is_missing(nested_get(data, dotted_path)):
            findings.append(Finding(rule_id, path.as_posix(), f"missing required field `{dotted_path}`", f"provide a non-empty `{dotted_path}` value"))

    style_id = nested_get(data, "locks.style.style_id")
    override_allowed = nested_get(data, "locks.style.override_allowed")
    if style_id != "modern-flat":
        findings.append(Finding("SCENE-STYLE-001", path.as_posix(), "Style Lock must use `modern-flat`", "set `locks.style.style_id` to `modern-flat`"))
    if override_allowed is not False:
        findings.append(Finding("SCENE-STYLE-002", path.as_posix(), "Style Lock must be non-overridable", "set `locks.style.override_allowed` to false"))

    level = nested_get(data, "locks.composition.level")
    if not isinstance(level, int) or isinstance(level, bool) or level < 0 or level > 4:
        findings.append(Finding("SCENE-COMP-001", path.as_posix(), "Composition Lock level must be an integer from 0 to 4", "set `locks.composition.level` to 0, 1, 2, 3, or 4"))

    visible_text = nested_get(data, "output_requirements.visible_text")
    safe_area = nested_get(data, "composition.safe_area")
    if visible_text not in (None, "", "none", False) and is_missing(safe_area):
        findings.append(Finding("SCENE-SAFE-001", path.as_posix(), "visible text requires an explicit safe area", "define `composition.safe_area` or set visible text to `none`"))

    text = normalize_text(data)
    for left, right in CONFLICT_PAIRS:
        if left in text and right in text:
            findings.append(Finding("SCENE-CONFLICT-001", path.as_posix(), f"contradictory requirements contain both `{left}` and `{right}`", "remove the lower-priority requirement and record the resolved decision"))

    light_text = normalize_text(nested_get(data, "style_system.lighting"))
    directions = [direction for direction in ("from left", "from right", "from above", "from below") if direction in light_text]
    if len(directions) > 1:
        findings.append(Finding("SCENE-LIGHT-001", path.as_posix(), f"multiple key-light directions detected: {', '.join(directions)}", "declare one dominant key-light direction"))

    return findings


def run() -> int:
    parser = argparse.ArgumentParser(description="Validate a Modern Flat Generation Specification YAML file.")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    findings: list[Finding] = []
    for path in args.paths:
        findings.extend(validate(path))
    return print_findings(findings)


if __name__ == "__main__":
    main_guard(run)
