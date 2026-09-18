"""Repository index tests (Phase 3)."""

from __future__ import annotations

from pathlib import Path

from praxis.config import load_config
from praxis.core.index import Repository

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_repository_load_valid() -> None:
    repo = Repository.load(load_config(FIXTURES / "valid_repo"))
    assert repo.parse_errors == []
    assert repo.duplicates == []
    assert len(repo.all_entities) == 6


def test_by_id_lookup() -> None:
    repo = Repository.load(load_config(FIXTURES / "valid_repo"))
    entity = repo.by_id("PRINCIPLE-LIFE-001")
    assert entity is not None
    assert entity.type == "principle"
    assert repo.by_id("PRINCIPLE-404") is None


def test_by_type_index() -> None:
    """TC-3.5: by_type returns every entity of a type."""
    repo = Repository.load(load_config(FIXTURES / "valid_repo"))
    assert len(repo.by_type("principle")) == 1
    assert len(repo.by_type("value")) == 1
    assert len(repo.by_type("model")) == 1
    assert len(repo.by_type("decision")) == 1
    assert len(repo.by_type("experiment")) == 1
    assert len(repo.by_type("review")) == 1


def test_duplicate_id_detected() -> None:
    """TC-3.3: duplicate IDs are flagged by the index."""
    repo = Repository.load(load_config(FIXTURES / "invalid_repo"))
    assert "PRINCIPLE-CAREER-002" in repo.duplicates


def test_private_not_indexed() -> None:
    repo = Repository.load(load_config(FIXTURES / "valid_repo"))
    paths = {str(e.path) for e in repo.all_entities}
    assert not any("private" in p for p in paths)