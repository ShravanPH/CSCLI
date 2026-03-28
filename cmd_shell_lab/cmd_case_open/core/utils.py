from __future__ import annotations

import os

from .constants import ANSI_PATTERN, ANSI_RESET, RARITY_TO_COLOR


def rarity_key(rarity: str) -> str:
    return (rarity or "").split()[0].lower()


def rarity_label(key: str) -> str:
    labels = {
        "mil-spec": "Mil-Spec",
        "restricted": "Restricted",
        "classified": "Classified",
        "covert": "Covert",
        "extraordinary": "Extraordinary",
    }
    return labels.get(key, key.title())


def force_colorize_rarity(rarity: str) -> str:
    key = rarity_key(rarity)
    color = RARITY_TO_COLOR.get(key, "")
    if not color:
        return rarity
    return f"{color}{rarity}{ANSI_RESET}"


def colorize_rarity(rarity: str) -> str:
    if os.getenv("NO_COLOR") or not os.isatty(1):
        return rarity
    return force_colorize_rarity(rarity)


def visible_length(text: str) -> int:
    return len(ANSI_PATTERN.sub("", text))
