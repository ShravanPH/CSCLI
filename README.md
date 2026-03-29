# cmd_case_open

CLI for Counter Strike style case openings. 

## Quick start

```bash
cd cmd_case_open
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Open a new terminal after your shell requires you and run the following when triggered:

```bash
case-reveal 
case-reveal-stats # Track your stats
```
## Commands

```bash
cmd-case-open case-open 
cmd-case-open inventory-stats # Track your stats
```

## Storage

Inventory entries are appended to:

- `~/.local/state/cmd_case_open/inventory.jsonl`
- fallback: `/tmp/cmd_case_open_state/inventory.jsonl`

Each entry stores timestamp, name, rarity, rarity key, and a colorized rarity snapshot.

Shell hooks are auto-installed on first CLI run when possible depending on shell version.

Supported shell: 
   1. Zsh 
   2. Powershell

