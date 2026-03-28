from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
import json
import random
from typing import Any


@dataclass
class CaseOpenPreview:
    source_text: str
    generated_output: dict[str, Any]


def _load_case_data() -> list[dict[str, Any]]:
    data_pkg = resources.files("cmd_case_open.data")
    candidate = data_pkg.joinpath("spectrum-case.json")
    if candidate.is_file():
        with candidate.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    raise FileNotFoundError("Expected spectrum-case.json in cmd_case_open.data")


def build_case_open_preview(source_text: str) -> CaseOpenPreview:
    cases = _load_case_data()

    len_items = len(cases)
    rarity = "Covert"
    spectrum_rarity_sections = []
    for i in range(len_items):
        if rarity not in cases[i]["rarity"].split(" ")[0]:
            spectrum_rarity_sections.append(i)
            rarity = cases[i]["rarity"].split(" ")[0]

    spectrum_skins_sections = {
        "Mil-Spec": cases[spectrum_rarity_sections[2] : spectrum_rarity_sections[3]],
        "Restricted": cases[spectrum_rarity_sections[1] : spectrum_rarity_sections[2]],
        "Classified": cases[spectrum_rarity_sections[0] : spectrum_rarity_sections[1]],
        "Covert": cases[0 : spectrum_rarity_sections[0]],
        "Extraordinary": cases[spectrum_rarity_sections[3] : len_items],
    }

    items = ("Mil-Spec", "Restricted", "Classified", "Covert", "Extraordinary")
    weights = [800, 160, 32, 6, 2]

    selected_rarity = random.choices(items, weights=weights, k=1)[0]
    items_of_rarity = spectrum_skins_sections[selected_rarity]
    skin_selected = items_of_rarity[random.randrange(0, len(items_of_rarity))]

    return CaseOpenPreview(
        source_text=source_text,
        generated_output={
            "name": skin_selected.get("name", "Unknown Item"),
            "rarity": skin_selected.get("rarity", "Mil-spec"),
            "ascii": skin_selected.get("ascii", ""),
        },
    )
