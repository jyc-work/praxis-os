"""Stable ID utilities.

ID format: ``TYPE-DOMAIN-NNN``  (e.g. ``PRINCIPLE-CAREER-001``).

Rules:
- an ID never changes because a title changed;
- retired IDs are never reused;
- relations reference IDs, never file paths.
"""

from __future__ import annotations

import re

ENTITY_TYPES = ("value", "model", "principle", "decision", "experiment", "review")

# TYPE prefix per entity type
TYPE_PREFIX = {
    "value": "VALUE",
    "model": "MODEL",
    "principle": "PRINCIPLE",
    "decision": "DECISION",
    "experiment": "EXPERIMENT",
    "review": "REVIEW",
}
PREFIX_TO_TYPE = {v: k for k, v in TYPE_PREFIX.items()}

_ID_RE = re.compile(r"^([A-Z]+)-([A-Z]+)-(\d{3})$")

#: relation fields that hold IDs of other entities, per entity type
RELATION_FIELDS: dict[str, tuple[str, ...]] = {
    "value": ("conflicts_with", "related_values"),
    "model": ("derived_principles", "related_values"),
    "principle": (
        "sources", "evidence", "related_values", "related_models",
        "related_principles",
    ),
    "decision": (
        "related_values", "related_models", "related_principles",
        "experiments",
    ),
    "experiment": ("related_decision", "related_principles"),
    "review": ("target", "principles_changed"),
}


class IdError(ValueError):
    """Raised when an ID violates the PraxisOS ID contract."""


def validate_id(entity_type: str, id_: str) -> None:
    """Validate ``id_`` against the TYPE-DOMAIN-NNN contract for entity_type."""
    prefix = TYPE_PREFIX.get(entity_type)
    if prefix is None:
        raise IdError(f"unknown entity type {entity_type!r}")
    match = _ID_RE.match(id_)
    if match is None:
        raise IdError(
            f"invalid ID {id_!r}: expected {prefix}-DOMAIN-NNN"
        )
    actual_prefix, _, _ = match.groups()
    if actual_prefix != prefix:
        raise IdError(
            f"ID prefix {actual_prefix!r} does not match entity type "
            f"{entity_type!r} (expected {prefix!r})"
        )


def parse_id(id_: str) -> tuple[str, str, int]:
    """Split an ID into (entity_type, domain, number)."""
    match = _ID_RE.match(id_)
    if match is None:
        raise IdError(f"invalid ID format {id_!r}")
    prefix, domain, number = match.groups()
    entity_type = PREFIX_TO_TYPE.get(prefix)
    if entity_type is None:
        raise IdError(f"unknown ID prefix {prefix!r}")
    return entity_type, domain, int(number)


def domain_of(id_: str) -> str:
    """Return the domain part of an ID."""
    _, domain, _ = parse_id(id_)
    return domain


def next_id(existing: list[str], entity_type: str, domain: str) -> str:
    """Generate the next unused ID for (entity_type, domain).

    ``existing`` is every ID currently present in the repository.
    """
    if entity_type not in TYPE_PREFIX:
        raise IdError(f"unknown entity type {entity_type!r}")
    prefix = TYPE_PREFIX[entity_type]
    expected = re.compile(rf"^{re.escape(prefix)}-{re.escape(domain)}-(\d{{3}})$")
    max_number = 0
    for id_ in existing:
        match = expected.match(id_)
        if match:
            max_number = max(max_number, int(match.group(1)))
    return f"{prefix}-{domain}-{max_number + 1:03d}"