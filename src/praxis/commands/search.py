"""praxis search — metadata + full-text search (no embeddings in v0.1).

    praxis search "离职"
    praxis search "autonomy" --type value
    praxis search --status testing
    praxis search --domain career
    praxis search --related VALUE-LIFE-001
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from praxis.config import find_repo_root, load_config
from praxis.core.entity import Entity
from praxis.core.index import Repository


def entity_matches(
    entity: Entity,
    query: str | None = None,
    entity_type: str | None = None,
    status: str | None = None,
    domain: str | None = None,
    related: str | None = None,
) -> bool:
    """Whether one entity satisfies every supplied filter."""
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
    if query:
        needle = query.lower()
        haystack = " ".join(
            [str(v) for v in entity.metadata.values() if isinstance(v, (str, int))]
            + [entity.body, entity.id]
        ).lower()
        if needle not in haystack:
            return False
    return True


def search(
    repo: Repository,
    query: str | None = None,
    entity_type: str | None = None,
    status: str | None = None,
    domain: str | None = None,
    related: str | None = None,
) -> list[Entity]:
    return [
        entity
        for entity in sorted(repo.all_entities, key=lambda e: e.id)
        if entity_matches(entity, query, entity_type, status, domain, related)
    ]


def render(results: list[Entity]) -> str:
    if not results:
        return "no matches"
    lines = [f"{len(results)} match(es):"]
    for entity in results:
        lines.append(
            f"  {entity.id}  [{entity.type}/{entity.metadata.get('status', '-')}]  "
            f"{entity.title}"
        )
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    try:
        root = Path(args.root).resolve() if getattr(args, "root", None) else find_repo_root()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    config = load_config(root)
    repo = Repository.load(config)
    results = search(
        repo,
        query=getattr(args, "query", None),
        entity_type=getattr(args, "type", None),
        status=getattr(args, "status", None),
        domain=getattr(args, "domain", None),
        related=getattr(args, "related", None),
    )
    print(render(results))
    return 0