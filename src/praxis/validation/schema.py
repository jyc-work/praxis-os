"""Level 1 validation: JSON Schema conformance per entity type."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

from praxis.core.entity import Entity
from praxis.validation.issue import Severity, ValidationIssue

#: fallback when no repository root / schema dir is supplied (tests, tooling)
_SCHEMA_DIR = Path(__file__).resolve().parents[3] / "schemas"


def _installed_schema_dir() -> Path:
    """Where the packaged default schemas land (wheel installs)."""
    for prefix in (sys.prefix, sys.base_prefix):
        candidate = Path(prefix) / "praxis_data" / "schemas"
        if candidate.is_dir():
            return candidate
    return _SCHEMA_DIR


def _resolve_schema_dir(schema_dir: Path | None) -> Path:
    """Priority: repository schemas/ → packaged defaults → source tree."""
    if schema_dir is not None and schema_dir.is_dir():
        return schema_dir
    return _installed_schema_dir()


def load_schema(entity_type: str, schema_dir: Path | None = None) -> dict:
    """Load one JSON Schema (cached per directory)."""
    base = _resolve_schema_dir(schema_dir)
    path = base / f"{entity_type}.schema.json"
    if not path.is_file():
        raise FileNotFoundError(f"missing schema for entity type {entity_type!r}")
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def validate_entity_schema(
    entity: Entity, schema_dir: Path | None = None
) -> list[ValidationIssue]:
    """Validate one entity's frontmatter against its JSON Schema.

    ``schema_dir`` points at a repository's ``schemas/`` folder so schemas work
    even when the package is installed from a wheel (schemas live in the repo).
    """
    issues: list[ValidationIssue] = []

    try:
        schema = load_schema(entity.type, schema_dir=schema_dir)
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