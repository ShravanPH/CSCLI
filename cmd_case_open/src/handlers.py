from __future__ import annotations

import argparse

from ..core.rendering import print_case_open_fallback, render_display_block, run_random_tte
from ..domain.case_catalog import build_case_open_preview
from ..inventory import print_inventory_stats, write_inventory_entry


def handle_case_open(args: argparse.Namespace) -> int:
    preview = build_case_open_preview(args.text)
    name = preview.generated_output["name"]
    rarity = preview.generated_output["rarity"]
    ascii_art = preview.generated_output.get("ascii", "")

    write_inventory_entry(name=name, rarity=rarity)

    display_block = render_display_block(name=name, rarity=rarity, ascii_art=ascii_art)
    run_random_tte(display_block)
    return 0


def handle_inventory_stats(_: argparse.Namespace) -> int:
    return print_inventory_stats()
