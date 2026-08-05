#!/usr/bin/env python3
"""Dependency-free structural checks for Dashboard Maker SKILL.md files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return ["SKILL.md is missing."]
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ["SKILL.md must begin with YAML frontmatter."]
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return ["SKILL.md frontmatter is not closed."]
    frontmatter, body = parts[1], parts[2]
    values = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    name = values.get("name", "")
    description = values.get("description", "")
    if not NAME_PATTERN.fullmatch(name):
        errors.append("Frontmatter name must be lowercase hyphen-case.")
    if name != skill_dir.name:
        errors.append(f"Frontmatter name '{name}' does not match directory '{skill_dir.name}'.")
    if not description or description.startswith("[TODO"):
        errors.append("Frontmatter description is missing or incomplete.")
    if not body.strip() or "TODO" in body:
        errors.append("Skill body is missing or still contains TODO placeholders.")
    if not (skill_dir / "agents" / "openai.yaml").is_file():
        errors.append("agents/openai.yaml is missing.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="skills", help="Skill directory or skills root.")
    args = parser.parse_args()
    root = Path(args.path)
    skill_dirs = [root] if (root / "SKILL.md").is_file() else sorted(path for path in root.iterdir() if path.is_dir())
    failures = 0
    for skill_dir in skill_dirs:
        errors = validate_skill(skill_dir)
        if errors:
            failures += 1
            print(f"INVALID {skill_dir}")
            for error in errors:
                print(f"- {error}")
        else:
            print(f"VALID {skill_dir}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
