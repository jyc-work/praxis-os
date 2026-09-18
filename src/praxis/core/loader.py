"""Repository scanner: walks configured entity directories and parses files.

The loader never enters private/ignored paths and never touches .git, tests,
examples or templates.
"""

from __future__ import annotations

from pathlib import Path

from praxis.config import PraxisConfig
from praxis.core.parser import ParseError, parse_file

#: path segments that are always excluded from scanning
PRIVATE_SEGMENTS = {".git", "private", "tests", "examples", "templates", "schemas", "skills", "docs"}
#: file names always excluded
EXCLUDED_FILES = {"README.md"}
EXCLUDED_SUFFIXES = {".template.md", ".schema.json"}


def _is_ignored(rel: Path, ignored_patterns: list[str]) -> bool:
    from fnmatch import fnmatch

    text = rel.as_posix()
    if text in {"", "."}:
        return False
    if rel.name in EXCLUDED_FILES or rel.name.startswith("."):
        return True
    if any(rel.suffix == s or rel.name.endswith(s) for s in EXCLUDED_SUFFIXES):
        return True
    if any(part in PRIVATE_SEGMENTS for part in rel.parts):
        return True
    for pattern in ignored_patterns:
        if fnmatch(text, pattern) or fnmatch(rel.name, pattern):
            return True
    return False


def collect_markdown_files(root: Path, ignored_patterns: list[str]) -> list[Path]:
    """Return every candidate Markdown file under ``root`` (non-recursive-safe)."""
    if not root.is_dir():
        return []
    return [
        path
        for path in root.rglob("*.md")
        if not _is_ignored(path.relative_to(root), ignored_patterns)
    ]


def load_entities(config: PraxisConfig) -> tuple[list, list]:
    """Scan configured directories and parse everything.

    Returns:
        (entities, errors) where errors is a list of (path, ParseError).
    """
    entities: list = []
    errors: list[tuple[Path, ParseError]] = []
    seen_files: set[Path] = set()

    for entity_dir in config.entity_dirs().values():
        for path in collect_markdown_files(entity_dir, config.privacy_ignored):
            resolved = path.resolve()
            if resolved in seen_files:
                continue
            seen_files.add(resolved)
            try:
                entities.append(parse_file(path))
            except ParseError as exc:
                errors.append((path, exc))
    return entities, errors