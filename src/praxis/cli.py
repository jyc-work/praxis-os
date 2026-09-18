"""CLI entry point for PraxisOS.

Commands (v0.1):
    validate   full repository validation
    search     metadata + full-text search
    new        create a new entity from a template
    doctor     repository health report
"""

from __future__ import annotations

import argparse
import sys


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="praxis",
        description="PraxisOS — personal philosophy & decision operating system.",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s 0.1.0"
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    validate_p = sub.add_parser("validate", help="validate the whole repository")
    validate_p.add_argument(
        "--root", default=None, help="repository root (default: nearest praxis.yaml)"
    )

    search_p = sub.add_parser("search", help="search metadata and markdown bodies")
    search_p.add_argument("query", nargs="?", default=None, help="full-text query")
    search_p.add_argument("--root", default=None)
    search_p.add_argument("--type", default=None, help="entity type filter")
    search_p.add_argument("--status", default=None, help="status filter")
    search_p.add_argument("--domain", default=None, help="domain filter")
    search_p.add_argument("--related", default=None, help="related entity ID")

    new_p = sub.add_parser("new", help="create a new entity from a template")
    new_p.add_argument(
        "entity_type",
        choices=["value", "model", "principle", "decision", "experiment", "review"],
    )
    new_p.add_argument("--root", default=None)
    new_p.add_argument("--title", default="Untitled", help="entity title")
    new_p.add_argument("--domain", default=None, help="domain (e.g. career, life)")
    new_p.add_argument(
        "--type", dest="review_type", default=None,
        help="review type: weekly/monthly/quarterly/annual/decision",
    )
    new_p.add_argument(
        "--model-type", default=None,
        help="model type: thinker/philosophy/mental-model/world-model",
    )

    doctor_p = sub.add_parser("doctor", help="repository health report")
    doctor_p.add_argument("--root", default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0

    # Command implementations are imported lazily so `praxis --help` works
    # even if optional pieces are missing.
    if args.command == "validate":
        from praxis.commands.validate import run as run_validate

        return run_validate(args)
    if args.command == "search":
        from praxis.commands.search import run as run_search

        return run_search(args)
    if args.command == "new":
        from praxis.commands.new import run as run_new

        return run_new(args)
    if args.command == "doctor":
        from praxis.commands.doctor import run as run_doctor

        return run_doctor(args)
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())