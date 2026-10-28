#!/usr/bin/env python3
"""Verify the fixed private reference-image payload without opening images visually.

This module performs only filesystem, checksum, and file-signature checks.  It does
not inspect pixels or make any network/API call.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any

EXPECTED_FILES: dict[str, str] = {
    "assets/identity/jack-portrait-arms-crossed.jpg": "identity",
    "assets/identity/jack-portrait-pointing.jpg": "identity",
    "assets/identity/jack-standing-pointing-front.png": "identity",
    "assets/identity/jack-standing-pointing-relaxed.jpg": "identity",
    "assets/environments/office/office-main-desk.webp": "environment",
    "assets/environments/office/office-wide-loft.png": "environment",
    "assets/environments/office/office-hallway-reverse.png": "environment",
    "assets/environments/office/office-desk-closeup.png": "environment",
}
EXPECTED_SKILL = "z-jack-social-graphics"
EXPECTED_SCHEMA_VERSION = 1


class VerificationError(ValueError):
    """A supplied manifest or payload did not meet the fixed contract."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def is_safe_relative_path(value: object) -> bool:
    """Accept a portable, non-empty relative POSIX path below the payload root."""
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        return False
    candidate = PurePosixPath(value)
    return (
        not candidate.is_absolute()
        and candidate.as_posix() == value
        and all(part not in ("", ".", "..") for part in candidate.parts)
    )


def _contained_path(root: Path, relative_path: str) -> Path:
    if not is_safe_relative_path(relative_path):
        raise VerificationError(f"unsafe manifest path: {relative_path!r}")
    root_resolved = root.resolve(strict=True)
    candidate = root.joinpath(*PurePosixPath(relative_path).parts)
    try:
        candidate_resolved = candidate.resolve(strict=True)
    except FileNotFoundError as exc:
        raise VerificationError(f"missing payload file: {relative_path}") from exc
    try:
        candidate_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise VerificationError(f"payload path escapes skill directory: {relative_path}") from exc

    # A regular final file is required; reject symlinked traversal even if it happens
    # to point back into the skill root, so source identity is unambiguous.
    current = root
    for part in PurePosixPath(relative_path).parts:
        current = current / part
        if current.is_symlink():
            raise VerificationError(f"symlink not permitted in payload path: {relative_path}")
    return candidate


def magic_matches_extension(path: Path) -> bool:
    """Check a lightweight file signature; this is not a visual or pixel review."""
    with path.open("rb") as handle:
        header = handle.read(16)
    suffix = path.suffix.lower()
    if suffix in (".jpg", ".jpeg"):
        return header.startswith(b"\xff\xd8\xff")
    if suffix == ".png":
        return header.startswith(b"\x89PNG\r\n\x1a\n")
    if suffix == ".webp":
        return len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP"
    return False


def _load_manifest(manifest_path: Path) -> dict[str, Any]:
    try:
        raw = manifest_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise VerificationError(f"cannot read manifest: {manifest_path}: {exc}") from exc
    try:
        document = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise VerificationError(f"manifest is not valid JSON: {exc.msg}") from exc
    if not isinstance(document, dict):
        raise VerificationError("manifest must be a JSON object")
    return document


def verify_assets(skill_dir: str | Path, manifest_path: str | Path | None = None) -> dict[str, Any]:
    """Return a structured pass/fail result for one fixed reference payload.

    The function is intentionally reusable by ``build_package.py``.  Validation
    failures are data failures (not exceptions) so callers can present all known
    issues without treating the input as trusted.
    """
    root = Path(skill_dir)
    manifest = Path(manifest_path) if manifest_path is not None else root / "assets/reference-manifest.json"
    errors: list[str] = []
    verified_files: list[dict[str, Any]] = []

    try:
        if root.is_symlink() or not root.is_dir():
            raise VerificationError(f"skill directory must be a real directory: {root}")
        if manifest.is_symlink() or not manifest.is_file():
            raise VerificationError(f"manifest must be a regular file: {manifest}")
        document = _load_manifest(manifest)

        if document.get("schema_version") != EXPECTED_SCHEMA_VERSION:
            errors.append(f"unsupported schema_version; expected {EXPECTED_SCHEMA_VERSION}")
        if document.get("skill") != EXPECTED_SKILL:
            errors.append(f"manifest skill must be {EXPECTED_SKILL!r}")
        files = document.get("files")
        if not isinstance(files, list):
            errors.append("manifest files must be a list")
            files = []

        entries: dict[str, dict[str, Any]] = {}
        for index, entry in enumerate(files):
            if not isinstance(entry, dict):
                errors.append(f"files[{index}] must be an object")
                continue
            path_value = entry.get("path")
            if not is_safe_relative_path(path_value):
                errors.append(f"files[{index}] has an unsafe path")
                continue
            if path_value in entries:
                errors.append(f"duplicate manifest path: {path_value}")
                continue
            entries[path_value] = entry

        found_paths = set(entries)
        expected_paths = set(EXPECTED_FILES)
        missing = sorted(expected_paths - found_paths)
        extra = sorted(found_paths - expected_paths)
        if missing:
            errors.append("manifest is missing expected paths: " + ", ".join(missing))
        if extra:
            errors.append("manifest contains unexpected paths: " + ", ".join(extra))
        if len(files) != len(EXPECTED_FILES):
            errors.append(f"manifest must contain exactly {len(EXPECTED_FILES)} files")

        for relative_path, expected_role in EXPECTED_FILES.items():
            entry = entries.get(relative_path)
            if entry is None:
                continue
            if entry.get("role") != expected_role:
                errors.append(f"wrong role for {relative_path}; expected {expected_role}")
            expected_size = entry.get("size_bytes")
            expected_hash = entry.get("sha256")
            if not isinstance(expected_size, int) or isinstance(expected_size, bool) or expected_size < 1:
                errors.append(f"invalid size_bytes for {relative_path}")
                continue
            if not isinstance(expected_hash, str) or len(expected_hash) != 64 or any(
                char not in "0123456789abcdef" for char in expected_hash.lower()
            ):
                errors.append(f"invalid sha256 for {relative_path}")
                continue
            try:
                file_path = _contained_path(root, relative_path)
                mode = file_path.stat(follow_symlinks=False).st_mode
                if not stat.S_ISREG(mode):
                    raise VerificationError(f"payload item is not a regular file: {relative_path}")
                actual_size = file_path.stat(follow_symlinks=False).st_size
                if actual_size != expected_size:
                    raise VerificationError(
                        f"size mismatch for {relative_path}; expected {expected_size}, got {actual_size}"
                    )
                actual_hash = sha256_file(file_path)
                if actual_hash.lower() != expected_hash.lower():
                    raise VerificationError(f"SHA256 mismatch for {relative_path}")
                if not magic_matches_extension(file_path):
                    raise VerificationError(f"image magic does not match extension for {relative_path}")
                verified_files.append(
                    {"path": relative_path, "size_bytes": actual_size, "sha256": actual_hash}
                )
            except VerificationError as exc:
                errors.append(str(exc))
            except OSError as exc:
                errors.append(f"cannot inspect {relative_path}: {exc}")

    except VerificationError as exc:
        errors.append(str(exc))

    return {
        "ok": not errors,
        "skill_dir": str(root),
        "manifest": str(manifest),
        "verified_files": verified_files if not errors else [],
        "errors": errors,
        "caveat": "Checksum and magic-byte verification only; images were not visually opened or reviewed.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Manifest path (default: SKILL_DIR/assets/reference-manifest.json)",
    )
    arguments = parser.parse_args(argv)
    try:
        result = verify_assets(arguments.skill_dir, arguments.manifest)
    except Exception as exc:  # Defensive boundary for unexpected local I/O failures.
        print(
            json.dumps(
                {
                    "ok": False,
                    "errors": [f"verifier operational error: {exc}"],
                    "caveat": "Checksum and magic-byte verification only; images were not visually opened or reviewed.",
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
