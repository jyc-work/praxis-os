"""Final acceptance: the full v0.1 acceptance flow, end to end.

Implementation Plan §15:

    Create Value → Create Model → Extract Principle → Create Decision
    → Attach Relevant Principle → Create Experiment → Record Outcome
    → Create Review → Revise Principle → praxis validate → PASS
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from praxis.commands.new import build_entity
from praxis.config import load_config
from praxis.commands.validate import run_validation
from praxis.core.index import Repository
from praxis.core.relations import resolve_relations

REPO_ROOT = Path(__file__).resolve().parents[2]

CONFIG_TEXT = """\
version: 1
paths:
  constitution: constitution
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
def fresh_repo(tmp_path: Path) -> Path:
    (tmp_path / "praxis.yaml").write_text(CONFIG_TEXT, encoding="utf-8")
    shutil.copytree(REPO_ROOT / "templates", tmp_path / "templates")
    for d in ("values", "models", "principles", "decisions", "experiments", "reviews", "constitution"):
        (tmp_path / d).mkdir()
    return tmp_path


def _edit(path: Path, replacements: dict[str, str]) -> None:
    """Apply frontmatter replacements (helper for wiring relations)."""
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        assert old in text, f"pattern not found in {path.name}: {old!r}"
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


@pytest.mark.parametrize("use_demo_repo", [False, True])
def test_acceptance_flow_completes_and_validates(fresh_repo: Path, use_demo_repo: bool) -> None:
    """The v0.1 acceptance flow ends with `praxis validate` → PASS."""
    if use_demo_repo:
        issues, _ = run_validation(REPO_ROOT / "examples" / "demo-persona")
        failures = [i for i in issues if i.severity.name in ("ERROR", "FATAL")]
        assert failures == [], [f.format() for f in failures]
        return

    config = load_config(fresh_repo)

    # 1. Create Value
    value = build_entity(config, "value", "Focus", "life", None, None)
    # 2. Create Model
    model = build_entity(config, "model", "Deep Work", None, None, "mental-model")
    # 3. Extract Principle (candidate)
    principle = build_entity(config, "principle", "深度工作优先于碎片响应", "career", None, None)
    assert "PRINCIPLE-CAREER-001" in principle.name
    # 4+5. Create Decision, attach the relevant principle
    decision = build_entity(config, "decision", "是否接受管理岗", "career", None, None)
    decision_text = decision.read_text(encoding="utf-8")
    decision_text = decision_text.replace(
        "related_principles: []",
        "related_principles:\n  - PRINCIPLE-CAREER-001",
    )
    decision.write_text(decision_text, encoding="utf-8")
    # 6+7. Create Experiment, record outcome
    experiment = build_entity(config, "experiment", "30 天深度工作实验", "career", None, None)
    experiment_text = experiment.read_text(encoding="utf-8")
    experiment_text = experiment_text.replace(
        "status: planned", "status: completed"
    ).replace(
        "related_decision: []",
        "related_decision:\n  - DECISION-CAREER-001",
    ).replace(
        "related_principles: []",
        "related_principles:\n  - PRINCIPLE-CAREER-001",
    ).replace(
        "# Actual Result\n\n# What I Learned",
        "# Actual Result\n\n实验完成：深度工作时间提升 40%。\n\n# What I Learned",
    )
    experiment.write_text(experiment_text, encoding="utf-8")
    # 8. Create Review (decision review)
    review = build_entity(config, "review", "管理岗决策复盘", None, "decision", None)
    review_text = review.read_text(encoding="utf-8")
    review_text = review_text.replace(
        "review_type: decision", "review_type: decision"
    ).replace(
        "review_date: 2026-09-17", "review_date: 2026-09-17"
    )
    review.write_text(review_text, encoding="utf-8")

    # 9. Revise Principle (candidate → testing with revision history)
    principle_text = principle.read_text(encoding="utf-8")
    principle_text = principle_text.replace(
        "status: candidate", "status: testing"
    ).replace(
        "## Revision History\n\n- 2026-09-17: 创建为 candidate。未经现实检验，不得升级为 validated。",
        "## Revision History\n\n- 2026-09-17: 创建为 candidate。\n- 2026-09-18: 升级为 testing——实验提供了支持证据。",
    )
    principle.write_text(principle_text, encoding="utf-8")

    # 10. Run praxis validate → PASS (no ERROR/FATAL)
    issues, repo = run_validation(fresh_repo)
    failures = [i for i in issues if i.severity.name in ("ERROR", "FATAL")]
    assert failures == [], [f.format() for f in failures]

    # relations all resolve
    broken = resolve_relations(repo.all_entities, repo.ids)
    assert broken == []


def test_acceptance_negative_control(fresh_repo: Path) -> None:
    """AC-02/AC-03: an invalid status and a broken relation are both detected."""
    from praxis.core.parser import parse_file
    from praxis.commands.validate import run_validation as run_val
    from praxis.validation.schema import validate_entity_schema
    from praxis.validation.repository import validate_repository
    from praxis.validation.issue import Severity

    config = load_config(fresh_repo)
    principle = build_entity(config, "principle", "坏状态原则", "career", None, None)
    text = principle.read_text(encoding="utf-8").replace("status: candidate", "status: approved")
    principle.write_text(text, encoding="utf-8")

    entity = parse_file(principle)
    schema_issues = validate_entity_schema(entity)
    assert any(i.severity in (Severity.ERROR, Severity.FATAL) for i in schema_issues)

    # broken relation
    decision = build_entity(config, "decision", "带断链的决策", "career", None, None)
    dtext = decision.read_text(encoding="utf-8").replace(
        "related_principles: []",
        "related_principles:\n  - PRINCIPLE-404",
    )
    decision.write_text(dtext, encoding="utf-8")
    repo = Repository.load(config)
    repo_issues = validate_repository(repo)
    assert any(i.code == "BROKEN_RELATION" for i in repo_issues)

    issues, _ = run_val(fresh_repo)
    assert any(i.severity.name in ("ERROR", "FATAL") for i in issues)  # validate fails