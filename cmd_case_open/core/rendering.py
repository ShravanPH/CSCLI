from __future__ import annotations

import random
import shutil
import subprocess

from .constants import ANSI_RESET, BANNER_COLOR, RARITY_TO_COLOR, TTE_EFFECT_POOL
from .utils import colorize_rarity, rarity_key


def render_display_block(name: str, rarity: str, ascii_art: str) -> str:
    width = shutil.get_terminal_size(fallback=(120, 40)).columns
    width = max(80, width)
    rarity_color = RARITY_TO_COLOR.get(rarity_key(rarity), "\x1b[37m")

    border = f"{BANNER_COLOR}{'═' * width}{ANSI_RESET}"
    title = f" DROP UNLOCKED | {name} | {rarity} "
    title_line = f"{rarity_color}{title.center(width, '═')[:width]}{ANSI_RESET}"

    content_lines: list[str] = [border, title_line, border]
    if isinstance(ascii_art, list):
        raw_ascii = "\n".join(str(line) for line in ascii_art).strip("\n")
    else:
        raw_ascii = str(ascii_art or "").strip("\n")

    if raw_ascii:
        for ascii_line in raw_ascii.splitlines():
            centered = ascii_line[:width].center(width)
            content_lines.append(f"{rarity_color}{centered}{ANSI_RESET}")
    else:
        fallback = f"[ no ascii configured for {name} ]".center(width)
        content_lines.append(f"{rarity_color}{fallback}{ANSI_RESET}")

    content_lines.append(border)
    return "\n".join(content_lines)


def run_random_tte(display_block: str, timeout_seconds: float = 10.0) -> bool:
    selected_effect = random.choice(TTE_EFFECT_POOL)
    command = [
        "tte",
        "--frame-rate",
        "0",
        "--canvas-width",
        "0",
        "--existing-color-handling",
        "always",
        selected_effect,
    ]
    try:
        subprocess.run(
            command,
            input=display_block,
            text=True,
            check=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("expired 2")
        return False
    return True


def print_case_open_fallback(name: str, rarity: str, ascii_art: str) -> None:
    colored_rarity = colorize_rarity(rarity)
    print(f"Unlocked: {name} [{colored_rarity}]")
    if not ascii_art:
        return

    color = RARITY_TO_COLOR.get(rarity_key(rarity), "")
    reset = ANSI_RESET if color else ""
    if isinstance(ascii_art, list):
        fallback_ascii = "\n".join(str(line) for line in ascii_art)
    else:
        fallback_ascii = str(ascii_art)
    print(f"{color}{fallback_ascii}{reset}")
