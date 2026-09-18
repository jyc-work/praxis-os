"""Privacy Guard — heuristic secret detection (never a classifier).

Detected (all → ERROR POSSIBLE_SECRET / POSSIBLE_CREDENTIAL_FILE):

    API keys      sk-…, AIza…, AKIA…
    private keys  -----BEGIN … PRIVATE KEY-----
    tokens        ghp_…, xoxb-…, gho_…, glpat-…
    passwords     password = …, passwd: …, api_key = …
    emails        name@example.com
    phones        +86 138…, 13812345678
    filenames     *.pem, *.key, id_rsa, credentials.*, .env

The scan is deliberately shallow: it is a tripwire that fails CI, not a
classification system (no OCR, no ML, no full PII taxonomy in v0.1).
"""

from __future__ import annotations

import re
from pathlib import Path

from praxis.validation.issue import Severity, ValidationIssue

SECRET_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    (
        "API_KEY",
        re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"),
        "possible API key (sk-…)",
    ),
    (
        "API_KEY",
        re.compile(r"\bAIza[0-9A-Za-z_\-]{30,}\b"),
        "possible Google API key (AIza…)",
    ),
    (
        "API_KEY",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "possible AWS access key ID",
    ),
    (
        "PRIVATE_KEY",
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        "private key block",
    ),
    (
        "TOKEN",
        re.compile(r"\b(?:ghp|gho|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
        "possible GitHub token",
    ),
    (
        "TOKEN",
        re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
        "possible Slack token",
    ),
    (
        "TOKEN",
        re.compile(r"\bglpat-[A-Za-z0-9_\-]{20,}\b"),
        "possible GitLab token",
    ),
    (
        "PASSWORD",
        re.compile(
            r"(?i)\b(?:password|passwd|pwd|secret|api[_\-]?key|access[_\-]?token)\b"
            r"\s*[:=]\s*[\"']?([^\s\"']{8,})[\"']?"
        ),
        "password-like assignment",
    ),
    (
        "EMAIL",
        re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
        "email address",
    ),
    (
        "PHONE",
        re.compile(r"(?<!\d)(?:\+?86[\s\-]?)?1[3-9]\d{9}(?!\d)"),
        "possible phone number",
    ),
]

CREDENTIAL_FILENAME_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r".*\.pem$", re.IGNORECASE),
    re.compile(r".*\.key$", re.IGNORECASE),
    re.compile(r"^id_(rsa|dsa|ecdsa|ed25519)$", re.IGNORECASE),
    re.compile(r"^credentials(\..*)?$", re.IGNORECASE),
    re.compile(r"^\.env(\..*)?$", re.IGNORECASE),
    re.compile(r".*\.secret\..*$", re.IGNORECASE),
]

#: allow obvious documentation placeholders through untouched
ALLOWLIST_MARKERS = ("example.com", "your-key-here", "xxxxx", "<redacted>")


def scan_text(text: str, path: Path | None = None, entity_id: str | None = None) -> list[ValidationIssue]:
    """Scan a blob of text for secret tripwires."""
    issues: list[ValidationIssue] = []
    for code, pattern, description in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            snippet = match.group(0)
            if any(marker in snippet.lower() for marker in ALLOWLIST_MARKERS):
                continue
            if code == "EMAIL" and snippet.lower().endswith("example.com"):
                continue
            issues.append(
                ValidationIssue(
                    Severity.ERROR,
                    "POSSIBLE_SECRET",
                    f"{description} detected ({_mask(snippet)})",
                    path=path,
                    entity_id=entity_id,
                )
            )
    return issues


def scan_file(path: Path, entity_id: str | None = None) -> list[ValidationIssue]:
    """Scan one file's contents and its filename."""
    issues: list[ValidationIssue] = []
    for pattern in CREDENTIAL_FILENAME_PATTERNS:
        if pattern.match(path.name):
            issues.append(
                ValidationIssue(
                    Severity.ERROR,
                    "POSSIBLE_CREDENTIAL_FILE",
                    f"credential-looking filename {path.name!r}",
                    path=path,
                    entity_id=entity_id,
                )
            )
            break
    if not path.is_file():
        return issues
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        issues.append(
            ValidationIssue(
                Severity.WARNING, "UNREADABLE", str(exc), path=path, entity_id=entity_id
            )
        )
        return issues
    issues.extend(scan_text(text, path=path, entity_id=entity_id))
    return issues


def scan_paths(root: Path, paths: list[Path] | None = None) -> list[ValidationIssue]:
    """Scan a repository subtree for secrets."""
    issues: list[ValidationIssue] = []
    candidates = paths if paths is not None else [p for p in root.rglob("*") if p.is_file()]
    for path in candidates:
        if not path.is_file():
            continue
        issues.extend(scan_file(path))
    return issues


def _mask(snippet: str) -> str:
    """Never echo a suspected secret in full."""
    clean = snippet.strip()
    if len(clean) <= 8:
        return "*" * len(clean)
    return f"{clean[:4]}…{clean[-2:]}"