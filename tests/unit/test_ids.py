"""ID utility tests (Phase 3)."""

from __future__ import annotations

import pytest

from praxis.core.ids import (
    IdError,
    domain_of,
    next_id,
    parse_id,
    validate_id,
)


def test_parse_id() -> None:
    assert parse_id("PRINCIPLE-CAREER-001") == ("principle", "CAREER", 1)
    assert parse_id("VALUE-LIFE-001") == ("value", "LIFE", 1)
    assert parse_id("REVIEW-DECISION-003") == ("review", "DECISION", 3)


def test_parse_id_invalid_format() -> None:
    for bad in ("principle-career-001", "PRINCIPLE-CAREER", "PRINCIPLE-CAREER-001x", ""):
        with pytest.raises(IdError):
            parse_id(bad)


def test_validate_id_prefix_mismatch() -> None:
    with pytest.raises(IdError):
        validate_id("principle", "DECISION-CAREER-001")
    with pytest.raises(IdError):
        validate_id("unknown-type", "PRINCIPLE-CAREER-001")


def test_validate_id_ok() -> None:
    validate_id("principle", "PRINCIPLE-CAREER-001")
    validate_id("decision", "DECISION-FINANCE-010")


def test_domain_of() -> None:
    assert domain_of("MODEL-STOICISM-001") == "STOICISM"


def test_next_id_sequence() -> None:
    existing = [
        "PRINCIPLE-CAREER-001",
        "PRINCIPLE-CAREER-002",
        "DECISION-CAREER-001",
    ]
    assert next_id(existing, "principle", "CAREER") == "PRINCIPLE-CAREER-003"
    assert next_id(existing, "decision", "CAREER") == "DECISION-CAREER-002"
    assert next_id(existing, "value", "LIFE") == "VALUE-LIFE-001"


def test_next_id_no_collision_with_higher_number() -> None:
    existing = ["PRINCIPLE-CAREER-100"]
    assert next_id(existing, "principle", "CAREER") == "PRINCIPLE-CAREER-101"