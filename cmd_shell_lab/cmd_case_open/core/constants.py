from __future__ import annotations

import re

ANSI_RESET = "\x1b[0m"
BANNER_COLOR = "\x1b[38;2;255;255;255m"

RARITY_TO_COLOR = {
    "mil-spec": "\x1b[38;2;59;130;246m",
    "restricted": "\x1b[38;2;139;92;246m",
    "classified": "\x1b[38;2;236;72;153m",
    "covert": "\x1b[38;2;239;68;68m",
    "extraordinary": "\x1b[38;2;245;158;11m",
}

RARITY_ORDER = ("mil-spec", "restricted", "classified", "covert", "extraordinary")

TTE_EFFECT_POOL = (
    "blackhole",
    "burn",
    "decrypt",
    "middleout",
    "wipe",
    "slice",
    "smoke",
    "rain",
    "randomsequence",
    "beams",
)

ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")
