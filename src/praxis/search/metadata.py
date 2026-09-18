"""Metadata-filtered search: type, status, domain, related-entity filters."""

from __future__ import annotations

from praxis.core.entity import Entity


def matches_metadata(
    entity: Entity,
    entity_type: str | None = None,
    status: str | None = None,
    domain: str | None = None,
    related: str | None = None,
) -> bool:
    """Whether one entity satisfies every supplied metadata filter."""
    if entity_type and entity.type != entity_type.rstrip("s"):
        return False
    if status and str(entity.metadata.get("status", "")) != status:
        return False
    if domain:
        domains = [str(d).lower() for d in entity.metadata.get("domains", []) or []]
        single = entity.metadata.get("domain")
        if single:
            domains.append(str(single).lower())
        if domain.lower() not in domains:
            return False
    if related:
        haystack: list[str] = []
        for key, value in entity.metadata.items():
            if isinstance(value, list):
                haystack.extend(str(v) for v in value)
            elif isinstance(value, str):
                haystack.append(value)
        if related not in haystack:
            return False
    return True