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
    sub.add_parser("validate", help="validate the whole repository")
    sub.add_parser("search", help="search metadata and markdown bodies")
    sub.add_parser("new", help="create a new entity from a template")
    sub.add_parser("doctor", help="repository health report")
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