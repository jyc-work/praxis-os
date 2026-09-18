"""Validation issue model.

Severity ladder (Technical Design §37):

    FATAL   → duplicate ID, invalid YAML
    ERROR   → broken relation, invalid status
    WARNING → missing counter evidence, overdue review
    INFO    → principle not tested for 365 days
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class ValidationIssue:
    severity: Severity
    code: str
    message: str
    path: Path | None = None
    entity_id: str | None = None
    section: str | None = None

    def format(self) -> str:
        prefix = f"[{self.severity}] {self.code}"
        location = self.entity_id or (str(self.path) if self.path else "-")
        return f"{prefix} {location}: {self.message}"


def is_failure(severity: Severity) -> bool:
    """Whether a single issue forces validation failure (exit code 1)."""
    return severity in (Severity.ERROR, Severity.FATAL)