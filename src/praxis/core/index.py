"""In-memory repository index.

Builds ``entities_by_id`` and ``entities_by_type`` from parsed entities and
flags duplicates and parse errors. Relation resolution lives in
:mod:`praxis.core.relations`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from praxis.config import PraxisConfig
from praxis.core.entity import Entity
from praxis.core.loader import load_entities


@dataclass
class Repository:
    """One loaded PraxisOS repository (read model)."""

    config: PraxisConfig
    entities_by_id: dict[str, Entity] = field(default_factory=dict)
    entities_by_type: dict[str, list[Entity]] = field(default_factory=dict)
    duplicates: list[str] = field(default_factory=list)
    parse_errors: list[tuple[Path, Exception]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.entities_by_type:
            for t in ("value", "model", "principle", "decision", "experiment", "review"):
                self.entities_by_type.setdefault(t, [])

    # -- lookup --------------------------------------------------------
    def by_id(self, id_: str) -> Entity | None:
        return self.entities_by_id.get(id_)

    def by_type(self, entity_type: str) -> list[Entity]:
        return self.entities_by_type.get(entity_type, [])

    @property
    def all_entities(self) -> list[Entity]:
        return list(self.entities_by_id.values())

    @property
    def ids(self) -> set[str]:
        return set(self.entities_by_id)

    @staticmethod
    def load(config: PraxisConfig) -> "Repository":
        """Load a repository from disk: scan, parse, index."""
        entities, errors = load_entities(config)
        repo = Repository(
            config=config,
            entities_by_id={},
            entities_by_type={},
            parse_errors=errors,
        )
        for entity in entities:
            existing = repo.entities_by_id.get(entity.id)
            if existing is not None:
                repo.duplicates.append(entity.id)
            # first occurrence wins for lookup; duplicates are reported
            repo.entities_by_id.setdefault(entity.id, entity)
            bucket = repo.entities_by_type.setdefault(entity.type, [])
            bucket.append(entity)
        return repo