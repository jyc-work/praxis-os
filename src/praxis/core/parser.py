"""Markdown + frontmatter parser.

Reads one Markdown file and produces an :class:`Entity`. The parser is
responsible only for mechanical extraction:

    read file → parse YAML frontmatter → extract body → normalise metadata

Schema validation, semantic validation and relation resolution happen in
later layers, never here.
"""

from __future__ import annotations

import datetime
from pathlib import Path

import frontmatter

from praxis.core.entity import Entity


class ParseError(ValueError):
    """Controlled parse failure — never a raw stack trace.

    Attributes:
        path: the file that failed to parse.
        cause: short human-readable reason (e.g. ``invalid-yaml``).
        detail: optional longer message.
    """

    def __init__(self, path: Path, cause: str, detail: str = "") -> None:
        self.path = path
        self.cause = cause
        self.detail = detail
        super().__init__(f"{path}: {cause}" + (f" — {detail}" if detail else ""))


def normalise_metadata(raw: dict) -> dict:
    """Recursively convert YAML date objects to ISO date strings.

    YAML parses ``2026-09-17`` as ``datetime.date``; the JSON Schemas require
    ``"YYYY-MM-DD"`` strings, so this normalisation is part of the parser
    contract and applies to every frontmatter the loader reads.
    """
    out: dict = {}
    for key, value in raw.items():
        out[key] = _normalise(value)
    return out


def _normalise(value):
    if isinstance(value, datetime.datetime):
        return value.date().isoformat()
    if isinstance(value, datetime.date):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _normalise(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalise(v) for v in value]
    return value


def parse_file(path: Path) -> Entity:
    """Parse one Markdown file into an Entity.

    Raises:
        ParseError: when the file cannot be read, has no frontmatter,
            invalid YAML, or an empty/invalid entity id.
    """
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ParseError(path, "unreadable", str(exc)) from exc

    try:
        post = frontmatter.loads(text)
    except Exception as exc:  # frontmatter wraps YAML errors in its own type
        raise ParseError(path, "invalid-yaml", str(exc)) from exc

    metadata = dict(post.metadata or {})
    if not metadata:
        raise ParseError(path, "missing-frontmatter", "no YAML frontmatter found")

    raw = normalise_metadata(metadata)
    entity_type = str(raw.get("type") or "")
    entity_id = str(raw.get("id") or "")
    if not entity_id:
        raise ParseError(path, "missing-id", "frontmatter has no `id`")

    return Entity(
        id=entity_id,
        type=entity_type,
        metadata=raw,
        body=str(post.content or ""),
        path=path,
        raw_metadata=metadata,
    )