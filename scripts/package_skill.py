#!/usr/bin/env python3
"""Build one ZIP that works as an Agent Skill or a skill-only plugin."""

from __future__ import annotations

import io
import json
import os
import re
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUTPUT = DIST / "prompt-master.zip"
PACKAGE_ROOT = "prompt-master"
SKILL_FILES = (
    Path("SKILL.md"),
    Path("LICENSE"),
    Path("references/platforms.md"),
    Path("references/templates.md"),
    Path("references/patterns.md"),
)
PORTABLE_FALLBACK = Path("install/portable-instructions.md")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


def read_skill_metadata() -> tuple[str, str, str]:
    skill_path = ROOT / "SKILL.md"
    source = skill_path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", source, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter.")

    frontmatter = match.group(1)
    fields = {
        key: value.strip().strip("\"'")
        for key, value in re.findall(r"^(name|description|version):\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    }
    version_match = re.search(r"^\s+version:\s*[\"']?([^\"'\s]+)", frontmatter, re.MULTILINE)
    if version_match:
        fields["version"] = version_match.group(1)

    name = fields.get("name", "")
    description = fields.get("description", "")
    version = fields.get("version", "")
    if name != "prompt-master":
        raise ValueError("SKILL.md name must be 'prompt-master'.")
    if not description or len(description) > 1024:
        raise ValueError("SKILL.md description must contain 1–1024 characters.")
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError("SKILL.md metadata.version must use semantic versioning (for example 2.0.0).")
    return name, description, version


def validate_sources() -> tuple[str, str, str]:
    metadata = read_skill_metadata()
    missing = [path.as_posix() for path in (*SKILL_FILES, PORTABLE_FALLBACK) if not (ROOT / path).is_file()]
    if missing:
        raise FileNotFoundError("Missing package files: " + ", ".join(missing))

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)]+)\)", skill_text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        local_target = target.split("#", 1)[0]
        if local_target and not (ROOT / local_target).is_file():
            raise ValueError(f"SKILL.md links to a missing file: {target}")
    return metadata


def plugin_manifest(name: str, description: str, version: str) -> bytes:
    manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": name,
        "version": version,
        "description": description,
        "author": {
            "name": "siimsek",
            "url": "https://github.com/siimsek",
        },
        "homepage": "https://github.com/siimsek/prompt-master",
        "repository": "https://github.com/siimsek/prompt-master",
        "license": "MIT",
        "keywords": ["prompt-engineering", "agent-skill", "ai"],
        "extensions": {
            "com.openai": {
                "interface": {
                    "displayName": "Prompt Master",
                    "shortDescription": "Write prompts for any AI",
                    "longDescription": (
                        "Turn rough requests into clear, tool-aware prompts for chat models, coding agents, "
                        "research tools, and creative AI."
                    ),
                    "developerName": "siimsek",
                    "category": "Productivity",
                    "capabilities": [],
                    "defaultPrompt": ["Create a clear prompt for [AI tool] to [goal]."],
                }
            }
        },
    }
    return (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def build_archive(name: str, description: str, version: str) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        # These files make the top-level folder directly usable as an Agent Skill.
        for source_path in SKILL_FILES:
            archive.write(ROOT / source_path, f"{PACKAGE_ROOT}/{source_path.as_posix()}")
        archive.write(ROOT / PORTABLE_FALLBACK, f"{PACKAGE_ROOT}/{PORTABLE_FALLBACK.as_posix()}")

        # The same folder is also a portable plugin root. The nested copy is the
        # plugin's canonical skills/<name>/SKILL.md layout.
        archive.writestr(f"{PACKAGE_ROOT}/plugin.json", plugin_manifest(name, description, version))
        for source_path in SKILL_FILES:
            if source_path.name == "LICENSE":
                continue
            if source_path == Path("SKILL.md"):
                plugin_path = Path("skills") / name / "SKILL.md"
            else:
                # Keep each reference at its original relative path so the
                # nested SKILL.md resolves links the same way as the root copy.
                plugin_path = Path("skills") / name / source_path
            archive.write(ROOT / source_path, f"{PACKAGE_ROOT}/{plugin_path.as_posix()}")

    return buffer.getvalue()


def validate_archive(data: bytes, name: str) -> None:
    expected = {
        f"{PACKAGE_ROOT}/SKILL.md",
        f"{PACKAGE_ROOT}/plugin.json",
        f"{PACKAGE_ROOT}/skills/{name}/SKILL.md",
        f"{PACKAGE_ROOT}/references/platforms.md",
        f"{PACKAGE_ROOT}/references/templates.md",
        f"{PACKAGE_ROOT}/references/patterns.md",
        f"{PACKAGE_ROOT}/skills/{name}/references/platforms.md",
        f"{PACKAGE_ROOT}/skills/{name}/references/templates.md",
        f"{PACKAGE_ROOT}/skills/{name}/references/patterns.md",
        f"{PACKAGE_ROOT}/install/portable-instructions.md",
    }
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        bad_file = archive.testzip()
        if bad_file:
            raise ValueError(f"Archive CRC check failed for {bad_file}.")
        files = set(archive.namelist())
        missing = sorted(expected - files)
        if missing:
            raise ValueError("Archive is missing required files: " + ", ".join(missing))
        skill_paths = sorted(path for path in files if path.endswith("/SKILL.md"))
        required_skills = [f"{PACKAGE_ROOT}/SKILL.md", f"{PACKAGE_ROOT}/skills/{name}/SKILL.md"]
        if skill_paths != required_skills:
            raise ValueError("Archive must contain exactly the portable skill and its plugin skill copy.")
        manifest = json.loads(archive.read(f"{PACKAGE_ROOT}/plugin.json"))
        if manifest.get("name") != name or manifest.get("version") != read_skill_metadata()[2]:
            raise ValueError("Plugin manifest identity does not match SKILL.md metadata.")
        if not manifest.get("extensions", {}).get("com.openai", {}).get("interface", {}).get("displayName"):
            raise ValueError("Plugin manifest is missing the OpenAI display name.")


def main() -> None:
    name, description, version = validate_sources()
    data = build_archive(name, description, version)
    validate_archive(data, name)

    DIST.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=DIST, prefix=".prompt-master-", suffix=".zip", delete=False) as temporary:
            temporary.write(data)
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, OUTPUT)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()

    # Remove the old separate plugin artifact so the distribution directory has
    # one current download instead of suggesting that two files are required.
    legacy_plugin_zip = DIST / "prompt-master-chatgpt-plugin.zip"
    if legacy_plugin_zip.exists():
        legacy_plugin_zip.unlink()

    print(f"Built and validated {OUTPUT.relative_to(ROOT)} ({len(data):,} bytes)")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError, zipfile.BadZipFile, json.JSONDecodeError) as error:
        raise SystemExit(f"package error: {error}") from error
