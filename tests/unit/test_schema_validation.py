"""Schema validation tests (Phase 4, Level 1)."""

from __future__ import annotations

from pathlib import Path

import pytest

from praxis.config import load_config
from praxis.core.index import Repository
from praxis.core.parser import ParseError, parse_file
from praxis.validation.issue import Severity
from praxis.validation.schema import validate_entity_schema

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_clean_repo_schema_passes() -> None:
    repo = Repository.load(load_config(FIXTURES / "valid_repo"))
    issues = []
    for entity in repo.all_entities:
        issues.extend(validate_entity_schema(entity))
    assert issues == []


def test_missing_id_yields_parse_error() -> None:
    tmp = Path(__file__).parent / "_no_id.md"
    tmp.write_text(
        "---\ntype: principle\ntitle: x\n---\n\n# body\n", encoding="utf-8"
    )
    try:
        with pytest.raises(ParseError) as excinfo:
            parse_file(tmp)
        assert excinfo.value.cause == "missing-id"
    finally:
        if tmp.exists():
            tmp.unlink()


def test_invalid_status_is_error() -> None:
    tmp = Path(__file__).parent / "_bad_status.md"
    tmp.write_text(
        "---\n"
        "id: PRINCIPLE-CAREER-099\n"
        "type: principle\n"
        "title: x\n"
        "status: approved\n"  # not in enum
        "confidence: low\n"
        "domains: [career]\n"
        "created_at: 2026-09-17\n"
        "updated_at: 2026-09-17\n"
        "---\n\n# body\n",
        encoding="utf-8",
    )
    try:
        entity = parse_file(tmp)
        issues = validate_entity_schema(entity)
        assert len(issues) == 1
        assert issues[0].code == "SCHEMA"
        assert issues[0].severity in (Severity.ERROR, Severity.FATAL)
    finally:
        if tmp.exists():
            tmp.unlink()


def test_wrong_id_prefix_is_error() -> None:
    tmp = Path(__file__).parent / "_bad_prefix.md"
    tmp.write_text(
        "---\n"
        "id: DECISION-CAREER-001\n"  # prefix mismatch with type=principle
        "type: principle\n"
        "title: x\n"
        "status: candidate\n"
        "confidence: low\n"
        "domains: [career]\n"
        "created_at: 2026-09-17\n"
        "updated_at: 2026-09-17\n"
        "---\n\n# body\n",
        encoding="utf-8",
    )
    try:
        entity = parse_file(tmp)
        issues = validate_entity_schema(entity)
        assert len(issues) == 1
        assert issues[0].severity in (Severity.ERROR, Severity.FATAL)
    finally:
        if tmp.exists():
            tmp.unlink()