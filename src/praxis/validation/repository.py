"""Level 2 validation: repository-wide integrity.

Checks:
    duplicate IDs       → FATAL DUPLICATE_ID
    broken relations    → ERROR BROKEN_RELATION
    wrong ID prefix     → ERROR ID_PREFIX
    unknown entity type → ERROR UNKNOWN_TYPE
    wrong directory     → ERROR WRONG_DIRECTORY
    missing review target → ERROR MISSING_REVIEW_TARGET
"""

from __future__ import annotations

from pathlib import Path

from praxis.core.index import Repository
from praxis.core.ids import TYPE_PREFIX, validate_id
from praxis.core.relations import resolve_relations
from praxis.validation.issue import Severity, ValidationIssue


def validate_repository(repo: Repository) -> list[ValidationIssue]:
    """Run all Level-2 checks against an indexed repository."""
    issues: list[ValidationIssue] = []
    known_ids = repo.ids

    # -- duplicate IDs -------------------------------------------------
    for dup_id in repo.duplicates:
        issues.append(
            ValidationIssue(
                Severity.FATAL,
                "DUPLICATE_ID",
                f"duplicate ID {dup_id!r} used by more than one file",
                entity_id=dup_id,
            )
        )

    # -- parse errors --------------------------------------------------
    for path, exc in repo.parse_errors:
        issues.append(
            ValidationIssue(
                Severity.FATAL if exc.cause != "missing-frontmatter" else Severity.ERROR,
                "PARSE",
                str(exc),
                path=path,
            )
        )

    # -- ID prefix / entity type / directory ---------------------------
    for entity in repo.all_entities:
        prefix = TYPE_PREFIX.get(entity.type)
        if prefix is None:
            issues.append(
                ValidationIssue(
                    Severity.ERROR,
                    "UNKNOWN_TYPE",
                    f"unknown entity type {entity.type!r}",
                    path=entity.path,
                    entity_id=entity.id,
                )
            )
            continue

        try:
            validate_id(entity.type, entity.id)
        except ValueError as exc:
            issues.append(
                ValidationIssue(
                    Severity.ERROR,
                    "ID_PREFIX",
                    str(exc),
                    path=entity.path,
                    entity_id=entity.id,
                )
            )

        if not _has_correct_placement(repo, entity):
            issues.append(
                ValidationIssue(
                    Severity.ERROR,
                    "WRONG_DIRECTORY",
                    f"entity type {entity.type!r} must live under "
                    f"{repo.config.paths.get(entity.type + 's', entity.type + 's')}/"
                    f" (found at {entity.path.relative_to(repo.config.root)})",
                    path=entity.path,
                    entity_id=entity.id,
                )
            )

    # -- relations -----------------------------------------------------
    for broken in resolve_relations(repo.all_entities, known_ids):
        issues.append(
            ValidationIssue(
                Severity.ERROR,
                "BROKEN_RELATION",
                f"field {broken.field!r} references missing ID {broken.target_id!r}",
                path=Path(broken.source_path),
                entity_id=broken.source_id,
            )
        )

    # -- decision reviews must name their target -----------------------
    for entity in repo.by_type("review"):
        if (
            str(entity.metadata.get("review_type", "")) == "decision"
            and not entity.metadata.get("target")
            and entity.metadata.get("status") == "completed"
        ):
            issues.append(
                ValidationIssue(
                    Severity.ERROR,
                    "MISSING_REVIEW_TARGET",
                    "completed decision review has no target decision",
                    path=entity.path,
                    entity_id=entity.id,
                )
            )

    return issues


def _has_correct_placement(repo: Repository, entity) -> bool:
    """Entity type must map to its configured directory (any sub-level is fine)."""
    dir_name = repo.config.paths.get(entity.type + "s") or repo.config.paths.get(
        entity.type, entity.type + "s"
    )
    root = repo.config.root
    try:
        rel = entity.path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return rel.parts[0] == dir_name