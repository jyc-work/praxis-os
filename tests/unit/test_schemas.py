"""Phase 2 acceptance tests: JSON schemas and template compatibility (TC-2.x)."""

from __future__ import annotations

import datetime
import json
from pathlib import Path

import frontmatter
import jsonschema
import pytest
import yaml

from praxis.validation.schema import validate_entity_schema

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = REPO_ROOT / "schemas"
TEMPLATES = REPO_ROOT / "templates"

ENTITY_TYPES = ["value", "model", "principle", "decision", "experiment", "review"]


def normalize_metadata(data: dict) -> dict:
    """Recursively convert YAML date objects to ISO strings (parser contract).

    YAML parses ``2026-09-17`` as datetime.date; the schemas require date
    strings, so every frontmatter loader normalises dates before validation.
    """
    out: dict = {}
    for key, value in data.items():
        if isinstance(value, datetime.datetime):
            out[key] = value.date().isoformat()
        elif isinstance(value, datetime.date):
            out[key] = value.isoformat()
        elif isinstance(value, dict):
            out[key] = normalize_metadata(value)
        elif isinstance(value, list):
            out[key] = [
                normalize_metadata(v) if isinstance(v, dict) else
                v.date().isoformat() if isinstance(v, datetime.datetime) else
                v.isoformat() if isinstance(v, datetime.date) else v
                for v in value
            ]
        else:
            out[key] = value
    return out


def template_metadata(template_file: str) -> dict:
    doc = frontmatter.load(TEMPLATES / template_file)
    return normalize_metadata(dict(doc.metadata))


def load_schema(entity_type: str) -> dict:
    path = SCHEMAS / f"{entity_type}.schema.json"
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(scope="module")
def schemas() -> dict[str, dict]:
    return {t: load_schema(t) for t in ENTITY_TYPES}


def minimum_valid(entity_type: str) -> dict:
    today = "2026-09-17"
    base: dict = {"type": entity_type, "created_at": today, "updated_at": today}
    if entity_type == "value":
        base.update(
            id="VALUE-LIFE-001", name="Autonomy", status="active",
            priority="high", domains=["life"], confidence="medium",
        )
    elif entity_type == "model":
        base.update(
            id="MODEL-STOICISM-001", model_type="philosophy",
            name="Stoicism", status="studying", domains=["emotion"],
        )
    elif entity_type == "principle":
        base.update(
            id="PRINCIPLE-CAREER-001", title="Test principle",
            status="candidate", confidence="low", domains=["career"],
        )
    elif entity_type == "decision":
        base.update(
            id="DECISION-CAREER-001", title="Test decision",
            status="considering", domain="career", confidence=60,
        )
    elif entity_type == "experiment":
        base.update(
            id="EXPERIMENT-CAREER-001", title="Test experiment",
            status="planned", hypothesis="Test hypothesis",
        )
    elif entity_type == "review":
        base.update(
            id="REVIEW-WEEKLY-001", review_type="weekly", status="completed",
        )
    return base


# -- TC-2.1 / TC-2.5: valid entities pass -----------------------------
@pytest.mark.parametrize("entity_type", ENTITY_TYPES)
def test_valid_entity_passes(schemas, entity_type: str) -> None:
    jsonschema.validate(minimum_valid(entity_type), schemas[entity_type])


def test_valid_decision_full_template_passes(schemas) -> None:
    """TC-2.5: a complete decision template document passes schema."""
    data = template_metadata("decision.md")
    data["id"] = "DECISION-CAREER-001"
    data["title"] = "Test decision"
    data["status"] = "considering"
    jsonschema.validate(data, schemas["decision"])


# -- TC-2.2: invalid principle status fails ---------------------------
def test_invalid_principle_status_fails(schemas) -> None:
    bad = minimum_valid("principle")
    bad["status"] = "approved"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, schemas["principle"])


# -- TC-2.3: missing ID fails -----------------------------------------
@pytest.mark.parametrize("entity_type", ENTITY_TYPES)
def test_missing_id_fails(schemas, entity_type: str) -> None:
    bad = minimum_valid(entity_type)
    del bad["id"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, schemas[entity_type])


# -- TC-2.4: invalid model type fails ---------------------------------
def test_invalid_model_type_fails(schemas) -> None:
    bad = minimum_valid("model")
    bad["model_type"] = "ideology-engine"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, schemas["model"])


# -- wrong ID prefix fails --------------------------------------------
@pytest.mark.parametrize("entity_type", ENTITY_TYPES)
def test_wrong_id_prefix_fails(schemas, entity_type: str) -> None:
    bad = minimum_valid(entity_type)
    bad["id"] = "WRONG-PREFIX-001"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, schemas[entity_type])


# -- TC-2.10: templates are schema-compatible --------------------------
@pytest.mark.parametrize(
    ("template_file", "entity_type"),
    [
        ("value.md", "value"),
        ("thinker.md", "model"),
        ("principle.md", "principle"),
        ("decision.md", "decision"),
        ("experiment.md", "experiment"),
        ("weekly-review.md", "review"),
        ("quarterly-review.md", "review"),
    ],
)
def test_template_schema_compatible(schemas, template_file: str, entity_type: str) -> None:
    data = template_metadata(template_file)
    # ensure type-specific enum/id are template-valid; template ids use valid
    # prefixes already (e.g. REVIEW-WEEKLY-001).
    jsonschema.validate(data, schemas[entity_type])


# -- schema documents are valid JSON and carry required sections ---------
def test_schemas_are_valid_json() -> None:
    for entity_type in ENTITY_TYPES:
        with (SCHEMAS / f"{entity_type}.schema.json").open(encoding="utf-8") as fh:
            parsed = json.load(fh)
        assert parsed["$schema"].startswith("http://json-schema.org/")
        assert "required" in parsed


def test_data_model_doc_mentions_all_six_entities() -> None:
    doc = (REPO_ROOT / "docs" / "data-model.md").read_text(encoding="utf-8")
    for entity_type in ENTITY_TYPES:
        assert entity_type in doc


def test_validate_entity_schema_accepts_explicit_schema_dir() -> None:
    """Schema resolution prefers a repository's schemas/ directory and never
    hard-requires the source tree (wheel-install safety)."""
    from praxis.core.parser import parse_file

    entity = parse_file(SCHEMAS.parent / "tests" / "fixtures" / "valid_repo" / "values" / "VALUE-LIFE-001-autonomy.md")
    # explicit real dir → clean
    issues_ok = validate_entity_schema(entity, schema_dir=SCHEMAS)
    assert issues_ok == []
    # missing/empty dir → falls back gracefully, never a crash
    issues_fallback = validate_entity_schema(
        entity, schema_dir=Path(__file__).parent / "_nonexistent"
    )
    assert all(i.code != "UNKNOWN_SCHEMA" for i in issues_fallback)