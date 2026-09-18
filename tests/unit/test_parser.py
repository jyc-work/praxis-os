"""Parser unit tests (Phase 3, TC-3.x)."""

from __future__ import annotations

from pathlib import Path

import pytest

from praxis.core.parser import ParseError, normalise_metadata, parse_file

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
VALID = FIXTURES / "valid_repo"
INVALID = FIXTURES / "invalid_repo"


def test_parse_valid_markdown() -> None:
    entity = parse_file(VALID / "principles" / "life" / "PRINCIPLE-LIFE-001-anxiety-action.md")
    assert entity.id == "PRINCIPLE-LIFE-001"
    assert entity.type == "principle"
    assert entity.metadata["title"] == "对不可控结果持续焦虑时，转向 24 小时内可执行的可控动作"
    assert "## Statement" in entity.body
    assert entity.path.name.endswith(".md")


def test_parse_normalises_dates() -> None:
    entity = parse_file(VALID / "principles" / "life" / "PRINCIPLE-LIFE-001-anxiety-action.md")
    assert isinstance(entity.metadata["created_at"], str)
    assert entity.metadata["created_at"] == "2026-09-17"


def test_parse_body_preserved() -> None:
    entity = parse_file(VALID / "values" / "VALUE-LIFE-001-autonomy.md")
    assert "## Definition" in entity.body
    assert "## Revision History" in entity.body


def test_parse_invalid_yaml_raises_controlled_error() -> None:
    """TC-3.2: invalid YAML must raise ParseError, not a raw traceback."""
    with pytest.raises(ParseError) as excinfo:
        parse_file(INVALID / "principles" / "career" / "PRINCIPLE-CAREER-001-broken.yaml.md")
    assert excinfo.value.cause == "invalid-yaml"
    assert excinfo.value.path.name.endswith(".md")


def test_parse_missing_frontmatter_raises() -> None:
    with pytest.raises(ParseError) as excinfo:
        parse_file(INVALID / "principles" / "career" / "no-frontmatter.md")
    assert excinfo.value.cause == "missing-frontmatter"


def test_parse_missing_id_raises(tmp_path: Path) -> None:
    tmp = tmp_path / "no_id.md"
    tmp.write_text(
        "---\ntype: principle\ntitle: x\n---\n\n# body\n", encoding="utf-8"
    )
    with pytest.raises(ParseError) as excinfo:
        parse_file(tmp)
    assert excinfo.value.cause == "missing-id"


def test_normalise_metadata_recursive() -> None:
    import datetime

    data = {
        "date": datetime.date(2026, 9, 17),
        "when": datetime.datetime(2026, 9, 17, 10, 30),
        "nested": {"d": datetime.date(2026, 1, 1)},
        "list": [datetime.date(2026, 2, 2)],
        "keep": "text",
    }
    out = normalise_metadata(data)
    assert out["date"] == "2026-09-17"
    assert out["when"] == "2026-09-17"
    assert out["nested"]["d"] == "2026-01-01"
    assert out["list"] == ["2026-02-02"]
    assert out["keep"] == "text"