"""Full-text search over markdown bodies and metadata (no embeddings).

Plain substring search, case-insensitive, over:

    entity.body + every string metadata value + entity.id

Matches any occurrence of the query as a substring. Deterministic.
"""

from __future__ import annotations

from praxis.core.entity import Entity


def matches_text(entity: Entity, query: str) -> bool:
    """Whether the query appears in body, metadata strings, or the ID."""
    needle = query.strip().lower()
    if not needle:
        return True
    parts = [entity.body, entity.id]
    for key, value in entity.metadata.items():
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, (int, float)):
            parts.append(str(value))
        elif isinstance(value, list):
            parts.extend(str(v) for v in value if isinstance(v, (str, int, float)))
    return needle in " ".join(parts).lower()