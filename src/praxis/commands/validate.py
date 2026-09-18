"""praxis validate — full repository validation.

    praxis validate [--root PATH]

Runs: schema (L1) → repository integrity (L2) → semantic (L3) → privacy.
Exit code: 0 when there are no ERROR/FATAL issues; 1 otherwise.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from praxis.config import find_repo_root, load_config
from praxis.core.index import Repository
from praxis.validation.issue import Severity, ValidationIssue
from praxis.validation.privacy import scan_file
from praxis.validation.repository import validate_repository
from praxis.validation.schema import validate_entity_schema
from praxis.validation.semantic import validate_semantic

CATEGORY_ORDER = [
    ("Schema", "schema"),
    ("IDs", "ids"),
    ("Relations", "relations"),
    ("Semantic", "semantic"),
    ("Privacy", "privacy"),
]


def _classify(issues: list[ValidationIssue]) -> dict[str, list[ValidationIssue]]:
    buckets: dict[str, list[ValidationIssue]] = {
        "schema": [], "ids": [], "relations": [], "semantic": [], "privacy": []
    }
    for issue in issues:
        code = issue.code
        if code == "SCHEMA" or code == "UNKNOWN_SCHEMA":
            buckets["schema"].append(issue)
        elif code in {"DUPLICATE_ID", "PARSE", "ID_PREFIX", "UNKNOWN_TYPE", "WRONG_DIRECTORY"}:
            buckets["ids"].append(issue)
        elif code in {"BROKEN_RELATION", "MISSING_REVIEW_TARGET"}:
            buckets["relations"].append(issue)
        elif code == "POSSIBLE_SECRET" or code.startswith("POSSIBLE_"):
            buckets["privacy"].append(issue)
        elif code.startswith(("VALUE_", "MODEL_", "PRINCIPLE_", "DECISION_",
                              "EXPERIMENT_", "REVIEW_")):
            buckets["semantic"].append(issue)
        else:
            buckets["schema"].append(issue)
    return buckets


def run_validation(root: Path) -> tuple[list[ValidationIssue], Repository]:
    """Run every validation level; returns (issues, repo)."""
    config = load_config(root)
    repo = Repository.load(config)
    issues: list[ValidationIssue] = []
    schema_dir = root / "schemas"

    for entity in repo.all_entities:
        issues.extend(validate_entity_schema(entity, schema_dir=schema_dir))
        issues.extend(validate_semantic(entity, options=config.validation))

    repo_issues = validate_repository(repo)
    issues.extend(repo_issues)

    for entity in repo.all_entities:
        issues.extend(scan_file(entity.path, entity_id=entity.id))

    return issues, repo


def render_report(
    issues: list[ValidationIssue],
    root: Path,
    repo: Repository,
) -> str:
    """Build the human-readable validation report."""
    buckets = _classify(issues)
    lines: list[str] = []

    total = len(repo.all_entities) + len(repo.parse_errors)
    lines.append(f"Scanning {total} entities in {root}…")
    lines.append("")

    for label, bucket in CATEGORY_ORDER:
        bucket_issues = buckets[bucket]
        failed = [i for i in bucket_issues if i.severity in (Severity.ERROR, Severity.FATAL)]
        warned = [i for i in bucket_issues if i.severity == Severity.WARNING]
        if failed:
            status = "FAIL"
        elif warned:
            status = "WARN"
        else:
            status = "PASS"
        lines.append(f"{label:<11} {status}")
        for issue in failed + warned:
            lines.append(f"  {issue.format()}")

    errors = [i for i in issues if i.severity in (Severity.ERROR, Severity.FATAL)]
    warnings = [i for i in issues if i.severity == Severity.WARNING]
    lines.append("")
    lines.append(f"Errors: {len(errors)}")
    lines.append(f"Warnings: {len(warnings)}")
    if errors:
        lines.append("")
        lines.append("RESULT: FAILED")
    else:
        lines.append("")
        lines.append("RESULT: PASS")
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    root_arg = getattr(args, "root", None)
    try:
        root = Path(root_arg).resolve() if root_arg else find_repo_root()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    try:
        issues, repo = run_validation(root)
    except Exception as exc:  # never crash with a raw traceback
        print(f"ERROR: validation aborted: {exc}", file=sys.stderr)
        return 1

    print(render_report(issues, root, repo))

    has_failure = any(
        i.severity in (Severity.ERROR, Severity.FATAL) for i in issues
    )
    return 1 if has_failure else 0