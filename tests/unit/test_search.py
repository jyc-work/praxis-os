"""Tests for `praxis search` filters (Phase 5, TC-5.2/5.3)."""

from __future__ import annotations

from pathlib import Path

from praxis.config import load_config
from praxis.core.index import Repository
from praxis.commands.search import entity_matches, render, search

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def _repo() -> Repository:
    return Repository.load(load_config(FIXTURES / "valid_repo"))


def test_search_by_text() -> None:
    """TC-5.2: full-text search returns matching entities."""
    results = search(_repo(), query="焦虑")
    assert any(e.id == "PRINCIPLE-LIFE-001" for e in results)


def test_search_by_status() -> None:
    """TC-5.3: --status returns only that status."""
    results = search(_repo(), status="candidate")
    assert [e.id for e in results] == ["PRINCIPLE-LIFE-001"]
    results = search(_repo(), status="validated")
    assert results == []


def test_search_by_type() -> None:
    results = search(_repo(), entity_type="principle")
    assert [e.id for e in results] == ["PRINCIPLE-LIFE-001"]


def test_search_by_domain() -> None:
    results = search(_repo(), domain="life")
    ids = {e.id for e in results}
    assert "VALUE-LIFE-001" in ids
    assert "PRINCIPLE-LIFE-001" in ids


def test_search_by_related() -> None:
    results = search(_repo(), related="VALUE-LIFE-001")
    ids = {e.id for e in results}
    assert "PRINCIPLE-LIFE-001" in ids  # principle references the value


def test_search_no_match() -> None:
    assert search(_repo(), query="不存在的关键字xyz") == []


def test_entity_matches_all_filters_and() -> None:
    repo = _repo()
    entity = repo.by_id("PRINCIPLE-LIFE-001")
    assert entity_matches(entity, query="焦虑", entity_type="principle", status="candidate")


def test_render_empty_and_nonempty() -> None:
    assert render([]) == "no matches"
    out = render(search(_repo(), query="焦虑"))
    assert "PRINCIPLE-LIFE-001" in out