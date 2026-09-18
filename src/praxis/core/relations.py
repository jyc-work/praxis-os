"""Relation model: every reference between entities is an ID reference.

Resolution pipeline:

    Repository scan → build ID index → resolve relations → report missing IDs

Relations are read from the metadata fields documented in
:mod:`praxis.core.ids` (``RELATION_FIELDS``). No file-path references are
allowed anywhere in v0.1.
"""

from __future__ import annotations

from dataclasses import dataclass

from praxis.core.entity import Entity
from praxis.core.ids import RELATION_FIELDS, parse_id

#: relation fields that are lists of IDs (all of them in v0.1)
_LIST_FIELDS = {
    "conflicts_with", "related_values", "derived_principles", "sources",
    "evidence", "related_models", "related_principles", "experiments",
    "related_decision", "target", "principles_changed",
}


@dataclass(frozen=True)
class Relation:
    """One outgoing edge from ``source`` to ``target_id``."""

    source_id: str
    field: str
    target_id: str


@dataclass(frozen=True)
class BrokenRelation:
    """An edge whose target ID does not exist in the repository."""

    source_id: str
    field: str
    target_id: str
    source_path: str


def _id_fields(entity_type: str) -> tuple[str, ...]:
    return RELATION_FIELDS.get(entity_type, ())


def collect_relations(entity: Entity) -> list[Relation]:
    """Extract all ID-valued edges declared by one entity's frontmatter."""
    relations: list[Relation] = []
    for field in _id_fields(entity.type):
        value = entity.metadata.get(field)
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            targets = [v for v in value if isinstance(v, str) and v]
        elif isinstance(value, str) and value:
            targets = [value]
        else:
            targets = []
        for target_id in targets:
            if isinstance(target_id, str) and target_id.strip():
                relations.append(Relation(entity.id, field, target_id.strip()))
    return relations


def resolve_relations(entities: list[Entity], known_ids: set[str]) -> list[BrokenRelation]:
    """Resolve every relation in the repository against the ID index.

    Returns the list of broken (missing target) relations.
    """
    broken: list[BrokenRelation] = []
    for entity in entities:
        for relation in collect_relations(entity):
            if relation.target_id not in known_ids:
                broken.append(
                    BrokenRelation(
                        source_id=relation.source_id,
                        field=relation.field,
                        target_id=relation.target_id,
                        source_path=str(entity.path),
                    )
                )
    return broken


def referenced_ids(entities: list[Entity]) -> set[str]:
    """All IDs referenced by any relation in the repository."""
    result: set[str] = set()
    for entity in entities:
        for relation in collect_relations(entity):
            result.add(relation.target_id)
    return result