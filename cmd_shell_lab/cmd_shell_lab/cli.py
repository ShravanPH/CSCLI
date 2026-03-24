from __future__ import annotations

import argparse
import json
import os
import time
from typing import Sequence

from .anim import play_drop_animation
from .examples import build_seed_preview, read_cli_input, shell_split

ANSI_RESET = "\x1b[0m" # To reset color
RARITY_TO_COLOR = {
    "mil-spec": "\x1b[34m",       # Blue
    "restricted": "\x1b[35m",     # Purple
    "classified": "\x1b[95m",     # Pink (bright magenta)
    "covert": "\x1b[31m",         # Red
    "extraordinary": "\x1b[33m",  # Gold-ish yellow
}


def colorize_rarity(rarity: str) -> str:
    if os.getenv("NO_COLOR") or not os.isatty(1):
        return rarity
    rarity_key = (rarity or "").split()[0].lower()
    color = RARITY_TO_COLOR.get(rarity_key, "")
    if not color:
        return rarity
    return f"{color}{rarity}{ANSI_RESET}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cmd-shell-lab",
        description="Example-only CLI boilerplate for terminal workflow experiments",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    seed_demo = subparsers.add_parser("seed-demo", help="Show deterministic seeding from input text")
    seed_demo.add_argument("--text", default="", help="Input text to hash into a seed")
    seed_demo.add_argument("--no-anim", action="store_true", help="Disable animation")

    input_demo = subparsers.add_parser("input-demo", help="Read text from --text or stdin")
    input_demo.add_argument("--text", default="", help="Optional explicit input")

    split_demo = subparsers.add_parser("split-demo", help="Split shell command text")
    split_demo.add_argument("--text", default="", help="Command text")


    scaffold = subparsers.add_parser("scaffold-feature", help="Placeholder command for future implementation")
    scaffold.add_argument("--name", default="terminal-effect", help="Name for your future feature")

    return parser


def handle_seed_demo(args: argparse.Namespace) -> int:
    preview = build_seed_preview(args.text)
    name = preview.generated_output["name"]
    rarity = preview.generated_output["rarity"]
    colored_rarity = colorize_rarity(rarity)
    if args.no_anim:
        print(f"Unlocked: {name} [{colored_rarity}]")
    else:
        play_drop_animation(item_name=name, rarity_text=colored_rarity)
        # time.sleep(0.5)
    return 0


def handle_input_demo(args: argparse.Namespace) -> int:
    payload = read_cli_input(args)
    print(f"[command] {payload}" if payload else "<empty-input>")
    return 0


def handle_split_demo(args: argparse.Namespace) -> int:
    print(json.dumps(shell_split(args.text), indent=2))
    return 0



def handle_scaffold_feature(args: argparse.Namespace) -> int:
    print(f"feature scaffold only: {args.name}")
    print("no implementation is included yet")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    handlers = {
        "seed-demo": handle_seed_demo,
        "input-demo": handle_input_demo,
        "split-demo": handle_split_demo,
        "scaffold-feature": handle_scaffold_feature,
    }

    return handlers[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
