"""Level 1 validation: JSON Schema conformance per entity type."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from praxis.core.entity import Entity
from praxis.validation.issue import Severity, ValidationIssue

SCHEMA_DIR = Path(__file__).resolve().parents[3] / "schemas"

_SCHEMA_CACHE: dict[str, dict] = {}


def load_schema(entity_type: str) -> dict:
    """Load one JSON Schema (cached)."""
    if entity_type not in _SCHEMA_CACHE:
        path = SCHEMA_DIR / f"{entity_type}.schema.json"
        if not path.is_file():
            raise FileNotFoundError(f"missing schema for entity type {entity_type!r}")
        with path.open(encoding="utf-8") as fh:
            _SCHEMA_CACHE[entity_type] = json.load(fh)
    return _SCHEMA_CACHE[entity_type]


def validate_entity_schema(entity: Entity) -> list[ValidationIssue]:
    """Validate one entity's frontmatter against its JSON Schema."""
    issues: list[ValidationIssue] = []

    try:
        schema = load_schema(entity.type)
    except FileNotFoundError as exc:
        issues.append(
            ValidationIssue(
                Severity.FATAL,
                "UNKNOWN_SCHEMA",
                str(exc),
                path=entity.path,
                entity_id=entity.id,
            )
        )
        return issues

    validator = jsonschema.Draft7Validator(
        schema, format_checker=jsonschema.FormatChecker()
    )
    errors = sorted(validator.iter_errors(entity.metadata), key=lambda e: list(e.path))
    if not errors:
        return issues

    # Report the most representative error(s), capped to stay readable.
    for error in errors[:5]:
        where = ".".join(str(p) for p in error.path) or "(root)"
        issues.append(
            ValidationIssue(
                Severity.FATAL if _is_fatal(entity.type, where, error) else Severity.ERROR,
                "SCHEMA",
                f"field `{where}`: {error.message}",
                path=entity.path,
                entity_id=entity.id,
                section=where,
            )
        )
    return issues


def _is_fatal(entity_type: str, where: str, error: jsonschema.ValidationError) -> bool:
    # Missing/invalid id or wrong type makes the document unusable.
    if where in {"id", "type"}:
        return True
    if entity_type and entity_type not in {
        "value", "model", "principle", "decision", "experiment", "review"
    }:
        return True
    return False