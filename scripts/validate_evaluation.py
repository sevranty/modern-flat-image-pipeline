from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from validation_common import Finding, KEBAB_RE, load_yaml, main_guard, print_findings

QUALITY_BANDS = {"accept", "local_correction", "required_iteration", "reject"}
RUNTIME_ACTIONS = {"accept", "targeted_correction", "regenerate", "fail"}


def _load_mapping(path: Path, rule_id: str) -> tuple[dict[str, Any] | None, list[Finding]]:
    try:
        data = load_yaml(path)
    except ValueError as exc:
        return None, [Finding(rule_id, path.as_posix(), str(exc), "restore valid UTF-8 YAML")]
    if not isinstance(data, dict):
        return None, [Finding(rule_id, path.as_posix(), "top level must be a mapping", "use a YAML mapping")]
    return data, []


def validate(root: Path) -> list[Finding]:
    root = root.resolve()
    findings: list[Finding] = []
    fixture_path = root / "tests" / "fixtures" / "reference-descriptors.yaml"
    case_path = root / "tests" / "cases" / "e2e-cases.yaml"
    expected_path = root / "tests" / "expected" / "decisions.yaml"
    accepted_path = root / "skills" / "modern-flat-image-pipeline" / "assets" / "anchors" / "accepted" / "catalog.yaml"
    rejected_path = root / "skills" / "modern-flat-image-pipeline" / "assets" / "anchors" / "rejected" / "catalog.yaml"

    fixtures_doc, errors = _load_mapping(fixture_path, "EVAL-FIXTURE-001")
    findings.extend(errors)
    cases_doc, errors = _load_mapping(case_path, "EVAL-CASE-001")
    findings.extend(errors)
    expected_doc, errors = _load_mapping(expected_path, "EVAL-EXPECTED-001")
    findings.extend(errors)
    accepted_doc, errors = _load_mapping(accepted_path, "EVAL-ANCHOR-001")
    findings.extend(errors)
    rejected_doc, errors = _load_mapping(rejected_path, "EVAL-ANCHOR-001")
    findings.extend(errors)
    if findings:
        return findings

    fixtures = fixtures_doc.get("fixtures") if fixtures_doc else None
    cases = cases_doc.get("cases") if cases_doc else None
    expected = expected_doc.get("expected_decisions") if expected_doc else None
    accepted = accepted_doc.get("anchors") if accepted_doc else None
    rejected = rejected_doc.get("anchors") if rejected_doc else None

    if not isinstance(fixtures, list):
        findings.append(Finding("EVAL-FIXTURE-002", fixture_path.relative_to(root).as_posix(), "`fixtures` must be a list", "define a list of fixture mappings"))
        fixtures = []
    if not isinstance(cases, list):
        findings.append(Finding("EVAL-CASE-002", case_path.relative_to(root).as_posix(), "`cases` must be a list", "define a list of case mappings"))
        cases = []
    if not isinstance(expected, dict):
        findings.append(Finding("EVAL-EXPECTED-002", expected_path.relative_to(root).as_posix(), "`expected_decisions` must be a mapping", "map every case ID to one expected decision"))
        expected = {}
    if not isinstance(accepted, list):
        findings.append(Finding("EVAL-ANCHOR-002", accepted_path.relative_to(root).as_posix(), "accepted `anchors` must be a list", "define accepted anchor mappings"))
        accepted = []
    if not isinstance(rejected, list):
        findings.append(Finding("EVAL-ANCHOR-002", rejected_path.relative_to(root).as_posix(), "rejected `anchors` must be a list", "define rejected anchor mappings"))
        rejected = []

    fixture_ids: set[str] = set()
    for index, fixture in enumerate(fixtures):
        path = f"{fixture_path.relative_to(root).as_posix()}#fixtures[{index}]"
        fixture_id = fixture.get("fixture_id") if isinstance(fixture, dict) else None
        if not isinstance(fixture_id, str) or not KEBAB_RE.fullmatch(fixture_id):
            findings.append(Finding("EVAL-ID-001", path, "fixture ID must be stable ASCII kebab-case", "set a unique kebab-case `fixture_id`"))
            continue
        if fixture_id in fixture_ids:
            findings.append(Finding("EVAL-ID-002", path, f"duplicate fixture ID `{fixture_id}`", "use one unique fixture ID"))
        fixture_ids.add(fixture_id)

    case_ids: set[str] = set()
    for index, case in enumerate(cases):
        path = f"{case_path.relative_to(root).as_posix()}#cases[{index}]"
        if not isinstance(case, dict):
            findings.append(Finding("EVAL-CASE-003", path, "case must be a mapping", "replace it with a case mapping"))
            continue
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not KEBAB_RE.fullmatch(case_id):
            findings.append(Finding("EVAL-ID-003", path, "case ID must be stable ASCII kebab-case", "set a unique kebab-case `case_id`"))
            continue
        if case_id in case_ids:
            findings.append(Finding("EVAL-ID-004", path, f"duplicate case ID `{case_id}`", "use one unique case ID"))
        case_ids.add(case_id)

        referenced = case.get("fixture_ids")
        if not isinstance(referenced, list) or not referenced:
            findings.append(Finding("EVAL-REF-001", path, "case must reference at least one fixture", "add a non-empty `fixture_ids` list"))
        else:
            for fixture_id in referenced:
                if fixture_id not in fixture_ids:
                    findings.append(Finding("EVAL-REF-002", path, f"unknown fixture ID `{fixture_id}`", "reference an existing fixture ID"))

        roles = case.get("expected_reference_roles")
        locks = case.get("expected_locks")
        if not isinstance(roles, dict) or not roles:
            findings.append(Finding("EVAL-CASE-004", path, "missing expected reference roles", "define `expected_reference_roles`"))
        if not isinstance(locks, dict):
            findings.append(Finding("EVAL-LOCK-001", path, "missing expected locks", "define `expected_locks`"))
        else:
            if locks.get("style_id") != "modern-flat":
                findings.append(Finding("EVAL-LOCK-002", path, "Style Lock must use `modern-flat`", "set `expected_locks.style_id` to `modern-flat`"))
            if locks.get("style_override_allowed") is not False:
                findings.append(Finding("EVAL-LOCK-003", path, "Style Lock must be non-overridable", "set `style_override_allowed` to false"))
            level = locks.get("composition_level")
            if not isinstance(level, int) or not 0 <= level <= 4:
                findings.append(Finding("EVAL-LOCK-004", path, "Composition Lock level must be an integer from 0 through 4", "set a valid `composition_level`"))

        for field in ("required_prompt_markers", "forbidden_prompt_markers"):
            if not isinstance(case.get(field), list) or not case[field]:
                findings.append(Finding("EVAL-PROMPT-001", path, f"`{field}` must be a non-empty list", f"add semantic markers to `{field}`"))

        quality_band = case.get("expected_quality_band")
        action = case.get("expected_runtime_action")
        if quality_band not in QUALITY_BANDS:
            findings.append(Finding("EVAL-DECISION-001", path, f"invalid quality band `{quality_band}`", f"use one of {sorted(QUALITY_BANDS)}"))
        if action not in RUNTIME_ACTIONS:
            findings.append(Finding("EVAL-DECISION-002", path, f"invalid runtime action `{action}`", f"use one of {sorted(RUNTIME_ACTIONS)}"))
        if quality_band == "reject" or action in {"regenerate", "fail"}:
            if not case.get("expected_primary_diagnostic_category"):
                findings.append(Finding("EVAL-REJECT-001", path, "rejected case lacks a primary diagnostic category", "set `expected_primary_diagnostic_category`"))
            criteria = case.get("expected_critical_rejection_criteria")
            if not isinstance(criteria, list) or not criteria:
                findings.append(Finding("EVAL-REJECT-002", path, "rejected case lacks critical rejection criteria", "add `expected_critical_rejection_criteria`"))

    for case_id in sorted(case_ids):
        if case_id not in expected:
            findings.append(Finding("EVAL-EXPECTED-003", expected_path.relative_to(root).as_posix(), f"missing expected decision for `{case_id}`", "add a matching `expected_decisions` entry"))
    for case_id in sorted(expected):
        if case_id not in case_ids:
            findings.append(Finding("EVAL-EXPECTED-004", expected_path.relative_to(root).as_posix(), f"orphan expected decision `{case_id}`", "remove it or add the matching case"))

    anchor_ids: set[str] = set()
    for status, anchors, source_path in (("accepted", accepted, accepted_path), ("rejected", rejected, rejected_path)):
        for index, anchor in enumerate(anchors):
            path = f"{source_path.relative_to(root).as_posix()}#anchors[{index}]"
            if not isinstance(anchor, dict):
                findings.append(Finding("EVAL-ANCHOR-003", path, "anchor must be a mapping", "replace it with an anchor mapping"))
                continue
            anchor_id = anchor.get("anchor_id")
            case_id = anchor.get("case_id")
            if not isinstance(anchor_id, str) or not KEBAB_RE.fullmatch(anchor_id):
                findings.append(Finding("EVAL-ID-005", path, "anchor ID must be stable ASCII kebab-case", "set a unique kebab-case `anchor_id`"))
            elif anchor_id in anchor_ids:
                findings.append(Finding("EVAL-ID-006", path, f"duplicate anchor ID `{anchor_id}`", "use one unique anchor ID"))
            else:
                anchor_ids.add(anchor_id)
            if case_id not in case_ids:
                findings.append(Finding("EVAL-REF-003", path, f"anchor references unknown case `{case_id}`", "reference an existing case ID"))
            if status == "accepted" and not anchor.get("acceptance_reasons"):
                findings.append(Finding("EVAL-ANCHOR-004", path, "accepted anchor lacks acceptance reasons", "add `acceptance_reasons`"))
            if status == "rejected":
                if not anchor.get("rejection_reasons"):
                    findings.append(Finding("EVAL-ANCHOR-005", path, "rejected anchor lacks rejection reasons", "add `rejection_reasons`"))
                if not anchor.get("primary_diagnostic_category"):
                    findings.append(Finding("EVAL-ANCHOR-006", path, "rejected anchor lacks a primary diagnostic category", "add `primary_diagnostic_category`"))

    if len(cases) < 12:
        findings.append(Finding("EVAL-COVERAGE-001", case_path.relative_to(root).as_posix(), f"only {len(cases)} cases found; at least 12 are required", "add the missing regression families"))
    if len(accepted) + len(rejected) < 12:
        findings.append(Finding("EVAL-COVERAGE-002", "skills/modern-flat-image-pipeline/assets/anchors", f"only {len(accepted) + len(rejected)} anchor specifications found; at least 12 are required", "add accepted and rejected anchor specifications"))
    if "fail-user-visible-delivery" not in case_ids:
        findings.append(Finding("EVAL-COVERAGE-003", case_path.relative_to(root).as_posix(), "missing user-visible delivery regression", "add case `fail-user-visible-delivery`"))

    return findings


def run() -> int:
    parser = argparse.ArgumentParser(description="Validate the Modern Flat evaluation suite and golden anchor contracts.")
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    args = parser.parse_args()
    return print_findings(validate(args.root))


if __name__ == "__main__":
    main_guard(run)
