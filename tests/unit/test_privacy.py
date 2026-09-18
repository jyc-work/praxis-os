"""Privacy guard tests (Phase 4)."""

from __future__ import annotations

from pathlib import Path

from praxis.validation.issue import Severity
from praxis.validation.privacy import (
    CREDENTIAL_FILENAME_PATTERNS,
    scan_file,
    scan_text,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_api_key_detected() -> None:
    """TC-4.4: fake API keys in fixtures are ERROR POSSIBLE_SECRET."""
    issues = scan_text("token = sk-abcdefghijklmnopqrstuvwxyz123456")
    assert any(i.code == "POSSIBLE_SECRET" for i in issues)
    assert all(i.severity == Severity.ERROR for i in issues)


def test_aws_key_detected() -> None:
    issues = scan_text("AKIAIOSFODNN7EXAMPLE")
    assert any(i.code == "POSSIBLE_SECRET" for i in issues)


def test_private_key_block_detected() -> None:
    issues = scan_text(
        "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA\n-----END RSA PRIVATE KEY-----"
    )
    assert len(issues) >= 1
    assert any("private key" in i.message.lower() for i in issues)


def test_email_detected() -> None:
    issues = scan_text("contact me at alice.personal.2026@protonmail.com soon")
    assert any(i.code == "POSSIBLE_SECRET" for i in issues)


def test_phone_detected() -> None:
    issues = scan_text("call me at 13812345678")
    assert any(i.code == "POSSIBLE_SECRET" for i in issues)


def test_password_assignment_detected() -> None:
    issues = scan_text("password = hunter2secret")
    assert any(i.code == "POSSIBLE_SECRET" for i in issues)


def test_clean_text_no_false_positive() -> None:
    body = "今天讨论了自由与依赖的关系。PRINCIPLE-CAREER-001 已更新。"
    assert scan_text(body) == []


def test_example_email_allowed() -> None:
    assert scan_text("someone@example.com") == []


def test_credential_filename_detected(tmp_path: Path) -> None:
    for name in ("id_rsa", "credentials.json", "server.pem", ".env"):
        issues = scan_file(tmp_path / name)
        assert any(i.code == "POSSIBLE_CREDENTIAL_FILE" for i in issues), name


def test_normal_filename_ok(tmp_path: Path) -> None:
    issues = scan_file(tmp_path / "principle.md")
    assert issues == []


def test_patterns_cover_expected_extensions() -> None:
    for name in ("key.pem", "cert.key", "id_ed25519", "credentials.yaml", ".env.prod"):
        assert any(p.match(name) for p in CREDENTIAL_FILENAME_PATTERNS), name