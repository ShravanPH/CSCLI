from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cmd-case-open",
        description="CLI for terminal case opening experiments",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    case_open = subparsers.add_parser("case-open", help="Open a case from input text")
    case_open.add_argument("--text", default="", help="Input text to drive case selection")
    case_open.add_argument("--no-anim", action="store_true", help="Disable terminal animation")

    subparsers.add_parser("inventory-stats", help="Show unboxed inventory and rarity statistics")
    return parser
