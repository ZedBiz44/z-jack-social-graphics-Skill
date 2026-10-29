from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build_package
import check_save_receipt
import verify_reference_assets


def image_bytes(suffix: str, tag: bytes = b"x") -> bytes:
    if suffix in (".jpg", ".jpeg"):
        return b"\xff\xd8\xff" + tag
    if suffix == ".png":
        return b"\x89PNG\r\n\x1a\n" + tag
    if suffix == ".webp":
        return b"RIFF\x04\x00\x00\x00WEBP" + tag
    if suffix == ".gif":
        return b"GIF89a" + tag
    raise ValueError(suffix)


def write_image(path: Path, tag: bytes = b"x") -> bytes:
    payload = image_bytes(path.suffix.lower(), tag)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return payload


def manifest_for(root: Path) -> dict:
    files = []
    for relative, role in sorted(verify_reference_assets.EXPECTED_FILES.items()):
        payload = write_image(root / relative, relative.encode("utf-8")[:8])
        files.append(
            {
                "path": relative,
                "role": role,
                "size_bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    return {
        "schema_version": 1,
        "skill": "z-jack-social-graphics",
        "files": files,
    }


def write_manifest(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


class ReferenceVerifierTests(unittest.TestCase):
    def test_oversized_but_hash_valid_references_fail_before_provider_call(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "payload"
            manifest = manifest_for(root)
            relative = verify_reference_assets.OFFICE_INPUTS[0]
            payload = write_image(root / relative, b"x" * verify_reference_assets.MAX_OFFICE_REFERENCE_BYTES)
            entry = next(item for item in manifest["files"] if item["path"] == relative)
            entry.update(size_bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest())
            manifest_path = Path(directory) / "reference-manifest.json"
            write_manifest(manifest_path, manifest)
            result = verify_reference_assets.verify_assets(root, manifest_path)
            self.assertFalse(result["ok"])
            self.assertTrue(any("byte budget" in error for error in result["errors"]))

    def test_valid_synthetic_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "payload"
            manifest = manifest_for(root)
            manifest_path = Path(directory) / "reference-manifest.json"
            write_manifest(manifest_path, manifest)
            result = verify_reference_assets.verify_assets(root, manifest_path)
            self.assertTrue(result["ok"], result["errors"])
            self.assertEqual(len(verify_reference_assets.EXPECTED_FILES), len(result["verified_files"]))
            self.assertIn("not visually opened", result["caveat"])

    def test_missing_nonoffice_comparison_cannot_pass_current_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "payload"
            manifest = manifest_for(root)
            manifest["files"] = [entry for entry in manifest["files"] if entry["role"] != "approved-scene"]
            manifest_path = Path(directory) / "reference-manifest.json"
            write_manifest(manifest_path, manifest)
            result = verify_reference_assets.verify_assets(root, manifest_path)
            self.assertFalse(result["ok"])
            self.assertTrue(any("missing expected paths" in error for error in result["errors"]))

    def test_selected_office_base_is_unique(self) -> None:
        office_paths = [path for path in verify_reference_assets.EXPECTED_FILES if path.startswith("assets/environments/office/")]
        self.assertEqual(["assets/environments/office/office-main.jpg"], office_paths)
        self.assertFalse(any("jack-office-" in path for path in verify_reference_assets.EXPECTED_FILES))

    def test_retired_office_image_in_active_payload_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "payload"
            manifest = manifest_for(root)
            write_image(root / "assets/environments/office/office-main-desk.webp", b"retired")
            manifest_path = Path(directory) / "reference-manifest.json"
            write_manifest(manifest_path, manifest)
            result = verify_reference_assets.verify_assets(root, manifest_path)
            self.assertFalse(result["ok"])
            self.assertTrue(any("unlisted image in active payload" in error for error in result["errors"]))

    def test_missing_and_tampered_payload_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "payload"
            manifest = manifest_for(root)
            manifest_path = Path(directory) / "reference-manifest.json"
            write_manifest(manifest_path, manifest)
            target = root / "assets/identity/jack-portrait-pointing.jpg"
            target.unlink()
            missing = verify_reference_assets.verify_assets(root, manifest_path)
            self.assertFalse(missing["ok"])
            self.assertTrue(any("missing payload file" in error for error in missing["errors"]))

            write_image(target, b"tampered")
            tampered = verify_reference_assets.verify_assets(root, manifest_path)
            self.assertFalse(tampered["ok"])
            self.assertTrue(any("mismatch" in error for error in tampered["errors"]))

    def test_unsafe_manifest_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "payload"
            manifest = manifest_for(root)
            manifest["files"][0]["path"] = "../escape.png"
            manifest_path = Path(directory) / "reference-manifest.json"
            write_manifest(manifest_path, manifest)
            result = verify_reference_assets.verify_assets(root, manifest_path)
            self.assertFalse(result["ok"])
            self.assertTrue(any("unsafe" in error for error in result["errors"]))


class ReceiptCheckerTests(unittest.TestCase):
    def _valid_receipt(self, image: Path, now: datetime) -> dict:
        payload = write_image(image, b"receipt")
        return {
            "expected": {
                "name": "graphic.png",
                "parent_id": "parent-123",
                "drive_id": "drive-123",
                "boundary_id": "boundary-123",
                "owner": "jack",
                "knowledge_key": "zedbiz-graphics",
            },
            "file": {
                "id": "file-123",
                "name": "graphic.png",
                "parents": ["parent-123"],
                "driveId": "drive-123",
                "mimeType": "image/png",
                "size": str(len(payload)),
                "md5Checksum": hashlib.md5(payload).hexdigest(),  # nosec B324 - Drive field test fixture.
                "webViewLink": "https://drive.google.com/file/d/file-123/view",
                "trashed": False,
            },
            "ancestors": [
                {
                    "id": "parent-123",
                    "name": "Approved Output",
                    "parents": ["boundary-123"],
                    "driveId": "drive-123",
                    "mimeType": "application/vnd.google-apps.folder",
                },
                {
                    "id": "boundary-123",
                    "name": "Scoped Boundary",
                    "parents": ["outside-boundary"],
                    "driveId": "drive-123",
                    "mimeType": "application/vnd.google-apps.folder",
                },
            ],
            "verification": {
                "account_verified": True,
                "policy_checked": True,
                "metadata_read_back": True,
                "content_opened": True,
            },
            "content_evidence": "Observed successful tool result: opened the uploaded image.",
            "metadata_read_at": now.isoformat().replace("+00:00", "Z"),
        }

    def _validate(self, receipt: dict, image: Path, now: datetime) -> dict:
        receipt_path = image.with_suffix(".receipt.json")
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        return check_save_receipt.validate_receipt(receipt_path, image, now=now)

    def test_valid_receipt_with_minimal_header(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            now = datetime(2026, 10, 28, 20, 0, tzinfo=timezone.utc)
            image = Path(directory) / "graphic.png"
            result = self._validate(self._valid_receipt(image, now), image, now)
            self.assertTrue(result["ok"], result["errors"])
            self.assertIn("cannot prove", result["caveat"])

    def test_wrong_name_parent_and_drive_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            now = datetime(2026, 10, 28, 20, 0, tzinfo=timezone.utc)
            image = Path(directory) / "graphic.png"
            receipt = self._valid_receipt(image, now)
            receipt["file"].update({"name": "copy of bad_name.png", "parents": ["other-parent"], "driveId": "other-drive"})
            result = self._validate(receipt, image, now)
            self.assertFalse(result["ok"])
            text = "\n".join(result["errors"])
            self.assertIn("unsafe", text)
            self.assertIn("direct parent", text)
            self.assertIn("driveId", text)

    def test_missing_boundary_and_bad_ancestry_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            now = datetime(2026, 10, 28, 20, 0, tzinfo=timezone.utc)
            image = Path(directory) / "graphic.png"
            receipt = self._valid_receipt(image, now)
            receipt["ancestors"] = []
            result = self._validate(receipt, image, now)
            self.assertFalse(result["ok"])
            self.assertTrue(any("non-empty" in error for error in result["errors"]))

            receipt = self._valid_receipt(image, now)
            receipt["ancestors"][0]["parents"] = ["wrong-edge"]
            receipt["ancestors"][1]["name"] = "Shared Drive"
            result = self._validate(receipt, image, now)
            self.assertFalse(result["ok"])
            text = "\n".join(result["errors"])
            self.assertIn("next ancestor", text)
            self.assertIn("whole Shared Drive", text)

    def test_local_hash_mismatch_stale_timestamp_and_false_content_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            now = datetime(2026, 10, 28, 20, 0, tzinfo=timezone.utc)
            image = Path(directory) / "graphic.png"
            receipt = self._valid_receipt(image, now)
            image.write_bytes(image_bytes(".png", b"changed"))
            receipt["metadata_read_at"] = (now - timedelta(hours=25)).isoformat()
            receipt["verification"]["content_opened"] = False
            receipt["content_evidence"] = "not inspected"
            result = self._validate(receipt, image, now)
            self.assertFalse(result["ok"])
            text = "\n".join(result["errors"])
            self.assertIn("md5Checksum", text)
            self.assertIn("older than 24 hours", text)
            self.assertIn("content_opened", text)
            self.assertIn("content_evidence", text)


class PackageBuilderTests(unittest.TestCase):
    def _repository(self, directory: Path, include_private: bool = False) -> tuple[Path, Path | None, dict]:
        root = directory / "skill"
        root.mkdir()
        (root / "SKILL.md").write_text(
            "---\nname: z-jack-social-graphics\ndescription: Test only.\n---\n\n# Test skill\n",
            encoding="utf-8",
        )
        (root / "package-resources.txt").write_text("agents/\nreferences/\nassets/\nscripts/\n", encoding="utf-8")
        (root / "agents").mkdir()
        (root / "agents" / "openai.yaml").write_text("name: test\n", encoding="utf-8")
        (root / "references").mkdir()
        (root / "references" / "guide.md").write_text("Runtime guidance\n", encoding="utf-8")
        (root / "references" / "docs").mkdir()
        (root / "references" / "docs" / "authoring.md").write_text("must stay out\n", encoding="utf-8")
        (root / "assets").mkdir()
        (root / "assets" / "pilot-request.md").write_text("runtime asset\n", encoding="utf-8")
        (root / "scripts").mkdir()
        (root / "scripts" / "runtime.py").write_text("print('runtime')\n", encoding="utf-8")
        (root / "scripts" / "README.md").write_text("authoring note\n", encoding="utf-8")
        (root / "scripts" / "test_runtime.py").write_text("raise AssertionError\n", encoding="utf-8")
        private = directory / "private" if include_private else None
        target = private if private is not None else root
        manifest = manifest_for(target)
        write_manifest(root / "assets/reference-manifest.json", manifest)
        return root, private, manifest

    def test_resource_allowlist_rejects_unapproved_resource(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "package-resources.txt"
            file.write_text("agents/\nreferences/\nassets/\nscripts/\ndocs/\n", encoding="utf-8")
            with self.assertRaises(build_package.PackageError):
                build_package.parse_resource_allowlist(file)

    def test_code_only_package_has_source_record_and_no_authoring_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, _, manifest = self._repository(Path(directory))
            output = Path(directory) / "output"
            result = build_package.build_package(root=root, output_dir=output, source_commit="test-commit")
            self.assertTrue(result["ok"])
            self.assertFalse(result["generation_ready"])
            runtime = Path(result["runtime"])
            self.assertTrue((runtime / "scripts/package-status.json").is_file())
            status = json.loads((runtime / "scripts/package-status.json").read_text(encoding="utf-8"))
            self.assertEqual("reference images absent, NOT generation-ready", status["reference_image_status"])
            self.assertFalse((runtime / "assets/identity/jack-portrait-pointing.jpg").exists())
            self.assertFalse((runtime / "scripts/README.md").exists())
            self.assertFalse((runtime / "scripts/test_runtime.py").exists())
            self.assertFalse((runtime / "references/docs/authoring.md").exists())

            source_receipt = json.loads(Path(result["source_receipt"]).read_text(encoding="utf-8"))
            self.assertEqual("test-commit", source_receipt["source_commit"])
            self.assertFalse(source_receipt["generation_ready"])
            self.assertEqual(
                hashlib.sha256((root / "assets/reference-manifest.json").read_bytes()).hexdigest(),
                source_receipt["reference_manifest_sha256"],
            )
            self.assertTrue(source_receipt["runtime_files"])
            self.assertEqual(
                hashlib.sha256(Path(result["zip"]).read_bytes()).hexdigest(),
                source_receipt["zip_sha256"],
            )
            with zipfile.ZipFile(result["zip"]) as archive:
                archived = archive.namelist()
            self.assertFalse(any("README" in name or "authoring" in name or "test_runtime" in name for name in archived))
            self.assertEqual(set(manifest["files"][0]), {"path", "role", "size_bytes", "sha256"})

    def test_verified_private_payload_makes_generation_ready_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, private, _ = self._repository(Path(directory), include_private=True)
            self.assertIsNotNone(private)
            result = build_package.build_package(
                root=root,
                output_dir=Path(directory) / "output",
                private_assets=private,
                source_commit="test-commit",
            )
            self.assertTrue(result["generation_ready"])
            runtime = Path(result["runtime"])
            for relative in verify_reference_assets.EXPECTED_FILES:
                self.assertTrue((runtime / relative).is_file(), relative)

    def test_unlisted_source_image_cannot_leak_into_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, private, _ = self._repository(Path(directory), include_private=True)
            write_image(root / "assets/environments/office/retired.png", b"retired")
            with self.assertRaises(build_package.PackageError):
                build_package.build_package(root=root, output_dir=Path(directory) / "output", private_assets=private, source_commit="test-commit")


if __name__ == "__main__":
    unittest.main()
