"""Self-scan entry point for CI: scan the whole repository for secrets.

Run as ``python -m praxis.validate_repo_self [ROOT]``.

Scans every file under the repository root except VCS/metadata/venv
directories and the ``tests/`` tree (tests may intentionally construct
secret-looking fixtures). Exits 0 when nothing is found, 1 otherwise.
"""

from __future__ import annotations

import sys
from pathlib import Path

from praxis.validation.issue import Severity
from praxis.validation.privacy import scan_file

EXCLUDED_DIRS = {".git", ".venv", "node_modules", "private", "__pycache__", ".pytest_cache", ".idea", ".vscode"}


def _iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts):
            continue
        if path.relative_to(root).parts[0] == "tests":
            continue
        yield path


def main(argv: list[str] | None = None) -> int:
    args = list(argv) if argv is not None else sys.argv[1:]
    root = Path(args[0]).resolve() if args else Path.cwd().resolve()
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        return 1

    issues = []
    for path in _iter_files(root):
        issues.extend(scan_file(path))

    severe = [i for i in issues if i.severity in (Severity.ERROR, Severity.FATAL)]
    print(f"Privacy self-scan: scanned {root}")
    if not severe:
        print("  PASS — no secret-like patterns found")
        return 0
    for issue in severe:
        print(f"  {issue.format()}")
    print(f"  FAIL — {len(severe)} finding(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())