"""Repository validation tests (Phase 4, Level 2)."""

from __future__ import annotations

from pathlib import Path

import pytest

from praxis.config import load_config
from praxis.core.index import Repository
from praxis.core.relations import resolve_relations
from praxis.validation.issue import Severity
from praxis.validation.repository import validate_repository

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def codes(issues) -> list[str]:
    return sorted(i.code for i in issues)


def test_clean_repo_passes_repository_checks() -> None:
    repo = Repository.load(load_config(FIXTURES / "valid_repo"))
    issues = validate_repository(repo)
    assert issues == []


def test_broken_relation_detected() -> None:
    """TC-4.1: a reference to a missing ID is an ERROR BROKEN_RELATION."""
    repo = Repository.load(load_config(FIXTURES / "valid_repo"))
    broken = resolve_relations(repo.all_entities, repo.ids)
    assert broken == []

    # simulate a broken relation
    entity = repo.by_id("PRINCIPLE-LIFE-001")
    entity.metadata["related_values"].append("VALUE-404")
    issues = validate_repository(repo)
    assert any(
        i.code == "BROKEN_RELATION" and i.severity == Severity.ERROR
        for i in issues
    )


def test_duplicate_id_is_fatal() -> None:
    """TC-4.2: duplicate IDs are FATAL."""
    repo = Repository.load(load_config(FIXTURES / "invalid_repo"))
    issues = validate_repository(repo)
    assert any(
        i.code == "DUPLICATE_ID" and i.severity == Severity.FATAL for i in issues
    )