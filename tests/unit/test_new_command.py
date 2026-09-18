"""Tests for `praxis new` (Phase 5, TC-5.x)."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from praxis.config import load_config
from praxis.commands.new import build_entity
from praxis.core.index import Repository
from praxis.core.parser import parse_file
from praxis.core.ids import IdError
from praxis.validation.schema import validate_entity_schema

REPO_ROOT = Path(__file__).resolve().parents[2]

CONFIG_TEXT = """\
version: 1
paths:
  values: values
  models: models
  principles: principles
  decisions: decisions
  experiments: experiments
  reviews: reviews
privacy:
  ignored:
    - private/**
validation:
  require_counter_evidence: true
  require_principle_boundary: true
  require_decision_next_action: true
"""


@pytest.fixture
def repo(tmp_path: Path):
    (tmp_path / "praxis.yaml").write_text(CONFIG_TEXT, encoding="utf-8")
    shutil.copytree(REPO_ROOT / "templates", tmp_path / "templates")
    for d in ("values", "models", "principles", "decisions", "experiments", "reviews", "constitution"):
        (tmp_path / d).mkdir()
    return tmp_path


def test_create_principle(repo: Path) -> None:
    """TC-5.1: praxis new principle creates a schema-valid file with unique ID."""
    config = load_config(repo)
    path = build_entity(config, "principle", "Test Principle", "career", None, None)
    assert path.is_file()
    assert path.name.startswith("PRINCIPLE-CAREER-001-")

    entity = parse_file(path)
    assert entity.id == "PRINCIPLE-CAREER-001"
    assert entity.metadata["status"] == "candidate"
    assert entity.metadata["domains"] == ["career"]
    assert validate_entity_schema(entity) == []

    # ID is unique across the repo
    repo_index = Repository.load(config)
    assert repo_index.by_id("PRINCIPLE-CAREER-001") is not None


def test_second_principle_gets_next_id(repo: Path) -> None:
    config = load_config(repo)
    build_entity(config, "principle", "One", "career", None, None)
    second = build_entity(config, "principle", "Two", "career", None, None)
    assert second.name.startswith("PRINCIPLE-CAREER-002-")


def test_create_decision_with_domain(repo: Path) -> None:
    config = load_config(repo)
    path = build_entity(config, "decision", "Test Decision", "finance", None, None)
    assert "decisions" in str(path) and "finance" in str(path)
    entity = parse_file(path)
    assert entity.metadata["domain"] == "finance"
    assert validate_entity_schema(entity) == []


def test_create_value(repo: Path) -> None:
    config = load_config(repo)
    path = build_entity(config, "value", "Autonomy", "life", None, None)
    entity = parse_file(path)
    assert entity.id == "VALUE-LIFE-001"
    assert validate_entity_schema(entity) == []


def test_create_model_with_type(repo: Path) -> None:
    config = load_config(repo)
    path = build_entity(config, "model", "Stoicism", None, None, "philosophy")
    assert "philosophies" in str(path)
    entity = parse_file(path)
    assert entity.metadata["model_type"] == "philosophy"
    assert validate_entity_schema(entity) == []


def test_create_review_by_type(repo: Path) -> None:
    config = load_config(repo)
    path = build_entity(config, "review", "Weekly Check", None, "weekly", None)
    assert "weekly" in str(path)
    entity = parse_file(path)
    assert entity.metadata["review_type"] == "weekly"
    assert validate_entity_schema(entity) == []


def test_invalid_domain_rejected_no_file(repo: Path) -> None:
    """TC-5.5: invalid domain is a controlled error; no file is created."""
    config = load_config(repo)
    before = list((repo / "principles").rglob("*.md"))
    with pytest.raises(ValueError):
        build_entity(config, "principle", "Bad", "bad domain!", None, None)
    after = list((repo / "principles").rglob("*.md"))
    assert before == after


def test_unsupported_type_rejected(repo: Path) -> None:
    config = load_config(repo)
    with pytest.raises(ValueError):
        build_entity(config, "task", "Nope", None, None, None)  # type: ignore[arg-type]