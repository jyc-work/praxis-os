"""Level 3 validation: semantic requirements per entity type.

Markdown sections are parsed from the body; an "empty" section is one whose
content is blank or only placeholder text (e.g. "…", "（待填写）", "TBD").

Checks (per Implementation Plan §4.6):

    principle   → Statement, Counter Evidence, Boundary, Action Rule
    decision    → Facts, Unknowns, Next Action, Final Judgment
    experiment  → Hypothesis, Metric
    review      → Actual Outcome, Lessons (when completed)
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from praxis.core.entity import Entity
from praxis.validation.issue import Severity, ValidationIssue

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

#: placeholder-ish lines that count as "empty" content
PLACEHOLDER_RE = re.compile(
    r"^\s*(\.{2,}|…|[-—~]*\s*$)",
    re.IGNORECASE,
)
PLACEHOLDER_WORDS = ("待填写", "未填写", "未完成", "todo", "tbd", "填写", "placeholder")

SECTION_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "principle": ("Statement", "Counter Evidence", "Boundary", "Action Rule"),
    "decision": ("Facts", "Unknowns", "Next Action", "Final Judgment"),
    "experiment": ("Hypothesis", "Metric"),
    "review": ("Actual Outcome", "Lessons"),
}


@dataclass
class _Section:
    name: str
    content: str


def extract_sections(body: str) -> dict[str, str]:
    """Map '## Heading' → trimmed content until the next heading."""
    lines = body.splitlines()
    sections: dict[str, str] = {}
    current: _Section | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal current, buffer
        if current is not None:
            sections[current.name] = "\n".join(buffer).strip()
        current = None
        buffer = []

    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            flush()
            current = _Section(name=match.group(2).strip(), content="")
        elif current is not None:
            buffer.append(line)
    flush()
    return sections


def section_is_effectively_empty(content: str) -> bool:
    if not content or not content.strip():
        return True
    lines = [ln for ln in content.splitlines() if ln.strip()]
    if not lines:
        return True
    substantive = [
        ln
        for ln in lines
        if not PLACEHOLDER_RE.match(ln)
        and not any(word in ln for word in PLACEHOLDER_WORDS)
    ]
    return not substantive


#: sections that can be skipped when their config toggle is off
OPTION_TOGGLE_SECTIONS: dict[str, str] = {
    "require_counter_evidence": "Counter Evidence",
    "require_principle_boundary": "Boundary",
    "require_decision_next_action": "Next Action",
}


def _option_enabled(options: dict | None, key: str) -> bool:
    if not options:
        return True
    return bool(options.get(key, True))


def validate_semantic(entity: Entity, options: dict | None = None) -> list[ValidationIssue]:
    """Run Level-3 semantic checks on one entity.

    ``options`` maps praxis.yaml ``validation.*`` flags to booleans; a section
    whose toggle is disabled is not checked.
    """
    issues: list[ValidationIssue] = []
    sections = extract_sections(entity.body)

    if entity.type not in SECTION_REQUIREMENTS:
        return issues

    for section in SECTION_REQUIREMENTS[entity.type]:
        # honor config toggles (e.g. require_counter_evidence)
        if _section_toggled_off(section, options):
            continue

        content = sections.get(section)
        if content is None:
            issues.append(_issue(entity, section, "MISSING", "section not found"))
            continue
        if section_is_effectively_empty(content):
            severity = _empty_severity(entity, section)
            issues.append(
                _issue(
                    entity,
                    section,
                    "EMPTY",
                    "section content is empty or placeholder-only",
                    severity=severity,
                )
            )

    return issues


def _section_toggled_off(section: str, options: dict | None) -> bool:
    for option_key, option_section in OPTION_TOGGLE_SECTIONS.items():
        if option_section == section and not _option_enabled(options, option_key):
            return True
    return False


def _empty_severity(entity: Entity, section: str) -> Severity:
    """Severity for an empty required section, depending on entity state."""
    if entity.type == "review" and _review_not_completed(entity):
        return Severity.INFO
    # a considering decision has not produced a Final Judgment yet — that is
    # expected, not a violation (but for decided/executing/reviewed it is)
    if (
        entity.type == "decision"
        and section == "Final Judgment"
        and entity.metadata.get("status") == "considering"
    ):
        return Severity.INFO
    return Severity.WARNING


def _review_not_completed(entity: Entity) -> bool:
    return entity.metadata.get("status") not in ("completed",)


def _issue(
    entity: Entity,
    section: str,
    kind: str,
    message: str,
    severity: Severity = Severity.WARNING,
) -> ValidationIssue:
    code = f"{entity.type.upper().replace('-', '_')}_{section.upper().replace(' ', '_')}_{kind}"
    return ValidationIssue(
        severity=severity,
        code=code,
        message=f"principle/decision section {section!r}: {message}",
        path=entity.path,
        entity_id=entity.id,
        section=section,
    )