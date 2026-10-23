"""Offline MFP adapter for Presento v1 materialized assets.

This adapter never generates images or invokes a paid provider. The caller must
supply an already materialized, MFP-owned image after the normal MFP review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

REQUEST_KEYS = frozenset({
    "schema_version", "request_id", "provider_id", "asset_kind",
    "prompt_profile", "requirements", "config",
})
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
MIME_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".svg": "image/svg+xml"}


class ProviderError(ValueError):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


def _fail(code: str, message: str) -> None:
    raise ProviderError(code, message)


def validate_request(request: Any) -> None:
    if not isinstance(request, dict) or set(request) != REQUEST_KEYS:
        _fail("invalid_request", "request fields do not match Presento v1")
    if request["schema_version"] != "1.0.0" or request["provider_id"] != "mfp":
        _fail("invalid_request", "unsupported contract version or provider")
    if not isinstance(request["request_id"], str) or not SAFE_ID.fullmatch(request["request_id"]):
        _fail("invalid_request", "request_id must be an ASCII filename-safe identifier")
    if request["asset_kind"] not in ("raster-image", "vector-image"):
        _fail("unsupported_asset_kind", "MFP supports raster-image or vector-image")
    if request["prompt_profile"] is not None and not isinstance(request["prompt_profile"], str):
        _fail("invalid_request", "prompt_profile must be a string or null")
    if not isinstance(request["requirements"], dict) or not isinstance(request["config"], dict):
        _fail("invalid_request", "requirements and config must be objects")
    try:
        json.dumps(request["config"], ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        _fail("invalid_config", str(exc))


def _detect_mime(path: Path, data: bytes) -> str:
    mime = MIME_TYPES.get(path.suffix.lower())
    if mime is None:
        _fail("unsupported_asset", "only PNG, JPEG, WEBP and SVG are supported")
    if mime == "image/png" and not data.startswith(b"\x89PNG\r\n\x1a\n"):
        _fail("invalid_asset", "PNG signature mismatch")
    if mime == "image/jpeg" and not data.startswith(b"\xff\xd8\xff"):
        _fail("invalid_asset", "JPEG signature mismatch")
    if mime == "image/webp" and not (len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"):
        _fail("invalid_asset", "WEBP signature mismatch")
    if mime == "image/svg+xml" and b"<svg" not in data[:4096].lower():
        _fail("invalid_asset", "SVG root not found")
    return mime


def adapt_materialized_asset(request: dict[str, Any], *, asset: Path, asset_root: Path, provider_revision: str) -> dict[str, Any]:
    """Build a Presento-compatible result from an existing, reviewed MFP asset."""
    validate_request(request)
    if not isinstance(provider_revision, str) or not SHA40.fullmatch(provider_revision):
        _fail("missing_provider_revision", "provider_revision must be an exact 40-character lowercase commit SHA")
    try:
        root = asset_root.resolve(strict=True)
        source = asset.resolve(strict=True)
    except OSError as exc:
        _fail("missing_asset_provenance", str(exc))
    try:
        source.relative_to(root)
    except ValueError:
        _fail("invalid_asset_path", "asset must be inside the declared MFP output root")
    if not source.is_file():
        _fail("missing_asset_provenance", "asset is not a regular file")
    data = source.read_bytes()
    if not data:
        _fail("missing_asset_provenance", "asset is empty")
    mime = _detect_mime(source, data)
    if request["asset_kind"] == "vector-image" and mime != "image/svg+xml":
        _fail("asset_kind_mismatch", "vector-image requires SVG")
    if request["asset_kind"] == "raster-image" and mime == "image/svg+xml":
        _fail("asset_kind_mismatch", "raster-image requires raster bytes")
    canonical = json.dumps(request["config"], ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return {
        "schema_version": "1.0.0",
        "request_id": request["request_id"],
        "provider_id": "mfp",
        "provider_project_id": "MODERN_FLAT_IMAGE_PIPELINE",
        "provider_revision": provider_revision,
        "config_sha256": hashlib.sha256(canonical).hexdigest(),
        "asset_kind": request["asset_kind"],
        "materialization": "local-file",
        "mime_type": mime,
        "path": source.as_posix(),
        "checksum": hashlib.sha256(data).hexdigest(),
        "dimensions": None,
        "diagnostics": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Wrap a reviewed MFP image in the Presento v1 result contract")
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--asset", type=Path, required=True)
    parser.add_argument("--asset-root", type=Path, required=True)
    parser.add_argument("--provider-revision", required=True)
    args = parser.parse_args()
    try:
        request = json.loads(args.request.read_text(encoding="utf-8"))
        result = adapt_materialized_asset(request, asset=args.asset, asset_root=args.asset_root, provider_revision=args.provider_revision)
    except (ProviderError, OSError, json.JSONDecodeError) as exc:
        code = exc.code if isinstance(exc, ProviderError) else "provider_failure"
        print(json.dumps({"error": {"code": code, "message": str(exc)}}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
