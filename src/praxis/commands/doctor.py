"""praxis doctor — repository health report.

Checks (Implementation Plan §5.6):

    orphan principles
    decisions without review dates
    overdue decision reviews
    unused values
    principles never tested
    retired principles still referenced
    stale constitution
"""

from __future__ import annotations

import argparse
import datetime
import sys
from dataclasses import dataclass
from pathlib import Path

from praxis.config import find_repo_root, load_config
from praxis.core.index import Repository
from praxis.core.relations import referenced_ids, resolve_relations

STALE_CONSTITUTION_DAYS = 90
NEVER_TESTED_DAYS = 365


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str  # INFO | WARNING
    message: str
    entity_id: str | None = None

    def format(self) -> str:
        location = self.entity_id or "-"
        return f"  [{self.severity}] {self.code} {location}: {self.message}"


def _today() -> datetime.date:
    return datetime.date.today()


def _parse_date(value) -> datetime.date | None:
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


def _relations_of(entity) -> set[str]:
    from praxis.core.relations import collect_relations

    return {r.target_id for r in collect_relations(entity)}


def diagnose(repo: Repository) -> list[Finding]:
    findings: list[Finding] = []
    today = _today()

    principles = {e.id: e for e in repo.by_type("principle")}
    values = {e.id: e for e in repo.by_type("value")}
    decisions = repo.by_type("decision")
    references = referenced_ids(repo.all_entities)

    # -- orphan principles (no relations at all) -----------------------
    for entity in repo.by_type("principle"):
        if not _relations_of(entity):
            findings.append(
                Finding(
                    "ORPHAN_PRINCIPLE",
                    "WARNING",
                    "principle has no relations (values/models/evidence)",
                    entity.id,
                )
            )

    # -- decisions without review dates --------------------------------
    for entity in decisions:
        if not entity.metadata.get("review_dates"):
            findings.append(
                Finding(
                    "DECISION_WITHOUT_REVIEW",
                    "WARNING",
                    "no review_dates configured; predictions cannot be checked",
                    entity.id,
                )
            )
        else:
            dates = [_parse_date(d) for d in entity.metadata.get("review_dates") or []]
            overdue = [d for d in dates if d and d <= today]
            if overdue and entity.metadata.get("status") != "reviewed":
                findings.append(
                    Finding(
                        "DECISION_REVIEW_OVERDUE",
                        "WARNING",
                        f"review date {min(overdue).isoformat()} has passed and "
                        f"status is still {entity.metadata.get('status')!r}",
                        entity.id,
                    )
                )

    # -- unused values -------------------------------------------------
    for value_id in values:
        if value_id not in references:
            findings.append(
                Finding(
                    "UNUSED_VALUE",
                    "INFO",
                    "value is not referenced by any principle or decision",
                    value_id,
                )
            )

    # -- principles never tested ---------------------------------------
    for entity in repo.by_type("principle"):
        status = str(entity.metadata.get("status", ""))
        last_tested = _parse_date(entity.metadata.get("last_tested"))
        if status in ("validated", "core") and last_tested is None:
            findings.append(
                Finding(
                    "PRINCIPLE_NEVER_TESTED",
                    "WARNING",
                    f"status is {status!r} but last_tested is empty",
                    entity.id,
                )
            )
        elif last_tested and (today - last_tested).days > NEVER_TESTED_DAYS:
            findings.append(
                Finding(
                    "PRINCIPLE_STALE",
                    "INFO",
                    f"not tested for {(today - last_tested).days} days",
                    entity.id,
                )
            )

    # -- retired principles still referenced ---------------------------
    for entity in repo.by_type("principle"):
        if entity.metadata.get("status") == "retired" and entity.id in references:
            findings.append(
                Finding(
                    "RETIRED_PRINCIPLE_REFERENCED",
                    "WARNING",
                    "retired principle is still referenced by other entities",
                    entity.id,
                )
            )

    # -- broken relations (also a validate concern) --------------------
    for broken in resolve_relations(repo.all_entities, repo.ids):
        findings.append(
            Finding(
                "BROKEN_RELATION",
                "WARNING",
                f"{broken.field} references missing {broken.target_id}",
                broken.source_id,
            )
        )

    # -- stale constitution --------------------------------------------
    constitution_dir = repo.config.root / repo.config.paths.get("constitution", "constitution")
    constitution = constitution_dir / "constitution.md"
    if not constitution.is_file():
        findings.append(
            Finding("NO_CONSTITUTION", "INFO", f"{constitution} not found")
        )
    else:
        import frontmatter

        from praxis.core.parser import normalise_metadata

        try:
            post = frontmatter.load(constitution)
            metadata = normalise_metadata(dict(post.metadata or {}))
            last_reviewed = _parse_date(metadata.get("last_reviewed"))
            if last_reviewed is None:
                findings.append(
                    Finding(
                        "CONSTITUTION_NOT_REVIEWED",
                        "INFO",
                        "no last_reviewed date recorded",
                    )
                )
            elif (today - last_reviewed).days > STALE_CONSTITUTION_DAYS:
                findings.append(
                    Finding(
                        "STALE_CONSTITUTION",
                        "WARNING",
                        f"last reviewed {(today - last_reviewed).days} days ago",
                    )
                )
        except Exception as exc:  # never crash the health report
            findings.append(
                Finding("CONSTITUTION_UNREADABLE", "INFO", str(exc))
            )

    return findings


def render(findings: list[Finding], repo: Repository) -> str:
    lines = ["PraxisOS health report", ""]
    checked = len(repo.all_entities)
    lines.append(f"Entities: {checked}")
    lines.append(f"Findings: {len(findings)}")
    lines.append("")
    if not findings:
        lines.append("  no findings — repository looks healthy")
        return "\n".join(lines)
    for finding in findings:
        lines.append(finding.format())
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    try:
        root = Path(args.root).resolve() if getattr(args, "root", None) else find_repo_root()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    config = load_config(root)
    repo = Repository.load(config)
    findings = diagnose(repo)
    print(render(findings, repo))
    return 0