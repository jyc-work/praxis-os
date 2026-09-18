"""Core domain object: Entity.

An Entity is one Markdown file with YAML frontmatter, loaded from a PraxisOS
repository. It carries no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Entity:
    """One parsed PraxisOS record."""

    id: str
    type: str
    metadata: dict
    body: str
    path: Path
    #: raw parsed frontmatter before date normalisation, kept for debugging
    raw_metadata: dict = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("entity id must not be empty")

    @property
    def title(self) -> str:
        return str(self.metadata.get("title") or self.metadata.get("name") or self.id)