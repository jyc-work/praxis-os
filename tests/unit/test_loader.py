"""Loader tests (Phase 3): scan, exclusion, parse error collection."""

from __future__ import annotations

from pathlib import Path

from praxis.config import load_config
from praxis.core.loader import collect_markdown_files, load_entities

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_loader_finds_all_valid_entities() -> None:
    config = load_config(FIXTURES / "valid_repo")
    entities, errors = load_entities(config)
    ids = {e.id for e in entities}
    assert "VALUE-LIFE-001" in ids
    assert "MODEL-STOICISM-001" in ids
    assert "PRINCIPLE-LIFE-001" in ids
    assert "DECISION-CAREER-001" in ids
    assert "EXPERIMENT-CAREER-001" in ids
    assert "REVIEW-DECISION-001" in ids
    assert errors == []


def test_private_folder_excluded() -> None:
    """TC-3.4: everything under private/ is not indexed."""
    config = load_config(FIXTURES / "valid_repo")
    entities, errors = load_entities(config)
    paths = {str(e.path) for e in entities}
    assert not any("private" in p for p in paths)

    collected = collect_markdown_files(
        FIXTURES / "valid_repo", config.privacy_ignored
    )
    assert not any("private" in str(p) for p in collected)


def test_loader_collects_parse_errors() -> None:
    config = load_config(FIXTURES / "invalid_repo")
    entities, errors = load_entities(config)
    causes = {exc.cause for _, exc in errors}
    assert "invalid-yaml" in causes
    assert "missing-frontmatter" in causes
    # valid duplicate files still parse; the broken ones are reported
    assert any(e.id == "PRINCIPLE-CAREER-002" for e in entities)


def test_loader_excludes_non_entity_dirs() -> None:
    from praxis.config import load_config as load
    from praxis.core.loader import collect_markdown_files

    config = load(FIXTURES / "valid_repo")
    files = collect_markdown_files(FIXTURES / "valid_repo", config.privacy_ignored)
    # scanning from repo root must never descend into tests/examples/templates
    assert not any("templates" in str(p) for p in files)