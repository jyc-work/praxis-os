"""Phase 6 tests: skill structure, demo persona integrity (TC-6.x)."""

from __future__ import annotations

from pathlib import Path

from praxis.config import load_config
from praxis.core.index import Repository
from praxis.core.relations import resolve_relations
from praxis.commands.validate import run_validation

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS = REPO_ROOT / "skills"
DEMO = REPO_ROOT / "examples" / "demo-persona"

REQUIRED_SKILL_HEADINGS = [
    "Purpose",
    "Inputs",
    "Required Context",
    "Procedure",
    "Output Contract",
    "Write Permissions",
    "Forbidden Actions",
    "Examples",
]

SKILL_NAMES = [
    "principle-extractor",
    "decision-review",
    "values-audit",
    "quarterly-review",
]


def test_tc61_skill_structure() -> None:
    """TC-6.1: every SKILL.md has the required headings."""
    for name in SKILL_NAMES:
        skill_md = SKILLS / name / "SKILL.md"
        assert skill_md.is_file(), f"missing {skill_md}"
        text = skill_md.read_text(encoding="utf-8")
        for heading in REQUIRED_SKILL_HEADINGS:
            assert f"# {heading}" in text, f"{name}: missing '# {heading}'"


def test_tc62_no_illegal_promotion_in_examples() -> None:
    """TC-6.2: principle-extractor example never promotes to validated/core."""
    output = (SKILLS / "principle-extractor" / "examples" / "output-01.md").read_text(
        encoding="utf-8"
    )
    assert "status: candidate" in output
    yaml_block = output.split("```")[1]
    assert "status: validated" not in yaml_block
    assert "status: core" not in yaml_block
    assert "Final Judgment" in (
        SKILLS / "decision-review" / "SKILL.md"
    ).read_text(encoding="utf-8")


def test_tc63_demo_persona_validates() -> None:
    """TC-6.3: `praxis validate examples/demo-persona` passes."""
    issues, _repo = run_validation(DEMO)
    failures = [i for i in issues if i.severity.name in ("ERROR", "FATAL")]
    assert failures == [], [f.format() for f in failures]


def test_tc64_demo_relation_integrity() -> None:
    """TC-6.4: every relation in the demo resolves."""
    config = load_config(DEMO)
    repo = Repository.load(config)
    broken = resolve_relations(repo.all_entities, repo.ids)
    assert broken == []


def test_tc65_demo_has_principle_revision() -> None:
    """TC-6.5: at least one principle shows validated → revised history."""
    repo = Repository.load(load_config(DEMO))
    revised = [e for e in repo.by_type("principle") if e.metadata.get("status") == "revised"]
    assert len(revised) >= 1
    body = revised[0].body
    assert "Revision History" in body
    assert "validated" in body
    assert "revised" in body.lower()


def test_demo_contains_required_counts() -> None:
    repo = Repository.load(load_config(DEMO))
    assert len(repo.by_type("value")) >= 3
    assert len(repo.by_type("model")) >= 2
    assert len(repo.by_type("principle")) >= 5
    assert len(repo.by_type("decision")) >= 2
    assert len(repo.by_type("experiment")) >= 1
    assert len(repo.by_type("review")) >= 2


def test_demo_has_prediction_vs_actual_review() -> None:
    repo = Repository.load(load_config(DEMO))
    decision_reviews = [
        e for e in repo.by_type("review")
        if e.metadata.get("review_type") == "decision"
    ]
    assert len(decision_reviews) >= 1
    assert "# Actual Outcome" in decision_reviews[0].body
    assert "# Difference" in decision_reviews[0].body


def test_demo_is_fictional() -> None:
    """Demo must not contain real personal data markers."""
    config = load_config(DEMO)
    repo = Repository.load(config)
    all_text = "\n".join(e.body for e in repo.all_entities).lower()
    for marker in ("alex@", "138", "secret", "password", "-----begin"):
        assert marker not in all_text, f"demo leaks marker {marker!r}"


def test_skills_examples_exist() -> None:
    for name in SKILL_NAMES:
        examples = SKILLS / name / "examples"
        assert (examples / "input-01.md").is_file()
        assert (examples / "output-01.md").is_file()