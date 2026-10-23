"""Offline positive/negative fixtures for the optional Presento v1 boundary."""
from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from presento_asset_provider import ProviderError, adapt_materialized_asset

REVISION = "f6af684d8b1c58e59d5edd6075392376ad86e635"
PNG = b"\x89PNG\r\n\x1a\n" + b"offline-test-asset"


def request() -> dict:
    return {
        "schema_version": "1.0.0", "request_id": "mfp-fixture-001",
        "provider_id": "mfp", "asset_kind": "raster-image",
        "prompt_profile": None, "requirements": {}, "config": {"b": 2, "a": 1},
    }


class PresentoProviderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.asset = self.root / "fixture.png"
        self.asset.write_bytes(PNG)

    def adapt(self, req: dict | None = None, **kwargs):
        return adapt_materialized_asset(req if req is not None else request(), asset=kwargs.get("asset", self.asset), asset_root=self.root, provider_revision=kwargs.get("revision", REVISION))

    def assert_error(self, code: str, req: dict | None = None, **kwargs) -> None:
        with self.assertRaises(ProviderError) as caught:
            self.adapt(req, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def test_positive_provenance_and_contract_fields(self):
        result = self.adapt()
        self.assertEqual(result["provider_revision"], REVISION)
        self.assertEqual(result["checksum"], hashlib.sha256(PNG).hexdigest())
        self.assertEqual(result["config_sha256"], hashlib.sha256(b'{"a":1,"b":2}').hexdigest())
        self.assertEqual(result["path"], self.asset.as_posix())
        self.assertEqual(result["materialization"], "local-file")
        self.assertEqual(result["provider_project_id"], "MODERN_FLAT_IMAGE_PIPELINE")
        self.assertEqual(len(result), 13)
        self.assertEqual(result["diagnostics"], [])

    def test_missing_revision(self):
        self.assert_error("missing_provider_revision", revision="")

    def test_invalid_config(self):
        req = request()
        req["config"] = {"invalid": float("nan")}
        self.assert_error("invalid_config", req)

    def test_missing_asset(self):
        self.assert_error("missing_asset_provenance", asset=self.root / "missing.png")

    def test_reject_path_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            other = Path(outside) / "asset.png"
            other.write_bytes(PNG)
            self.assert_error("invalid_asset_path", asset=other)

    def test_reject_fake_png(self):
        self.asset.write_bytes(b"not an image")
        self.assert_error("invalid_asset")

    def test_reject_provider_mismatch(self):
        req = request()
        req["provider_id"] = "ogp"
        self.assert_error("invalid_request", req)

    def test_reject_vector_raster_mismatch(self):
        req = request()
        req["asset_kind"] = "vector-image"
        self.assert_error("asset_kind_mismatch", req)

    def test_reject_unsafe_request_id(self):
        req = request()
        req["request_id"] = "../escape"
        self.assert_error("invalid_request", req)

    def test_machine_readable_error(self):
        req = request()
        req["asset_kind"] = "3d-render"
        self.assert_error("unsupported_asset_kind", req)


if __name__ == "__main__":
    unittest.main()
