from __future__ import annotations

import argparse
import re
from pathlib import Path

from validation_common import Finding, has_all_groups, main_guard, print_findings, read_text

REQUIRED_GROUPS = {
    "geometry": ("planar", "vector-like", "vector like"),
    "gradients": ("volumetric gradient", "dimensional gradient", "gradient modeling", "gradient modelling"),
    "shadows": ("layered shadow", "cast shadow", "contact shadow"),
    "directional_light": ("directional light", "directional key light", "consistent key light"),
    "non_photorealistic": ("non-photorealistic", "non photorealistic", "not photorealistic"),
    "anti_drift": ("exclude", "do not", "avoid", "without"),
}

FORBIDDEN_PATTERNS = {
    "PROMPT-DRIFT-001": re.compile(r"(?i)\bphotorealistic\b|\bhyperrealistic\b"),
    "PROMPT-DRIFT-002": re.compile(r"(?i)\bglossy\s+(?:3d\s+)?cgi\b|\bchrome\b|ray[- ]traced reflections?"),
    "PROMPT-ARTIST-001": re.compile(r"(?i)\b(?:in the style of|style of|as painted by|inspired by)\s+[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+){0,3}"),
    "PROMPT-BRAND-001": re.compile(r"(?i)\b(?:use|apply|copy|inherit)\s+[a-z0-9-]+\s+(?:branding|brand system|design system|corporate palette)\b|\bcorporate\s+(?:color|colour|palette)\s*#?[0-9a-f]{6}\b"),
    "PROMPT-LOGO-001": re.compile(r"(?i)\b(?:add|include|place|render)\s+(?:the\s+)?(?:brand\s+)?logo\b"),
}

NEGATION_MARKERS = (
    "exclude",
    "avoid",
    "without",
    "do not",
    "don't",
    "must not",
    "not ",
    "non-",
    "non ",
    "forbid",
    "forbidden",
    "remove",
)


def _is_negated(text: str, match: re.Match[str]) -> bool:
    start = match.start()
    prefix = text[max(0, start - 96):start].lower()
    clause_start = max(prefix.rfind("\n"), prefix.rfind("."), prefix.rfind(";"), prefix.rfind(":"))
    clause = prefix[clause_start + 1:]
    if match.group(0).lower() == "photorealistic" and start >= 4:
        immediate = text[max(0, start - 5):start].lower()
        if immediate.endswith("non-") or immediate.endswith("non "):
            return True
    return any(marker in clause for marker in NEGATION_MARKERS)


def validate(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = read_text(path)
    except ValueError as exc:
        return [Finding("PROMPT-PARSE-001", path.as_posix(), str(exc), "provide a UTF-8 prompt file")]

    missing = has_all_groups(text, REQUIRED_GROUPS)
    for group in missing:
        findings.append(Finding("PROMPT-REQ-001", path.as_posix(), f"missing required semantic group `{group}`", f"add a clear {group.replace('_', ' ')} instruction"))

    for rule_id, pattern in FORBIDDEN_PATTERNS.items():
        for match in pattern.finditer(text):
            if _is_negated(text, match):
                continue
            findings.append(Finding(rule_id, path.as_posix(), f"forbidden marker detected: `{match.group(0)}`", "remove the marker or convert it into an explicit exclusion or formal Modern Flat constraint"))
            break

    left = bool(re.search(r"(?i)(?:light|key light)\s+(?:comes\s+)?from\s+the\s+left|from left", text))
    right = bool(re.search(r"(?i)(?:light|key light)\s+(?:comes\s+)?from\s+the\s+right|from right", text))
    if left and right:
        findings.append(Finding("PROMPT-LIGHT-001", path.as_posix(), "conflicting left and right key-light directions detected", "keep one dominant key-light direction"))

    return findings


def run() -> int:
    parser = argparse.ArgumentParser(description="Validate a compiled Modern Flat generation prompt.")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    findings: list[Finding] = []
    for path in args.paths:
        findings.extend(validate(path))
    return print_findings(findings)


if __name__ == "__main__":
    main_guard(run)
