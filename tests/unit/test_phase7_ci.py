"""Phase 7 tests: CI workflow sanity, privacy self-scan, release files."""

from __future__ import annotations

from pathlib import Path

import yaml

from praxis import validate_repo_self
from praxis.validation.issue import Severity

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_workflow_files_exist_and_parse() -> None:
    workflows = REPO_ROOT / ".github" / "workflows"
    for name in ("test.yml", "validate.yml"):
        path = workflows / name
        assert path.is_file(), f"missing {name}"
        with path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        assert "jobs" in data
        # GitHub Actions uses `on:` which YAML 1.1 parses as boolean True
        assert ("on" in data) or (True in data)


def test_pre_commit_config_parses() -> None:
    path = REPO_ROOT / ".pre-commit-config.yaml"
    assert path.is_file()
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert isinstance(data.get("repos"), list)


def test_release_files_present() -> None:
    assert (REPO_ROOT / "CHANGELOG.md").is_file()
    assert (REPO_ROOT / "RELEASE_CHECKLIST.md").is_file()


def test_privacy_self_scan_passes() -> None:
    """The repository itself must not trip the privacy scanner."""
    files = list(validate_repo_self._iter_files(REPO_ROOT))
    assert files, "self-scan found no files to check"
    issues = []
    for path in files:
        issues.extend(validate_repo_self.scan_file(path))  # type: ignore[attr-defined]
    severe = [i for i in issues if i.severity in (Severity.ERROR, Severity.FATAL)]
    assert severe == [], [i.format() for i in severe]


def test_cli_entrypoints_remain() -> None:
    import tomllib

    with (REPO_ROOT / "pyproject.toml").open("rb") as fh:
        data = tomllib.load(fh)
    scripts = data["project"]["scripts"]
    assert scripts["praxis"] == "praxis.cli:main"