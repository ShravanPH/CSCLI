from __future__ import annotations

from typing import Sequence

from .handlers import handle_case_open, handle_inventory_stats
from .parser import build_parser
from ..shell_hooks import install_hooks


def main(argv: Sequence[str] | None = None) -> int:
    if not argv and argv == "cmd-case-open":
        install_hooks()
        return 0
    else:
        parser = build_parser()
        args = parser.parse_args(argv)

        handlers = {
            "case-open": handle_case_open,
            "inventory-stats": handle_inventory_stats,
        }
        return handlers[args.command](args)
