from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

from .core.constants import RARITY_ORDER
from .core.utils import colorize_rarity, force_colorize_rarity, rarity_key, rarity_label, visible_length


def _writable_state_dir() -> Path:
    candidates = (
        Path.home() / ".local" / "state" / "cmd_case_open",
        Path("/tmp/cmd_case_open_state"),
    )
    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            # Check folder writeability.
            probe = candidate / ".write_probe"
            with probe.open("a", encoding="utf-8"):
                pass
            probe.unlink(missing_ok=True)
            return candidate
        except OSError:
            continue
    raise OSError("No writable state directory available")


def inventory_path() -> Path:
    return _writable_state_dir() / "inventory.jsonl"


def write_inventory_entry(name: str, rarity: str) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "name": name,
        "rarity": rarity,
        "rarity_key": rarity_key(rarity),
        "rarity_colored": force_colorize_rarity(rarity),
    }

    path = inventory_path()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry))
        handle.write("\n")


def load_inventory_entries() -> list[dict[str, str]]:
    path = inventory_path()
    if not path.exists():
        return []

    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows.append(
                {
                    "name": str(payload.get("name", "Unknown Item")),
                    "rarity": str(payload.get("rarity", "Unknown")),
                    "rarity_key": str(payload.get("rarity_key", rarity_key(str(payload.get("rarity", ""))))),
                }
            )
    return rows


def print_table(headers: list[str], rows: list[list[str]]) -> None:
    if not rows:
        print("(no rows)")
        return

    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], visible_length(cell))

    divider = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    print(divider)
    print("| " + " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers))) + " |")
    print(divider)
    for row in rows:
        padded_cells: list[str] = []
        for i in range(len(headers)):
            cell = row[i]
            padded_cells.append(cell + (" " * max(0, widths[i] - visible_length(cell))))
        print("| " + " | ".join(padded_cells) + " |")
    print(divider)


def print_inventory_stats() -> int:
    entries = load_inventory_entries()
    if not entries:
        print("No inventory entries found yet.")
        print(f"Expected file: {inventory_path()}")
        return 0

    inventory_rows: list[list[str]] = []
    for index, entry in enumerate(entries, start=1):
        inventory_rows.append([str(index), entry["name"], colorize_rarity(entry["rarity"])])

    print("Inventory")
    print_table(["#", "Name", "Rarity"], inventory_rows)

    total = len(entries)
    counts = {key: 0 for key in RARITY_ORDER}
    for entry in entries:
        key = rarity_key(entry["rarity"])
        if key in counts:
            counts[key] += 1

    stat_rows: list[list[str]] = []
    for key in RARITY_ORDER:
        count = counts[key]
        percent = (count / total) * 100 if total else 0.0
        stat_rows.append([rarity_label(key), str(count), f"{percent:.2f}%"])

    print("\nStatistics")
    print(f"Cases opened: {total}")
    print_table(["Rarity", "Count", "Percent"], stat_rows)
    print(f"Inventory file: {inventory_path()}")
    return 0
