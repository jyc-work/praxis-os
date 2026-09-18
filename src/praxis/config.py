"""Configuration loading for PraxisOS repositories.

Reads ``praxis.yaml`` from the repository root. All directory paths are
relative to the repository root (the directory containing ``praxis.yaml``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {
    "version": 1,
    "paths": {
        "constitution": "constitution",
        "values": "values",
        "models": "models",
        "principles": "principles",
        "decisions": "decisions",
        "experiments": "experiments",
        "reviews": "reviews",
    },
    "privacy": {
        "ignored": ["private/**", "data/private/**", "journals/private/**"],
    },
    "validation": {
        "require_counter_evidence": True,
        "require_principle_boundary": True,
        "require_decision_next_action": True,
    },
}


@dataclass
class PraxisConfig:
    """Resolved configuration for one repository."""

    root: Path
    version: int = 1
    paths: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_CONFIG["paths"]))
    privacy_ignored: list[str] = field(
        default_factory=lambda: list(DEFAULT_CONFIG["privacy"]["ignored"])
    )
    validation: dict[str, bool] = field(
        default_factory=lambda: dict(DEFAULT_CONFIG["validation"])
    )

    # -- paths ---------------------------------------------------------
    def dir_for(self, entity_type: str) -> Path:
        rel = self.paths.get(entity_type)
        if rel is None:
            raise KeyError(f"no path configured for entity type {entity_type!r}")
        return (self.root / rel).resolve()

    def entity_dirs(self) -> dict[str, Path]:
        """Directories the loader scans, keyed by entity type."""
        return {t: self.dir_for(t) for t in self._entity_types()}

    @staticmethod
    def _entity_types() -> list[str]:
        return ["values", "models", "principles", "decisions", "experiments", "reviews"]

    # -- helpers -------------------------------------------------------
    def option(self, key: str, default: bool = False) -> bool:
        return bool(self.validation.get(key, default))


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def find_repo_root(start: Path | None = None) -> Path:
    """Walk up from ``start`` (or CWD) to the directory containing praxis.yaml.

    Raises FileNotFoundError when no praxis.yaml is found.
    """
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "praxis.yaml").is_file():
            return candidate
    raise FileNotFoundError(
        "no praxis.yaml found in this directory or any parent; run praxis inside "
        "a PraxisOS repository"
    )


def load_config(root: Path | None = None) -> PraxisConfig:
    """Load and merge praxis.yaml with sane defaults."""
    root = (root or find_repo_root()).resolve()
    path = root / "praxis.yaml"
    raw: dict[str, Any] = {}
    if path.is_file():
        with path.open(encoding="utf-8") as fh:
            loaded = yaml.safe_load(fh) or {}
        if not isinstance(loaded, dict):
            raise ValueError(f"{path}: expected a YAML mapping at top level")
        raw = loaded

    merged = _deep_merge(DEFAULT_CONFIG, raw)
    paths = merged.get("paths") or {}
    privacy = merged.get("privacy") or {}
    validation = merged.get("validation") or {}

    return PraxisConfig(
        root=root,
        version=int(merged.get("version", 1)),
        paths={k: str(v) for k, v in paths.items()},
        privacy_ignored=[str(p) for p in privacy.get("ignored", [])],
        validation={k: bool(v) for k, v in validation.items()},
    )