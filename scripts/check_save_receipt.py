#!/usr/bin/env python3
"""Offline consistency checks for a submitted Google Drive save receipt.

This checker never calls Drive.  It only checks whether a supplied receipt is
internally consistent with a local image.  Live Drive tools must still provide the
actual account, policy, upload, metadata read-back, and opened-content facts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

SUPPORTED_IMAGES = {
    ".png": ("image/png", b"\x89PNG\r\n\x1a\n"),
    ".jpg": ("image/jpeg", b"\xff\xd8\xff"),
    ".jpeg": ("image/jpeg", b"\xff\xd8\xff"),
    ".webp": ("image/webp", b"RIFF"),
    ".gif": ("image/gif", b"GIF"),
}
FOLDER_MIME = "application/vnd.google-apps.folder"
REQUIRED_EXPECTED = {"name", "parent_id", "drive_id", "boundary_id", "owner", "knowledge_key"}
REQUIRED_FILE = {"id", "name", "parents", "driveId", "mimeType", "size", "md5Checksum", "webViewLink", "trashed"}
REQUIRED_ANCESTOR = {"id", "name", "parents", "driveId", "mimeType"}
REQUIRED_VERIFICATION = {"account_verified", "policy_checked", "metadata_read_back", "content_opened"}


class ReceiptError(ValueError):
    """A receipt is malformed, unsafe, stale, or internally inconsistent."""


def _sha256_unused() -> None:
    """Keep the module's intent explicit: receipt matching uses Drive MD5, not SHA256."""


def md5_file(path: Path) -> str:
    digest = hashlib.md5()  # nosec B324 -- Drive metadata uses MD5 as a comparison value.
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def image_mime_from_magic(path: Path) -> str | None:
    with path.open("rb") as handle:
        header = handle.read(16)
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if header.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "image/webp"
    if header.startswith(b"GIF87a") or header.startswith(b"GIF89a"):
        return "image/gif"
    return None


def is_safe_leaf_name(value: object) -> bool:
    """Accept a plain generated filename, never a path or duplicate-style name."""
    if not isinstance(value, str) or not value or value != value.strip() or "\x00" in value:
        return False
    lowered = value.casefold()
    return not (
        any(char.isspace() for char in value)
        or "_" in value
        or "/" in value
        or "\\" in value
        or ".." in value
        or "copy of" in lowered
    )


def _require_nonempty_string(mapping: dict[str, Any], key: str, label: str, errors: list[str]) -> str | None:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}.{key} must be a non-empty string")
        return None
    return value


def _require_mapping(document: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = document.get(key)
    if not isinstance(value, dict):
        errors.append(f"receipt.{key} must be an object")
        return {}
    return value


def _parse_timestamp(value: object, now: datetime, errors: list[str]) -> None:
    if not isinstance(value, str) or not value:
        errors.append("receipt.metadata_read_at must be an ISO-8601 timestamp")
        return
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append("receipt.metadata_read_at is not ISO-8601")
        return
    if parsed.tzinfo is None:
        errors.append("receipt.metadata_read_at must include a timezone")
        return
    parsed = parsed.astimezone(timezone.utc)
    now = now.astimezone(timezone.utc)
    if parsed > now + timedelta(minutes=5):
        errors.append("receipt.metadata_read_at is more than five minutes in the future")
    if parsed < now - timedelta(hours=24):
        errors.append("receipt.metadata_read_at is older than 24 hours")


def _validate_local_image(image_path: Path, file_data: dict[str, Any], errors: list[str]) -> None:
    try:
        if image_path.is_symlink() or not image_path.is_file():
            raise ReceiptError("--image must be a regular, non-symlink local file")
        mode = image_path.stat(follow_symlinks=False).st_mode
        if not stat.S_ISREG(mode):
            raise ReceiptError("--image must be a regular local file")
        declared = SUPPORTED_IMAGES.get(image_path.suffix.lower())
        if declared is None:
            raise ReceiptError("--image has an unsupported extension; allowed PNG/JPEG/WEBP/GIF")
        magic_mime = image_mime_from_magic(image_path)
        if magic_mime is None:
            raise ReceiptError("--image magic bytes are not a supported image type")
        extension_mime, _ = declared
        if magic_mime != extension_mime:
            raise ReceiptError("--image extension does not match image magic bytes")
        if file_data.get("mimeType") != extension_mime:
            raise ReceiptError("receipt.file.mimeType does not match local image extension")
        drive_name = file_data.get("name")
        if not isinstance(drive_name, str) or SUPPORTED_IMAGES.get(Path(drive_name).suffix.lower(), (None,))[0] != extension_mime:
            raise ReceiptError("receipt.file.name extension does not match local image MIME type")
        actual_size = image_path.stat(follow_symlinks=False).st_size
        size_value = file_data.get("size")
        if isinstance(size_value, bool) or not isinstance(size_value, (int, str)):
            raise ReceiptError("receipt.file.size must be a decimal byte count")
        if isinstance(size_value, str) and not re.fullmatch(r"[0-9]+", size_value):
            raise ReceiptError("receipt.file.size must be a decimal byte count")
        if int(size_value) != actual_size:
            raise ReceiptError("receipt.file.size does not match local image")
        expected_md5 = file_data.get("md5Checksum")
        if not isinstance(expected_md5, str) or not re.fullmatch(r"[0-9a-fA-F]{32}", expected_md5):
            raise ReceiptError("receipt.file.md5Checksum must be a 32-character hexadecimal MD5")
        if md5_file(image_path).lower() != expected_md5.lower():
            raise ReceiptError("receipt.file.md5Checksum does not match local image")
    except (OSError, ReceiptError) as exc:
        errors.append(str(exc))


def _validate_ancestors(
    expected: dict[str, Any], file_data: dict[str, Any], ancestors: object, errors: list[str]
) -> None:
    if not isinstance(ancestors, list) or not ancestors:
        errors.append("receipt.ancestors must be a non-empty ordered list")
        return
    normalized: list[dict[str, Any]] = []
    for index, ancestor in enumerate(ancestors):
        if not isinstance(ancestor, dict):
            errors.append(f"receipt.ancestors[{index}] must be an object")
            continue
        missing = REQUIRED_ANCESTOR - set(ancestor)
        if missing:
            errors.append(f"receipt.ancestors[{index}] is missing: {', '.join(sorted(missing))}")
        for key in ("id", "name", "driveId", "mimeType"):
            _require_nonempty_string(ancestor, key, f"receipt.ancestors[{index}]", errors)
        parents = ancestor.get("parents")
        if not isinstance(parents, list) or not all(isinstance(item, str) and item for item in parents):
            errors.append(f"receipt.ancestors[{index}].parents must be a list of non-empty IDs")
        # Folder names may legitimately contain spaces; reject only path-like or traversal values.
        name = ancestor.get("name")
        if isinstance(name, str) and ("/" in name or "\\" in name or name in (".", "..") or "\x00" in name):
            errors.append(f"receipt.ancestors[{index}].name is path-like or unsafe")
        if ancestor.get("mimeType") != FOLDER_MIME:
            errors.append(f"receipt.ancestors[{index}] must be a scoped Drive folder")
        if ancestor.get("driveId") != expected.get("drive_id"):
            errors.append(f"receipt.ancestors[{index}].driveId does not match expected drive_id")
        normalized.append(ancestor)

    if len(normalized) != len(ancestors):
        return
    ancestor_ids = [item.get("id") for item in normalized]
    if len(set(ancestor_ids)) != len(ancestor_ids):
        errors.append("receipt.ancestors contains duplicate IDs")
    file_id = file_data.get("id")
    if isinstance(file_id, str) and file_id in ancestor_ids:
        errors.append("receipt.file.id duplicates an ancestor ID")
    if normalized[0].get("id") != expected.get("parent_id"):
        errors.append("first ancestor must be the expected direct parent")
    if normalized[-1].get("id") != expected.get("boundary_id"):
        errors.append("last ancestor must be the approved scoped boundary")
    if expected.get("boundary_id") == expected.get("drive_id"):
        errors.append("approved boundary must not be the whole Shared Drive")
    boundary = normalized[-1]
    boundary_name = str(boundary.get("name", "")).casefold()
    if (
        boundary_name in {"shared drive", "shared drives", "my drive"}
        or "shared drive" in boundary_name
        or boundary.get("mimeType") == "application/vnd.google-apps.drive"
    ):
        errors.append("approved boundary must be a scoped folder, not a whole Shared Drive")
    for index, ancestor in enumerate(normalized[:-1]):
        next_id = normalized[index + 1].get("id")
        if ancestor.get("parents") != [next_id]:
            errors.append(f"receipt.ancestors[{index}] does not point to the next ancestor")


def validate_receipt(
    receipt_path: str | Path, image_path: str | Path, *, now: datetime | None = None
) -> dict[str, Any]:
    """Check a receipt offline and return JSON-serializable results.

    ``now`` is injectable solely for deterministic unit tests.
    """
    receipt_file = Path(receipt_path)
    image = Path(image_path)
    errors: list[str] = []
    if now is None:
        now = datetime.now(timezone.utc)
    try:
        if receipt_file.is_symlink() or not receipt_file.is_file():
            raise ReceiptError("receipt JSON must be a regular, non-symlink file")
        document = json.loads(receipt_file.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise ReceiptError("receipt JSON must be an object")
    except (OSError, json.JSONDecodeError, ReceiptError) as exc:
        return {
            "ok": False,
            "receipt": str(receipt_file),
            "image": str(image),
            "errors": [f"cannot read receipt: {exc}"],
            "caveat": "Offline checker only checks a submitted receipt; live Drive tools must provide the actual facts.",
        }

    expected = _require_mapping(document, "expected", errors)
    file_data = _require_mapping(document, "file", errors)
    verification = _require_mapping(document, "verification", errors)

    missing_expected = REQUIRED_EXPECTED - set(expected)
    if missing_expected:
        errors.append("receipt.expected is missing: " + ", ".join(sorted(missing_expected)))
    missing_file = REQUIRED_FILE - set(file_data)
    if missing_file:
        errors.append("receipt.file is missing: " + ", ".join(sorted(missing_file)))
    missing_verification = REQUIRED_VERIFICATION - set(verification)
    if missing_verification:
        errors.append("receipt.verification is missing: " + ", ".join(sorted(missing_verification)))

    for key in REQUIRED_EXPECTED:
        _require_nonempty_string(expected, key, "receipt.expected", errors)
    expected_name = expected.get("name")
    file_name = file_data.get("name")
    if not is_safe_leaf_name(expected_name):
        errors.append("receipt.expected.name is unsafe (spaces, underscores, paths, and 'copy of' are not allowed)")
    if not is_safe_leaf_name(file_name):
        errors.append("receipt.file.name is unsafe (spaces, underscores, paths, and 'copy of' are not allowed)")
    if expected_name != file_name:
        errors.append("receipt.file.name does not match receipt.expected.name")
    if not isinstance(file_data.get("id"), str) or not file_data.get("id"):
        errors.append("receipt.file.id must be a non-empty string")
    parents = file_data.get("parents")
    if parents != [expected.get("parent_id")]:
        errors.append("receipt.file.parents must contain only the expected direct parent")
    if file_data.get("driveId") != expected.get("drive_id"):
        errors.append("receipt.file.driveId does not match receipt.expected.drive_id")
    if file_data.get("trashed") is not False:
        errors.append("receipt.file.trashed must be false")
    web_link = file_data.get("webViewLink")
    if not isinstance(web_link, str) or not web_link.startswith("https://"):
        errors.append("receipt.file.webViewLink must be a non-empty HTTPS URL")

    _validate_local_image(image, file_data, errors)
    _validate_ancestors(expected, file_data, document.get("ancestors"), errors)

    for key in REQUIRED_VERIFICATION:
        if verification.get(key) is not True:
            errors.append(f"receipt.verification.{key} must be true")
    evidence = document.get("content_evidence")
    if not isinstance(evidence, str) or not evidence.strip():
        errors.append("receipt.content_evidence must be a non-empty observed successful tool-result reference")
    else:
        lowered = evidence.casefold()
        if "observed" not in lowered or not any(token in lowered for token in ("success", "opened", "tool result")):
            errors.append("receipt.content_evidence must reference an observed successful tool result")
    _parse_timestamp(document.get("metadata_read_at"), now, errors)

    return {
        "ok": not errors,
        "receipt": str(receipt_file),
        "image": str(image),
        "errors": errors,
        "caveat": "Offline checker only checks a submitted receipt; it cannot prove a live upload, Drive metadata read-back, account boundary, or true visual review. Live tools must provide those facts.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt_json", type=Path, help="Locally supplied normalized receipt JSON")
    parser.add_argument("--image", type=Path, required=True, help="Local PNG/JPEG/WEBP/GIF to match")
    arguments = parser.parse_args(argv)
    try:
        result = validate_receipt(arguments.receipt_json, arguments.image)
    except Exception as exc:  # Defensive boundary: malformed local state is not a successful validation.
        print(
            json.dumps(
                {
                    "ok": False,
                    "errors": [f"checker operational error: {exc}"],
                    "caveat": "Offline checker only checks a submitted receipt; live Drive tools must provide the actual facts.",
                },
                sort_keys=True,
                indent=2,
            )
        )
        return 2
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
