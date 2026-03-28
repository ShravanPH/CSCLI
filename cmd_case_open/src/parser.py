from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cmd-case-open",
        description="CLI for terminal case opening experiments",
    )

    subparsers = parser.add_subparsers(dest="command")

    case_open = subparsers.add_parser("case-open",help=argparse.SUPPRESS)
    case_open.add_argument("--text", default="", help="Input text to drive case selection")

    subparsers.add_parser("inventory-stats",help=argparse.SUPPRESS)

    return parser
