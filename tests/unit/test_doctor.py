"""Tests for `praxis doctor` health report (Phase 5, TC-5.4)."""

from __future__ import annotations

from pathlib import Path

from praxis.config import load_config
from praxis.core.index import Repository
from praxis.commands.doctor import diagnose

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def codes(findings) -> list[str]:
    return sorted(f.code for f in findings)


def test_valid_repo_has_no_findings() -> None:
    repo = Repository.load(load_config(FIXTURES / "valid_repo"))
    findings = diagnose(repo)
    # every entity in the valid fixture is related; values are used; no retired principle
    assert codes(findings) == []


def test_orphan_principle_detected(tmp_path: Path) -> None:
    """TC-5.4: a principle without relations is reported as orphan."""
    import shutil

    from praxis.commands.new import build_entity

    # minimal repo in tmp_path
    config_text = (FIXTURES / "valid_repo" / "praxis.yaml").read_text(encoding="utf-8")
    (tmp_path / "praxis.yaml").write_text(config_text, encoding="utf-8")
    shutil.copytree(Path(__file__).resolve().parents[2] / "templates", tmp_path / "templates")
    for d in ("values", "models", "principles", "decisions", "experiments", "reviews", "constitution"):
        (tmp_path / d).mkdir()

    config = load_config(tmp_path)
    path = build_entity(config, "principle", "Lonely", "career", None, None)
    assert path.is_file()

    repo = Repository.load(config)
    findings = diagnose(repo)
    assert any(
        f.code == "ORPHAN_PRINCIPLE" and f.entity_id == "PRINCIPLE-CAREER-001"
        for f in findings
    )