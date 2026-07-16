from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from typing import Any

from validation_common import Finding, KEBAB_RE, load_yaml, main_guard, print_findings

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VALID_STATES = {"published", "unavailable"}
VALID_DECISIONS = {"accepted", "rejected"}
VALID_FORMATS = {"png", "jpg", "jpeg", "webp", "svg"}


def _mapping(path: Path, rule_id: str) -> tuple[dict[str, Any] | None, list[Finding]]:
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
    anchor_root = root / "skills" / "modern-flat-image-pipeline" / "assets" / "anchors"
    accepted_path = anchor_root / "accepted" / "catalog.yaml"
    rejected_path = anchor_root / "rejected" / "catalog.yaml"
    evidence_path = anchor_root / "evidence.yaml"

    accepted_doc, errors = _mapping(accepted_path, "ANCHOR-CATALOG-001")
    findings.extend(errors)
    rejected_doc, errors = _mapping(rejected_path, "ANCHOR-CATALOG-001")
    findings.extend(errors)
    evidence_doc, errors = _mapping(evidence_path, "ANCHOR-EVIDENCE-001")
    findings.extend(errors)
    if findings:
        return findings

    expected: dict[str, tuple[str, str]] = {}
    for decision, document in (("accepted", accepted_doc), ("rejected", rejected_doc)):
        anchors = document.get("anchors") if document else None
        if not isinstance(anchors, list):
            findings.append(Finding("ANCHOR-CATALOG-002", anchor_root.relative_to(root).as_posix(), f"{decision} anchors must be a list", "restore the anchor catalog"))
            continue
        for index, anchor in enumerate(anchors):
            path = f"{decision}/catalog.yaml#anchors[{index}]"
            if not isinstance(anchor, dict):
                findings.append(Finding("ANCHOR-CATALOG-003", path, "anchor must be a mapping", "replace it with an anchor mapping"))
                continue
            anchor_id = anchor.get("anchor_id")
            case_id = anchor.get("case_id")
            if not isinstance(anchor_id, str) or not KEBAB_RE.fullmatch(anchor_id):
                findings.append(Finding("ANCHOR-ID-001", path, "anchor_id must be ASCII kebab-case", "set a stable anchor_id"))
                continue
            if anchor_id in expected:
                findings.append(Finding("ANCHOR-ID-002", path, f"duplicate anchor_id `{anchor_id}`", "keep one normative anchor"))
                continue
            if not isinstance(case_id, str) or not KEBAB_RE.fullmatch(case_id):
                findings.append(Finding("ANCHOR-REF-001", path, "case_id must be ASCII kebab-case", "reference the normative case_id"))
                continue
            expected[anchor_id] = (case_id, decision)

    records = evidence_doc.get("records") if evidence_doc else None
    if not isinstance(records, list):
        findings.append(Finding("ANCHOR-EVIDENCE-002", evidence_path.relative_to(root).as_posix(), "records must be a list", "define one evidence record per anchor"))
        return findings

    seen: set[str] = set()
    for index, record in enumerate(records):
        path = f"{evidence_path.relative_to(root).as_posix()}#records[{index}]"
        if not isinstance(record, dict):
            findings.append(Finding("ANCHOR-EVIDENCE-003", path, "record must be a mapping", "replace it with an evidence mapping"))
            continue
        anchor_id = record.get("anchor_id")
        if not isinstance(anchor_id, str) or not KEBAB_RE.fullmatch(anchor_id):
            findings.append(Finding("ANCHOR-ID-003", path, "anchor_id must be ASCII kebab-case", "set the normative anchor_id"))
            continue
        if anchor_id in seen:
            findings.append(Finding("ANCHOR-ID-004", path, f"duplicate evidence record `{anchor_id}`", "keep one evidence record per anchor"))
            continue
        seen.add(anchor_id)
        if anchor_id not in expected:
            findings.append(Finding("ANCHOR-REF-002", path, f"evidence references unknown anchor `{anchor_id}`", "reference an existing normative anchor"))
            continue

        expected_case, expected_decision = expected[anchor_id]
        if record.get("case_id") != expected_case:
            findings.append(Finding("ANCHOR-REF-003", path, f"case_id does not match `{expected_case}`", "copy the normative case_id"))
        decision = record.get("decision")
        if decision not in VALID_DECISIONS or decision != expected_decision:
            findings.append(Finding("ANCHOR-DECISION-001", path, f"decision must be `{expected_decision}`", "copy the normative anchor decision"))

        state = record.get("evidence_state")
        if state not in VALID_STATES:
            findings.append(Finding("ANCHOR-STATE-001", path, f"invalid evidence_state `{state}`", f"use one of {sorted(VALID_STATES)}"))
            continue

        if state == "unavailable":
            if not isinstance(record.get("unavailable_reason"), str) or not record["unavailable_reason"].strip():
                findings.append(Finding("ANCHOR-UNAVAILABLE-001", path, "unavailable evidence lacks a reason", "add unavailable_reason"))
            if not isinstance(record.get("unblock_condition"), str) or not record["unblock_condition"].strip():
                findings.append(Finding("ANCHOR-UNAVAILABLE-002", path, "unavailable evidence lacks an unblock condition", "add unblock_condition"))
            continue

        asset_path = record.get("asset_path")
        if not isinstance(asset_path, str) or not asset_path or asset_path.startswith("/") or ".." in Path(asset_path).parts:
            findings.append(Finding("ANCHOR-ASSET-001", path, "published evidence requires a safe repository-relative asset_path", "set a relative asset_path"))
            continue
        try:
            asset_path.encode("ascii")
        except UnicodeEncodeError:
            findings.append(Finding("ANCHOR-ASSET-002", path, "asset_path must be ASCII", "rename the asset path"))
        asset = root / asset_path
        if not asset.is_file():
            findings.append(Finding("ANCHOR-ASSET-003", path, f"asset does not exist: {asset_path}", "publish the evidence asset or mark unavailable"))
            continue

        digest = record.get("sha256")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            findings.append(Finding("ANCHOR-CHECKSUM-001", path, "published evidence requires a lowercase SHA-256", "record the 64-character sha256"))
        elif hashlib.sha256(asset.read_bytes()).hexdigest() != digest:
            findings.append(Finding("ANCHOR-CHECKSUM-002", path, "sha256 does not match the asset bytes", "recalculate the checksum"))

        image_format = record.get("format")
        if image_format not in VALID_FORMATS:
            findings.append(Finding("ANCHOR-ASSET-004", path, f"unsupported format `{image_format}`", f"use one of {sorted(VALID_FORMATS)}"))
        dimensions = record.get("dimensions")
        if not isinstance(dimensions, dict) or not all(isinstance(dimensions.get(key), int) and dimensions[key] > 0 for key in ("width", "height")):
            findings.append(Finding("ANCHOR-ASSET-005", path, "published evidence requires positive width and height", "record dimensions.width and dimensions.height"))

        provenance = record.get("provenance")
        if not isinstance(provenance, dict):
            findings.append(Finding("ANCHOR-PROVENANCE-001", path, "published evidence lacks provenance", "record source, tool_or_model, verified_at, and prompt_or_spec"))
        else:
            for key in ("source", "tool_or_model", "prompt_or_spec"):
                if not isinstance(provenance.get(key), str) or not provenance[key].strip():
                    findings.append(Finding("ANCHOR-PROVENANCE-002", path, f"missing provenance.{key}", f"record provenance.{key}"))
            if not isinstance(provenance.get("verified_at"), str) or not DATE_RE.fullmatch(provenance["verified_at"]):
                findings.append(Finding("ANCHOR-PROVENANCE-003", path, "provenance.verified_at must be YYYY-MM-DD", "record the verification date"))

        rights = record.get("rights")
        if not isinstance(rights, dict) or rights.get("redistribution_permitted") is not True or not isinstance(rights.get("basis"), str) or not rights["basis"].strip():
            findings.append(Finding("ANCHOR-RIGHTS-001", path, "published evidence lacks confirmed redistribution rights", "set redistribution_permitted true and record the basis"))

        qa = record.get("qa")
        if not isinstance(qa, dict) or qa.get("decision") != expected_decision or not isinstance(qa.get("findings"), list):
            findings.append(Finding("ANCHOR-QA-001", path, "published evidence lacks completed QA aligned to the anchor decision", "record qa.decision and qa.findings"))

    for anchor_id in sorted(expected):
        if anchor_id not in seen:
            findings.append(Finding("ANCHOR-COVERAGE-001", evidence_path.relative_to(root).as_posix(), f"missing evidence record for `{anchor_id}`", "add published or unavailable evidence"))

    return findings


def run() -> int:
    parser = argparse.ArgumentParser(description="Validate provenance-controlled golden-anchor evidence.")
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    args = parser.parse_args()
    return print_findings(validate(args.root))


if __name__ == "__main__":
    main_guard(run)
