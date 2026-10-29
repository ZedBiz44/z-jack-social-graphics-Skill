#!/usr/bin/env python3
"""Build a clean, local skill package without network, upload, or generation work."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from verify_reference_assets import EXPECTED_FILES, sha256_file, verify_assets

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_RUNTIME_DIRECTORIES = ("agents", "references", "assets", "scripts")
MAX_ZIP_BYTES = 25 * 1024 * 1024
SENSITIVE_NAME_TOKENS = ("credential", "secret", "token", "password", "private_key", "apikey", "api_key")


class PackageError(ValueError):
    """A requested package is unsafe, incomplete, or would overwrite a destination."""


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _safe_sha256(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise PackageError(f"cannot hash non-regular file: {path}")
    return sha256_file(path)


def parse_skill_name(skill_file: Path) -> str:
    try:
        content = skill_file.read_text(encoding="utf-8")
    except OSError as exc:
        raise PackageError(f"cannot read SKILL.md: {exc}") from exc
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", content, flags=re.DOTALL)
    if not match:
        raise PackageError("SKILL.md must start with shared YAML frontmatter")
    name: str | None = None
    for line in match.group(1).splitlines():
        field = re.fullmatch(r"\s*name\s*:\s*([^#\n]+?)\s*", line)
        if field:
            candidate = field.group(1).strip().strip('"\'')
            name = candidate
            break
    if not name or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        raise PackageError("shared frontmatter must contain a safe lowercase kebab-case name")
    return name


def parse_resource_allowlist(resource_file: Path) -> tuple[str, ...]:
    try:
        lines = resource_file.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise PackageError(f"cannot read package-resources.txt: {exc}") from exc
    resources: list[str] = []
    for line in lines:
        value = line.strip()
        if not value or value.startswith("#"):
            continue
        if not re.fullmatch(r"[a-z][a-z0-9-]*/", value):
            raise PackageError(f"unsafe resource declaration: {value!r}")
        resources.append(value[:-1])
    if len(resources) != len(set(resources)):
        raise PackageError("package-resources.txt contains duplicate declarations")
    if set(resources) != set(ALLOWED_RUNTIME_DIRECTORIES):
        raise PackageError(
            "package-resources.txt must declare only agents/, references/, assets/, and scripts/"
        )
    return tuple(resources)


def default_source_commit(root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return "uncommitted"
    value = completed.stdout.strip()
    return value or "uncommitted"


def _is_authoring_or_test_path(relative: PurePosixPath, resource: str) -> bool:
    lowered_parts = [part.casefold() for part in relative.parts]
    filename = relative.name.casefold()
    if any(part in {".git", ".github", "docs", "tests", "test"} for part in lowered_parts):
        return True
    if filename.startswith("readme") or filename.startswith("test_") or filename.endswith("_test.py"):
        return True
    # Markdown is allowed within the established references and assets runtime folders.
    if resource == "scripts" and filename.endswith((".md", ".rst", ".txt")):
        return True
    return False


def _is_sensitive_filename(relative: PurePosixPath) -> bool:
    filename = relative.name.casefold()
    return (
        filename in {".env", ".netrc", "id_rsa", "id_ed25519"}
        or filename.endswith((".pem", ".key", ".p12", ".pfx"))
        or any(token in filename for token in SENSITIVE_NAME_TOKENS)
    )


def _copy_public_tree(source: Path, destination: Path, resource: str, private_images: set[str]) -> None:
    """Copy one approved directory, refusing symlinks and skipping authoring artifacts."""
    if source.is_symlink() or not source.is_dir():
        raise PackageError(f"declared runtime directory is missing or not real: {source}")
    for current_text, dirnames, filenames in os.walk(source, topdown=True, followlinks=False):
        current = Path(current_text)
        retained_dirs: list[str] = []
        for dirname in dirnames:
            child = current / dirname
            relative = child.relative_to(source)
            if child.is_symlink():
                raise PackageError(f"symlinked directory is not permitted: {child}")
            if dirname == "__pycache__" or _is_authoring_or_test_path(PurePosixPath(relative.as_posix()), resource):
                continue
            retained_dirs.append(dirname)
        dirnames[:] = retained_dirs

        for filename in filenames:
            source_file = current / filename
            relative = source_file.relative_to(source)
            relative_posix = PurePosixPath(relative.as_posix())
            full_relative = f"{resource}/{relative_posix.as_posix()}"
            if source_file.is_symlink():
                raise PackageError(f"symlinked file is not permitted: {source_file}")
            if filename.endswith(".pyc") or _is_authoring_or_test_path(relative_posix, resource):
                continue
            if full_relative in private_images:
                # Reference payload must be copied only from an independently verified
                # private payload, never from source assets accidentally left in-tree.
                continue
            if _is_sensitive_filename(relative_posix):
                raise PackageError(f"sensitive-looking file is not permitted in runtime package: {source_file}")
            mode = source_file.stat(follow_symlinks=False).st_mode
            if not stat.S_ISREG(mode):
                raise PackageError(f"runtime item is not a regular file: {source_file}")
            destination_file = destination / relative
            destination_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_file, destination_file)


def _copy_verified_private_images(private_root: Path, runtime_root: Path, manifest_path: Path) -> None:
    result = verify_assets(private_root, manifest_path)
    if not result["ok"]:
        raise PackageError("private reference payload failed verification: " + "; ".join(result["errors"]))
    for relative_text in sorted(EXPECTED_FILES):
        source = private_root.joinpath(*PurePosixPath(relative_text).parts)
        target = runtime_root.joinpath(*PurePosixPath(relative_text).parts)
        if source.is_symlink() or not source.is_file():
            raise PackageError(f"verified payload unexpectedly lacks regular file: {relative_text}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def _runtime_file_records(runtime_root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(runtime_root.rglob("*")):
        if path.is_dir():
            continue
        if path.is_symlink() or not path.is_file():
            raise PackageError(f"runtime contains a non-regular file: {path}")
        records.append(
            {
                "path": path.relative_to(runtime_root).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": _safe_sha256(path),
            }
        )
    return records


def _write_zip(runtime_root: Path, skill_name: str, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(runtime_root.rglob("*")):
            if path.is_dir():
                continue
            if path.is_symlink() or not path.is_file():
                raise PackageError(f"cannot archive non-regular runtime item: {path}")
            archive.write(path, arcname=(Path(skill_name) / path.relative_to(runtime_root)).as_posix())
    if zip_path.stat().st_size > MAX_ZIP_BYTES:
        raise PackageError(f"compressed ZIP exceeds 25 MiB limit ({zip_path.stat().st_size} bytes)")


def _check_output_location(root: Path, output_dir: Path) -> None:
    resolved_root = root.resolve(strict=True)
    resolved_output = output_dir.resolve(strict=False)
    protected = [resolved_root / ".git"] + [resolved_root / name for name in ALLOWED_RUNTIME_DIRECTORIES]
    if any(resolved_output == entry or _is_relative_to(resolved_output, entry) for entry in protected):
        raise PackageError("output directory may not be inside .git or a runtime source directory")
    if _is_relative_to(resolved_root, resolved_output):
        raise PackageError("output directory may not be an ancestor of the source repository")


def _remove_destination(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink():
        raise PackageError(f"refusing to replace symlink destination: {path}")
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def build_package(
    *,
    root: str | Path = ROOT,
    output_dir: str | Path | None = None,
    private_assets: str | Path | None = None,
    source_commit: str | None = None,
    replace: bool = False,
) -> dict[str, Any]:
    """Build a package and its adjacent source receipt; no external service is used."""
    requested_root = Path(root)
    if requested_root.is_symlink():
        raise PackageError("source root may not be a symlink")
    source_root = requested_root.resolve(strict=True)
    if not source_root.is_dir():
        raise PackageError("source root must be a real directory")
    skill_name = parse_skill_name(source_root / "SKILL.md")
    resources = parse_resource_allowlist(source_root / "package-resources.txt")
    manifest_path = source_root / "assets/reference-manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise PackageError("assets/reference-manifest.json is required for a source receipt")
    manifest_hash = _safe_sha256(manifest_path)

    if output_dir is None:
        output = source_root / "dist"
    else:
        output = Path(output_dir)
        if not output.is_absolute():
            output = (Path.cwd() / output).resolve(strict=False)
    if output.is_symlink():
        raise PackageError("output directory may not be a symlink")
    _check_output_location(source_root, output)
    output.mkdir(parents=True, exist_ok=True)

    runtime_destination = output / skill_name
    zip_destination = output / f"{skill_name}.zip"
    receipt_destination = output / f"{skill_name}.source-receipt.json"
    destinations = (runtime_destination, zip_destination, receipt_destination)
    existing = [path for path in destinations if path.exists() or path.is_symlink()]
    if existing and not replace:
        raise PackageError("destination already exists; pass --replace to replace: " + ", ".join(map(str, existing)))
    if source_commit is None:
        source_commit = default_source_commit(source_root)
    if not isinstance(source_commit, str) or not source_commit.strip():
        raise PackageError("source commit must be a non-empty value")

    private_root: Path | None = None
    if private_assets is not None:
        requested_private_root = Path(private_assets)
        if requested_private_root.is_symlink():
            raise PackageError("--private-assets may not be a symlink")
        private_root = requested_private_root.resolve(strict=True)
        if not private_root.is_dir():
            raise PackageError("--private-assets must be a real directory")

    temporary_parent = output.parent
    with tempfile.TemporaryDirectory(prefix=f".{skill_name}-build-", dir=temporary_parent) as work:
        work_root = Path(work)
        staged_runtime = work_root / skill_name
        staged_runtime.mkdir()
        private_image_paths = set(EXPECTED_FILES)
        # SKILL.md is the only permitted root-level runtime file.
        shutil.copyfile(source_root / "SKILL.md", staged_runtime / "SKILL.md")
        for resource in resources:
            _copy_public_tree(
                source_root / resource,
                staged_runtime / resource,
                resource,
                private_image_paths,
            )

        generation_ready = private_root is not None
        if private_root is not None:
            _copy_verified_private_images(private_root, staged_runtime, manifest_path)
            status = "verified private reference payload present; generation-ready"
        else:
            status = "reference images absent, NOT generation-ready"

        actual_images = {
            path.relative_to(staged_runtime).as_posix()
            for path in (staged_runtime / "assets").rglob("*")
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}
        }
        unlisted_images = sorted(actual_images - set(EXPECTED_FILES))
        if unlisted_images:
            raise PackageError("unlisted image in runtime package: " + ", ".join(unlisted_images))
        if generation_ready:
            final_assets = verify_assets(staged_runtime, staged_runtime / "assets/reference-manifest.json")
            if not final_assets["ok"]:
                raise PackageError("built runtime references failed verification: " + "; ".join(final_assets["errors"]))

        (staged_runtime / "scripts" / "package-status.json").write_text(
            json.dumps(
                {"generation_ready": generation_ready, "reference_image_status": status},
                sort_keys=True,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        records = _runtime_file_records(staged_runtime)
        staged_zip = work_root / f"{skill_name}.zip"
        _write_zip(staged_runtime, skill_name, staged_zip)
        zip_hash = _safe_sha256(staged_zip)
        receipt = {
            "schema_version": 1,
            "skill": skill_name,
            "source_commit": source_commit,
            "reference_manifest_sha256": manifest_hash,
            "generation_ready": generation_ready,
            "reference_image_status": status,
            "runtime_files": records,
            "zip_file": zip_destination.name,
            "zip_sha256": zip_hash,
            "zip_size_bytes": staged_zip.stat().st_size,
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        staged_receipt = work_root / receipt_destination.name
        staged_receipt.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8")

        if replace:
            for destination in destinations:
                _remove_destination(destination)
        # Recheck just before publishing so a concurrent writer cannot be overwritten
        # without the explicit --replace intent that was already supplied.
        if not replace:
            conflict = [path for path in destinations if path.exists() or path.is_symlink()]
            if conflict:
                raise PackageError("destination appeared during build; refusing overwrite: " + ", ".join(map(str, conflict)))
        shutil.move(str(staged_runtime), str(runtime_destination))
        shutil.move(str(staged_zip), str(zip_destination))
        shutil.move(str(staged_receipt), str(receipt_destination))

    return {
        "ok": True,
        "runtime": str(runtime_destination),
        "zip": str(zip_destination),
        "source_receipt": str(receipt_destination),
        "generation_ready": generation_ready,
        "reference_image_status": status,
        "zip_sha256": zip_hash,
        "zip_size_bytes": zip_destination.stat().st_size,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-assets", type=Path, help="Private payload root containing assets/identity and assets/environments/office")
    parser.add_argument("--output-dir", type=Path, default=None, help="Output directory (default: repository dist/)")
    parser.add_argument("--source-commit", help="Source commit recorded in the receipt (default: git HEAD or uncommitted)")
    parser.add_argument("--replace", action="store_true", help="Explicitly replace this skill's existing package artifacts")
    arguments = parser.parse_args(argv)
    try:
        result = build_package(
            output_dir=arguments.output_dir,
            private_assets=arguments.private_assets,
            source_commit=arguments.source_commit,
            replace=arguments.replace,
        )
    except (PackageError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True, indent=2))
        return 1
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
