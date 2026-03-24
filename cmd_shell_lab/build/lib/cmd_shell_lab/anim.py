from __future__ import annotations

import os
import random
import shutil
import string
import sys
import time

GLITCH_CHARS = string.ascii_uppercase + string.digits + "!@#$%&*?"
ANSI_RESET = "\x1b[0m"
ANSI_GREEN = "\x1b[32m"


def _can_animate() -> bool:
    return sys.stdout.isatty() and not os.getenv("NO_COLOR")


def _frame_write(text: str) -> None:
    sys.stdout.write(f"\r\x1b[2K{text}")
    sys.stdout.flush()


def _random_block(width: int) -> str:
    return "".join(random.choice(GLITCH_CHARS) for _ in range(width))


def _terminal_width() -> int:
    return max(60, shutil.get_terminal_size(fallback=(100, 24)).columns)


def _pad_scramble_line(prefix: str, text: str, width: int) -> str:
    base = f"{prefix}{text}"
    remaining = width - len(base)
    if remaining <= 0:
        return base
    return base + _random_block(remaining)


def play_drop_animation(item_name: str, rarity_text: str) -> None:
    """Render a short glitch/reveal animation for a terminal drop."""
    if not _can_animate():
        print(f"Unlocked: {item_name} [{rarity_text}]")
        return

    width = _terminal_width()
    intro_frames = 10
    intro_delay = 0.012
    reveal_delay = 0.05

    for i in range(intro_frames):
        dots = "." * ((i % 3) + 1)
        intro_prefix = f"Scanning command entropy{dots} "
        intro_scramble = _pad_scramble_line(intro_prefix, "", width)
        _frame_write(f"{ANSI_GREEN}{intro_scramble}{ANSI_RESET}")
        time.sleep(intro_delay)

    for step in range(len(item_name) + 1):
        lock_count = step
        scrambled = "".join(
            item_name[index] if index < lock_count else random.choice(GLITCH_CHARS)
            for index in range(len(item_name))
        )
        reveal_prefix = "Unpacking drop: "
        reveal_line = _pad_scramble_line(reveal_prefix, scrambled, width)
        _frame_write(f"{ANSI_GREEN}{reveal_line}{ANSI_RESET}")
        time.sleep(reveal_delay)

    _frame_write(f"Unlocked: {item_name} [{rarity_text}]")
    sys.stdout.write("\n")
    sys.stdout.flush()
