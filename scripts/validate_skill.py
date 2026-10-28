"""Validate the structure and YAML metadata of an Agent Skill."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
README_SUBJECTS = {
    "purpose": ("this repository", "skill"),
    "appropriate-use guidance": ("when to use",),
    "inappropriate-use guidance": ("do not use",),
    "SKILL.md authority": ("skill.md", "authoritative"),
    "validation or deployment guidance": ("validate",),
    "safety or approval boundary": ("secret", "approval"),
}
OPENCLAW_KEYS = {
    "name",
    "description",
    "metadata",
    "homepage",
    "license",
    "allowed-tools",
    "user-invocable",
    "disable-model-invocation",
    "command-dispatch",
    "command-tool",
    "command-arg-mode",
}
NODE_YAML_CHECK = r"""
const fs = require("fs");
let YAML;
try {
  const resolved = require.resolve("yaml", {paths: [process.cwd(), "/app"]});
  YAML = require(resolved);
} catch (error) {
  process.stderr.write("YAML_READER_UNAVAILABLE");
  process.exit(3);
}
const source = fs.readFileSync(0, "utf8");
const document = YAML.parseDocument(source, {uniqueKeys: true});
if (document.errors.length) {
  process.stderr.write(document.errors.map(error => error.message).join("\n"));
  process.exit(2);
}
process.stdout.write(JSON.stringify(document.toJS({mapAsMap: false})));
"""


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def parse_yaml(source: str, label: str, errors: list[str]) -> object | None:
    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        yaml = None

    if yaml is not None:
        try:
            return yaml.safe_load(source)
        except yaml.YAMLError as error:
            fail(f"{label} contains invalid YAML: {error}", errors)
            return None

    node = shutil.which("node")
    if node:
        result = subprocess.run(
            [node, "-e", NODE_YAML_CHECK],
            input=source,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError as error:
                fail(f"{label} YAML reader returned invalid output: {error}", errors)
                return None
        if result.returncode != 3:
            fail(f"{label} contains invalid YAML: {result.stderr.strip()}", errors)
            return None

    unavailable = (
        "A real YAML reader is required. Install PyYAML or use a target runtime "
        "that supplies the Node 'yaml' package."
    )
    if unavailable not in errors:
        fail(unavailable, errors)
    return None


def parse_frontmatter(
    text: str, errors: list[str]
) -> tuple[dict[str, object] | None, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail("SKILL.md must start with YAML frontmatter.", errors)
        return None, text
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail("SKILL.md frontmatter is not closed.", errors)
        return None, text

    source = "\n".join(lines[1:end])
    parsed = parse_yaml(source, "SKILL.md frontmatter", errors)
    if parsed is None:
        return None, "\n".join(lines[end + 1 :])
    if not isinstance(parsed, dict):
        fail("SKILL.md frontmatter must be a YAML mapping of keys and values.", errors)
        return None, "\n".join(lines[end + 1 :])
    return parsed, "\n".join(lines[end + 1 :])


def validate_readme(readme_file: Path, errors: list[str]) -> None:
    if not readme_file.is_file():
        fail("README.md is required at the repository root.", errors)
        return

    readme = readme_file.read_text(encoding="utf-8").strip()
    readme_lower = readme.lower()
    if not readme.startswith("# "):
        fail("README.md must begin with one H1 heading.", errors)
    if len(readme) < 200:
        fail("README.md is too short to document the skill responsibly.", errors)
    if readme.count("\n## ") < 3:
        fail("README.md must contain at least three H2 sections.", errors)
    for subject, keywords in README_SUBJECTS.items():
        if not all(keyword in readme_lower for keyword in keywords):
            fail(f"README.md is missing required {subject}.", errors)


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("--repository", action="store_true")
    argument_parser.add_argument(
        "--platform", choices=("shared", "openclaw"), default="shared"
    )
    argument_parser.add_argument("skill_directory", nargs="?", default=".")
    args = argument_parser.parse_args()

    repository_mode = args.repository
    root = Path(args.skill_directory).resolve()
    skill_file = root / "SKILL.md"
    errors: list[str] = []

    if not skill_file.is_file():
        print(f"ERROR: {skill_file} does not exist.")
        return 1

    text = skill_file.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text, errors)

    name: object = ""
    description: object = ""
    if frontmatter is not None:
        required_keys = {"name", "description"}
        found_keys = set(frontmatter)
        if args.platform == "shared" and found_keys != required_keys:
            fail(
                "Shared frontmatter must contain exactly name and description; "
                f"found: {', '.join(sorted(found_keys)) or 'none'}.",
                errors,
            )
        if args.platform == "openclaw":
            missing = required_keys - found_keys
            unsupported = found_keys - OPENCLAW_KEYS
            if missing:
                fail(
                    f"OpenClaw frontmatter is missing: {', '.join(sorted(missing))}.",
                    errors,
                )
            if unsupported:
                fail(
                    "OpenClaw frontmatter contains unsupported fields: "
                    f"{', '.join(sorted(unsupported))}.",
                    errors,
                )

        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")

        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            fail("name must use lowercase letters, numbers, and single hyphens.", errors)
        if isinstance(name, str) and len(name) > 64:
            fail("name must not exceed 64 characters.", errors)
        if not repository_mode and root.name != name:
            fail(f"folder name '{root.name}' must match name '{name}'.", errors)
        if not isinstance(description, str) or not description:
            fail("description must be a non-empty text value.", errors)
        if isinstance(description, str) and len(description) > 160:
            fail(
                "description must not exceed 160 characters for shared "
                "OpenClaw compatibility.",
                errors,
            )
    if "TODO" in text:
        fail("SKILL.md contains a TODO placeholder.", errors)
    if len(text.splitlines()) > 500:
        fail("SKILL.md must stay under 500 lines.", errors)

    if repository_mode:
        validate_readme(root / "README.md", errors)

    for target in LINK_RE.findall(body):
        if "://" in target or target.startswith("#"):
            continue
        path = (root / target.split("#", 1)[0]).resolve()
        if not path.exists():
            fail(f"Referenced file does not exist: {target}", errors)

    openai_yaml = root / "agents" / "openai.yaml"
    if openai_yaml.is_file():
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        openai_data = parse_yaml(yaml_text, "agents/openai.yaml", errors)
        if openai_data is not None and not isinstance(openai_data, dict):
            fail("agents/openai.yaml must contain a YAML mapping.", errors)
        if isinstance(name, str) and name and f"${name}" not in yaml_text:
            fail(f"agents/openai.yaml default_prompt must mention ${name}.", errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
