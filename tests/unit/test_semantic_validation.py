"""Semantic validation tests (Phase 4, Level 3)."""

from __future__ import annotations

from pathlib import Path

from praxis.config import load_config
from praxis.core.index import Repository
from praxis.core.parser import parse_file
from praxis.validation.issue import Severity
from praxis.validation.semantic import (
    extract_sections,
    section_is_effectively_empty,
    validate_semantic,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_extract_sections_h1_and_h2() -> None:
    body = "# Situation\n\ncontent a\n\n## Facts\n\ncontent b\n\n# Unknowns\n\ncontent c"
    sections = extract_sections(body)
    assert sections["Situation"] == "content a"
    assert sections["Facts"] == "content b"
    assert sections["Unknowns"] == "content c"


def test_empty_section_detection() -> None:
    assert section_is_effectively_empty("")
    assert section_is_effectively_empty("  \n")
    assert section_is_effectively_empty("（待填写）")
    assert section_is_effectively_empty("...")
    assert not section_is_effectively_empty("fixture content")
    assert not section_is_effectively_empty("调研了市场，得到三个结论。")


def test_clean_principle_passes_semantic() -> None:
    repo = Repository.load(load_config(FIXTURES / "valid_repo"))
    entity = repo.by_id("PRINCIPLE-LIFE-001")
    issues = validate_semantic(entity)
    assert issues == []


def test_empty_boundary_is_warning() -> None:
    """TC-4.3: empty Boundary is at least a WARNING PRINCIPLE_BOUNDARY_*."""
    tmp = Path(__file__).parent / "_empty_boundary.md"
    tmp.write_text(
        "---\nid: PRINCIPLE-CAREER-099\ntype: principle\ntitle: x\n"
        "status: candidate\nconfidence: low\ndomains: [career]\n"
        "created_at: 2026-09-17\nupdated_at: 2026-09-17\n---\n\n"
        "# Principle\n\n## Statement\n\nok\n\n## Why\n\nok\n\n## Evidence\n\nok\n\n"
        "## Counter Evidence\n\nok\n\n## Boundary\n\n（待填写）\n\n## Trigger\n\nok\n\n"
        "## Action Rule\n\nok\n\n## Revision History\n\nv1\n",
        encoding="utf-8",
    )
    try:
        entity = parse_file(tmp)
        issues = validate_semantic(entity)
        codes = [i.code for i in issues]
        assert any("BOUNDARY" in c and "EMPTY" in c for c in codes)
        assert all(i.severity == Severity.WARNING for i in issues)
    finally:
        if tmp.exists():
            tmp.unlink()


def test_missing_action_rule_is_warning() -> None:
    tmp = Path(__file__).parent / "_missing_ar.md"
    tmp.write_text(
        "---\nid: PRINCIPLE-CAREER-098\ntype: principle\ntitle: x\n"
        "status: candidate\nconfidence: low\ndomains: [career]\n"
        "created_at: 2026-09-17\nupdated_at: 2026-09-17\n---\n\n# Principle\n\n"
        "## Statement\n\nok\n\n## Why\n\nok\n\n## Evidence\n\nok\n\n"
        "## Counter Evidence\n\nok\n\n## Boundary\n\nok\n\n## Trigger\n\nok\n\n"
        "## Revision History\n\nv1\n",
        encoding="utf-8",
    )
    try:
        entity = parse_file(tmp)
        issues = validate_semantic(entity)
        assert any("ACTION_RULE" in i.code and "MISSING" in i.code for i in issues)
    finally:
        if tmp.exists():
            tmp.unlink()


def test_planned_review_not_flagged_hard() -> None:
    repo = Repository.load(load_config(FIXTURES / "valid_repo"))
    entity = repo.by_id("REVIEW-DECISION-001")
    issues = validate_semantic(entity)
    # planned review may lack outcome data: only INFO, never WARNING/ERROR
    assert all(i.severity != Severity.WARNING for i in issues)