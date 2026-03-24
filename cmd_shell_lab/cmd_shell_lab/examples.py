"""Example-only building blocks for CLI experimentation.

This module intentionally avoids implementing any product feature logic.
It provides small reference snippets you can evolve quickly.
"""

from __future__ import annotations

import argparse
from importlib import resources
import random
import shlex
import sys
import json
from dataclasses import dataclass


@dataclass
class SeedPreview:
    """Demonstrates deterministic seeding from terminal input."""

    source_text: str
    generated_output: str


def build_seed_preview(source_text: str) -> SeedPreview:
    """Convert command text into a stable seed and sample random value."""
    data_file = resources.files("cmd_shell_lab.data").joinpath("spectrum-case.json")
    with data_file.open("r", encoding="utf-8") as f:
        cases = json.load(f)
    
    len_items = len(cases)
    rarity = "Covert"
    spectrum_rarity_sections = []
    for i in range(len_items):
        if rarity not in cases[i]["rarity"].split(" ")[0]:
            spectrum_rarity_sections.append(i)
            rarity = cases[i]["rarity"].split(" ")[0]
    spectrum_skins_sections = {
        "Mil-Spec":cases[spectrum_rarity_sections[2]:spectrum_rarity_sections[3]], #5
        "Restricted":cases[spectrum_rarity_sections[1]:spectrum_rarity_sections[2]], #4
        "Classified":cases[spectrum_rarity_sections[0]:spectrum_rarity_sections[1]], #3
        "Covert":cases[0:spectrum_rarity_sections[0]], #4
        "Extraordinary":cases[spectrum_rarity_sections[3]:len_items], #5
    }

    items = ["Mil-Spec", "Restricted", "Classified", "Covert", "Extraordinary"]
    weights = [800, 160, 32, 6, 2]

    choice = random.choices(items, weights=weights, k=1)[0]
    items_of_rarity = spectrum_skins_sections[choice]
    skin_idx = random.randrange(0,len(items_of_rarity))
    skin_selected = items_of_rarity[skin_idx]

    return SeedPreview(
        source_text=source_text,
        generated_output=skin_selected,
    )


def read_cli_input(args: argparse.Namespace) -> str:
    """Example: read input from args or stdin fallback."""
    if args.text:
        return args.text

    if not sys.stdin.isatty():
        piped = sys.stdin.read().strip()
        if piped:
            return piped

    return ""


def shell_split(command_text: str) -> list[str]:
    """Example: safely split command text as a shell would."""
    if not command_text.strip():
        return []
    return shlex.split(command_text)
