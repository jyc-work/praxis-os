"""Phase 1 acceptance tests: package import, CLI entry, config load, .gitignore."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_package_import() -> None:
    import praxis  # noqa: F401

    assert praxis.__version__.startswith("0.1.0")


def test_cli_entry_help() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "praxis.cli", "--help"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0
    assert "validate" in result.stdout
    assert "search" in result.stdout
    assert "new" in result.stdout
    assert "doctor" in result.stdout


def test_config_load_version_is_1() -> None:
    from praxis.config import load_config

    config = load_config(REPO_ROOT)
    assert config.version == 1


def test_config_paths() -> None:
    from praxis.config import load_config

    config = load_config(REPO_ROOT)
    for entity in ["values", "models", "principles", "decisions", "experiments", "reviews"]:
        assert (config.root / entity).is_dir(), f"missing {entity}/"


def test_private_ignored_in_gitignore() -> None:
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "/private/**" in gitignore
    assert "/data/private/**" in gitignore
    assert "/journals/private/**" in gitignore


def test_config_reads_validation_flags() -> None:
    from praxis.config import load_config

    config = load_config(REPO_ROOT)
    assert config.option("require_counter_evidence") is True
    assert config.option("require_principle_boundary") is True
    assert config.option("require_decision_next_action") is True