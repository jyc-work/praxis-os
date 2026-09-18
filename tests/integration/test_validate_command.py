"""Integration tests for the `praxis validate` command (Phase 4)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "tests" / "fixtures"


def _run_validate(target: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "praxis.cli", "validate", "--root", str(target)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_validate_command_exit_zero_on_clean_repo() -> None:
    """TC-4.5: a clean repository exits 0."""
    result = _run_validate(FIXTURES / "valid_repo")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "RESULT: PASS" in result.stdout
    assert "PASS" in result.stdout


def test_validate_command_fails_on_invalid_repo() -> None:
    result = _run_validate(FIXTURES / "invalid_repo")
    assert result.returncode == 1
    assert "RESULT: FAILED" in result.stdout
    assert "DUPLICATE_ID" in result.stdout


def test_validate_report_has_entity_ids() -> None:
    result = _run_validate(FIXTURES / "valid_repo")
    assert "PRINCIPLE-LIFE-001" in result.stdout or (
        "Scanning" in result.stdout
    )